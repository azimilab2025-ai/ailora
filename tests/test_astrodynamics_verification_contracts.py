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


# --- COMMAND 21 / ENT-014 additions ---


def test_independent_corpus_record_accepts_valid_digest() -> None:
    from ailora.services.astrodynamics.verification import IndependentCorpusRecord

    rec = IndependentCorpusRecord(
        source_id="REF-CORPUS-1",
        digest="a" * 64,
        revision="rev-1",
        object_pair_count=2,
        notes="synthetic bounded corpus",
    )
    assert rec.source_id == "REF-CORPUS-1"
    assert rec.object_pair_count == 2


def test_independent_corpus_record_rejects_bad_digest() -> None:
    from ailora.services.astrodynamics.verification import (
        IndependentCorpusRecord,
        VerificationError,
    )

    with pytest.raises(VerificationError):
        IndependentCorpusRecord(
            source_id="bad",
            digest="not-a-digest",
            revision="r",
            object_pair_count=1,
            notes="",
        )


def test_common_mode_map_agreement_status() -> None:
    from datetime import UTC, datetime

    from ailora.services.astrodynamics.verification import CommonModeMap

    epoch = datetime(2026, 8, 15, tzinfo=UTC)
    m = CommonModeMap(
        primary_tca_epoch=epoch,
        independent_tca_epoch=epoch,
        delta_seconds=0.0,
        primary_miss_distance_km=1.0,
        independent_miss_distance_km=1.0,
        agreement_status="AGREE",
    )
    assert m.agreement_status == "AGREE"


def test_multiple_minimum_evidence_flags() -> None:
    from ailora.services.astrodynamics.verification import MultipleMinimumEvidence

    ev = MultipleMinimumEvidence(
        candidate_count=2,
        ranked_epochs=(),
        ranked_miss_distances=(0.5, 1.2),
        completeness_flag="PARTIAL",
    )
    assert ev.completeness_flag == "PARTIAL"
    assert ev.candidate_count == 2
