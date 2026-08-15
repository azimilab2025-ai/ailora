"""Expand Alembic revision identifier capacity before revision 0010.

Revision ID: 0009a_expand_version
Revises: 0009_space_data_contracts
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0009a_expand_version"
down_revision: str | None = "0009_space_data_contracts"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Allow Alembic to persist revision identifiers longer than 32 chars."""
    if op.get_bind().dialect.name == "postgresql":
        op.alter_column(
            "alembic_version",
            "version_num",
            existing_type=sa.String(length=32),
            type_=sa.String(length=64),
            existing_nullable=False,
        )


def downgrade() -> None:
    """Restore Alembic's original version-column capacity on PostgreSQL."""
    if op.get_bind().dialect.name == "postgresql":
        op.alter_column(
            "alembic_version",
            "version_num",
            existing_type=sa.String(length=64),
            type_=sa.String(length=32),
            existing_nullable=False,
        )
