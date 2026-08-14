"""Create tenant-scoped advisory SSA scenarios.

Revision ID: 0004_ssa_scenarios
Revises: 0003_identity_sessions
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision = "0004_ssa_scenarios"
down_revision = "0003_identity_sessions"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "ssa_scenarios",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("tenant_id", sa.Uuid(), nullable=False),
        sa.Column("created_by_user_id", sa.Uuid(), nullable=False),
        sa.Column("reference_epoch", sa.JSON(), nullable=False),
        sa.Column("primary_object", sa.JSON(), nullable=False),
        sa.Column("secondary_object", sa.JSON(), nullable=False),
        sa.Column("combined_classification", sa.String(length=32), nullable=False),
        sa.Column("advisory_only", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["created_by_user_id"], ["users.id"], ondelete="RESTRICT"),
        sa.CheckConstraint("advisory_only", name="ck_ssa_scenarios_advisory_only"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_ssa_scenarios_tenant_id", "ssa_scenarios", ["tenant_id"], unique=False)
    op.create_index(
        "ix_ssa_scenarios_tenant_created",
        "ssa_scenarios",
        ["tenant_id", "created_at"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_ssa_scenarios_tenant_created", table_name="ssa_scenarios")
    op.drop_index("ix_ssa_scenarios_tenant_id", table_name="ssa_scenarios")
    op.drop_table("ssa_scenarios")
