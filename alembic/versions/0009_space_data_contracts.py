"""Create typed space-data observations, quarantine, and ingestion evidence.

Revision ID: 0009_space_data_contracts
Revises: 0008_ssa_audit_events
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0009_space_data_contracts"
down_revision: str | None = "0008_ssa_audit_events"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "space_data_observations",
        sa.Column("id", sa.String(32), primary_key=True),
        sa.Column(
            "tenant_id",
            sa.Uuid(as_uuid=True),
            sa.ForeignKey("tenants.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("observation_id", sa.String(128), nullable=False),
        sa.Column("object_id", sa.String(128), nullable=False),
        sa.Column("schema_version", sa.String(16), nullable=False),
        sa.Column("reference_frame", sa.String(16), nullable=False),
        sa.Column("distance_unit", sa.String(16), nullable=False),
        sa.Column("velocity_unit", sa.String(16), nullable=False),
        sa.Column("time_scale", sa.String(16), nullable=False),
        sa.Column("epoch", sa.DateTime(timezone=True), nullable=False),
        sa.Column("evaluated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("max_age_seconds", sa.Float(), nullable=False),
        sa.Column("position", sa.JSON(), nullable=False),
        sa.Column("velocity", sa.JSON(), nullable=False),
        sa.Column("covariance", sa.JSON(), nullable=True),
        sa.Column("quality", sa.String(16), nullable=False),
        sa.Column("source_id", sa.String(128), nullable=False),
        sa.Column("source_version", sa.String(128), nullable=False),
        sa.Column("ingested_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("canonical_digest", sa.String(64), nullable=False),
        sa.Column("classification", sa.String(32), nullable=False),
        sa.Column("advisory_only", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("tenant_id", "canonical_digest", name="uq_space_data_tenant_digest"),
        sa.CheckConstraint("advisory_only = true", name="ck_space_data_advisory_only"),
        sa.CheckConstraint("schema_version = '1.0'", name="ck_space_data_schema_version"),
        sa.CheckConstraint("quality = 'VALID'", name="ck_space_data_quality"),
        sa.CheckConstraint("length(canonical_digest) = 64", name="ck_space_data_digest_length"),
    )
    op.create_index(
        "ix_space_data_tenant_object_epoch",
        "space_data_observations",
        ["tenant_id", "object_id", "epoch"],
    )
    op.create_index(
        "ix_space_data_tenant_quality_source",
        "space_data_observations",
        ["tenant_id", "quality", "source_id"],
    )
    op.create_table(
        "space_data_quarantine_records",
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
        sa.Column("canonical_digest", sa.String(64), nullable=False),
        sa.Column("reason_code", sa.String(64), nullable=False),
        sa.Column("reason_detail", sa.Text(), nullable=False),
        sa.Column("classification", sa.String(32), nullable=False),
        sa.Column("advisory_only", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint("advisory_only = true", name="ck_space_quarantine_advisory_only"),
        sa.CheckConstraint(
            "length(canonical_digest) = 64", name="ck_space_quarantine_digest_length"
        ),
        sa.CheckConstraint(
            "length(reason_detail) <= 512", name="ck_space_quarantine_detail_length"
        ),
    )
    op.create_index(
        "ix_space_quarantine_tenant_created",
        "space_data_quarantine_records",
        ["tenant_id", "created_at"],
    )
    op.create_table(
        "space_data_ingestion_evidence",
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
        sa.Column("event_type", sa.String(32), nullable=False),
        sa.Column("resource_id", sa.String(128), nullable=False),
        sa.Column("canonical_digest", sa.String(64), nullable=False),
        sa.Column("detail", sa.Text(), nullable=False),
        sa.Column("advisory_only", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint("advisory_only = true", name="ck_space_evidence_advisory_only"),
        sa.CheckConstraint("length(canonical_digest) = 64", name="ck_space_evidence_digest_length"),
    )
    op.create_index(
        "ix_space_evidence_tenant_created",
        "space_data_ingestion_evidence",
        ["tenant_id", "created_at"],
    )


def downgrade() -> None:
    op.drop_index("ix_space_evidence_tenant_created", table_name="space_data_ingestion_evidence")
    op.drop_table("space_data_ingestion_evidence")
    op.drop_index("ix_space_quarantine_tenant_created", table_name="space_data_quarantine_records")
    op.drop_table("space_data_quarantine_records")
    op.drop_index("ix_space_data_tenant_quality_source", table_name="space_data_observations")
    op.drop_index("ix_space_data_tenant_object_epoch", table_name="space_data_observations")
    op.drop_table("space_data_observations")
