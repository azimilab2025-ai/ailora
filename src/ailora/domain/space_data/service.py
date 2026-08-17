from __future__ import annotations

import re
import uuid
from datetime import UTC, datetime
from enum import StrEnum

from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from ailora.domain.space_data.contracts import ObservationEnvelope, canonical_payload_digest
from ailora.domain.space_data.models import (
    SpaceDataEvidenceRecord,
    SpaceDataObservationRecord,
    SpaceDataQuarantineRecord,
)
from ailora.domain.space_data.repository import SpaceDataRepository

_SECRET = re.compile(r"(?i)(password|secret|token|api[_-]?key|authorization|bearer)\s*[:=]")
_DIGEST = re.compile(r"^[0-9a-f]{64}$")


class IngestionStatus(StrEnum):
    ACCEPTED = "ACCEPTED"
    QUARANTINED = "QUARANTINED"
    DUPLICATE = "DUPLICATE"
    REPLAYED = "REPLAYED"


class ObservationNotFoundError(Exception):
    pass


class IngestionResult:
    def __init__(
        self,
        *,
        status: IngestionStatus,
        observation_id: str | None,
        evidence_id: str,
        canonical_digest: str,
    ) -> None:
        self.status = status
        self.observation_id = observation_id
        self.evidence_id = evidence_id
        self.canonical_digest = canonical_digest


def _safe_detail(error: ValidationError) -> str:
    detail = "; ".join(
        f"{'.'.join(str(item) for item in entry['loc'])}: {entry['msg']}"
        for entry in error.errors(include_url=False, include_input=False)
    )
    if _SECRET.search(detail):
        return "validation failed; sensitive detail redacted"
    return detail[:512]


class SpaceDataIngestionService:
    def __init__(
        self,
        database: AsyncSession,
        *,
        repository: SpaceDataRepository | None = None,
    ) -> None:
        self._database = database
        self._repository = repository or SpaceDataRepository(database)

    async def ingest(
        self,
        *,
        tenant_id: uuid.UUID,
        actor_user_id: uuid.UUID,
        payload: dict[str, object],
    ) -> IngestionResult:
        now = datetime.now(tz=UTC)
        canonical_digest = canonical_payload_digest(payload)
        supplied_tenant = payload.get("tenant_id")
        if str(supplied_tenant) != str(tenant_id):
            return await self._quarantine(
                tenant_id=tenant_id,
                actor_user_id=actor_user_id,
                digest=canonical_digest,
                detail="tenant_id: payload tenant does not match authorized tenant",
                now=now,
            )

        try:
            envelope = ObservationEnvelope.model_validate(payload)
        except ValidationError as error:
            return await self._quarantine(
                tenant_id=tenant_id,
                actor_user_id=actor_user_id,
                digest=canonical_digest,
                detail=_safe_detail(error),
                now=now,
            )

        canonical_digest = envelope.provenance.canonical_digest
        existing = await self._repository.find_by_digest(
            tenant_id=tenant_id,
            canonical_digest=canonical_digest,
        )
        if existing is not None:
            evidence = self._evidence(
                tenant_id=tenant_id,
                actor_user_id=actor_user_id,
                event_type=IngestionStatus.DUPLICATE,
                resource_id=existing.id,
                digest=canonical_digest,
                detail="duplicate canonical digest resolved idempotently",
                now=now,
            )
            await self._repository.add_evidence(evidence)
            return IngestionResult(
                status=IngestionStatus.DUPLICATE,
                observation_id=existing.id,
                evidence_id=evidence.id,
                canonical_digest=canonical_digest,
            )

        record = SpaceDataObservationRecord(
            id=envelope.processing_id.hex,
            tenant_id=tenant_id,
            observation_id=envelope.observation_id,
            object_id=envelope.object_id,
            schema_version=envelope.schema_version.value,
            reference_frame=envelope.reference_frame.value,
            distance_unit=envelope.distance_unit.value,
            velocity_unit=envelope.velocity_unit.value,
            time_scale=envelope.time_scale.value,
            epoch=envelope.epoch,
            evaluated_at=envelope.evaluated_at,
            max_age_seconds=envelope.max_age_seconds,
            position=list(envelope.position),
            velocity=list(envelope.velocity),
            covariance=(
                [list(row) for row in envelope.covariance]
                if envelope.covariance is not None
                else None
            ),
            quality=envelope.quality.value,
            source_id=envelope.provenance.source_id,
            source_version=envelope.provenance.source_version,
            ingested_at=envelope.provenance.ingested_at,
            canonical_digest=canonical_digest,
            classification=envelope.provenance.classification.value,
            advisory_only=True,
            created_at=now,
        )
        evidence = self._evidence(
            tenant_id=tenant_id,
            actor_user_id=actor_user_id,
            event_type=IngestionStatus.ACCEPTED,
            resource_id=record.id,
            digest=canonical_digest,
            detail="validated space-data observation accepted",
            now=now,
        )
        await self._repository.add_observation(record)
        await self._repository.add_evidence(evidence)
        return IngestionResult(
            status=IngestionStatus.ACCEPTED,
            observation_id=record.id,
            evidence_id=evidence.id,
            canonical_digest=canonical_digest,
        )

    async def replay(
        self,
        *,
        tenant_id: uuid.UUID,
        actor_user_id: uuid.UUID,
        source_observation_id: str,
    ) -> IngestionResult:
        source = await self._repository.get_observation(
            tenant_id=tenant_id,
            observation_id=source_observation_id,
        )
        if source is None:
            raise ObservationNotFoundError("source observation was not found")
        replay_processing_id = uuid.uuid4().hex
        evidence = self._evidence(
            tenant_id=tenant_id,
            actor_user_id=actor_user_id,
            event_type=IngestionStatus.REPLAYED,
            resource_id=replay_processing_id,
            digest=source.canonical_digest,
            detail=(
                f"replay of {source.id} preserving source "
                f"{source.source_id}@{source.source_version}"
            ),
            now=datetime.now(tz=UTC),
        )
        await self._repository.add_evidence(evidence)
        return IngestionResult(
            status=IngestionStatus.REPLAYED,
            observation_id=replay_processing_id,
            evidence_id=evidence.id,
            canonical_digest=source.canonical_digest,
        )

    async def quarantine_source_failure(
        self,
        *,
        tenant_id: uuid.UUID,
        actor_user_id: uuid.UUID,
        source_digest: str,
    ) -> IngestionResult:
        """Persist sanitized evidence when source transformation fails closed."""
        if not _DIGEST.fullmatch(source_digest):
            raise ValueError("source_digest must be a lowercase SHA-256 digest")
        return await self._quarantine(
            tenant_id=tenant_id,
            actor_user_id=actor_user_id,
            digest=source_digest,
            detail="provider payload could not be transformed into a validated observation",
            now=datetime.now(tz=UTC),
            reason_code="SOURCE_TRANSFORMATION_FAILED",
        )

    async def _quarantine(
        self,
        *,
        tenant_id: uuid.UUID,
        actor_user_id: uuid.UUID,
        digest: str,
        detail: str,
        now: datetime,
        reason_code: str = "SEMANTIC_VALIDATION_FAILED",
    ) -> IngestionResult:
        quarantine = SpaceDataQuarantineRecord(
            id=uuid.uuid4().hex,
            tenant_id=tenant_id,
            actor_user_id=actor_user_id,
            canonical_digest=digest,
            reason_code=reason_code,
            reason_detail=detail,
            classification="INTERNAL",
            advisory_only=True,
            created_at=now,
        )
        evidence = self._evidence(
            tenant_id=tenant_id,
            actor_user_id=actor_user_id,
            event_type=IngestionStatus.QUARANTINED,
            resource_id=quarantine.id,
            digest=digest,
            detail="space-data payload quarantined",
            now=now,
        )
        await self._repository.add_quarantine(quarantine)
        await self._repository.add_evidence(evidence)
        return IngestionResult(
            status=IngestionStatus.QUARANTINED,
            observation_id=None,
            evidence_id=evidence.id,
            canonical_digest=digest,
        )

    @staticmethod
    def _evidence(
        *,
        tenant_id: uuid.UUID,
        actor_user_id: uuid.UUID,
        event_type: IngestionStatus,
        resource_id: str,
        digest: str,
        detail: str,
        now: datetime,
    ) -> SpaceDataEvidenceRecord:
        return SpaceDataEvidenceRecord(
            id=uuid.uuid4().hex,
            tenant_id=tenant_id,
            actor_user_id=actor_user_id,
            event_type=event_type.value,
            resource_id=resource_id,
            canonical_digest=digest,
            detail=detail,
            advisory_only=True,
            created_at=now,
        )
