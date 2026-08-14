from __future__ import annotations

import uuid
from datetime import UTC, datetime, timedelta

import pytest
import pytest_asyncio
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from ailora.domain.identity.models import Tenant, User
from ailora.domain.space_data.contracts import canonical_payload_digest
from ailora.domain.space_data.models import (
    SpaceDataEvidenceRecord,
    SpaceDataObservationRecord,
    SpaceDataQuarantineRecord,
)
from ailora.domain.space_data.repository import SpaceDataRepository
from ailora.domain.space_data.service import (
    IngestionStatus,
    ObservationNotFoundError,
    SpaceDataIngestionService,
)

NOW = datetime(2026, 8, 14, 18, 45, tzinfo=UTC)


def payload(tenant_id: uuid.UUID, object_id: str = "SAT-25544") -> dict[str, object]:
    value: dict[str, object] = {
        "tenant_id": str(tenant_id),
        "observation_id": str(uuid.uuid4()),
        "object_id": object_id,
        "schema_version": "1.0",
        "reference_frame": "GCRF",
        "distance_unit": "km",
        "velocity_unit": "km/s",
        "time_scale": "UTC",
        "epoch": (NOW - timedelta(seconds=10)).isoformat(),
        "evaluated_at": NOW.isoformat(),
        "max_age_seconds": 60.0,
        "position": [7000.0, 0.0, 0.0],
        "velocity": [0.0, 7.5, 0.0],
        "covariance": None,
        "quality": "VALID",
        "advisory_only": True,
        "provenance": {
            "source_id": "provider-a",
            "source_version": "v1",
            "ingested_at": NOW.isoformat(),
            "canonical_digest": "0" * 64,
            "classification": "PUBLIC",
        },
    }
    provenance = value["provenance"]
    assert isinstance(provenance, dict)
    provenance["canonical_digest"] = canonical_payload_digest(value)
    return value


@pytest_asyncio.fixture
async def database() -> AsyncSession:
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as connection:
        await connection.run_sync(Tenant.__table__.create)
        await connection.run_sync(User.__table__.create)
        await connection.run_sync(
            lambda sync_connection: SpaceDataObservationRecord.__table__.create(sync_connection)
        )
        await connection.run_sync(
            lambda sync_connection: SpaceDataQuarantineRecord.__table__.create(sync_connection)
        )
        await connection.run_sync(
            lambda sync_connection: SpaceDataEvidenceRecord.__table__.create(sync_connection)
        )
    factory = async_sessionmaker(engine, expire_on_commit=False)
    async with factory() as session:
        yield session
    await engine.dispose()


@pytest.mark.asyncio
async def test_valid_observation_and_evidence_are_persisted_atomically(
    database: AsyncSession,
) -> None:
    tenant_id = uuid.uuid4()
    result = await SpaceDataIngestionService(database).ingest(
        tenant_id=tenant_id,
        actor_user_id=uuid.uuid4(),
        payload=payload(tenant_id),
    )
    await database.commit()
    assert result.status is IngestionStatus.ACCEPTED
    assert await database.scalar(select(func.count()).select_from(SpaceDataObservationRecord)) == 1
    assert await database.scalar(select(func.count()).select_from(SpaceDataEvidenceRecord)) == 1
    assert await database.scalar(select(func.count()).select_from(SpaceDataQuarantineRecord)) == 0


@pytest.mark.asyncio
async def test_invalid_observation_is_quarantined_without_raw_payload(
    database: AsyncSession,
) -> None:
    tenant_id = uuid.uuid4()
    invalid = payload(tenant_id)
    invalid["reference_frame"] = "UNKNOWN"
    result = await SpaceDataIngestionService(database).ingest(
        tenant_id=tenant_id,
        actor_user_id=uuid.uuid4(),
        payload=invalid,
    )
    await database.commit()
    assert result.status is IngestionStatus.QUARANTINED
    record = await database.scalar(select(SpaceDataQuarantineRecord))
    assert record is not None
    assert not hasattr(record, "raw_payload")
    assert len(record.canonical_digest) == 64
    assert await database.scalar(select(func.count()).select_from(SpaceDataObservationRecord)) == 0
    assert await database.scalar(select(func.count()).select_from(SpaceDataEvidenceRecord)) == 1


@pytest.mark.asyncio
async def test_duplicate_is_idempotent_and_audited(database: AsyncSession) -> None:
    tenant_id = uuid.uuid4()
    value = payload(tenant_id)
    service = SpaceDataIngestionService(database)
    first = await service.ingest(tenant_id=tenant_id, actor_user_id=uuid.uuid4(), payload=value)
    second = await service.ingest(tenant_id=tenant_id, actor_user_id=uuid.uuid4(), payload=value)
    await database.commit()
    assert first.status is IngestionStatus.ACCEPTED
    assert second.status is IngestionStatus.DUPLICATE
    assert first.observation_id == second.observation_id
    assert await database.scalar(select(func.count()).select_from(SpaceDataObservationRecord)) == 1
    assert await database.scalar(select(func.count()).select_from(SpaceDataEvidenceRecord)) == 2


@pytest.mark.asyncio
async def test_replay_preserves_digest_and_creates_new_processing_identity(
    database: AsyncSession,
) -> None:
    tenant_id = uuid.uuid4()
    actor_user_id = uuid.uuid4()
    service = SpaceDataIngestionService(database)
    accepted = await service.ingest(
        tenant_id=tenant_id,
        actor_user_id=actor_user_id,
        payload=payload(tenant_id),
    )
    replayed = await service.replay(
        tenant_id=tenant_id,
        actor_user_id=actor_user_id,
        source_observation_id=accepted.observation_id or "",
    )
    await database.commit()
    assert replayed.status is IngestionStatus.REPLAYED
    assert replayed.observation_id != accepted.observation_id
    assert replayed.canonical_digest == accepted.canonical_digest
    evidence = await database.scalar(
        select(SpaceDataEvidenceRecord).where(SpaceDataEvidenceRecord.id == replayed.evidence_id)
    )
    assert evidence is not None
    assert accepted.observation_id in evidence.detail


@pytest.mark.asyncio
async def test_cross_tenant_replay_fails_closed(database: AsyncSession) -> None:
    tenant_a = uuid.uuid4()
    tenant_b = uuid.uuid4()
    service = SpaceDataIngestionService(database)
    accepted = await service.ingest(
        tenant_id=tenant_a,
        actor_user_id=uuid.uuid4(),
        payload=payload(tenant_a),
    )
    with pytest.raises(ObservationNotFoundError):
        await service.replay(
            tenant_id=tenant_b,
            actor_user_id=uuid.uuid4(),
            source_observation_id=accepted.observation_id or "",
        )


@pytest.mark.asyncio
async def test_same_digest_is_isolated_by_tenant(database: AsyncSession) -> None:
    tenant_a = uuid.uuid4()
    tenant_b = uuid.uuid4()
    value_a = payload(tenant_a)
    value_b = dict(value_a)
    value_b["tenant_id"] = str(tenant_b)
    provenance = dict(value_a["provenance"])  # type: ignore[arg-type]
    value_b["provenance"] = provenance
    provenance["canonical_digest"] = canonical_payload_digest(value_b)
    service = SpaceDataIngestionService(database)
    assert (
        await service.ingest(tenant_id=tenant_a, actor_user_id=uuid.uuid4(), payload=value_a)
    ).status is IngestionStatus.ACCEPTED
    assert (
        await service.ingest(tenant_id=tenant_b, actor_user_id=uuid.uuid4(), payload=value_b)
    ).status is IngestionStatus.ACCEPTED
    await database.commit()
    assert await database.scalar(select(func.count()).select_from(SpaceDataObservationRecord)) == 2


@pytest.mark.asyncio
async def test_repository_has_no_update_or_delete_surface(database: AsyncSession) -> None:
    repository = SpaceDataRepository(database)
    assert not hasattr(repository, "update")
    assert not hasattr(repository, "delete")


@pytest.mark.asyncio
async def test_failure_after_observation_flush_rolls_back_everything(
    database: AsyncSession, monkeypatch: pytest.MonkeyPatch
) -> None:
    tenant_id = uuid.uuid4()

    async def fail_evidence(record: SpaceDataEvidenceRecord) -> SpaceDataEvidenceRecord:
        raise RuntimeError("simulated evidence failure")

    repository = SpaceDataRepository(database)
    monkeypatch.setattr(repository, "add_evidence", fail_evidence)
    service = SpaceDataIngestionService(database, repository=repository)
    with pytest.raises(RuntimeError, match="simulated"):
        await service.ingest(
            tenant_id=tenant_id,
            actor_user_id=uuid.uuid4(),
            payload=payload(tenant_id),
        )
    await database.rollback()
    assert await database.scalar(select(func.count()).select_from(SpaceDataObservationRecord)) == 0
    assert await database.scalar(select(func.count()).select_from(SpaceDataEvidenceRecord)) == 0


def test_implementation_contains_no_operational_command_surface() -> None:
    from pathlib import Path

    text = "\n".join(
        path.read_text(encoding="utf-8").lower()
        for path in Path("src/ailora/domain/space_data").glob("*.py")
    )
    for forbidden in (
        "execute_command(",
        "send_uplink(",
        "maneuver_execute(",
        "operational_clearance=true",
    ):
        assert forbidden not in text
