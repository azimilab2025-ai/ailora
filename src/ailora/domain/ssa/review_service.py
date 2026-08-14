"""Fail-closed tenant service for advisory SSA human review workflows."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ailora.domain.identity.models import Membership, Tenant, User
from ailora.domain.ssa.audit import AuditEventType
from ailora.domain.ssa.audit_service import TenantAuditService
from ailora.domain.ssa.review import ReviewRecord as DomainReviewRecord
from ailora.domain.ssa.review import ReviewState
from ailora.domain.ssa.review_models import ReviewRecordModel, ReviewTransitionRecord
from ailora.domain.ssa.review_repository import DuplicateReviewError, ReviewRepository
from ailora.domain.ssa.risk_models import RiskAssessmentRecord
from ailora.domain.ssa.risk_service import TenantRiskAssessmentService
from ailora.security.authorization import (
    AuthorizationDeniedError,
    Permission,
    authorize_tenant_membership,
)


class ReviewAccessDeniedError(Exception):
    """The authenticated identity lacks review-write authority."""


class ReviewNotFoundError(Exception):
    """No review exists inside the fully verified ownership scope."""


class ReviewAlreadyExistsError(Exception):
    """A single review already exists for the risk assessment."""


class ReviewInputError(ValueError):
    """The persisted parent or requested notes violate the review contract."""


class TenantReviewService:
    """Creates, reads, and transitions tenant-scoped advisory reviews."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._risk_service = TenantRiskAssessmentService(session)
        self._repository = ReviewRepository(session)

    async def require_tenant_writer(
        self,
        *,
        actor_user_id: uuid.UUID,
        tenant_id: uuid.UUID,
    ) -> None:
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
            raise ReviewAccessDeniedError("tenant review write access denied")

        user, tenant, membership = row
        role = membership.role.value if hasattr(membership.role, "value") else str(membership.role)
        policy_role = {"owner": "admin", "member": "viewer"}.get(role, role)
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
            raise ReviewAccessDeniedError("tenant review write access denied") from exc

    @staticmethod
    def _validate_assessment(assessment: RiskAssessmentRecord) -> None:
        if assessment.advisory_only is not True:
            raise ReviewInputError("risk assessment violates advisory-only boundary")
        if not assessment.combined_classification:
            raise ReviewInputError("risk assessment classification is missing")

    @staticmethod
    def _validate_notes(notes: str) -> None:
        if len(notes) > 4000:
            raise ReviewInputError("review notes exceed 4000 characters")

    async def _assessment_for_scope(
        self,
        *,
        actor_user_id: uuid.UUID,
        tenant_id: uuid.UUID,
        scenario_id: uuid.UUID,
        screening_id: uuid.UUID,
        assessment_id: uuid.UUID,
    ) -> RiskAssessmentRecord:
        assessment = await self._risk_service.get_assessment(
            actor_user_id=actor_user_id,
            tenant_id=tenant_id,
            scenario_id=scenario_id,
            screening_id=screening_id,
            assessment_id=assessment_id,
        )
        self._validate_assessment(assessment)
        return assessment

    async def create_review(
        self,
        *,
        actor_user_id: uuid.UUID,
        tenant_id: uuid.UUID,
        scenario_id: uuid.UUID,
        screening_id: uuid.UUID,
        assessment_id: uuid.UUID,
    ) -> ReviewRecordModel:
        await self.require_tenant_writer(
            actor_user_id=actor_user_id,
            tenant_id=tenant_id,
        )
        assessment = await self._assessment_for_scope(
            actor_user_id=actor_user_id,
            tenant_id=tenant_id,
            scenario_id=scenario_id,
            screening_id=screening_id,
            assessment_id=assessment_id,
        )
        existing = await self._repository.get_for_assessment(assessment.id)
        if existing is not None:
            raise ReviewAlreadyExistsError("risk assessment already has a review")

        domain_review = DomainReviewRecord(scenario_id=scenario_id)
        if domain_review.COMMAND_PATH is not False:
            raise RuntimeError("review command path must remain disabled")
        record = ReviewRecordModel(
            tenant_id=tenant_id,
            scenario_id=scenario_id,
            screening_id=screening_id,
            assessment_id=assessment.id,
            created_by_user_id=actor_user_id,
            reviewer_user_id=None,
            state=domain_review.state.value,
            notes="",
            transition_count=0,
            combined_classification=assessment.combined_classification,
            provenance_label=assessment.provenance_label,
            advisory_only=True,
            operational_clearance=False,
        )
        try:
            record = await self._repository.create(record)
            await TenantAuditService(self._session).append_event(
                tenant_id=tenant_id,
                actor_user_id=actor_user_id,
                event_type=AuditEventType.REVIEW_OPENED,
                resource_type="review",
                resource_id=record.id,
                combined_classification=record.combined_classification,
                detail="Advisory human review opened",
            )
            return record
        except DuplicateReviewError as exc:
            raise ReviewAlreadyExistsError("risk assessment already has a review") from exc

    async def list_reviews(
        self,
        *,
        actor_user_id: uuid.UUID,
        tenant_id: uuid.UUID,
        scenario_id: uuid.UUID,
        screening_id: uuid.UUID,
        assessment_id: uuid.UUID,
    ) -> list[ReviewRecordModel]:
        assessment = await self._assessment_for_scope(
            actor_user_id=actor_user_id,
            tenant_id=tenant_id,
            scenario_id=scenario_id,
            screening_id=screening_id,
            assessment_id=assessment_id,
        )
        return await self._repository.list_for_scope(
            tenant_id=tenant_id,
            scenario_id=scenario_id,
            screening_id=screening_id,
            assessment_id=assessment.id,
        )

    async def get_review(
        self,
        *,
        actor_user_id: uuid.UUID,
        tenant_id: uuid.UUID,
        scenario_id: uuid.UUID,
        screening_id: uuid.UUID,
        assessment_id: uuid.UUID,
        review_id: uuid.UUID,
    ) -> ReviewRecordModel:
        assessment = await self._assessment_for_scope(
            actor_user_id=actor_user_id,
            tenant_id=tenant_id,
            scenario_id=scenario_id,
            screening_id=screening_id,
            assessment_id=assessment_id,
        )
        record = await self._repository.get_for_scope(
            tenant_id=tenant_id,
            scenario_id=scenario_id,
            screening_id=screening_id,
            assessment_id=assessment.id,
            review_id=review_id,
        )
        if record is None:
            raise ReviewNotFoundError("review not found")
        return record

    async def transition_review(
        self,
        *,
        actor_user_id: uuid.UUID,
        tenant_id: uuid.UUID,
        scenario_id: uuid.UUID,
        screening_id: uuid.UUID,
        assessment_id: uuid.UUID,
        review_id: uuid.UUID,
        target_state: ReviewState,
        notes: str = "",
    ) -> ReviewRecordModel:
        self._validate_notes(notes)
        await self.require_tenant_writer(
            actor_user_id=actor_user_id,
            tenant_id=tenant_id,
        )
        assessment = await self._assessment_for_scope(
            actor_user_id=actor_user_id,
            tenant_id=tenant_id,
            scenario_id=scenario_id,
            screening_id=screening_id,
            assessment_id=assessment_id,
        )
        record = await self._repository.get_for_scope(
            tenant_id=tenant_id,
            scenario_id=scenario_id,
            screening_id=screening_id,
            assessment_id=assessment.id,
            review_id=review_id,
            lock_for_update=True,
        )
        if record is None:
            raise ReviewNotFoundError("review not found")
        if record.advisory_only is not True:
            raise ReviewInputError("review violates advisory-only boundary")
        if record.operational_clearance is not False:
            raise ReviewInputError("review cannot grant operational clearance")

        try:
            current_state = ReviewState(record.state)
        except ValueError as exc:
            raise ReviewInputError("persisted review state is invalid") from exc
        domain_review = DomainReviewRecord(
            scenario_id=record.scenario_id,
            initial_state=current_state,
        )
        domain_review.reviewer_id = record.reviewer_user_id
        domain_review.notes = record.notes
        domain_review.transition(
            target_state,
            reviewer_id=actor_user_id,
            notes=notes,
        )

        previous_state = current_state
        next_sequence = record.transition_count + 1
        record.state = domain_review.state.value
        record.reviewer_user_id = domain_review.reviewer_id
        record.notes = domain_review.notes
        record.transition_count = next_sequence
        record.updated_at = datetime.now(tz=UTC)
        await self._repository.append_transition(
            ReviewTransitionRecord(
                review_id=record.id,
                sequence_number=next_sequence,
                from_state=previous_state.value,
                to_state=target_state.value,
                actor_user_id=actor_user_id,
                notes=notes,
            )
        )
        audit_event = (
            AuditEventType.REVIEW_CLOSED
            if target_state is ReviewState.CLOSED
            else AuditEventType.REVIEW_STATE_CHANGED
        )
        await TenantAuditService(self._session).append_event(
            tenant_id=tenant_id,
            actor_user_id=actor_user_id,
            event_type=audit_event,
            resource_type="review",
            resource_id=record.id,
            combined_classification=record.combined_classification,
            detail=(f"Advisory review transition {previous_state.value} to {target_state.value}"),
        )
        await self._session.flush()
        return record
