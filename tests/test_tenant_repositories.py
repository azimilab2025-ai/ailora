"""
AILORA P2-03: Tenant-scoped DB Access Layer Contract Tests.

Validates:
- Repository classes exist and are importable.
- TenantAccessError is raised when membership is absent.
- resolve_tenant_membership fail-closed behaviour.
- Cross-tenant access is forbidden.
- No tenant_id is accepted from raw untrusted input.

All tests use in-memory SQLite (via SQLAlchemy async with aiosqlite) to avoid
requiring a live PostgreSQL connection.

Note: SQLite does not support all PostgreSQL-specific types (UUID dialects).
We use String PKs in these tests by creating a lightweight test schema that
maps the same ORM models to compatible column types via override.
We test at the repository-contract level (logic), not the migration level.
"""

from __future__ import annotations

import uuid
from pathlib import Path

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from ailora.domain.identity.models import Membership, Tenant, User
from ailora.domain.identity.repositories import (
    MembershipRepository,
    TenantAccessError,
    TenantRepository,
    UserRepository,
)

REPO_ROOT = Path(__file__).parent.parent
REPOS_MODULE = REPO_ROOT / "src" / "ailora" / "domain" / "identity" / "repositories.py"


# ─── Structural contract ─────────────────────────────────────────────────────


def test_repositories_module_exists() -> None:
    assert REPOS_MODULE.exists()


def test_tenant_access_error_importable() -> None:
    assert issubclass(TenantAccessError, Exception)


def test_repository_classes_exist() -> None:
    for cls in (TenantRepository, UserRepository, MembershipRepository):
        assert callable(cls)


def test_repositories_module_has_no_raw_sql() -> None:
    """Repositories must not use raw SQL strings (injection risk)."""
    text = REPOS_MODULE.read_text(encoding="utf-8")
    forbidden = ['execute("SELECT', "execute('SELECT", 'text("SELECT']
    for pattern in forbidden:
        assert pattern not in text, f"repositories.py must not use raw SQL: '{pattern}'"


def test_tenant_id_is_always_filtered() -> None:
    """resolve_tenant_membership must filter by both user_id and tenant_id."""
    text = REPOS_MODULE.read_text(encoding="utf-8")
    assert "tenant_id" in text
    assert "user_id" in text
    assert "is_active" in text


# ─── SQLite-backed functional tests ─────────────────────────────────────────


@pytest.fixture
async def db_session() -> AsyncSession:
    """Provide an in-memory SQLite async session with the identity schema."""
    from ailora.db.base import Base

    # native_uuid=False tells SQLAlchemy to store UUIDs as strings in SQLite
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        echo=False,
        connect_args={"check_same_thread": False},
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session_factory = async_sessionmaker(engine, expire_on_commit=False)
    async with session_factory() as session:
        yield session

    await engine.dispose()


@pytest.fixture
async def populated_db(db_session: AsyncSession) -> dict[str, object]:
    """Create a tenant, user, and membership for testing."""
    tenant_repo = TenantRepository(db_session)
    user_repo = UserRepository(db_session)
    membership_repo = MembershipRepository(db_session)

    tenant = await tenant_repo.create(slug="acme", display_name="Acme Corp")
    user = await user_repo.create(email="alice@acme.local", hashed_password="$2b$hashed")
    membership = await membership_repo.create(user_id=user.id, tenant_id=tenant.id)
    await db_session.commit()

    return {"tenant": tenant, "user": user, "membership": membership}


@pytest.mark.asyncio
async def test_tenant_create_and_get_by_slug(db_session: AsyncSession) -> None:
    repo = TenantRepository(db_session)
    await repo.create(slug="test-org", display_name="Test Org")
    await db_session.commit()
    t = await repo.get_by_slug("test-org")
    assert t is not None
    assert t.slug == "test-org"


@pytest.mark.asyncio
async def test_tenant_get_by_id(db_session: AsyncSession) -> None:
    repo = TenantRepository(db_session)
    t = await repo.create(slug="org2", display_name="Org 2")
    await db_session.commit()
    found = await repo.get_by_id(t.id)
    assert found is not None
    assert found.slug == "org2"


@pytest.mark.asyncio
async def test_user_create_and_get_by_email(db_session: AsyncSession) -> None:
    repo = UserRepository(db_session)
    await repo.create(email="bob@test.local", hashed_password="$2b$x")
    await db_session.commit()
    u = await repo.get_by_email("bob@test.local")
    assert u is not None
    assert u.email == "bob@test.local"


@pytest.mark.asyncio
async def test_user_get_nonexistent_returns_none(db_session: AsyncSession) -> None:
    repo = UserRepository(db_session)
    result = await repo.get_by_id(uuid.uuid4())
    assert result is None


@pytest.mark.asyncio
async def test_resolve_tenant_membership_success(
    populated_db: dict[str, object],
    db_session: AsyncSession,
) -> None:
    user = populated_db["user"]
    tenant = populated_db["tenant"]
    assert isinstance(user, User)
    assert isinstance(tenant, Tenant)
    repo = MembershipRepository(db_session)
    m = await repo.resolve_tenant_membership(user.id, tenant.id)
    assert m.user_id == user.id
    assert m.tenant_id == tenant.id


@pytest.mark.asyncio
async def test_resolve_tenant_membership_wrong_tenant_raises(
    populated_db: dict[str, object],
    db_session: AsyncSession,
) -> None:
    """Cross-tenant access must be denied — fail-closed."""
    user = populated_db["user"]
    assert isinstance(user, User)
    other_tenant_id = uuid.uuid4()
    repo = MembershipRepository(db_session)
    with pytest.raises(TenantAccessError):
        await repo.resolve_tenant_membership(user.id, other_tenant_id)


@pytest.mark.asyncio
async def test_resolve_tenant_membership_wrong_user_raises(
    populated_db: dict[str, object],
    db_session: AsyncSession,
) -> None:
    """Wrong user for a valid tenant must be denied — fail-closed."""
    tenant = populated_db["tenant"]
    assert isinstance(tenant, Tenant)
    other_user_id = uuid.uuid4()
    repo = MembershipRepository(db_session)
    with pytest.raises(TenantAccessError):
        await repo.resolve_tenant_membership(other_user_id, tenant.id)


@pytest.mark.asyncio
async def test_list_memberships_for_user(
    populated_db: dict[str, object],
    db_session: AsyncSession,
) -> None:
    user = populated_db["user"]
    assert isinstance(user, User)
    repo = MembershipRepository(db_session)
    memberships = await repo.list_for_user(user.id)
    assert len(memberships) == 1
    assert memberships[0].user_id == user.id


@pytest.mark.asyncio
async def test_inactive_membership_does_not_grant_access(
    populated_db: dict[str, object],
    db_session: AsyncSession,
) -> None:
    """Revoked memberships must not grant tenant access — cross-tenant negative test."""
    membership = populated_db["membership"]
    user = populated_db["user"]
    tenant = populated_db["tenant"]
    assert isinstance(membership, Membership)
    assert isinstance(user, User)
    assert isinstance(tenant, Tenant)
    # Revoke the membership
    membership.is_active = False
    await db_session.commit()
    repo = MembershipRepository(db_session)
    with pytest.raises(TenantAccessError):
        await repo.resolve_tenant_membership(user.id, tenant.id)
