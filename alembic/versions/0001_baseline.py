"""baseline: initial empty schema

Revision ID: 0001_baseline
Revises:
Create Date: 2026-08-05

This is the baseline migration that establishes the Alembic version table.
No application tables exist yet; they will be added in subsequent migrations
as domain models are introduced in PHASE_1 through PHASE_3.
"""

from collections.abc import Sequence

from alembic import op  # noqa: F401 — required by Alembic runner

# revision identifiers, used by Alembic.
revision: str = "0001_baseline"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Apply the baseline migration (no-op; establishes version tracking)."""
    pass


def downgrade() -> None:
    """Reverse the baseline migration (no-op)."""
    pass
