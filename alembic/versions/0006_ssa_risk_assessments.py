"""Create tenant-scoped advisory SSA risk assessments.

Revision ID: 0006_ssa_risk_assessments
Revises: 0005_ssa_screenings
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision = "0006_ssa_risk_assessments"
down_revision = "0005_ssa_screenings"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "ssa_risk_assessments",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("tenant_id", sa.Uuid(), nullable=False),
        sa.Column("scenario_id", sa.Uuid(), nullable=False),
        sa.Column("screening_id", sa.Uuid(), nullable=False),
        sa.Column("created_by_user_id", sa.Uuid(), nullable=False),
        sa.Column("risk_level", sa.String(length=32), nullable=False),
        sa.Column("distance_km", sa.Float(), nullable=False),
        sa.Column("threshold_km", sa.Float(), nullable=False),
        sa.Column("screening_outcome", sa.String(length=64), nullable=False),
        sa.Column("screening_tier", sa.String(length=32), nullable=False),
        sa.Column("combined_classification", sa.String(length=32), nullable=False),
        sa.Column("explanation", sa.Text(), nullable=False),
        sa.Column("recommendation", sa.Text(), nullable=False),
        sa.Column("provenance_label", sa.Text(), nullable=False),
        sa.Column("advisory_only", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["scenario_id"], ["ssa_scenarios.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["screening_id"], ["ssa_screenings.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["created_by_user_id"], ["users.id"], ondelete="RESTRICT"),
        sa.CheckConstraint("advisory_only", name="ck_ssa_risk_advisory_only"),
        sa.CheckConstraint("distance_km >= 0", name="ck_ssa_risk_nonnegative_distance"),
        sa.CheckConstraint("threshold_km > 0", name="ck_ssa_risk_positive_threshold"),
        sa.CheckConstraint(
            "risk_level IN ('NEGLIGIBLE', 'LOW', 'MODERATE', 'HIGH', 'CRITICAL')",
            name="ck_ssa_risk_level_domain",
        ),
        sa.CheckConstraint(
            "screening_outcome IN ('CONJUNCTION_POSSIBLE', 'NO_CONJUNCTION')",
            name="ck_ssa_risk_screening_outcome_domain",
        ),
        sa.CheckConstraint(
            "screening_tier = 'T0_PHY_C1'",
            name="ck_ssa_risk_screening_tier_domain",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_ssa_risk_assessments_tenant_id",
        "ssa_risk_assessments",
        ["tenant_id"],
        unique=False,
    )
    op.create_index(
        "ix_ssa_risk_assessments_scenario_id",
        "ssa_risk_assessments",
        ["scenario_id"],
        unique=False,
    )
    op.create_index(
        "ix_ssa_risk_assessments_screening_id",
        "ssa_risk_assessments",
        ["screening_id"],
        unique=False,
    )
    op.create_index(
        "ix_ssa_risk_tenant_scenario_screening_created",
        "ssa_risk_assessments",
        ["tenant_id", "scenario_id", "screening_id", "created_at"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        "ix_ssa_risk_tenant_scenario_screening_created",
        table_name="ssa_risk_assessments",
    )
    op.drop_index("ix_ssa_risk_assessments_screening_id", table_name="ssa_risk_assessments")
    op.drop_index("ix_ssa_risk_assessments_scenario_id", table_name="ssa_risk_assessments")
    op.drop_index("ix_ssa_risk_assessments_tenant_id", table_name="ssa_risk_assessments")
    op.drop_table("ssa_risk_assessments")
