"""Security and contract tests for tenant identity management."""

from __future__ import annotations

import importlib
from collections.abc import AsyncIterator
from uuid import UUID

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from ailora.domain.identity.models import Membership, RoleEnum, Tenant, User


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


async def _identity(
    database: AsyncSession,
    *,
    tenant_slug: str,
    email: str,
    role: RoleEnum,
    user_active: bool = True,
    tenant_active: bool = True,
    membership_active: bool = True,
) -> tuple[Tenant, User, Membership]:
    tenant = Tenant(
        slug=tenant_slug,
        display_name=tenant_slug.title(),
        is_active=tenant_active,
    )
    user = User(
        email=email,
        hashed_password="$2b$test-placeholder",
        is_active=user_active,
    )
    database.add_all([tenant, user])
    await database.flush()
    membership = Membership(
        user_id=user.id,
        tenant_id=tenant.id,
        role=role,
        is_active=membership_active,
    )
    database.add(membership)
    await database.commit()
    return tenant, user, membership


def _service(database: AsyncSession) -> object:
    module = importlib.import_module("ailora.domain.identity.management")
    return module.TenantIdentityManagementService(database)


@pytest.mark.asyncio
async def test_owner_lists_only_requested_tenant(database: AsyncSession) -> None:
    tenant_a, owner, _ = await _identity(
        database,
        tenant_slug="alpha",
        email="owner@alpha.test",
        role=RoleEnum.OWNER,
    )
    await _identity(
        database,
        tenant_slug="bravo",
        email="owner@bravo.test",
        role=RoleEnum.OWNER,
    )

    memberships = await _service(database).list_memberships(
        actor_user_id=owner.id,
        tenant_id=tenant_a.id,
    )

    assert memberships
    assert all(item.tenant_id == tenant_a.id for item in memberships)


@pytest.mark.asyncio
async def test_member_is_denied_management(database: AsyncSession) -> None:
    module = importlib.import_module("ailora.domain.identity.management")
    tenant, member, _ = await _identity(
        database,
        tenant_slug="member-tenant",
        email="member@example.test",
        role=RoleEnum.MEMBER,
    )

    with pytest.raises(module.TenantManagementForbiddenError):
        await _service(database).list_memberships(
            actor_user_id=member.id,
            tenant_id=tenant.id,
        )


@pytest.mark.asyncio
async def test_cross_tenant_actor_is_denied(database: AsyncSession) -> None:
    module = importlib.import_module("ailora.domain.identity.management")
    _, owner, _ = await _identity(
        database,
        tenant_slug="source",
        email="owner@source.test",
        role=RoleEnum.OWNER,
    )
    target_tenant, _, _ = await _identity(
        database,
        tenant_slug="target",
        email="owner@target.test",
        role=RoleEnum.OWNER,
    )

    with pytest.raises(module.TenantManagementForbiddenError):
        await _service(database).list_memberships(
            actor_user_id=owner.id,
            tenant_id=target_tenant.id,
        )


@pytest.mark.asyncio
async def test_inactive_identity_states_fail_closed(database: AsyncSession) -> None:
    module = importlib.import_module("ailora.domain.identity.management")
    tenant, user, _ = await _identity(
        database,
        tenant_slug="inactive-user",
        email="inactive@example.test",
        role=RoleEnum.OWNER,
        user_active=False,
    )
    with pytest.raises(module.TenantManagementForbiddenError):
        await _service(database).list_memberships(
            actor_user_id=user.id,
            tenant_id=tenant.id,
        )


@pytest.mark.asyncio
async def test_owner_creates_tenant_bound_membership(database: AsyncSession) -> None:
    tenant, owner, _ = await _identity(
        database,
        tenant_slug="create",
        email="owner@create.test",
        role=RoleEnum.OWNER,
    )
    target = User(
        email="target@create.test",
        hashed_password="$2b$test-placeholder",
        is_active=True,
    )
    database.add(target)
    await database.commit()

    created = await _service(database).create_membership(
        actor_user_id=owner.id,
        tenant_id=tenant.id,
        target_user_id=target.id,
        role=RoleEnum.MEMBER,
    )

    assert created.tenant_id == tenant.id
    assert created.user_id == target.id
    assert created.role is RoleEnum.MEMBER


@pytest.mark.asyncio
async def test_duplicate_membership_is_rejected(database: AsyncSession) -> None:
    module = importlib.import_module("ailora.domain.identity.management")
    tenant, owner, _ = await _identity(
        database,
        tenant_slug="duplicate",
        email="owner@duplicate.test",
        role=RoleEnum.OWNER,
    )

    with pytest.raises(module.TenantManagementConflictError, match="already exists"):
        await _service(database).create_membership(
            actor_user_id=owner.id,
            tenant_id=tenant.id,
            target_user_id=owner.id,
            role=RoleEnum.MEMBER,
        )


@pytest.mark.asyncio
async def test_membership_idor_is_not_found_inside_verified_tenant(
    database: AsyncSession,
) -> None:
    module = importlib.import_module("ailora.domain.identity.management")
    tenant_a, owner_a, _ = await _identity(
        database,
        tenant_slug="idor-a",
        email="owner@idor-a.test",
        role=RoleEnum.OWNER,
    )
    _, _, membership_b = await _identity(
        database,
        tenant_slug="idor-b",
        email="owner@idor-b.test",
        role=RoleEnum.OWNER,
    )

    with pytest.raises(module.TenantManagementNotFoundError):
        await _service(database).update_membership(
            actor_user_id=owner_a.id,
            tenant_id=tenant_a.id,
            membership_id=membership_b.id,
            role=RoleEnum.MEMBER,
            is_active=True,
        )


@pytest.mark.asyncio
async def test_self_membership_change_is_rejected(database: AsyncSession) -> None:
    module = importlib.import_module("ailora.domain.identity.management")
    tenant, owner, owner_membership = await _identity(
        database,
        tenant_slug="self-change",
        email="owner@self-change.test",
        role=RoleEnum.OWNER,
    )

    with pytest.raises(module.TenantManagementConflictError, match="self"):
        await _service(database).revoke_membership(
            actor_user_id=owner.id,
            tenant_id=tenant.id,
            membership_id=owner_membership.id,
        )


@pytest.mark.asyncio
async def test_admin_cannot_assign_owner_role(database: AsyncSession) -> None:
    module = importlib.import_module("ailora.domain.identity.management")
    tenant, admin, _ = await _identity(
        database,
        tenant_slug="admin-boundary",
        email="admin@example.test",
        role=RoleEnum.ADMIN,
    )
    target = User(
        email="target@admin-boundary.test",
        hashed_password="$2b$test-placeholder",
        is_active=True,
    )
    database.add(target)
    await database.commit()

    with pytest.raises(module.TenantManagementForbiddenError, match="owner"):
        await _service(database).create_membership(
            actor_user_id=admin.id,
            tenant_id=tenant.id,
            target_user_id=target.id,
            role=RoleEnum.OWNER,
        )


def test_openapi_exposes_protected_management_routes() -> None:
    app_module = importlib.import_module("ailora.api.app")
    schema = app_module.app.openapi()
    collection = "/v1/tenants/{tenant_id}/memberships"
    item = "/v1/tenants/{tenant_id}/memberships/{membership_id}"

    assert {"get", "post"}.issubset(schema["paths"][collection])
    assert {"patch", "delete"}.issubset(schema["paths"][item])
    for path, methods in ((collection, ("get", "post")), (item, ("patch", "delete"))):
        for method in methods:
            assert schema["paths"][path][method].get("security")


def test_management_response_has_no_secret_or_password_fields() -> None:
    app_module = importlib.import_module("ailora.api.app")
    schema = app_module.app.openapi()
    response = schema["components"]["schemas"]["MembershipResponse"]
    fields = set(response["properties"])

    assert fields == {"id", "user_id", "tenant_id", "role", "is_active"}
    assert not fields.intersection({"password", "hashed_password", "token", "secret"})


def test_tenant_id_is_not_accepted_in_request_bodies() -> None:
    router_module = importlib.import_module("ailora.api.routers.tenant_identity")

    create_fields = set(router_module.MembershipCreateRequest.model_fields)
    update_fields = set(router_module.MembershipUpdateRequest.model_fields)
    assert "tenant_id" not in create_fields
    assert "tenant_id" not in update_fields
    assert create_fields == {"user_id", "role"}
    assert update_fields == {"role", "is_active"}


def test_malformed_actor_subject_is_rejected() -> None:
    router_module = importlib.import_module("ailora.api.routers.tenant_identity")
    from fastapi import HTTPException

    with pytest.raises(HTTPException) as captured:
        router_module._authenticated_user_id({"sub": "not-a-uuid"})
    assert captured.value.status_code == 401


def test_role_enum_rejects_unknown_role() -> None:
    with pytest.raises(ValueError):
        RoleEnum("super-admin")


def test_membership_response_uuid_contract() -> None:
    router_module = importlib.import_module("ailora.api.routers.tenant_identity")
    fields = router_module.MembershipResponse.model_fields
    assert fields["id"].annotation is UUID
    assert fields["tenant_id"].annotation is UUID
    assert fields["user_id"].annotation is UUID
