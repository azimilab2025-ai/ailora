"""
AILORA P3-04: Risk Level and Explanation Output Tests.

Validates:
- RiskLevel classification thresholds (NEGLIGIBLE, LOW, MODERATE, HIGH, CRITICAL)
- ConjunctionRiskAssessment carries advisory-only flag
- Human-readable explanation is present and correct
- Non-binding recommendation is returned
- Provenance label references PHY-C1 and Prompt 06
- No normative claim or operational command implied
"""

from __future__ import annotations

import pytest

from ailora.domain.shared.value_objects import CartesianState, Epoch, ReferenceFrame, TemporalStamp
from ailora.domain.ssa.risk import (
    ConjunctionRiskAssessment,
    RiskLevel,
    assess_conjunction_risk,
)
from ailora.domain.ssa.screening import screen_t0_phy_c1

_EPOCH = Epoch(iso_utc="2026-08-05T00:00:00Z")
_STAMP = TemporalStamp(epoch=_EPOCH, frame=ReferenceFrame.TEME)


def _state(x_km: float) -> CartesianState:
    return CartesianState(
        stamp=_STAMP,
        x_m=x_km * 1_000.0,
        y_m=0.0,
        z_m=0.0,
        vx_ms=0.0,
        vy_ms=0.0,
        vz_ms=0.0,
    )


def _assess(dist_km: float, cdt_km: float = 5.0) -> ConjunctionRiskAssessment:
    s1 = _state(0.0)
    s2 = _state(dist_km)
    result = screen_t0_phy_c1(s1, s2, conjunction_distance_threshold_km=cdt_km)
    return assess_conjunction_risk(result)


# ─── Risk level thresholds ────────────────────────────────────────────────────


def test_critical_risk_at_under_1km() -> None:
    a = _assess(0.5)
    assert a.risk_level == RiskLevel.CRITICAL


def test_critical_risk_at_exactly_1km() -> None:
    a = _assess(1.0)
    assert a.risk_level == RiskLevel.CRITICAL


def test_high_risk_within_cdt() -> None:
    a = _assess(3.0, cdt_km=5.0)
    assert a.risk_level == RiskLevel.HIGH


def test_high_risk_at_exactly_cdt() -> None:
    a = _assess(5.0, cdt_km=5.0)
    assert a.risk_level == RiskLevel.HIGH


def test_moderate_risk_within_2x_cdt() -> None:
    a = _assess(8.0, cdt_km=5.0)
    assert a.risk_level == RiskLevel.MODERATE


def test_low_risk_within_10x_cdt() -> None:
    a = _assess(30.0, cdt_km=5.0)
    assert a.risk_level == RiskLevel.LOW


def test_negligible_risk_beyond_10x_cdt() -> None:
    a = _assess(100.0, cdt_km=5.0)
    assert a.risk_level == RiskLevel.NEGLIGIBLE


# ─── Advisory flags ───────────────────────────────────────────────────────────


def test_assessment_is_advisory_only() -> None:
    a = _assess(3.0)
    assert a.is_advisory is True


@pytest.mark.parametrize("dist", [0.5, 3.0, 8.0, 30.0, 100.0])
def test_advisory_always_true_for_all_risk_levels(dist: float) -> None:
    a = _assess(dist)
    assert a.is_advisory is True


def test_provenance_label_references_phy_c1() -> None:
    a = _assess(3.0)
    assert "PHY-C1" in a.provenance_label or "T0" in a.provenance_label


def test_provenance_label_references_prompt_06() -> None:
    a = _assess(3.0)
    assert "prompt 06" in a.provenance_label.lower()


def test_provenance_label_references_advisory() -> None:
    a = _assess(3.0)
    assert "advisory" in a.provenance_label.lower()


# ─── Explanation content ─────────────────────────────────────────────────────


def test_explanation_contains_risk_level() -> None:
    a = _assess(3.0)
    assert "HIGH" in a.explanation


def test_explanation_contains_distance() -> None:
    a = _assess(3.0)
    assert "3.0" in a.explanation or "3.00" in a.explanation


def test_explanation_is_advisory_label() -> None:
    a = _assess(3.0)
    assert "advisory" in a.explanation.lower()


def test_explanation_does_not_contain_command() -> None:
    a = _assess(3.0)
    forbidden = ["execute maneuver", "send command", "uplink", "telecommand"]
    for f in forbidden:
        assert f not in a.explanation.lower(), (
            f"Explanation must not contain operational command term: '{f}'"
        )


# ─── Recommendation ──────────────────────────────────────────────────────────


def test_recommendation_is_not_a_command() -> None:
    a = _assess(3.0)
    assert "not an operational command" in a.recommendation.lower()


@pytest.mark.parametrize("dist", [0.5, 3.0, 8.0, 30.0, 100.0])
def test_recommendation_never_a_command(dist: float) -> None:
    a = _assess(dist)
    assert "not an operational command" in a.recommendation.lower()


def test_critical_high_recommend_human_review() -> None:
    a = _assess(0.5)
    assert "human" in a.recommendation.lower() or "review" in a.recommendation.lower()


# ─── Module boundary ─────────────────────────────────────────────────────────


def test_risk_module_advisory_boundary() -> None:
    from pathlib import Path

    text = (
        Path(__file__).parent.parent / "src" / "ailora" / "domain" / "ssa" / "risk.py"
    ).read_text()
    assert "advisory" in text.lower()
    assert "prompt 06" in text.lower()
    assert "domain_review_required" in text.lower()


# --- COMMAND 25 / ENT-018 additions ---


def test_pc_method_result_accepts_valid() -> None:
    from ailora.domain.ssa.risk import PcMethodResult

    r = PcMethodResult(
        method_id="M-1",
        method_kind="ALFANO",
        pc_value=1.2e-5,
        limitations="Gaussian assumption",
        evidence_digest="a" * 64,
    )
    assert r.method_kind == "ALFANO"


def test_pc_method_result_rejects_out_of_range() -> None:
    from ailora.domain.ssa.risk import PcMethodResult, RiskAssessmentError

    with pytest.raises(RiskAssessmentError):
        PcMethodResult(
            method_id="M-1",
            method_kind="ALFANO",
            pc_value=1.5,
            limitations="bad",
            evidence_digest="a" * 64,
        )


def test_deterministic_monte_carlo_spec_accepts_valid() -> None:
    from ailora.domain.ssa.risk import DeterministicMonteCarloSpec

    s = DeterministicMonteCarloSpec(
        sample_count=10000,
        seed=42,
        max_runtime_ms=5000,
        limitation_notes="bounded samples only",
    )
    assert s.sample_count == 10000


def test_conjunction_risk_assessment_v2_accepts_valid() -> None:
    from ailora.domain.ssa.risk import (
        ConjunctionRiskAssessmentV2,
        PcMethodResult,
    )

    primary = PcMethodResult(
        method_id="M-1",
        method_kind="ALFANO",
        pc_value=1e-5,
        limitations="none",
        evidence_digest="a" * 64,
    )
    secondary = PcMethodResult(
        method_id="M-2",
        method_kind="FOSTER",
        pc_value=2e-5,
        limitations="none",
        evidence_digest="b" * 64,
    )
    v2 = ConjunctionRiskAssessmentV2(
        assessment_id="A-1",
        primary_pc=primary,
        secondary_pc=secondary,
        combined_level="LOW",
        notes="dual-method advisory",
    )
    assert v2.combined_level == "LOW"
