"""Protected tenant-scoped API for advisory SSA human reviews."""

from __future__ import annotations

from typing import Annotated, Literal
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from ailora.db.session import get_db
from ailora.domain.ssa.review import ReviewState, ReviewTransitionError
from ailora.domain.ssa.review_models import ReviewRecordModel
from ailora.domain.ssa.review_service import (
    ReviewAccessDeniedError,
    ReviewAlreadyExistsError,
    ReviewInputError,
    ReviewNotFoundError,
    TenantReviewService,
)
from ailora.domain.ssa.risk_service import (
    RiskAssessmentInputError,
    RiskAssessmentNotFoundError,
)
from ailora.domain.ssa.scenario import DataClassification
from ailora.domain.ssa.scenario_service import (
    ScenarioAccessDeniedError,
    ScenarioNotFoundError,
)
from ailora.domain.ssa.screening_service import ScreeningNotFoundError
from ailora.security.dependencies import require_authenticated_user

router = APIRouter(
    prefix=(
        "/v1/tenants/{tenant_id}/ssa/scenarios/{scenario_id}"
        "/screenings/{screening_id}/risk-assessments/{assessment_id}/reviews"
    ),
    tags=["SSA Reviews"],
)


class ReviewTransitionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    target_state: ReviewState
    notes: str = Field(default="", max_length=4000)


class ReviewResponse(BaseModel):
    id: UUID
    tenant_id: UUID
    scenario_id: UUID
    screening_id: UUID
    assessment_id: UUID
    created_by_user_id: UUID
    reviewer_user_id: UUID | None
    state: ReviewState
    notes: str
    transition_count: int
    combined_classification: DataClassification
    provenance_label: str
    advisory_only: Literal[True]
    operational_clearance: Literal[False]

    @classmethod
    def from_record(cls, record: ReviewRecordModel) -> ReviewResponse:
        if record.advisory_only is not True:
            raise ValueError("persisted review violates advisory-only boundary")
        if record.operational_clearance is not False:
            raise ValueError("persisted review grants forbidden operational clearance")
        return cls(
            id=record.id,
            tenant_id=record.tenant_id,
            scenario_id=record.scenario_id,
            screening_id=record.screening_id,
            assessment_id=record.assessment_id,
            created_by_user_id=record.created_by_user_id,
            reviewer_user_id=record.reviewer_user_id,
            state=ReviewState(record.state),
            notes=record.notes,
            transition_count=record.transition_count,
            combined_classification=DataClassification(record.combined_classification),
            provenance_label=record.provenance_label,
            advisory_only=True,
            operational_clearance=False,
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
    if isinstance(error, (ScenarioAccessDeniedError, ReviewAccessDeniedError)):
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Tenant review access denied",
        )
    if isinstance(error, (ReviewAlreadyExistsError, ReviewTransitionError)):
        return HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Review state conflict",
        )
    if isinstance(error, (ReviewInputError, RiskAssessmentInputError)):
        return HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Review input is not eligible",
        )
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Scenario, screening, risk assessment, or review not found",
    )


@router.post("", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
async def create_review(
    tenant_id: UUID,
    scenario_id: UUID,
    screening_id: UUID,
    assessment_id: UUID,
    payload: Annotated[dict[str, object], Depends(require_authenticated_user)],
    database: Annotated[AsyncSession, Depends(get_db)],
) -> ReviewResponse:
    try:
        record = await TenantReviewService(database).create_review(
            actor_user_id=_actor_user_id(payload),
            tenant_id=tenant_id,
            scenario_id=scenario_id,
            screening_id=screening_id,
            assessment_id=assessment_id,
        )
        await database.commit()
        await database.refresh(record)
        return ReviewResponse.from_record(record)
    except (
        ScenarioAccessDeniedError,
        ScenarioNotFoundError,
        ScreeningNotFoundError,
        RiskAssessmentInputError,
        RiskAssessmentNotFoundError,
        ReviewAccessDeniedError,
        ReviewAlreadyExistsError,
        ReviewInputError,
        ReviewNotFoundError,
    ) as exc:
        await database.rollback()
        raise _translate_error(exc) from exc


@router.get("", response_model=list[ReviewResponse])
async def list_reviews(
    tenant_id: UUID,
    scenario_id: UUID,
    screening_id: UUID,
    assessment_id: UUID,
    payload: Annotated[dict[str, object], Depends(require_authenticated_user)],
    database: Annotated[AsyncSession, Depends(get_db)],
) -> list[ReviewResponse]:
    try:
        records = await TenantReviewService(database).list_reviews(
            actor_user_id=_actor_user_id(payload),
            tenant_id=tenant_id,
            scenario_id=scenario_id,
            screening_id=screening_id,
            assessment_id=assessment_id,
        )
        return [ReviewResponse.from_record(record) for record in records]
    except (
        ScenarioAccessDeniedError,
        ScenarioNotFoundError,
        ScreeningNotFoundError,
        RiskAssessmentInputError,
        RiskAssessmentNotFoundError,
        ReviewInputError,
    ) as exc:
        raise _translate_error(exc) from exc


@router.get("/{review_id}", response_model=ReviewResponse)
async def read_review(
    tenant_id: UUID,
    scenario_id: UUID,
    screening_id: UUID,
    assessment_id: UUID,
    review_id: UUID,
    payload: Annotated[dict[str, object], Depends(require_authenticated_user)],
    database: Annotated[AsyncSession, Depends(get_db)],
) -> ReviewResponse:
    try:
        record = await TenantReviewService(database).get_review(
            actor_user_id=_actor_user_id(payload),
            tenant_id=tenant_id,
            scenario_id=scenario_id,
            screening_id=screening_id,
            assessment_id=assessment_id,
            review_id=review_id,
        )
        return ReviewResponse.from_record(record)
    except (
        ScenarioAccessDeniedError,
        ScenarioNotFoundError,
        ScreeningNotFoundError,
        RiskAssessmentInputError,
        RiskAssessmentNotFoundError,
        ReviewInputError,
        ReviewNotFoundError,
    ) as exc:
        raise _translate_error(exc) from exc


@router.patch("/{review_id}", response_model=ReviewResponse)
async def transition_review(
    tenant_id: UUID,
    scenario_id: UUID,
    screening_id: UUID,
    assessment_id: UUID,
    review_id: UUID,
    request: ReviewTransitionRequest,
    payload: Annotated[dict[str, object], Depends(require_authenticated_user)],
    database: Annotated[AsyncSession, Depends(get_db)],
) -> ReviewResponse:
    try:
        record = await TenantReviewService(database).transition_review(
            actor_user_id=_actor_user_id(payload),
            tenant_id=tenant_id,
            scenario_id=scenario_id,
            screening_id=screening_id,
            assessment_id=assessment_id,
            review_id=review_id,
            target_state=request.target_state,
            notes=request.notes,
        )
        await database.commit()
        await database.refresh(record)
        return ReviewResponse.from_record(record)
    except (
        ScenarioAccessDeniedError,
        ScenarioNotFoundError,
        ScreeningNotFoundError,
        RiskAssessmentInputError,
        RiskAssessmentNotFoundError,
        ReviewAccessDeniedError,
        ReviewInputError,
        ReviewNotFoundError,
        ReviewTransitionError,
    ) as exc:
        await database.rollback()
        raise _translate_error(exc) from exc
