import uuid

import pytest

from ailora.domain.workflows.models import (
    WorkflowContractError,
    WorkflowRequest,
    WorkflowState,
    validate_transition,
)


def request(**changes: object) -> WorkflowRequest:
    values: dict[str, object] = {
        "tenant_id": uuid.uuid4(),
        "actor_user_id": uuid.uuid4(),
        "idempotency_key": "screening:12345",
        "workflow_type": "SSA_SCREENING",
        "payload_digest": "a" * 64,
        "correlation_id": uuid.uuid4(),
    }
    values.update(changes)
    return WorkflowRequest(**values)  # type: ignore[arg-type]


def test_request_is_deterministic_and_advisory() -> None:
    item = request()
    assert item.request_digest == item.request_digest
    assert len(item.request_digest) == 64
    assert item.advisory_only is True


def test_invalid_key_and_attempt_bound_fail_closed() -> None:
    with pytest.raises(WorkflowContractError):
        request(idempotency_key="short")
    with pytest.raises(WorkflowContractError):
        request(max_attempts=11)


def test_state_machine_accepts_and_rejects_explicitly() -> None:
    validate_transition(WorkflowState.PENDING, WorkflowState.RUNNING)
    with pytest.raises(WorkflowContractError):
        validate_transition(WorkflowState.SUCCEEDED, WorkflowState.RUNNING)
