from __future__ import annotations

import uuid
from datetime import UTC, datetime
from pathlib import Path

import pytest
import pytest_asyncio
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from ailora.domain.identity.models import Tenant, User
from ailora.domain.space_data.contracts import ReferenceFrame, SpaceDataClassification
from ailora.domain.space_data.models import (
    SpaceDataEvidenceRecord,
    SpaceDataObservationRecord,
    SpaceDataQuarantineRecord,
)
from ailora.domain.space_data.service import IngestionStatus
from ailora.services.space_data.interfaces import ProviderResponse
from ailora.services.space_data.tle_bridge import TLEObservationBridge

LINE0 = "VANGUARD 1"
LINE1 = "1 00005U 58002B   00179.78495062  .00000023  00000-0  28098-4 0  4753"
LINE2 = "2 00005  34.2682 348.7242 1859667 331.7664  19.3264 10.82419157413667"
EPOCH = datetime(2000, 6, 27, 18, 50, 19, 733568, tzinfo=UTC)


@pytest_asyncio.fixture
async def database() -> AsyncSession:
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as connection:
        await connection.run_sync(Tenant.__table__.create)
        await connection.run_sync(User.__table__.create)
        await connection.run_sync(SpaceDataObservationRecord.__table__.create)
        await connection.run_sync(SpaceDataQuarantineRecord.__table__.create)
        await connection.run_sync(SpaceDataEvidenceRecord.__table__.create)
    factory = async_sessionmaker(engine, expire_on_commit=False)
    async with factory() as session:
        yield session
    await engine.dispose()


def response(*, payload: bytes | None = None, object_id: str = "00005") -> ProviderResponse:
    return ProviderResponse(
        provider_id="CELESTRAK",
        provider_version="gp-v1",
        request_id=uuid.uuid4(),
        object_id=object_id,
        fetched_at=EPOCH,
        status_code=200,
        content_type="text/plain",
        payload=payload or f"{LINE0}\n{LINE1}\n{LINE2}\n".encode(),
        attribution_text="CelesTrak attribution required",
    )


def test_observation_contract_accepts_truthful_native_teme_without_relabeling() -> None:
    assert ReferenceFrame.TEME.value == "TEME"
    assert ReferenceFrame.GCRF.value == "GCRF"


@pytest.mark.asyncio
async def test_valid_provider_tle_is_propagated_and_ingested_as_teme(
    database: AsyncSession,
) -> None:
    result = await TLEObservationBridge(database).ingest(
        tenant_id=uuid.uuid4(),
        actor_user_id=uuid.uuid4(),
        response=response(),
        evaluated_at=EPOCH,
        classification=SpaceDataClassification.PUBLIC,
    )
    assert result.status is IngestionStatus.ACCEPTED
    observation = await database.scalar(select(SpaceDataObservationRecord))
    assert observation is not None
    assert observation.reference_frame == "TEME"
    assert observation.distance_unit == "km"
    assert observation.velocity_unit == "km/s"
    assert observation.source_id == "CELESTRAK"
    assert "SGP4" in observation.source_version
    assert "RAW-" in observation.source_version
    assert observation.advisory_only is True


@pytest.mark.asyncio
async def test_malformed_or_identity_mismatched_tle_is_quarantined(
    database: AsyncSession,
) -> None:
    bridge = TLEObservationBridge(database)
    tenant_id = uuid.uuid4()
    malformed = await bridge.ingest(
        tenant_id=tenant_id,
        actor_user_id=uuid.uuid4(),
        response=response(payload=b"not-a-tle"),
        evaluated_at=EPOCH,
        classification=SpaceDataClassification.PUBLIC,
    )
    mismatched = await bridge.ingest(
        tenant_id=tenant_id,
        actor_user_id=uuid.uuid4(),
        response=response(object_id="25544"),
        evaluated_at=EPOCH,
        classification=SpaceDataClassification.PUBLIC,
    )
    assert malformed.status is IngestionStatus.QUARANTINED
    assert mismatched.status is IngestionStatus.QUARANTINED
    assert await database.scalar(select(func.count()).select_from(SpaceDataQuarantineRecord)) == 2
    assert await database.scalar(select(func.count()).select_from(SpaceDataObservationRecord)) == 0


@pytest.mark.asyncio
async def test_identical_provider_response_remains_tenant_scoped(database: AsyncSession) -> None:
    bridge = TLEObservationBridge(database)
    provider_response = response()
    for tenant_id in (uuid.uuid4(), uuid.uuid4()):
        result = await bridge.ingest(
            tenant_id=tenant_id,
            actor_user_id=uuid.uuid4(),
            response=provider_response,
            evaluated_at=EPOCH,
            classification=SpaceDataClassification.PUBLIC,
        )
        assert result.status is IngestionStatus.ACCEPTED
    assert await database.scalar(select(func.count()).select_from(SpaceDataObservationRecord)) == 2


def test_bridge_contains_no_unqualified_gcrf_conversion_or_network_path() -> None:
    source = Path("src/ailora/services/space_data/tle_bridge.py").read_text(encoding="utf-8")
    lowered = source.lower()
    assert "transform_to" not in lowered
    assert "import httpx" not in lowered
    assert "import requests" not in lowered
    assert "ReferenceFrame.GCRF" not in source
    assert 'ReferenceFrame("GCRF")' not in source
    assert "AstrodynamicsFrame.GCRF" not in source
