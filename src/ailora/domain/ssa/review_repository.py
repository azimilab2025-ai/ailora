"""Fully scoped persistence for SSA reviews and transition history."""

from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from ailora.domain.ssa.review_models import ReviewRecordModel, ReviewTransitionRecord


class DuplicateReviewError(Exception):
    """The assessment already owns its single review record."""


class ReviewRepository:
    """Every review read requires the complete verified parent scope."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, record: ReviewRecordModel) -> ReviewRecordModel:
        self._session.add(record)
        try:
            await self._session.flush()
        except IntegrityError as exc:
            raise DuplicateReviewError("risk assessment already has a review") from exc
        return record

    async def list_for_scope(
        self,
        *,
        tenant_id: uuid.UUID,
        scenario_id: uuid.UUID,
        screening_id: uuid.UUID,
        assessment_id: uuid.UUID,
    ) -> list[ReviewRecordModel]:
        statement = (
            select(ReviewRecordModel)
            .where(
                ReviewRecordModel.tenant_id == tenant_id,
                ReviewRecordModel.scenario_id == scenario_id,
                ReviewRecordModel.screening_id == screening_id,
                ReviewRecordModel.assessment_id == assessment_id,
            )
            .order_by(ReviewRecordModel.created_at, ReviewRecordModel.id)
        )
        result = await self._session.scalars(statement)
        return list(result.all())

    async def get_for_scope(
        self,
        *,
        tenant_id: uuid.UUID,
        scenario_id: uuid.UUID,
        screening_id: uuid.UUID,
        assessment_id: uuid.UUID,
        review_id: uuid.UUID,
        lock_for_update: bool = False,
    ) -> ReviewRecordModel | None:
        statement = select(ReviewRecordModel).where(
            ReviewRecordModel.id == review_id,
            ReviewRecordModel.tenant_id == tenant_id,
            ReviewRecordModel.scenario_id == scenario_id,
            ReviewRecordModel.screening_id == screening_id,
            ReviewRecordModel.assessment_id == assessment_id,
        )
        if lock_for_update:
            statement = statement.with_for_update()
        result = await self._session.execute(statement)
        return result.scalar_one_or_none()

    async def get_for_assessment(
        self,
        assessment_id: uuid.UUID,
    ) -> ReviewRecordModel | None:
        statement = select(ReviewRecordModel).where(
            ReviewRecordModel.assessment_id == assessment_id
        )
        result = await self._session.execute(statement)
        return result.scalar_one_or_none()

    async def append_transition(
        self,
        transition: ReviewTransitionRecord,
    ) -> ReviewTransitionRecord:
        self._session.add(transition)
        await self._session.flush()
        return transition

    async def list_transitions(
        self,
        review_id: uuid.UUID,
    ) -> list[ReviewTransitionRecord]:
        statement = (
            select(ReviewTransitionRecord)
            .where(ReviewTransitionRecord.review_id == review_id)
            .order_by(ReviewTransitionRecord.sequence_number)
        )
        result = await self._session.scalars(statement)
        return list(result.all())
