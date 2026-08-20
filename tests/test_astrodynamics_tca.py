from __future__ import annotations

import uuid
from datetime import UTC, datetime, timedelta

import pytest

from ailora.services.astrodynamics.adapter import Sgp4Engine
from ailora.services.astrodynamics.config import AstrodynamicsConfig
from ailora.services.astrodynamics.models import (
    AstrodynamicsFrame,
    DistanceUnit,
    PropagationRequest,
    PropagationResult,
    TLEInput,
    VelocityUnit,
)
from ailora.services.astrodynamics.service import AstrodynamicsService
from ailora.services.astrodynamics.tca import (
    TcaAnalyzer,
    TcaConvergenceStatus,
    TcaSearchConfig,
    TcaSearchRequest,
)

LINE1 = "1 00005U 58002B   00179.78495062  .00000023  00000-0  28098-4 0  4753"
LINE2 = "2 00005  34.2682 348.7242 1859667 331.7664  19.3264 10.82419157413667"
SECONDARY_LINE2 = "2 00005  34.2682 348.7242 1859667 331.7664  20.3264 10.82419157413669"
EPOCH = datetime(2000, 6, 27, 18, 50, 19, 733568, tzinfo=UTC)


class LinearPropagation:
    def __init__(self, origin: datetime) -> None:
        self.origin = origin

    def propagate(self, request: PropagationRequest) -> PropagationResult:
        seconds = (request.target_epoch - self.origin).total_seconds()
        if request.tle.name == "PRIMARY":
            position = (seconds - 5.0, 1.0, 0.0)
            velocity = (1.0, 0.0, 0.0)
        else:
            position = (0.0, 0.0, 0.0)
            velocity = (0.0, 0.0, 0.0)
        return PropagationResult(
            request.request_id,
            request.target_epoch,
            2_451_723.0,
            position,
            velocity,
            AstrodynamicsFrame.TEME,
            DistanceUnit.KILOMETER,
            VelocityUnit.KILOMETER_PER_SECOND,
            "LINEAR_TEST_DOUBLE",
            "1.0",
            "a" * 64,
            "b" * 64,
            True,
        )


def tle(name: str) -> TLEInput:
    line2 = SECONDARY_LINE2 if name == "VANGUARD SECONDARY" else LINE2
    return TLEInput(name, LINE1, line2)


def search_request(start: datetime = EPOCH, duration: float = 10.0) -> TcaSearchRequest:
    return TcaSearchRequest(
        uuid.UUID("11111111-2222-3333-4444-555555555555"),
        tle("PRIMARY"),
        tle("SECONDARY"),
        start,
        start + timedelta(seconds=duration),
        "bounded conjunction analysis",
    )


def test_linear_crossing_has_known_bounded_tca_and_is_deterministic() -> None:
    analyzer = TcaAnalyzer(
        LinearPropagation(EPOCH),  # type: ignore[arg-type]
        TcaSearchConfig(coarse_intervals=20),
    )
    first = analyzer.find(search_request())
    second = analyzer.find(search_request())
    assert first == second
    assert abs((first.tca_epoch - (EPOCH + timedelta(seconds=5))).total_seconds()) <= 0.001
    assert first.miss_distance_km == pytest.approx(1.0, abs=1e-12)
    assert first.relative_velocity_km_s == (1.0, 0.0, 0.0)
    assert first.status is TcaConvergenceStatus.CONVERGED
    assert first.frame is AstrodynamicsFrame.TEME
    assert first.advisory_only is True


def test_endpoint_minimum_uses_earliest_epoch() -> None:
    request = search_request(start=EPOCH + timedelta(seconds=5), duration=5.0)
    result = TcaAnalyzer(
        LinearPropagation(EPOCH),  # type: ignore[arg-type]
        TcaSearchConfig(coarse_intervals=20),
    ).find(request)
    assert result.tca_epoch == request.search_start
    assert result.status is TcaConvergenceStatus.ENDPOINT_MINIMUM


def test_fixed_sgp4_pair_is_deterministic_and_native_teme() -> None:
    service = AstrodynamicsService(AstrodynamicsConfig(), Sgp4Engine())
    request = TcaSearchRequest(
        uuid.UUID("aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"),
        tle("VANGUARD PRIMARY"),
        tle("VANGUARD SECONDARY"),
        EPOCH,
        EPOCH + timedelta(seconds=60),
        "fixed SGP4 pair verification",
    )
    analyzer = TcaAnalyzer(service, TcaSearchConfig(coarse_intervals=12))
    first = analyzer.find(request)
    second = analyzer.find(request)
    assert first == second
    assert first.tca_epoch == EPOCH + timedelta(seconds=60)
    assert first.status is TcaConvergenceStatus.ENDPOINT_MINIMUM
    assert first.miss_distance_km == pytest.approx(177.96354279336228, abs=2e-9)
    assert first.frame is AstrodynamicsFrame.TEME
    assert first.algorithm_id == "BOUNDED_TCA_SEARCH"


def test_request_and_config_reject_invalid_windows_and_bounds() -> None:
    with pytest.raises(ValueError, match="after"):
        search_request(duration=0.0)
    with pytest.raises(ValueError, match="timezone-aware"):
        search_request(start=EPOCH.replace(tzinfo=None))
    with pytest.raises(ValueError, match="coarse_intervals"):
        TcaSearchConfig(coarse_intervals=3)
    with pytest.raises(ValueError, match="max_evaluations"):
        TcaSearchConfig(coarse_intervals=48, max_evaluations=50)


# --- COMMAND 24 / ENT-017 additions ---


def test_encounter_geometry_accepts_valid() -> None:
    from ailora.services.astrodynamics.tca import EncounterGeometry

    g = EncounterGeometry(
        relative_position_rtn=(100.0, 0.0, 0.0),
        relative_velocity_rtn=(0.0, 1.0, 0.0),
        miss_distance_m=100.0,
    )
    assert g.miss_distance_m == 100.0


def test_encounter_geometry_rejects_nonfinite() -> None:
    from ailora.services.astrodynamics.tca import EncounterGeometry, TcaAnalysisError

    with pytest.raises(TcaAnalysisError):
        EncounterGeometry(
            relative_position_rtn=(float("nan"), 0.0, 0.0),
            relative_velocity_rtn=(0.0, 1.0, 0.0),
            miss_distance_m=100.0,
        )


def test_hard_body_radius_record_accepts_valid() -> None:
    from ailora.services.astrodynamics.tca import HardBodyRadiusRecord

    r = HardBodyRadiusRecord(
        object_id="OBJ-1",
        radius_m=5.0,
        source_class="CATALOG",
        evidence_digest="a" * 64,
    )
    assert r.radius_m == 5.0


def test_hard_body_radius_record_rejects_nonpositive() -> None:
    from ailora.services.astrodynamics.tca import HardBodyRadiusRecord, TcaAnalysisError

    with pytest.raises(TcaAnalysisError):
        HardBodyRadiusRecord(
            object_id="OBJ-1",
            radius_m=0.0,
            source_class="CATALOG",
            evidence_digest="a" * 64,
        )


def test_validity_domain_gate_accepts_valid() -> None:
    from ailora.services.astrodynamics.tca import ValidityDomainGate

    gate = ValidityDomainGate(
        domain_id="DOM-1",
        regime="NOMINAL",
        accepted=True,
        reject_reason="",
    )
    assert gate.regime == "NOMINAL"
