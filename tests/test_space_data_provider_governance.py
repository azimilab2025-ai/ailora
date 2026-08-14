from __future__ import annotations

import uuid
from dataclasses import replace
from datetime import UTC, datetime, timedelta

import pytest

from ailora.services.space_data.governance import (
    ProviderQualification,
    QualificationGate,
    QualificationState,
    UnqualifiedProviderError,
)

NOW = datetime(2026, 8, 14, 20, 0, tzinfo=UTC)


def qualification(
    state: QualificationState = QualificationState.QUALIFIED,
    expires_at: datetime | None = None,
) -> ProviderQualification:
    return ProviderQualification(
        qualification_id=uuid.uuid4(),
        provider_id="CELESTRAK",
        provider_version="gp-v1",
        state=state,
        license_name="EXTERNAL_REVIEW_REQUIRED",
        terms_uri="https://celestrak.org/",
        terms_digest="a" * 64,
        retrieved_at=NOW - timedelta(days=1),
        reviewed_at=NOW - timedelta(hours=1),
        expires_at=expires_at,
        reviewer_reference="LEGAL-REVIEW-001",
        redistribution_permitted=False,
        attribution_text="CelesTrak source attribution required",
    )


def test_qualified_current_evidence_passes_gate() -> None:
    QualificationGate().require(qualification(), NOW)


@pytest.mark.parametrize(
    "state",
    [
        QualificationState.UNQUALIFIED,
        QualificationState.SUSPENDED,
        QualificationState.REVOKED,
    ],
)
def test_nonqualified_states_fail_closed(state: QualificationState) -> None:
    with pytest.raises(UnqualifiedProviderError):
        QualificationGate().require(qualification(state), NOW)


def test_expired_evidence_fails_closed() -> None:
    with pytest.raises(UnqualifiedProviderError):
        QualificationGate().require(qualification(expires_at=NOW), NOW)


def test_invalid_terms_digest_and_non_https_uri_rejected() -> None:
    with pytest.raises(ValueError):
        replace(qualification(), terms_digest="bad")
    with pytest.raises(ValueError):
        replace(qualification(), terms_uri="http://celestrak.org")
