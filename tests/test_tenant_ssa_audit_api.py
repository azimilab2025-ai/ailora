"""Transactional, tenant isolation, immutability, and API contracts for SSA audit."""

from __future__ import annotations

import importlib
import uuid
from collections.abc import AsyncIterator

import pytest
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from ailora.domain.identity.models import Membership, RoleEnum, Tenant, User
from ailora.domain.shared.value_objects import CartesianState, Epoch, ReferenceFrame, TemporalStamp
from ailora.domain.ssa.review import ReviewState
from ailora.domain.ssa.scenario import DataClassification, DataProvenance, OrbitalObjectDescriptor


@pytest.fixture
async def database() -> AsyncIterator[AsyncSession]:
    from ailora.db.base import Base
    from ailora.domain.identity import session_models  # noqa: F401
    from ailora.domain.ssa import (  # noqa: F401
        risk_models,
        scenario_models,
        screening_models,
    )

    for module_name in ("review_models", "audit_models"):
        try:
            importlib.import_module(f"ailora.domain.ssa.{module_name}")
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
            role=RoleEnum.OWNER,
            is_active=active,
        )
    )
    await database.commit()
    return tenant, user


def _inputs(
    classification: DataClassification = DataClassification.SYNTHETIC,
) -> tuple[TemporalStamp, OrbitalObjectDescriptor, OrbitalObjectDescriptor]:
    epoch = Epoch(iso_utc="2026-08-14T00:00:00Z")
    stamp = TemporalStamp(epoch=epoch, frame=ReferenceFrame.TEME)
    provenance = DataProvenance(
        source_label="audit-test",
        classification=classification,
        ingested_at=epoch,
        is_synthetic=classification is DataClassification.SYNTHETIC,
    )
    return (
        stamp,
        OrbitalObjectDescriptor(object_id="PRIMARY", provenance=provenance),
        OrbitalObjectDescriptor(object_id="SECONDARY", provenance=provenance),
    )


def _states(stamp: TemporalStamp) -> tuple[CartesianState, CartesianState]:
    return (
        CartesianState(
            stamp=stamp,
            x_m=7_000_000.0,
            y_m=0.0,
            z_m=0.0,
            vx_ms=0.0,
            vy_ms=7_500.0,
            vz_ms=0.0,
        ),
        CartesianState(
            stamp=stamp,
            x_m=7_003_000.0,
            y_m=0.0,
            z_m=0.0,
            vx_ms=0.0,
            vy_ms=7_500.0,
            vz_ms=0.0,
        ),
    )


async def _workflow(
    database: AsyncSession,
    tenant: Tenant,
    user: User,
    *,
    classification: DataClassification = DataClassification.SYNTHETIC,
) -> tuple[object, object, object, object]:
    scenario_service = importlib.import_module("ailora.domain.ssa.scenario_service")
    screening_service = importlib.import_module("ailora.domain.ssa.screening_service")
    risk_service = importlib.import_module("ailora.domain.ssa.risk_service")
    review_service = importlib.import_module("ailora.domain.ssa.review_service")
    stamp, primary_object, secondary_object = _inputs(classification)
    scenario = await scenario_service.TenantScenarioService(database).create_scenario(
        actor_user_id=user.id,
        tenant_id=tenant.id,
        reference_epoch=stamp,
        primary_object=primary_object,
        secondary_object=secondary_object,
    )
    primary_state, secondary_state = _states(stamp)
    screening = await screening_service.TenantScreeningService(database).create_screening(
        actor_user_id=user.id,
        tenant_id=tenant.id,
        scenario_id=scenario.id,
        primary_state=primary_state,
        secondary_state=secondary_state,
        threshold_km=5.0,
    )
    assessment = await risk_service.TenantRiskAssessmentService(database).create_assessment(
        actor_user_id=user.id,
        tenant_id=tenant.id,
        scenario_id=scenario.id,
        screening_id=screening.id,
    )
    review = await review_service.TenantReviewService(database).create_review(
        actor_user_id=user.id,
        tenant_id=tenant.id,
        scenario_id=scenario.id,
        screening_id=screening.id,
        assessment_id=assessment.id,
    )
    await database.commit()
    return scenario, screening, assessment, review


@pytest.mark.asyncio
async def test_lifecycle_writes_transactional_ordered_audit(database: AsyncSession) -> None:
    tenant, owner = await _identity(database, slug="audit-flow", email="flow@audit.test")
    scenario, screening, assessment, review = await _workflow(database, tenant, owner)
    module = importlib.import_module("ailora.domain.ssa.audit_service")
    records = await module.TenantAuditService(database).list_events(
        actor_user_id=owner.id, tenant_id=tenant.id
    )
    assert [record.event_type for record in records] == [
        "SCENARIO_INGESTED",
        "SCENARIO_SCREENED",
        "SCENARIO_RISK_ASSESSED",
        "REVIEW_OPENED",
    ]
    assert [record.resource_id for record in records] == [
        scenario.id,
        screening.id,
        assessment.id,
        review.id,
    ]
    assert all(record.advisory_only is True for record in records)
    assert len({record.correlation_id for record in records}) == 4


@pytest.mark.asyncio
async def test_review_transition_and_close_are_audited(database: AsyncSession) -> None:
    tenant, owner = await _identity(database, slug="audit-review", email="review@audit.test")
    scenario, screening, assessment, review = await _workflow(database, tenant, owner)
    review_module = importlib.import_module("ailora.domain.ssa.review_service")
    service = review_module.TenantReviewService(database)
    await service.transition_review(
        actor_user_id=owner.id,
        tenant_id=tenant.id,
        scenario_id=scenario.id,
        screening_id=screening.id,
        assessment_id=assessment.id,
        review_id=review.id,
        target_state=ReviewState.UNDER_REVIEW,
    )
    await service.transition_review(
        actor_user_id=owner.id,
        tenant_id=tenant.id,
        scenario_id=scenario.id,
        screening_id=screening.id,
        assessment_id=assessment.id,
        review_id=review.id,
        target_state=ReviewState.REVIEWED,
    )
    await service.transition_review(
        actor_user_id=owner.id,
        tenant_id=tenant.id,
        scenario_id=scenario.id,
        screening_id=screening.id,
        assessment_id=assessment.id,
        review_id=review.id,
        target_state=ReviewState.CLOSED,
    )
    await database.commit()
    audit_module = importlib.import_module("ailora.domain.ssa.audit_service")
    records = await audit_module.TenantAuditService(database).list_events(
        actor_user_id=owner.id, tenant_id=tenant.id
    )
    assert [record.event_type for record in records[-3:]] == [
        "REVIEW_STATE_CHANGED",
        "REVIEW_STATE_CHANGED",
        "REVIEW_CLOSED",
    ]


@pytest.mark.asyncio
async def test_business_and_audit_rows_rollback_together(database: AsyncSession) -> None:
    tenant, owner = await _identity(database, slug="audit-rollback", email="rollback@audit.test")
    stamp, primary, secondary = _inputs()
    scenario_module = importlib.import_module("ailora.domain.ssa.scenario_service")
    await scenario_module.TenantScenarioService(database).create_scenario(
        actor_user_id=owner.id,
        tenant_id=tenant.id,
        reference_epoch=stamp,
        primary_object=primary,
        secondary_object=secondary,
    )
    await database.rollback()
    scenario_models = importlib.import_module("ailora.domain.ssa.scenario_models")
    audit_models = importlib.import_module("ailora.domain.ssa.audit_models")
    scenario_count = await database.scalar(
        select(func.count()).select_from(scenario_models.ScenarioRecord)
    )
    audit_count = await database.scalar(
        select(func.count()).select_from(audit_models.AuditEventRecord)
    )
    assert scenario_count == 0
    assert audit_count == 0


@pytest.mark.asyncio
async def test_cross_tenant_audit_isolation_and_idor(database: AsyncSession) -> None:
    tenant_a, user_a = await _identity(database, slug="audit-a", email="a@audit.test")
    tenant_b, user_b = await _identity(database, slug="audit-b", email="b@audit.test")
    await _workflow(database, tenant_b, user_b)
    module = importlib.import_module("ailora.domain.ssa.audit_service")
    service = module.TenantAuditService(database)
    with pytest.raises(module.AuditAccessDeniedError):
        await service.list_events(actor_user_id=user_a.id, tenant_id=tenant_b.id)
    records_b = await service.list_events(actor_user_id=user_b.id, tenant_id=tenant_b.id)
    with pytest.raises(module.AuditEventNotFoundError):
        await service.get_event(
            actor_user_id=user_a.id,
            tenant_id=tenant_a.id,
            event_id=records_b[0].id,
        )


@pytest.mark.asyncio
async def test_inactive_identity_fails_closed(database: AsyncSession) -> None:
    tenant, user = await _identity(
        database, slug="audit-inactive", email="inactive@audit.test", active=False
    )
    module = importlib.import_module("ailora.domain.ssa.audit_service")
    with pytest.raises(module.AuditAccessDeniedError):
        await module.TenantAuditService(database).list_events(
            actor_user_id=user.id, tenant_id=tenant.id
        )


def test_domain_rejects_secrets_in_every_free_text_field() -> None:
    from ailora.domain.ssa.audit import AuditEntry, AuditEventType

    values = {
        "resource_id": "token=abc",
        "outcome": "password=hunter2",
        "correlation_id": "Authorization: Bearer abc",
        "detail": "api_key=abc",
    }
    for field_name, value in values.items():
        kwargs = {
            "tenant_id": uuid.uuid4(),
            "actor_id": uuid.uuid4(),
            "event_type": AuditEventType.SCENARIO_INGESTED,
            "resource_id": str(uuid.uuid4()),
            "outcome": "SUCCESS",
            "correlation_id": str(uuid.uuid4()),
            "detail": "safe",
        }
        kwargs[field_name] = value
        with pytest.raises(ValueError):
            AuditEntry.create(**kwargs)


def test_repository_has_no_update_or_delete_surface() -> None:
    repository = importlib.import_module("ailora.domain.ssa.audit_repository").AuditEventRepository
    assert not hasattr(repository, "update")
    assert not hasattr(repository, "delete")


def test_openapi_exposes_read_only_protected_audit_routes() -> None:
    app_module = importlib.import_module("ailora.api.app")
    schema = app_module.app.openapi()
    collection = "/v1/tenants/{tenant_id}/ssa/audit-events"
    item = collection + "/{event_id}"
    assert set(schema["paths"][collection]) == {"get"}
    assert set(schema["paths"][item]) == {"get"}
    assert schema["paths"][collection]["get"]["security"]
    assert schema["paths"][item]["get"]["security"]


def test_audit_response_is_secret_safe_and_advisory() -> None:
    app_module = importlib.import_module("ailora.api.app")
    schema = app_module.app.openapi()
    fields = set(schema["components"]["schemas"]["AuditEventResponse"]["properties"])
    assert {"tenant_id", "event_type", "correlation_id", "advisory_only"}.issubset(fields)
    assert not fields.intersection(
        {"password", "hashed_password", "token", "secret", "authorization", "claims"}
    )


def test_audit_implementation_has_no_operational_capability() -> None:
    from pathlib import Path

    files = [
        Path("src/ailora/domain/ssa/audit_service.py"),
        Path("src/ailora/api/routers/ssa_audit.py"),
    ]
    text = "\n".join(path.read_text(encoding="utf-8").lower() for path in files)
    for forbidden in (
        "execute_command(",
        "send_uplink(",
        "maneuver_execute(",
        "probability_of_collision",
    ):
        assert forbidden not in text
