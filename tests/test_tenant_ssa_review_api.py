"""Security, transition, persistence, and API contracts for tenant SSA reviews."""

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
from ailora.domain.ssa.review import ReviewState, ReviewTransitionError
from ailora.domain.ssa.scenario import (
    DataClassification,
    DataProvenance,
    OrbitalObjectDescriptor,
)


@pytest.fixture
async def database() -> AsyncIterator[AsyncSession]:
    from ailora.db.base import Base
    from ailora.domain.identity import session_models  # noqa: F401
    from ailora.domain.ssa import (  # noqa: F401
        risk_models,
        scenario_models,
        screening_models,
    )

    try:
        importlib.import_module("ailora.domain.ssa.review_models")
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
    role: RoleEnum = RoleEnum.OWNER,
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
            role=role,
            is_active=active,
        )
    )
    await database.commit()
    return tenant, user


async def _add_member(
    database: AsyncSession,
    tenant: Tenant,
    *,
    email: str,
) -> User:
    user = User(email=email, hashed_password="$2b$test", is_active=True)
    database.add(user)
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
    return user


def _scenario_inputs(
    classification: DataClassification = DataClassification.SYNTHETIC,
) -> tuple[TemporalStamp, OrbitalObjectDescriptor, OrbitalObjectDescriptor]:
    epoch = Epoch(iso_utc="2026-08-14T00:00:00Z")
    stamp = TemporalStamp(epoch=epoch, frame=ReferenceFrame.TEME)
    provenance = DataProvenance(
        source_label="verified-review-test",
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
        x_m=7_003_000.0,
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


def _review_service(database: AsyncSession) -> object:
    return importlib.import_module("ailora.domain.ssa.review_service").TenantReviewService(database)


async def _create_assessment(
    database: AsyncSession,
    tenant: Tenant,
    user: User,
    *,
    classification: DataClassification = DataClassification.SYNTHETIC,
) -> tuple[object, object, object]:
    stamp, primary_object, secondary_object = _scenario_inputs(classification)
    scenario = await _scenario_service(database).create_scenario(
        actor_user_id=user.id,
        tenant_id=tenant.id,
        reference_epoch=stamp,
        primary_object=primary_object,
        secondary_object=secondary_object,
    )
    primary_state, secondary_state = _states(stamp)
    screening = await _screening_service(database).create_screening(
        actor_user_id=user.id,
        tenant_id=tenant.id,
        scenario_id=scenario.id,
        primary_state=primary_state,
        secondary_state=secondary_state,
        threshold_km=5.0,
    )
    assessment = await _risk_service(database).create_assessment(
        actor_user_id=user.id,
        tenant_id=tenant.id,
        scenario_id=scenario.id,
        screening_id=screening.id,
    )
    await database.commit()
    return scenario, screening, assessment


async def _create_review(
    database: AsyncSession,
    tenant: Tenant,
    user: User,
    *,
    classification: DataClassification = DataClassification.SYNTHETIC,
) -> tuple[object, object, object, object]:
    scenario, screening, assessment = await _create_assessment(
        database,
        tenant,
        user,
        classification=classification,
    )
    review = await _review_service(database).create_review(
        actor_user_id=user.id,
        tenant_id=tenant.id,
        scenario_id=scenario.id,
        screening_id=screening.id,
        assessment_id=assessment.id,
    )
    await database.commit()
    return scenario, screening, assessment, review


@pytest.mark.asyncio
async def test_owner_creates_pending_advisory_review(database: AsyncSession) -> None:
    tenant, owner = await _identity(
        database,
        slug="review-create",
        email="owner@review.test",
    )
    scenario, screening, assessment, review = await _create_review(
        database,
        tenant,
        owner,
    )
    assert review.tenant_id == tenant.id
    assert review.scenario_id == scenario.id
    assert review.screening_id == screening.id
    assert review.assessment_id == assessment.id
    assert review.state == ReviewState.PENDING_REVIEW.value
    assert review.transition_count == 0
    assert review.reviewer_user_id is None
    assert review.advisory_only is True
    assert review.operational_clearance is False
    assert "advisory" in review.provenance_label.lower()


@pytest.mark.asyncio
async def test_review_inherits_restricted_classification(database: AsyncSession) -> None:
    tenant, owner = await _identity(
        database,
        slug="review-class",
        email="class@review.test",
    )
    _, _, _, review = await _create_review(
        database,
        tenant,
        owner,
        classification=DataClassification.RESTRICTED,
    )
    assert review.combined_classification == "RESTRICTED"


@pytest.mark.asyncio
async def test_member_cannot_create_or_transition_review(database: AsyncSession) -> None:
    review_module = importlib.import_module("ailora.domain.ssa.review_service")
    tenant, owner = await _identity(
        database,
        slug="review-writer",
        email="owner@writer.test",
    )
    member = await _add_member(database, tenant, email="member@writer.test")
    scenario, screening, assessment = await _create_assessment(
        database,
        tenant,
        owner,
    )
    with pytest.raises(review_module.ReviewAccessDeniedError):
        await _review_service(database).create_review(
            actor_user_id=member.id,
            tenant_id=tenant.id,
            scenario_id=scenario.id,
            screening_id=screening.id,
            assessment_id=assessment.id,
        )
    review = await _review_service(database).create_review(
        actor_user_id=owner.id,
        tenant_id=tenant.id,
        scenario_id=scenario.id,
        screening_id=screening.id,
        assessment_id=assessment.id,
    )
    with pytest.raises(review_module.ReviewAccessDeniedError):
        await _review_service(database).transition_review(
            actor_user_id=member.id,
            tenant_id=tenant.id,
            scenario_id=scenario.id,
            screening_id=screening.id,
            assessment_id=assessment.id,
            review_id=review.id,
            target_state=ReviewState.UNDER_REVIEW,
        )


@pytest.mark.asyncio
async def test_member_can_read_review(database: AsyncSession) -> None:
    tenant, owner = await _identity(
        database,
        slug="review-reader",
        email="owner@reader.test",
    )
    member = await _add_member(database, tenant, email="member@reader.test")
    scenario, screening, assessment, review = await _create_review(
        database,
        tenant,
        owner,
    )
    record = await _review_service(database).get_review(
        actor_user_id=member.id,
        tenant_id=tenant.id,
        scenario_id=scenario.id,
        screening_id=screening.id,
        assessment_id=assessment.id,
        review_id=review.id,
    )
    assert record.id == review.id


@pytest.mark.asyncio
async def test_cross_tenant_review_creation_is_denied(database: AsyncSession) -> None:
    review_module = importlib.import_module("ailora.domain.ssa.review_service")
    _, owner_a = await _identity(database, slug="review-a", email="a@review.test")
    tenant_b, owner_b = await _identity(
        database,
        slug="review-b",
        email="b@review.test",
    )
    scenario_b, screening_b, assessment_b = await _create_assessment(
        database,
        tenant_b,
        owner_b,
    )
    with pytest.raises(review_module.ReviewAccessDeniedError):
        await _review_service(database).create_review(
            actor_user_id=owner_a.id,
            tenant_id=tenant_b.id,
            scenario_id=scenario_b.id,
            screening_id=screening_b.id,
            assessment_id=assessment_b.id,
        )


@pytest.mark.asyncio
async def test_scenario_idor_is_not_found_inside_verified_tenant(
    database: AsyncSession,
) -> None:
    scenario_module = importlib.import_module("ailora.domain.ssa.scenario_service")
    tenant_a, owner_a = await _identity(
        database,
        slug="review-sid-a",
        email="a@review-sid.test",
    )
    tenant_b, owner_b = await _identity(
        database,
        slug="review-sid-b",
        email="b@review-sid.test",
    )
    scenario_b, screening_b, assessment_b = await _create_assessment(
        database,
        tenant_b,
        owner_b,
    )
    with pytest.raises(scenario_module.ScenarioNotFoundError):
        await _review_service(database).create_review(
            actor_user_id=owner_a.id,
            tenant_id=tenant_a.id,
            scenario_id=scenario_b.id,
            screening_id=screening_b.id,
            assessment_id=assessment_b.id,
        )


@pytest.mark.asyncio
async def test_screening_idor_is_not_found_inside_verified_scenario(
    database: AsyncSession,
) -> None:
    screening_module = importlib.import_module("ailora.domain.ssa.screening_service")
    tenant, owner = await _identity(
        database,
        slug="review-screen-idor",
        email="screen@review.test",
    )
    scenario_one, _, _ = await _create_assessment(database, tenant, owner)
    _, screening_two, assessment_two = await _create_assessment(database, tenant, owner)
    with pytest.raises(screening_module.ScreeningNotFoundError):
        await _review_service(database).create_review(
            actor_user_id=owner.id,
            tenant_id=tenant.id,
            scenario_id=scenario_one.id,
            screening_id=screening_two.id,
            assessment_id=assessment_two.id,
        )


@pytest.mark.asyncio
async def test_assessment_idor_is_not_found_inside_verified_screening(
    database: AsyncSession,
) -> None:
    risk_module = importlib.import_module("ailora.domain.ssa.risk_service")
    tenant, owner = await _identity(
        database,
        slug="review-risk-idor",
        email="risk@review.test",
    )
    scenario_one, screening_one, _ = await _create_assessment(database, tenant, owner)
    _, _, assessment_two = await _create_assessment(database, tenant, owner)
    with pytest.raises(risk_module.RiskAssessmentNotFoundError):
        await _review_service(database).create_review(
            actor_user_id=owner.id,
            tenant_id=tenant.id,
            scenario_id=scenario_one.id,
            screening_id=screening_one.id,
            assessment_id=assessment_two.id,
        )


@pytest.mark.asyncio
async def test_review_list_is_fully_scope_filtered(database: AsyncSession) -> None:
    tenant, owner = await _identity(
        database,
        slug="review-list",
        email="list@review.test",
    )
    first = await _create_review(database, tenant, owner)
    await _create_review(database, tenant, owner)
    scenario, screening, assessment, review = first
    records = await _review_service(database).list_reviews(
        actor_user_id=owner.id,
        tenant_id=tenant.id,
        scenario_id=scenario.id,
        screening_id=screening.id,
        assessment_id=assessment.id,
    )
    assert [record.id for record in records] == [review.id]


@pytest.mark.asyncio
async def test_review_idor_is_not_found_inside_verified_assessment(
    database: AsyncSession,
) -> None:
    review_module = importlib.import_module("ailora.domain.ssa.review_service")
    tenant, owner = await _identity(
        database,
        slug="review-idor",
        email="idor@review.test",
    )
    scenario_one, screening_one, assessment_one, _ = await _create_review(
        database,
        tenant,
        owner,
    )
    _, _, _, review_two = await _create_review(database, tenant, owner)
    with pytest.raises(review_module.ReviewNotFoundError):
        await _review_service(database).get_review(
            actor_user_id=owner.id,
            tenant_id=tenant.id,
            scenario_id=scenario_one.id,
            screening_id=screening_one.id,
            assessment_id=assessment_one.id,
            review_id=review_two.id,
        )


@pytest.mark.asyncio
async def test_duplicate_review_is_rejected(database: AsyncSession) -> None:
    review_module = importlib.import_module("ailora.domain.ssa.review_service")
    tenant, owner = await _identity(
        database,
        slug="review-duplicate",
        email="duplicate@review.test",
    )
    scenario, screening, assessment, _ = await _create_review(
        database,
        tenant,
        owner,
    )
    with pytest.raises(review_module.ReviewAlreadyExistsError):
        await _review_service(database).create_review(
            actor_user_id=owner.id,
            tenant_id=tenant.id,
            scenario_id=scenario.id,
            screening_id=screening.id,
            assessment_id=assessment.id,
        )


@pytest.mark.asyncio
async def test_valid_transitions_persist_ordered_history(database: AsyncSession) -> None:
    repository_module = importlib.import_module("ailora.domain.ssa.review_repository")
    tenant, owner = await _identity(
        database,
        slug="review-transition",
        email="transition@review.test",
    )
    scenario, screening, assessment, review = await _create_review(
        database,
        tenant,
        owner,
    )
    service = _review_service(database)
    for state, notes in (
        (ReviewState.UNDER_REVIEW, "Review opened"),
        (ReviewState.REVIEWED, "Advisory output reviewed"),
        (ReviewState.CLOSED, "Review cycle closed"),
    ):
        review = await service.transition_review(
            actor_user_id=owner.id,
            tenant_id=tenant.id,
            scenario_id=scenario.id,
            screening_id=screening.id,
            assessment_id=assessment.id,
            review_id=review.id,
            target_state=state,
            notes=notes,
        )
    await database.commit()
    history = await repository_module.ReviewRepository(database).list_transitions(review.id)
    assert review.state == ReviewState.CLOSED.value
    assert review.transition_count == 3
    assert review.reviewer_user_id == owner.id
    assert [item.sequence_number for item in history] == [1, 2, 3]
    assert [item.to_state for item in history] == [
        ReviewState.UNDER_REVIEW.value,
        ReviewState.REVIEWED.value,
        ReviewState.CLOSED.value,
    ]


@pytest.mark.asyncio
async def test_invalid_transition_is_rejected_without_history(
    database: AsyncSession,
) -> None:
    repository_module = importlib.import_module("ailora.domain.ssa.review_repository")
    tenant, owner = await _identity(
        database,
        slug="review-invalid",
        email="invalid@review.test",
    )
    scenario, screening, assessment, review = await _create_review(
        database,
        tenant,
        owner,
    )
    with pytest.raises(ReviewTransitionError):
        await _review_service(database).transition_review(
            actor_user_id=owner.id,
            tenant_id=tenant.id,
            scenario_id=scenario.id,
            screening_id=screening.id,
            assessment_id=assessment.id,
            review_id=review.id,
            target_state=ReviewState.REVIEWED,
        )
    history = await repository_module.ReviewRepository(database).list_transitions(review.id)
    assert history == []
    assert review.state == ReviewState.PENDING_REVIEW.value
    assert review.transition_count == 0


@pytest.mark.asyncio
async def test_closed_review_cannot_reopen(database: AsyncSession) -> None:
    tenant, owner = await _identity(
        database,
        slug="review-closed",
        email="closed@review.test",
    )
    scenario, screening, assessment, review = await _create_review(
        database,
        tenant,
        owner,
    )
    service = _review_service(database)
    for state in (
        ReviewState.UNDER_REVIEW,
        ReviewState.REVIEWED,
        ReviewState.CLOSED,
    ):
        review = await service.transition_review(
            actor_user_id=owner.id,
            tenant_id=tenant.id,
            scenario_id=scenario.id,
            screening_id=screening.id,
            assessment_id=assessment.id,
            review_id=review.id,
            target_state=state,
        )
    with pytest.raises(ReviewTransitionError):
        await service.transition_review(
            actor_user_id=owner.id,
            tenant_id=tenant.id,
            scenario_id=scenario.id,
            screening_id=screening.id,
            assessment_id=assessment.id,
            review_id=review.id,
            target_state=ReviewState.UNDER_REVIEW,
        )


@pytest.mark.asyncio
async def test_inactive_identity_fails_closed(database: AsyncSession) -> None:
    scenario_module = importlib.import_module("ailora.domain.ssa.scenario_service")
    tenant, owner = await _identity(
        database,
        slug="review-inactive",
        email="inactive@review.test",
        active=False,
    )
    with pytest.raises(scenario_module.ScenarioAccessDeniedError):
        await _review_service(database).list_reviews(
            actor_user_id=owner.id,
            tenant_id=tenant.id,
            scenario_id=uuid.uuid4(),
            screening_id=uuid.uuid4(),
            assessment_id=uuid.uuid4(),
        )


def test_openapi_exposes_protected_review_routes() -> None:
    app_module = importlib.import_module("ailora.api.app")
    schema = app_module.app.openapi()
    collection = (
        "/v1/tenants/{tenant_id}/ssa/scenarios/{scenario_id}"
        "/screenings/{screening_id}/risk-assessments/{assessment_id}/reviews"
    )
    item = collection + "/{review_id}"
    assert {"get", "post"}.issubset(schema["paths"][collection])
    assert {"get", "patch"}.issubset(schema["paths"][item])
    for path, methods in (
        (collection, ("get", "post")),
        (item, ("get", "patch")),
    ):
        for method in methods:
            assert schema["paths"][path][method].get("security")


def test_request_bodies_cannot_select_scope_authority_or_safety_output() -> None:
    app_module = importlib.import_module("ailora.api.app")
    schema = app_module.app.openapi()
    collection = (
        "/v1/tenants/{tenant_id}/ssa/scenarios/{scenario_id}"
        "/screenings/{screening_id}/risk-assessments/{assessment_id}/reviews"
    )
    item = collection + "/{review_id}"
    assert "requestBody" not in schema["paths"][collection]["post"]
    body_schema = schema["paths"][item]["patch"]["requestBody"]["content"]["application/json"][
        "schema"
    ]
    reference = body_schema["$ref"].rsplit("/", 1)[-1]
    fields = set(schema["components"]["schemas"][reference]["properties"])
    assert fields == {"target_state", "notes"}
    assert not fields.intersection(
        {
            "tenant_id",
            "scenario_id",
            "screening_id",
            "assessment_id",
            "review_id",
            "reviewer_user_id",
            "advisory_only",
            "command_path",
        }
    )


def test_response_contract_is_advisory_and_secret_safe() -> None:
    app_module = importlib.import_module("ailora.api.app")
    schema = app_module.app.openapi()
    fields = set(schema["components"]["schemas"]["ReviewResponse"]["properties"])
    required = {
        "state",
        "reviewer_user_id",
        "notes",
        "transition_count",
        "combined_classification",
        "provenance_label",
        "advisory_only",
        "operational_clearance",
    }
    assert required.issubset(fields)
    assert not fields.intersection(
        {
            "password",
            "hashed_password",
            "token",
            "secret",
            "probability_of_collision",
            "collision_probability",
            "pc",
            "command_path",
        }
    )


def test_review_api_has_no_spacecraft_command_capability() -> None:
    from pathlib import Path

    files = [
        Path("src/ailora/domain/ssa/review_service.py"),
        Path("src/ailora/api/routers/ssa_reviews.py"),
    ]
    forbidden = ["execute_command(", "send_uplink(", "maneuver_execute("]
    text = "\n".join(path.read_text(encoding="utf-8").lower() for path in files)
    for pattern in forbidden:
        assert pattern not in text
