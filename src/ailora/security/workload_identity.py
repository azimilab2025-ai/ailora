"""Tenant-bound OAuth client-credentials and service authorization contracts."""

from __future__ import annotations

import re
import secrets
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from enum import StrEnum
from typing import Final
from uuid import UUID

from ailora.security.asymmetric_tokens import (
    AsymmetricTokenError,
    AsymmetricTokenProfile,
    RotatingJwtKeyRing,
    decode_access_token,
)

_IDENTIFIER_PATTERN: Final = re.compile(r"^[a-z][a-z0-9._-]{2,63}$")
_SCOPE_PATTERN: Final = re.compile(r"^[a-z][a-z0-9_-]{1,31}:[a-z][a-z0-9_-]{1,31}$")
_RESOURCE_PATTERN: Final = re.compile(r"^[a-z][a-z0-9._/-]{1,127}$")
_ACTION_PATTERN: Final = re.compile(r"^[a-z][a-z0-9_-]{1,31}$")
_HUMAN_IDENTITY_CLAIMS: Final = frozenset(
    {"acr", "amr", "email", "email_verified", "name", "preferred_username", "roles", "sid"}
)


class WorkloadIdentityError(Exception):
    """Safe generic failure for workload authentication or authorization."""


class ServicePermission(StrEnum):
    """Bounded service permissions; no spacecraft-command permission exists."""

    SPACE_DATA_READ = "space-data:read"
    WORKFLOW_READ = "workflow:read"
    WORKFLOW_SUBMIT = "workflow:submit"
    AUDIT_APPEND = "audit:append"


@dataclass(frozen=True, slots=True)
class WorkloadIdentityProfile:
    """Exact JWT trust profile plus bounded workload-token lifetime policy."""

    token_profile: AsymmetricTokenProfile
    maximum_token_lifetime: timedelta = timedelta(minutes=10)
    clock_skew_seconds: int = 30

    def __post_init__(self) -> None:
        if not timedelta(seconds=1) <= self.maximum_token_lifetime <= timedelta(minutes=15):
            raise ValueError(
                "workload token lifetime must be between one second and fifteen minutes"
            )
        if not 0 <= self.clock_skew_seconds <= 30:
            raise ValueError("clock skew must be between zero and thirty seconds")


@dataclass(frozen=True, slots=True)
class WorkloadRegistration:
    """Current tenant-bound registration; it contains no client secret."""

    workload_id: str
    oauth_client_id: str
    tenant_id: UUID
    allowed_scopes: frozenset[str]
    allowed_permissions: frozenset[ServicePermission]
    active: bool = True

    def __post_init__(self) -> None:
        workload_id = self.workload_id.strip()
        oauth_client_id = self.oauth_client_id.strip()
        if not _IDENTIFIER_PATTERN.fullmatch(workload_id):
            raise ValueError("workload identifier is invalid")
        if not _IDENTIFIER_PATTERN.fullmatch(oauth_client_id):
            raise ValueError("OAuth client identifier is invalid")
        if not 1 <= len(self.allowed_scopes) <= 32:
            raise ValueError("one to thirty-two allowed scopes are required")
        if any(not _SCOPE_PATTERN.fullmatch(scope) for scope in self.allowed_scopes):
            raise ValueError("allowed scope is invalid")
        if not self.allowed_permissions:
            raise ValueError("at least one service permission is required")
        object.__setattr__(self, "workload_id", workload_id)
        object.__setattr__(self, "oauth_client_id", oauth_client_id)


@dataclass(frozen=True, slots=True)
class VerifiedWorkloadPrincipal:
    """Verified machine identity that remains bound to one tenant."""

    issuer: str
    workload_id: str
    oauth_client_id: str
    tenant_id: UUID
    scopes: frozenset[str]
    token_id: UUID
    issued_at: datetime
    expires_at: datetime


@dataclass(frozen=True, slots=True)
class ServiceAuthorizationRule:
    """Exact resource/action/scope mapping for one service permission."""

    permission: ServicePermission
    resource: str
    action: str
    required_scope: str

    def __post_init__(self) -> None:
        if not _RESOURCE_PATTERN.fullmatch(self.resource):
            raise ValueError("service resource is invalid")
        if not _ACTION_PATTERN.fullmatch(self.action):
            raise ValueError("service action is invalid")
        if not _SCOPE_PATTERN.fullmatch(self.required_scope):
            raise ValueError("required scope is invalid")


@dataclass(frozen=True, slots=True)
class WorkloadAuthorizationContext:
    """Auditable result of a successful service authorization decision."""

    workload_id: str
    oauth_client_id: str
    tenant_id: UUID
    token_id: UUID
    permission: ServicePermission
    resource: str
    action: str


class WorkloadTokenVerifier:
    """Verify short-lived client-credentials access tokens without remote key lookup."""

    def __init__(
        self,
        *,
        profile: WorkloadIdentityProfile,
        key_ring: RotatingJwtKeyRing,
        registrations: Iterable[WorkloadRegistration],
    ) -> None:
        self._profile = profile
        self._key_ring = key_ring
        self._registrations = _registration_index(registrations)

    def verify(
        self,
        token: str,
        *,
        now: datetime | None = None,
    ) -> VerifiedWorkloadPrincipal:
        """Return a tenant-bound principal only after every claim and registration check."""
        checked_at = _aware_time(now)
        try:
            payload = decode_access_token(
                token,
                key_ring=self._key_ring,
                profile=self._profile.token_profile,
                leeway_seconds=self._profile.clock_skew_seconds,
            )
            if _HUMAN_IDENTITY_CLAIMS.intersection(payload):
                raise WorkloadIdentityError("workload identity validation failed")
            if payload.get("gty") != "client_credentials" or payload.get("token_use") != "access":
                raise WorkloadIdentityError("workload identity validation failed")

            workload_id = _required_string(payload.get("sub"))
            oauth_client_id = _required_string(payload.get("client_id"))
            if payload.get("azp") != oauth_client_id:
                raise WorkloadIdentityError("workload identity validation failed")
            tenant_id = UUID(_required_string(payload.get("tenant_id")))
            scopes = _parse_scope(payload.get("scope"))
            token_id = UUID(_required_string(payload.get("jti")))
            issued_at = _numeric_date(payload.get("iat"))
            expires_at = _numeric_date(payload.get("exp"))

            registration = self._registrations.get(workload_id)
            if registration is None or not registration.active:
                raise WorkloadIdentityError("workload identity validation failed")
            if not secrets.compare_digest(registration.oauth_client_id, oauth_client_id):
                raise WorkloadIdentityError("workload identity validation failed")
            if registration.tenant_id != tenant_id or not scopes.issubset(
                registration.allowed_scopes
            ):
                raise WorkloadIdentityError("workload identity validation failed")
            skew = timedelta(seconds=self._profile.clock_skew_seconds)
            if (
                issued_at - checked_at > skew
                or expires_at <= issued_at
                or expires_at - issued_at > self._profile.maximum_token_lifetime
                or checked_at - issued_at > self._profile.maximum_token_lifetime + skew
                or expires_at < checked_at - skew
            ):
                raise WorkloadIdentityError("workload identity validation failed")
        except WorkloadIdentityError:
            raise
        except (AsymmetricTokenError, TypeError, ValueError) as exc:
            raise WorkloadIdentityError("workload identity validation failed") from exc

        return VerifiedWorkloadPrincipal(
            issuer=self._profile.token_profile.issuer,
            workload_id=workload_id,
            oauth_client_id=oauth_client_id,
            tenant_id=tenant_id,
            scopes=scopes,
            token_id=token_id,
            issued_at=issued_at,
            expires_at=expires_at,
        )


class ServiceAuthorizationPolicy:
    """Recheck current registration and exact tenant/resource/action before use."""

    def __init__(
        self,
        *,
        registrations: Iterable[WorkloadRegistration],
        rules: Iterable[ServiceAuthorizationRule],
    ) -> None:
        self._registrations = _registration_index(registrations)
        rule_records = tuple(rules)
        self._rules = {rule.permission: rule for rule in rule_records}
        if not rule_records or len(self._rules) != len(rule_records):
            raise ValueError("authorization rules must be non-empty and permission-unique")

    def authorize(
        self,
        principal: VerifiedWorkloadPrincipal,
        *,
        requested_tenant_id: UUID,
        permission: ServicePermission,
        resource: str,
        action: str,
    ) -> WorkloadAuthorizationContext:
        """Authorize one exact service effect and reject confused-deputy transitions."""
        registration = self._registrations.get(principal.workload_id)
        rule = self._rules.get(permission)
        if registration is None or not registration.active or rule is None:
            raise WorkloadIdentityError("service authorization denied")
        if (
            registration.tenant_id != principal.tenant_id
            or requested_tenant_id != principal.tenant_id
            or not secrets.compare_digest(registration.oauth_client_id, principal.oauth_client_id)
            or permission not in registration.allowed_permissions
            or rule.required_scope not in principal.scopes
            or not secrets.compare_digest(rule.resource, resource)
            or not secrets.compare_digest(rule.action, action)
        ):
            raise WorkloadIdentityError("service authorization denied")
        return WorkloadAuthorizationContext(
            workload_id=principal.workload_id,
            oauth_client_id=principal.oauth_client_id,
            tenant_id=principal.tenant_id,
            token_id=principal.token_id,
            permission=permission,
            resource=resource,
            action=action,
        )


def _registration_index(
    registrations: Iterable[WorkloadRegistration],
) -> dict[str, WorkloadRegistration]:
    records = tuple(registrations)
    by_workload = {record.workload_id: record for record in records}
    client_ids = {record.oauth_client_id for record in records}
    if not records or len(records) > 256:
        raise ValueError("one to two-hundred-fifty-six workload registrations are required")
    if len(by_workload) != len(records) or len(client_ids) != len(records):
        raise ValueError("workload and OAuth client identifiers must be unique")
    return by_workload


def _aware_time(value: datetime | None) -> datetime:
    result = value or datetime.now(UTC)
    if result.tzinfo is None or result.utcoffset() is None:
        raise ValueError("verification time must be timezone-aware")
    return result.astimezone(UTC)


def _required_string(value: object) -> str:
    if not isinstance(value, str) or not value.strip():
        raise WorkloadIdentityError("workload identity validation failed")
    return value.strip()


def _parse_scope(value: object) -> frozenset[str]:
    raw_scope = _required_string(value)
    values = raw_scope.split(" ")
    scopes = frozenset(values)
    if len(scopes) != len(values) or any(not _SCOPE_PATTERN.fullmatch(scope) for scope in scopes):
        raise WorkloadIdentityError("workload identity validation failed")
    return scopes


def _numeric_date(value: object) -> datetime:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise WorkloadIdentityError("workload identity validation failed")
    return datetime.fromtimestamp(value, tz=UTC)
