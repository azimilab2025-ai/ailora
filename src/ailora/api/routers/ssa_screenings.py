"""Protected tenant-scoped API for advisory T0/PHY-C1 screenings."""

from __future__ import annotations

from typing import Annotated, Literal
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from ailora.db.session import get_db
from ailora.domain.shared.value_objects import CartesianState
from ailora.domain.ssa.scenario import DataClassification
from ailora.domain.ssa.scenario_service import (
    ScenarioAccessDeniedError,
    ScenarioNotFoundError,
)
from ailora.domain.ssa.screening import ConjunctionTier, ScreeningOutcome
from ailora.domain.ssa.screening_models import ScreeningRecord
from ailora.domain.ssa.screening_service import (
    ScreeningInputError,
    ScreeningNotFoundError,
    TenantScreeningService,
)
from ailora.security.dependencies import require_authenticated_user

router = APIRouter(
    prefix="/v1/tenants/{tenant_id}/ssa/scenarios/{scenario_id}/screenings",
    tags=["SSA Screenings"],
)


class ScreeningCreateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    primary_state: CartesianState
    secondary_state: CartesianState
    threshold_km: float = Field(default=5.0, gt=0, allow_inf_nan=False)


class ScreeningResponse(BaseModel):
    id: UUID
    tenant_id: UUID
    scenario_id: UUID
    created_by_user_id: UUID
    primary_state: CartesianState
    secondary_state: CartesianState
    threshold_km: float
    tier: ConjunctionTier
    outcome: ScreeningOutcome
    distance_km: float
    combined_classification: DataClassification
    advisory_only: Literal[True]
    advisory_statement: str

    @classmethod
    def from_record(cls, record: ScreeningRecord) -> ScreeningResponse:
        if record.advisory_only is not True:
            raise ValueError("persisted screening violates advisory-only boundary")
        return cls(
            id=record.id,
            tenant_id=record.tenant_id,
            scenario_id=record.scenario_id,
            created_by_user_id=record.created_by_user_id,
            primary_state=CartesianState.model_validate(record.primary_state),
            secondary_state=CartesianState.model_validate(record.secondary_state),
            threshold_km=record.threshold_km,
            tier=ConjunctionTier(record.tier),
            outcome=ScreeningOutcome(record.outcome),
            distance_km=record.distance_km,
            combined_classification=DataClassification(record.combined_classification),
            advisory_only=True,
            advisory_statement=record.advisory_statement,
        )


def _actor_user_id(payload: dict[str, object]) -> UUID:
    try:
        return UUID(str(payload.get("sub")))
    except (TypeError, ValueError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        ) from exc


def _translate_error(error: Exception) -> HTTPException:
    if isinstance(error, ScenarioAccessDeniedError):
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Tenant screening access denied",
        )
    if isinstance(error, ScreeningInputError):
        return HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(error),
        )
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Scenario or screening not found",
    )


@router.post("", response_model=ScreeningResponse, status_code=status.HTTP_201_CREATED)
async def create_screening(
    tenant_id: UUID,
    scenario_id: UUID,
    request: ScreeningCreateRequest,
    payload: Annotated[dict[str, object], Depends(require_authenticated_user)],
    database: Annotated[AsyncSession, Depends(get_db)],
) -> ScreeningResponse:
    try:
        record = await TenantScreeningService(database).create_screening(
            actor_user_id=_actor_user_id(payload),
            tenant_id=tenant_id,
            scenario_id=scenario_id,
            primary_state=request.primary_state,
            secondary_state=request.secondary_state,
            threshold_km=request.threshold_km,
        )
        await database.commit()
        await database.refresh(record)
        return ScreeningResponse.from_record(record)
    except (
        ScenarioAccessDeniedError,
        ScenarioNotFoundError,
        ScreeningInputError,
        ScreeningNotFoundError,
    ) as exc:
        await database.rollback()
        raise _translate_error(exc) from exc


@router.get("", response_model=list[ScreeningResponse])
async def list_screenings(
    tenant_id: UUID,
    scenario_id: UUID,
    payload: Annotated[dict[str, object], Depends(require_authenticated_user)],
    database: Annotated[AsyncSession, Depends(get_db)],
) -> list[ScreeningResponse]:
    try:
        records = await TenantScreeningService(database).list_screenings(
            actor_user_id=_actor_user_id(payload),
            tenant_id=tenant_id,
            scenario_id=scenario_id,
        )
        return [ScreeningResponse.from_record(record) for record in records]
    except (ScenarioAccessDeniedError, ScenarioNotFoundError) as exc:
        raise _translate_error(exc) from exc


@router.get("/{screening_id}", response_model=ScreeningResponse)
async def read_screening(
    tenant_id: UUID,
    scenario_id: UUID,
    screening_id: UUID,
    payload: Annotated[dict[str, object], Depends(require_authenticated_user)],
    database: Annotated[AsyncSession, Depends(get_db)],
) -> ScreeningResponse:
    try:
        record = await TenantScreeningService(database).get_screening(
            actor_user_id=_actor_user_id(payload),
            tenant_id=tenant_id,
            scenario_id=scenario_id,
            screening_id=screening_id,
        )
        return ScreeningResponse.from_record(record)
    except (
        ScenarioAccessDeniedError,
        ScenarioNotFoundError,
        ScreeningNotFoundError,
    ) as exc:
        raise _translate_error(exc) from exc
