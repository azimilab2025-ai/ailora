"""
AILORA P3-07: Reproducible Demo Scenario and Vertical Slice Integration Tests.

This is the PHASE_3 exit test: a complete end-to-end integration of the
conjunction risk assessment pipeline using SYNTHETIC data only.

Expected outputs are deterministic given fixed inputs — this test is
reproducible and serves as the PHASE_3 exit-condition evidence.

All outputs are Advisory, Bounded, PHY-C1/T0, Non-normative.
Prompt 06 DOMAIN_REVIEW_REQUIRED sentinel applies.
"""

from __future__ import annotations

import pytest

from ailora.domain.ssa.demo import (
    DEMO_SEPARATION_CLOSE_M,
    DEMO_SEPARATION_FAR_M,
    DemoScenarioResult,
    run_demo_scenario,
)
from ailora.domain.ssa.review import ReviewState
from ailora.domain.ssa.risk import RiskLevel
from ailora.domain.ssa.screening import ScreeningOutcome

# ─── Close conjunction scenario (3 km separation) ────────────────────────────


@pytest.fixture(scope="module")
def close_result() -> DemoScenarioResult:
    return run_demo_scenario(separation_m=DEMO_SEPARATION_CLOSE_M)


def test_close_scenario_runs_without_error(close_result: DemoScenarioResult) -> None:
    assert close_result is not None


def test_close_scenario_is_advisory(close_result: DemoScenarioResult) -> None:
    assert close_result.is_advisory is True


def test_close_scenario_tle_a_parsed(close_result: DemoScenarioResult) -> None:
    assert close_result.tle_a.name == "SYNTH-SAT-A"


def test_close_scenario_tle_b_parsed(close_result: DemoScenarioResult) -> None:
    assert close_result.tle_b.name == "SYNTH-SAT-B"


def test_close_scenario_screening_outcome_conjunction_possible(
    close_result: DemoScenarioResult,
) -> None:
    """3 km separation < 5 km CDT → CONJUNCTION_POSSIBLE."""
    assert close_result.screening_result.outcome == ScreeningOutcome.CONJUNCTION_POSSIBLE


def test_close_scenario_distance_correct(close_result: DemoScenarioResult) -> None:
    """3 000 m separation → 3.0 km distance."""
    assert abs(close_result.screening_result.distance_km - 3.0) < 0.001


def test_close_scenario_risk_level_high_or_critical(
    close_result: DemoScenarioResult,
) -> None:
    """3 km separation (< 5 km CDT, > 1 km) → HIGH risk."""
    assert close_result.risk_assessment.risk_level == RiskLevel.HIGH


def test_close_scenario_risk_is_advisory(close_result: DemoScenarioResult) -> None:
    assert close_result.risk_assessment.is_advisory is True


def test_close_scenario_explanation_contains_high(close_result: DemoScenarioResult) -> None:
    assert "HIGH" in close_result.risk_assessment.explanation


def test_close_scenario_recommendation_is_not_command(
    close_result: DemoScenarioResult,
) -> None:
    assert "not an operational command" in close_result.risk_assessment.recommendation.lower()


def test_close_scenario_review_state_under_review(
    close_result: DemoScenarioResult,
) -> None:
    assert close_result.review_record.state == ReviewState.UNDER_REVIEW


def test_close_scenario_audit_has_4_entries(close_result: DemoScenarioResult) -> None:
    """Demo pipeline appends exactly 4 audit entries."""
    assert close_result.audit_log.total_entries == 4


def test_close_scenario_audit_tenant_isolation(close_result: DemoScenarioResult) -> None:
    """All audit entries belong to the demo tenant."""
    entries = close_result.audit_log.entries_for_tenant(close_result.tenant_id)
    assert len(entries) == 4


def test_close_scenario_scenario_advisory_only(close_result: DemoScenarioResult) -> None:
    assert close_result.scenario.ADVISORY_ONLY is True


# ─── Far separation scenario (500 km) ────────────────────────────────────────


@pytest.fixture(scope="module")
def far_result() -> DemoScenarioResult:
    return run_demo_scenario(separation_m=DEMO_SEPARATION_FAR_M)


def test_far_scenario_no_conjunction(far_result: DemoScenarioResult) -> None:
    assert far_result.screening_result.outcome == ScreeningOutcome.NO_CONJUNCTION


def test_far_scenario_risk_negligible(far_result: DemoScenarioResult) -> None:
    assert far_result.risk_assessment.risk_level == RiskLevel.NEGLIGIBLE


def test_far_scenario_distance_approximately_500km(far_result: DemoScenarioResult) -> None:
    assert abs(far_result.screening_result.distance_km - 500.0) < 1.0


# ─── Advisory label integrity ─────────────────────────────────────────────────


def test_demo_advisory_label_contains_prompt_06(close_result: DemoScenarioResult) -> None:
    assert "prompt 06" in close_result.advisory_label.lower()


def test_demo_advisory_label_contains_phy_c1(close_result: DemoScenarioResult) -> None:
    assert "PHY-C1" in close_result.advisory_label or "T0" in close_result.advisory_label


def test_demo_result_no_command_path(close_result: DemoScenarioResult) -> None:
    """DemoScenarioResult must not carry any command execution path."""
    assert not hasattr(close_result, "execute_command")
    assert not hasattr(close_result, "send_telecommand")
    assert not hasattr(close_result, "uplink")


# ─── Reproducibility check ───────────────────────────────────────────────────


def test_demo_is_reproducible() -> None:
    """
    Running the demo twice with identical inputs must produce identical
    deterministic outputs (distance, outcome, risk level).
    """
    r1 = run_demo_scenario(separation_m=3_000.0)
    r2 = run_demo_scenario(separation_m=3_000.0)

    assert r1.screening_result.distance_km == r2.screening_result.distance_km
    assert r1.screening_result.outcome == r2.screening_result.outcome
    assert r1.risk_assessment.risk_level == r2.risk_assessment.risk_level
    assert r1.risk_assessment.explanation == r2.risk_assessment.explanation
