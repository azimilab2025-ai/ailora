"""Authenticated tenant-scoped production orbital-data ingestion API."""

from __future__ import annotations

import asyncio
import uuid
from datetime import UTC, datetime
from typing import Annotated, Literal
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict, Field, field_validator
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from ailora.config import settings
from ailora.db.session import get_db
from ailora.domain.identity.models import User
from ailora.domain.space_data.contracts import SpaceDataClassification
from ailora.domain.space_data.service import IngestionStatus
from ailora.security.dependencies import require_authenticated_user
from ailora.services.space_data.governance import (
    ProviderQualification,
    QualificationState,
    UnqualifiedProviderError,
)
from ailora.services.space_data.interfaces import ProviderError
from ailora.services.space_data.models import ProviderQualificationRecord
from ailora.services.space_data.production_wiring import (
    ProductionSpaceDataPipeline,
    ProductionWiringError,
    ProductionWiringErrorCode,
)

router = APIRouter(
    prefix="/v1/tenants/{tenant_id}/space-data",
    tags=["Space Data"],
)


class GcrfIngestionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    object_id: str = Field(min_length=1, max_length=128, pattern=r"^[A-Za-z0-9._:-]+$")
    evaluated_at: datetime
    idempotency_key: str = Field(min_length=16, max_length=128, pattern=r"^[A-Za-z0-9._:-]+$")
    classification: SpaceDataClassification = SpaceDataClassification.PUBLIC

    @field_validator("evaluated_at")
    @classmethod
    def require_aware_epoch(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("evaluated_at must be timezone-aware")
        return value.astimezone(UTC)


class GcrfIngestionResponse(BaseModel):
    status: IngestionStatus
    raw_artifact_id: str
    raw_payload_digest: str
    raw_duplicate: bool
    native_teme_observation_id: str | None
    gcrf_observation_id: str | None
    gcrf_canonical_digest: str | None
    transformation_digest: str | None
    target_frame: Literal["GCRF"] | None
    advisory_only: Literal[True]


class ProviderQualificationRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    provider_id: Literal["CELESTRAK"] = "CELESTRAK"
    provider_version: Literal["gp-v1"] = "gp-v1"
    license_name: str = Field(min_length=1, max_length=128)
    terms_uri: str = Field(min_length=8, max_length=512)
    terms_digest: str = Field(pattern=r"^[0-9a-f]{64}$")
    retrieved_at: datetime
    reviewed_at: datetime
    expires_at: datetime | None = None
    reviewer_reference: str = Field(min_length=1, max_length=128)
    redistribution_permitted: bool
    attribution_text: str = Field(min_length=1, max_length=2048)


class ProviderQualificationResponse(BaseModel):
    qualification_id: UUID
    state: Literal["QUALIFIED"]
    provider_id: Literal["CELESTRAK"]
    provider_version: Literal["gp-v1"]


async def _require_platform_reviewer(database: AsyncSession, actor_user_id: UUID) -> User:
    user = await database.scalar(select(User).where(User.id == actor_user_id))
    if user is None or not user.is_active or not user.is_superuser:
        raise HTTPException(status_code=403, detail="Provider qualification access denied")
    return user


def _actor_user_id(payload: dict[str, object]) -> UUID:
    try:
        return UUID(str(payload.get("sub")))
    except (TypeError, ValueError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        ) from exc


def _translate_error(error: Exception) -> HTTPException:
    if isinstance(error, ProductionWiringError):
        if error.code is ProductionWiringErrorCode.ACCESS_DENIED:
            return HTTPException(status_code=403, detail="Tenant space-data access denied")
        if error.code is ProductionWiringErrorCode.QUALIFICATION_REQUIRED:
            return HTTPException(status_code=409, detail="Provider qualification is required")
        return HTTPException(status_code=503, detail="Space-data production pipeline unavailable")
    if isinstance(error, UnqualifiedProviderError):
        return HTTPException(status_code=409, detail="Provider qualification is required")
    if isinstance(error, ProviderError):
        return HTTPException(status_code=503, detail=f"Provider unavailable: {error.code.value}")
    return HTTPException(status_code=422, detail="Space-data request is invalid")


@router.post(
    "/provider-qualifications",
    response_model=ProviderQualificationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register independently reviewed provider qualification evidence",
)
async def register_provider_qualification(
    tenant_id: UUID,
    request: ProviderQualificationRequest,
    payload: Annotated[dict[str, object], Depends(require_authenticated_user)],
    database: Annotated[AsyncSession, Depends(get_db)],
) -> ProviderQualificationResponse:
    del tenant_id
    actor_user_id = _actor_user_id(payload)
    await _require_platform_reviewer(database, actor_user_id)
    qualification_id = uuid.uuid4()
    evidence = ProviderQualification(
        qualification_id=qualification_id,
        provider_id=request.provider_id,
        provider_version=request.provider_version,
        state=QualificationState.QUALIFIED,
        license_name=request.license_name,
        terms_uri=request.terms_uri,
        terms_digest=request.terms_digest,
        retrieved_at=request.retrieved_at,
        reviewed_at=request.reviewed_at,
        expires_at=request.expires_at,
        reviewer_reference=request.reviewer_reference,
        redistribution_permitted=request.redistribution_permitted,
        attribution_text=request.attribution_text,
    )
    database.add(
        ProviderQualificationRecord(
            id=qualification_id.hex,
            reviewer_user_id=actor_user_id,
            provider_id=evidence.provider_id,
            provider_version=evidence.provider_version,
            state=evidence.state.value,
            license_name=evidence.license_name,
            terms_uri=evidence.terms_uri,
            terms_digest=evidence.terms_digest,
            retrieved_at=evidence.retrieved_at,
            reviewed_at=evidence.reviewed_at,
            expires_at=evidence.expires_at,
            reviewer_reference=evidence.reviewer_reference,
            redistribution_permitted=evidence.redistribution_permitted,
            attribution_text=evidence.attribution_text,
            created_at=datetime.now(tz=UTC),
        )
    )
    try:
        await database.commit()
    except IntegrityError as exc:
        await database.rollback()
        raise HTTPException(
            status_code=409, detail="Provider qualification already exists"
        ) from exc
    return ProviderQualificationResponse(
        qualification_id=qualification_id,
        state="QUALIFIED",
        provider_id="CELESTRAK",
        provider_version="gp-v1",
    )


@router.post(
    "/observations/gcrf:ingest",
    response_model=GcrfIngestionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Fetch qualified provider data and persist TEME plus transformed GCRF evidence",
)
async def ingest_gcrf_observation(
    tenant_id: UUID,
    request: GcrfIngestionRequest,
    payload: Annotated[dict[str, object], Depends(require_authenticated_user)],
    database: Annotated[AsyncSession, Depends(get_db)],
) -> GcrfIngestionResponse:
    try:
        result = await ProductionSpaceDataPipeline(
            database,
            settings,
            lambda: datetime.now(tz=UTC),
            asyncio.sleep,
        ).ingest_gcrf(
            tenant_id=tenant_id,
            actor_user_id=_actor_user_id(payload),
            object_id=request.object_id,
            evaluated_at=request.evaluated_at,
            idempotency_key=request.idempotency_key,
            classification=request.classification,
        )
        return GcrfIngestionResponse(
            status=result.status,
            raw_artifact_id=result.raw_artifact_id,
            raw_payload_digest=result.raw_payload_digest,
            raw_duplicate=result.raw_duplicate,
            native_teme_observation_id=result.native_teme_observation_id,
            gcrf_observation_id=result.gcrf_observation_id,
            gcrf_canonical_digest=result.gcrf_canonical_digest,
            transformation_digest=result.transformation_digest,
            target_frame="GCRF" if result.target_frame == "GCRF" else None,
            advisory_only=True,
        )
    except (ProductionWiringError, UnqualifiedProviderError, ProviderError, ValueError) as exc:
        await database.rollback()
        raise _translate_error(exc) from exc
