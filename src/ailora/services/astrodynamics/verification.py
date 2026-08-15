from __future__ import annotations

import hashlib
import json
import math
import re
from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum

from ailora.services.astrodynamics.models import AstrodynamicsFrame, DistanceUnit, VelocityUnit
from ailora.services.astrodynamics.tca import TcaResult

Vector3 = tuple[float, float, float]
_DIGEST = re.compile(r"^[0-9a-f]{64}$")


class VerificationStatus(StrEnum):
    AGREEMENT_WITHIN_TOLERANCE = "AGREEMENT_WITHIN_TOLERANCE"
    MATERIAL_DISAGREEMENT_REVIEW_REQUIRED = "MATERIAL_DISAGREEMENT_REVIEW_REQUIRED"
    REFERENCE_UNAVAILABLE_REVIEW_REQUIRED = "REFERENCE_UNAVAILABLE_REVIEW_REQUIRED"


class VerificationErrorCode(StrEnum):
    INVALID_INPUT = "INVALID_INPUT"
    SAME_ENGINE_NOT_INDEPENDENT = "SAME_ENGINE_NOT_INDEPENDENT"
    SEMANTIC_MISMATCH = "SEMANTIC_MISMATCH"
    NONFINITE_RESULT = "NONFINITE_RESULT"
    DIGEST_MISMATCH = "DIGEST_MISMATCH"


class VerificationError(ValueError):
    def __init__(self, code: VerificationErrorCode, detail: str) -> None:
        super().__init__(detail.strip()[:256] or code.value)
        self.code = code


@dataclass(frozen=True, slots=True)
class VerificationTolerance:
    tca_time_seconds: float = 0.001
    miss_distance_km: float = 1e-6
    position_component_km: float = 1e-6
    velocity_component_km_s: float = 1e-9
    relative: float = 1e-12

    def __post_init__(self) -> None:
        values = (
            self.tca_time_seconds,
            self.miss_distance_km,
            self.position_component_km,
            self.velocity_component_km_s,
            self.relative,
        )
        if not all(math.isfinite(value) and value >= 0.0 for value in values):
            raise ValueError("verification tolerances must be finite and nonnegative")
        if not any(value > 0.0 for value in values):
            raise ValueError("at least one verification tolerance must be positive")


def reference_content_digest(
    *,
    reference_id: str,
    source_revision: str,
    engine_id: str,
    engine_version: str,
    independent_from_algorithm_id: str,
    tca_epoch: datetime,
    miss_distance_km: float,
    relative_position_km: Vector3,
    relative_velocity_km_s: Vector3,
) -> str:
    payload = {
        "engine_id": engine_id,
        "engine_version": engine_version,
        "independent_from_algorithm_id": independent_from_algorithm_id,
        "miss_distance_km": miss_distance_km,
        "reference_id": reference_id,
        "relative_position_km": relative_position_km,
        "relative_velocity_km_s": relative_velocity_km_s,
        "source_revision": source_revision,
        "tca_epoch": tca_epoch.astimezone(UTC).isoformat(),
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


@dataclass(frozen=True, slots=True)
class IndependentTcaReference:
    reference_id: str
    source_revision: str
    source_digest: str
    engine_id: str
    engine_version: str
    independent_from_algorithm_id: str
    tca_epoch: datetime
    miss_distance_km: float
    relative_position_km: Vector3
    relative_velocity_km_s: Vector3
    content_digest: str
    frame: AstrodynamicsFrame = AstrodynamicsFrame.TEME
    distance_unit: DistanceUnit = DistanceUnit.KILOMETER
    velocity_unit: VelocityUnit = VelocityUnit.KILOMETER_PER_SECOND
    time_scale: str = "UTC"

    def __post_init__(self) -> None:
        if not all(
            value.strip()
            for value in (
                self.reference_id,
                self.source_revision,
                self.engine_id,
                self.engine_version,
                self.independent_from_algorithm_id,
            )
        ):
            raise VerificationError(
                VerificationErrorCode.INVALID_INPUT, "reference identity is required"
            )
        if not _DIGEST.fullmatch(self.source_digest):
            raise VerificationError(VerificationErrorCode.INVALID_INPUT, "source digest is invalid")
        if self.tca_epoch.tzinfo is None or self.tca_epoch.utcoffset() is None:
            raise VerificationError(
                VerificationErrorCode.INVALID_INPUT, "reference epoch must be aware"
            )
        object.__setattr__(self, "tca_epoch", self.tca_epoch.astimezone(UTC))
        values = (self.miss_distance_km, *self.relative_position_km, *self.relative_velocity_km_s)
        if not all(math.isfinite(value) for value in values) or self.miss_distance_km < 0.0:
            raise VerificationError(
                VerificationErrorCode.NONFINITE_RESULT, "reference values are invalid"
            )
        expected = reference_content_digest(
            reference_id=self.reference_id,
            source_revision=self.source_revision,
            engine_id=self.engine_id,
            engine_version=self.engine_version,
            independent_from_algorithm_id=self.independent_from_algorithm_id,
            tca_epoch=self.tca_epoch,
            miss_distance_km=self.miss_distance_km,
            relative_position_km=self.relative_position_km,
            relative_velocity_km_s=self.relative_velocity_km_s,
        )
        if self.content_digest != expected:
            raise VerificationError(
                VerificationErrorCode.DIGEST_MISMATCH, "reference content digest mismatch"
            )


@dataclass(frozen=True, slots=True)
class DifferentialVerificationResult:
    status: VerificationStatus
    reference_id: str | None
    tca_time_delta_seconds: float | None
    miss_distance_delta_km: float | None
    position_component_delta_km: Vector3 | None
    velocity_component_delta_km_s: Vector3 | None
    tolerance_digest: str
    evidence_digest: str
    limitations: tuple[str, ...]
    collision_probability: None = None
    advisory_only: bool = True
    independent_scientific_approval: str = "EXTERNAL_GATE_NOT_SELF_ISSUED"


def _tolerance_digest(tolerance: VerificationTolerance) -> str:
    payload = {
        "miss_distance_km": tolerance.miss_distance_km,
        "position_component_km": tolerance.position_component_km,
        "relative": tolerance.relative,
        "tca_time_seconds": tolerance.tca_time_seconds,
        "velocity_component_km_s": tolerance.velocity_component_km_s,
    }
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def _within(actual: float, expected: float, absolute: float, relative: float) -> bool:
    return abs(actual - expected) <= absolute + relative * max(abs(actual), abs(expected))


def verify_tca_result(
    primary: TcaResult,
    reference: IndependentTcaReference | None,
    tolerance: VerificationTolerance,
) -> DifferentialVerificationResult:
    tolerance_digest = _tolerance_digest(tolerance)
    limitations = (
        "ADVISORY_ONLY",
        "COLLISION_PROBABILITY_NOT_COMPUTED",
        "INDEPENDENT_SCIENTIFIC_APPROVAL_REMAINS_EXTERNAL",
    )
    if reference is None:
        evidence = hashlib.sha256(
            f"{primary.input_digest}:{tolerance_digest}:REFERENCE_UNAVAILABLE".encode()
        ).hexdigest()
        return DifferentialVerificationResult(
            status=VerificationStatus.REFERENCE_UNAVAILABLE_REVIEW_REQUIRED,
            reference_id=None,
            tca_time_delta_seconds=None,
            miss_distance_delta_km=None,
            position_component_delta_km=None,
            velocity_component_delta_km_s=None,
            tolerance_digest=tolerance_digest,
            evidence_digest=evidence,
            limitations=limitations + ("REFERENCE_UNAVAILABLE",),
        )
    if reference.engine_id == primary.propagator_algorithm_id:
        raise VerificationError(
            VerificationErrorCode.SAME_ENGINE_NOT_INDEPENDENT,
            "reference engine must differ from the primary propagator",
        )
    if reference.independent_from_algorithm_id != primary.propagator_algorithm_id:
        raise VerificationError(
            VerificationErrorCode.SAME_ENGINE_NOT_INDEPENDENT,
            "reference independence declaration does not match the primary propagator",
        )
    if (
        reference.frame is not primary.frame
        or reference.distance_unit is not primary.distance_unit
        or reference.velocity_unit is not primary.velocity_unit
        or reference.time_scale != "UTC"
    ):
        raise VerificationError(
            VerificationErrorCode.SEMANTIC_MISMATCH, "reference semantics differ"
        )
    time_delta = abs((primary.tca_epoch - reference.tca_epoch).total_seconds())
    miss_delta = abs(primary.miss_distance_km - reference.miss_distance_km)
    position_delta: Vector3 = (
        abs(primary.relative_position_km[0] - reference.relative_position_km[0]),
        abs(primary.relative_position_km[1] - reference.relative_position_km[1]),
        abs(primary.relative_position_km[2] - reference.relative_position_km[2]),
    )
    velocity_delta: Vector3 = (
        abs(primary.relative_velocity_km_s[0] - reference.relative_velocity_km_s[0]),
        abs(primary.relative_velocity_km_s[1] - reference.relative_velocity_km_s[1]),
        abs(primary.relative_velocity_km_s[2] - reference.relative_velocity_km_s[2]),
    )
    checks = [
        _within(time_delta, 0.0, tolerance.tca_time_seconds, 0.0),
        _within(
            primary.miss_distance_km,
            reference.miss_distance_km,
            tolerance.miss_distance_km,
            tolerance.relative,
        ),
    ]
    checks.extend(
        _within(
            primary.relative_position_km[index],
            reference.relative_position_km[index],
            tolerance.position_component_km,
            tolerance.relative,
        )
        for index in range(3)
    )
    checks.extend(
        _within(
            primary.relative_velocity_km_s[index],
            reference.relative_velocity_km_s[index],
            tolerance.velocity_component_km_s,
            tolerance.relative,
        )
        for index in range(3)
    )
    status = (
        VerificationStatus.AGREEMENT_WITHIN_TOLERANCE
        if all(checks)
        else VerificationStatus.MATERIAL_DISAGREEMENT_REVIEW_REQUIRED
    )
    evidence_payload = {
        "primary_configuration_digest": primary.configuration_digest,
        "primary_input_digest": primary.input_digest,
        "reference_content_digest": reference.content_digest,
        "reference_source_digest": reference.source_digest,
        "status": status.value,
        "tolerance_digest": tolerance_digest,
    }
    evidence = hashlib.sha256(
        json.dumps(evidence_payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    return DifferentialVerificationResult(
        status=status,
        reference_id=reference.reference_id,
        tca_time_delta_seconds=time_delta,
        miss_distance_delta_km=miss_delta,
        position_component_delta_km=position_delta,
        velocity_component_delta_km_s=velocity_delta,
        tolerance_digest=tolerance_digest,
        evidence_digest=evidence,
        limitations=limitations,
    )
