"""Create governed provider qualification, raw artifacts, and attempt evidence.

Revision ID: 0010_space_data_provider_governance
Revises: 0009a_expand_version
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0010_space_data_provider_governance"
down_revision: str | None = "0009a_expand_version"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "space_data_provider_qualifications",
        sa.Column("id", sa.String(32), primary_key=True),
        sa.Column(
            "reviewer_user_id",
            sa.Uuid(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column("provider_id", sa.String(64), nullable=False),
        sa.Column("provider_version", sa.String(64), nullable=False),
        sa.Column("state", sa.String(16), nullable=False),
        sa.Column("license_name", sa.String(128), nullable=False),
        sa.Column("terms_uri", sa.String(512), nullable=False),
        sa.Column("terms_digest", sa.String(64), nullable=False),
        sa.Column("retrieved_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("reviewed_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True)),
        sa.Column("reviewer_reference", sa.String(128), nullable=False),
        sa.Column("redistribution_permitted", sa.Boolean(), nullable=False),
        sa.Column("attribution_text", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint("length(terms_digest) = 64", name="ck_provider_terms_digest"),
        sa.CheckConstraint(
            "state IN ('UNQUALIFIED','QUALIFIED','SUSPENDED','REVOKED')",
            name="ck_provider_qualification_state",
        ),
        sa.UniqueConstraint(
            "provider_id", "provider_version", "terms_digest", name="uq_provider_terms"
        ),
    )
    op.create_table(
        "space_data_provider_raw_artifacts",
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
            "qualification_id",
            sa.String(32),
            sa.ForeignKey("space_data_provider_qualifications.id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column("request_id", sa.String(32), nullable=False),
        sa.Column("provider_id", sa.String(64), nullable=False),
        sa.Column("provider_version", sa.String(64), nullable=False),
        sa.Column("external_object_id", sa.String(128), nullable=False),
        sa.Column("status_code", sa.Integer(), nullable=False),
        sa.Column("content_type", sa.String(128), nullable=False),
        sa.Column("fetched_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("payload", sa.LargeBinary(), nullable=False),
        sa.Column("byte_length", sa.Integer(), nullable=False),
        sa.Column("payload_digest", sa.String(64), nullable=False),
        sa.Column("classification", sa.String(32), nullable=False),
        sa.Column("attribution_text", sa.Text(), nullable=False),
        sa.Column("advisory_only", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint("byte_length > 0", name="ck_provider_raw_positive_length"),
        sa.CheckConstraint("length(payload_digest) = 64", name="ck_provider_raw_digest"),
        sa.CheckConstraint("advisory_only = true", name="ck_provider_raw_advisory"),
        sa.UniqueConstraint(
            "tenant_id", "provider_id", "payload_digest", name="uq_provider_raw_tenant_digest"
        ),
    )
    op.create_index(
        "ix_provider_raw_tenant_object",
        "space_data_provider_raw_artifacts",
        ["tenant_id", "external_object_id", "fetched_at"],
    )
    op.create_table(
        "space_data_provider_attempts",
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
        ),
        sa.Column("request_id", sa.String(32), nullable=False),
        sa.Column("provider_id", sa.String(64), nullable=False),
        sa.Column("status", sa.String(32), nullable=False),
        sa.Column("error_code", sa.String(32), nullable=False),
        sa.Column("error_detail", sa.String(256), nullable=False),
        sa.Column("attempt_count", sa.Integer(), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("advisory_only", sa.Boolean(), nullable=False),
        sa.CheckConstraint("attempt_count > 0", name="ck_provider_attempt_positive"),
        sa.CheckConstraint("advisory_only = true", name="ck_provider_attempt_advisory"),
    )
    op.create_index(
        "ix_provider_attempt_tenant_request",
        "space_data_provider_attempts",
        ["tenant_id", "request_id"],
    )


def downgrade() -> None:
    op.drop_index("ix_provider_attempt_tenant_request", table_name="space_data_provider_attempts")
    op.drop_table("space_data_provider_attempts")
    op.drop_index("ix_provider_raw_tenant_object", table_name="space_data_provider_raw_artifacts")
    op.drop_table("space_data_provider_raw_artifacts")
    op.drop_table("space_data_provider_qualifications")
