"""Tenant-scoped persistence for advisory SSA human reviews."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import Uuid

from ailora.db.base import Base

_REVIEW_STATES_SQL = (
    "'PENDING_REVIEW', 'UNDER_REVIEW', 'REVIEWED', 'ESCALATED', 'DISMISSED', 'CLOSED'"
)


class ReviewRecordModel(Base):
    """Current review state constrained to the complete SSA ownership chain."""

    __tablename__ = "ssa_reviews"
    __table_args__ = (
        Index(
            "ix_ssa_reviews_scope_created",
            "tenant_id",
            "scenario_id",
            "screening_id",
            "assessment_id",
            "created_at",
        ),
        UniqueConstraint("assessment_id", name="uq_ssa_reviews_assessment"),
        CheckConstraint("advisory_only", name="ck_ssa_reviews_advisory_only"),
        CheckConstraint(
            "NOT operational_clearance",
            name="ck_ssa_reviews_no_operational_clearance",
        ),
        CheckConstraint(
            f"state IN ({_REVIEW_STATES_SQL})",
            name="ck_ssa_reviews_state_domain",
        ),
        CheckConstraint(
            "transition_count >= 0",
            name="ck_ssa_reviews_nonnegative_transition_count",
        ),
        CheckConstraint(
            "length(notes) <= 4000",
            name="ck_ssa_reviews_notes_length",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    scenario_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("ssa_scenarios.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    screening_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("ssa_screenings.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    assessment_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("ssa_risk_assessments.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    created_by_user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
    )
    reviewer_user_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=True,
    )
    state: Mapped[str] = mapped_column(String(32), nullable=False)
    notes: Mapped[str] = mapped_column(Text, nullable=False, default="")
    transition_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    combined_classification: Mapped[str] = mapped_column(String(32), nullable=False)
    provenance_label: Mapped[str] = mapped_column(Text, nullable=False)
    advisory_only: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    operational_clearance: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(tz=UTC),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(tz=UTC),
    )


class ReviewTransitionRecord(Base):
    """Append-only audit entry for one validated review-state transition."""

    __tablename__ = "ssa_review_transitions"
    __table_args__ = (
        UniqueConstraint(
            "review_id",
            "sequence_number",
            name="uq_ssa_review_transition_sequence",
        ),
        CheckConstraint(
            "sequence_number > 0",
            name="ck_ssa_review_transition_positive_sequence",
        ),
        CheckConstraint(
            f"from_state IN ({_REVIEW_STATES_SQL})",
            name="ck_ssa_review_transition_from_state",
        ),
        CheckConstraint(
            f"to_state IN ({_REVIEW_STATES_SQL})",
            name="ck_ssa_review_transition_to_state",
        ),
        CheckConstraint(
            "from_state <> to_state",
            name="ck_ssa_review_transition_distinct_states",
        ),
        CheckConstraint(
            "length(notes) <= 4000",
            name="ck_ssa_review_transition_notes_length",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    review_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("ssa_reviews.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    sequence_number: Mapped[int] = mapped_column(Integer, nullable=False)
    from_state: Mapped[str] = mapped_column(String(32), nullable=False)
    to_state: Mapped[str] = mapped_column(String(32), nullable=False)
    actor_user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
    )
    notes: Mapped[str] = mapped_column(Text, nullable=False, default="")
    transitioned_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(tz=UTC),
    )
