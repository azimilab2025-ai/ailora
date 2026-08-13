"""Fail-closed tenant identity management domain service.

Every lookup combines the requested tenant with the authenticated actor or
target membership. This makes tenant isolation a query invariant rather than
an API convention and prevents identifier-based cross-tenant disclosure.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from ailora.domain.identity.models import Membership, RoleEnum, Tenant, User


class TenantIdentityManagementError(Exception):
    """Base error for safe HTTP translation without leaking tenant state."""


class TenantManagementForbiddenError(TenantIdentityManagementError):
    """The authenticated actor is not allowed to manage this tenant."""


class TenantManagementConflictError(TenantIdentityManagementError):
    """The requested change violates an identity lifecycle invariant."""


class TenantManagementNotFoundError(TenantIdentityManagementError):
    """The target is absent from the verified tenant boundary."""


@dataclass(frozen=True, slots=True)
class VerifiedTenantManager:
    user: User
    tenant: Tenant
    membership: Membership


def _role_value(role: RoleEnum | str) -> str:
    return role.value if isinstance(role, RoleEnum) else str(role)


def _is_owner(role: RoleEnum | str) -> bool:
    return _role_value(role) == "owner"


def _is_manager(role: RoleEnum | str) -> bool:
    return _role_value(role) in {"owner", "admin"}


class TenantIdentityManagementService:
    """Tenant-scoped membership administration with deny-by-default policy."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def require_manager(
        self,
        *,
        actor_user_id: uuid.UUID,
        tenant_id: uuid.UUID,
    ) -> VerifiedTenantManager:
        statement = (
            select(User, Tenant, Membership)
            .join(Membership, Membership.user_id == User.id)
            .join(Tenant, Tenant.id == Membership.tenant_id)
            .where(
                User.id == actor_user_id,
                Tenant.id == tenant_id,
                Membership.user_id == actor_user_id,
                Membership.tenant_id == tenant_id,
            )
        )
        row = (await self._session.execute(statement)).one_or_none()
        if row is None:
            raise TenantManagementForbiddenError("tenant management denied")

        user, tenant, membership = row
        if not user.is_active or not tenant.is_active or not membership.is_active:
            raise TenantManagementForbiddenError("tenant management denied")
        if not _is_manager(membership.role):
            raise TenantManagementForbiddenError("tenant management denied")

        return VerifiedTenantManager(
            user=user,
            tenant=tenant,
            membership=membership,
        )

    async def list_memberships(
        self,
        *,
        actor_user_id: uuid.UUID,
        tenant_id: uuid.UUID,
    ) -> list[Membership]:
        await self.require_manager(actor_user_id=actor_user_id, tenant_id=tenant_id)
        statement = (
            select(Membership)
            .where(Membership.tenant_id == tenant_id)
            .order_by(Membership.created_at, Membership.id)
        )
        return list((await self._session.scalars(statement)).all())

    async def create_membership(
        self,
        *,
        actor_user_id: uuid.UUID,
        tenant_id: uuid.UUID,
        target_user_id: uuid.UUID,
        role: RoleEnum,
    ) -> Membership:
        manager = await self.require_manager(
            actor_user_id=actor_user_id,
            tenant_id=tenant_id,
        )
        self._require_role_assignment_allowed(manager.membership.role, role)

        user = await self._session.get(User, target_user_id)
        if user is None or not user.is_active:
            raise TenantManagementNotFoundError("eligible user not found")

        existing = await self._session.scalar(
            select(Membership).where(
                Membership.user_id == target_user_id,
                Membership.tenant_id == tenant_id,
            )
        )
        if existing is not None:
            raise TenantManagementConflictError("membership already exists")

        membership = Membership(
            user_id=target_user_id,
            tenant_id=tenant_id,
            role=role,
            is_active=True,
        )
        self._session.add(membership)
        await self._session.flush()
        return membership

    async def update_membership(
        self,
        *,
        actor_user_id: uuid.UUID,
        tenant_id: uuid.UUID,
        membership_id: uuid.UUID,
        role: RoleEnum,
        is_active: bool,
    ) -> Membership:
        manager = await self.require_manager(
            actor_user_id=actor_user_id,
            tenant_id=tenant_id,
        )
        target = await self._target_membership(
            tenant_id=tenant_id,
            membership_id=membership_id,
        )
        self._require_not_self(actor_user_id=actor_user_id, target=target)
        self._require_target_manageable(manager.membership.role, target.role)
        self._require_role_assignment_allowed(manager.membership.role, role)

        if _is_owner(target.role) and (not _is_owner(role) or not is_active):
            await self._require_another_active_owner(
                tenant_id=tenant_id,
                excluded_membership_id=target.id,
            )

        target.role = role
        target.is_active = is_active
        await self._session.flush()
        return target

    async def revoke_membership(
        self,
        *,
        actor_user_id: uuid.UUID,
        tenant_id: uuid.UUID,
        membership_id: uuid.UUID,
    ) -> None:
        manager = await self.require_manager(
            actor_user_id=actor_user_id,
            tenant_id=tenant_id,
        )
        target = await self._target_membership(
            tenant_id=tenant_id,
            membership_id=membership_id,
        )
        self._require_not_self(actor_user_id=actor_user_id, target=target)
        self._require_target_manageable(manager.membership.role, target.role)

        if _is_owner(target.role) and target.is_active:
            await self._require_another_active_owner(
                tenant_id=tenant_id,
                excluded_membership_id=target.id,
            )

        target.is_active = False
        await self._session.flush()

    async def _target_membership(
        self,
        *,
        tenant_id: uuid.UUID,
        membership_id: uuid.UUID,
    ) -> Membership:
        target = await self._session.scalar(
            select(Membership).where(
                Membership.id == membership_id,
                Membership.tenant_id == tenant_id,
            )
        )
        if target is None:
            raise TenantManagementNotFoundError("membership not found")
        return target

    async def _require_another_active_owner(
        self,
        *,
        tenant_id: uuid.UUID,
        excluded_membership_id: uuid.UUID,
    ) -> None:
        owner_count = await self._session.scalar(
            select(func.count(Membership.id)).where(
                Membership.tenant_id == tenant_id,
                Membership.id != excluded_membership_id,
                Membership.role == RoleEnum.OWNER,
                Membership.is_active.is_(True),
            )
        )
        if not owner_count:
            raise TenantManagementConflictError("tenant must retain an active owner")

    @staticmethod
    def _require_not_self(
        *,
        actor_user_id: uuid.UUID,
        target: Membership,
    ) -> None:
        if target.user_id == actor_user_id:
            raise TenantManagementConflictError("self membership changes are not allowed")

    @staticmethod
    def _require_target_manageable(
        manager_role: RoleEnum | str,
        target_role: RoleEnum | str,
    ) -> None:
        if not _is_owner(manager_role) and _is_owner(target_role):
            raise TenantManagementForbiddenError("owner membership management denied")

    @staticmethod
    def _require_role_assignment_allowed(
        manager_role: RoleEnum | str,
        requested_role: RoleEnum | str,
    ) -> None:
        if not _is_owner(manager_role) and _is_owner(requested_role):
            raise TenantManagementForbiddenError("owner role assignment denied")
