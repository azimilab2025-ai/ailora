# AILORA Command 08 — Tenant-Bound Workload Identity Foundation

Baseline: `177278c089aa10b82133e3b00e9d50c13913e837`

## Status

`OFFLINE_FOUNDATION_IMPLEMENTED_DISABLED_FROM_RUNTIME_ROUTING`

This command adds a provider-neutral verification and authorization boundary for short-lived
OAuth client-credentials access tokens. It does not configure an identity provider, create a
production tenant credential, implement a live token endpoint, store a client secret or activate
runtime authentication routing.

## Implemented contract

- Exact RS256 issuer and audience validation through the bounded asymmetric-token foundation.
- Mandatory `sub`, `client_id`, `azp`, `tenant_id`, `gty=client_credentials`,
  `token_use=access`, `scope`, `iat`, `exp` and UUID `jti` semantics.
- Current workload registration binding across workload subject, OAuth client and tenant.
- Explicit allowlisted scopes and service permissions without wildcard authorization.
- Maximum fifteen-minute configured lifetime and maximum thirty-second clock skew.
- Human-identity claim rejection to keep users and workloads distinct.
- Exact tenant, permission, resource and action checks against a current authorization rule.
- Registration revocation recheck at authorization time.
- Auditable authorization context carrying workload, client, tenant and token identifiers.
- Permanent absence of spacecraft-command, uplink, telecommand or maneuver authority.

## Verification

The contract suite covers valid client-credentials tokens, issuer and audience pinning,
client/tenant/authorized-party mismatches, wrong grant and token use, human-claim smuggling,
inactive or unregistered workloads, excessive lifetime, duplicate/unregistered/wildcard scopes,
cross-tenant confused-deputy attempts, resource/action substitution, scope-plus-permission checks,
revocation rechecks and ambiguous catalog rejection.

## Remaining external and runtime gates

- Approved authorization server or tenant identity-provider configuration.
- Protected client authentication and credential/key custody with rotation evidence.
- Durable registration, revocation, replay and audit persistence.
- Explicit runtime middleware/route integration and staged deployment acceptance.
- Production tenant credential and controlled authenticated end-to-end qualification.
- Command 09 contextual authorization and privilege-boundary hardening.

No source-code test can self-attest those operational gates. ENT-004 therefore remains `PARTIAL`.
