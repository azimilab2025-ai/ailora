import importlib.util
from pathlib import Path
from types import ModuleType, SimpleNamespace
from uuid import UUID, uuid4

import pytest
from pydantic import ValidationError
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from starlette.requests import Request

from ailora.config import Settings
from ailora.db.tenant_context import (
    SESSION_CONTEXT_KEY,
    TenantDatabaseContext,
    _apply_postgres_transaction_context,
    clear_session_context,
    configure_session_context,
    context_from_request,
    transaction_settings,
)

ROOT = Path(__file__).parents[1]


def _migration_module() -> ModuleType:
    path = ROOT / "alembic/versions/0013_postgres_tenant_rls.py"
    spec = importlib.util.spec_from_file_location("postgres_tenant_rls", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


MIGRATION = _migration_module()

EXPECTED_TENANT_TABLES = {
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
}


def _request(
    *,
    tenant_id: object | None = None,
    actor_id: object | None = None,
    correlation_id: object | None = None,
) -> Request:
    request = Request(
        {
            "type": "http",
            "method": "GET",
            "path": "/",
            "headers": [],
            "path_params": {} if tenant_id is None else {"tenant_id": tenant_id},
        }
    )
    if actor_id is not None:
        request.state.actor_id = actor_id
    if correlation_id is not None:
        request.state.correlation_id = correlation_id
    return request


def _context() -> TenantDatabaseContext:
    return TenantDatabaseContext(
        tenant_id=UUID("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"),
        actor_id=UUID("bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb"),
        correlation_id=UUID("cccccccc-cccc-cccc-cccc-cccccccccccc"),
        statement_timeout_ms=10_000,
        lock_timeout_ms=2_000,
        idle_transaction_timeout_ms=15_000,
    )


def test_migration_chain_is_linear() -> None:
    assert MIGRATION.revision == "0013_postgres_tenant_rls"
    assert MIGRATION.down_revision == "0012_frame_transformations"


def test_rls_scope_is_exact_and_duplicate_free() -> None:
    assert set(MIGRATION.TENANT_TABLES) == EXPECTED_TENANT_TABLES
    assert len(MIGRATION.TENANT_TABLES) == len(EXPECTED_TENANT_TABLES) == 14


@pytest.mark.parametrize("table_name", sorted(EXPECTED_TENANT_TABLES))
def test_rls_policy_identifier_is_safe(table_name: str) -> None:
    assert MIGRATION._quoted(table_name) == f'"{table_name}"'


def test_unsafe_migration_identifier_is_rejected() -> None:
    with pytest.raises(ValueError, match="unsafe migration identifier"):
        MIGRATION._quoted('memberships"; DROP TABLE users; --')


def test_rls_expression_fails_closed_without_tenant_context() -> None:
    expression = MIGRATION._tenant_expression()
    assert "current_setting('app.current_tenant_id', true)" in expression
    assert "NULLIF" in expression
    assert expression.endswith("::uuid")


def test_migration_enables_forces_and_checks_rls(monkeypatch: pytest.MonkeyPatch) -> None:
    statements: list[str] = []
    monkeypatch.setattr(MIGRATION, "_postgresql", lambda: True)
    monkeypatch.setattr(
        MIGRATION.op, "execute", lambda statement: statements.append(str(statement))
    )

    MIGRATION.upgrade()

    joined = "\n".join(statements)
    for table_name in EXPECTED_TENANT_TABLES:
        assert f'ALTER TABLE "{table_name}" ENABLE ROW LEVEL SECURITY' in joined
        assert f'ALTER TABLE "{table_name}" FORCE ROW LEVEL SECURITY' in joined
        assert f'CREATE POLICY "tenant_isolation_{table_name}" ON "{table_name}"' in joined
    assert joined.count("WITH CHECK") == 14


def test_migration_uses_only_preprovisioned_bounded_roles(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    statements: list[str] = []
    monkeypatch.setattr(MIGRATION, "_postgresql", lambda: True)
    monkeypatch.setattr(
        MIGRATION.op, "execute", lambda statement: statements.append(str(statement))
    )

    MIGRATION.upgrade()

    grant_sql = statements[-1]
    assert "to_regrole('ailora_runtime')" in grant_sql
    assert "to_regrole('ailora_readonly')" in grant_sql
    assert "GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE" in grant_sql
    assert "GRANT SELECT ON TABLE" in grant_sql
    assert "ALL TABLES" not in grant_sql
    assert "CREATE ROLE" not in grant_sql
    assert "BYPASSRLS" not in grant_sql


def test_non_postgres_upgrade_is_noop(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(MIGRATION, "_postgresql", lambda: False)
    monkeypatch.setattr(
        MIGRATION.op,
        "execute",
        lambda statement: pytest.fail(f"unexpected SQL: {statement}"),
    )
    MIGRATION.upgrade()


def test_downgrade_removes_policy_before_disabling_rls(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    statements: list[str] = []
    monkeypatch.setattr(MIGRATION, "_postgresql", lambda: True)
    monkeypatch.setattr(
        MIGRATION.op, "execute", lambda statement: statements.append(str(statement))
    )

    MIGRATION.downgrade()

    for table_name in EXPECTED_TENANT_TABLES:
        policy = f'DROP POLICY IF EXISTS "tenant_isolation_{table_name}"'
        no_force = f'ALTER TABLE "{table_name}" NO FORCE ROW LEVEL SECURITY'
        disable = f'ALTER TABLE "{table_name}" DISABLE ROW LEVEL SECURITY'
        assert statements.index(
            next(item for item in statements if policy in item)
        ) < statements.index(no_force)
        assert statements.index(no_force) < statements.index(disable)


def test_transaction_settings_are_exact_and_bounded() -> None:
    assert transaction_settings(_context()) == (
        ("app.current_tenant_id", "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"),
        ("app.current_actor_id", "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb"),
        ("app.correlation_id", "cccccccc-cccc-cccc-cccc-cccccccccccc"),
        ("statement_timeout", "10000ms"),
        ("lock_timeout", "2000ms"),
        ("idle_in_transaction_session_timeout", "15000ms"),
    )


def test_missing_identity_becomes_empty_fail_closed_context() -> None:
    context = TenantDatabaseContext(
        tenant_id=None,
        actor_id=None,
        correlation_id=uuid4(),
        statement_timeout_ms=100,
        lock_timeout_ms=50,
        idle_transaction_timeout_ms=1_000,
    )
    settings = dict(transaction_settings(context))
    assert settings["app.current_tenant_id"] == ""
    assert settings["app.current_actor_id"] == ""


def test_request_context_preserves_valid_uuid_identity() -> None:
    tenant_id = uuid4()
    actor_id = uuid4()
    correlation_id = uuid4()
    context = context_from_request(
        _request(tenant_id=str(tenant_id), actor_id=actor_id, correlation_id=str(correlation_id)),
        statement_timeout_ms=5_000,
        lock_timeout_ms=1_000,
        idle_transaction_timeout_ms=9_000,
    )
    assert context.tenant_id == tenant_id
    assert context.actor_id == actor_id
    assert context.correlation_id == correlation_id


def test_request_context_rejects_invalid_untrusted_uuid_identity() -> None:
    context = context_from_request(
        _request(tenant_id="not-a-uuid", actor_id="bad", correlation_id="also-bad"),
        statement_timeout_ms=5_000,
        lock_timeout_ms=1_000,
        idle_transaction_timeout_ms=9_000,
    )
    assert context.tenant_id is None
    assert context.actor_id is None
    assert isinstance(context.correlation_id, UUID)


def test_session_context_is_attached_and_cleared() -> None:
    session = SimpleNamespace(sync_session=SimpleNamespace(info={}))
    configure_session_context(session, _context())  # type: ignore[arg-type]
    assert session.sync_session.info[SESSION_CONTEXT_KEY] == _context()
    clear_session_context(session)  # type: ignore[arg-type]
    assert SESSION_CONTEXT_KEY not in session.sync_session.info


def test_sqlite_transaction_listener_is_noop() -> None:
    context = _context()
    with Session(create_engine("sqlite://")) as session:
        session.info[SESSION_CONTEXT_KEY] = context
        assert session.execute(__import__("sqlalchemy").text("SELECT 1")).scalar_one() == 1


def test_postgres_transaction_listener_sets_every_value() -> None:
    calls: list[tuple[str, dict[str, str]]] = []
    session = SimpleNamespace(info={SESSION_CONTEXT_KEY: _context()})
    connection = SimpleNamespace(
        dialect=SimpleNamespace(name="postgresql"),
        execute=lambda statement, parameters: calls.append((str(statement), parameters)),
    )

    _apply_postgres_transaction_context(session, object(), connection)  # type: ignore[arg-type]

    assert len(calls) == 6
    assert all("set_config" in statement for statement, _ in calls)
    assert [parameters["setting_name"] for _, parameters in calls] == [
        name for name, _ in transaction_settings(_context())
    ]
    assert [parameters["setting_value"] for _, parameters in calls] == [
        value for _, value in transaction_settings(_context())
    ]


def test_database_timeout_defaults_are_bounded() -> None:
    settings = Settings(_env_file=None)
    assert settings.database_statement_timeout_ms == 10_000
    assert settings.database_lock_timeout_ms == 2_000
    assert settings.database_idle_transaction_timeout_ms == 15_000


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("database_statement_timeout_ms", 99),
        ("database_lock_timeout_ms", 49),
        ("database_idle_transaction_timeout_ms", 999),
        ("database_statement_timeout_ms", 120_001),
        ("database_lock_timeout_ms", 30_001),
        ("database_idle_transaction_timeout_ms", 120_001),
    ],
)
def test_database_timeout_bounds_reject_unsafe_values(field: str, value: int) -> None:
    with pytest.raises(ValidationError):
        Settings(_env_file=None, **{field: value})
