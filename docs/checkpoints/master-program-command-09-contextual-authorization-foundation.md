# AILORA Command 09 — Contextual Authorization and Privilege Boundaries

Baseline: `589700693382b9f4cb5955de4b36732347a2f3e5`

## Status

`OFFLINE_CONTEXTUAL_POLICY_IMPLEMENTED_DISABLED_FROM_RUNTIME_ROUTING`

This command adds a fail-closed, provider-neutral contextual policy evaluator. It extends the
existing tenant and workload foundations without modifying API routes, repositories, database
schema, deployment configuration or Render services.

## Implemented contract

- Closed, code-reviewed permission-to-resource/action mappings without wildcards.
- Strict separation of human and workload actor classes.
- Exact reconciliation of requested tenant, resource tenant, grant tenant and trusted membership tenant.
- Principal, purpose, classification, object and correlation context bound into each decision.
- Policy-version fencing for immediate stale-grant invalidation.
- Fresh tenant, identity and session/credential state rechecked before every allowed effect.
- Maximum eight-hour human and fifteen-minute workload authentication/grant boundaries.
- Recent MFA required for privileged review decisions and membership administration.
- Workloads prohibited from human-only privileged contracts.
- Ambient or implicit delegation rejected until a dedicated delegation contract exists.
- Optional object-level grant constraints to prevent lateral resource access.
- Auditable allow decision with grant, principal, tenant, resource, permission and policy version.
- No spacecraft-command, uplink, telecommand or maneuver permission/action.

## Verification

Tests exercise valid human and workload decisions, every tenant mismatch, trusted-membership
reconciliation, principal/actor substitution, permission-resource-action mismatches, purpose and
classification ceilings, stale policy versions, inactive tenant/identity/credential state, revoked
and expired grants, authentication freshness, privileged MFA freshness, workload privilege
escalation, ambient delegation, object constraints, lifetime validation and catalog ambiguity.

## Remaining runtime and external gates

- Explicit middleware and repository integration at every protected effect.
- Durable policy, membership, revocation and audit state with transactional enforcement.
- Approved policy-administration workflow and separation of duties.
- Production monitoring, alerting and revocation-latency evidence.
- Production tenant credential and controlled authenticated end-to-end qualification.
- Independent privilege-boundary review and final release acceptance.

ENT-004 remains `PARTIAL`; an offline policy test is not production authorization evidence.
