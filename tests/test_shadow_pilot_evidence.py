import pytest


def test_frozen_criteria_record_accepts_valid() -> None:
    from ailora.observability.workflow_slo import FrozenCriteriaRecord

    r = FrozenCriteriaRecord(
        criteria_id="FC-1",
        version="1.0.0",
        rules_digest="a" * 64,
        approved_by="release-authority",
    )
    assert r.version == "1.0.0"


def test_frozen_criteria_record_rejects_bad_digest() -> None:
    from ailora.observability.workflow_slo import FrozenCriteriaRecord, SloContractError

    with pytest.raises(SloContractError):
        FrozenCriteriaRecord(
            criteria_id="FC-1",
            version="1.0.0",
            rules_digest="bad",
            approved_by="release-authority",
        )


def test_shadow_comparison_evidence_accepts_valid() -> None:
    from ailora.observability.workflow_slo import ShadowComparisonEvidence

    e = ShadowComparisonEvidence(
        comparison_id="SC-1",
        tenant_scope="tenant-demo",
        baseline_digest="b" * 64,
        candidate_digest="c" * 64,
        matched=True,
    )
    assert e.matched is True


def test_incident_drill_evidence_accepts_valid() -> None:
    from ailora.observability.workflow_slo import IncidentDrillEvidence

    d = IncidentDrillEvidence(
        drill_id="ID-1",
        scenario="api-timeout",
        outcome="PASSED",
        evidence_digest="d" * 64,
    )
    assert d.outcome == "PASSED"


def test_synthetic_monitor_result_accepts_valid() -> None:
    from ailora.observability.workflow_slo import SyntheticMonitorResult

    m = SyntheticMonitorResult(
        monitor_id="SM-1",
        probe_kind="HTTP_HEALTH",
        success=True,
        latency_ms=12,
    )
    assert m.success is True
