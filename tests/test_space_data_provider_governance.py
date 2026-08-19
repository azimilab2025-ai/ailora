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


# --- COMMAND 22 / ENT-015 additions ---


def test_legal_status_record_accepts_valid() -> None:
    from datetime import UTC, datetime

    from ailora.services.space_data.governance import LegalStatusRecord

    rec = LegalStatusRecord(
        provider_id="PROV-1",
        legal_status="ACTIVE",
        effective_from=datetime(2026, 1, 1, tzinfo=UTC),
        evidence_digest="a" * 64,
    )
    assert rec.legal_status == "ACTIVE"


def test_legal_status_record_rejects_bad_digest() -> None:
    from datetime import UTC, datetime

    from ailora.services.space_data.governance import GovernanceError, LegalStatusRecord

    with pytest.raises(GovernanceError):
        LegalStatusRecord(
            provider_id="PROV-1",
            legal_status="ACTIVE",
            effective_from=datetime(2026, 1, 1, tzinfo=UTC),
            evidence_digest="bad",
        )


def test_freshness_taxonomy_accepts_valid() -> None:
    from ailora.services.space_data.governance import FreshnessTaxonomy

    t = FreshnessTaxonomy(
        source_class="TLE_PROVIDER",
        max_age_seconds=86400,
        poisoning_risk_class="LOW",
    )
    assert t.max_age_seconds == 86400


def test_poisoning_defense_signal_accepts_valid() -> None:
    from datetime import UTC, datetime

    from ailora.services.space_data.governance import PoisoningDefenseSignal

    s = PoisoningDefenseSignal(
        signal_id="SIG-1",
        detected_at=datetime(2026, 8, 19, tzinfo=UTC),
        severity="MEDIUM",
        mitigation_action="HOLD_AND_REVIEW",
    )
    assert s.severity == "MEDIUM"


def test_provider_change_monitor_snapshot_accepts_valid() -> None:
    from datetime import UTC, datetime

    from ailora.services.space_data.governance import ProviderChangeMonitorSnapshot

    snap = ProviderChangeMonitorSnapshot(
        provider_id="PROV-1",
        last_change_epoch=datetime(2026, 8, 19, tzinfo=UTC),
        change_digest="b" * 64,
        monitor_status="WATCHING",
    )
    assert snap.monitor_status == "WATCHING"
