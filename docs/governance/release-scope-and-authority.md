# AILORA release scope and authority baseline

Status: `ACTIVE_QUALIFICATION_BASELINE`

This document defines the declared scope, decision ownership and release boundary for the
thirty-command enterprise qualification program. It is a governance contract, not evidence that
future controls are implemented or that an external gate has passed.

## Declared product scope

AILORA is an advisory orbital decision-support platform. Its declared scope includes tenant-aware
scenario intake, proximity screening, bounded astrodynamics analysis, scientific provenance,
independent-verification states, human review, audit evidence and governed space-data ingestion.

The currently implemented foundation is preserved and extended. `PARTIAL`, `TARGET` and
`EXTERNAL_GATE` capabilities are never rebuilt or relabelled as complete merely because a design,
test, dashboard or source file exists.

## Permanent safety boundary

- Human authority remains mandatory for review, risk acceptance and release.
- No spacecraft command, uplink, telecommand, flight-control or autonomous-maneuver execution
  surface is permitted.
- AI/Oya remains advisory and cannot authorize access, alter scientific truth or approve release.
- Proximity severity is not collision probability and must never be presented as Pc.
- Missing, stale, conflicted, unverified or unavailable evidence is not PASS.
- A production label is release-specific and applies only to the approved scope, version, runtime,
  data sources and evidence snapshot.

## Current verified boundary

At baseline commit `59d0fbc55e9e1b50fe1877af382df382602ae54a`, the public status is
`PRODUCTION_CANDIDATE_ACTIVE_QUALIFICATION`. The provider-to-GCRF engineering path is deployed,
while the controlled authenticated tenant-scoped production E2E remains
`DEFERRED_REQUIRED_BEFORE_FINAL_RELEASE`.

The existing SGP4/TEME, bounded TCA, covariance-health, provider-governance, frame-transform,
tenant, workflow, audit, observability, CI and container foundations remain authoritative within
their declared limitations. None of those foundations independently proves scientific approval,
HA, DR, production SLO, provider legality, penetration-test acceptance or shadow qualification.

## Target release claim

Only after every applicable P0 release gate has immutable evidence and accepted residual risk may
the Release Authority approve the declared version as an enterprise production-grade advisory
orbital decision-support release. Flight certification and any spacecraft-command capability
remain outside that claim.

## Qualification dimensions

| Dimension | Required final evidence | Default when incomplete |
|---|---|---|
| Software correctness | implementation, tests, artifact identity and reviewed evidence | `NOT_QUALIFIED` |
| Scientific validity | bounded validity domain, independent corpus/engine/reviewer and signed evidence | `UNVERIFIED` |
| Security | threat evidence, hardened controls, authorized independent assessment and accepted findings | `NOT_SECURITY_QUALIFIED` |
| Data/provider | legal and technical qualification, provenance, freshness, conflict and outage evidence | `PROVIDER_UNQUALIFIED` |
| Reliability | measured SLO, capacity, HA, failover, restore, RTO and RPO evidence | `NOT_OPERATIONALLY_PROVEN` |
| Release assurance | traceability, assurance case, immutable manifest, approvals and residual-risk acceptance | `RELEASE_BLOCKED` |

## Decision roles and separation

| Role | Accountable decision | Cannot self-approve |
|---|---|---|
| Developer | implementation and developer verification | independent scientific/security acceptance |
| Scientific Verifier | validity domain, corpus, tolerances and scientific disagreements | own implementation as sole authority |
| Security Assessor | security scope, findings and closure evidence | release by ignoring an open critical finding |
| Data Governance / Legal Reviewer | provider rights, retention, jurisdiction and legal findings | scientific or production reliability claims |
| SRE / Operations Reviewer | SLO, capacity, HA, DR, rollback and operational evidence | scientific validity |
| Release Authority | scope-specific release decision and residual-risk acceptance | evidence requirements or permanent safety boundaries |

An individual may perform multiple roles during development, but a final independent gate requires
organizationally independent evidence and identity. Repository authorship alone cannot satisfy an
independent gate.

## Exception contract

Every exception requires an identifier, exact scope, owner, rationale, compensating control,
creation date, expiration date, affected requirements, evidence references and explicit risk
acceptance. Exceptions cannot authorize spacecraft command paths, silently convert missing evidence
to PASS or permanently waive a P0 gate.

## Active assurance artifacts

Threats, hazards, risks, claims and evidence digests are bound through [`docs/assurance/assurance-case.md`](../assurance/assurance-case.md). The current status is `SKELETON_BLOCKED_PENDING_IMPLEMENTATION_EVIDENCE_AND_INDEPENDENT_REVIEW`; creation of the assurance structure does not close any external gate.

## Release decision rule

The Release Authority may choose `APPROVE`, `REJECT` or `DEFER`. `APPROVE` is valid only when the
release manifest identifies the exact artifact, runtime, scientific configuration, data snapshot,
evidence digests, independent approvals and residual risks. Any unresolved blocker forces
`REJECT` or `DEFER`.
