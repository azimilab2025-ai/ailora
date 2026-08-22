# Partial residual matrix (honest)

<!-- AILORA_PARTIAL_RESIDUAL_MATRIX_V1 -->

Generated: 2026-08-22T10:37:48Z

Status policy: all rows remain **PARTIAL**. Local evidence does not equal production/live qualification.
Excluded from this close-out wave: OYA activation, real-email tenant E2E.

| ID | Title | Bucket | Notes |
|----|-------|--------|-------|
| ENT-002 | Release-specific traceability assurance and decision authority | LOCAL_EVIDENCE_PRESENT_LIVE_GATE_OPEN | Complete assurance case evidence index independent approvals and accepted residual risk. |
| ENT-003 | OIDC MFA asymmetric JWT JWKS and hardened sessions | NEEDS_LIVE_OR_IDP_INFRA | Complete authorization-code exchange, account linking, MFA enrollment, durable replay-state integration, protected produ |
| ENT-004 | Tenant-bound workload identity and contextual authorization | NEEDS_LIVE_OR_IDP_INFRA | Integrate an approved authorization server, protected client authentication, durable registration/policy/revocation stat |
| ENT-007 | PITR restore RTO RPO and disaster recovery | NEEDS_LIVE_OR_IDP_INFRA | Define approved recovery objectives through business impact analysis, provision a PITR-capable managed PostgreSQL topolo |
| ENT-009 | Runtime and edge security hardening | LOCAL_EVIDENCE_PRESENT_LIVE_GATE_OPEN | Add SSRF egress secret manager headers rate limits read-only runtime and edge controls. |
| ENT-010 | OpenTelemetry SLO alerts error budget and synthetic monitoring | NEEDS_LIVE_OR_IDP_INFRA | Wire end-to-end signals dashboards alerts burn policy scientific metrics and synthetics. |
| ENT-012 | Time scales EOP leap seconds frames and ITRF qualification | LOCAL_EVIDENCE_PRESENT_LIVE_GATE_OPEN | Obtain independently sourced truth vectors, execute independent scientific review, and accept release-specific tolerance |
| ENT-013 | Covariance propagation transformation and quality controls | LOCAL_EVIDENCE_PRESENT_LIVE_GATE_OPEN | Add propagation Jacobian frame/epoch transformation conditioning staleness and correlation policy. |
| ENT-014 | Independent scientific engine corpus and complete TCA search | LOCAL_EVIDENCE_PRESENT_LIVE_GATE_OPEN | Add executable independent path independent corpus common-mode map and multiple-minimum recall evidence. |
| ENT-015 | Provider legal technical freshness poisoning and outage qualification | LOCAL_EVIDENCE_PRESENT_LIVE_GATE_OPEN | Complete legal status freshness taxonomy poisoning defense change monitoring and qualification evidence. Local minimal e |
| ENT-019 | Durable queue scheduler workers DLQ backpressure and replay | MIXED_LOCAL_TYPES_PLUS_LIVE_OPS | Split web/workers and add durable broker scheduler DLQ priority backpressure cancellation and redundancy. Local minimal  |
| ENT-020 | Capacity fault injection soak scientific telemetry and cost guardrails | MIXED_LOCAL_TYPES_PLUS_LIVE_OPS | Run representative capacity 100k-object recall failure soak and cost evidence. Local minimal evidence surface (capacity, |
| ENT-021 | Multi-instance HA staging parity rollout rollback and failover | MIXED_LOCAL_TYPES_PLUS_LIVE_OPS | Qualify redundant web/workers database failover parity rollout rollback and outage behavior. Local minimal evidence surf |

## Bucket legend
- **LOCAL_EVIDENCE_PRESENT_LIVE_GATE_OPEN**: contracts/types/tests exist; independent review or live drill still open.
- **MIXED_LOCAL_TYPES_PLUS_LIVE_OPS**: evidence types present; broker/HA/soak live ops not claimed COMPLETE.
- **NEEDS_LIVE_OR_IDP_INFRA**: requires real IdP/MFA, PITR measured, or production telemetry wiring.

No status flipped to COMPLETE by this document.

