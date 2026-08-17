"""Append-only tenant-filtered persistence for SSA audit evidence."""

from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ailora.domain.ssa.audit_integrity import assign_chain_values
from ailora.domain.ssa.audit_models import AuditEventRecord


class AuditEventRepository:
    """Audit repository intentionally exposing append and scoped reads only."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def append(self, record: AuditEventRecord) -> AuditEventRecord:
        previous = await self._session.scalar(
            select(AuditEventRecord)
            .where(AuditEventRecord.tenant_id == record.tenant_id)
            .order_by(AuditEventRecord.sequence_no.desc())
            .limit(1)
        )
        assign_chain_values(
            record,
            previous_sequence=previous.sequence_no if previous else None,
            previous_hash=previous.event_hash if previous else None,
        )
        self._session.add(record)
        await self._session.flush()
        if self._session.bind and self._session.bind.dialect.name == "postgresql":
            await self._session.refresh(
                record,
                attribute_names=["sequence_no", "previous_hash", "event_hash"],
            )
        return record

    async def list_for_tenant(self, tenant_id: uuid.UUID) -> list[AuditEventRecord]:
        statement = (
            select(AuditEventRecord)
            .where(AuditEventRecord.tenant_id == tenant_id)
            .order_by(AuditEventRecord.sequence_no, AuditEventRecord.id)
        )
        return list((await self._session.scalars(statement)).all())

    async def get_for_tenant(
        self, *, tenant_id: uuid.UUID, event_id: uuid.UUID
    ) -> AuditEventRecord | None:
        statement = select(AuditEventRecord).where(
            AuditEventRecord.tenant_id == tenant_id,
            AuditEventRecord.id == event_id,
        )
        return (await self._session.execute(statement)).scalar_one_or_none()
