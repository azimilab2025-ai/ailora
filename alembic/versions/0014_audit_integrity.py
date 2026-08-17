"""Add tenant audit hash chains and database-enforced immutability.

Revision ID: 0014_audit_integrity
Revises: 0013_postgres_tenant_rls
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0014_audit_integrity"
down_revision: str | None = "0013_postgres_tenant_rls"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def _postgresql() -> bool:
    return op.get_bind().dialect.name == "postgresql"


def _require_pgcrypto() -> None:
    op.execute(
        """
        DO $require_pgcrypto$
        BEGIN
          IF to_regprocedure('digest(bytea,text)') IS NULL THEN
            RAISE EXCEPTION
              'pgcrypto digest(bytea,text) must be pre-provisioned before audit migration';
          END IF;
        END
        $require_pgcrypto$;
        """
    )


def _expand() -> None:
    op.add_column("ssa_audit_events", sa.Column("sequence_no", sa.BigInteger(), nullable=True))
    op.add_column(
        "ssa_audit_events",
        sa.Column("previous_hash", sa.String(length=64), nullable=True),
    )
    op.add_column(
        "ssa_audit_events",
        sa.Column("event_hash", sa.String(length=64), nullable=True),
    )


def _migrate() -> None:
    op.execute("ALTER TABLE ssa_audit_events NO FORCE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE ssa_audit_events DISABLE ROW LEVEL SECURITY")
    op.execute(
        """
        CREATE FUNCTION ailora_audit_component(value text)
        RETURNS text
        LANGUAGE sql
        IMMUTABLE
        STRICT
        AS $function$
          SELECT octet_length(convert_to(value, 'UTF8'))::text || ':' || value
        $function$;
        """
    )
    op.execute(
        """
        CREATE FUNCTION ailora_audit_payload(
          tenant_id uuid,
          event_id uuid,
          actor_user_id uuid,
          event_type text,
          resource_type text,
          resource_id uuid,
          outcome text,
          correlation_id uuid,
          detail text,
          combined_classification text,
          advisory_only boolean,
          timestamp_utc timestamptz
        ) RETURNS text
        LANGUAGE sql
        IMMUTABLE
        STRICT
        AS $function$
          SELECT
            ailora_audit_component(tenant_id::text) ||
            ailora_audit_component(event_id::text) ||
            ailora_audit_component(actor_user_id::text) ||
            ailora_audit_component(event_type) ||
            ailora_audit_component(resource_type) ||
            ailora_audit_component(resource_id::text) ||
            ailora_audit_component(outcome) ||
            ailora_audit_component(correlation_id::text) ||
            ailora_audit_component(detail) ||
            ailora_audit_component(combined_classification) ||
            ailora_audit_component(CASE WHEN advisory_only THEN 'true' ELSE 'false' END) ||
            ailora_audit_component(
              to_char(
                timestamp_utc AT TIME ZONE 'UTC',
                'YYYY-MM-DD"T"HH24:MI:SS.US"Z"'
              )
            )
        $function$;
        """
    )
    op.execute(
        """
        DO $backfill_audit_chain$
        DECLARE
          audit_row record;
          current_tenant uuid := NULL;
          next_sequence bigint := 0;
          predecessor_hash text := repeat('0', 64);
          payload text;
          calculated_hash text;
        BEGIN
          FOR audit_row IN
            SELECT * FROM ssa_audit_events
            ORDER BY tenant_id, timestamp_utc, id
          LOOP
            IF current_tenant IS DISTINCT FROM audit_row.tenant_id THEN
              current_tenant := audit_row.tenant_id;
              next_sequence := 0;
              predecessor_hash := repeat('0', 64);
            END IF;
            next_sequence := next_sequence + 1;
            payload := ailora_audit_payload(
              audit_row.tenant_id,
              audit_row.id,
              audit_row.actor_user_id,
              audit_row.event_type,
              audit_row.resource_type,
              audit_row.resource_id,
              audit_row.outcome,
              audit_row.correlation_id,
              audit_row.detail,
              audit_row.combined_classification,
              audit_row.advisory_only,
              audit_row.timestamp_utc
            );
            calculated_hash := encode(
              digest(convert_to(predecessor_hash || payload, 'UTF8'), 'sha256'),
              'hex'
            );
            UPDATE ssa_audit_events
            SET sequence_no = next_sequence,
                previous_hash = predecessor_hash,
                event_hash = calculated_hash
            WHERE id = audit_row.id;
            predecessor_hash := calculated_hash;
          END LOOP;
        END
        $backfill_audit_chain$;
        """
    )
    op.execute("ALTER TABLE ssa_audit_events ENABLE ROW LEVEL SECURITY")
    op.execute("ALTER TABLE ssa_audit_events FORCE ROW LEVEL SECURITY")


def _contract() -> None:
    op.alter_column("ssa_audit_events", "sequence_no", nullable=False)
    op.alter_column("ssa_audit_events", "previous_hash", nullable=False)
    op.alter_column("ssa_audit_events", "event_hash", nullable=False)
    op.create_check_constraint(
        "ck_ssa_audit_sequence_positive",
        "ssa_audit_events",
        "sequence_no > 0",
    )
    op.create_check_constraint(
        "ck_ssa_audit_previous_hash_length",
        "ssa_audit_events",
        "previous_hash ~ '^[0-9a-f]{64}$'",
    )
    op.create_check_constraint(
        "ck_ssa_audit_event_hash_length",
        "ssa_audit_events",
        "event_hash ~ '^[0-9a-f]{64}$'",
    )
    op.create_index(
        "uq_ssa_audit_tenant_sequence",
        "ssa_audit_events",
        ["tenant_id", "sequence_no"],
        unique=True,
    )
    op.create_index(
        "uq_ssa_audit_tenant_hash",
        "ssa_audit_events",
        ["tenant_id", "event_hash"],
        unique=True,
    )
    op.execute(
        """
        CREATE FUNCTION ailora_assign_audit_chain()
        RETURNS trigger
        LANGUAGE plpgsql
        AS $function$
        DECLARE
          predecessor_sequence bigint;
          predecessor_hash text;
          payload text;
        BEGIN
          PERFORM pg_advisory_xact_lock(hashtextextended(NEW.tenant_id::text, 0));
          SELECT sequence_no, event_hash
          INTO predecessor_sequence, predecessor_hash
          FROM ssa_audit_events
          WHERE tenant_id = NEW.tenant_id
          ORDER BY sequence_no DESC
          LIMIT 1;
          NEW.sequence_no := COALESCE(predecessor_sequence, 0) + 1;
          NEW.previous_hash := COALESCE(predecessor_hash, repeat('0', 64));
          payload := ailora_audit_payload(
            NEW.tenant_id,
            NEW.id,
            NEW.actor_user_id,
            NEW.event_type,
            NEW.resource_type,
            NEW.resource_id,
            NEW.outcome,
            NEW.correlation_id,
            NEW.detail,
            NEW.combined_classification,
            NEW.advisory_only,
            NEW.timestamp_utc
          );
          NEW.event_hash := encode(
            digest(convert_to(NEW.previous_hash || payload, 'UTF8'), 'sha256'),
            'hex'
          );
          RETURN NEW;
        END
        $function$;
        """
    )
    op.execute(
        """
        CREATE TRIGGER trg_ssa_audit_chain_insert
        BEFORE INSERT ON ssa_audit_events
        FOR EACH ROW EXECUTE FUNCTION ailora_assign_audit_chain();
        """
    )
    op.execute(
        """
        CREATE FUNCTION ailora_reject_audit_mutation()
        RETURNS trigger
        LANGUAGE plpgsql
        AS $function$
        BEGIN
          RAISE EXCEPTION 'ssa_audit_events is append-only';
        END
        $function$;
        """
    )
    op.execute(
        """
        CREATE TRIGGER trg_ssa_audit_immutable
        BEFORE UPDATE OR DELETE ON ssa_audit_events
        FOR EACH ROW EXECUTE FUNCTION ailora_reject_audit_mutation();
        """
    )
    op.execute(
        """
        DO $audit_role_contract$
        BEGIN
          IF to_regrole('ailora_runtime') IS NOT NULL THEN
            REVOKE UPDATE, DELETE ON TABLE ssa_audit_events FROM ailora_runtime;
            GRANT SELECT, INSERT ON TABLE ssa_audit_events TO ailora_runtime;
          END IF;
          IF to_regrole('ailora_readonly') IS NOT NULL THEN
            GRANT SELECT ON TABLE ssa_audit_events TO ailora_readonly;
          END IF;
        END
        $audit_role_contract$;
        """
    )


def upgrade() -> None:
    if not _postgresql():
        return
    _require_pgcrypto()
    _expand()
    _migrate()
    _contract()


def downgrade() -> None:
    if not _postgresql():
        return
    op.execute("DROP TRIGGER IF EXISTS trg_ssa_audit_immutable ON ssa_audit_events")
    op.execute("DROP FUNCTION IF EXISTS ailora_reject_audit_mutation()")
    op.execute("DROP TRIGGER IF EXISTS trg_ssa_audit_chain_insert ON ssa_audit_events")
    op.execute("DROP FUNCTION IF EXISTS ailora_assign_audit_chain()")
    op.drop_index("uq_ssa_audit_tenant_hash", table_name="ssa_audit_events")
    op.drop_index("uq_ssa_audit_tenant_sequence", table_name="ssa_audit_events")
    op.drop_constraint(
        "ck_ssa_audit_event_hash_length",
        "ssa_audit_events",
        type_="check",
    )
    op.drop_constraint(
        "ck_ssa_audit_previous_hash_length",
        "ssa_audit_events",
        type_="check",
    )
    op.drop_constraint(
        "ck_ssa_audit_sequence_positive",
        "ssa_audit_events",
        type_="check",
    )
    op.drop_column("ssa_audit_events", "event_hash")
    op.drop_column("ssa_audit_events", "previous_hash")
    op.drop_column("ssa_audit_events", "sequence_no")
    op.execute(
        "DROP FUNCTION IF EXISTS ailora_audit_payload("
        "uuid,uuid,uuid,text,text,uuid,text,uuid,text,text,boolean,timestamptz)"
    )
    op.execute("DROP FUNCTION IF EXISTS ailora_audit_component(text)")
