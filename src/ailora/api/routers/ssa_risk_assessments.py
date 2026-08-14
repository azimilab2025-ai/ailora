"""Protected tenant-scoped API for advisory SSA risk assessments."""

from __future__ import annotations

from typing import Annotated, Literal
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from ailora.db.session import get_db
from ailora.domain.ssa.risk import RiskLevel
from ailora.domain.ssa.risk_models import RiskAssessmentRecord
from ailora.domain.ssa.risk_service import (
    RiskAssessmentInputError,
    RiskAssessmentNotFoundError,
    TenantRiskAssessmentService,
)
from ailora.domain.ssa.scenario import DataClassification
from ailora.domain.ssa.scenario_service import (
    ScenarioAccessDeniedError,
    ScenarioNotFoundError,
)
from ailora.domain.ssa.screening import ConjunctionTier, ScreeningOutcome
from ailora.domain.ssa.screening_service import ScreeningNotFoundError
from ailora.security.dependencies import require_authenticated_user

router = APIRouter(
    prefix=(
        "/v1/tenants/{tenant_id}/ssa/scenarios/{scenario_id}"
        "/screenings/{screening_id}/risk-assessments"
    ),
    tags=["SSA Risk Assessments"],
)


class RiskAssessmentResponse(BaseModel):
    id: UUID
    tenant_id: UUID
    scenario_id: UUID
    screening_id: UUID
    created_by_user_id: UUID
    risk_level: RiskLevel
    distance_km: float
    threshold_km: float
    screening_outcome: ScreeningOutcome
    screening_tier: ConjunctionTier
    combined_classification: DataClassification
    explanation: str
    recommendation: str
    provenance_label: str
    advisory_only: Literal[True]

    @classmethod
    def from_record(cls, record: RiskAssessmentRecord) -> RiskAssessmentResponse:
        if record.advisory_only is not True:
            raise ValueError("persisted risk assessment violates advisory-only boundary")
        return cls(
            id=record.id,
            tenant_id=record.tenant_id,
            scenario_id=record.scenario_id,
            screening_id=record.screening_id,
            created_by_user_id=record.created_by_user_id,
            risk_level=RiskLevel(record.risk_level),
            distance_km=record.distance_km,
            threshold_km=record.threshold_km,
            screening_outcome=ScreeningOutcome(record.screening_outcome),
            screening_tier=ConjunctionTier(record.screening_tier),
            combined_classification=DataClassification(record.combined_classification),
            explanation=record.explanation,
            recommendation=record.recommendation,
            provenance_label=record.provenance_label,
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
            detail="Tenant risk assessment access denied",
        )
    if isinstance(error, RiskAssessmentInputError):
        return HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Persisted screening is not eligible for risk assessment",
        )
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Scenario, screening, or risk assessment not found",
    )


@router.post("", response_model=RiskAssessmentResponse, status_code=status.HTTP_201_CREATED)
async def create_risk_assessment(
    tenant_id: UUID,
    scenario_id: UUID,
    screening_id: UUID,
    payload: Annotated[dict[str, object], Depends(require_authenticated_user)],
    database: Annotated[AsyncSession, Depends(get_db)],
) -> RiskAssessmentResponse:
    try:
        record = await TenantRiskAssessmentService(database).create_assessment(
            actor_user_id=_actor_user_id(payload),
            tenant_id=tenant_id,
            scenario_id=scenario_id,
            screening_id=screening_id,
        )
        await database.commit()
        await database.refresh(record)
        return RiskAssessmentResponse.from_record(record)
    except (
        ScenarioAccessDeniedError,
        ScenarioNotFoundError,
        ScreeningNotFoundError,
        RiskAssessmentInputError,
        RiskAssessmentNotFoundError,
    ) as exc:
        await database.rollback()
        raise _translate_error(exc) from exc


@router.get("", response_model=list[RiskAssessmentResponse])
async def list_risk_assessments(
    tenant_id: UUID,
    scenario_id: UUID,
    screening_id: UUID,
    payload: Annotated[dict[str, object], Depends(require_authenticated_user)],
    database: Annotated[AsyncSession, Depends(get_db)],
) -> list[RiskAssessmentResponse]:
    try:
        records = await TenantRiskAssessmentService(database).list_assessments(
            actor_user_id=_actor_user_id(payload),
            tenant_id=tenant_id,
            scenario_id=scenario_id,
            screening_id=screening_id,
        )
        return [RiskAssessmentResponse.from_record(record) for record in records]
    except (
        ScenarioAccessDeniedError,
        ScenarioNotFoundError,
        ScreeningNotFoundError,
    ) as exc:
        raise _translate_error(exc) from exc


@router.get("/{assessment_id}", response_model=RiskAssessmentResponse)
async def read_risk_assessment(
    tenant_id: UUID,
    scenario_id: UUID,
    screening_id: UUID,
    assessment_id: UUID,
    payload: Annotated[dict[str, object], Depends(require_authenticated_user)],
    database: Annotated[AsyncSession, Depends(get_db)],
) -> RiskAssessmentResponse:
    try:
        record = await TenantRiskAssessmentService(database).get_assessment(
            actor_user_id=_actor_user_id(payload),
            tenant_id=tenant_id,
            scenario_id=scenario_id,
            screening_id=screening_id,
            assessment_id=assessment_id,
        )
        return RiskAssessmentResponse.from_record(record)
    except (
        ScenarioAccessDeniedError,
        ScenarioNotFoundError,
        ScreeningNotFoundError,
        RiskAssessmentNotFoundError,
    ) as exc:
        raise _translate_error(exc) from exc
