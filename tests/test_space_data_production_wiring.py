from __future__ import annotations

import uuid
from datetime import UTC, datetime

import pytest
import pytest_asyncio
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from ailora.config import Settings
from ailora.db.base import Base
from ailora.domain.identity.models import Membership, RoleEnum, Tenant, User
from ailora.domain.space_data.contracts import SpaceDataClassification
from ailora.domain.space_data.models import (
    FrameTransformationEvidenceRecord,
    SpaceDataObservationRecord,
)
from ailora.domain.space_data.service import IngestionStatus
from ailora.services.space_data.governance import QualificationGate
from ailora.services.space_data.interfaces import ProviderRequest, ProviderResponse
from ailora.services.space_data.models import ProviderQualificationRecord, ProviderRawArtifactRecord
from ailora.services.space_data.production_wiring import (
    ProductionSpaceDataPipeline,
    ProductionWiringError,
    ProductionWiringErrorCode,
)
from ailora.services.space_data.service import ProviderIngestionService

LINE0 = "VANGUARD 1"
LINE1 = "1 00005U 58002B   00179.78495062  .00000023  00000-0  28098-4 0  4753"
LINE2 = "2 00005  34.2682 348.7242 1859667 331.7664  19.3264 10.82419157413667"
EPOCH = datetime(2000, 6, 27, 18, 50, 19, 733568, tzinfo=UTC)


class FakeProvider:
    def __init__(self) -> None:
        self.calls = 0

    async def fetch(self, request: ProviderRequest) -> ProviderResponse:
        self.calls += 1
        return ProviderResponse(
            provider_id="CELESTRAK",
            provider_version="gp-v1",
            request_id=request.request_id,
            object_id=request.object_id,
            fetched_at=EPOCH,
            status_code=200,
            content_type="text/plain",
            payload=f"{LINE0}\n{LINE1}\n{LINE2}\n".encode(),
            attribution_text="CelesTrak attribution required",
        )


@pytest_asyncio.fixture
async def database() -> AsyncSession:
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    factory = async_sessionmaker(engine, expire_on_commit=False)
    async with factory() as session:
        yield session
    await engine.dispose()


async def identity(database: AsyncSession) -> tuple[Tenant, User]:
    tenant = Tenant(slug=f"tenant-{uuid.uuid4().hex[:8]}", display_name="Tenant")
    user = User(email=f"{uuid.uuid4().hex}@example.test", hashed_password="$2b$test")
    database.add_all([tenant, user])
    await database.flush()
    database.add(
        Membership(
            tenant_id=tenant.id,
            user_id=user.id,
            role=RoleEnum.MEMBER,
            is_active=True,
        )
    )
    await database.commit()
    return tenant, user


async def qualify(database: AsyncSession, user: User) -> None:
    database.add(
        ProviderQualificationRecord(
            id=uuid.uuid4().hex,
            reviewer_user_id=user.id,
            provider_id="CELESTRAK",
            provider_version="gp-v1",
            state="QUALIFIED",
            license_name="EXTERNAL_REVIEW_REQUIRED",
            terms_uri="https://celestrak.org/",
            terms_digest="a" * 64,
            retrieved_at=EPOCH,
            reviewed_at=EPOCH,
            expires_at=None,
            reviewer_reference="LEGAL-001",
            redistribution_permitted=False,
            attribution_text="CelesTrak attribution required",
            created_at=EPOCH,
        )
    )
    await database.commit()


def pipeline(database: AsyncSession, provider: FakeProvider) -> ProductionSpaceDataPipeline:
    provider_ingestion = ProviderIngestionService(database, provider, QualificationGate())

    async def no_sleep(delay: float) -> None:
        del delay

    return ProductionSpaceDataPipeline(
        database,
        Settings(enable_live_space_data_provider=True),
        lambda: EPOCH,
        no_sleep,
        provider_ingestion=provider_ingestion,
    )


@pytest.mark.asyncio
async def test_real_pipeline_persists_raw_native_teme_gcrf_and_provenance(
    database: AsyncSession,
) -> None:
    tenant, user = await identity(database)
    await qualify(database, user)
    provider = FakeProvider()
    result = await pipeline(database, provider).ingest_gcrf(
        tenant_id=tenant.id,
        actor_user_id=user.id,
        object_id="00005",
        evaluated_at=EPOCH,
        idempotency_key="production-test-00005",
        classification=SpaceDataClassification.PUBLIC,
    )
    assert result.status is IngestionStatus.ACCEPTED
    assert result.target_frame == "GCRF"
    assert result.native_teme_observation_id is not None
    assert result.gcrf_observation_id is not None
    frames = set(
        (
            await database.scalars(
                select(SpaceDataObservationRecord.reference_frame).where(
                    SpaceDataObservationRecord.tenant_id == tenant.id
                )
            )
        ).all()
    )
    assert frames == {"TEME", "GCRF"}
    assert await database.scalar(select(func.count()).select_from(ProviderRawArtifactRecord)) == 1
    evidence = await database.scalar(select(FrameTransformationEvidenceRecord))
    assert evidence is not None
    assert evidence.transformation_digest == result.transformation_digest
    assert evidence.source_frame == "TEME"
    assert evidence.target_frame == "GCRF"


@pytest.mark.asyncio
async def test_idempotent_replay_deduplicates_all_persistent_outputs(
    database: AsyncSession,
) -> None:
    tenant, user = await identity(database)
    await qualify(database, user)
    provider = FakeProvider()
    service = pipeline(database, provider)
    arguments = {
        "tenant_id": tenant.id,
        "actor_user_id": user.id,
        "object_id": "00005",
        "evaluated_at": EPOCH,
        "idempotency_key": "repeatable-request-00005",
        "classification": SpaceDataClassification.PUBLIC,
    }
    first = await service.ingest_gcrf(**arguments)  # type: ignore[arg-type]
    second = await service.ingest_gcrf(**arguments)  # type: ignore[arg-type]
    assert first.gcrf_observation_id == second.gcrf_observation_id
    assert second.raw_duplicate is True
    assert await database.scalar(select(func.count()).select_from(ProviderRawArtifactRecord)) == 1
    assert await database.scalar(select(func.count()).select_from(SpaceDataObservationRecord)) == 2
    assert (
        await database.scalar(select(func.count()).select_from(FrameTransformationEvidenceRecord))
        == 1
    )


@pytest.mark.asyncio
async def test_authorization_and_qualification_fail_before_provider_network(
    database: AsyncSession,
) -> None:
    tenant, user = await identity(database)
    outsider = User(email=f"{uuid.uuid4().hex}@example.test", hashed_password="$2b$test")
    database.add(outsider)
    await database.commit()
    provider = FakeProvider()
    with pytest.raises(ProductionWiringError) as denied:
        await pipeline(database, provider).ingest_gcrf(
            tenant_id=tenant.id,
            actor_user_id=outsider.id,
            object_id="00005",
            evaluated_at=EPOCH,
            idempotency_key="denied-request-00005",
            classification=SpaceDataClassification.PUBLIC,
        )
    assert denied.value.code is ProductionWiringErrorCode.ACCESS_DENIED
    with pytest.raises(ProductionWiringError) as unqualified:
        await pipeline(database, provider).ingest_gcrf(
            tenant_id=tenant.id,
            actor_user_id=user.id,
            object_id="00005",
            evaluated_at=EPOCH,
            idempotency_key="unqualified-00005",
            classification=SpaceDataClassification.PUBLIC,
        )
    assert unqualified.value.code is ProductionWiringErrorCode.QUALIFICATION_REQUIRED
    assert provider.calls == 0


def test_openapi_exposes_only_authenticated_tenant_scoped_gcrf_ingestion() -> None:
    from ailora.api.app import app

    schema = app.openapi()
    path = "/v1/tenants/{tenant_id}/space-data/observations/gcrf:ingest"
    assert set(schema["paths"][path]) == {"post"}
    operation = schema["paths"][path]["post"]
    assert operation.get("security")
    response_schema = schema["components"]["schemas"]["GcrfIngestionResponse"]
    assert "target_frame" in response_schema["properties"]


def test_render_activates_live_provider_without_startup_fetch() -> None:
    from pathlib import Path

    text = Path("render.yaml").read_text(encoding="utf-8")
    assert 'AILORA_ENABLE_LIVE_SPACE_DATA_PROVIDER\n        value: "true"' in text
    app_source = Path("src/ailora/api/app.py").read_text(encoding="utf-8")
    assert "provider.fetch" not in app_source


def test_pipeline_has_no_spacecraft_command_surface() -> None:
    from pathlib import Path

    source = Path("src/ailora/services/space_data/production_wiring.py").read_text().lower()
    for forbidden in ("send_uplink", "execute_maneuver", "telecommand"):
        assert forbidden not in source
