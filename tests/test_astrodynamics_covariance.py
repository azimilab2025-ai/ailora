from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest

from ailora.services.astrodynamics.covariance import (
    CovarianceContract,
    CovarianceError,
    assess_conditioning,
    check_staleness,
    combine_position_covariances,
    conservative_trace_bound,
    propagate_covariance,
    transform_covariance_frame,
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


# --- COMMAND 20 / ENT-013 additions ---


def test_propagate_covariance_applies_stm_and_advances_epoch() -> None:
    from datetime import timedelta

    contract = covariance()
    # Identity STM → matrix unchanged, epoch advanced
    stm = tuple(tuple(1.0 if i == j else 0.0 for j in range(6)) for i in range(6))
    result = propagate_covariance(contract, stm, 60.0)
    assert result.epoch == contract.epoch + timedelta(seconds=60)
    assert result.matrix == contract.matrix
    assert result.frame == contract.frame


def test_propagate_covariance_rejects_bad_stm_or_dt() -> None:
    contract = covariance()
    bad_stm = ((1.0, 0.0), (0.0, 1.0))  # not 6x6
    with pytest.raises(CovarianceError):
        propagate_covariance(contract, bad_stm, 10.0)  # type: ignore[arg-type]
    with pytest.raises(CovarianceError):
        propagate_covariance(contract, tuple(tuple(0.0 for _ in range(6)) for _ in range(6)), -1.0)


def test_transform_covariance_frame_rejects_invalid_rotation() -> None:
    contract = covariance()
    bad_rot = ((1.0, 0.0), (0.0, 1.0))  # not 3x3
    with pytest.raises(CovarianceError):
        transform_covariance_frame(contract, AstrodynamicsFrame.TEME, bad_rot)  # type: ignore[arg-type]


def test_assess_conditioning_returns_explicit_label() -> None:
    contract = covariance()
    label = assess_conditioning(contract)
    assert isinstance(label, str)
    assert "CONDITION" in label or "NOT_COMPUTED" in label or "FINITE" in label


def test_check_staleness_raises_when_too_old() -> None:
    from datetime import timedelta

    contract = covariance()
    now = contract.epoch + timedelta(seconds=3600)
    with pytest.raises(CovarianceError):
        check_staleness(contract, now, max_age_seconds=10.0)
    # should not raise when within bound
    check_staleness(contract, contract.epoch + timedelta(seconds=5), max_age_seconds=10.0)
