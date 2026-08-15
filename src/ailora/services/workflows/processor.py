"""Fail-closed bounded processor outcome classification."""

from __future__ import annotations

from dataclasses import dataclass

from ailora.domain.workflows.models import FailureKind, WorkflowState


@dataclass(frozen=True, slots=True)
class ProcessingOutcome:
    target_state: WorkflowState
    failure_kind: FailureKind | None = None
    error_code: str = ""


def classify_processing_outcome(
    *, succeeded: bool, failure_kind: FailureKind | None = None
) -> ProcessingOutcome:
    if succeeded:
        return ProcessingOutcome(WorkflowState.SUCCEEDED)
    if failure_kind is FailureKind.RETRYABLE:
        return ProcessingOutcome(WorkflowState.RETRY_WAIT, failure_kind, "RETRYABLE_FAILURE")
    if failure_kind is None:
        failure_kind = FailureKind.PERMANENT
    return ProcessingOutcome(WorkflowState.FAILED, failure_kind, failure_kind.value)
