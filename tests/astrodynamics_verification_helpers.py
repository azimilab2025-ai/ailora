from __future__ import annotations

import uuid
from datetime import UTC, datetime

from ailora.services.astrodynamics.models import AstrodynamicsFrame, DistanceUnit, VelocityUnit
from ailora.services.astrodynamics.tca import TcaConvergenceStatus, TcaResult
from ailora.services.astrodynamics.verification import (
    IndependentTcaReference,
    reference_content_digest,
)

EPOCH = datetime(2026, 8, 15, tzinfo=UTC)


def primary() -> TcaResult:
    return TcaResult(
        request_id=uuid.UUID("12345678-1234-5678-1234-567812345678"),
        tca_epoch=EPOCH,
        miss_distance_km=1.0,
        relative_position_km=(1.0, 0.0, 0.0),
        relative_velocity_km_s=(0.0, 0.01, 0.0),
        frame=AstrodynamicsFrame.TEME,
        distance_unit=DistanceUnit.KILOMETER,
        velocity_unit=VelocityUnit.KILOMETER_PER_SECOND,
        status=TcaConvergenceStatus.CONVERGED,
        evaluation_count=10,
        iteration_count=3,
        search_start=EPOCH,
        search_end=EPOCH.replace(minute=1),
        time_tolerance_seconds=0.001,
        distance_tolerance_km=1e-9,
        algorithm_id="BOUNDED_TCA_GOLDEN_SECTION",
        algorithm_version="1.0.0",
        propagator_algorithm_id="SGP4_WGS72",
        propagator_version="2.27",
        input_digest="1" * 64,
        configuration_digest="2" * 64,
    )


def reference(
    *,
    miss_distance_km: float = 1.0,
    position: tuple[float, float, float] = (1.0, 0.0, 0.0),
    engine_id: str = "INDEPENDENT_FIXTURE_ENGINE",
    independent_from: str = "SGP4_WGS72",
) -> IndependentTcaReference:
    values = {
        "reference_id": "fixture-001",
        "source_revision": "verified-fixture-v1",
        "engine_id": engine_id,
        "engine_version": "1.0",
        "independent_from_algorithm_id": independent_from,
        "tca_epoch": EPOCH,
        "miss_distance_km": miss_distance_km,
        "relative_position_km": position,
        "relative_velocity_km_s": (0.0, 0.01, 0.0),
    }
    digest = reference_content_digest(**values)
    return IndependentTcaReference(source_digest="a" * 64, content_digest=digest, **values)
