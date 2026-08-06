"""
AILORA Coarse Conjunction Screening (T0 / PHY-C1 / Advisory).

Implements the T0 (coarse) screening tier and PHY-C1 (geometric sphere
intersection) check as defined in the AILORA development contract.

Scientific boundary (Prompt 06 — CSIP-EO-RS-STAGE-20):
  SENTINEL: DOMAIN_REVIEW_REQUIRED — NOT_NORMATIVELY_ACTIVATED
  All outputs from this module are:
    - Advisory only
    - Bounded (PHY-C1 tier, not T3/T4 high-fidelity propagation)
    - Non-normative until independent qualified Astrodynamics review
  No output may be labeled Normative, Qualified, or Operationally Authoritative.

Algorithm: T0 / PHY-C1 — Geometric sphere intersection screening.
  Given two orbital objects with position vectors at a common epoch,
  compute the Euclidean distance between their positions and compare it
  to a configurable conjunction distance threshold (CDT).
  
  This is the coarsest possible screen:
    IF distance ≤ CDT  →  CONJUNCTION_POSSIBLE (requires further analysis)
    IF distance > CDT  →  NO_CONJUNCTION (objects are far apart at this epoch)

Assumptions (PHY-C1 tier):
  - Position vectors are at the SAME epoch (no propagation).
  - No uncertainty covariance is applied (T0 = no uncertainty).
  - This is NOT a probability of collision calculation.
  - Results apply ONLY at the supplied epoch, not over any time window.

No spacecraft command path — permanently denied.
"""

from __future__ import annotations

import math
from enum import StrEnum

from ailora.domain.shared.value_objects import CartesianState

# ---------------------------------------------------------------------------
# Screening result
# ---------------------------------------------------------------------------


class ConjunctionTier(StrEnum):
    """Advisory classification tier for conjunction screening output."""

    T0_PHY_C1 = "T0_PHY_C1"   # Coarse geometric screening (this module)


class ScreeningOutcome(StrEnum):
    """Possible outcomes of a T0/PHY-C1 screening pass."""

    CONJUNCTION_POSSIBLE = "CONJUNCTION_POSSIBLE"
    NO_CONJUNCTION = "NO_CONJUNCTION"


# Default conjunction distance threshold (km)
# PHY-C1 uses 5 km as a very conservative coarse threshold.
# This value is advisory and must be independently validated.
_DEFAULT_CDT_KM = 5.0


class ConjunctionScreeningResult:
    """
    Result of a T0/PHY-C1 coarse conjunction screening pass.

    All fields are advisory-only and non-normative.

    Attributes:
        outcome:            CONJUNCTION_POSSIBLE or NO_CONJUNCTION.
        distance_km:        Euclidean distance between the two position vectors (km).
        threshold_km:       The CDT used for this screening pass.
        tier:               Screening tier (always T0_PHY_C1 from this module).
        is_advisory:        Always True — not an operational recommendation.
        advisory_statement: Human-readable advisory label.
    """

    def __init__(
        self,
        outcome: ScreeningOutcome,
        distance_km: float,
        threshold_km: float,
    ) -> None:
        self.outcome = outcome
        self.distance_km = distance_km
        self.threshold_km = threshold_km
        self.tier = ConjunctionTier.T0_PHY_C1
        self.is_advisory: bool = True
        self.advisory_statement = (
            "Advisory output only — PHY-C1 / T0 geometric screening. "
            "Non-normative. Prompt 06 domain review required for operational use."
        )

    def __repr__(self) -> str:
        return (
            f"ConjunctionScreeningResult("
            f"outcome={self.outcome!r}, "
            f"distance_km={self.distance_km:.3f}, "
            f"threshold_km={self.threshold_km:.3f})"
        )


# ---------------------------------------------------------------------------
# Screening function
# ---------------------------------------------------------------------------


def screen_t0_phy_c1(
    primary: CartesianState,
    secondary: CartesianState,
    conjunction_distance_threshold_km: float = _DEFAULT_CDT_KM,
) -> ConjunctionScreeningResult:
    """
    Perform T0 / PHY-C1 coarse conjunction screening.

    Computes the Euclidean distance between two position vectors (in km)
    and classifies the pair as CONJUNCTION_POSSIBLE or NO_CONJUNCTION.

    ADVISORY ONLY — PHY-C1 tier — Non-normative.
    See module docstring for Prompt 06 domain review boundary.

    Args:
        primary:    Primary object Cartesian state (SI units — metres).
        secondary:  Secondary object Cartesian state (SI units — metres).
        conjunction_distance_threshold_km:
                    Conjunction distance threshold in km.
                    Default: 5.0 km (very conservative coarse screen).

    Returns:
        ConjunctionScreeningResult with outcome, distance, and advisory label.

    Note:
        Position vectors must be at the same epoch and in the same reference frame.
        No epoch or frame consistency check is enforced here — callers must ensure
        this condition.
    """
    # Convert positions from metres to km
    dx_km = (primary.x_m - secondary.x_m) / 1_000.0
    dy_km = (primary.y_m - secondary.y_m) / 1_000.0
    dz_km = (primary.z_m - secondary.z_m) / 1_000.0

    distance_km = math.sqrt(dx_km**2 + dy_km**2 + dz_km**2)

    if distance_km <= conjunction_distance_threshold_km:
        outcome = ScreeningOutcome.CONJUNCTION_POSSIBLE
    else:
        outcome = ScreeningOutcome.NO_CONJUNCTION

    return ConjunctionScreeningResult(
        outcome=outcome,
        distance_km=distance_km,
        threshold_km=conjunction_distance_threshold_km,
    )
