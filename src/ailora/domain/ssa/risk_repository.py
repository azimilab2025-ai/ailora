"""Tenant-, scenario-, and screening-filtered risk persistence."""

from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ailora.domain.ssa.risk_models import RiskAssessmentRecord


class RiskAssessmentRepository:
    """Every read requires the complete verified ownership path."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, record: RiskAssessmentRecord) -> RiskAssessmentRecord:
        self._session.add(record)
        await self._session.flush()
        return record

    async def list_for_scope(
        self,
        *,
        tenant_id: uuid.UUID,
        scenario_id: uuid.UUID,
        screening_id: uuid.UUID,
    ) -> list[RiskAssessmentRecord]:
        statement = (
            select(RiskAssessmentRecord)
            .where(
                RiskAssessmentRecord.tenant_id == tenant_id,
                RiskAssessmentRecord.scenario_id == scenario_id,
                RiskAssessmentRecord.screening_id == screening_id,
            )
            .order_by(RiskAssessmentRecord.created_at, RiskAssessmentRecord.id)
        )
        result = await self._session.scalars(statement)
        return list(result.all())

    async def get_for_scope(
        self,
        *,
        tenant_id: uuid.UUID,
        scenario_id: uuid.UUID,
        screening_id: uuid.UUID,
        assessment_id: uuid.UUID,
    ) -> RiskAssessmentRecord | None:
        statement = select(RiskAssessmentRecord).where(
            RiskAssessmentRecord.id == assessment_id,
            RiskAssessmentRecord.tenant_id == tenant_id,
            RiskAssessmentRecord.scenario_id == scenario_id,
            RiskAssessmentRecord.screening_id == screening_id,
        )
        result = await self._session.execute(statement)
        return result.scalar_one_or_none()
