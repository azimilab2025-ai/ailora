"""Create tenant-scoped durable workflows and append-only events.

Revision ID: 0011_durable_workflows
Revises: 0010_space_data_provider_governance
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0011_durable_workflows"
down_revision: str | None = "0010_space_data_provider_governance"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "durable_workflows",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column(
            "tenant_id",
            sa.Uuid(as_uuid=True),
            sa.ForeignKey("tenants.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "actor_user_id",
            sa.Uuid(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column("idempotency_key", sa.String(128), nullable=False),
        sa.Column("workflow_type", sa.String(64), nullable=False),
        sa.Column("request_digest", sa.String(64), nullable=False),
        sa.Column("payload_digest", sa.String(64), nullable=False),
        sa.Column("correlation_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("causation_id", sa.Uuid(as_uuid=True)),
        sa.Column("state", sa.String(32), nullable=False),
        sa.Column("attempt_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("max_attempts", sa.Integer(), nullable=False),
        sa.Column("event_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("version", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("failure_kind", sa.String(32), nullable=False, server_default=""),
        sa.Column("error_code", sa.String(64), nullable=False, server_default=""),
        sa.Column("lease_token", sa.Uuid(as_uuid=True)),
        sa.Column("next_attempt_at", sa.DateTime(timezone=True)),
        sa.Column("completed_at", sa.DateTime(timezone=True)),
        sa.Column("advisory_only", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("tenant_id", "idempotency_key", name="uq_workflow_tenant_idempotency"),
        sa.CheckConstraint(
            "attempt_count >= 0 AND attempt_count <= max_attempts",
            name="ck_workflow_attempt_bounds",
        ),
        sa.CheckConstraint(
            "max_attempts >= 1 AND max_attempts <= 10", name="ck_workflow_max_attempts"
        ),
        sa.CheckConstraint("advisory_only = true", name="ck_workflow_advisory_only"),
    )
    op.create_index(
        "ix_workflow_tenant_state_next",
        "durable_workflows",
        ["tenant_id", "state", "next_attempt_at"],
    )
    op.create_table(
        "durable_workflow_events",
        sa.Column("id", sa.Uuid(as_uuid=True), primary_key=True),
        sa.Column(
            "workflow_id",
            sa.Uuid(as_uuid=True),
            sa.ForeignKey("durable_workflows.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "tenant_id",
            sa.Uuid(as_uuid=True),
            sa.ForeignKey("tenants.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("sequence_number", sa.Integer(), nullable=False),
        sa.Column("event_type", sa.String(64), nullable=False),
        sa.Column("from_state", sa.String(32), nullable=False),
        sa.Column("to_state", sa.String(32), nullable=False),
        sa.Column(
            "actor_user_id",
            sa.Uuid(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column("correlation_id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column("causation_id", sa.Uuid(as_uuid=True)),
        sa.Column("evidence_digest", sa.String(64), nullable=False),
        sa.Column("advisory_only", sa.Boolean(), nullable=False),
        sa.Column("occurred_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("workflow_id", "sequence_number", name="uq_workflow_event_sequence"),
        sa.CheckConstraint("sequence_number > 0", name="ck_workflow_event_sequence"),
        sa.CheckConstraint("advisory_only = true", name="ck_workflow_event_advisory"),
    )
    op.create_index(
        "ix_workflow_event_tenant_correlation",
        "durable_workflow_events",
        ["tenant_id", "correlation_id"],
    )


def downgrade() -> None:
    op.drop_index("ix_workflow_event_tenant_correlation", table_name="durable_workflow_events")
    op.drop_table("durable_workflow_events")
    op.drop_index("ix_workflow_tenant_state_next", table_name="durable_workflows")
    op.drop_table("durable_workflows")
