"""Fail-closed authorization policy and tenant-isolation contracts."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from uuid import UUID


class Permission(StrEnum):
    """Permissions evaluated by the bounded authorization policy."""

    TENANT_READ = "tenant:read"
    TENANT_WRITE = "tenant:write"
    MEMBERSHIP_MANAGE = "membership:manage"


class AuthorizationDeniedError(Exception):
    """Raised when authentication is valid but authorization is denied."""


_ROLE_PERMISSIONS: dict[str, frozenset[Permission]] = {
    "viewer": frozenset({Permission.TENANT_READ}),
    "analyst": frozenset({Permission.TENANT_READ, Permission.TENANT_WRITE}),
    "reviewer": frozenset({Permission.TENANT_READ, Permission.TENANT_WRITE}),
    "admin": frozenset(Permission),
    "tenant_admin": frozenset(Permission),
}


@dataclass(frozen=True, slots=True)
class TenantAuthorizationContext:
    """Verified tenant context derived from trusted identity and membership state."""

    user_id: UUID
    tenant_id: UUID
    role: str
    permissions: frozenset[Permission]


def _normalized_role(role: object) -> str:
    value = getattr(role, "value", role)
    if not isinstance(value, str):
        raise AuthorizationDeniedError("membership role is invalid")
    return value.strip().casefold()


def require_claim_subject(*, authenticated_user_id: UUID, token_subject: str) -> None:
    """Reject a missing, malformed, or forged token subject claim."""
    try:
        claimed_user_id = UUID(token_subject)
    except (TypeError, ValueError) as exc:
        raise AuthorizationDeniedError("token subject is invalid") from exc

    if claimed_user_id != authenticated_user_id:
        raise AuthorizationDeniedError("token subject does not match authenticated user")


def authorize_tenant_membership(
    *,
    authenticated_user_id: UUID,
    requested_tenant_id: UUID,
    membership_user_id: UUID,
    membership_tenant_id: UUID,
    membership_role: object,
    user_active: bool,
    tenant_active: bool,
    membership_active: bool,
    required_permission: Permission = Permission.TENANT_READ,
) -> TenantAuthorizationContext:
    """Build a tenant context only after every fail-closed check succeeds."""
    if not user_active:
        raise AuthorizationDeniedError("inactive user")
    if not tenant_active:
        raise AuthorizationDeniedError("inactive tenant")
    if not membership_active:
        raise AuthorizationDeniedError("revoked membership")
    if membership_user_id != authenticated_user_id:
        raise AuthorizationDeniedError("membership user mismatch")
    if membership_tenant_id != requested_tenant_id:
        raise AuthorizationDeniedError("cross-tenant access denied")

    role = _normalized_role(membership_role)
    permissions = _ROLE_PERMISSIONS.get(role)
    if permissions is None:
        raise AuthorizationDeniedError("unknown role denied")
    if required_permission not in permissions:
        raise AuthorizationDeniedError("permission denied")

    return TenantAuthorizationContext(
        user_id=authenticated_user_id,
        tenant_id=requested_tenant_id,
        role=role,
        permissions=permissions,
    )
