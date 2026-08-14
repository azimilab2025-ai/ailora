"""Tenant- and scenario-filtered persistence for advisory screenings."""

from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ailora.domain.ssa.screening_models import ScreeningRecord


class ScreeningRepository:
    """Every read requires both verified tenant and scenario identifiers."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, record: ScreeningRecord) -> ScreeningRecord:
        self._session.add(record)
        await self._session.flush()
        return record

    async def list_for_tenant_scenario(
        self,
        *,
        tenant_id: uuid.UUID,
        scenario_id: uuid.UUID,
    ) -> list[ScreeningRecord]:
        statement = (
            select(ScreeningRecord)
            .where(
                ScreeningRecord.tenant_id == tenant_id,
                ScreeningRecord.scenario_id == scenario_id,
            )
            .order_by(ScreeningRecord.created_at, ScreeningRecord.id)
        )
        result = await self._session.scalars(statement)
        return list(result.all())

    async def get_for_tenant_scenario(
        self,
        *,
        tenant_id: uuid.UUID,
        scenario_id: uuid.UUID,
        screening_id: uuid.UUID,
    ) -> ScreeningRecord | None:
        statement = select(ScreeningRecord).where(
            ScreeningRecord.id == screening_id,
            ScreeningRecord.tenant_id == tenant_id,
            ScreeningRecord.scenario_id == scenario_id,
        )
        result = await self._session.execute(statement)
        return result.scalar_one_or_none()
