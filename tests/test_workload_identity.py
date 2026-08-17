"""Tenant-bound workload identity and service authorization contracts."""

from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime, timedelta
from uuid import UUID, uuid4

import pytest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from ailora.security.asymmetric_tokens import (
    AsymmetricTokenProfile,
    JwtSigningKey,
    RotatingJwtKeyRing,
    issue_access_token,
)
from ailora.security.workload_identity import (
    ServiceAuthorizationPolicy,
    ServiceAuthorizationRule,
    ServicePermission,
    WorkloadIdentityError,
    WorkloadIdentityProfile,
    WorkloadRegistration,
    WorkloadTokenVerifier,
)

TENANT_ID = UUID("11111111-1111-4111-8111-111111111111")
OTHER_TENANT_ID = UUID("22222222-2222-4222-8222-222222222222")


@pytest.fixture(scope="module")
def signing_key() -> JwtSigningKey:
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    private_pem = private_key.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption(),
    ).decode("ascii")
    return JwtSigningKey.from_private_pem(kid="workload-key-01", private_key_pem=private_pem)


@pytest.fixture
def token_profile() -> AsymmetricTokenProfile:
    return AsymmetricTokenProfile(
        issuer="https://workload-id.ailora.example/",
        audience="ailora-service-api",
        access_token_ttl=timedelta(minutes=5),
    )


@pytest.fixture
def registration() -> WorkloadRegistration:
    return WorkloadRegistration(
        workload_id="orbit-ingest-worker",
        oauth_client_id="orbit-ingest-client",
        tenant_id=TENANT_ID,
        allowed_scopes=frozenset({"space-data:read", "workflow:submit"}),
        allowed_permissions=frozenset(
            {ServicePermission.SPACE_DATA_READ, ServicePermission.WORKFLOW_SUBMIT}
        ),
    )


@pytest.fixture
def rules() -> tuple[ServiceAuthorizationRule, ...]:
    return (
        ServiceAuthorizationRule(
            permission=ServicePermission.SPACE_DATA_READ,
            resource="space-data/catalog",
            action="read",
            required_scope="space-data:read",
        ),
        ServiceAuthorizationRule(
            permission=ServicePermission.WORKFLOW_SUBMIT,
            resource="workflows/screening",
            action="submit",
            required_scope="workflow:submit",
        ),
    )


def _ring(signing_key: JwtSigningKey) -> RotatingJwtKeyRing:
    return RotatingJwtKeyRing(keys=[signing_key], active_kid=signing_key.kid)


def _token(
    signing_key: JwtSigningKey,
    token_profile: AsymmetricTokenProfile,
    registration: WorkloadRegistration,
    *,
    now: datetime,
    claims: dict[str, object] | None = None,
) -> str:
    client_id = registration.oauth_client_id
    return issue_access_token(
        subject=registration.workload_id,
        key_ring=_ring(signing_key),
        profile=token_profile,
        now=now,
        jti=uuid4(),
        extra_claims={
            "azp": client_id,
            "client_id": client_id,
            "gty": "client_credentials",
            "scope": " ".join(sorted(registration.allowed_scopes)),
            "tenant_id": str(registration.tenant_id),
            "token_use": "access",
            **(claims or {}),
        },
    )


def _verifier(
    signing_key: JwtSigningKey,
    token_profile: AsymmetricTokenProfile,
    registrations: tuple[WorkloadRegistration, ...],
) -> WorkloadTokenVerifier:
    return WorkloadTokenVerifier(
        profile=WorkloadIdentityProfile(token_profile=token_profile),
        key_ring=_ring(signing_key),
        registrations=registrations,
    )


def test_client_credentials_token_builds_tenant_bound_principal_and_context(
    signing_key: JwtSigningKey,
    token_profile: AsymmetricTokenProfile,
    registration: WorkloadRegistration,
    rules: tuple[ServiceAuthorizationRule, ...],
) -> None:
    now = datetime.now(UTC).replace(microsecond=0)
    principal = _verifier(signing_key, token_profile, (registration,)).verify(
        _token(signing_key, token_profile, registration, now=now),
        now=now,
    )
    context = ServiceAuthorizationPolicy(registrations=(registration,), rules=rules).authorize(
        principal,
        requested_tenant_id=TENANT_ID,
        permission=ServicePermission.SPACE_DATA_READ,
        resource="space-data/catalog",
        action="read",
    )

    assert principal.workload_id == "orbit-ingest-worker"
    assert principal.oauth_client_id == "orbit-ingest-client"
    assert principal.tenant_id == TENANT_ID
    assert principal.scopes == frozenset({"space-data:read", "workflow:submit"})
    assert context.tenant_id == TENANT_ID
    assert context.token_id == principal.token_id


@pytest.mark.parametrize(
    ("tenant_id", "resource", "action"),
    (
        (OTHER_TENANT_ID, "space-data/catalog", "read"),
        (TENANT_ID, "workflows/screening", "read"),
        (TENANT_ID, "space-data/catalog", "write"),
    ),
)
def test_cross_tenant_resource_and_action_confusion_fail_closed(
    tenant_id: UUID,
    resource: str,
    action: str,
    signing_key: JwtSigningKey,
    token_profile: AsymmetricTokenProfile,
    registration: WorkloadRegistration,
    rules: tuple[ServiceAuthorizationRule, ...],
) -> None:
    now = datetime.now(UTC).replace(microsecond=0)
    principal = _verifier(signing_key, token_profile, (registration,)).verify(
        _token(signing_key, token_profile, registration, now=now), now=now
    )
    policy = ServiceAuthorizationPolicy(registrations=(registration,), rules=rules)

    with pytest.raises(WorkloadIdentityError, match="service authorization denied"):
        policy.authorize(
            principal,
            requested_tenant_id=tenant_id,
            permission=ServicePermission.SPACE_DATA_READ,
            resource=resource,
            action=action,
        )


def test_scope_and_registered_permission_are_both_required(
    signing_key: JwtSigningKey,
    token_profile: AsymmetricTokenProfile,
    registration: WorkloadRegistration,
    rules: tuple[ServiceAuthorizationRule, ...],
) -> None:
    now = datetime.now(UTC).replace(microsecond=0)
    read_only = replace(
        registration,
        allowed_scopes=frozenset({"space-data:read"}),
        allowed_permissions=frozenset({ServicePermission.SPACE_DATA_READ}),
    )
    principal = _verifier(signing_key, token_profile, (read_only,)).verify(
        _token(signing_key, token_profile, read_only, now=now), now=now
    )

    with pytest.raises(WorkloadIdentityError, match="service authorization denied"):
        ServiceAuthorizationPolicy(registrations=(read_only,), rules=rules).authorize(
            principal,
            requested_tenant_id=TENANT_ID,
            permission=ServicePermission.WORKFLOW_SUBMIT,
            resource="workflows/screening",
            action="submit",
        )


def test_registration_revocation_is_rechecked_at_authorization_time(
    signing_key: JwtSigningKey,
    token_profile: AsymmetricTokenProfile,
    registration: WorkloadRegistration,
    rules: tuple[ServiceAuthorizationRule, ...],
) -> None:
    now = datetime.now(UTC).replace(microsecond=0)
    principal = _verifier(signing_key, token_profile, (registration,)).verify(
        _token(signing_key, token_profile, registration, now=now), now=now
    )
    revoked = replace(registration, active=False)

    with pytest.raises(WorkloadIdentityError, match="service authorization denied"):
        ServiceAuthorizationPolicy(registrations=(revoked,), rules=rules).authorize(
            principal,
            requested_tenant_id=TENANT_ID,
            permission=ServicePermission.SPACE_DATA_READ,
            resource="space-data/catalog",
            action="read",
        )


@pytest.mark.parametrize(
    "claims",
    (
        {"client_id": "different-client", "azp": "different-client"},
        {"tenant_id": str(OTHER_TENANT_ID)},
        {"azp": "different-client"},
    ),
)
def test_client_and_tenant_binding_mismatch_is_rejected(
    claims: dict[str, object],
    signing_key: JwtSigningKey,
    token_profile: AsymmetricTokenProfile,
    registration: WorkloadRegistration,
) -> None:
    now = datetime.now(UTC).replace(microsecond=0)
    token = _token(signing_key, token_profile, registration, now=now, claims=claims)

    with pytest.raises(WorkloadIdentityError, match="workload identity validation failed"):
        _verifier(signing_key, token_profile, (registration,)).verify(token, now=now)


@pytest.mark.parametrize(
    "claims",
    ({"gty": "authorization_code"}, {"token_use": "id"}),
)
def test_only_client_credentials_access_tokens_are_accepted(
    claims: dict[str, object],
    signing_key: JwtSigningKey,
    token_profile: AsymmetricTokenProfile,
    registration: WorkloadRegistration,
) -> None:
    now = datetime.now(UTC).replace(microsecond=0)
    token = _token(signing_key, token_profile, registration, now=now, claims=claims)

    with pytest.raises(WorkloadIdentityError, match="workload identity validation failed"):
        _verifier(signing_key, token_profile, (registration,)).verify(token, now=now)


@pytest.mark.parametrize("claim", ("email", "amr", "roles", "sid"))
def test_human_identity_claims_cannot_be_smuggled_into_workload_tokens(
    claim: str,
    signing_key: JwtSigningKey,
    token_profile: AsymmetricTokenProfile,
    registration: WorkloadRegistration,
) -> None:
    now = datetime.now(UTC).replace(microsecond=0)
    token = _token(
        signing_key,
        token_profile,
        registration,
        now=now,
        claims={claim: ["admin"] if claim in {"amr", "roles"} else "value"},
    )

    with pytest.raises(WorkloadIdentityError, match="workload identity validation failed"):
        _verifier(signing_key, token_profile, (registration,)).verify(token, now=now)


def test_unregistered_or_inactive_workload_is_rejected(
    signing_key: JwtSigningKey,
    token_profile: AsymmetricTokenProfile,
    registration: WorkloadRegistration,
) -> None:
    now = datetime.now(UTC).replace(microsecond=0)
    token = _token(signing_key, token_profile, registration, now=now)
    other = replace(
        registration,
        workload_id="different-worker",
        oauth_client_id="different-client",
    )

    for registrations in ((other,), (replace(registration, active=False),)):
        with pytest.raises(WorkloadIdentityError, match="workload identity validation failed"):
            _verifier(signing_key, token_profile, registrations).verify(token, now=now)


def test_excessive_token_lifetime_is_rejected(
    signing_key: JwtSigningKey,
    token_profile: AsymmetricTokenProfile,
    registration: WorkloadRegistration,
) -> None:
    now = datetime.now(UTC).replace(microsecond=0)
    long_profile = replace(token_profile, access_token_ttl=timedelta(minutes=11))
    token = _token(signing_key, long_profile, registration, now=now)

    with pytest.raises(WorkloadIdentityError, match="workload identity validation failed"):
        _verifier(signing_key, token_profile, (registration,)).verify(token, now=now)


@pytest.mark.parametrize(
    "scope",
    ("space-data:read space-data:read", "platform:admin", "space-data:*"),
)
def test_duplicate_unregistered_or_wildcard_scope_is_rejected(
    scope: str,
    signing_key: JwtSigningKey,
    token_profile: AsymmetricTokenProfile,
    registration: WorkloadRegistration,
) -> None:
    now = datetime.now(UTC).replace(microsecond=0)
    token = _token(signing_key, token_profile, registration, now=now, claims={"scope": scope})

    with pytest.raises(WorkloadIdentityError, match="workload identity validation failed"):
        _verifier(signing_key, token_profile, (registration,)).verify(token, now=now)


def test_wrong_issuer_or_audience_inherits_exact_asymmetric_validation(
    signing_key: JwtSigningKey,
    token_profile: AsymmetricTokenProfile,
    registration: WorkloadRegistration,
) -> None:
    now = datetime.now(UTC).replace(microsecond=0)
    token = _token(signing_key, token_profile, registration, now=now)
    wrong_profiles = (
        replace(token_profile, issuer="https://wrong.example"),
        replace(token_profile, audience="wrong-service"),
    )

    for wrong_profile in wrong_profiles:
        with pytest.raises(WorkloadIdentityError, match="workload identity validation failed"):
            _verifier(signing_key, wrong_profile, (registration,)).verify(token, now=now)


def test_registration_and_rule_catalogs_reject_ambiguity(
    signing_key: JwtSigningKey,
    token_profile: AsymmetricTokenProfile,
    registration: WorkloadRegistration,
    rules: tuple[ServiceAuthorizationRule, ...],
) -> None:
    duplicate = replace(registration, tenant_id=OTHER_TENANT_ID)

    with pytest.raises(ValueError, match="identifiers must be unique"):
        _verifier(signing_key, token_profile, (registration, duplicate))
    with pytest.raises(ValueError, match="permission-unique"):
        ServiceAuthorizationPolicy(registrations=(registration,), rules=(rules[0], rules[0]))


def test_catalog_has_no_wildcard_or_spacecraft_command_authority() -> None:
    permissions = {permission.value for permission in ServicePermission}

    assert all("*" not in permission for permission in permissions)
    assert all("command" not in permission for permission in permissions)
    assert all("uplink" not in permission for permission in permissions)
    assert all("maneuver" not in permission for permission in permissions)
