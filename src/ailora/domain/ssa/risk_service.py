"""Fail-closed tenant service for advisory SSA risk assessments."""

from __future__ import annotations

import math
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from ailora.domain.ssa.risk import assess_conjunction_risk
from ailora.domain.ssa.risk_models import RiskAssessmentRecord
from ailora.domain.ssa.risk_repository import RiskAssessmentRepository
from ailora.domain.ssa.screening import (
    ConjunctionScreeningResult,
    ConjunctionTier,
    ScreeningOutcome,
)
from ailora.domain.ssa.screening_models import ScreeningRecord
from ailora.domain.ssa.screening_service import TenantScreeningService


class RiskAssessmentNotFoundError(Exception):
    """No risk assessment exists inside the fully verified ownership scope."""


class RiskAssessmentInputError(ValueError):
    """The persisted screening violates the bounded risk input contract."""


class TenantRiskAssessmentService:
    """Creates and reads tenant-scoped, advisory-only risk snapshots."""

    def __init__(self, session: AsyncSession) -> None:
        self._screening_service = TenantScreeningService(session)
        self._repository = RiskAssessmentRepository(session)

    @staticmethod
    def _to_domain_screening(record: ScreeningRecord) -> ConjunctionScreeningResult:
        if record.advisory_only is not True:
            raise RiskAssessmentInputError("screening violates advisory-only boundary")
        if record.tier != ConjunctionTier.T0_PHY_C1.value:
            raise RiskAssessmentInputError("unsupported screening tier")
        if (
            not math.isfinite(record.distance_km)
            or record.distance_km < 0
            or not math.isfinite(record.threshold_km)
            or record.threshold_km <= 0
        ):
            raise RiskAssessmentInputError("screening distance or threshold is invalid")
        try:
            outcome = ScreeningOutcome(record.outcome)
        except ValueError as exc:
            raise RiskAssessmentInputError("screening outcome is invalid") from exc
        return ConjunctionScreeningResult(
            outcome=outcome,
            distance_km=record.distance_km,
            threshold_km=record.threshold_km,
        )

    async def create_assessment(
        self,
        *,
        actor_user_id: uuid.UUID,
        tenant_id: uuid.UUID,
        scenario_id: uuid.UUID,
        screening_id: uuid.UUID,
    ) -> RiskAssessmentRecord:
        screening = await self._screening_service.get_screening(
            actor_user_id=actor_user_id,
            tenant_id=tenant_id,
            scenario_id=scenario_id,
            screening_id=screening_id,
        )
        domain_screening = self._to_domain_screening(screening)
        assessment = assess_conjunction_risk(domain_screening)
        if assessment.is_advisory is not True:
            raise RuntimeError("non-advisory risk output is forbidden")

        record = RiskAssessmentRecord(
            tenant_id=tenant_id,
            scenario_id=scenario_id,
            screening_id=screening.id,
            created_by_user_id=actor_user_id,
            risk_level=assessment.risk_level.value,
            distance_km=assessment.distance_km,
            threshold_km=assessment.threshold_km,
            screening_outcome=domain_screening.outcome.value,
            screening_tier=domain_screening.tier.value,
            combined_classification=screening.combined_classification,
            explanation=assessment.explanation,
            recommendation=assessment.recommendation,
            provenance_label=assessment.provenance_label,
            advisory_only=True,
        )
        return await self._repository.create(record)

    async def list_assessments(
        self,
        *,
        actor_user_id: uuid.UUID,
        tenant_id: uuid.UUID,
        scenario_id: uuid.UUID,
        screening_id: uuid.UUID,
    ) -> list[RiskAssessmentRecord]:
        screening = await self._screening_service.get_screening(
            actor_user_id=actor_user_id,
            tenant_id=tenant_id,
            scenario_id=scenario_id,
            screening_id=screening_id,
        )
        return await self._repository.list_for_scope(
            tenant_id=tenant_id,
            scenario_id=scenario_id,
            screening_id=screening.id,
        )

    async def get_assessment(
        self,
        *,
        actor_user_id: uuid.UUID,
        tenant_id: uuid.UUID,
        scenario_id: uuid.UUID,
        screening_id: uuid.UUID,
        assessment_id: uuid.UUID,
    ) -> RiskAssessmentRecord:
        screening = await self._screening_service.get_screening(
            actor_user_id=actor_user_id,
            tenant_id=tenant_id,
            scenario_id=scenario_id,
            screening_id=screening_id,
        )
        record = await self._repository.get_for_scope(
            tenant_id=tenant_id,
            scenario_id=scenario_id,
            screening_id=screening.id,
            assessment_id=assessment_id,
        )
        if record is None:
            raise RiskAssessmentNotFoundError("risk assessment not found")
        return record
