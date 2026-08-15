"""Tenant-scoped durable workflow persistence."""

from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from ailora.domain.workflows.models import WorkflowEventRecord, WorkflowRecord


class DuplicateWorkflowError(Exception):
    """The tenant/idempotency key already owns a workflow."""


class WorkflowRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, record: WorkflowRecord) -> WorkflowRecord:
        self._session.add(record)
        try:
            await self._session.flush()
        except IntegrityError as exc:
            raise DuplicateWorkflowError("duplicate tenant idempotency key") from exc
        return record

    async def get_by_key(
        self, *, tenant_id: uuid.UUID, idempotency_key: str
    ) -> WorkflowRecord | None:
        result = await self._session.execute(
            select(WorkflowRecord).where(
                WorkflowRecord.tenant_id == tenant_id,
                WorkflowRecord.idempotency_key == idempotency_key,
            )
        )
        return result.scalar_one_or_none()

    async def get_for_update(
        self, *, tenant_id: uuid.UUID, workflow_id: uuid.UUID
    ) -> WorkflowRecord | None:
        result = await self._session.execute(
            select(WorkflowRecord)
            .where(WorkflowRecord.tenant_id == tenant_id, WorkflowRecord.id == workflow_id)
            .with_for_update()
        )
        return result.scalar_one_or_none()

    async def append_event(self, event: WorkflowEventRecord) -> WorkflowEventRecord:
        self._session.add(event)
        await self._session.flush()
        return event

    async def events(
        self, *, tenant_id: uuid.UUID, workflow_id: uuid.UUID
    ) -> list[WorkflowEventRecord]:
        result = await self._session.scalars(
            select(WorkflowEventRecord)
            .where(
                WorkflowEventRecord.tenant_id == tenant_id,
                WorkflowEventRecord.workflow_id == workflow_id,
            )
            .order_by(WorkflowEventRecord.sequence_number)
        )
        return list(result.all())
