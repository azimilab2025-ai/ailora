from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AstrodynamicsConfig:
    max_days_from_tle_epoch: float = 14.0
    gravity_model: str = "WGS72"
    advisory_only: bool = True

    def __post_init__(self) -> None:
        if (
            not math.isfinite(self.max_days_from_tle_epoch)
            or not 0.0 < self.max_days_from_tle_epoch <= 30.0
        ):
            raise ValueError("max_days_from_tle_epoch must be within (0, 30]")
        if self.gravity_model != "WGS72":
            raise ValueError("only the TLE-standard WGS72 gravity model is supported")
        if self.advisory_only is not True:
            raise ValueError("astrodynamics results must remain advisory-only")
