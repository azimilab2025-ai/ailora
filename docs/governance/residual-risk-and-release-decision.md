# Residual risk and release decision

Final engineering decision: `CONDITIONAL_LOCAL_Production-Grade_PASS_PRODUCTION_BLOCKED`.

`PRODUCTION_RELEASE=BLOCKED` and `HUMAN_RELEASE_AUTHORITY=MANDATORY`. This decision is fail-closed: missing or stale closure evidence cannot be interpreted as approval.

| ID | Residual risk | Severity | Owner | Mitigation / required closure evidence | Status |
|---|---|---|---|---|---|
| SCI-001 | Normative astrodynamics validity is not independently approved | CRITICAL | Qualified astrodynamics review authority | Independent review report and explicit closure of `DOMAIN_REVIEW_REQUIRED` | OPEN_EXTERNAL_GATE |
| DATA-001 | Live NASA/CelesTrak source rights, provenance and operations are not qualified | HIGH | Data governance and provider owner | Executed terms, source qualification, provenance and outage evidence | OPEN_EXTERNAL_GATE |
| LEGAL-001 | License, privacy, residency and regulatory conclusions are unreviewed | CRITICAL | Independent legal/privacy authority | Written review; `LEGAL_REVIEW_REQUIRED` remains active | OPEN_EXTERNAL_GATE |
| OYA-001 | Vendor, security, residency, latency and commercial terms are unknown | HIGH | Product, security and vendor owners | Due diligence, contract, safety assessment and explicit activation authority | OPEN_EXTERNAL_GATE |
| OPS-001 | Production infrastructure, soak, pentest, signing keys, alerting and DR are absent | CRITICAL | Production release authority | Environment evidence, pentest, signed artifacts, monitored soak and recovery drill | OPEN_EXTERNAL_GATE |

`LIVE_NASA_DATA=NOT_ACTIVATED`. `OYA_STATUS=DISABLED`. Local backup timings are qualification observations, not production RPO/RTO. The repository may be described as a verified local production-grade baseline only.
