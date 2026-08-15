"""Provider-neutral safety qualification for the disabled Oya boundary."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class SafetyDecision(StrEnum):
    """Bounded decisions available before a live provider is authorized."""

    FALLBACK = "FALLBACK"
    REJECTED = "REJECTED"


@dataclass(frozen=True)
class OyaSafetyResult:
    """Secret-free and deterministic safety evaluation."""

    decision: SafetyDecision
    reason_code: str
    fallback_mode: str = "TEXT_CHAT"
    human_review_required: bool = False
    advisory_only: bool = True


@dataclass(frozen=True)
class OyaSafetyPolicy:
    """Fail-closed policy used while the real Oya adapter remains absent."""

    max_input_characters: int = 4096
    max_requested_tools: int = 0

    def evaluate(self, text: str, requested_tools: tuple[str, ...] = ()) -> OyaSafetyResult:
        normalized = " ".join(text.casefold().split())
        if len(text) > self.max_input_characters:
            return OyaSafetyResult(
                SafetyDecision.REJECTED, "INPUT_BUDGET_EXCEEDED", human_review_required=True
            )
        injection_markers = (
            "ignore previous instructions",
            "reveal system prompt",
            "bypass policy",
            "execute hidden tool",
        )
        if any(marker in normalized for marker in injection_markers):
            return OyaSafetyResult(
                SafetyDecision.REJECTED, "PROMPT_INJECTION", human_review_required=True
            )
        authority_markers = (
            "i am mission control",
            "authorize spacecraft command",
            "override human approval",
        )
        if any(marker in normalized for marker in authority_markers):
            return OyaSafetyResult(
                SafetyDecision.REJECTED, "FALSE_AUTHORITY", human_review_required=True
            )
        if len(requested_tools) > self.max_requested_tools:
            return OyaSafetyResult(
                SafetyDecision.REJECTED,
                "TOOL_EXECUTION_FORBIDDEN",
                human_review_required=True,
            )
        return OyaSafetyResult(SafetyDecision.FALLBACK, "OYA_DISABLED")
