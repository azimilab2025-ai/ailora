"""Security, persistence, and OpenAPI contracts for tenant SSA scenarios."""

from __future__ import annotations

import importlib
from collections.abc import AsyncIterator

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from ailora.domain.identity.models import Membership, RoleEnum, Tenant, User
from ailora.domain.shared.value_objects import Epoch, OrbitalRegime, TemporalStamp
from ailora.domain.ssa.scenario import (
    DataClassification,
    DataProvenance,
    OrbitalObjectDescriptor,
)


@pytest.fixture
async def database() -> AsyncIterator[AsyncSession]:
    from ailora.db.base import Base
    from ailora.domain.identity import session_models  # noqa: F401
    from ailora.domain.ssa import scenario_models  # noqa: F401

    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    factory = async_sessionmaker(engine, expire_on_commit=False)
    async with factory() as session:
        yield session
    await engine.dispose()


async def _identity(
    database: AsyncSession,
    *,
    slug: str,
    email: str,
    active: bool = True,
) -> tuple[Tenant, User]:
    tenant = Tenant(slug=slug, display_name=slug.title(), is_active=active)
    user = User(email=email, hashed_password="$2b$test", is_active=active)
    database.add_all([tenant, user])
    await database.flush()
    database.add(
        Membership(
            tenant_id=tenant.id,
            user_id=user.id,
            role=RoleEnum.MEMBER,
            is_active=active,
        )
    )
    await database.commit()
    return tenant, user


def _inputs(
    secondary_classification: DataClassification = DataClassification.SYNTHETIC,
) -> tuple[TemporalStamp, OrbitalObjectDescriptor, OrbitalObjectDescriptor]:
    epoch = Epoch(iso_utc="2026-08-14T00:00:00Z")
    stamp = TemporalStamp(epoch=epoch)
    primary = OrbitalObjectDescriptor(
        object_id="SAT-PRIMARY",
        object_name="Primary",
        regime=OrbitalRegime.LEO,
        provenance=DataProvenance(
            source_label="verified-test-source",
            classification=DataClassification.SYNTHETIC,
            ingested_at=epoch,
            is_synthetic=True,
        ),
    )
    secondary = OrbitalObjectDescriptor(
        object_id="SAT-SECONDARY",
        object_name="Secondary",
        regime=OrbitalRegime.LEO,
        provenance=DataProvenance(
            source_label="verified-test-source",
            classification=secondary_classification,
            ingested_at=epoch,
            is_synthetic=secondary_classification is DataClassification.SYNTHETIC,
        ),
    )
    return stamp, primary, secondary


def _service(database: AsyncSession) -> object:
    module = importlib.import_module("ailora.domain.ssa.scenario_service")
    return module.TenantScenarioService(database)


@pytest.mark.asyncio
async def test_active_member_creates_advisory_scenario(database: AsyncSession) -> None:
    tenant, user = await _identity(database, slug="create-scenario", email="member@create.test")
    stamp, primary, secondary = _inputs()
    record = await _service(database).create_scenario(
        actor_user_id=user.id,
        tenant_id=tenant.id,
        reference_epoch=stamp,
        primary_object=primary,
        secondary_object=secondary,
    )
    await database.commit()
    assert record.tenant_id == tenant.id
    assert record.created_by_user_id == user.id
    assert record.advisory_only is True


@pytest.mark.asyncio
async def test_classification_escalates_to_restricted(database: AsyncSession) -> None:
    tenant, user = await _identity(database, slug="restricted", email="member@restricted.test")
    stamp, primary, secondary = _inputs(DataClassification.RESTRICTED)
    record = await _service(database).create_scenario(
        actor_user_id=user.id,
        tenant_id=tenant.id,
        reference_epoch=stamp,
        primary_object=primary,
        secondary_object=secondary,
    )
    assert record.combined_classification == "RESTRICTED"


@pytest.mark.asyncio
async def test_cross_tenant_creation_is_denied(database: AsyncSession) -> None:
    module = importlib.import_module("ailora.domain.ssa.scenario_service")
    _, user_a = await _identity(database, slug="tenant-a", email="a@example.test")
    tenant_b, _ = await _identity(database, slug="tenant-b", email="b@example.test")
    stamp, primary, secondary = _inputs()
    with pytest.raises(module.ScenarioAccessDeniedError):
        await _service(database).create_scenario(
            actor_user_id=user_a.id,
            tenant_id=tenant_b.id,
            reference_epoch=stamp,
            primary_object=primary,
            secondary_object=secondary,
        )


@pytest.mark.asyncio
async def test_list_is_strictly_tenant_scoped(database: AsyncSession) -> None:
    tenant_a, user_a = await _identity(database, slug="list-a", email="a@list.test")
    tenant_b, user_b = await _identity(database, slug="list-b", email="b@list.test")
    stamp, primary, secondary = _inputs()
    await _service(database).create_scenario(
        actor_user_id=user_a.id,
        tenant_id=tenant_a.id,
        reference_epoch=stamp,
        primary_object=primary,
        secondary_object=secondary,
    )
    await _service(database).create_scenario(
        actor_user_id=user_b.id,
        tenant_id=tenant_b.id,
        reference_epoch=stamp,
        primary_object=primary,
        secondary_object=secondary,
    )
    records = await _service(database).list_scenarios(
        actor_user_id=user_a.id, tenant_id=tenant_a.id
    )
    assert len(records) == 1
    assert all(record.tenant_id == tenant_a.id for record in records)


@pytest.mark.asyncio
async def test_scenario_idor_is_not_found_in_verified_tenant(
    database: AsyncSession,
) -> None:
    module = importlib.import_module("ailora.domain.ssa.scenario_service")
    tenant_a, user_a = await _identity(database, slug="idor-a", email="a@idor.test")
    tenant_b, user_b = await _identity(database, slug="idor-b", email="b@idor.test")
    stamp, primary, secondary = _inputs()
    record_b = await _service(database).create_scenario(
        actor_user_id=user_b.id,
        tenant_id=tenant_b.id,
        reference_epoch=stamp,
        primary_object=primary,
        secondary_object=secondary,
    )
    with pytest.raises(module.ScenarioNotFoundError):
        await _service(database).get_scenario(
            actor_user_id=user_a.id,
            tenant_id=tenant_a.id,
            scenario_id=record_b.id,
        )


@pytest.mark.asyncio
async def test_inactive_identity_fails_closed(database: AsyncSession) -> None:
    module = importlib.import_module("ailora.domain.ssa.scenario_service")
    tenant, user = await _identity(
        database,
        slug="inactive-scenario",
        email="inactive@scenario.test",
        active=False,
    )
    with pytest.raises(module.ScenarioAccessDeniedError):
        await _service(database).list_scenarios(actor_user_id=user.id, tenant_id=tenant.id)


def test_openapi_exposes_protected_scenario_routes() -> None:
    app_module = importlib.import_module("ailora.api.app")
    schema = app_module.app.openapi()
    collection = "/v1/tenants/{tenant_id}/ssa/scenarios"
    item = collection + "/{scenario_id}"
    assert {"get", "post"}.issubset(schema["paths"][collection])
    assert "get" in schema["paths"][item]
    for path, methods in ((collection, ("get", "post")), (item, ("get",))):
        for method in methods:
            assert schema["paths"][path][method].get("security")


def test_create_body_cannot_select_tenant_or_creator() -> None:
    module = importlib.import_module("ailora.api.routers.ssa_scenarios")
    fields = set(module.ScenarioCreateRequest.model_fields)
    assert fields == {"reference_epoch", "primary_object", "secondary_object"}
    assert "tenant_id" not in fields
    assert "created_by_user_id" not in fields


def test_response_contract_is_advisory_and_secret_safe() -> None:
    app_module = importlib.import_module("ailora.api.app")
    schema = app_module.app.openapi()
    fields = set(schema["components"]["schemas"]["ScenarioResponse"]["properties"])
    assert "advisory_only" in fields
    assert not fields.intersection({"password", "hashed_password", "token", "secret"})


def test_scenario_modules_have_no_command_capability() -> None:
    from pathlib import Path

    files = [
        Path("src/ailora/domain/ssa/scenario_service.py"),
        Path("src/ailora/api/routers/ssa_scenarios.py"),
    ]
    forbidden = ["execute_command(", "send_uplink(", "maneuver_execute("]
    text = "\n".join(path.read_text(encoding="utf-8").lower() for path in files)
    for pattern in forbidden:
        assert pattern not in text
