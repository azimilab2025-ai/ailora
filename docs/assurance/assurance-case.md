# AILORA formal assurance case baseline

Status: `SKELETON_BLOCKED_PENDING_IMPLEMENTATION_EVIDENCE_AND_INDEPENDENT_REVIEW`

## Top-level claim

`CLAIM-001`: AILORA provides trustworthy, human-authority-first orbital decision support within
its declared release and scientific scope.

The claim is not accepted at this baseline. This document defines the argument structure and
evidence obligations that every later command must satisfy.

## Argument structure

| Sub-claim | Argument | Current disposition |
|---|---|---|
| `CLAIM-002` Human authority | deterministic authorization/review/audit boundaries prohibit model or command authority | partial repository evidence; final audit required |
| `CLAIM-003` Identity and tenancy | short-lived identity, resource/action/scope authorization and DB isolation prevent cross-tenant access | OIDC/workload/RLS/pentest open |
| `CLAIM-004` Space data | qualified sources, immutable raw evidence, freshness, poisoning defense and conflict states preserve data trust | legal/multi-source/covariance source/shadow open |
| `CLAIM-005` Scientific validity | complete semantics, covariance, independent engine/corpus, encounter plane/HBR/Pc and tolerances bound results | major implementation and IV&V gates open |
| `CLAIM-006` Workflow reliability | durable idempotent bounded work with DLQ/backpressure/replay prevents duplicate or silent effects | queue/worker production evidence open |
| `CLAIM-007` Security/supply chain | defense-in-depth controls and signed provenance protect runtime and release artifacts | scanners/signing/pentest open |
| `CLAIM-008` Operations/recovery | measured SLO, capacity, HA, failover, restore, RTO/RPO and shadow operation prove service commitments | production-like environment open |
| `CLAIM-009` Reproducibility | immutable configuration, runtime, data and evidence manifests reproduce historical analyses | unified registry/manifest/drift controls open |
| `CLAIM-010` Release assurance | traceability, independent approvals and accepted residual risks bind the exact release decision | final gate open |

## Evidence acceptance rule

A claim can advance only when it has:

1. implementation linked to requirement and architecture decision;
2. positive, negative, isolation, failure and regression verification appropriate to the claim;
3. immutable/versioned evidence bound to the exact commit, artifact, runtime, data and configuration;
4. qualified reviewer identity, scope, date, decision and evidence digest;
5. explicit residual-risk disposition by authorized human authority.

File existence, test count, coverage, dashboard presence, a passing self-authored report or a
release label alone is insufficient.

## Defeaters that block acceptance

- Missing/stale/conflicted evidence or mismatched release/runtime/configuration identity.
- Open critical/high risk without explicit authorized acceptance and compensating control.
- Scientific disagreement, unavailable verifier or unsupported validity domain.
- Missing provider/legal approval, penetration test, HA/DR/SLO evidence or shadow qualification.
- Reviewer conflict of interest or self-issued independent approval.
- Any spacecraft command/uplink path or AI authority escalation.

## Machine-readable binding

- Claims: `docs/assurance/claims.json`
- Threats: `docs/assurance/threat-model.md`
- Hazards: `docs/assurance/hazards.md`
- Risks: `docs/assurance/risk-register.json`
- Evidence digests: `docs/assurance/evidence-index.json`
- Requirements: `docs/governance/enterprise-requirements-traceability.json`
- Release scope and authority: `docs/governance/release-scope-and-authority.md`

## Release rule

`SKELETON_BLOCKED_PENDING_IMPLEMENTATION_EVIDENCE_AND_INDEPENDENT_REVIEW` remains until every
applicable P0 claim has accepted evidence, every external review is recorded, residual risks are
accepted or closed, and the human Release Authority signs the exact release manifest. No override
may weaken the permanent no-command or human-authority boundary.
