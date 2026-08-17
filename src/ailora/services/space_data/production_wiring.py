"""Production composition from governed CelesTrak bytes to persisted GCRF evidence."""

from __future__ import annotations

import uuid
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from ailora.config import Settings
from ailora.domain.identity.models import Membership, Tenant, User
from ailora.domain.space_data.contracts import (
    DataQuality,
    DistanceUnit,
    ReferenceFrame,
    SchemaVersion,
    SpaceDataClassification,
    TimeScale,
    VelocityUnit,
    canonical_payload_digest,
)
from ailora.domain.space_data.models import FrameTransformationEvidenceRecord
from ailora.domain.space_data.repository import SpaceDataRepository
from ailora.domain.space_data.service import IngestionStatus, SpaceDataIngestionService
from ailora.security.authorization import (
    AuthorizationDeniedError,
    Permission,
    authorize_tenant_membership,
)
from ailora.services.astrodynamics.frame_transform import (
    FrameTransformationError,
    OfflineTemeToGcrfTransformer,
)
from ailora.services.space_data.governance import (
    ProviderQualification,
    QualificationState,
)
from ailora.services.space_data.interfaces import ProviderRequest
from ailora.services.space_data.models import ProviderQualificationRecord
from ailora.services.space_data.repository import ProviderRepository
from ailora.services.space_data.runtime import build_live_provider_ingestion_service
from ailora.services.space_data.service import ProviderIngestionService
from ailora.services.space_data.tle_bridge import TLEObservationBridge


class ProductionWiringErrorCode(StrEnum):
    ACCESS_DENIED = "ACCESS_DENIED"
    QUALIFICATION_REQUIRED = "QUALIFICATION_REQUIRED"
    SOURCE_TRANSFORMATION_FAILED = "SOURCE_TRANSFORMATION_FAILED"
    PERSISTENCE_FAILED = "PERSISTENCE_FAILED"


class ProductionWiringError(RuntimeError):
    def __init__(self, code: ProductionWiringErrorCode) -> None:
        super().__init__(code.value)
        self.code = code


@dataclass(frozen=True, slots=True)
class ProductionIngestionResult:
    status: IngestionStatus
    raw_artifact_id: str
    raw_payload_digest: str
    raw_duplicate: bool
    native_teme_observation_id: str | None
    gcrf_observation_id: str | None
    gcrf_canonical_digest: str | None
    transformation_digest: str | None
    target_frame: str | None
    advisory_only: bool = True


def _aware(value: datetime) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        return value.replace(tzinfo=UTC)
    return value.astimezone(UTC)


def _qualification(record: ProviderQualificationRecord) -> ProviderQualification:
    return ProviderQualification(
        qualification_id=uuid.UUID(str(record.id)),
        provider_id=str(record.provider_id),
        provider_version=str(record.provider_version),
        state=QualificationState(str(record.state)),
        license_name=str(record.license_name),
        terms_uri=str(record.terms_uri),
        terms_digest=str(record.terms_digest),
        retrieved_at=_aware(record.retrieved_at),
        reviewed_at=_aware(record.reviewed_at),
        expires_at=(_aware(record.expires_at) if record.expires_at is not None else None),
        reviewer_reference=str(record.reviewer_reference),
        redistribution_permitted=bool(record.redistribution_permitted),
        attribution_text=str(record.attribution_text),
    )


class ProductionSpaceDataPipeline:
    """Execute the authorized provider→TEME→GCRF path with append-only evidence."""

    def __init__(
        self,
        session: AsyncSession,
        settings: Settings,
        clock: Callable[[], datetime],
        sleeper: Callable[[float], Awaitable[None]],
        *,
        provider_ingestion: ProviderIngestionService | None = None,
        transformer: OfflineTemeToGcrfTransformer | None = None,
    ) -> None:
        self._session = session
        self._settings = settings
        self._clock = clock
        self._provider_ingestion = provider_ingestion or build_live_provider_ingestion_service(
            session=session,
            settings=settings,
            clock=clock,
            sleeper=sleeper,
        )
        self._transformer = transformer or OfflineTemeToGcrfTransformer()
        self._space_repository = SpaceDataRepository(session)
        self._provider_repository = ProviderRepository(session)

    async def _authorize_writer(self, *, actor_user_id: uuid.UUID, tenant_id: uuid.UUID) -> None:
        statement = (
            select(User, Tenant, Membership)
            .join(Membership, Membership.user_id == User.id)
            .join(Tenant, Tenant.id == Membership.tenant_id)
            .where(
                User.id == actor_user_id,
                Tenant.id == tenant_id,
                Membership.user_id == actor_user_id,
                Membership.tenant_id == tenant_id,
            )
        )
        row = (await self._session.execute(statement)).one_or_none()
        if row is None:
            raise ProductionWiringError(ProductionWiringErrorCode.ACCESS_DENIED)
        user, tenant, membership = row
        role = membership.role.value if hasattr(membership.role, "value") else str(membership.role)
        policy_role = {"owner": "admin", "member": "analyst"}.get(role, role)
        try:
            authorize_tenant_membership(
                authenticated_user_id=actor_user_id,
                requested_tenant_id=tenant_id,
                membership_user_id=membership.user_id,
                membership_tenant_id=membership.tenant_id,
                membership_role=policy_role,
                user_active=user.is_active,
                tenant_active=tenant.is_active,
                membership_active=membership.is_active,
                required_permission=Permission.TENANT_WRITE,
            )
        except AuthorizationDeniedError as exc:
            raise ProductionWiringError(ProductionWiringErrorCode.ACCESS_DENIED) from exc

    async def ingest_gcrf(
        self,
        *,
        tenant_id: uuid.UUID,
        actor_user_id: uuid.UUID,
        object_id: str,
        evaluated_at: datetime,
        idempotency_key: str,
        classification: SpaceDataClassification,
    ) -> ProductionIngestionResult:
        await self._authorize_writer(actor_user_id=actor_user_id, tenant_id=tenant_id)
        now = _aware(self._clock())
        qualification_record = await self._provider_repository.get_current_qualification(
            provider_id="CELESTRAK",
            provider_version="gp-v1",
            now=now,
        )
        if qualification_record is None:
            raise ProductionWiringError(ProductionWiringErrorCode.QUALIFICATION_REQUIRED)
        request_id = uuid.uuid5(tenant_id, idempotency_key)
        acquisition = await self._provider_ingestion.acquire(
            tenant_id=tenant_id,
            actor_user_id=actor_user_id,
            request=ProviderRequest(
                request_id=request_id,
                object_id=object_id,
                evaluated_at=evaluated_at,
                purpose="production advisory GCRF observation ingestion",
            ),
            qualification=_qualification(qualification_record),
            classification=classification.value,
            now=now,
        )
        native = await TLEObservationBridge(self._session).ingest(
            tenant_id=tenant_id,
            actor_user_id=actor_user_id,
            response=acquisition.response,
            evaluated_at=evaluated_at,
            classification=classification,
        )
        await self._session.commit()
        if native.observation_id is None:
            return ProductionIngestionResult(
                status=native.status,
                raw_artifact_id=acquisition.ingestion.raw_artifact_id,
                raw_payload_digest=acquisition.ingestion.payload_digest,
                raw_duplicate=acquisition.ingestion.duplicate,
                native_teme_observation_id=None,
                gcrf_observation_id=None,
                gcrf_canonical_digest=None,
                transformation_digest=None,
                target_frame=None,
            )
        native_record = await self._space_repository.get_observation(
            tenant_id=tenant_id,
            observation_id=native.observation_id,
        )
        if native_record is None or native_record.reference_frame != "TEME":
            raise ProductionWiringError(ProductionWiringErrorCode.SOURCE_TRANSFORMATION_FAILED)
        try:
            transformed = self._transformer.transform(
                native_record.position,
                native_record.velocity,
                _aware(native_record.epoch),
            )
            provenance: dict[str, object] = {
                "source_id": native_record.source_id,
                "source_version": (
                    f"{native_record.source_version[:54]}|GCRF-{transformed.transformation_digest}"
                ),
                "ingested_at": _aware(native_record.ingested_at),
                "canonical_digest": "0" * 64,
                "classification": classification,
            }
            payload: dict[str, object] = {
                "tenant_id": tenant_id,
                "observation_id": f"GCRF:{request_id.hex}",
                "object_id": native_record.object_id,
                "schema_version": SchemaVersion.V1,
                "reference_frame": ReferenceFrame.GCRF,
                "distance_unit": DistanceUnit.KILOMETER,
                "velocity_unit": VelocityUnit.KILOMETER_PER_SECOND,
                "time_scale": TimeScale.UTC,
                "epoch": transformed.epoch,
                "evaluated_at": transformed.epoch,
                "max_age_seconds": 0.0,
                "position": transformed.position_km,
                "velocity": transformed.velocity_km_s,
                "covariance": None,
                "quality": DataQuality.VALID,
                "provenance": provenance,
                "advisory_only": True,
            }
            provenance["canonical_digest"] = canonical_payload_digest(payload)
            gcrf = await SpaceDataIngestionService(self._session).ingest(
                tenant_id=tenant_id,
                actor_user_id=actor_user_id,
                payload=payload,
            )
            if gcrf.observation_id is None:
                raise ProductionWiringError(ProductionWiringErrorCode.SOURCE_TRANSFORMATION_FAILED)
            existing = await self._space_repository.find_transformation_by_digest(
                tenant_id=tenant_id,
                transformation_digest=transformed.transformation_digest,
            )
            if existing is None:
                await self._space_repository.add_transformation(
                    FrameTransformationEvidenceRecord(
                        id=uuid.uuid4().hex,
                        tenant_id=tenant_id,
                        actor_user_id=actor_user_id,
                        raw_artifact_id=acquisition.ingestion.raw_artifact_id,
                        native_observation_id=native_record.id,
                        gcrf_observation_id=gcrf.observation_id,
                        epoch=transformed.epoch,
                        source_frame=transformed.source_frame,
                        target_frame=transformed.target_frame,
                        frame_realization=transformed.frame_realization,
                        algorithm_id=transformed.algorithm_id,
                        algorithm_version=transformed.algorithm_version,
                        astropy_version=transformed.astropy_version,
                        iers_data_version=transformed.iers_data_version,
                        iers_source=transformed.iers_source,
                        iers_mjd_start=transformed.iers_mjd_start,
                        iers_mjd_end=transformed.iers_mjd_end,
                        eop_status=transformed.eop_status,
                        input_digest=transformed.input_digest,
                        iers_data_digest=transformed.iers_data_digest,
                        transformation_digest=transformed.transformation_digest,
                        source_position=list(native_record.position),
                        source_velocity=list(native_record.velocity),
                        target_position=list(transformed.position_km),
                        target_velocity=list(transformed.velocity_km_s),
                        advisory_only=True,
                        created_at=now,
                    )
                )
            await self._session.commit()
        except (FrameTransformationError, SQLAlchemyError, ValueError) as exc:
            await self._session.rollback()
            quarantine = await SpaceDataIngestionService(self._session).quarantine_source_failure(
                tenant_id=tenant_id,
                actor_user_id=actor_user_id,
                source_digest=acquisition.ingestion.payload_digest,
            )
            await self._session.commit()
            if isinstance(exc, SQLAlchemyError):
                raise ProductionWiringError(ProductionWiringErrorCode.PERSISTENCE_FAILED) from exc
            return ProductionIngestionResult(
                status=quarantine.status,
                raw_artifact_id=acquisition.ingestion.raw_artifact_id,
                raw_payload_digest=acquisition.ingestion.payload_digest,
                raw_duplicate=acquisition.ingestion.duplicate,
                native_teme_observation_id=native_record.id,
                gcrf_observation_id=None,
                gcrf_canonical_digest=None,
                transformation_digest=None,
                target_frame=None,
            )
        return ProductionIngestionResult(
            status=gcrf.status,
            raw_artifact_id=acquisition.ingestion.raw_artifact_id,
            raw_payload_digest=acquisition.ingestion.payload_digest,
            raw_duplicate=acquisition.ingestion.duplicate,
            native_teme_observation_id=native_record.id,
            gcrf_observation_id=gcrf.observation_id,
            gcrf_canonical_digest=gcrf.canonical_digest,
            transformation_digest=transformed.transformation_digest,
            target_frame="GCRF",
        )
