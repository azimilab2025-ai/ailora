from __future__ import annotations

import pytest

from ailora.services.astrodynamics.verification import (
    IndependentTcaReference,
    VerificationError,
    VerificationErrorCode,
    VerificationTolerance,
    verify_tca_result,
)
from tests.astrodynamics_verification_helpers import primary, reference


def test_verification_is_deterministic() -> None:
    first = verify_tca_result(primary(), reference(), VerificationTolerance())
    second = verify_tca_result(primary(), reference(), VerificationTolerance())
    assert first == second
    assert len(first.evidence_digest) == 64
    assert len(first.tolerance_digest) == 64


def test_tampered_reference_digest_is_rejected() -> None:
    valid = reference()
    payload = {field: getattr(valid, field) for field in valid.__dataclass_fields__}
    payload["content_digest"] = "0" * 64
    with pytest.raises(VerificationError) as captured:
        IndependentTcaReference(**payload)
    assert captured.value.code is VerificationErrorCode.DIGEST_MISMATCH
