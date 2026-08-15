from __future__ import annotations

from dataclasses import replace

import pytest

from ailora.services.astrodynamics.verification import (
    VerificationError,
    VerificationErrorCode,
    VerificationStatus,
    VerificationTolerance,
    verify_tca_result,
)
from tests.astrodynamics_verification_helpers import primary, reference


def test_missing_reference_is_review_required_not_agreement() -> None:
    result = verify_tca_result(primary(), None, VerificationTolerance())
    assert result.status is VerificationStatus.REFERENCE_UNAVAILABLE_REVIEW_REQUIRED


def test_same_engine_cannot_claim_independence() -> None:
    with pytest.raises(VerificationError) as captured:
        verify_tca_result(primary(), reference(engine_id="SGP4_WGS72"), VerificationTolerance())
    assert captured.value.code is VerificationErrorCode.SAME_ENGINE_NOT_INDEPENDENT


def test_false_independence_declaration_is_rejected() -> None:
    with pytest.raises(VerificationError) as captured:
        verify_tca_result(
            primary(), reference(independent_from="OTHER_PRIMARY"), VerificationTolerance()
        )
    assert captured.value.code is VerificationErrorCode.SAME_ENGINE_NOT_INDEPENDENT


def test_semantic_mismatch_is_rejected() -> None:
    mismatched = replace(reference(), time_scale="TAI")
    with pytest.raises(VerificationError) as captured:
        verify_tca_result(primary(), mismatched, VerificationTolerance())
    assert captured.value.code is VerificationErrorCode.SEMANTIC_MISMATCH
