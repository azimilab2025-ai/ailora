"""
AILORA P3-03: Coarse Conjunction Screening Tests (T0 / PHY-C1 / Advisory).

Validates:
- screen_t0_phy_c1 returns CONJUNCTION_POSSIBLE when distance ≤ CDT.
- screen_t0_phy_c1 returns NO_CONJUNCTION when distance > CDT.
- ConjunctionScreeningResult carries advisory-only flag.
- Custom CDT override works correctly.
- Distance calculation is correct (unit conversion metres → km).
- Advisory-only labeling on the screening module.
- No operational command path.
"""

from __future__ import annotations

from ailora.domain.shared.value_objects import CartesianState, Epoch, ReferenceFrame, TemporalStamp
from ailora.domain.ssa.screening import (
    ConjunctionTier,
    ScreeningOutcome,
    screen_t0_phy_c1,
)

_EPOCH = Epoch(iso_utc="2026-08-05T00:00:00Z")
_STAMP = TemporalStamp(epoch=_EPOCH, frame=ReferenceFrame.TEME)


def _state(x_km: float, y_km: float, z_km: float) -> CartesianState:
    """Create a CartesianState from km values (stored as metres)."""
    return CartesianState(
        stamp=_STAMP,
        x_m=x_km * 1_000.0,
        y_m=y_km * 1_000.0,
        z_m=z_km * 1_000.0,
        vx_ms=0.0,
        vy_ms=0.0,
        vz_ms=0.0,
    )


# ─── Outcome correctness ─────────────────────────────────────────────────────


def test_objects_at_same_position_is_conjunction_possible() -> None:
    s1 = _state(7000.0, 0.0, 0.0)
    s2 = _state(7000.0, 0.0, 0.0)
    result = screen_t0_phy_c1(s1, s2)
    assert result.outcome == ScreeningOutcome.CONJUNCTION_POSSIBLE


def test_objects_close_within_default_cdt() -> None:
    """Objects 3 km apart must be CONJUNCTION_POSSIBLE (< 5 km default CDT)."""
    s1 = _state(7000.0, 0.0, 0.0)
    s2 = _state(7003.0, 0.0, 0.0)
    result = screen_t0_phy_c1(s1, s2)
    assert result.outcome == ScreeningOutcome.CONJUNCTION_POSSIBLE
    assert abs(result.distance_km - 3.0) < 0.001


def test_objects_just_at_default_cdt_boundary() -> None:
    """Objects exactly at CDT boundary must be CONJUNCTION_POSSIBLE."""
    s1 = _state(7000.0, 0.0, 0.0)
    s2 = _state(7005.0, 0.0, 0.0)
    result = screen_t0_phy_c1(s1, s2)
    assert result.outcome == ScreeningOutcome.CONJUNCTION_POSSIBLE
    assert abs(result.distance_km - 5.0) < 0.001


def test_objects_far_apart_no_conjunction() -> None:
    """Objects 100 km apart must be NO_CONJUNCTION."""
    s1 = _state(7000.0, 0.0, 0.0)
    s2 = _state(7100.0, 0.0, 0.0)
    result = screen_t0_phy_c1(s1, s2)
    assert result.outcome == ScreeningOutcome.NO_CONJUNCTION
    assert abs(result.distance_km - 100.0) < 0.001


def test_objects_in_different_orbits_no_conjunction() -> None:
    """Objects 1000 km apart must be NO_CONJUNCTION."""
    s1 = _state(7000.0, 0.0, 0.0)
    s2 = _state(7000.0, 1000.0, 0.0)
    result = screen_t0_phy_c1(s1, s2)
    assert result.outcome == ScreeningOutcome.NO_CONJUNCTION
    assert abs(result.distance_km - 1000.0) < 0.001


def test_3d_distance_computed_correctly() -> None:
    """Distance must use Euclidean 3D formula."""
    s1 = _state(0.0, 0.0, 0.0)
    s2 = _state(3.0, 4.0, 0.0)
    result = screen_t0_phy_c1(s1, s2, conjunction_distance_threshold_km=10.0)
    assert abs(result.distance_km - 5.0) < 0.001


def test_custom_cdt_smaller_threshold() -> None:
    """Objects 3 km apart but CDT=2 km must yield NO_CONJUNCTION."""
    s1 = _state(7000.0, 0.0, 0.0)
    s2 = _state(7003.0, 0.0, 0.0)
    result = screen_t0_phy_c1(s1, s2, conjunction_distance_threshold_km=2.0)
    assert result.outcome == ScreeningOutcome.NO_CONJUNCTION


def test_custom_cdt_larger_threshold() -> None:
    """Objects 20 km apart but CDT=50 km must yield CONJUNCTION_POSSIBLE."""
    s1 = _state(7000.0, 0.0, 0.0)
    s2 = _state(7020.0, 0.0, 0.0)
    result = screen_t0_phy_c1(s1, s2, conjunction_distance_threshold_km=50.0)
    assert result.outcome == ScreeningOutcome.CONJUNCTION_POSSIBLE


# ─── Advisory labeling ───────────────────────────────────────────────────────


def test_result_is_advisory_only() -> None:
    s1 = _state(7000.0, 0.0, 0.0)
    s2 = _state(7001.0, 0.0, 0.0)
    result = screen_t0_phy_c1(s1, s2)
    assert result.is_advisory is True


def test_result_tier_is_t0_phy_c1() -> None:
    s1 = _state(7000.0, 0.0, 0.0)
    s2 = _state(7001.0, 0.0, 0.0)
    result = screen_t0_phy_c1(s1, s2)
    assert result.tier == ConjunctionTier.T0_PHY_C1


def test_result_advisory_statement_present() -> None:
    s1 = _state(7000.0, 0.0, 0.0)
    s2 = _state(7001.0, 0.0, 0.0)
    result = screen_t0_phy_c1(s1, s2)
    assert "advisory" in result.advisory_statement.lower()
    assert "prompt 06" in result.advisory_statement.lower()


def test_result_repr_contains_outcome() -> None:
    s1 = _state(7000.0, 0.0, 0.0)
    s2 = _state(7001.0, 0.0, 0.0)
    result = screen_t0_phy_c1(s1, s2)
    assert "CONJUNCTION_POSSIBLE" in repr(result)


def test_screening_module_advisory_boundary() -> None:
    from pathlib import Path

    text = (
        Path(__file__).parent.parent / "src" / "ailora" / "domain" / "ssa" / "screening.py"
    ).read_text()
    assert "advisory" in text.lower()
    assert "prompt 06" in text.lower()
    assert "domain_review_required" in text.lower()


def test_no_pc_calculation_in_t0_module() -> None:
    """T0/PHY-C1 screening must not claim to compute Probability of Collision."""
    from pathlib import Path

    text = (
        (Path(__file__).parent.parent / "src" / "ailora" / "domain" / "ssa" / "screening.py")
        .read_text()
        .lower()
    )
    # These would indicate a T3/T4 normative claim
    forbidden = ["probability_of_collision", "p_c =", "pc =", "foster_1992"]
    for f in forbidden:
        assert f not in text, f"T0 screening must not claim Pc calculation: '{f}'"


# ─── Distance edge cases ─────────────────────────────────────────────────────


def test_zero_distance_is_conjunction_possible() -> None:
    s = _state(7000.0, 0.0, 0.0)
    result = screen_t0_phy_c1(s, s)
    assert result.outcome == ScreeningOutcome.CONJUNCTION_POSSIBLE
    assert result.distance_km == 0.0


def test_very_large_distance_no_conjunction() -> None:
    s1 = _state(0.0, 0.0, 0.0)
    s2 = _state(100_000.0, 0.0, 0.0)
    result = screen_t0_phy_c1(s1, s2)
    assert result.outcome == ScreeningOutcome.NO_CONJUNCTION
    assert result.distance_km > 90_000.0


def test_negative_position_components_handled() -> None:
    s1 = _state(-7000.0, 0.0, 0.0)
    s2 = _state(-7002.0, 0.0, 0.0)
    result = screen_t0_phy_c1(s1, s2)
    assert result.outcome == ScreeningOutcome.CONJUNCTION_POSSIBLE
    assert abs(result.distance_km - 2.0) < 0.001
