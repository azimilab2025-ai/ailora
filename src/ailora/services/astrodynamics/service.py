from __future__ import annotations

import hashlib
import json
import math
from datetime import datetime

from sgp4.api import jday

from ailora.services.astrodynamics.config import AstrodynamicsConfig
from ailora.services.astrodynamics.interfaces import (
    AstrodynamicsEngine,
    AstrodynamicsError,
    AstrodynamicsErrorCode,
)
from ailora.services.astrodynamics.models import (
    AstrodynamicsFrame,
    DistanceUnit,
    PropagationRequest,
    PropagationResult,
    VelocityUnit,
)


def _julian_parts(value: datetime) -> tuple[float, float]:
    seconds = value.second + value.microsecond / 1_000_000.0
    julian_day, fraction = jday(
        value.year, value.month, value.day, value.hour, value.minute, seconds
    )
    return float(julian_day), float(fraction)


def _digest(payload: dict[str, object]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode(
        "utf-8"
    )
    return hashlib.sha256(encoded).hexdigest()


class AstrodynamicsService:
    def __init__(self, config: AstrodynamicsConfig, engine: AstrodynamicsEngine) -> None:
        self._config = config
        self._engine = engine

    def propagate(self, request: PropagationRequest) -> PropagationResult:
        prepared = self._engine.prepare(request.tle)
        julian_day, fraction = _julian_parts(request.target_epoch)
        target_julian_date = julian_day + fraction
        delta_days = abs(target_julian_date - prepared.tle_epoch_julian_date)
        if delta_days > self._config.max_days_from_tle_epoch:
            raise AstrodynamicsError(
                AstrodynamicsErrorCode.OUT_OF_DOMAIN,
                "target epoch is outside the configured TLE validity window",
            )
        output = prepared.propagate(julian_day, fraction)
        if output.error_code != 0:
            raise AstrodynamicsError(
                AstrodynamicsErrorCode.MODEL_ERROR,
                f"SGP4 model error {output.error_code}: {output.detail}",
            )
        values = (*output.position_km, *output.velocity_km_s)
        if not all(math.isfinite(value) for value in values):
            raise AstrodynamicsError(
                AstrodynamicsErrorCode.NONFINITE_OUTPUT,
                "SGP4 returned a nonfinite state vector",
            )
        input_digest = _digest(
            {
                "line1": request.tle.line1,
                "line2": request.tle.line2,
                "target_epoch": request.target_epoch.isoformat(),
            }
        )
        configuration_digest = _digest(
            {
                "advisory_only": self._config.advisory_only,
                "gravity_model": self._config.gravity_model,
                "max_days_from_tle_epoch": self._config.max_days_from_tle_epoch,
            }
        )
        return PropagationResult(
            request_id=request.request_id,
            target_epoch=request.target_epoch,
            tle_epoch_julian_date=prepared.tle_epoch_julian_date,
            position_km=output.position_km,
            velocity_km_s=output.velocity_km_s,
            frame=AstrodynamicsFrame.TEME,
            distance_unit=DistanceUnit.KILOMETER,
            velocity_unit=VelocityUnit.KILOMETER_PER_SECOND,
            algorithm_id=self._engine.algorithm_id,
            algorithm_version=prepared.model_version,
            input_digest=input_digest,
            configuration_digest=configuration_digest,
            advisory_only=True,
        )
