# Privacy, data classification and residency

Status: governance baseline; `LEGAL_REVIEW_REQUIRED` before production use.

| class | examples | retention | deletion | residency |
|---|---|---|---|---|
| Public | published documentation | project lifecycle | repository process | approved public systems |
| Internal | engineering evidence | bounded business need | owner-approved workflow | approved organization region |
| Confidential | tenant operational data | contract/policy defined | verified dependency-aware workflow | tenant-approved region |
| Restricted | credentials, sensitive personal data | minimum necessary | cryptographic/physical workflow with evidence | explicitly authorized region only |

Unknown classification, purpose, tenant, legal basis, retention, deletion dependency, transfer basis or residency fails closed. Backups must preserve classification and reapply current deletion/revocation controls on restore. This document is not legal advice and does not claim regulatory compliance.
