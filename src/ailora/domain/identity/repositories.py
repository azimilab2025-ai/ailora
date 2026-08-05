"""
AILORA tenant-scoped database access layer.

Provides a repository pattern for the Identity bounded context.
All tenant-scoped queries MUST go through these repositories to
ensure the mandatory tenant_id filter is always applied.

Security contracts (Prompt 15 §12):
- tenant_id is never taken directly from client input; it is resolved
  from a validated Membership record.
- Cross-tenant data access is forbidden at this layer (fail-closed).
- Repositories raise TenantAccessError (→ HTTP 403) when isolation fails.
- No raw SQL strings; all queries use SQLAlchemy ORM to prevent injection.
"""

from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ailora.domain.identity.models import Membership, RoleEnum, Tenant, User


class TenantAccessError(Exception):
    """Raised when a tenant isolation boundary is violated."""


# ---------------------------------------------------------------------------
# TenantRepository
# ---------------------------------------------------------------------------


class TenantRepository:
    """Data-access operations for Tenant entities."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, tenant_id: uuid.UUID) -> Tenant | None:
        result = await self._session.execute(
            select(Tenant).where(Tenant.id == tenant_id)
        )
        return result.scalar_one_or_none()

    async def get_by_slug(self, slug: str) -> Tenant | None:
        result = await self._session.execute(
            select(Tenant).where(Tenant.slug == slug)
        )
        return result.scalar_one_or_none()

    async def create(self, slug: str, display_name: str) -> Tenant:
        tenant = Tenant(id=uuid.uuid4(), slug=slug, display_name=display_name)
        self._session.add(tenant)
        await self._session.flush()
        return tenant


# ---------------------------------------------------------------------------
# UserRepository
# ---------------------------------------------------------------------------


class UserRepository:
    """Data-access operations for User entities."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, user_id: uuid.UUID) -> User | None:
        result = await self._session.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> User | None:
        result = await self._session.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def create(self, email: str, hashed_password: str) -> User:
        user = User(id=uuid.uuid4(), email=email, hashed_password=hashed_password)
        self._session.add(user)
        await self._session.flush()
        return user


# ---------------------------------------------------------------------------
# MembershipRepository
# ---------------------------------------------------------------------------


class MembershipRepository:
    """
    Data-access operations for Membership entities.

    This is the authoritative layer for tenant context resolution.
    Callers must always use resolve_tenant_membership() to obtain a
    validated membership before proceeding with tenant-scoped operations.
    """

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def resolve_tenant_membership(
        self,
        user_id: uuid.UUID,
        tenant_id: uuid.UUID,
    ) -> Membership:
        """
        Return the active membership for (user_id, tenant_id).

        Raises:
            TenantAccessError: If no active membership exists.
        """
        result = await self._session.execute(
            select(Membership).where(
                Membership.user_id == user_id,
                Membership.tenant_id == tenant_id,
                Membership.is_active.is_(True),
            )
        )
        membership = result.scalar_one_or_none()
        if membership is None:
            raise TenantAccessError(
                "No active membership for this user in the requested tenant"
            )
        return membership

    async def create(
        self,
        user_id: uuid.UUID,
        tenant_id: uuid.UUID,
        role: RoleEnum = RoleEnum.MEMBER,
    ) -> Membership:
        membership = Membership(
            id=uuid.uuid4(),
            user_id=user_id,
            tenant_id=tenant_id,
            role=role,
        )
        self._session.add(membership)
        await self._session.flush()
        return membership

    async def list_for_user(self, user_id: uuid.UUID) -> list[Membership]:
        """Return all active memberships for a user across all tenants."""
        result = await self._session.execute(
            select(Membership).where(
                Membership.user_id == user_id,
                Membership.is_active.is_(True),
            )
        )
        return list(result.scalars().all())
