from __future__ import annotations

import hashlib
import uuid
from dataclasses import dataclass
from datetime import datetime

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from ailora.services.space_data.governance import (
    ProviderQualification,
    QualificationGate,
)
from ailora.services.space_data.interfaces import (
    ProviderError,
    ProviderRequest,
    ProviderResponseError,
    SpaceDataProvider,
)
from ailora.services.space_data.models import (
    ProviderAttemptRecord,
    ProviderRawArtifactRecord,
)
from ailora.services.space_data.repository import ProviderRepository


@dataclass(frozen=True, slots=True)
class ProviderIngestionResult:
    raw_artifact_id: str
    payload_digest: str
    duplicate: bool
    advisory_only: bool = True


class ProviderIngestionService:
    def __init__(
        self,
        session: AsyncSession,
        provider: SpaceDataProvider,
        qualification_gate: QualificationGate,
    ) -> None:
        self._session = session
        self._provider = provider
        self._gate = qualification_gate
        self._repository = ProviderRepository(session)

    async def ingest(
        self,
        *,
        tenant_id: uuid.UUID,
        actor_user_id: uuid.UUID,
        request: ProviderRequest,
        qualification: ProviderQualification,
        classification: str,
        now: datetime,
    ) -> ProviderIngestionResult:
        self._gate.require(qualification, now)
        try:
            response = await self._provider.fetch(request)
            if (
                response.provider_id != qualification.provider_id
                or response.provider_version != qualification.provider_version
            ):
                raise ProviderResponseError("provider identity does not match qualification")
        except ProviderError as exc:
            failed_attempt = ProviderAttemptRecord(
                id=uuid.uuid4().hex,
                tenant_id=tenant_id,
                actor_user_id=actor_user_id,
                raw_artifact_id=None,
                request_id=request.request_id.hex,
                provider_id=qualification.provider_id,
                status="FAILED",
                error_code=exc.code.value,
                error_detail=exc.code.value,
                attempt_count=1,
                started_at=now,
                completed_at=now,
                advisory_only=True,
            )
            self._repository.add_attempt(failed_attempt)
            await self._commit()
            raise
        digest = hashlib.sha256(response.payload).hexdigest()
        existing = await self._repository.get_raw_by_digest(tenant_id, response.provider_id, digest)
        if existing is not None:
            duplicate_attempt = ProviderAttemptRecord(
                id=uuid.uuid4().hex,
                tenant_id=tenant_id,
                actor_user_id=actor_user_id,
                raw_artifact_id=existing.id,
                request_id=request.request_id.hex,
                provider_id=response.provider_id,
                status="DUPLICATE",
                error_code="NONE",
                error_detail="",
                attempt_count=1,
                started_at=now,
                completed_at=now,
                advisory_only=True,
            )
            self._repository.add_attempt(duplicate_attempt)
            await self._commit()
            return ProviderIngestionResult(existing.id, digest, duplicate=True)
        raw_id = uuid.uuid4().hex
        raw = ProviderRawArtifactRecord(
            id=raw_id,
            tenant_id=tenant_id,
            actor_user_id=actor_user_id,
            qualification_id=qualification.qualification_id.hex,
            request_id=request.request_id.hex,
            provider_id=response.provider_id,
            provider_version=response.provider_version,
            external_object_id=response.object_id,
            status_code=response.status_code,
            content_type=response.content_type,
            fetched_at=response.fetched_at,
            payload=response.payload,
            byte_length=len(response.payload),
            payload_digest=digest,
            classification=classification,
            attribution_text=qualification.attribution_text,
            advisory_only=True,
            created_at=now,
        )
        attempt = ProviderAttemptRecord(
            id=uuid.uuid4().hex,
            tenant_id=tenant_id,
            actor_user_id=actor_user_id,
            raw_artifact_id=raw_id,
            request_id=request.request_id.hex,
            provider_id=response.provider_id,
            status="RAW_STORED",
            error_code="NONE",
            error_detail="",
            attempt_count=1,
            started_at=now,
            completed_at=now,
            advisory_only=True,
        )
        self._repository.add_raw_artifact(raw)
        self._repository.add_attempt(attempt)
        await self._commit()
        return ProviderIngestionResult(raw_id, digest, duplicate=False)

    async def _commit(self) -> None:
        try:
            await self._session.commit()
        except SQLAlchemyError:
            await self._session.rollback()
            raise
