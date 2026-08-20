import pytest


def test_capacity_run_evidence_accepts_valid() -> None:
    from ailora.performance.budgets import CapacityRunEvidence

    e = CapacityRunEvidence(
        run_id="R-1",
        object_count=1000,
        duration_ms=2500,
        recall_ok=True,
        evidence_digest="a" * 64,
    )
    assert e.object_count == 1000


def test_capacity_run_evidence_rejects_bad_digest() -> None:
    from ailora.performance.budgets import CapacityRunEvidence, PerformanceContractError

    with pytest.raises(PerformanceContractError):
        CapacityRunEvidence(
            run_id="R-1",
            object_count=1000,
            duration_ms=2500,
            recall_ok=True,
            evidence_digest="bad",
        )


def test_fault_injection_record_accepts_valid() -> None:
    from ailora.performance.budgets import FaultInjectionRecord

    r = FaultInjectionRecord(
        injection_id="F-1",
        fault_class="TIMEOUT",
        target="ssa.ingest",
        injected=True,
        recovered=True,
    )
    assert r.fault_class == "TIMEOUT"


def test_soak_window_result_accepts_valid() -> None:
    from ailora.performance.budgets import SoakWindowResult

    s = SoakWindowResult(
        window_id="W-1",
        duration_s=3600,
        error_count=0,
        passed=True,
    )
    assert s.passed is True


def test_cost_guardrail_snapshot_accepts_valid() -> None:
    from ailora.performance.budgets import CostGuardrailSnapshot

    c = CostGuardrailSnapshot(
        snapshot_id="C-1",
        estimated_units=120.0,
        budget_units=500.0,
        within_budget=True,
    )
    assert c.within_budget is True
