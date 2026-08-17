from __future__ import annotations

import importlib.util
import uuid
from collections.abc import AsyncIterator
from dataclasses import dataclass, replace
from datetime import UTC, datetime
from pathlib import Path
from types import ModuleType

import pytest
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from ailora.domain.identity.models import Membership, RoleEnum, Tenant, User
from ailora.domain.ssa.audit import AuditEventType
from ailora.domain.ssa.audit_integrity import (
    GENESIS_HASH,
    AuditIntegrityError,
    _component,
    assign_chain_values,
    canonical_audit_payload,
    compute_event_hash,
    verify_audit_chain,
)
from ailora.domain.ssa.audit_models import AuditEventRecord
from ailora.domain.ssa.audit_service import (
    AuditIntegrityViolationError,
    TenantAuditService,
)

ROOT = Path(__file__).parents[1]


def _migration_module() -> ModuleType:
    path = ROOT / "alembic/versions/0014_audit_integrity.py"
    spec = importlib.util.spec_from_file_location("audit_integrity_migration", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


MIGRATION = _migration_module()


@dataclass
class ChainRecord:
    id: uuid.UUID
    tenant_id: uuid.UUID
    actor_user_id: uuid.UUID
    event_type: str
    resource_type: str
    resource_id: uuid.UUID
    outcome: str
    correlation_id: uuid.UUID
    detail: str
    combined_classification: str
    advisory_only: bool
    timestamp_utc: datetime
    sequence_no: int = 0
    previous_hash: str = GENESIS_HASH
    event_hash: str = GENESIS_HASH


def _record(*, tenant_id: uuid.UUID | None = None, offset: int = 0) -> ChainRecord:
    return ChainRecord(
        id=uuid.UUID(int=100 + offset),
        tenant_id=tenant_id or uuid.UUID(int=1),
        actor_user_id=uuid.UUID(int=2),
        event_type="SCENARIO_INGESTED",
        resource_type="scenario",
        resource_id=uuid.UUID(int=3 + offset),
        outcome="SUCCESS",
        correlation_id=uuid.UUID(int=4 + offset),
        detail=f"safe detail {offset}",
        combined_classification="SYNTHETIC",
        advisory_only=True,
        timestamp_utc=datetime(2026, 8, 17, 12, 0, offset, 123456, tzinfo=UTC),
    )


def _chain(length: int = 3) -> list[ChainRecord]:
    records: list[ChainRecord] = []
    previous: ChainRecord | None = None
    for offset in range(length):
        record = _record(offset=offset)
        assign_chain_values(
            record,
            previous_sequence=previous.sequence_no if previous else None,
            previous_hash=previous.event_hash if previous else None,
        )
        records.append(record)
        previous = record
    return records


@pytest.fixture
async def database() -> AsyncIterator[AsyncSession]:
    from ailora.db.base import Base
    from ailora.domain.identity import session_models  # noqa: F401

    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    factory = async_sessionmaker(engine, expire_on_commit=False)
    async with factory() as session:
        yield session
    await engine.dispose()


def test_migration_chain_and_phase_names() -> None:
    assert MIGRATION.revision == "0014_audit_integrity"
    assert MIGRATION.down_revision == "0013_postgres_tenant_rls"
    assert all(hasattr(MIGRATION, name) for name in ("_expand", "_migrate", "_contract"))


def test_upgrade_rehearsal_orders_expand_migrate_contract(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[str] = []
    monkeypatch.setattr(MIGRATION, "_postgresql", lambda: True)
    for name in ("_require_pgcrypto", "_expand", "_migrate", "_contract"):
        monkeypatch.setattr(MIGRATION, name, lambda name=name: calls.append(name))
    MIGRATION.upgrade()
    assert calls == ["_require_pgcrypto", "_expand", "_migrate", "_contract"]


def test_non_postgres_upgrade_is_noop(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(MIGRATION, "_postgresql", lambda: False)
    monkeypatch.setattr(
        MIGRATION,
        "_expand",
        lambda: pytest.fail("non-PostgreSQL migration must be a no-op"),
    )
    MIGRATION.upgrade()


def test_migration_requires_preprovisioned_pgcrypto_without_creating_extension() -> None:
    source = (ROOT / "alembic/versions/0014_audit_integrity.py").read_text()
    assert "to_regprocedure('digest(bytea,text)')" in source
    assert "must be pre-provisioned" in source
    assert "CREATE EXTENSION" not in source


def test_migrate_phase_restores_forced_rls_after_transactional_backfill() -> None:
    source = (ROOT / "alembic/versions/0014_audit_integrity.py").read_text()
    no_force = source.index("NO FORCE ROW LEVEL SECURITY")
    disabled = source.index("DISABLE ROW LEVEL SECURITY")
    backfill = source.index("$backfill_audit_chain$")
    enabled = source.index("ENABLE ROW LEVEL SECURITY", backfill)
    forced = source.index("FORCE ROW LEVEL SECURITY", enabled)
    assert no_force < disabled < backfill < enabled < forced


def test_contract_has_database_hash_chain_and_concurrency_lock() -> None:
    source = (ROOT / "alembic/versions/0014_audit_integrity.py").read_text()
    for marker in (
        "digest(convert_to(",
        "pg_advisory_xact_lock",
        "hashtextextended",
        "trg_ssa_audit_chain_insert",
        "BEFORE INSERT",
        "sequence_no DESC",
    ):
        assert marker in source


def test_contract_rejects_update_delete_and_removes_runtime_privileges() -> None:
    source = (ROOT / "alembic/versions/0014_audit_integrity.py").read_text()
    assert "BEFORE UPDATE OR DELETE" in source
    assert "ssa_audit_events is append-only" in source
    assert "REVOKE UPDATE, DELETE" in source
    assert "GRANT SELECT, INSERT" in source
    assert "BYPASSRLS" not in source


def test_downgrade_drops_integrity_objects_without_disabling_rls() -> None:
    source = (ROOT / "alembic/versions/0014_audit_integrity.py").read_text()
    downgrade = source.split("def downgrade()", 1)[1]
    assert "DROP TRIGGER IF EXISTS trg_ssa_audit_immutable" in downgrade
    assert "DROP FUNCTION IF EXISTS ailora_audit_payload" in downgrade
    assert "DISABLE ROW LEVEL SECURITY" not in downgrade
    assert "GRANT UPDATE" not in downgrade


def test_component_uses_utf8_byte_length() -> None:
    assert _component("é") == "2:é"
    assert _component("safe") == "4:safe"


def test_canonical_payload_is_deterministic_and_length_prefixed() -> None:
    record = _record()
    first = canonical_audit_payload(record)
    second = canonical_audit_payload(replace(record))
    assert first == second
    assert first.startswith("36:00000000-0000-0000-0000-000000000001")
    assert first.endswith("27:2026-08-17T12:00:00.123456Z")


def test_genesis_assignment_and_hash_are_deterministic() -> None:
    record = _record()
    assign_chain_values(record, previous_sequence=None, previous_hash=None)
    assert record.sequence_no == 1
    assert record.previous_hash == GENESIS_HASH
    assert record.event_hash == compute_event_hash(
        previous_hash=GENESIS_HASH,
        payload=canonical_audit_payload(record),
    )


def test_multi_event_chain_verifies() -> None:
    verify_audit_chain(_chain())


@pytest.mark.parametrize(
    ("field", "replacement"),
    [
        ("event_type", "ACCESS_DENIED"),
        ("resource_type", "review"),
        ("outcome", "DENIED"),
        ("detail", "tampered"),
        ("combined_classification", "RESTRICTED"),
        ("advisory_only", False),
        ("actor_user_id", uuid.UUID(int=99)),
        ("resource_id", uuid.UUID(int=98)),
        ("correlation_id", uuid.UUID(int=97)),
    ],
)
def test_payload_tampering_is_detected(field: str, replacement: object) -> None:
    records = _chain()
    setattr(records[1], field, replacement)
    with pytest.raises(AuditIntegrityError, match="hash mismatch"):
        verify_audit_chain(records)


def test_sequence_gap_is_detected() -> None:
    records = _chain()
    records[1].sequence_no = 7
    with pytest.raises(AuditIntegrityError, match="sequence is discontinuous"):
        verify_audit_chain(records)


def test_predecessor_substitution_is_detected() -> None:
    records = _chain()
    records[1].previous_hash = GENESIS_HASH
    with pytest.raises(AuditIntegrityError, match="predecessor hash"):
        verify_audit_chain(records)


def test_cross_tenant_splice_is_detected() -> None:
    records = _chain()
    records[1].tenant_id = uuid.UUID(int=55)
    with pytest.raises(AuditIntegrityError, match="crosses tenant"):
        verify_audit_chain(records)


def test_malformed_predecessor_hash_is_rejected() -> None:
    with pytest.raises(AuditIntegrityError, match="lowercase SHA-256"):
        compute_event_hash(previous_hash="not-a-hash", payload="payload")


def test_sqlite_naive_timestamp_is_normalized_to_utc() -> None:
    record = _record()
    record.timestamp_utc = datetime(2026, 8, 17, 12, 0, 0)
    assert canonical_audit_payload(record).endswith("27:2026-08-17T12:00:00.000000Z")


@pytest.mark.asyncio
async def test_repository_assigns_tenant_chain_and_service_verifies(database: AsyncSession) -> None:
    tenant = Tenant(slug="integrity", display_name="Integrity", is_active=True)
    user = User(email="integrity@example.test", hashed_password="$2b$test", is_active=True)
    database.add_all([tenant, user])
    await database.flush()
    database.add(
        Membership(
            tenant_id=tenant.id,
            user_id=user.id,
            role=RoleEnum.OWNER,
            is_active=True,
        )
    )
    await database.flush()
    service = TenantAuditService(database)
    for offset in range(2):
        await service.append_event(
            tenant_id=tenant.id,
            actor_user_id=user.id,
            event_type=AuditEventType.SCENARIO_INGESTED,
            resource_type="scenario",
            resource_id=uuid.uuid4(),
            combined_classification="SYNTHETIC",
            detail=f"safe {offset}",
        )
    await database.commit()
    records = await service.list_events(actor_user_id=user.id, tenant_id=tenant.id)
    assert [record.sequence_no for record in records] == [1, 2]
    assert records[0].previous_hash == GENESIS_HASH
    assert records[1].previous_hash == records[0].event_hash
    verify_audit_chain(records)


@pytest.mark.asyncio
async def test_persisted_tampering_fails_closed_on_read(database: AsyncSession) -> None:
    tenant = Tenant(slug="tamper", display_name="Tamper", is_active=True)
    user = User(email="tamper@example.test", hashed_password="$2b$test", is_active=True)
    database.add_all([tenant, user])
    await database.flush()
    database.add(
        Membership(
            tenant_id=tenant.id,
            user_id=user.id,
            role=RoleEnum.OWNER,
            is_active=True,
        )
    )
    await database.flush()
    service = TenantAuditService(database)
    record = await service.append_event(
        tenant_id=tenant.id,
        actor_user_id=user.id,
        event_type=AuditEventType.SCENARIO_INGESTED,
        resource_type="scenario",
        resource_id=uuid.uuid4(),
        combined_classification="SYNTHETIC",
    )
    await database.commit()
    await database.execute(
        update(AuditEventRecord).where(AuditEventRecord.id == record.id).values(detail="tampered")
    )
    await database.commit()
    with pytest.raises(AuditIntegrityViolationError):
        await service.list_events(actor_user_id=user.id, tenant_id=tenant.id)
