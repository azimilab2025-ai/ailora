# AILORA enterprise architecture decision register

This register records architecture decisions for the active thirty-command qualification program.
It does not duplicate implementation. `ACCEPTED_PARTIAL` means an existing foundation must be
extended; `ACCEPTED_TARGET` means the decision is approved but not yet implemented; and
`EXTERNAL_GATE` cannot be closed by repository self-attestation.

| ADR | Decision | Status | Existing foundation preserved | Remaining owner command(s) |
|---|---|---|---|---|
| ADR-001 | Advisory, human-authority-first platform with no spacecraft command path | `ACCEPTED_IMPLEMENTED_BOUNDARY` | review state, authorization and audit contracts | all commands preserve boundary |
| ADR-002 | Domain → service → API dependency direction with typed persistence | `ACCEPTED_IMPLEMENTED` | current package boundaries and repositories | regression preservation |
| ADR-003 | Shared PostgreSQL tenancy with tenant keys plus database RLS defense | `ACCEPTED_PARTIAL` | tenant-scoped models, repositories and authorization | C09, C11–C12 |
| ADR-004 | External OIDC for humans and short-lived tenant-bound workload identities for services | `ACCEPTED_TARGET` | session lifecycle and authorization foundations | C06–C09 |
| ADR-005 | Versioned `/api/v1` contracts with Problem Details, request identity, idempotency and budgets | `ACCEPTED_TARGET` | current FastAPI routers and OpenAPI | C10 |
| ADR-006 | Provider → immutable raw evidence → normalize → validate/quarantine → reconcile → trusted catalog | `ACCEPTED_PARTIAL` | CelesTrak transport, raw evidence, quarantine and provenance | C22–C23 |
| ADR-007 | Primary scientific engine plus genuinely independent reference path and conflict state | `ACCEPTED_PARTIAL` | SGP4/TCA and differential-verification contracts | C19–C25 |
| ADR-008 | Scientific Configuration Registry and immutable ScientificExecutionManifest bind every qualified run | `ACCEPTED_TARGET` | distributed configuration and provenance digests | C18–C21 |
| ADR-009 | Covariance-capable data precedes qualified encounter-plane/HBR/Pc assessment | `ACCEPTED_TARGET` | covariance-health contract | C20, C23–C25 |
| ADR-010 | Stateless web tier separated from durable scheduler/queue/workers with idempotency, DLQ and replay | `ACCEPTED_PARTIAL` | durable database workflow state machine | C26 |
| ADR-011 | HA PostgreSQL, PITR, measured restore and safe immutable artifact promotion | `ACCEPTED_TARGET` | migrations, local restore fixture, Docker/Render baseline | C11–C17, C28 |
| ADR-012 | OpenTelemetry signals, SLO/error budget and scientific disagreement metrics govern operations | `ACCEPTED_PARTIAL` | structured logging, tracing and bounded metrics | C17, C27–C29 |
| ADR-013 | Release qualification is evidence-driven, release-specific and fail-closed | `ACCEPTED_PARTIAL` | evidence pack and release manifest | C04–C05, C30 |
| ADR-014 | Independent scientific, security, legal, SRE and release decisions cannot be self-issued | `EXTERNAL_GATE` | role and gate contracts | C21–C25, C28–C30 |

## Decision lifecycle

1. An implementation command may refine an ADR without changing its core safety boundary.
2. A material alternative requires a new ADR or an explicit superseding decision; history is not
   deleted.
3. Status changes require implementation references, verification, evidence digest, reviewer and
   residual-risk disposition.
4. A design document, dependency import or test name alone cannot advance an ADR to implemented or
   qualified.
5. Scientific disagreement remains `CONFLICT` or `UNVERIFIED`; it is never silently resolved by the
   primary engine.

## Deferred product choices

Vendor, region, queue product, OIDC provider, covariance-capable source, reference engine, signing
authority and monitoring backend remain provider-neutral until their owning command performs the
required technical, legal, cost and exit analysis. Deferral is deliberate and is not approval.
