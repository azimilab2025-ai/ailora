"""create revocable identity refresh sessions

Revision ID: 0003_identity_sessions
Revises: 0002_identity
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0003_identity_sessions"
down_revision: str | None = "0002_identity"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "identity_sessions",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("refresh_token_hash", sa.String(length=64), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("refresh_token_hash"),
    )
    op.create_index(
        "ix_identity_sessions_expires_at",
        "identity_sessions",
        ["expires_at"],
        unique=False,
    )
    op.create_index(
        "ix_identity_sessions_user_id",
        "identity_sessions",
        ["user_id"],
        unique=False,
    )
    op.create_index(
        "ix_identity_sessions_user_active",
        "identity_sessions",
        ["user_id", "revoked_at"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_identity_sessions_user_active", table_name="identity_sessions")
    op.drop_index("ix_identity_sessions_user_id", table_name="identity_sessions")
    op.drop_index("ix_identity_sessions_expires_at", table_name="identity_sessions")
    op.drop_table("identity_sessions")
