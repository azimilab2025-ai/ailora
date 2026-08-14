from __future__ import annotations

import math
import re
import uuid
from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum

from ailora.domain.ssa.tle_parser import parse_tle

_DIGEST = re.compile(r"^[0-9a-f]{64}$")


class AstrodynamicsFrame(StrEnum):
    TEME = "TEME"


class DistanceUnit(StrEnum):
    KILOMETER = "km"


class VelocityUnit(StrEnum):
    KILOMETER_PER_SECOND = "km/s"


@dataclass(frozen=True, slots=True)
class TLEInput:
    name: str
    line1: str
    line2: str

    def __post_init__(self) -> None:
        if not self.name.strip() or len(self.name) > 128:
            raise ValueError("TLE name is invalid")
        try:
            parse_tle(self.name, self.line1, self.line2)
        except ValueError as exc:
            raise ValueError("TLE is invalid") from exc


@dataclass(frozen=True, slots=True)
class PropagationRequest:
    request_id: uuid.UUID
    tle: TLEInput
    target_epoch: datetime
    purpose: str

    def __post_init__(self) -> None:
        if self.target_epoch.tzinfo is None or self.target_epoch.utcoffset() is None:
            raise ValueError("target_epoch must be timezone-aware")
        if not self.purpose.strip() or len(self.purpose) > 256:
            raise ValueError("purpose is invalid")
        object.__setattr__(self, "target_epoch", self.target_epoch.astimezone(UTC))


@dataclass(frozen=True, slots=True)
class PropagationResult:
    request_id: uuid.UUID
    target_epoch: datetime
    tle_epoch_julian_date: float
    position_km: tuple[float, float, float]
    velocity_km_s: tuple[float, float, float]
    frame: AstrodynamicsFrame
    distance_unit: DistanceUnit
    velocity_unit: VelocityUnit
    algorithm_id: str
    algorithm_version: str
    input_digest: str
    configuration_digest: str
    advisory_only: bool

    def __post_init__(self) -> None:
        if len(self.position_km) != 3 or len(self.velocity_km_s) != 3:
            raise ValueError("propagation vectors must have exactly three components")
        values = (*self.position_km, *self.velocity_km_s, self.tle_epoch_julian_date)
        if not all(math.isfinite(value) for value in values):
            raise ValueError("propagation result must contain finite values")
        if self.target_epoch.tzinfo is None or self.target_epoch.utcoffset() is None:
            raise ValueError("target_epoch must be timezone-aware")
        if self.frame is not AstrodynamicsFrame.TEME:
            raise ValueError("native SGP4 results must remain TEME")
        if not _DIGEST.fullmatch(self.input_digest):
            raise ValueError("input_digest must be a lowercase SHA-256 digest")
        if not _DIGEST.fullmatch(self.configuration_digest):
            raise ValueError("configuration_digest must be a lowercase SHA-256 digest")
        if self.advisory_only is not True:
            raise ValueError("propagation result must remain advisory-only")
