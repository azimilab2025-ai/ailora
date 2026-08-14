from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Protocol

from ailora.services.astrodynamics.models import TLEInput

Vector3 = tuple[float, float, float]


class AstrodynamicsErrorCode(StrEnum):
    INVALID_INPUT = "INVALID_INPUT"
    UNSUPPORTED_TIME = "UNSUPPORTED_TIME"
    UNSUPPORTED_FRAME = "UNSUPPORTED_FRAME"
    OUT_OF_DOMAIN = "OUT_OF_DOMAIN"
    MODEL_ERROR = "MODEL_ERROR"
    NONFINITE_OUTPUT = "NONFINITE_OUTPUT"
    DEPENDENCY_ERROR = "DEPENDENCY_ERROR"


class AstrodynamicsError(RuntimeError):
    def __init__(self, code: AstrodynamicsErrorCode, detail: str) -> None:
        safe_detail = detail.strip()[:256] or code.value
        super().__init__(safe_detail)
        self.code = code


@dataclass(frozen=True, slots=True)
class EngineOutput:
    error_code: int
    position_km: Vector3
    velocity_km_s: Vector3
    detail: str


class PreparedPropagator(Protocol):
    @property
    def tle_epoch_julian_date(self) -> float: ...

    @property
    def model_version(self) -> str: ...

    def propagate(self, julian_day: float, fraction: float) -> EngineOutput: ...


class AstrodynamicsEngine(Protocol):
    @property
    def algorithm_id(self) -> str: ...

    def prepare(self, tle: TLEInput) -> PreparedPropagator: ...
