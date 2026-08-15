from __future__ import annotations

from ailora.services.astrodynamics.verification import (
    VerificationStatus,
    VerificationTolerance,
    verify_tca_result,
)
from tests.astrodynamics_verification_helpers import primary, reference


def test_exact_reference_agrees_and_is_advisory_only() -> None:
    result = verify_tca_result(primary(), reference(), VerificationTolerance())
    assert result.status is VerificationStatus.AGREEMENT_WITHIN_TOLERANCE
    assert result.collision_probability is None
    assert result.advisory_only is True
    assert result.independent_scientific_approval == "EXTERNAL_GATE_NOT_SELF_ISSUED"


def test_equality_at_absolute_tolerance_is_inclusive() -> None:
    tolerance = VerificationTolerance(miss_distance_km=0.25, relative=0.0)
    result = verify_tca_result(primary(), reference(miss_distance_km=1.25), tolerance)
    assert result.status is VerificationStatus.AGREEMENT_WITHIN_TOLERANCE


def test_material_disagreement_never_becomes_pass() -> None:
    result = verify_tca_result(
        primary(), reference(position=(2.0, 0.0, 0.0)), VerificationTolerance()
    )
    assert result.status is VerificationStatus.MATERIAL_DISAGREEMENT_REVIEW_REQUIRED
