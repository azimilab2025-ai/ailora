# AILORA enterprise qualification baseline

Artifact: `AILORA-ENTERPRISE-QUALIFICATION-BASELINE`
Version: `2.0.0-production-candidate`
Baseline source commit: `594324c35ad587207b3515d7e2a9cd34b74f0fcc`
Decision: `PRODUCTION_CANDIDATE_ACTIVE_QUALIFICATION`

## Verified engineering scope

The current baseline contains 700 passing tests, 87.61% statement coverage against an enforced
85% floor, 20 OpenAPI paths / 27 operations, and one Alembic head through revision
`0012_frame_transformations`. It includes tenant-scoped identity and SSA evidence, bounded
astrodynamics, governed CelesTrak transport, persisted TEME-to-GCRF provenance, durable database
workflows, SBOM/build controls and a live Render service.

The machine-readable source is `docs/qualification/final-release-manifest.json`. Historical
evidence remains digest-bound. This baseline identifies implemented software; it does not
self-issue scientific, legal, security, HA, DR or operational approval.

## Mandatory boundaries

- `PRODUCTION_RELEASE=BLOCKED_PENDING_P0_GATES`
- `CONTROLLED_PROVIDER_E2E=DEFERRED_REQUIRED_BEFORE_FINAL_RELEASE`
- `PROXIMITY_SEVERITY_IS_NOT_COLLISION_PROBABILITY`
- `DOMAIN_REVIEW_REQUIRED`
- `LEGAL_REVIEW_REQUIRED`
- `LIVE_NASA_DATA=NOT_ACTIVATED`
- `OYA_STATUS=DISABLED`
- `HUMAN_RELEASE_AUTHORITY=MANDATORY`
- Spacecraft command, telecommand, uplink and autonomous maneuver paths remain prohibited.
