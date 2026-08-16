# AILORA Final Program Risk Register

## Scoring

Likelihood and impact use `LOW`, `MEDIUM`, `HIGH`, or `CRITICAL`.
Residual risk is reassessed only after the owning command supplies evidence.

| ID | Risk | Likelihood | Impact | Primary treatment | Owner command | External gate |
|---|---|---|---|---|---|---|
| K-01 | Health-only API mistaken for operational capability | HIGH | HIGH | Deliver and test a real vertical slice | C-05, C-06 | No |
| K-02 | Cross-tenant data exposure or IDOR | MEDIUM | CRITICAL | Deny-by-default policy and isolation tests | C-04, C-06 | Security review |
| K-03 | Weak or invalid production configuration | MEDIUM | HIGH | Typed configuration and fail-closed startup | C-03 | No |
| K-04 | Scientific production-grade presented as operational truth | HIGH | CRITICAL | Coarse labels, validity domains and review gates | C-10 through C-12 | Independent reviewer |
| K-05 | Invalid frame, epoch, unit, covariance or stale data | HIGH | CRITICAL | Typed contracts and explicit rejection/degradation | C-08 through C-12 | Domain review |
| K-06 | Unlicensed or misattributed provider data | MEDIUM | CRITICAL | Qualification and legal approval before activation | C-09, C-18 | Legal approval |
| K-07 | Agent tool abuse, prompt injection or false claims | MEDIUM | HIGH | Sandboxing, allowlists, budgets and physics verification | C-14 | Vendor assessment |
| K-08 | Unbounded retry, duplicate work or workflow races | MEDIUM | HIGH | Durable state, idempotency and bounded retries | C-07, C-13 | No |
| K-09 | Missing operational telemetry or leaked secrets | MEDIUM | HIGH | Redaction, metrics, traces and audit validation | C-15 | No |
| K-10 | Dependency or build-chain compromise | MEDIUM | CRITICAL | Scanning, SBOM, signing and pinned CI | C-17 | Signing authority |
| K-11 | Backup exists but restore is unproven | HIGH | HIGH | Reproducible restore drill and recovery evidence | C-18, C-19 | Infrastructure access |
| K-12 | Capacity, latency or cost growth is unbounded | MEDIUM | HIGH | Performance budgets, quotas and FinOps controls | C-16 | Cost authorization |
| K-13 | Documentation overstates implementation | HIGH | HIGH | Evidence-linked documentation reconciliation | C-19, C-20 | No |
| K-14 | Proprietary license is legally incomplete | HIGH | HIGH | LICENSE/NOTICE inventory and specialist legal review | C-18 | Legal approval |
| K-15 | Final release label exceeds available evidence | MEDIUM | CRITICAL | Fail-closed release manifest and residual-risk register | C-20 | Release authority |

## Risk rules

- No critical or high vulnerability may be hidden by test suppression.
- Risk acceptance must name the owner, scope, expiry, evidence, and rationale.
- Missing external approval remains an unresolved external gate.
- Production approval cannot be inferred from successful local tests.
- All safety- and science-critical failures default to review or rejection.
