"""Fail-closed authorization, tenant isolation, and OpenAPI security tests."""

from __future__ import annotations

import importlib
from uuid import uuid4

import pytest


def _policy() -> object:
    return importlib.import_module("ailora.security.authorization")


def _authorize(**overrides: object) -> object:
    policy = _policy()
    user_id = uuid4()
    tenant_id = uuid4()
    values: dict[str, object] = {
        "authenticated_user_id": user_id,
        "requested_tenant_id": tenant_id,
        "membership_user_id": user_id,
        "membership_tenant_id": tenant_id,
        "membership_role": "viewer",
        "user_active": True,
        "tenant_active": True,
        "membership_active": True,
        "required_permission": policy.Permission.TENANT_READ,
    }
    values.update(overrides)
    return policy.authorize_tenant_membership(**values)


def test_matching_active_membership_grants_tenant_context() -> None:
    context = _authorize()
    assert context.role == "viewer"
    assert "tenant:read" in context.permissions


def test_cross_tenant_request_is_denied() -> None:
    policy = _policy()
    with pytest.raises(policy.AuthorizationDeniedError, match="cross-tenant"):
        _authorize(membership_tenant_id=uuid4())


def test_membership_for_different_user_is_denied() -> None:
    policy = _policy()
    with pytest.raises(policy.AuthorizationDeniedError, match="user mismatch"):
        _authorize(membership_user_id=uuid4())


@pytest.mark.parametrize(
    ("state", "message"),
    [
        ({"user_active": False}, "inactive user"),
        ({"tenant_active": False}, "inactive tenant"),
        ({"membership_active": False}, "revoked membership"),
    ],
)
def test_inactive_or_revoked_state_is_denied(
    state: dict[str, object],
    message: str,
) -> None:
    policy = _policy()
    with pytest.raises(policy.AuthorizationDeniedError, match=message):
        _authorize(**state)


def test_unknown_role_is_denied_by_default() -> None:
    policy = _policy()
    with pytest.raises(policy.AuthorizationDeniedError, match="unknown role"):
        _authorize(membership_role="untrusted_superuser")


def test_viewer_privilege_escalation_is_denied() -> None:
    policy = _policy()
    with pytest.raises(policy.AuthorizationDeniedError, match="permission denied"):
        _authorize(required_permission=policy.Permission.MEMBERSHIP_MANAGE)


def test_admin_can_manage_memberships() -> None:
    policy = _policy()
    context = _authorize(
        membership_role="admin",
        required_permission=policy.Permission.MEMBERSHIP_MANAGE,
    )
    assert policy.Permission.MEMBERSHIP_MANAGE in context.permissions


def test_forged_subject_claim_is_denied() -> None:
    policy = _policy()
    authenticated_user_id = uuid4()
    with pytest.raises(policy.AuthorizationDeniedError, match="does not match"):
        policy.require_claim_subject(
            authenticated_user_id=authenticated_user_id,
            token_subject=str(uuid4()),
        )


@pytest.mark.parametrize("subject", ["", "not-a-uuid"])
def test_malformed_subject_claim_is_denied(subject: str) -> None:
    policy = _policy()
    with pytest.raises(policy.AuthorizationDeniedError, match="invalid"):
        policy.require_claim_subject(
            authenticated_user_id=uuid4(),
            token_subject=subject,
        )


def test_openapi_exposes_protected_authorization_route() -> None:
    app_module = importlib.import_module("ailora.api.app")
    schema = app_module.app.openapi()
    operation = schema["paths"]["/v1/auth/session"]["get"]
    schemes = schema.get("components", {}).get("securitySchemes", {})

    assert schemes
    assert operation.get("security")


def test_authorization_route_has_no_secret_response_fields() -> None:
    app_module = importlib.import_module("ailora.api.app")
    schema = app_module.app.openapi()
    response_schema = schema["components"]["schemas"]["AuthorizationSessionResponse"]
    fields = set(response_schema.get("properties", {}))
    forbidden = {"token", "secret", "password", "claims", "tenant_id", "user_id"}

    assert fields.isdisjoint(forbidden)
