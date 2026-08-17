# AILORA Final Twenty-Command Execution Plan

> Historical baseline: this plan records the completed twenty-command foundation. It is preserved for audit history and is not the active thirty-command enterprise qualification map. Current scope and ownership are defined by [`enterprise-requirements-traceability.json`](../governance/enterprise-requirements-traceability.json), [`enterprise-adr-register.md`](enterprise-adr-register.md) and [`release-scope-and-authority.md`](../governance/release-scope-and-authority.md).

## Program objective

Advance AILORA from its verified foundation to the strongest defensible
enterprise production candidate supported by actual implementation and
evidence.

The program does not promise `PRODUCTION_READY` or `OPERATIONAL`.
Those labels require external gates, stable production-like staging and formal
human release authority.

## Non-negotiable execution rules

Every implementation command must:

1. verify branch, baseline commit and clean scope;
2. state risk, dependency, rollback and acceptance criteria;
3. add or strengthen tests before claiming completion;
4. preserve unrelated user work;
5. use an atomic conventional commit;
6. create or update command evidence;
7. avoid remote, paid, production or destructive actions without approval;
8. report failure rather than weakening a gate;
9. preserve the advisory-only and human-authority boundaries;
10. avoid unsupported scientific or production claims.

## Ordered command map

| ID | Work package | Principal deliverable | Completion gate |
|---|---|---|---|
| C-01 | Read-only current-state and license audit | Reproduced baseline and gap surface | PASS at commit `159a8c6` |
| C-02 | Traceability, risks and execution governance | RTM, risk register and ordered plan | Four-document atomic commit |
| C-03 | Configuration, secrets, database lifecycle, readiness | Fail-closed typed runtime foundation | Startup, outage and recovery tests |
| C-04 | Authorization, tenant isolation and threat-model baseline | Deny-by-default policy layer | IDOR and cross-tenant negative tests |
| C-05 | Persistent enterprise vertical-slice domain | Scenario, data, screening, review, evidence persistence | Migration and repository tests |
| C-06 | Versioned vertical-slice API | Authorized create/process/retrieve API | OpenAPI, integration and failure tests |
| C-07 | Human review state machine and immutable audit | Approval/reject/defer workflow | Invalid-transition, race and tamper tests |
| C-08 | Space-data contracts, provenance and quarantine | Typed/versioned semantic data layer | Frame/unit/time/freshness contract tests |
| C-09 | Qualified provider adapter and real-data governance | Provider boundary, raw storage and qualification report | License gate and outage simulations |
| C-10 | Primary astrodynamics adapter | Versioned physics-first computation boundary | Golden and deterministic tests |
| C-11 | TCA, covariance, uncertainty and safe scientific labels | Scientifically bounded risk result | Numerical and non-convergence tests |
| C-12 | Independent verification | Differential engine and conflict state | Cross-engine tolerance evidence |
| C-13 | Durable workflows and events | Idempotent stateful processing | Retry, duplicate, cancellation and replay tests |
| C-14 | Oya qualification and agent safety | Disabled-by-default advisory adapter and benchmark | Injection, isolation, budget and fallback tests |
| C-15 | Operational observability, audit and SRE | Metrics, traces, redaction and SLO definitions | Failure observability and secret-safety tests |
| C-16 | Performance, capacity and FinOps | Reproducible benchmark and budgets | p50/p95/p99, throughput and cost thresholds |
| C-17 | DevSecOps and supply chain | Hardened CI, SBOM, provenance and signing policy | Security scanners and artifact evidence |
| C-18 | Backup, DR, privacy, LICENSE and NOTICE | Recovery/governance/legal documentation package | Restore evidence or explicit external blocker |
| C-19 | Staging, deployment, rollback, runbooks and final docs | Truthful production-candidate documentation | Smoke/rollback evidence or external blocker |
| C-20 | Final evidence pack and release gate | Manifest, limitations, residual risks and decision | Fail-closed machine-readable final status |

## License commitment

License work is mandatory and owned by `C-18`.

Before any public or commercial release, C-18 must:

- reconcile `pyproject.toml` proprietary metadata with an actual tracked
  `LICENSE` file;
- create or justify `NOTICE`;
- inventory third-party packages, data, models, SDKs and Oya terms;
- distinguish repository copyright from third-party rights;
- record redistribution and attribution obligations;
- require specialist Software/IP legal review before commercial reliance.

Until that review exists, the license status remains
`EXTERNAL_GATE:LEGAL_REVIEW_REQUIRED`.

## Scientific completion boundary

Commands C-10 through C-12 may implement and test scientific software, but
independent astrodynamics approval cannot be self-issued.

If independent evidence is unavailable at C-20:

- implementation evidence may pass;
- scientific release approval remains blocked;
- no operational-risk-engine claim may be made.

## External-action boundary

Remote push, PR creation, deployment, paid provider activation, production
migration, signing with production keys and public publication require a
separate explicit authorization at the command that needs them.
