"""Security, persistence, and API contracts for tenant SSA risk assessments."""

from __future__ import annotations

import importlib
import uuid
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
    from ailora.domain.ssa import scenario_models, screening_models  # noqa: F401

    try:
        importlib.import_module("ailora.domain.ssa.risk_models")
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
        source_label="verified-risk-test",
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
    return importlib.import_module("ailora.domain.ssa.scenario_service").TenantScenarioService(
        database
    )


def _screening_service(database: AsyncSession) -> object:
    return importlib.import_module("ailora.domain.ssa.screening_service").TenantScreeningService(
        database
    )


def _risk_service(database: AsyncSession) -> object:
    return importlib.import_module("ailora.domain.ssa.risk_service").TenantRiskAssessmentService(
        database
    )


async def _create_screening(
    database: AsyncSession,
    tenant: Tenant,
    user: User,
    *,
    classification: DataClassification = DataClassification.SYNTHETIC,
    separation_m: float = 3_000.0,
) -> tuple[object, object]:
    stamp, primary_object, secondary_object = _scenario_inputs(classification)
    scenario = await _scenario_service(database).create_scenario(
        actor_user_id=user.id,
        tenant_id=tenant.id,
        reference_epoch=stamp,
        primary_object=primary_object,
        secondary_object=secondary_object,
    )
    primary_state, secondary_state = _states(stamp, separation_m=separation_m)
    screening = await _screening_service(database).create_screening(
        actor_user_id=user.id,
        tenant_id=tenant.id,
        scenario_id=scenario.id,
        primary_state=primary_state,
        secondary_state=secondary_state,
        threshold_km=5.0,
    )
    await database.commit()
    return scenario, screening


@pytest.mark.asyncio
async def test_active_member_creates_advisory_high_risk_assessment(
    database: AsyncSession,
) -> None:
    tenant, user = await _identity(database, slug="risk-create", email="member@risk.test")
    scenario, screening = await _create_screening(database, tenant, user)
    record = await _risk_service(database).create_assessment(
        actor_user_id=user.id,
        tenant_id=tenant.id,
        scenario_id=scenario.id,
        screening_id=screening.id,
    )
    await database.commit()
    assert record.tenant_id == tenant.id
    assert record.scenario_id == scenario.id
    assert record.screening_id == screening.id
    assert record.risk_level == "HIGH"
    assert record.distance_km == pytest.approx(3.0)
    assert record.advisory_only is True
    assert "advisory" in record.provenance_label.lower()
    assert "not an operational command" in record.recommendation.lower()


@pytest.mark.asyncio
async def test_risk_inherits_restricted_classification(database: AsyncSession) -> None:
    tenant, user = await _identity(database, slug="risk-class", email="class@risk.test")
    scenario, screening = await _create_screening(
        database,
        tenant,
        user,
        classification=DataClassification.RESTRICTED,
    )
    record = await _risk_service(database).create_assessment(
        actor_user_id=user.id,
        tenant_id=tenant.id,
        scenario_id=scenario.id,
        screening_id=screening.id,
    )
    assert record.combined_classification == "RESTRICTED"


@pytest.mark.asyncio
async def test_cross_tenant_risk_creation_is_denied(database: AsyncSession) -> None:
    scenario_module = importlib.import_module("ailora.domain.ssa.scenario_service")
    _, user_a = await _identity(database, slug="risk-a", email="a@risk.test")
    tenant_b, user_b = await _identity(database, slug="risk-b", email="b@risk.test")
    scenario_b, screening_b = await _create_screening(database, tenant_b, user_b)
    with pytest.raises(scenario_module.ScenarioAccessDeniedError):
        await _risk_service(database).create_assessment(
            actor_user_id=user_a.id,
            tenant_id=tenant_b.id,
            scenario_id=scenario_b.id,
            screening_id=screening_b.id,
        )


@pytest.mark.asyncio
async def test_scenario_idor_is_not_found_inside_verified_tenant(
    database: AsyncSession,
) -> None:
    scenario_module = importlib.import_module("ailora.domain.ssa.scenario_service")
    tenant_a, user_a = await _identity(database, slug="risk-sid-a", email="a@sidrisk.test")
    tenant_b, user_b = await _identity(database, slug="risk-sid-b", email="b@sidrisk.test")
    scenario_b, screening_b = await _create_screening(database, tenant_b, user_b)
    with pytest.raises(scenario_module.ScenarioNotFoundError):
        await _risk_service(database).create_assessment(
            actor_user_id=user_a.id,
            tenant_id=tenant_a.id,
            scenario_id=scenario_b.id,
            screening_id=screening_b.id,
        )


@pytest.mark.asyncio
async def test_screening_idor_is_not_found_inside_verified_scenario(
    database: AsyncSession,
) -> None:
    screening_module = importlib.import_module("ailora.domain.ssa.screening_service")
    tenant, user = await _identity(database, slug="risk-screen-idor", email="sid@risk.test")
    scenario_one, _ = await _create_screening(database, tenant, user)
    _, screening_two = await _create_screening(database, tenant, user)
    with pytest.raises(screening_module.ScreeningNotFoundError):
        await _risk_service(database).create_assessment(
            actor_user_id=user.id,
            tenant_id=tenant.id,
            scenario_id=scenario_one.id,
            screening_id=screening_two.id,
        )


@pytest.mark.asyncio
async def test_risk_list_is_fully_scope_filtered(database: AsyncSession) -> None:
    tenant, user = await _identity(database, slug="risk-list", email="list@risk.test")
    scenario_one, screening_one = await _create_screening(database, tenant, user)
    scenario_two, screening_two = await _create_screening(database, tenant, user)
    for scenario, screening in (
        (scenario_one, screening_one),
        (scenario_two, screening_two),
    ):
        await _risk_service(database).create_assessment(
            actor_user_id=user.id,
            tenant_id=tenant.id,
            scenario_id=scenario.id,
            screening_id=screening.id,
        )
    records = await _risk_service(database).list_assessments(
        actor_user_id=user.id,
        tenant_id=tenant.id,
        scenario_id=scenario_one.id,
        screening_id=screening_one.id,
    )
    assert len(records) == 1
    assert records[0].screening_id == screening_one.id


@pytest.mark.asyncio
async def test_risk_assessment_idor_is_not_found_inside_verified_screening(
    database: AsyncSession,
) -> None:
    risk_module = importlib.import_module("ailora.domain.ssa.risk_service")
    tenant, user = await _identity(database, slug="risk-idor", email="idor@risk.test")
    scenario_one, screening_one = await _create_screening(database, tenant, user)
    scenario_two, screening_two = await _create_screening(database, tenant, user)
    record_two = await _risk_service(database).create_assessment(
        actor_user_id=user.id,
        tenant_id=tenant.id,
        scenario_id=scenario_two.id,
        screening_id=screening_two.id,
    )
    with pytest.raises(risk_module.RiskAssessmentNotFoundError):
        await _risk_service(database).get_assessment(
            actor_user_id=user.id,
            tenant_id=tenant.id,
            scenario_id=scenario_one.id,
            screening_id=screening_one.id,
            assessment_id=record_two.id,
        )


@pytest.mark.asyncio
async def test_inactive_identity_fails_closed(database: AsyncSession) -> None:
    scenario_module = importlib.import_module("ailora.domain.ssa.scenario_service")
    tenant, user = await _identity(
        database,
        slug="risk-inactive",
        email="inactive@risk.test",
        active=False,
    )
    with pytest.raises(scenario_module.ScenarioAccessDeniedError):
        await _risk_service(database).list_assessments(
            actor_user_id=user.id,
            tenant_id=tenant.id,
            scenario_id=uuid.uuid4(),
            screening_id=uuid.uuid4(),
        )


def test_openapi_exposes_protected_risk_routes() -> None:
    app_module = importlib.import_module("ailora.api.app")
    schema = app_module.app.openapi()
    collection = (
        "/v1/tenants/{tenant_id}/ssa/scenarios/{scenario_id}"
        "/screenings/{screening_id}/risk-assessments"
    )
    item = collection + "/{assessment_id}"
    assert {"get", "post"}.issubset(schema["paths"][collection])
    assert "get" in schema["paths"][item]
    for path, methods in ((collection, ("get", "post")), (item, ("get",))):
        for method in methods:
            assert schema["paths"][path][method].get("security")


def test_post_has_no_body_control_over_scope_or_output() -> None:
    app_module = importlib.import_module("ailora.api.app")
    schema = app_module.app.openapi()
    collection = (
        "/v1/tenants/{tenant_id}/ssa/scenarios/{scenario_id}"
        "/screenings/{screening_id}/risk-assessments"
    )
    operation = schema["paths"][collection]["post"]
    assert "requestBody" not in operation


def test_response_contract_is_advisory_and_secret_safe() -> None:
    app_module = importlib.import_module("ailora.api.app")
    schema = app_module.app.openapi()
    fields = set(schema["components"]["schemas"]["RiskAssessmentResponse"]["properties"])
    required = {
        "risk_level",
        "explanation",
        "recommendation",
        "provenance_label",
        "advisory_only",
    }
    assert required.issubset(fields)
    assert not fields.intersection({"password", "hashed_password", "token", "secret"})
    assert not fields.intersection({"probability_of_collision", "collision_probability", "pc"})


def test_risk_api_has_no_spacecraft_command_capability() -> None:
    from pathlib import Path

    files = [
        Path("src/ailora/domain/ssa/risk_service.py"),
        Path("src/ailora/api/routers/ssa_risk_assessments.py"),
    ]
    forbidden = ["execute_command(", "send_uplink(", "maneuver_execute("]
    text = "\n".join(path.read_text(encoding="utf-8").lower() for path in files)
    for pattern in forbidden:
        assert pattern not in text
