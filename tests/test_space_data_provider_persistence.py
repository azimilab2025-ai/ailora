from __future__ import annotations

import uuid
from datetime import UTC, datetime

import pytest
import pytest_asyncio
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from ailora.domain.identity.models import Tenant, User
from ailora.services.space_data.governance import (
    ProviderQualification,
    QualificationGate,
    QualificationState,
)
from ailora.services.space_data.interfaces import (
    ProviderRequest,
    ProviderResponse,
)
from ailora.services.space_data.models import (
    ProviderAttemptRecord,
    ProviderQualificationRecord,
    ProviderRawArtifactRecord,
)
from ailora.services.space_data.repository import ProviderRepository
from ailora.services.space_data.service import ProviderIngestionService

NOW = datetime(2026, 8, 14, 20, 0, tzinfo=UTC)


class FakeProvider:
    async def fetch(self, request: ProviderRequest) -> ProviderResponse:
        return ProviderResponse(
            provider_id="CELESTRAK",
            provider_version="gp-v1",
            request_id=request.request_id,
            object_id=request.object_id,
            fetched_at=NOW,
            status_code=200,
            content_type="text/plain",
            payload=b"raw-tle",
            attribution_text="attribution required",
        )


@pytest_asyncio.fixture
async def database() -> AsyncSession:
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as connection:
        await connection.run_sync(Tenant.__table__.create)
        await connection.run_sync(User.__table__.create)
        await connection.run_sync(ProviderQualificationRecord.__table__.create)
        await connection.run_sync(ProviderRawArtifactRecord.__table__.create)
        await connection.run_sync(ProviderAttemptRecord.__table__.create)
    factory = async_sessionmaker(engine, expire_on_commit=False)
    async with factory() as session:
        yield session
    await engine.dispose()


@pytest.mark.asyncio
async def test_raw_artifact_round_trip_and_tenant_dedup(database: AsyncSession) -> None:
    tenant_id = uuid.uuid4()
    actor_id = uuid.uuid4()
    qualification = ProviderQualificationRecord(
        id=uuid.uuid4().hex,
        reviewer_user_id=actor_id,
        provider_id="CELESTRAK",
        provider_version="gp-v1",
        state="QUALIFIED",
        license_name="EXTERNAL_REVIEW_REQUIRED",
        terms_uri="https://celestrak.org/",
        terms_digest="a" * 64,
        retrieved_at=NOW,
        reviewed_at=NOW,
        expires_at=None,
        reviewer_reference="LEGAL-001",
        redistribution_permitted=False,
        attribution_text="attribution required",
        created_at=NOW,
    )
    raw = ProviderRawArtifactRecord(
        id=uuid.uuid4().hex,
        tenant_id=tenant_id,
        actor_user_id=actor_id,
        qualification_id=qualification.id,
        request_id=uuid.uuid4().hex,
        provider_id="CELESTRAK",
        provider_version="gp-v1",
        external_object_id="25544",
        status_code=200,
        content_type="text/plain",
        fetched_at=NOW,
        payload=b"raw-tle",
        byte_length=7,
        payload_digest="b" * 64,
        classification="UNCLASSIFIED",
        attribution_text="attribution required",
        advisory_only=True,
        created_at=NOW,
    )
    repository = ProviderRepository(database)
    repository.add_qualification(qualification)
    repository.add_raw_artifact(raw)
    await database.commit()
    found = await repository.get_raw_by_digest(tenant_id, "CELESTRAK", "b" * 64)
    assert found is not None
    assert found.payload == b"raw-tle"


@pytest.mark.asyncio
async def test_ingestion_service_persists_raw_and_duplicate_attempt_evidence(
    database: AsyncSession,
) -> None:
    tenant_id = uuid.uuid4()
    actor_id = uuid.uuid4()
    qualification_id = uuid.uuid4()
    database.add(
        ProviderQualificationRecord(
            id=qualification_id.hex,
            reviewer_user_id=actor_id,
            provider_id="CELESTRAK",
            provider_version="gp-v1",
            state="QUALIFIED",
            license_name="EXTERNAL_REVIEW_REQUIRED",
            terms_uri="https://celestrak.org/",
            terms_digest="a" * 64,
            retrieved_at=NOW,
            reviewed_at=NOW,
            expires_at=None,
            reviewer_reference="LEGAL-001",
            redistribution_permitted=False,
            attribution_text="attribution required",
            created_at=NOW,
        )
    )
    await database.commit()
    qualification = ProviderQualification(
        qualification_id=qualification_id,
        provider_id="CELESTRAK",
        provider_version="gp-v1",
        state=QualificationState.QUALIFIED,
        license_name="EXTERNAL_REVIEW_REQUIRED",
        terms_uri="https://celestrak.org/",
        terms_digest="a" * 64,
        retrieved_at=NOW,
        reviewed_at=NOW,
        expires_at=None,
        reviewer_reference="LEGAL-001",
        redistribution_permitted=False,
        attribution_text="attribution required",
    )
    request = ProviderRequest(uuid.uuid4(), "25544", NOW, "advisory screening")
    service = ProviderIngestionService(database, FakeProvider(), QualificationGate())
    first = await service.ingest(
        tenant_id=tenant_id,
        actor_user_id=actor_id,
        request=request,
        qualification=qualification,
        classification="UNCLASSIFIED",
        now=NOW,
    )
    second = await service.ingest(
        tenant_id=tenant_id,
        actor_user_id=actor_id,
        request=request,
        qualification=qualification,
        classification="UNCLASSIFIED",
        now=NOW,
    )
    assert first.duplicate is False
    assert second.duplicate is True
    assert await database.scalar(select(func.count()).select_from(ProviderRawArtifactRecord)) == 1
    assert await database.scalar(select(func.count()).select_from(ProviderAttemptRecord)) == 2


def test_repository_is_append_only() -> None:
    assert not hasattr(ProviderRepository, "update")
    assert not hasattr(ProviderRepository, "delete")
