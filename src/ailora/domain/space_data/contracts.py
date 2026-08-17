from __future__ import annotations

import hashlib
import json
import math
import re
import uuid
from datetime import UTC, datetime
from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, ValidationInfo, field_validator, model_validator

_IDENTIFIER = re.compile(r"^[A-Z0-9._:-]{1,128}$")
_DIGEST = re.compile(r"^[0-9a-f]{64}$")
_FUTURE_TOLERANCE_SECONDS = 5.0


class SchemaVersion(StrEnum):
    V1 = "1.0"


class ReferenceFrame(StrEnum):
    GCRF = "GCRF"
    TEME = "TEME"


class DistanceUnit(StrEnum):
    KILOMETER = "km"


class VelocityUnit(StrEnum):
    KILOMETER_PER_SECOND = "km/s"


class TimeScale(StrEnum):
    UTC = "UTC"


class DataQuality(StrEnum):
    VALID = "VALID"
    QUARANTINED = "QUARANTINED"
    REJECTED = "REJECTED"


class SpaceDataClassification(StrEnum):
    PUBLIC = "PUBLIC"
    INTERNAL = "INTERNAL"
    CONFIDENTIAL = "CONFIDENTIAL"
    RESTRICTED = "RESTRICTED"


def _json_default(value: object) -> str:
    if isinstance(value, datetime):
        return value.astimezone(UTC).isoformat()
    if isinstance(value, uuid.UUID):
        return str(value)
    if isinstance(value, StrEnum):
        return value.value
    raise TypeError(f"unsupported canonical value: {type(value).__name__}")


def _canonicalize(value: object, key: str | None = None) -> object:
    if isinstance(value, dict):
        return {
            str(item_key): _canonicalize(item_value, str(item_key))
            for item_key, item_value in value.items()
            if item_key != "canonical_digest"
        }
    if isinstance(value, (list, tuple)):
        return [_canonicalize(item) for item in value]
    if isinstance(value, datetime):
        return _aware_utc(value, key or "datetime").isoformat()
    if isinstance(value, uuid.UUID):
        return str(value)
    if isinstance(value, StrEnum):
        return value.value
    if isinstance(value, float) and not math.isfinite(value):
        if math.isnan(value):
            return "NaN"
        return "Infinity" if value > 0 else "-Infinity"
    if isinstance(value, str):
        if key in {"epoch", "evaluated_at", "ingested_at"}:
            try:
                parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
            except ValueError:
                return value
            if parsed.tzinfo is None or parsed.utcoffset() is None:
                return value
            return parsed.astimezone(UTC).isoformat()
        if key in {"observation_id", "object_id"}:
            return value.strip().upper()
        if key in {"source_id", "source_version"}:
            return value.strip()
        if key == "tenant_id":
            try:
                return str(uuid.UUID(value))
            except ValueError:
                return value
    return value


def canonical_payload_digest(payload: dict[str, object]) -> str:
    normalized = _canonicalize(payload)
    encoded = json.dumps(
        normalized,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _aware_utc(value: datetime, field_name: str) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{field_name} must be timezone-aware")
    return value.astimezone(UTC)


def _finite_vector(
    value: tuple[float, float, float], field_name: str
) -> tuple[float, float, float]:
    if not all(math.isfinite(component) for component in value):
        raise ValueError(f"{field_name} components must be finite")
    return value


class Provenance(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    source_id: str = Field(min_length=1, max_length=128)
    source_version: str = Field(min_length=1, max_length=128)
    ingested_at: datetime
    canonical_digest: str
    classification: SpaceDataClassification

    @field_validator("source_id", "source_version")
    @classmethod
    def strip_text(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("provenance identifiers must not be blank")
        return cleaned

    @field_validator("ingested_at")
    @classmethod
    def normalize_ingested_at(cls, value: datetime) -> datetime:
        return _aware_utc(value, "ingested_at")

    @field_validator("canonical_digest")
    @classmethod
    def validate_digest(cls, value: str) -> str:
        lowered = value.lower()
        if not _DIGEST.fullmatch(lowered):
            raise ValueError("canonical_digest must be a SHA-256 hex digest")
        return lowered


class ObservationEnvelope(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    processing_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    tenant_id: uuid.UUID
    observation_id: str
    object_id: str
    schema_version: SchemaVersion
    reference_frame: ReferenceFrame
    distance_unit: DistanceUnit
    velocity_unit: VelocityUnit
    time_scale: TimeScale
    epoch: datetime
    evaluated_at: datetime
    max_age_seconds: float = Field(ge=0.0, le=31_536_000.0)
    position: tuple[float, float, float]
    velocity: tuple[float, float, float]
    covariance: tuple[tuple[float, ...], ...] | None = None
    quality: Literal[DataQuality.VALID] = DataQuality.VALID
    provenance: Provenance
    advisory_only: Literal[True] = True

    @field_validator("observation_id", "object_id")
    @classmethod
    def normalize_identifier(cls, value: str) -> str:
        normalized = value.strip().upper()
        if not _IDENTIFIER.fullmatch(normalized):
            raise ValueError("identifier contains unsupported characters or length")
        return normalized

    @field_validator("epoch", "evaluated_at")
    @classmethod
    def normalize_datetime(cls, value: datetime, info: ValidationInfo) -> datetime:
        return _aware_utc(value, info.field_name or "datetime")

    @field_validator("position", "velocity")
    @classmethod
    def validate_vector(
        cls, value: tuple[float, float, float], info: ValidationInfo
    ) -> tuple[float, float, float]:
        return _finite_vector(value, info.field_name or "vector")

    @field_validator("covariance")
    @classmethod
    def validate_covariance(
        cls, value: tuple[tuple[float, ...], ...] | None
    ) -> tuple[tuple[float, ...], ...] | None:
        if value is None:
            return None
        if len(value) != 6 or any(len(row) != 6 for row in value):
            raise ValueError("covariance must be 6x6")
        if not all(math.isfinite(component) for row in value for component in row):
            raise ValueError("covariance components must be finite")
        return value

    @model_validator(mode="after")
    def validate_semantics(self) -> ObservationEnvelope:
        delta = (self.evaluated_at - self.epoch).total_seconds()
        if delta < -_FUTURE_TOLERANCE_SECONDS:
            raise ValueError("epoch exceeds future tolerance")
        if delta > self.max_age_seconds:
            raise ValueError("observation is stale")
        actual_digest = canonical_payload_digest(
            self.model_dump(mode="json", exclude={"processing_id"})
        )
        if actual_digest != self.provenance.canonical_digest:
            raise ValueError("canonical digest mismatch")
        return self

    @property
    def is_fresh(self) -> bool:
        return (self.evaluated_at - self.epoch).total_seconds() <= self.max_age_seconds
