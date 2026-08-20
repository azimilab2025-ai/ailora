from datetime import UTC, datetime

import pytest


def test_recovery_objective_record_accepts_valid() -> None:
    from ailora.recovery.qualification import RecoveryObjectiveRecord

    r = RecoveryObjectiveRecord(
        objective_id="OBJ-1",
        rpo_seconds=60,
        rto_seconds=300,
        rco_seconds=600,
        evidence_digest="a" * 64,
    )
    assert r.rpo_seconds == 60


def test_recovery_objective_record_rejects_bad_digest() -> None:
    from ailora.recovery.qualification import RecoveryContractError, RecoveryObjectiveRecord

    with pytest.raises(RecoveryContractError):
        RecoveryObjectiveRecord(
            objective_id="OBJ-1",
            rpo_seconds=60,
            rto_seconds=300,
            rco_seconds=600,
            evidence_digest="bad",
        )


def test_failover_drill_evidence_accepts_valid() -> None:
    from ailora.recovery.qualification import FailoverDrillEvidence

    e = FailoverDrillEvidence(
        drill_id="D-1",
        topology="primary-standby",
        started_at=datetime(2026, 8, 19, tzinfo=UTC),
        completed_at=datetime(2026, 8, 19, 1, 0, tzinfo=UTC),
        outcome="PASSED",
    )
    assert e.outcome == "PASSED"


def test_rollout_parity_snapshot_accepts_valid() -> None:
    from ailora.recovery.qualification import RolloutParitySnapshot

    s = RolloutParitySnapshot(
        snapshot_id="S-1",
        web_instances=2,
        worker_instances=2,
        parity_ok=True,
    )
    assert s.parity_ok is True


def test_rollback_decision_record_accepts_valid() -> None:
    from ailora.recovery.qualification import RollbackDecisionRecord

    d = RollbackDecisionRecord(
        decision_id="RB-1",
        reason="failed health checks",
        initiated_by="sre-oncall",
        reversible=True,
    )
    assert d.reversible is True
