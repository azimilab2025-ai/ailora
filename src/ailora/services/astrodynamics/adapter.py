from __future__ import annotations

import importlib.metadata
from collections.abc import Sequence
from typing import Protocol, cast

from sgp4.api import SGP4_ERRORS, WGS72, Satrec

from ailora.services.astrodynamics.interfaces import (
    AstrodynamicsEngine,
    AstrodynamicsError,
    AstrodynamicsErrorCode,
    EngineOutput,
    PreparedPropagator,
)
from ailora.services.astrodynamics.models import TLEInput


class _Satellite(Protocol):
    jdsatepoch: float
    jdsatepochF: float  # noqa: N815 - exact third-party SGP4 API attribute

    def sgp4(
        self, julian_day: float, fraction: float
    ) -> tuple[int, Sequence[float], Sequence[float]]: ...


class _Sgp4Prepared(PreparedPropagator):
    def __init__(self, satellite: _Satellite, model_version: str) -> None:
        self._satellite = satellite
        self._model_version = model_version

    @property
    def tle_epoch_julian_date(self) -> float:
        return float(self._satellite.jdsatepoch) + float(self._satellite.jdsatepochF)

    @property
    def model_version(self) -> str:
        return self._model_version

    def propagate(self, julian_day: float, fraction: float) -> EngineOutput:
        raw_code, raw_position, raw_velocity = self._satellite.sgp4(julian_day, fraction)
        code = int(raw_code)
        position = tuple(float(value) for value in raw_position)
        velocity = tuple(float(value) for value in raw_velocity)
        if len(position) != 3 or len(velocity) != 3:
            raise AstrodynamicsError(
                AstrodynamicsErrorCode.DEPENDENCY_ERROR,
                "SGP4 returned a vector with invalid dimensions",
            )
        detail = str(SGP4_ERRORS.get(code, "unknown SGP4 model error"))
        return EngineOutput(
            code,
            (position[0], position[1], position[2]),
            (velocity[0], velocity[1], velocity[2]),
            detail,
        )


class Sgp4Engine(AstrodynamicsEngine):
    @property
    def algorithm_id(self) -> str:
        return "SGP4"

    def prepare(self, tle: TLEInput) -> PreparedPropagator:
        try:
            satellite = cast(_Satellite, Satrec.twoline2rv(tle.line1, tle.line2, WGS72))
        except (TypeError, ValueError) as exc:
            raise AstrodynamicsError(
                AstrodynamicsErrorCode.INVALID_INPUT, "SGP4 rejected the TLE"
            ) from exc
        version = importlib.metadata.version("sgp4")
        return _Sgp4Prepared(satellite, version)
