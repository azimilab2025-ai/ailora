"""Transactional durable-workflow application service."""

from __future__ import annotations

import hashlib
import uuid
from datetime import UTC, datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from ailora.domain.workflows.models import (
    FailureKind,
    WorkflowContractError,
    WorkflowEventRecord,
    WorkflowRecord,
    WorkflowRequest,
    WorkflowState,
    deterministic_backoff_seconds,
    validate_transition,
)
from ailora.domain.workflows.repository import DuplicateWorkflowError, WorkflowRepository


class WorkflowNotFoundError(Exception):
    pass


class IdempotencyConflictError(Exception):
    pass


class WorkflowService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._repository = WorkflowRepository(session)

    async def submit(self, request: WorkflowRequest) -> tuple[WorkflowRecord, bool]:
        existing = await self._repository.get_by_key(
            tenant_id=request.tenant_id, idempotency_key=request.idempotency_key
        )
        if existing is not None:
            if existing.request_digest != request.request_digest:
                raise IdempotencyConflictError("idempotency key payload mismatch")
            return existing, True
        record = WorkflowRecord(
            tenant_id=request.tenant_id,
            actor_user_id=request.actor_user_id,
            idempotency_key=request.idempotency_key,
            workflow_type=request.workflow_type,
            request_digest=request.request_digest,
            payload_digest=request.payload_digest,
            correlation_id=request.correlation_id,
            causation_id=request.causation_id,
            state=WorkflowState.PENDING.value,
            max_attempts=request.max_attempts,
            advisory_only=True,
        )
        try:
            await self._repository.create(record)
        except DuplicateWorkflowError:
            winner = await self._repository.get_by_key(
                tenant_id=request.tenant_id, idempotency_key=request.idempotency_key
            )
            if winner is None or winner.request_digest != request.request_digest:
                raise IdempotencyConflictError("concurrent idempotency conflict") from None
            return winner, True
        await self._event(record, None, WorkflowState.PENDING, "WORKFLOW_ACCEPTED")
        return record, False

    async def transition(
        self,
        *,
        tenant_id: uuid.UUID,
        workflow_id: uuid.UUID,
        actor_user_id: uuid.UUID,
        target: WorkflowState,
        failure_kind: FailureKind | None = None,
        error_code: str = "",
    ) -> WorkflowRecord:
        record = await self._repository.get_for_update(tenant_id=tenant_id, workflow_id=workflow_id)
        if record is None:
            raise WorkflowNotFoundError("workflow not found")
        current = WorkflowState(record.state)
        validate_transition(current, target)
        if target is WorkflowState.RUNNING:
            record.attempt_count += 1
            record.lease_token = uuid.uuid4()
        if target is WorkflowState.RETRY_WAIT:
            if failure_kind is not FailureKind.RETRYABLE:
                raise WorkflowContractError("only retryable failures may enter retry wait")
            if record.attempt_count >= record.max_attempts:
                target = WorkflowState.FAILED
                error_code = "RETRY_EXHAUSTED"
            else:
                delay = deterministic_backoff_seconds(record.attempt_count)
                record.next_attempt_at = datetime.now(tz=UTC) + timedelta(seconds=delay)
        if target in {WorkflowState.SUCCEEDED, WorkflowState.FAILED, WorkflowState.CANCELLED}:
            record.completed_at = datetime.now(tz=UTC)
            record.lease_token = None
        previous = current
        record.state = target.value
        record.failure_kind = failure_kind.value if failure_kind else ""
        record.error_code = error_code.strip()[:64]
        record.version += 1
        record.updated_at = datetime.now(tz=UTC)
        record.actor_user_id = actor_user_id
        await self._event(record, previous, target, f"WORKFLOW_{target.value}")
        await self._session.flush()
        return record

    async def replay(self, *, tenant_id: uuid.UUID, workflow_id: uuid.UUID) -> tuple[str, ...]:
        events = await self._repository.events(tenant_id=tenant_id, workflow_id=workflow_id)
        if not events:
            raise WorkflowNotFoundError("workflow event history not found")
        expected = list(range(1, len(events) + 1))
        observed = [event.sequence_number for event in events]
        if observed != expected:
            raise WorkflowContractError("workflow event sequence is not contiguous")
        return tuple(event.to_state for event in events)

    async def _event(
        self,
        record: WorkflowRecord,
        previous: WorkflowState | None,
        target: WorkflowState,
        event_type: str,
    ) -> None:
        record.event_count += 1
        material = ":".join(
            (
                str(record.id),
                str(record.event_count),
                previous.value if previous else "NONE",
                target.value,
                record.request_digest,
            )
        )
        await self._repository.append_event(
            WorkflowEventRecord(
                workflow_id=record.id,
                tenant_id=record.tenant_id,
                sequence_number=record.event_count,
                event_type=event_type,
                from_state=previous.value if previous else "",
                to_state=target.value,
                actor_user_id=record.actor_user_id,
                correlation_id=record.correlation_id,
                causation_id=record.causation_id,
                evidence_digest=hashlib.sha256(material.encode()).hexdigest(),
                advisory_only=True,
            )
        )
