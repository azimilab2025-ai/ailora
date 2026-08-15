import pytest

from ailora.domain.workflows.models import (
    FailureKind,
    WorkflowContractError,
    deterministic_backoff_seconds,
)
from ailora.services.workflows.processor import classify_processing_outcome


def test_backoff_is_bounded_and_deterministic() -> None:
    assert [deterministic_backoff_seconds(i, cap_seconds=4.0) for i in range(1, 5)] == [
        1.0,
        2.0,
        4.0,
        4.0,
    ]


def test_invalid_retry_configuration_is_rejected() -> None:
    with pytest.raises(WorkflowContractError):
        deterministic_backoff_seconds(0)


def test_permanent_failure_is_not_retryable() -> None:
    result = classify_processing_outcome(succeeded=False, failure_kind=FailureKind.PERMANENT)
    assert result.target_state.value == "FAILED"


def test_retryable_failure_is_explicit() -> None:
    result = classify_processing_outcome(succeeded=False, failure_kind=FailureKind.RETRYABLE)
    assert result.target_state.value == "RETRY_WAIT"
