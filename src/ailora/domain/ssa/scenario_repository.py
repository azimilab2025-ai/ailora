"""Tenant-filtered database access for advisory SSA scenarios."""

from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ailora.domain.ssa.scenario_models import ScenarioRecord


class ScenarioRepository:
    """Repository whose read operations require an explicit verified tenant."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, record: ScenarioRecord) -> ScenarioRecord:
        self._session.add(record)
        await self._session.flush()
        return record

    async def list_for_tenant(self, tenant_id: uuid.UUID) -> list[ScenarioRecord]:
        statement = (
            select(ScenarioRecord)
            .where(ScenarioRecord.tenant_id == tenant_id)
            .order_by(ScenarioRecord.created_at, ScenarioRecord.id)
        )
        return list((await self._session.scalars(statement)).all())

    async def get_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        scenario_id: uuid.UUID,
    ) -> ScenarioRecord | None:
        statement = select(ScenarioRecord).where(
            ScenarioRecord.id == scenario_id,
            ScenarioRecord.tenant_id == tenant_id,
        )
        result = await self._session.execute(statement)
        return result.scalar_one_or_none()
