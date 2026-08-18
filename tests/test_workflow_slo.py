from datetime import UTC, datetime, timedelta

import pytest

from ailora.observability.workflow_slo import (
    AlertLevel,
    ScientificOutcome,
    SLOPolicy,
    SyntheticProbe,
    WorkflowObservation,
    WorkflowOutcome,
    WorkflowSLOMonitor,
)

NOW = datetime(2026, 8, 18, tzinfo=UTC)


def test_policy_rejects_unsafe_or_ambiguous_bounds() -> None:
    with pytest.raises(ValueError):
        SLOPolicy(availability_target=1.0)
    with pytest.raises(ValueError):
        SLOPolicy(availability_target=0.99, latency_target_ms=0)


def test_observation_rejects_unbounded_dimensions_and_invalid_latency() -> None:
    with pytest.raises(ValueError):
        WorkflowObservation(
            outcome=WorkflowOutcome.SUCCEEDED,
            scientific_outcome=ScientificOutcome.VERIFIED,
            latency_ms=-1,
        )
    with pytest.raises(ValueError):
        WorkflowObservation(
            outcome=WorkflowOutcome.SUCCEEDED,
            scientific_outcome=ScientificOutcome.VERIFIED,
            latency_ms=1,
            dimensions={"tenant_id": "secret-cardinality"},
        )


def test_snapshot_exposes_sli_error_budget_burn_and_scientific_counts() -> None:
    monitor = WorkflowSLOMonitor(SLOPolicy(availability_target=0.8, latency_target_ms=100))
    for latency in (10, 20, 30, 40):
        monitor.observe(
            WorkflowObservation(
                outcome=WorkflowOutcome.SUCCEEDED,
                scientific_outcome=ScientificOutcome.VERIFIED,
                latency_ms=latency,
            )
        )
    monitor.observe(
        WorkflowObservation(
            outcome=WorkflowOutcome.FAILED,
            scientific_outcome=ScientificOutcome.INDETERMINATE,
            latency_ms=250,
        )
    )
    snapshot = monitor.snapshot()
    assert snapshot.total == 5
    assert snapshot.availability == pytest.approx(0.8)
    assert snapshot.error_budget_remaining == pytest.approx(0.0)
    assert snapshot.burn_rate == pytest.approx(1.0)
    assert snapshot.latency_compliance == pytest.approx(0.8)
    assert snapshot.scientific_counts == {"INDETERMINATE": 1, "VERIFIED": 4}


def test_alert_policy_is_deterministic_and_fail_closed() -> None:
    policy = SLOPolicy(availability_target=0.99, latency_target_ms=100)
    monitor = WorkflowSLOMonitor(policy)
    monitor.observe(
        WorkflowObservation(
            outcome=WorkflowOutcome.FAILED,
            scientific_outcome=ScientificOutcome.FAILED,
            latency_ms=200,
        )
    )
    assert monitor.alert_level() is AlertLevel.CRITICAL


def test_synthetic_probe_has_freshness_and_advisory_boundaries() -> None:
    fresh = SyntheticProbe(
        probe_id="workflow-readiness",
        observed_at=NOW,
        succeeded=True,
        advisory_only=True,
    )
    assert fresh.is_healthy(now=NOW + timedelta(seconds=30), max_age=timedelta(minutes=1))
    assert not fresh.is_healthy(now=NOW + timedelta(minutes=2), max_age=timedelta(minutes=1))
    with pytest.raises(ValueError):
        SyntheticProbe(
            probe_id="workflow-readiness",
            observed_at=NOW,
            succeeded=True,
            advisory_only=False,
        )
