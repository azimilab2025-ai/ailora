"""Create tenant-scoped advisory SSA reviews and transition history.

Revision ID: 0007_ssa_reviews
Revises: 0006_ssa_risk_assessments
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision = "0007_ssa_reviews"
down_revision = "0006_ssa_risk_assessments"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


_REVIEW_STATES_SQL = (
    "'PENDING_REVIEW', 'UNDER_REVIEW', 'REVIEWED', 'ESCALATED', 'DISMISSED', 'CLOSED'"
)


def upgrade() -> None:
    op.create_table(
        "ssa_reviews",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("tenant_id", sa.Uuid(), nullable=False),
        sa.Column("scenario_id", sa.Uuid(), nullable=False),
        sa.Column("screening_id", sa.Uuid(), nullable=False),
        sa.Column("assessment_id", sa.Uuid(), nullable=False),
        sa.Column("created_by_user_id", sa.Uuid(), nullable=False),
        sa.Column("reviewer_user_id", sa.Uuid(), nullable=True),
        sa.Column("state", sa.String(length=32), nullable=False),
        sa.Column("notes", sa.Text(), nullable=False),
        sa.Column("transition_count", sa.Integer(), nullable=False),
        sa.Column("combined_classification", sa.String(length=32), nullable=False),
        sa.Column("provenance_label", sa.Text(), nullable=False),
        sa.Column("advisory_only", sa.Boolean(), nullable=False),
        sa.Column("operational_clearance", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["scenario_id"], ["ssa_scenarios.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["screening_id"], ["ssa_screenings.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["assessment_id"], ["ssa_risk_assessments.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["created_by_user_id"], ["users.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["reviewer_user_id"], ["users.id"], ondelete="RESTRICT"),
        sa.CheckConstraint("advisory_only", name="ck_ssa_reviews_advisory_only"),
        sa.CheckConstraint(
            "NOT operational_clearance",
            name="ck_ssa_reviews_no_operational_clearance",
        ),
        sa.CheckConstraint(
            f"state IN ({_REVIEW_STATES_SQL})",
            name="ck_ssa_reviews_state_domain",
        ),
        sa.CheckConstraint(
            "transition_count >= 0",
            name="ck_ssa_reviews_nonnegative_transition_count",
        ),
        sa.CheckConstraint(
            "length(notes) <= 4000",
            name="ck_ssa_reviews_notes_length",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("assessment_id", name="uq_ssa_reviews_assessment"),
    )
    op.create_index("ix_ssa_reviews_tenant_id", "ssa_reviews", ["tenant_id"])
    op.create_index("ix_ssa_reviews_scenario_id", "ssa_reviews", ["scenario_id"])
    op.create_index("ix_ssa_reviews_screening_id", "ssa_reviews", ["screening_id"])
    op.create_index("ix_ssa_reviews_assessment_id", "ssa_reviews", ["assessment_id"])
    op.create_index(
        "ix_ssa_reviews_scope_created",
        "ssa_reviews",
        ["tenant_id", "scenario_id", "screening_id", "assessment_id", "created_at"],
    )

    op.create_table(
        "ssa_review_transitions",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("review_id", sa.Uuid(), nullable=False),
        sa.Column("sequence_number", sa.Integer(), nullable=False),
        sa.Column("from_state", sa.String(length=32), nullable=False),
        sa.Column("to_state", sa.String(length=32), nullable=False),
        sa.Column("actor_user_id", sa.Uuid(), nullable=False),
        sa.Column("notes", sa.Text(), nullable=False),
        sa.Column("transitioned_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["review_id"], ["ssa_reviews.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["actor_user_id"], ["users.id"], ondelete="RESTRICT"),
        sa.CheckConstraint(
            "sequence_number > 0",
            name="ck_ssa_review_transition_positive_sequence",
        ),
        sa.CheckConstraint(
            f"from_state IN ({_REVIEW_STATES_SQL})",
            name="ck_ssa_review_transition_from_state",
        ),
        sa.CheckConstraint(
            f"to_state IN ({_REVIEW_STATES_SQL})",
            name="ck_ssa_review_transition_to_state",
        ),
        sa.CheckConstraint(
            "from_state <> to_state",
            name="ck_ssa_review_transition_distinct_states",
        ),
        sa.CheckConstraint(
            "length(notes) <= 4000",
            name="ck_ssa_review_transition_notes_length",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "review_id",
            "sequence_number",
            name="uq_ssa_review_transition_sequence",
        ),
    )
    op.create_index(
        "ix_ssa_review_transitions_review_id",
        "ssa_review_transitions",
        ["review_id"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_ssa_review_transitions_review_id",
        table_name="ssa_review_transitions",
    )
    op.drop_table("ssa_review_transitions")
    op.drop_index("ix_ssa_reviews_scope_created", table_name="ssa_reviews")
    op.drop_index("ix_ssa_reviews_assessment_id", table_name="ssa_reviews")
    op.drop_index("ix_ssa_reviews_screening_id", table_name="ssa_reviews")
    op.drop_index("ix_ssa_reviews_scenario_id", table_name="ssa_reviews")
    op.drop_index("ix_ssa_reviews_tenant_id", table_name="ssa_reviews")
    op.drop_table("ssa_reviews")
