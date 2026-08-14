"""Security, persistence, physics-boundary, and API screening contracts."""

from __future__ import annotations

import importlib
from collections.abc import AsyncIterator

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from ailora.domain.identity.models import Membership, RoleEnum, Tenant, User
from ailora.domain.shared.value_objects import (
    CartesianState,
    Epoch,
    ReferenceFrame,
    TemporalStamp,
)
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

    try:
        importlib.import_module("ailora.domain.ssa.screening_models")
    except ModuleNotFoundError:
        pass

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


def _scenario_inputs(
    classification: DataClassification = DataClassification.SYNTHETIC,
) -> tuple[TemporalStamp, OrbitalObjectDescriptor, OrbitalObjectDescriptor]:
    epoch = Epoch(iso_utc="2026-08-14T00:00:00Z")
    stamp = TemporalStamp(epoch=epoch, frame=ReferenceFrame.TEME)
    provenance = DataProvenance(
        source_label="verified-screening-test",
        classification=classification,
        ingested_at=epoch,
        is_synthetic=classification is DataClassification.SYNTHETIC,
    )
    return (
        stamp,
        OrbitalObjectDescriptor(object_id="PRIMARY", provenance=provenance),
        OrbitalObjectDescriptor(object_id="SECONDARY", provenance=provenance),
    )


def _states(
    stamp: TemporalStamp,
    *,
    separation_m: float = 3_000.0,
) -> tuple[CartesianState, CartesianState]:
    primary = CartesianState(
        stamp=stamp,
        x_m=7_000_000.0,
        y_m=0.0,
        z_m=0.0,
        vx_ms=0.0,
        vy_ms=7_500.0,
        vz_ms=0.0,
    )
    secondary = CartesianState(
        stamp=stamp,
        x_m=7_000_000.0 + separation_m,
        y_m=0.0,
        z_m=0.0,
        vx_ms=0.0,
        vy_ms=7_500.0,
        vz_ms=0.0,
    )
    return primary, secondary


def _scenario_service(database: AsyncSession) -> object:
    module = importlib.import_module("ailora.domain.ssa.scenario_service")
    return module.TenantScenarioService(database)


def _screening_service(database: AsyncSession) -> object:
    module = importlib.import_module("ailora.domain.ssa.screening_service")
    return module.TenantScreeningService(database)


async def _create_scenario(
    database: AsyncSession,
    tenant: Tenant,
    user: User,
    *,
    classification: DataClassification = DataClassification.SYNTHETIC,
) -> object:
    stamp, primary, secondary = _scenario_inputs(classification)
    scenario = await _scenario_service(database).create_scenario(
        actor_user_id=user.id,
        tenant_id=tenant.id,
        reference_epoch=stamp,
        primary_object=primary,
        secondary_object=secondary,
    )
    await database.commit()
    return scenario


@pytest.mark.asyncio
async def test_active_member_creates_advisory_screening(database: AsyncSession) -> None:
    tenant, user = await _identity(database, slug="screening-create", email="member@screening.test")
    scenario = await _create_scenario(database, tenant, user)
    stamp = TemporalStamp.model_validate(scenario.reference_epoch)
    primary, secondary = _states(stamp)
    record = await _screening_service(database).create_screening(
        actor_user_id=user.id,
        tenant_id=tenant.id,
        scenario_id=scenario.id,
        primary_state=primary,
        secondary_state=secondary,
        threshold_km=5.0,
    )
    await database.commit()
    assert record.tenant_id == tenant.id
    assert record.scenario_id == scenario.id
    assert record.created_by_user_id == user.id
    assert record.outcome == "CONJUNCTION_POSSIBLE"
    assert record.tier == "T0_PHY_C1"
    assert record.distance_km == pytest.approx(3.0)
    assert record.advisory_only is True


@pytest.mark.asyncio
async def test_screening_inherits_scenario_classification(database: AsyncSession) -> None:
    tenant, user = await _identity(
        database, slug="screening-classification", email="class@screening.test"
    )
    scenario = await _create_scenario(
        database, tenant, user, classification=DataClassification.RESTRICTED
    )
    stamp = TemporalStamp.model_validate(scenario.reference_epoch)
    primary, secondary = _states(stamp)
    record = await _screening_service(database).create_screening(
        actor_user_id=user.id,
        tenant_id=tenant.id,
        scenario_id=scenario.id,
        primary_state=primary,
        secondary_state=secondary,
        threshold_km=5.0,
    )
    assert record.combined_classification == "RESTRICTED"


@pytest.mark.asyncio
async def test_cross_tenant_scenario_screening_is_denied(database: AsyncSession) -> None:
    module = importlib.import_module("ailora.domain.ssa.scenario_service")
    _, user_a = await _identity(database, slug="screen-a", email="a@screen.test")
    tenant_b, user_b = await _identity(database, slug="screen-b", email="b@screen.test")
    scenario_b = await _create_scenario(database, tenant_b, user_b)
    stamp = TemporalStamp.model_validate(scenario_b.reference_epoch)
    primary, secondary = _states(stamp)
    with pytest.raises(module.ScenarioAccessDeniedError):
        await _screening_service(database).create_screening(
            actor_user_id=user_a.id,
            tenant_id=tenant_b.id,
            scenario_id=scenario_b.id,
            primary_state=primary,
            secondary_state=secondary,
            threshold_km=5.0,
        )


@pytest.mark.asyncio
async def test_scenario_idor_is_not_found_inside_verified_tenant(
    database: AsyncSession,
) -> None:
    module = importlib.import_module("ailora.domain.ssa.scenario_service")
    tenant_a, user_a = await _identity(database, slug="sid-a", email="a@sid.test")
    tenant_b, user_b = await _identity(database, slug="sid-b", email="b@sid.test")
    scenario_b = await _create_scenario(database, tenant_b, user_b)
    stamp = TemporalStamp.model_validate(scenario_b.reference_epoch)
    primary, secondary = _states(stamp)
    with pytest.raises(module.ScenarioNotFoundError):
        await _screening_service(database).create_screening(
            actor_user_id=user_a.id,
            tenant_id=tenant_a.id,
            scenario_id=scenario_b.id,
            primary_state=primary,
            secondary_state=secondary,
            threshold_km=5.0,
        )


@pytest.mark.asyncio
async def test_screening_list_is_tenant_and_scenario_scoped(
    database: AsyncSession,
) -> None:
    tenant, user = await _identity(database, slug="screen-list", email="list@screen.test")
    scenario_one = await _create_scenario(database, tenant, user)
    scenario_two = await _create_scenario(database, tenant, user)
    for scenario in (scenario_one, scenario_two):
        stamp = TemporalStamp.model_validate(scenario.reference_epoch)
        primary, secondary = _states(stamp)
        await _screening_service(database).create_screening(
            actor_user_id=user.id,
            tenant_id=tenant.id,
            scenario_id=scenario.id,
            primary_state=primary,
            secondary_state=secondary,
            threshold_km=5.0,
        )
    records = await _screening_service(database).list_screenings(
        actor_user_id=user.id,
        tenant_id=tenant.id,
        scenario_id=scenario_one.id,
    )
    assert len(records) == 1
    assert records[0].scenario_id == scenario_one.id
    assert records[0].tenant_id == tenant.id


@pytest.mark.asyncio
async def test_screening_idor_is_not_found_inside_verified_scenario(
    database: AsyncSession,
) -> None:
    module = importlib.import_module("ailora.domain.ssa.screening_service")
    tenant, user = await _identity(database, slug="screen-idor", email="idor@screen.test")
    scenario_one = await _create_scenario(database, tenant, user)
    scenario_two = await _create_scenario(database, tenant, user)
    stamp = TemporalStamp.model_validate(scenario_two.reference_epoch)
    primary, secondary = _states(stamp)
    record_two = await _screening_service(database).create_screening(
        actor_user_id=user.id,
        tenant_id=tenant.id,
        scenario_id=scenario_two.id,
        primary_state=primary,
        secondary_state=secondary,
        threshold_km=5.0,
    )
    with pytest.raises(module.ScreeningNotFoundError):
        await _screening_service(database).get_screening(
            actor_user_id=user.id,
            tenant_id=tenant.id,
            scenario_id=scenario_one.id,
            screening_id=record_two.id,
        )


@pytest.mark.asyncio
async def test_inactive_identity_fails_closed(database: AsyncSession) -> None:
    module = importlib.import_module("ailora.domain.ssa.scenario_service")
    tenant, user = await _identity(
        database,
        slug="screen-inactive",
        email="inactive@screen.test",
        active=False,
    )
    with pytest.raises(module.ScenarioAccessDeniedError):
        await _screening_service(database).list_screenings(
            actor_user_id=user.id,
            tenant_id=tenant.id,
            scenario_id=__import__("uuid").uuid4(),
        )


@pytest.mark.asyncio
async def test_mismatched_epoch_is_rejected(database: AsyncSession) -> None:
    module = importlib.import_module("ailora.domain.ssa.screening_service")
    tenant, user = await _identity(database, slug="epoch-check", email="epoch@screen.test")
    scenario = await _create_scenario(database, tenant, user)
    scenario_stamp = TemporalStamp.model_validate(scenario.reference_epoch)
    primary, _ = _states(scenario_stamp)
    other_stamp = TemporalStamp(
        epoch=Epoch(iso_utc="2026-08-14T00:01:00Z"),
        frame=ReferenceFrame.TEME,
    )
    _, secondary = _states(other_stamp)
    with pytest.raises(module.ScreeningInputError, match="share epoch"):
        await _screening_service(database).create_screening(
            actor_user_id=user.id,
            tenant_id=tenant.id,
            scenario_id=scenario.id,
            primary_state=primary,
            secondary_state=secondary,
            threshold_km=5.0,
        )


def test_openapi_exposes_protected_screening_routes() -> None:
    app_module = importlib.import_module("ailora.api.app")
    schema = app_module.app.openapi()
    collection = "/v1/tenants/{tenant_id}/ssa/scenarios/{scenario_id}/screenings"
    item = collection + "/{screening_id}"
    assert {"get", "post"}.issubset(schema["paths"][collection])
    assert "get" in schema["paths"][item]
    for path, methods in ((collection, ("get", "post")), (item, ("get",))):
        for method in methods:
            assert schema["paths"][path][method].get("security")


def test_create_body_cannot_select_scope_or_authority() -> None:
    module = importlib.import_module("ailora.api.routers.ssa_screenings")
    fields = set(module.ScreeningCreateRequest.model_fields)
    assert fields == {"primary_state", "secondary_state", "threshold_km"}
    assert not fields.intersection(
        {"tenant_id", "scenario_id", "created_by_user_id", "advisory_only"}
    )


def test_response_contract_is_advisory_and_secret_safe() -> None:
    app_module = importlib.import_module("ailora.api.app")
    schema = app_module.app.openapi()
    fields = set(schema["components"]["schemas"]["ScreeningResponse"]["properties"])
    assert {"advisory_only", "tier", "outcome", "distance_km"}.issubset(fields)
    assert not fields.intersection({"password", "hashed_password", "token", "secret"})


def test_screening_api_has_no_command_or_collision_probability_capability() -> None:
    from pathlib import Path

    files = [
        Path("src/ailora/domain/ssa/screening_service.py"),
        Path("src/ailora/api/routers/ssa_screenings.py"),
    ]
    forbidden = [
        "execute_command(",
        "send_uplink(",
        "maneuver_execute(",
        "probability_of_collision",
        "collision_probability",
    ]
    text = "\n".join(path.read_text(encoding="utf-8").lower() for path in files)
    for pattern in forbidden:
        assert pattern not in text
