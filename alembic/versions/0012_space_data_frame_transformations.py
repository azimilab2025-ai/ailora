"""Add append-only TEME-to-GCRF transformation provenance.

Revision ID: 0012_frame_transformations
Revises: 0011_durable_workflows
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0012_frame_transformations"
down_revision: str | None = "0011_durable_workflows"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "space_data_frame_transformations",
        sa.Column("id", sa.String(32), primary_key=True),
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
        sa.Column(
            "raw_artifact_id",
            sa.String(32),
            sa.ForeignKey("space_data_provider_raw_artifacts.id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column(
            "native_observation_id",
            sa.String(32),
            sa.ForeignKey("space_data_observations.id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column(
            "gcrf_observation_id",
            sa.String(32),
            sa.ForeignKey("space_data_observations.id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column("epoch", sa.DateTime(timezone=True), nullable=False),
        sa.Column("source_frame", sa.String(16), nullable=False),
        sa.Column("target_frame", sa.String(16), nullable=False),
        sa.Column("frame_realization", sa.String(32), nullable=False),
        sa.Column("algorithm_id", sa.String(64), nullable=False),
        sa.Column("algorithm_version", sa.String(32), nullable=False),
        sa.Column("astropy_version", sa.String(32), nullable=False),
        sa.Column("iers_data_version", sa.String(64), nullable=False),
        sa.Column("iers_source", sa.String(128), nullable=False),
        sa.Column("iers_mjd_start", sa.Float(), nullable=False),
        sa.Column("iers_mjd_end", sa.Float(), nullable=False),
        sa.Column("eop_status", sa.String(128), nullable=False),
        sa.Column("input_digest", sa.String(64), nullable=False),
        sa.Column("iers_data_digest", sa.String(64), nullable=False),
        sa.Column("transformation_digest", sa.String(64), nullable=False),
        sa.Column("source_position", sa.JSON(), nullable=False),
        sa.Column("source_velocity", sa.JSON(), nullable=False),
        sa.Column("target_position", sa.JSON(), nullable=False),
        sa.Column("target_velocity", sa.JSON(), nullable=False),
        sa.Column("advisory_only", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint(
            "tenant_id",
            "transformation_digest",
            name="uq_space_transform_tenant_digest",
        ),
        sa.CheckConstraint("source_frame = 'TEME'", name="ck_space_transform_source_teme"),
        sa.CheckConstraint("target_frame = 'GCRF'", name="ck_space_transform_target_gcrf"),
        sa.CheckConstraint("advisory_only = true", name="ck_space_transform_advisory"),
        sa.CheckConstraint("length(input_digest) = 64", name="ck_space_transform_input_digest"),
        sa.CheckConstraint("length(iers_data_digest) = 64", name="ck_space_transform_iers_digest"),
        sa.CheckConstraint(
            "length(transformation_digest) = 64",
            name="ck_space_transform_result_digest",
        ),
    )
    op.create_index(
        "ix_space_transform_tenant_epoch",
        "space_data_frame_transformations",
        ["tenant_id", "epoch"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_space_transform_tenant_epoch",
        table_name="space_data_frame_transformations",
    )
    op.drop_table("space_data_frame_transformations")
