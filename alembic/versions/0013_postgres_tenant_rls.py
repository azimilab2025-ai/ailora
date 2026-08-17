"""Add PostgreSQL tenant row-level security and least-privilege grants.

Revision ID: 0013_postgres_tenant_rls
Revises: 0012_frame_transformations
"""

from collections.abc import Sequence

from alembic import op

revision: str = "0013_postgres_tenant_rls"
down_revision: str | None = "0012_frame_transformations"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

TENANT_TABLES: tuple[str, ...] = (
    "memberships",
    "ssa_scenarios",
    "ssa_screenings",
    "ssa_risk_assessments",
    "ssa_reviews",
    "ssa_audit_events",
    "space_data_observations",
    "space_data_quarantine_records",
    "space_data_ingestion_evidence",
    "space_data_provider_raw_artifacts",
    "space_data_provider_attempts",
    "space_data_frame_transformations",
    "durable_workflows",
    "durable_workflow_events",
)


def _quoted(identifier: str) -> str:
    if not identifier.replace("_", "").isalnum():
        raise ValueError("unsafe migration identifier")
    return f'"{identifier}"'


def _tenant_expression() -> str:
    return "tenant_id = NULLIF(current_setting('app.current_tenant_id', true), '')::uuid"


def _postgresql() -> bool:
    return op.get_bind().dialect.name == "postgresql"


def upgrade() -> None:
    if not _postgresql():
        return

    tenant_expression = _tenant_expression()
    for table_name in TENANT_TABLES:
        table = _quoted(table_name)
        policy = _quoted(f"tenant_isolation_{table_name}")
        op.execute(f"ALTER TABLE {table} ENABLE ROW LEVEL SECURITY")
        op.execute(f"ALTER TABLE {table} FORCE ROW LEVEL SECURITY")
        op.execute(
            f"CREATE POLICY {policy} ON {table} "
            f"USING ({tenant_expression}) WITH CHECK ({tenant_expression})"
        )

    tenant_table_list = ", ".join(_quoted(table_name) for table_name in TENANT_TABLES)
    op.execute(
        f"""
        DO $least_privilege$
        BEGIN
          IF to_regrole('ailora_runtime') IS NOT NULL THEN
            GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE {tenant_table_list}
              TO ailora_runtime;
          END IF;
          IF to_regrole('ailora_readonly') IS NOT NULL THEN
            GRANT SELECT ON TABLE {tenant_table_list} TO ailora_readonly;
          END IF;
        END
        $least_privilege$;
        """
    )


def downgrade() -> None:
    if not _postgresql():
        return

    for table_name in reversed(TENANT_TABLES):
        table = _quoted(table_name)
        policy = _quoted(f"tenant_isolation_{table_name}")
        op.execute(f"DROP POLICY IF EXISTS {policy} ON {table}")
        op.execute(f"ALTER TABLE {table} NO FORCE ROW LEVEL SECURITY")
        op.execute(f"ALTER TABLE {table} DISABLE ROW LEVEL SECURITY")
