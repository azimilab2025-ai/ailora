"""Create tenant-scoped advisory SSA screenings.

Revision ID: 0005_ssa_screenings
Revises: 0004_ssa_scenarios
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision = "0005_ssa_screenings"
down_revision = "0004_ssa_scenarios"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "ssa_screenings",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("tenant_id", sa.Uuid(), nullable=False),
        sa.Column("scenario_id", sa.Uuid(), nullable=False),
        sa.Column("created_by_user_id", sa.Uuid(), nullable=False),
        sa.Column("primary_state", sa.JSON(), nullable=False),
        sa.Column("secondary_state", sa.JSON(), nullable=False),
        sa.Column("threshold_km", sa.Float(), nullable=False),
        sa.Column("tier", sa.String(length=32), nullable=False),
        sa.Column("outcome", sa.String(length=64), nullable=False),
        sa.Column("distance_km", sa.Float(), nullable=False),
        sa.Column("combined_classification", sa.String(length=32), nullable=False),
        sa.Column("advisory_only", sa.Boolean(), nullable=False),
        sa.Column("advisory_statement", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["scenario_id"], ["ssa_scenarios.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["created_by_user_id"], ["users.id"], ondelete="RESTRICT"),
        sa.CheckConstraint("advisory_only", name="ck_ssa_screenings_advisory_only"),
        sa.CheckConstraint("threshold_km > 0", name="ck_ssa_screenings_positive_threshold"),
        sa.CheckConstraint("distance_km >= 0", name="ck_ssa_screenings_nonnegative_distance"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_ssa_screenings_tenant_id",
        "ssa_screenings",
        ["tenant_id"],
        unique=False,
    )
    op.create_index(
        "ix_ssa_screenings_scenario_id",
        "ssa_screenings",
        ["scenario_id"],
        unique=False,
    )
    op.create_index(
        "ix_ssa_screenings_tenant_scenario_created",
        "ssa_screenings",
        ["tenant_id", "scenario_id", "created_at"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_ssa_screenings_tenant_scenario_created", table_name="ssa_screenings")
    op.drop_index("ix_ssa_screenings_scenario_id", table_name="ssa_screenings")
    op.drop_index("ix_ssa_screenings_tenant_id", table_name="ssa_screenings")
    op.drop_table("ssa_screenings")
