"""Contextual authorization, tenant isolation, and privilege-boundary contracts."""

from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime, timedelta
from uuid import UUID, uuid4

import pytest

from ailora.security.contextual_authorization import (
    ActorKind,
    AuthorizationAssurance,
    AuthorizationRequest,
    ContextualAuthorizationError,
    ContextualAuthorizationPolicy,
    ContextualGrant,
    ContextualPermission,
    DataClassification,
    PermissionContract,
    ResourceAction,
    ResourceKind,
    default_permission_contracts,
)

TENANT_ID = UUID("11111111-1111-4111-8111-111111111111")
OTHER_TENANT_ID = UUID("22222222-2222-4222-8222-222222222222")
RESOURCE_ID = UUID("33333333-3333-4333-8333-333333333333")
OTHER_RESOURCE_ID = UUID("44444444-4444-4444-8444-444444444444")


@pytest.fixture
def now() -> datetime:
    return datetime.now(UTC).replace(microsecond=0)


@pytest.fixture
def policy() -> ContextualAuthorizationPolicy:
    return ContextualAuthorizationPolicy(default_permission_contracts())


@pytest.fixture
def human_grant(now: datetime) -> ContextualGrant:
    return ContextualGrant(
        grant_id=uuid4(),
        principal_id="11111111-1111-4111-8111-111111111111",
        actor_kind=ActorKind.HUMAN,
        tenant_id=TENANT_ID,
        permissions=frozenset(
            {
                ContextualPermission.SCENARIO_READ,
                ContextualPermission.REVIEW_DECIDE,
                ContextualPermission.MEMBERSHIP_MANAGE,
            }
        ),
        purposes=frozenset({"mission_review", "tenant_administration"}),
        maximum_classification=DataClassification.RESTRICTED,
        issued_at=now - timedelta(minutes=1),
        expires_at=now + timedelta(hours=1),
        policy_version=7,
    )


@pytest.fixture
def workload_grant(now: datetime) -> ContextualGrant:
    return ContextualGrant(
        grant_id=uuid4(),
        principal_id="orbit-screening-worker",
        actor_kind=ActorKind.WORKLOAD,
        tenant_id=TENANT_ID,
        permissions=frozenset(
            {ContextualPermission.SCENARIO_READ, ContextualPermission.SCREENING_SUBMIT}
        ),
        purposes=frozenset({"automated_screening"}),
        maximum_classification=DataClassification.SENSITIVE,
        issued_at=now - timedelta(minutes=1),
        expires_at=now + timedelta(minutes=9),
        policy_version=7,
        constrained_resource_ids=frozenset({RESOURCE_ID}),
    )


def _request(
    grant: ContextualGrant,
    *,
    permission: ContextualPermission = ContextualPermission.SCENARIO_READ,
    resource_kind: ResourceKind = ResourceKind.SCENARIO,
    action: ResourceAction = ResourceAction.READ,
    purpose: str | None = None,
    classification: DataClassification = DataClassification.SENSITIVE,
) -> AuthorizationRequest:
    return AuthorizationRequest(
        principal_id=grant.principal_id,
        actor_kind=grant.actor_kind,
        requested_tenant_id=TENANT_ID,
        resource_tenant_id=TENANT_ID,
        resource_id=RESOURCE_ID,
        resource_kind=resource_kind,
        action=action,
        permission=permission,
        purpose=purpose or next(iter(sorted(grant.purposes))),
        classification=classification,
        correlation_id=uuid4(),
        policy_version=grant.policy_version,
    )


def _assurance(
    now: datetime,
    *,
    mfa_at: datetime | None = None,
) -> AuthorizationAssurance:
    return AuthorizationAssurance(
        now=now,
        authenticated_at=now - timedelta(minutes=2),
        trusted_membership_tenant_id=TENANT_ID,
        current_policy_version=7,
        mfa_at=mfa_at,
    )


def test_human_standard_access_returns_auditable_decision(
    policy: ContextualAuthorizationPolicy,
    human_grant: ContextualGrant,
    now: datetime,
) -> None:
    request = _request(human_grant, purpose="mission_review")
    decision = policy.authorize(
        grant=human_grant,
        request=request,
        assurance=_assurance(now),
    )

    assert decision.grant_id == human_grant.grant_id
    assert decision.principal_id == human_grant.principal_id
    assert decision.tenant_id == TENANT_ID
    assert decision.resource_id == RESOURCE_ID
    assert decision.correlation_id == request.correlation_id
    assert decision.policy_version == 7
    assert decision.evaluated_at == now


def test_workload_access_uses_separate_actor_contract(
    policy: ContextualAuthorizationPolicy,
    workload_grant: ContextualGrant,
    now: datetime,
) -> None:
    request = _request(
        workload_grant,
        permission=ContextualPermission.SCREENING_SUBMIT,
        resource_kind=ResourceKind.SCREENING,
        action=ResourceAction.SUBMIT,
        purpose="automated_screening",
    )
    decision = policy.authorize(
        grant=workload_grant,
        request=request,
        assurance=_assurance(now),
    )

    assert decision.actor_kind is ActorKind.WORKLOAD
    assert decision.permission is ContextualPermission.SCREENING_SUBMIT


@pytest.mark.parametrize(
    "request_change",
    (
        {"requested_tenant_id": OTHER_TENANT_ID},
        {"resource_tenant_id": OTHER_TENANT_ID},
    ),
)
def test_requested_and_resource_tenant_mismatch_fail_closed(
    request_change: dict[str, object],
    policy: ContextualAuthorizationPolicy,
    human_grant: ContextualGrant,
    now: datetime,
) -> None:
    request = replace(_request(human_grant), **request_change)

    with pytest.raises(ContextualAuthorizationError, match="contextual authorization denied"):
        policy.authorize(grant=human_grant, request=request, assurance=_assurance(now))


def test_trusted_membership_tenant_cannot_be_replaced_by_request_input(
    policy: ContextualAuthorizationPolicy,
    human_grant: ContextualGrant,
    now: datetime,
) -> None:
    assurance = replace(_assurance(now), trusted_membership_tenant_id=OTHER_TENANT_ID)

    with pytest.raises(ContextualAuthorizationError):
        policy.authorize(grant=human_grant, request=_request(human_grant), assurance=assurance)


@pytest.mark.parametrize(
    "request_change",
    (
        {"principal_id": "different-principal"},
        {"actor_kind": ActorKind.WORKLOAD},
    ),
)
def test_principal_and_actor_class_cannot_be_substituted(
    request_change: dict[str, object],
    policy: ContextualAuthorizationPolicy,
    human_grant: ContextualGrant,
    now: datetime,
) -> None:
    request = replace(_request(human_grant), **request_change)

    with pytest.raises(ContextualAuthorizationError):
        policy.authorize(grant=human_grant, request=request, assurance=_assurance(now))


@pytest.mark.parametrize(
    "request_change",
    (
        {"permission": ContextualPermission.SCREENING_READ},
        {"resource_kind": ResourceKind.SCREENING},
        {"action": ResourceAction.UPDATE},
    ),
)
def test_permission_resource_and_action_must_match_one_contract(
    request_change: dict[str, object],
    policy: ContextualAuthorizationPolicy,
    human_grant: ContextualGrant,
    now: datetime,
) -> None:
    request = replace(_request(human_grant), **request_change)

    with pytest.raises(ContextualAuthorizationError):
        policy.authorize(grant=human_grant, request=request, assurance=_assurance(now))


@pytest.mark.parametrize(
    "request_change",
    (
        {"purpose": "unapproved_export"},
        {"classification": DataClassification.RESTRICTED},
    ),
)
def test_purpose_and_classification_ceiling_are_enforced(
    request_change: dict[str, object],
    policy: ContextualAuthorizationPolicy,
    workload_grant: ContextualGrant,
    now: datetime,
) -> None:
    request = replace(_request(workload_grant), **request_change)

    with pytest.raises(ContextualAuthorizationError):
        policy.authorize(grant=workload_grant, request=request, assurance=_assurance(now))


@pytest.mark.parametrize(
    ("request_version", "current_version"),
    ((6, 7), (7, 8)),
)
def test_request_and_current_policy_versions_fence_stale_grants(
    request_version: int,
    current_version: int,
    policy: ContextualAuthorizationPolicy,
    human_grant: ContextualGrant,
    now: datetime,
) -> None:
    request = replace(_request(human_grant), policy_version=request_version)
    assurance = replace(_assurance(now), current_policy_version=current_version)

    with pytest.raises(ContextualAuthorizationError):
        policy.authorize(grant=human_grant, request=request, assurance=assurance)


@pytest.mark.parametrize(
    "assurance_change",
    (
        {"tenant_active": False},
        {"identity_active": False},
        {"session_or_credential_active": False},
    ),
)
def test_current_tenant_identity_and_credential_state_are_rechecked(
    assurance_change: dict[str, object],
    policy: ContextualAuthorizationPolicy,
    human_grant: ContextualGrant,
    now: datetime,
) -> None:
    assurance = replace(_assurance(now), **assurance_change)

    with pytest.raises(ContextualAuthorizationError):
        policy.authorize(grant=human_grant, request=_request(human_grant), assurance=assurance)


def test_revoked_grant_is_denied_immediately(
    policy: ContextualAuthorizationPolicy,
    human_grant: ContextualGrant,
    now: datetime,
) -> None:
    with pytest.raises(ContextualAuthorizationError):
        policy.authorize(
            grant=replace(human_grant, active=False),
            request=_request(human_grant),
            assurance=_assurance(now),
        )


@pytest.mark.parametrize(
    "assurance_change",
    (
        {"authenticated_at": datetime(2030, 1, 1, tzinfo=UTC)},
        {"authenticated_at": datetime(2020, 1, 1, tzinfo=UTC)},
    ),
)
def test_future_or_stale_authentication_is_denied(
    assurance_change: dict[str, object],
    policy: ContextualAuthorizationPolicy,
    human_grant: ContextualGrant,
    now: datetime,
) -> None:
    assurance = replace(_assurance(now), **assurance_change)

    with pytest.raises(ContextualAuthorizationError):
        policy.authorize(grant=human_grant, request=_request(human_grant), assurance=assurance)


def test_expired_grant_is_denied(
    policy: ContextualAuthorizationPolicy,
    human_grant: ContextualGrant,
    now: datetime,
) -> None:
    expired = replace(
        human_grant,
        issued_at=now - timedelta(hours=2),
        expires_at=now - timedelta(hours=1),
    )

    with pytest.raises(ContextualAuthorizationError):
        policy.authorize(grant=expired, request=_request(expired), assurance=_assurance(now))


def test_recent_mfa_allows_privileged_human_decision(
    policy: ContextualAuthorizationPolicy,
    human_grant: ContextualGrant,
    now: datetime,
) -> None:
    request = _request(
        human_grant,
        permission=ContextualPermission.REVIEW_DECIDE,
        resource_kind=ResourceKind.REVIEW,
        action=ResourceAction.DECIDE,
        purpose="mission_review",
    )
    decision = policy.authorize(
        grant=human_grant,
        request=request,
        assurance=_assurance(now, mfa_at=now - timedelta(minutes=1)),
    )

    assert decision.permission is ContextualPermission.REVIEW_DECIDE


@pytest.mark.parametrize(
    "mfa_at",
    (None, datetime(2020, 1, 1, tzinfo=UTC), datetime(2030, 1, 1, tzinfo=UTC)),
)
def test_missing_stale_or_future_mfa_denies_privileged_effect(
    mfa_at: datetime | None,
    policy: ContextualAuthorizationPolicy,
    human_grant: ContextualGrant,
    now: datetime,
) -> None:
    request = _request(
        human_grant,
        permission=ContextualPermission.MEMBERSHIP_MANAGE,
        resource_kind=ResourceKind.MEMBERSHIP,
        action=ResourceAction.MANAGE,
        purpose="tenant_administration",
    )

    with pytest.raises(ContextualAuthorizationError):
        policy.authorize(
            grant=human_grant,
            request=request,
            assurance=_assurance(now, mfa_at=mfa_at),
        )


def test_workload_cannot_receive_human_privileged_contract(
    policy: ContextualAuthorizationPolicy,
    workload_grant: ContextualGrant,
    now: datetime,
) -> None:
    elevated = replace(
        workload_grant,
        permissions=frozenset({ContextualPermission.REVIEW_DECIDE}),
        purposes=frozenset({"mission_review"}),
    )
    request = _request(
        elevated,
        permission=ContextualPermission.REVIEW_DECIDE,
        resource_kind=ResourceKind.REVIEW,
        action=ResourceAction.DECIDE,
        purpose="mission_review",
    )

    with pytest.raises(ContextualAuthorizationError):
        policy.authorize(
            grant=elevated,
            request=request,
            assurance=_assurance(now, mfa_at=now),
        )


def test_ambient_delegation_is_rejected_without_explicit_delegation_contract(
    policy: ContextualAuthorizationPolicy,
    human_grant: ContextualGrant,
    now: datetime,
) -> None:
    request = replace(_request(human_grant), delegation_id=uuid4())

    with pytest.raises(ContextualAuthorizationError):
        policy.authorize(grant=human_grant, request=request, assurance=_assurance(now))


def test_object_constraint_blocks_lateral_resource_access(
    policy: ContextualAuthorizationPolicy,
    workload_grant: ContextualGrant,
    now: datetime,
) -> None:
    request = replace(_request(workload_grant), resource_id=OTHER_RESOURCE_ID)

    with pytest.raises(ContextualAuthorizationError):
        policy.authorize(grant=workload_grant, request=request, assurance=_assurance(now))


def test_grant_lifetime_and_resource_constraint_validate_fail_closed(now: datetime) -> None:
    common = {
        "grant_id": uuid4(),
        "principal_id": "orbit-screening-worker",
        "actor_kind": ActorKind.WORKLOAD,
        "tenant_id": TENANT_ID,
        "permissions": frozenset({ContextualPermission.SCREENING_SUBMIT}),
        "purposes": frozenset({"automated_screening"}),
        "maximum_classification": DataClassification.SENSITIVE,
        "issued_at": now,
        "policy_version": 1,
    }

    with pytest.raises(ValueError, match="lifetime"):
        ContextualGrant(**common, expires_at=now + timedelta(minutes=16))
    with pytest.raises(ValueError, match="constraint cannot be empty"):
        ContextualGrant(
            **common,
            expires_at=now + timedelta(minutes=5),
            constrained_resource_ids=frozenset(),
        )


def test_permission_catalog_is_unique_closed_and_has_no_command_authority() -> None:
    contracts = default_permission_contracts()
    permissions = {record.permission.value for record in contracts}
    actions = {record.action.value for record in contracts}

    assert len(permissions) == len(contracts)
    assert all("*" not in value for value in permissions | actions)
    assert all("command" not in value for value in permissions | actions)
    assert all("uplink" not in value for value in permissions | actions)
    assert all("maneuver" not in value for value in permissions | actions)


def test_ambiguous_or_workload_privileged_contract_catalog_is_rejected() -> None:
    contract = default_permission_contracts()[0]

    with pytest.raises(ValueError, match="unique"):
        ContextualAuthorizationPolicy((contract, contract))
    with pytest.raises(ValueError, match="human-only"):
        PermissionContract(
            ContextualPermission.REVIEW_DECIDE,
            ResourceKind.REVIEW,
            ResourceAction.DECIDE,
            frozenset({ActorKind.WORKLOAD}),
            privileged=True,
        )
