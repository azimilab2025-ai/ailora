from __future__ import annotations

import uuid
from datetime import UTC, datetime, timedelta

import pytest

from ailora.services.astrodynamics.analysis import (
    ConjunctionAnalysisConfig,
    SafeScientificLabel,
    assess_bounded_conjunction,
)
from ailora.services.astrodynamics.covariance import CovarianceContract
from ailora.services.astrodynamics.models import (
    AstrodynamicsFrame,
    DistanceUnit,
    VelocityUnit,
)
from ailora.services.astrodynamics.tca import TcaConvergenceStatus, TcaResult

EPOCH = datetime(2026, 8, 15, tzinfo=UTC)


def tca(miss_distance: float) -> TcaResult:
    return TcaResult(
        uuid.uuid4(),
        EPOCH,
        miss_distance,
        (miss_distance, 0.0, 0.0),
        (0.0, 1.0, 0.0),
        AstrodynamicsFrame.TEME,
        DistanceUnit.KILOMETER,
        VelocityUnit.KILOMETER_PER_SECOND,
        TcaConvergenceStatus.CONVERGED,
        25,
        10,
        EPOCH - timedelta(minutes=1),
        EPOCH + timedelta(minutes=1),
        0.001,
        1e-9,
        "BOUNDED_TCA_SEARCH",
        "1.0.0",
        "SGP4",
        "2.27",
        "a" * 64,
        "b" * 64,
    )


def covariance(variance: float) -> CovarianceContract:
    matrix = tuple(
        tuple(
            variance if row == column and row < 3 else (0.01 if row == column else 0.0)
            for column in range(6)
        )
        for row in range(6)
    )
    return CovarianceContract(
        matrix,
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


def test_missing_uncertainty_never_creates_safe_label() -> None:
    result = assess_bounded_conjunction(tca(100.0), ConjunctionAnalysisConfig())
    assert result.label is SafeScientificLabel.UNCERTAINTY_UNAVAILABLE_REVIEW_REQUIRED
    assert result.uncertainty is None
    assert result.collision_probability is None
    assert result.advisory_only is True
    assert result.tca.time_uncertainty_seconds is None


def test_lower_bound_controls_advisory_label_including_equality() -> None:
    config = ConjunctionAnalysisConfig(advisory_threshold_km=10.0, sigma_multiplier=1.0)
    small = covariance(1.0 / 6.0)
    above = assess_bounded_conjunction(
        tca(12.0),
        config,
        primary_covariance=small,
        secondary_covariance=small,
        independence_assumed=True,
    )
    boundary = assess_bounded_conjunction(
        tca(11.0),
        config,
        primary_covariance=small,
        secondary_covariance=small,
        independence_assumed=True,
    )
    assert above.uncertainty is not None
    assert above.uncertainty.radius_km == pytest.approx(1.0)
    assert above.label is SafeScientificLabel.BOUNDED_SEPARATION_ABOVE_THRESHOLD
    assert boundary.label is SafeScientificLabel.POTENTIAL_CONJUNCTION_REVIEW_REQUIRED


def test_single_covariance_is_rejected_instead_of_imputed() -> None:
    with pytest.raises(ValueError, match="both covariance"):
        assess_bounded_conjunction(
            tca(20.0), ConjunctionAnalysisConfig(), primary_covariance=covariance(1.0)
        )


def test_assessment_is_deterministic_and_preserves_limitations() -> None:
    args = (tca(20.0), ConjunctionAnalysisConfig())
    first = assess_bounded_conjunction(*args)
    second = assess_bounded_conjunction(*args)
    assert first.label == second.label
    assert first.configuration_digest == second.configuration_digest
    assert "COLLISION_PROBABILITY_NOT_COMPUTED" in first.limitations
    assert "TCA_PHYSICAL_TIME_UNCERTAINTY_UNAVAILABLE" in first.limitations
    assert first.independent_verification_status == "NOT_VERIFIED_DEFERRED_TO_C12"
