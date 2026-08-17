from __future__ import annotations

import uuid
from typing import cast

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ailora.domain.space_data.models import (
    FrameTransformationEvidenceRecord,
    SpaceDataEvidenceRecord,
    SpaceDataObservationRecord,
    SpaceDataQuarantineRecord,
)


class SpaceDataRepository:
    def __init__(self, database: AsyncSession) -> None:
        self._database = database

    async def find_by_digest(
        self, *, tenant_id: uuid.UUID, canonical_digest: str
    ) -> SpaceDataObservationRecord | None:
        statement = select(SpaceDataObservationRecord).where(
            SpaceDataObservationRecord.tenant_id == tenant_id,
            SpaceDataObservationRecord.canonical_digest == canonical_digest,
        )
        return cast(
            SpaceDataObservationRecord | None,
            await self._database.scalar(statement),
        )

    async def get_observation(
        self, *, tenant_id: uuid.UUID, observation_id: str
    ) -> SpaceDataObservationRecord | None:
        statement = select(SpaceDataObservationRecord).where(
            SpaceDataObservationRecord.tenant_id == tenant_id,
            SpaceDataObservationRecord.id == observation_id,
        )
        return cast(
            SpaceDataObservationRecord | None,
            await self._database.scalar(statement),
        )

    async def add_observation(
        self, record: SpaceDataObservationRecord
    ) -> SpaceDataObservationRecord:
        self._database.add(record)
        await self._database.flush()
        return record

    async def add_quarantine(self, record: SpaceDataQuarantineRecord) -> SpaceDataQuarantineRecord:
        self._database.add(record)
        await self._database.flush()
        return record

    async def add_evidence(self, record: SpaceDataEvidenceRecord) -> SpaceDataEvidenceRecord:
        self._database.add(record)
        await self._database.flush()
        return record

    async def find_transformation_by_digest(
        self, *, tenant_id: uuid.UUID, transformation_digest: str
    ) -> FrameTransformationEvidenceRecord | None:
        statement = select(FrameTransformationEvidenceRecord).where(
            FrameTransformationEvidenceRecord.tenant_id == tenant_id,
            FrameTransformationEvidenceRecord.transformation_digest == transformation_digest,
        )
        return cast(
            FrameTransformationEvidenceRecord | None,
            await self._database.scalar(statement),
        )

    async def add_transformation(
        self, record: FrameTransformationEvidenceRecord
    ) -> FrameTransformationEvidenceRecord:
        self._database.add(record)
        await self._database.flush()
        return record
