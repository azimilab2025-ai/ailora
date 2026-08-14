from __future__ import annotations

import math
import uuid
from datetime import UTC, datetime, timedelta

import pytest

from ailora.services.astrodynamics.config import AstrodynamicsConfig
from ailora.services.astrodynamics.interfaces import (
    AstrodynamicsEngine,
    AstrodynamicsError,
    AstrodynamicsErrorCode,
    EngineOutput,
    PreparedPropagator,
)
from ailora.services.astrodynamics.models import PropagationRequest, TLEInput
from ailora.services.astrodynamics.service import AstrodynamicsService

LINE1 = "1 00005U 58002B   00179.78495062  .00000023  00000-0  28098-4 0  4753"
LINE2 = "2 00005  34.2682 348.7242 1859667 331.7664  19.3264 10.82419157413667"
EPOCH = datetime(2000, 6, 27, 18, 50, 19, 733568, tzinfo=UTC)


class FakePrepared(PreparedPropagator):
    def __init__(self, output: EngineOutput) -> None:
        self._output = output

    @property
    def tle_epoch_julian_date(self) -> float:
        return 2_451_723.28495062

    @property
    def model_version(self) -> str:
        return "test"

    def propagate(self, julian_day: float, fraction: float) -> EngineOutput:
        del julian_day, fraction
        return self._output


class FakeEngine(AstrodynamicsEngine):
    def __init__(self, output: EngineOutput) -> None:
        self.output = output

    @property
    def algorithm_id(self) -> str:
        return "SGP4"

    def prepare(self, tle: TLEInput) -> PreparedPropagator:
        del tle
        return FakePrepared(self.output)


def request(target: datetime = EPOCH) -> PropagationRequest:
    return PropagationRequest(
        uuid.uuid4(), TLEInput("VANGUARD 1", LINE1, LINE2), target, "advisory"
    )


def test_out_of_domain_epoch_fails_before_model_call() -> None:
    output = EngineOutput(0, (1.0, 2.0, 3.0), (4.0, 5.0, 6.0), "ok")
    service = AstrodynamicsService(AstrodynamicsConfig(), FakeEngine(output))
    with pytest.raises(AstrodynamicsError) as captured:
        service.propagate(request(EPOCH + timedelta(days=15)))
    assert captured.value.code is AstrodynamicsErrorCode.OUT_OF_DOMAIN


def test_model_error_is_typed_and_payload_safe() -> None:
    output = EngineOutput(6, (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), "decayed")
    service = AstrodynamicsService(AstrodynamicsConfig(), FakeEngine(output))
    with pytest.raises(AstrodynamicsError) as captured:
        service.propagate(request())
    assert captured.value.code is AstrodynamicsErrorCode.MODEL_ERROR
    assert LINE1 not in str(captured.value)


def test_nonfinite_model_output_fails_closed() -> None:
    output = EngineOutput(0, (math.nan, 2.0, 3.0), (4.0, 5.0, 6.0), "ok")
    service = AstrodynamicsService(AstrodynamicsConfig(), FakeEngine(output))
    with pytest.raises(AstrodynamicsError) as captured:
        service.propagate(request())
    assert captured.value.code is AstrodynamicsErrorCode.NONFINITE_OUTPUT
