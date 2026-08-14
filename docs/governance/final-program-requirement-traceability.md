# AILORA Final Program Requirement Traceability Matrix

## Purpose

This matrix maps the 29 sections of the approved enterprise engineering
mandate to the twenty-command final program.

It is a governance baseline, not evidence that an item is implemented.
A requirement may move to a stronger status only when reproducible evidence
and its command acceptance criteria pass.

## Status vocabulary

- `VERIFIED_BASELINE`: proven by existing reproducible evidence.
- `PARTIAL`: some supporting implementation exists, but the mandate is unmet.
- `PLANNED`: assigned to a future command.
- `EXTERNAL_GATE`: requires independent review, legal input, infrastructure,
  credentials, commercial approval, or another owner decision.
- `OUT_OF_SCOPE`: intentionally prohibited or excluded.
- `BLOCKED`: cannot advance until its stated dependency is resolved.

Unknown, stale, conflicted, missing, invalid, non-converged, and indeterminate
states are never equivalent to pass.

## Section-level traceability

| ID | Mandate area | Current classification | Owning commands | Required completion evidence |
|---|---|---|---|---|
| R-01 | Mission, safety principles, advisory boundary | PARTIAL | C-02, C-04, C-10, C-14, C-20 | Architecture boundaries, policy tests, release assertions |
| R-02 | Start rules, baseline evidence, small reversible changes | VERIFIED_BASELINE | C-01, C-02, all | Clean baseline, atomic commits, checkpoints |
| R-03 | API vertical slice, readiness, secrets, coverage, roles, migrations | PARTIAL | C-03 through C-07 | Working API-to-database slice and negative tests |
| R-04 | Enterprise architecture and ADRs | PLANNED | C-02, C-03, C-04, C-13, C-19 | ADR pack, trust boundaries, dependency direction |
| R-05 | Typed and versioned space-data contracts | PARTIAL | C-08, C-10, C-11 | Schema compatibility and semantic validation tests |
| R-06 | Space-object identity and data quality | IMPLEMENTED | C-08, C-09 | Provenance, quarantine, deduplication, replay evidence |
| R-07 | Astrodynamics and scientific computing | PARTIAL | C-10 through C-12 | Golden cases, tolerances, scientific limitation labels |
| R-08 | Qualified real-data connection | EXTERNAL_GATE | C-09 | Provider qualification, license, provenance, outage tests |
| R-09 | Oya and agentic integration | PARTIAL | C-14 | Disabled-by-default adapter, safety tests, benchmark report |
| R-10 | Workflows, events, and state machines | PARTIAL | C-07, C-13 | Invalid-transition, retry, duplicate and race tests |
| R-11 | API engineering | PARTIAL | C-06, C-13, C-15 | Versioned OpenAPI, error envelope, limits and failure tests |
| R-12 | Enterprise SaaS and multi-tenancy | PARTIAL | C-04 through C-07, C-13 | Cross-tenant denial and lifecycle evidence |
| R-13 | Security and Zero Trust | PARTIAL | C-04, C-06, C-14, C-17, C-20 | Threat model, security gates, residual-risk record |
| R-14 | Software supply-chain security | PARTIAL | C-17, C-20 | Scans, SBOM, provenance, signing and immutable artifacts |
| R-15 | Observability and immutable audit | PARTIAL | C-07, C-15 | Metrics, traces, redaction and tamper-evidence tests |
| R-16 | Reliability, SRE, and failure engineering | PARTIAL | C-03, C-13, C-15, C-16 | SLOs and bounded failure-injection evidence |
| R-17 | Performance and capacity | PLANNED | C-16 | Reproducible benchmark and regression thresholds |
| R-18 | Backup, disaster recovery, continuity | PLANNED | C-18, C-19 | Restore drill, RPO/RTO and recovery runbook |
| R-19 | Privacy, governance, and compliance | PLANNED | C-18, C-19 | Data inventory, retention and external legal gates |
| R-20 | Verification hierarchy | PARTIAL | C-05 through C-20 | Classified test evidence and independent verification |
| R-21 | Deployment and environment strategy | PARTIAL | C-03, C-17, C-19, C-20 | Promotion, smoke, rollback and deployment evidence |
| R-22 | Final documentation and truthful README | PARTIAL | C-18 through C-20 | Documentation-to-implementation reconciliation |
| R-23 | Ten-year maintainability | PARTIAL | C-03 through C-20 | Typed interfaces, boundaries, ownership and policy evidence |
| R-24 | FinOps and bounded cost | PLANNED | C-14, C-16, C-19 | Budgets, quotas, attribution and kill-switch evidence |
| R-25 | Definition of Done | PLANNED | C-02, all | Per-command acceptance records and checkpoints |
| R-26 | Final release gate | PLANNED | C-20 | Machine-verifiable release-readiness decision |
| R-27 | Required evidence deliverables | PLANNED | C-02 through C-20 | Evidence index and machine-readable manifest |
| R-28 | Atomic execution and explicit authorization | VERIFIED_BASELINE | C-02, all | Scope validation, rollback and authority markers |
| R-29 | Final evidence-based mandate | PLANNED | C-20 | Truthful final status and known-limitations register |

## Current verified baseline

The following facts were reproduced by Command 01:

- Branch `main` at commit
  `159a8c698943b54c61a29955305ad02661ba0f62`.
- Clean working tree.
- 376 tests passed with 97 percent statement coverage.
- Ruff format, Ruff lint, strict Mypy, package build, dependency audit,
  Alembic graph and Docker Compose configuration passed.
- No known dependency vulnerability was reported.
- OpenAPI exposes only `/health/live` and `/health/ready`.
- No operational non-health vertical slice exists.
- `cov-fail-under=0` remains configured.
- Configuration environment is currently typed as `str`.
- A proprietary license declaration exists in `pyproject.toml`.
- No tracked `LICENSE`, `NOTICE`, `LICENCE`, or `COPYING` file exists.

## Permanent exclusions

The following are `OUT_OF_SCOPE` for every command:

- Spacecraft command, telecommand, uplink, flight-control execution, or
  autonomous maneuver execution.
- Connecting advisory output directly to an operational execution path.
- Allowing AI, Oya, a model, agent, or tool to become physical truth,
  approval authority, or release authority.
- Printing or persisting secrets, raw chain-of-thought, or unauthorized
  sensitive data.
- Activating paid services, deployment, purchase, destructive action, or
  remote publication without explicit owner authorization.

## External release gates

The following cannot be satisfied by repository code alone:

- Independent astrodynamics review.
- Legal review of third-party data and commercial software licensing.
- Privacy and data-residency legal determination.
- Penetration testing by an authorized independent party.
- Production-like staging soak evidence.
- Backup restore drill against the selected managed infrastructure.
- Formal human release-authority approval.

Absent external evidence must remain `BLOCKED` or `EXTERNAL_GATE`; it must
never be converted to `PASS`.
