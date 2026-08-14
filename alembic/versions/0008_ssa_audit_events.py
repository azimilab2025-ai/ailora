"""Create append-only tenant-scoped SSA audit evidence.

Revision ID: 0008_ssa_audit_events
Revises: 0007_ssa_reviews
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision = "0008_ssa_audit_events"
down_revision = "0007_ssa_reviews"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_EVENT_TYPES_SQL = (
    "'SCENARIO_INGESTED', 'SCENARIO_SCREENED', 'SCENARIO_RISK_ASSESSED', "
    "'REVIEW_OPENED', 'REVIEW_STATE_CHANGED', 'REVIEW_CLOSED', "
    "'USER_AUTHENTICATED', 'USER_AUTH_FAILED', 'ACCESS_GRANTED', 'ACCESS_DENIED'"
)


def upgrade() -> None:
    op.create_table(
        "ssa_audit_events",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("tenant_id", sa.Uuid(), nullable=False),
        sa.Column("actor_user_id", sa.Uuid(), nullable=False),
        sa.Column("event_type", sa.String(length=64), nullable=False),
        sa.Column("resource_type", sa.String(length=32), nullable=False),
        sa.Column("resource_id", sa.Uuid(), nullable=False),
        sa.Column("outcome", sa.String(length=32), nullable=False),
        sa.Column("correlation_id", sa.Uuid(), nullable=False),
        sa.Column("detail", sa.Text(), nullable=False),
        sa.Column("combined_classification", sa.String(length=32), nullable=False),
        sa.Column("advisory_only", sa.Boolean(), nullable=False),
        sa.Column("timestamp_utc", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["actor_user_id"], ["users.id"], ondelete="RESTRICT"),
        sa.CheckConstraint(f"event_type IN ({_EVENT_TYPES_SQL})", name="ck_ssa_audit_event_type"),
        sa.CheckConstraint(
            "length(resource_type) BETWEEN 1 AND 32", name="ck_ssa_audit_resource_type"
        ),
        sa.CheckConstraint("length(outcome) BETWEEN 1 AND 32", name="ck_ssa_audit_outcome"),
        sa.CheckConstraint("length(detail) <= 1000", name="ck_ssa_audit_detail_length"),
        sa.CheckConstraint("advisory_only", name="ck_ssa_audit_advisory_only"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_ssa_audit_events_tenant_time",
        "ssa_audit_events",
        ["tenant_id", "timestamp_utc", "id"],
    )
    op.create_index(
        "ix_ssa_audit_events_tenant_resource",
        "ssa_audit_events",
        ["tenant_id", "resource_type", "resource_id"],
    )


def downgrade() -> None:
    op.drop_index("ix_ssa_audit_events_tenant_resource", table_name="ssa_audit_events")
    op.drop_index("ix_ssa_audit_events_tenant_time", table_name="ssa_audit_events")
    op.drop_table("ssa_audit_events")
