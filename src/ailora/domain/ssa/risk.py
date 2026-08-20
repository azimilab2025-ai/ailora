from __future__ import annotations

import math
import re
from dataclasses import dataclass
from enum import StrEnum

from ailora.domain.ssa.screening import ConjunctionScreeningResult


class RiskLevel(StrEnum):
    """Advisory risk level for a conjunction screening result."""

    NEGLIGIBLE = "NEGLIGIBLE"
    LOW = "LOW"
    MODERATE = "MODERATE"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


# ---------------------------------------------------------------------------
# Risk assessment output
# ---------------------------------------------------------------------------


class ConjunctionRiskAssessment:
    """
    An advisory risk assessment derived from a T0/PHY-C1 screening result.

    All fields are advisory-only and non-normative.
    This class carries both a machine-readable risk level and a human-readable
    explanation for operator review.

    Attributes:
        risk_level:           Advisory risk category.
        distance_km:          Separation distance (km) at the screening epoch.
        threshold_km:         The CDT used for screening.
        screening_result:     The underlying screening result.
        explanation:          Human-readable advisory explanation.
        is_advisory:          Always True.
        provenance_label:     Records the algorithm tier and advisory status.
        recommendation:       Non-binding advisory action hint (NOT a command).
    """

    def __init__(
        self,
        screening_result: ConjunctionScreeningResult,
    ) -> None:
        self.screening_result = screening_result
        self.distance_km = screening_result.distance_km
        self.threshold_km = screening_result.threshold_km
        self.is_advisory: bool = True
        self.provenance_label = (
            "AILORA Advisory Output | T0/PHY-C1 | Non-normative | Prompt 06 DOMAIN_REVIEW_REQUIRED"
        )

        self.risk_level = self._classify_risk()
        self.explanation = self._build_explanation()
        self.recommendation = self._build_recommendation()

    def _classify_risk(self) -> RiskLevel:
        """Classify risk level from distance and threshold."""
        d = self.distance_km
        cdt = self.threshold_km

        if d <= 1.0:
            return RiskLevel.CRITICAL
        if d <= cdt:
            return RiskLevel.HIGH
        if d <= 2.0 * cdt:
            return RiskLevel.MODERATE
        if d <= 10.0 * cdt:
            return RiskLevel.LOW
        return RiskLevel.NEGLIGIBLE

    def _build_explanation(self) -> str:
        """Build a human-readable advisory explanation."""
        outcome = self.screening_result.outcome
        d = self.distance_km
        cdt = self.threshold_km
        level = self.risk_level

        header = f"[ADVISORY — PHY-C1 / T0 — Non-normative] Risk level: {level.value}"

        if level == RiskLevel.CRITICAL:
            body = (
                f"Objects are within {d:.3f} km of each other — within critical range. "
                f"Screening threshold: {cdt:.1f} km. "
                f"Human review is strongly indicated. "
                f"This is an advisory flag only — no operational action is implied."
            )
        elif level == RiskLevel.HIGH:
            body = (
                f"Objects are within the conjunction distance threshold "
                f"({d:.3f} km ≤ {cdt:.1f} km). "
                f"Outcome: {outcome.value}. "
                f"Human review is indicated."
            )
        elif level == RiskLevel.MODERATE:
            body = (
                f"Objects are within 2× the conjunction distance threshold "
                f"({d:.3f} km, threshold {cdt:.1f} km). "
                f"Warrants human attention."
            )
        elif level == RiskLevel.LOW:
            body = (
                f"Objects are outside the CDT but within 10× "
                f"({d:.3f} km, threshold {cdt:.1f} km). "
                f"No immediate concern at this epoch."
            )
        else:  # NEGLIGIBLE
            body = (
                f"Objects are well separated ({d:.3f} km, threshold {cdt:.1f} km). "
                f"No conjunction indicated at this epoch."
            )

        return f"{header}. {body}"

    def _build_recommendation(self) -> str:
        """Build a non-binding advisory recommendation hint."""
        if self.risk_level in (RiskLevel.CRITICAL, RiskLevel.HIGH):
            return (
                "Advisory: Human operator review recommended. "
                "This is not an operational command or clearance."
            )
        if self.risk_level == RiskLevel.MODERATE:
            return (
                "Advisory: Monitor scenario at next available epoch. "
                "This is not an operational command or clearance."
            )
        return (
            "Advisory: No action indicated at this epoch. "
            "This is not an operational command or clearance."
        )

    def __repr__(self) -> str:
        return (
            f"ConjunctionRiskAssessment("
            f"risk_level={self.risk_level!r}, "
            f"distance_km={self.distance_km:.3f})"
        )


# ---------------------------------------------------------------------------
# Public factory
# ---------------------------------------------------------------------------


def assess_conjunction_risk(
    screening_result: ConjunctionScreeningResult,
) -> ConjunctionRiskAssessment:
    """
    Produce an advisory risk assessment from a T0/PHY-C1 screening result.

    Advisory-only. Non-normative. Prompt 06 domain review required for
    operational use.

    Args:
        screening_result: Output of screen_t0_phy_c1().

    Returns:
        ConjunctionRiskAssessment with risk level, explanation, and recommendation.
    """
    return ConjunctionRiskAssessment(screening_result)


class RiskAssessmentError(ValueError):
    """Fail-closed risk assessment contract error."""

    def __init__(self, detail: str) -> None:
        super().__init__(detail.strip()[:256] or "RISK_ASSESSMENT_ERROR")


@dataclass(frozen=True, slots=True)
class PcMethodResult:
    """Qualified Pc method result. Fail-closed. Advisory only."""

    method_id: str
    method_kind: str
    pc_value: float
    limitations: str
    evidence_digest: str

    def __post_init__(self) -> None:
        if not self.method_id.strip() or len(self.method_id) > 128:
            raise RiskAssessmentError("method_id must be explicit and bounded")
        if self.method_kind not in {"ALFANO", "FOSTER", "DETERMINISTIC_MC", "OTHER"}:
            raise RiskAssessmentError("method_kind must be ALFANO|FOSTER|DETERMINISTIC_MC|OTHER")
        if not math.isfinite(self.pc_value) or not (0.0 <= self.pc_value <= 1.0):
            raise RiskAssessmentError("pc_value must be finite in [0, 1]")
        if not self.limitations.strip():
            raise RiskAssessmentError("limitations must be explicit")
        if not re.fullmatch(r"[0-9a-f]{64}", self.evidence_digest):
            raise RiskAssessmentError("evidence_digest must be lowercase SHA-256")


@dataclass(frozen=True, slots=True)
class DeterministicMonteCarloSpec:
    """Bounded deterministic Monte Carlo specification. No non-deterministic RNG."""

    sample_count: int
    seed: int
    max_runtime_ms: int
    limitation_notes: str

    def __post_init__(self) -> None:
        if self.sample_count <= 0 or self.sample_count > 1_000_000:
            raise RiskAssessmentError("sample_count must be in (0, 1e6]")
        if self.max_runtime_ms <= 0:
            raise RiskAssessmentError("max_runtime_ms must be positive")
        if not self.limitation_notes.strip():
            raise RiskAssessmentError("limitation_notes must be explicit")


@dataclass(frozen=True, slots=True)
class ConjunctionRiskAssessmentV2:
    """Dual-method conjunction risk assessment V2. Advisory only."""

    assessment_id: str
    primary_pc: PcMethodResult
    secondary_pc: PcMethodResult
    combined_level: str
    notes: str

    def __post_init__(self) -> None:
        if not self.assessment_id.strip():
            raise RiskAssessmentError("assessment_id must be explicit")
        if self.combined_level not in {"NEGLIGIBLE", "LOW", "MEDIUM", "HIGH", "CRITICAL"}:
            raise RiskAssessmentError("combined_level invalid")
        if self.primary_pc.method_kind == self.secondary_pc.method_kind:
            raise RiskAssessmentError("dual-method requires distinct method_kind")
        if not self.notes.strip():
            raise RiskAssessmentError("notes must be explicit")
