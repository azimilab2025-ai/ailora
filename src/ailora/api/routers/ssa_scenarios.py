"""Protected tenant-scoped API for advisory SSA scenarios."""

from __future__ import annotations

from typing import Annotated, Literal
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from ailora.db.session import get_db
from ailora.domain.shared.value_objects import TemporalStamp
from ailora.domain.ssa.scenario import (
    DataClassification,
    OrbitalObjectDescriptor,
)
from ailora.domain.ssa.scenario_models import ScenarioRecord
from ailora.domain.ssa.scenario_service import (
    ScenarioAccessDeniedError,
    ScenarioNotFoundError,
    TenantScenarioService,
)
from ailora.security.dependencies import require_authenticated_user

router = APIRouter(
    prefix="/v1/tenants/{tenant_id}/ssa/scenarios",
    tags=["SSA Scenarios"],
)


class ScenarioCreateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    reference_epoch: TemporalStamp
    primary_object: OrbitalObjectDescriptor
    secondary_object: OrbitalObjectDescriptor


class ScenarioResponse(BaseModel):
    id: UUID
    tenant_id: UUID
    created_by_user_id: UUID
    reference_epoch: TemporalStamp
    primary_object: OrbitalObjectDescriptor
    secondary_object: OrbitalObjectDescriptor
    combined_classification: DataClassification
    advisory_only: Literal[True]

    @classmethod
    def from_record(cls, record: ScenarioRecord) -> ScenarioResponse:
        if record.advisory_only is not True:
            raise ValueError("persisted scenario violates advisory-only boundary")
        return cls(
            id=record.id,
            tenant_id=record.tenant_id,
            created_by_user_id=record.created_by_user_id,
            reference_epoch=TemporalStamp.model_validate(record.reference_epoch),
            primary_object=OrbitalObjectDescriptor.model_validate(record.primary_object),
            secondary_object=OrbitalObjectDescriptor.model_validate(record.secondary_object),
            combined_classification=DataClassification(record.combined_classification),
            advisory_only=True,
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
            detail="Tenant scenario access denied",
        )
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Scenario not found",
    )


@router.post("", response_model=ScenarioResponse, status_code=status.HTTP_201_CREATED)
async def create_scenario(
    tenant_id: UUID,
    request: ScenarioCreateRequest,
    payload: Annotated[dict[str, object], Depends(require_authenticated_user)],
    database: Annotated[AsyncSession, Depends(get_db)],
) -> ScenarioResponse:
    try:
        record = await TenantScenarioService(database).create_scenario(
            actor_user_id=_actor_user_id(payload),
            tenant_id=tenant_id,
            reference_epoch=request.reference_epoch,
            primary_object=request.primary_object,
            secondary_object=request.secondary_object,
        )
        await database.commit()
        await database.refresh(record)
        return ScenarioResponse.from_record(record)
    except (ScenarioAccessDeniedError, ScenarioNotFoundError) as exc:
        await database.rollback()
        raise _translate_error(exc) from exc


@router.get("", response_model=list[ScenarioResponse])
async def list_scenarios(
    tenant_id: UUID,
    payload: Annotated[dict[str, object], Depends(require_authenticated_user)],
    database: Annotated[AsyncSession, Depends(get_db)],
) -> list[ScenarioResponse]:
    try:
        records = await TenantScenarioService(database).list_scenarios(
            actor_user_id=_actor_user_id(payload),
            tenant_id=tenant_id,
        )
        return [ScenarioResponse.from_record(record) for record in records]
    except ScenarioAccessDeniedError as exc:
        raise _translate_error(exc) from exc


@router.get("/{scenario_id}", response_model=ScenarioResponse)
async def read_scenario(
    tenant_id: UUID,
    scenario_id: UUID,
    payload: Annotated[dict[str, object], Depends(require_authenticated_user)],
    database: Annotated[AsyncSession, Depends(get_db)],
) -> ScenarioResponse:
    try:
        record = await TenantScenarioService(database).get_scenario(
            actor_user_id=_actor_user_id(payload),
            tenant_id=tenant_id,
            scenario_id=scenario_id,
        )
        return ScenarioResponse.from_record(record)
    except (ScenarioAccessDeniedError, ScenarioNotFoundError) as exc:
        raise _translate_error(exc) from exc
