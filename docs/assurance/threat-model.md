# AILORA enterprise threat model

Status: `ACTIVE_BASELINE_NOT_INDEPENDENTLY_ASSESSED`

This model applies STRIDE and explicit abuse cases to the declared advisory platform. It records
security work and evidence ownership; it does not claim that future controls, a penetration test or
an independent security review have passed.

## Scope and trust zones

| Zone | Assets | Trust boundary |
|---|---|---|
| Edge/API | TLS requests, rate budgets, request identity | Internet → gateway/application |
| Identity | human sessions, tenant membership, roles, workload identity | IdP/token issuer → application |
| Application | scenarios, screenings, reviews, authorization context | API → domain/service layer |
| Workflow | jobs, retries, cancellation, replay, DLQ | web → durable broker/workers |
| Space data | raw payloads, provenance, normalized catalog, conflicts | provider/egress → ingest boundary |
| Scientific | states, frames, time, covariance, TCA, Pc configuration | data pipeline → scientific workers |
| Verification | reference results, tolerances, disagreement state | primary engine → independent verifier |
| Data/evidence | tenant records, audit, evidence digests, backups | application roles → database/object store |
| Delivery | source, CI, dependencies, SBOM, images, signatures | developer/CI → artifact/runtime |
| Observability | logs, metrics, traces, alerts | workloads → telemetry/SIEM |
| AI/Oya | prompts, model output, allowlisted advisory tools | untrusted content/model → deterministic controls |

## Protected assets

- Tenant identity, membership, authorization decisions and session state.
- Raw provider evidence, provenance, normalized catalog and scientific input lineage.
- Scientific configuration, frame/time metadata, covariance, TCA and future Pc results.
- Human reviews, append-only audit history, release evidence and residual-risk decisions.
- Production credentials, signing identities, database access and deployment authority.
- Availability, compute budgets, queue integrity, SLO evidence and incident records.

## Threat and abuse-case register

| ID | STRIDE | Threat / abuse case | Required control and safe response | Detection / evidence | Owner commands |
|---|---|---|---|---|---|
| THR-001 | Spoofing / Elevation | Forged, replayed or wrong-audience human token | asymmetric validation, issuer/audience/kid/jti, short TTL, revocation; deny | auth telemetry and negative token corpus | C06–C07 |
| THR-002 | Elevation / Information disclosure | BOLA/IDOR or forged tenant context crosses isolation boundary | resource-action-scope authorization, tenant binding, RLS; deny | cross-tenant tests, deny metrics, pentest | C08–C11, C30 |
| THR-003 | Spoofing / Elevation | User credential reused as workload identity or shared service secret | dedicated short-lived tenant-bound service identity; revoke | workload identity inventory and token-use alerts | C08, C29 |
| THR-004 | Tampering / Information disclosure | Provider URL manipulation, SSRF, redirect or DNS rebinding reaches internal network | allowlist, TLS, no redirects, resolved-IP policy, egress proxy, byte/time bounds; quarantine | egress logs and SSRF corpus | C16, C22 |
| THR-005 | Tampering | Malformed or poisoned orbital data changes screening outcome | immutable raw capture, schema/range/anomaly checks, source conflict state; reject/quarantine | digest, anomaly metrics and replay | C22–C23 |
| THR-006 | Tampering / Repudiation | Raw payload, normalized state, audit record or evidence digest is altered | append-only roles, content addressing, signed batches/WORM where applicable; block release | integrity verification and tamper alert | C11, C15, C30 |
| THR-007 | Tampering | Frame, epoch, time scale, EOP, constants or units are silently substituted | mandatory typed semantics and execution manifest; fail closed | configuration drift and cross-engine evidence | C18–C21 |
| THR-008 | Tampering / Repudiation | Primary and reference engines share a hidden common-mode dependency or disagreement is suppressed | independence map, separate configuration/corpus, explicit conflict state; unverified | differential report and reviewer sign-off | C21, C24–C25 |
| THR-009 | Tampering / Denial of service | Duplicate, reordered or unbounded retry jobs create inconsistent effects or queue exhaustion | idempotency, fencing, retry budget, DLQ, backpressure; reject/defer | queue depth, duplicate and replay tests | C10, C26–C27 |
| THR-010 | Elevation / Repudiation | Database owner/app role bypasses tenant or audit restrictions | least-privilege roles, RLS, immutable audit constraints; deny | DB-role tests and audit integrity checks | C11–C12 |
| THR-011 | Tampering / Elevation | Dependency, CI action, base image or built artifact is compromised | pins, scans, SBOM/VEX, isolated build, signature and provenance admission; block | CI evidence and digest verification | C14–C15 |
| THR-012 | Information disclosure / Repudiation | Password, token, authorization header, tenant-sensitive input or secret enters telemetry | structured allowlist/redaction and retention policy; drop sensitive field | canary-secret tests and SIEM review | C16–C17 |
| THR-013 | Elevation / Tampering | Prompt injection or model output attempts authorization, deployment, secret access or scientific override | allowlisted advisory tools, deterministic authorization, no command/deploy path; refuse | injection corpus and tool-call audit | C16, C30 |
| THR-014 | Repudiation / Elevation | Release authority ignores missing evidence, rewrites status or accepts expired exception | immutable manifest, deny-overrides gate, separation of duties; defer/reject | evidence integrity audit and approval digest | C05, C15, C30 |
| THR-015 | Denial of service | Request, provider burst, scientific workload, database or telemetry saturation exhausts capacity | budgets, quotas, timeouts, queue backpressure, autoscaling policy and degradation | saturation signals, load/soak/fault evidence | C10, C17, C26–C29 |

## Explicit prohibited transitions

- Unauthenticated or cross-tenant request → protected resource.
- Unverified provider payload → trusted catalog without validation and provenance.
- Missing/stale EOP or mixed frame/time state → qualified scientific result.
- Verifier unavailable/disagreed → verified/pass state.
- AI/model proposal → authorization, deployment, scientific truth or release approval.
- Missing evidence or open critical finding → production approval.
- Advisory result → spacecraft command, uplink, telecommand or autonomous maneuver execution.

## Assessment boundary

Repository tests may validate deterministic controls, but `ACTIVE_BASELINE_NOT_INDEPENDENTLY_ASSESSED`
remains until an authorized independent assessor tests the release-specific identity, tenant,
provider, runtime, CI/CD and operational surfaces and the Release Authority accepts the findings.
