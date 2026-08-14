from __future__ import annotations

import uuid
from datetime import UTC, datetime

import pytest

from ailora.services.astrodynamics.adapter import Sgp4Engine
from ailora.services.astrodynamics.config import AstrodynamicsConfig
from ailora.services.astrodynamics.models import PropagationRequest, TLEInput
from ailora.services.astrodynamics.service import AstrodynamicsService

LINE1 = "1 00005U 58002B   00179.78495062  .00000023  00000-0  28098-4 0  4753"
LINE2 = "2 00005  34.2682 348.7242 1859667 331.7664  19.3264 10.82419157413667"
EPOCH = datetime(2000, 6, 27, 18, 50, 19, 733568, tzinfo=UTC)


def request() -> PropagationRequest:
    return PropagationRequest(
        uuid.UUID("12345678-1234-5678-1234-567812345678"),
        TLEInput("VANGUARD 1", LINE1, LINE2),
        EPOCH,
        "golden verification",
    )


def test_vallado_golden_vector_at_tle_epoch() -> None:
    # Official SGP4-VER.TLE case 00005 paired with tcppver.out at tsince=0.
    result = AstrodynamicsService(AstrodynamicsConfig(), Sgp4Engine()).propagate(request())
    assert result.position_km == pytest.approx(
        (7022.46529266, -1400.08296755, 0.03995155), abs=2e-6
    )
    assert result.velocity_km_s == pytest.approx((1.893841015, 6.405893759, 4.534807250), abs=2e-9)


def test_repeated_propagation_is_deterministic() -> None:
    service = AstrodynamicsService(AstrodynamicsConfig(), Sgp4Engine())
    first = service.propagate(request())
    second = service.propagate(request())
    assert first == second
    assert len(first.input_digest) == 64
    assert len(first.configuration_digest) == 64
