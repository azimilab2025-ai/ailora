"""Fail-closed contextual authorization and tenant privilege-boundary contracts."""

from __future__ import annotations

import re
import secrets
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from enum import IntEnum, StrEnum
from typing import Final
from uuid import UUID

_PRINCIPAL_PATTERN: Final = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:@/-]{2,127}$")
_PURPOSE_PATTERN: Final = re.compile(r"^[a-z][a-z0-9_-]{2,47}$")
_HUMAN_MAX_AUTH_AGE: Final = timedelta(hours=8)
_WORKLOAD_MAX_AUTH_AGE: Final = timedelta(minutes=15)
_RECENT_MFA_AGE: Final = timedelta(minutes=5)


class ContextualAuthorizationError(Exception):
    """Generic denial that does not disclose which boundary rejected access."""


class ActorKind(StrEnum):
    """Identity classes remain distinct throughout authorization."""

    HUMAN = "human"
    WORKLOAD = "workload"


class ResourceKind(StrEnum):
    """Tenant resources that can participate in contextual policy."""

    SCENARIO = "scenario"
    SCREENING = "screening"
    REVIEW = "review"
    AUDIT = "audit"
    MEMBERSHIP = "membership"


class ResourceAction(StrEnum):
    """Exact effects; wildcard and spacecraft-command actions do not exist."""

    READ = "read"
    CREATE = "create"
    UPDATE = "update"
    SUBMIT = "submit"
    DECIDE = "decide"
    MANAGE = "manage"


class ContextualPermission(StrEnum):
    """Fine-grained permissions mapped to one exact resource/action pair."""

    SCENARIO_READ = "scenario:read"
    SCENARIO_WRITE = "scenario:write"
    SCREENING_READ = "screening:read"
    SCREENING_SUBMIT = "screening:submit"
    REVIEW_READ = "review:read"
    REVIEW_DECIDE = "review:decide"
    AUDIT_READ = "audit:read"
    MEMBERSHIP_MANAGE = "membership:manage"


class DataClassification(IntEnum):
    """Ordered ceiling used when a grant constrains sensitive resources."""

    INTERNAL = 1
    SENSITIVE = 2
    RESTRICTED = 3


@dataclass(frozen=True, slots=True)
class PermissionContract:
    """Canonical mapping from permission to resource, action and actor class."""

    permission: ContextualPermission
    resource_kind: ResourceKind
    action: ResourceAction
    actor_kinds: frozenset[ActorKind]
    privileged: bool = False

    def __post_init__(self) -> None:
        if not self.actor_kinds:
            raise ValueError("permission contract requires an actor kind")
        if self.privileged and self.actor_kinds != frozenset({ActorKind.HUMAN}):
            raise ValueError("privileged effects must be human-only")


@dataclass(frozen=True, slots=True)
class ContextualGrant:
    """Trusted server-side grant with tenant, purpose and policy-version fences."""

    grant_id: UUID
    principal_id: str
    actor_kind: ActorKind
    tenant_id: UUID
    permissions: frozenset[ContextualPermission]
    purposes: frozenset[str]
    maximum_classification: DataClassification
    issued_at: datetime
    expires_at: datetime
    policy_version: int
    constrained_resource_ids: frozenset[UUID] | None = None
    active: bool = True

    def __post_init__(self) -> None:
        principal_id = self.principal_id.strip()
        if not _PRINCIPAL_PATTERN.fullmatch(principal_id):
            raise ValueError("principal identifier is invalid")
        if not self.permissions:
            raise ValueError("grant requires at least one permission")
        if not self.purposes or any(not _PURPOSE_PATTERN.fullmatch(x) for x in self.purposes):
            raise ValueError("grant purposes must be explicit and valid")
        issued_at = _aware_time(self.issued_at)
        expires_at = _aware_time(self.expires_at)
        maximum_lifetime = (
            _HUMAN_MAX_AUTH_AGE if self.actor_kind is ActorKind.HUMAN else _WORKLOAD_MAX_AUTH_AGE
        )
        if not issued_at < expires_at <= issued_at + maximum_lifetime:
            raise ValueError("grant lifetime exceeds its actor-class boundary")
        if self.policy_version < 1:
            raise ValueError("policy version must be positive")
        if self.constrained_resource_ids is not None and not self.constrained_resource_ids:
            raise ValueError("resource constraint cannot be empty")
        object.__setattr__(self, "principal_id", principal_id)
        object.__setattr__(self, "issued_at", issued_at)
        object.__setattr__(self, "expires_at", expires_at)


@dataclass(frozen=True, slots=True)
class AuthorizationRequest:
    """Untrusted requested effect; every field is checked against trusted state."""

    principal_id: str
    actor_kind: ActorKind
    requested_tenant_id: UUID
    resource_tenant_id: UUID
    resource_id: UUID
    resource_kind: ResourceKind
    action: ResourceAction
    permission: ContextualPermission
    purpose: str
    classification: DataClassification
    correlation_id: UUID
    policy_version: int
    delegation_id: UUID | None = None


@dataclass(frozen=True, slots=True)
class AuthorizationAssurance:
    """Fresh trusted state rechecked immediately before an effect."""

    now: datetime
    authenticated_at: datetime
    trusted_membership_tenant_id: UUID
    current_policy_version: int
    tenant_active: bool = True
    identity_active: bool = True
    session_or_credential_active: bool = True
    mfa_at: datetime | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "now", _aware_time(self.now))
        object.__setattr__(self, "authenticated_at", _aware_time(self.authenticated_at))
        if self.mfa_at is not None:
            object.__setattr__(self, "mfa_at", _aware_time(self.mfa_at))
        if self.current_policy_version < 1:
            raise ValueError("current policy version must be positive")


@dataclass(frozen=True, slots=True)
class ContextualAuthorizationDecision:
    """Auditable allow decision; denial is represented only by an exception."""

    grant_id: UUID
    principal_id: str
    actor_kind: ActorKind
    tenant_id: UUID
    resource_id: UUID
    permission: ContextualPermission
    purpose: str
    correlation_id: UUID
    policy_version: int
    evaluated_at: datetime


class ContextualAuthorizationPolicy:
    """Evaluate tenant, actor, purpose, resource, freshness and privilege together."""

    def __init__(self, contracts: Iterable[PermissionContract]) -> None:
        records = tuple(contracts)
        self._contracts = {record.permission: record for record in records}
        if not records or len(self._contracts) != len(records):
            raise ValueError("permission contracts must be non-empty and unique")

    def authorize(
        self,
        *,
        grant: ContextualGrant,
        request: AuthorizationRequest,
        assurance: AuthorizationAssurance,
    ) -> ContextualAuthorizationDecision:
        """Return an allow decision only after every fail-closed boundary succeeds."""
        contract = self._contracts.get(request.permission)
        maximum_auth_age = (
            _HUMAN_MAX_AUTH_AGE if grant.actor_kind is ActorKind.HUMAN else _WORKLOAD_MAX_AUTH_AGE
        )
        if (
            contract is None
            or not grant.active
            or not assurance.tenant_active
            or not assurance.identity_active
            or not assurance.session_or_credential_active
            or request.delegation_id is not None
            or not secrets.compare_digest(grant.principal_id, request.principal_id)
            or grant.actor_kind is not request.actor_kind
            or request.requested_tenant_id != grant.tenant_id
            or request.resource_tenant_id != grant.tenant_id
            or assurance.trusted_membership_tenant_id != grant.tenant_id
            or request.permission not in grant.permissions
            or request.purpose not in grant.purposes
            or request.classification > grant.maximum_classification
            or request.resource_kind is not contract.resource_kind
            or request.action is not contract.action
            or request.actor_kind not in contract.actor_kinds
            or request.policy_version != grant.policy_version
            or assurance.current_policy_version != grant.policy_version
            or not grant.issued_at <= assurance.now < grant.expires_at
            or assurance.authenticated_at > assurance.now
            or assurance.now - assurance.authenticated_at > maximum_auth_age
            or (
                grant.constrained_resource_ids is not None
                and request.resource_id not in grant.constrained_resource_ids
            )
        ):
            raise ContextualAuthorizationError("contextual authorization denied")
        if contract.privileged and not _recent_mfa(assurance):
            raise ContextualAuthorizationError("contextual authorization denied")

        return ContextualAuthorizationDecision(
            grant_id=grant.grant_id,
            principal_id=grant.principal_id,
            actor_kind=grant.actor_kind,
            tenant_id=grant.tenant_id,
            resource_id=request.resource_id,
            permission=request.permission,
            purpose=request.purpose,
            correlation_id=request.correlation_id,
            policy_version=grant.policy_version,
            evaluated_at=assurance.now,
        )


def default_permission_contracts() -> tuple[PermissionContract, ...]:
    """Return the closed baseline catalog; additions require an explicit code change."""
    human = frozenset({ActorKind.HUMAN})
    both = frozenset({ActorKind.HUMAN, ActorKind.WORKLOAD})
    return (
        PermissionContract(
            ContextualPermission.SCENARIO_READ,
            ResourceKind.SCENARIO,
            ResourceAction.READ,
            both,
        ),
        PermissionContract(
            ContextualPermission.SCENARIO_WRITE,
            ResourceKind.SCENARIO,
            ResourceAction.UPDATE,
            human,
        ),
        PermissionContract(
            ContextualPermission.SCREENING_READ,
            ResourceKind.SCREENING,
            ResourceAction.READ,
            both,
        ),
        PermissionContract(
            ContextualPermission.SCREENING_SUBMIT,
            ResourceKind.SCREENING,
            ResourceAction.SUBMIT,
            both,
        ),
        PermissionContract(
            ContextualPermission.REVIEW_READ,
            ResourceKind.REVIEW,
            ResourceAction.READ,
            human,
        ),
        PermissionContract(
            ContextualPermission.REVIEW_DECIDE,
            ResourceKind.REVIEW,
            ResourceAction.DECIDE,
            human,
            privileged=True,
        ),
        PermissionContract(
            ContextualPermission.AUDIT_READ,
            ResourceKind.AUDIT,
            ResourceAction.READ,
            human,
        ),
        PermissionContract(
            ContextualPermission.MEMBERSHIP_MANAGE,
            ResourceKind.MEMBERSHIP,
            ResourceAction.MANAGE,
            human,
            privileged=True,
        ),
    )


def _aware_time(value: datetime) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("authorization time must be timezone-aware")
    return value.astimezone(UTC)


def _recent_mfa(assurance: AuthorizationAssurance) -> bool:
    mfa_at = assurance.mfa_at
    return bool(
        mfa_at is not None
        and assurance.authenticated_at <= mfa_at <= assurance.now
        and assurance.now - mfa_at <= _RECENT_MFA_AGE
    )
