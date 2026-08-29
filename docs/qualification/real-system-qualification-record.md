# Real-system qualification record (sanitized)

Evidence ID: AILORA-RSR-2026-08-29
Record class: documentation of already-executed live tests
Secrets policy: no password, no access token, no refresh token, no email, no database URL

## Binding
- Documentation HEAD at record creation: `1f9e259`
- Live Render deploy observed for OpenAPI/candidate wording: `0c9f153`
- Environment: `https://ailora-web.onrender.com`
- Operator: project owner
- Redaction: real tenant and real email used; identifiers not stored in git

## Executed scenarios (do not rerun unless evidence is lost)
| Scenario | Result | Notes |
|---|---|---|
| Real tenant create | PASS | sanitized REAL tenant class |
| Real email login | PASS | email redacted |
| Session issue | PASS | raw token not stored |
| Membership / identity read | PASS | tenant-bound |
| SSA create/list | PASS | advisory-only |
| External Oya getoya.ai against Render | PASS | Assistant and API Agent Live |
| In-repo Oya library-agent | NOT USED AS HOSTED RUNTIME | local package only |

## Negative / isolation
Cross-tenant and unauthenticated negatives were exercised in Swagger during the same window. Raw traces stay off-repo.

## Non-claims
NASA live is not activated. Collision probability is not claimed. Production-Ready is false. Production-Qualified is false.
