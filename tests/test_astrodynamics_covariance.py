from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest

from ailora.services.astrodynamics.covariance import (
    CovarianceContract,
    CovarianceError,
    combine_position_covariances,
    conservative_trace_bound,
)
from ailora.services.astrodynamics.models import (
    AstrodynamicsFrame,
    DistanceUnit,
    VelocityUnit,
)

EPOCH = datetime(2026, 8, 15, tzinfo=UTC)


def diagonal(*values: float) -> tuple[tuple[float, ...], ...]:
    return tuple(
        tuple(value if row == column else 0.0 for column, value in enumerate(values))
        for row in range(6)
    )


def covariance(matrix: tuple[tuple[float, ...], ...] | None = None) -> CovarianceContract:
    return CovarianceContract(
        matrix or diagonal(1.0, 4.0, 9.0, 0.01, 0.01, 0.01),
        EPOCH,
        AstrodynamicsFrame.TEME,
        DistanceUnit.KILOMETER,
        VelocityUnit.KILOMETER_PER_SECOND,
        "c" * 64,
        "catalog-revision-1",
        "STATE_ERROR_COVARIANCE",
        "CARTESIAN_TEME",
        "ONE_SIGMA",
        "OBJECT_INTERNAL_ONLY",
    )


def test_covariance_accepts_psd_and_exposes_position_block() -> None:
    contract = covariance()
    assert contract.position_block == ((1.0, 0.0, 0.0), (0.0, 4.0, 0.0), (0.0, 0.0, 9.0))
    assert contract.numerical_health == "FINITE_SYMMETRIC_PSD;CONDITION_NUMBER_NOT_COMPUTED"
    assert covariance(diagonal(0.0, 0.0, 0.0, 0.0, 0.0, 0.0)).position_block[0][0] == 0.0


@pytest.mark.parametrize(
    ("matrix", "message"),
    [
        (((0.0,) * 6,) * 5, "6x6"),
        (diagonal(float("nan"), 1.0, 1.0, 1.0, 1.0, 1.0), "finite"),
        (
            (
                (1.0, 0.1, 0.0, 0.0, 0.0, 0.0),
                (0.2, 1.0, 0.0, 0.0, 0.0, 0.0),
                (0.0, 0.0, 1.0, 0.0, 0.0, 0.0),
                (0.0, 0.0, 0.0, 1.0, 0.0, 0.0),
                (0.0, 0.0, 0.0, 0.0, 1.0, 0.0),
                (0.0, 0.0, 0.0, 0.0, 0.0, 1.0),
            ),
            "symmetric",
        ),
        (diagonal(-1.0, 1.0, 1.0, 1.0, 1.0, 1.0), "positive semidefinite"),
    ],
)
def test_covariance_rejects_shape_nonfinite_asymmetry_and_non_psd(
    matrix: tuple[tuple[float, ...], ...], message: str
) -> None:
    with pytest.raises(CovarianceError, match=message):
        covariance(matrix)


def test_combination_requires_explicit_independence_and_epoch_alignment() -> None:
    first = covariance()
    second = covariance(diagonal(4.0, 5.0, 6.0, 0.02, 0.02, 0.02))
    with pytest.raises(CovarianceError, match="independence"):
        combine_position_covariances(
            first,
            second,
            target_epoch=EPOCH,
            epoch_tolerance_seconds=0.0,
            independence_assumed=False,
        )
    with pytest.raises(CovarianceError, match="aligned"):
        combine_position_covariances(
            first,
            second,
            target_epoch=EPOCH + timedelta(seconds=1),
            epoch_tolerance_seconds=0.1,
            independence_assumed=True,
        )
    combined = combine_position_covariances(
        first,
        second,
        target_epoch=EPOCH,
        epoch_tolerance_seconds=0.0,
        independence_assumed=True,
    )
    assert combined == ((5.0, 0.0, 0.0), (0.0, 9.0, 0.0), (0.0, 0.0, 15.0))


def test_trace_bound_is_conservative_and_explicit() -> None:
    bound = conservative_trace_bound(
        ((1.0, 0.0, 0.0), (0.0, 4.0, 0.0), (0.0, 0.0, 9.0)),
        nominal_miss_distance_km=20.0,
        sigma_multiplier=3.0,
    )
    assert bound.radius_km == pytest.approx(3.0 * (14.0**0.5))
    assert bound.lower_miss_distance_km == pytest.approx(20.0 - bound.radius_km)
    assert bound.upper_miss_distance_km == pytest.approx(20.0 + bound.radius_km)
    assert bound.method == "TRACE_BOUND_V1"
