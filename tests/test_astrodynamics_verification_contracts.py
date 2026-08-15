from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from ailora.services.astrodynamics.verification import VerificationTolerance
from tests.astrodynamics_verification_helpers import reference


def test_reference_and_tolerance_are_immutable() -> None:
    item = reference()
    with pytest.raises(FrozenInstanceError):
        item.engine_id = "changed"  # type: ignore[misc]
    assert VerificationTolerance().relative == 1e-12


@pytest.mark.parametrize("value", [-1.0, float("inf"), float("nan")])
def test_tolerances_reject_invalid_values(value: float) -> None:
    with pytest.raises(ValueError, match="finite and nonnegative"):
        VerificationTolerance(tca_time_seconds=value)
