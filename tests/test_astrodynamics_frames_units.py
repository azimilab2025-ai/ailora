from __future__ import annotations

import uuid
from datetime import UTC, datetime, timedelta, timezone

from ailora.services.astrodynamics.adapter import Sgp4Engine
from ailora.services.astrodynamics.config import AstrodynamicsConfig
from ailora.services.astrodynamics.models import (
    AstrodynamicsFrame,
    DistanceUnit,
    PropagationRequest,
    TLEInput,
    VelocityUnit,
)
from ailora.services.astrodynamics.service import AstrodynamicsService

LINE1 = "1 00005U 58002B   00179.78495062  .00000023  00000-0  28098-4 0  4753"
LINE2 = "2 00005  34.2682 348.7242 1859667 331.7664  19.3264 10.82419157413667"
EPOCH = datetime(2000, 6, 27, 18, 50, 19, 733568, tzinfo=UTC)


def propagate(target: datetime):
    request = PropagationRequest(
        uuid.uuid4(), TLEInput("VANGUARD 1", LINE1, LINE2), target, "advisory"
    )
    return AstrodynamicsService(AstrodynamicsConfig(), Sgp4Engine()).propagate(request)


def test_output_truthfully_labels_native_teme_and_units() -> None:
    result = propagate(EPOCH)
    assert result.frame is AstrodynamicsFrame.TEME
    assert result.distance_unit is DistanceUnit.KILOMETER
    assert result.velocity_unit is VelocityUnit.KILOMETER_PER_SECOND
    assert result.advisory_only is True


def test_equivalent_offset_instant_produces_same_state() -> None:
    offset = timezone(timedelta(hours=3, minutes=30))
    shifted = EPOCH.astimezone(offset)
    assert propagate(EPOCH).position_km == propagate(shifted).position_km


def test_no_gcrf_value_exists_in_native_frame_contract() -> None:
    assert {item.value for item in AstrodynamicsFrame} == {"TEME"}
