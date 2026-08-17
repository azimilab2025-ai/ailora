# AILORA hazard analysis baseline

Status: `ACTIVE_BASELINE_DOMAIN_AND_IVV_REVIEW_REQUIRED`

This analysis combines FMEA/FMECA-style failure modes with STPA-inspired unsafe control actions.
It defines safe states and evidence ownership; it is not an independent scientific or safety
approval.

## Unacceptable losses

| Loss | Description |
|---|---|
| LOSS-001 | Human decision is materially misled by incorrect, stale, ambiguous or overclaimed orbital analysis. |
| LOSS-002 | Tenant-confidential data or authority crosses a tenant/security boundary. |
| LOSS-003 | Scientific, audit or release evidence becomes unreproducible, incomplete or tampered. |
| LOSS-004 | Required advisory capability is unavailable or silently degraded during the declared operating scope. |
| LOSS-005 | A release is approved beyond its evidence, validity domain, runtime, provider or residual-risk scope. |

## System safety constraints

- `SC-001`: Every analysis carries complete source, frame, epoch, time-scale, unit and configuration lineage.
- `SC-002`: Stale, malformed, conflicting or unqualified data is explicitly degraded, quarantined or rejected.
- `SC-003`: Distance/proximity severity is never presented as collision probability.
- `SC-004`: Invalid covariance or unsupported geometry cannot produce qualified Pc.
- `SC-005`: Verifier disagreement or absence cannot silently become PASS.
- `SC-006`: Tenant/resource/action/scope authorization is enforced outside AI and at persistence boundaries.
- `SC-007`: Retry/replay is idempotent, bounded and evidence-linked.
- `SC-008`: Recovery and availability claims require measured restore/failover/SLO evidence.
- `SC-009`: Release approval requires immutable evidence, independent reviews and accepted residual risk.
- `SC-010`: No spacecraft command, uplink, telecommand or autonomous maneuver execution path exists.

## Hazard and failure-mode register

| ID | Hazard / causal condition | Severity | Required safe state | Detection and closure evidence | Owner commands |
|---|---|---|---|---|---|
| HAZ-001 | Stale or unqualified provider data is treated as current truth | CRITICAL | `DEGRADED`, `QUARANTINED` or `BLOCKED` | acquisition/epoch freshness, qualification and shadow comparison | C22–C23, C29 |
| HAZ-002 | States with different frames, origins, epochs, units or time scales are combined | CRITICAL | reject before arithmetic | typed semantic validation and independent reference vectors | C18–C21 |
| HAZ-003 | Missing, stale or substituted EOP/leap-second data changes transformation without lineage | HIGH | bounded cache with label or block | dataset digest, age policy, replay after final EOP | C18–C19 |
| HAZ-004 | Covariance is invalid, ill-conditioned, stale, misframed or incorrectly propagated | CRITICAL | no qualified uncertainty/Pc result | PSD/conditioning/Jacobian/transform corpus | C20, C23–C25 |
| HAZ-005 | TCA search misses a material minimum or reports a non-converged point as valid | CRITICAL | `UNVERIFIED` or `BLOCKED` | multi-minima/edge/recall corpus and cross-engine report | C21, C29 |
| HAZ-006 | Encounter-plane/Pc assumptions fail for slow, long-duration, nonlinear or degenerate encounter | CRITICAL | method-specific rejection or qualified alternative | validity-domain classifier, reference and Monte Carlo evidence | C24–C25 |
| HAZ-007 | HBR lacks provenance or is silently defaulted | HIGH | no qualified Pc | HBR policy/version/source evidence | C24–C25 |
| HAZ-008 | Proximity severity is interpreted as collision probability or operational decision | CRITICAL | explicit semantic separation and human review | API/UI contract tests and reviewer evidence | C25, C29 |
| HAZ-009 | Independent verifier is unavailable, shares common-mode faults or materially disagrees | CRITICAL | `UNVERIFIED` or `CONFLICT` | independence map, disagreement telemetry and sign-off | C21, C25, C29 |
| HAZ-010 | Duplicate, delayed or replayed workflow produces repeated or inconsistent effects | HIGH | idempotent no-op, defer or DLQ | race/replay/fencing/failure evidence | C10, C26–C27 |
| HAZ-011 | Tenant authorization or database policy permits cross-tenant observation/mutation | CRITICAL | deny and alert | negative isolation, RLS and independent pentest evidence | C08–C11, C30 |
| HAZ-012 | Provider/scientific/audit evidence is overwritten or cannot be reproduced | CRITICAL | block qualification/release | content digests, immutable retention and replay | C11, C18, C22–C23, C30 |
| HAZ-013 | Capacity exhaustion or dependency outage creates silent partial analysis | HIGH | explicit degraded/blocked result with no false success | budgets, queue/fault/soak and SLO evidence | C17, C26–C29 |
| HAZ-014 | Backup exists but restore, PITR, RTO or RPO is not proven | HIGH | no recovery/HA claim | isolated restore and failover drill | C13, C28–C29 |
| HAZ-015 | Open critical risk, missing review or expired exception is overridden at release | CRITICAL | release `DEFER` or `REJECT` | assurance/evidence audit and signed human decision | C05, C30 |

## Unsafe control actions

The system must not provide a verified/qualified label when required provenance, configuration,
covariance, independent verification or evidence is missing. It must not omit a stale/conflict
warning, apply an approval to the wrong tenant/version/scope, continue after revocation, or allow an
AI/model to replace deterministic controls or human authority.

## Review rule

Severity or status may change only with linked implementation, verification, immutable evidence,
qualified review and residual-risk disposition. `ACTIVE_BASELINE_DOMAIN_AND_IVV_REVIEW_REQUIRED`
cannot be promoted by the author of this document alone.
