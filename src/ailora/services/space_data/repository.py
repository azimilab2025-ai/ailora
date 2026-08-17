from __future__ import annotations

import uuid
from datetime import datetime
from typing import cast

from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from ailora.services.space_data.models import (
    ProviderAttemptRecord,
    ProviderQualificationRecord,
    ProviderRawArtifactRecord,
)


class ProviderRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    def add_qualification(self, record: ProviderQualificationRecord) -> None:
        self._session.add(record)

    def add_raw_artifact(self, record: ProviderRawArtifactRecord) -> None:
        self._session.add(record)

    def add_attempt(self, record: ProviderAttemptRecord) -> None:
        self._session.add(record)

    async def get_raw_by_digest(
        self, tenant_id: uuid.UUID, provider_id: str, payload_digest: str
    ) -> ProviderRawArtifactRecord | None:
        result = await self._session.scalar(
            select(ProviderRawArtifactRecord).where(
                ProviderRawArtifactRecord.tenant_id == tenant_id,
                ProviderRawArtifactRecord.provider_id == provider_id,
                ProviderRawArtifactRecord.payload_digest == payload_digest,
            )
        )
        return result

    async def get_current_qualification(
        self,
        *,
        provider_id: str,
        provider_version: str,
        now: datetime,
    ) -> ProviderQualificationRecord | None:
        return cast(
            ProviderQualificationRecord | None,
            await self._session.scalar(
                select(ProviderQualificationRecord)
                .where(
                    ProviderQualificationRecord.provider_id == provider_id,
                    ProviderQualificationRecord.provider_version == provider_version,
                    ProviderQualificationRecord.state == "QUALIFIED",
                    (ProviderQualificationRecord.expires_at.is_(None))
                    | (ProviderQualificationRecord.expires_at > now),
                )
                .order_by(desc(ProviderQualificationRecord.reviewed_at))
                .limit(1)
            ),
        )
