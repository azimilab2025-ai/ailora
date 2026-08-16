# AILORA final evidence pack

Artifact: `AILORA-C20-FINAL-EVIDENCE-PACK`
Version: `1.0.0-local-production-grade`
Source commit: `a54ed30453e09253a12b5cd88e045c837214c5d2`
Decision: `CONDITIONAL_LOCAL_Production-Grade_PASS_PRODUCTION_BLOCKED`

## Verified local scope

The immutable baseline contains 633 passing tests, 87.77% statement coverage against an enforced 85% floor, 18 OpenAPI paths, one Alembic head through revision `0011_durable_workflows`, reproducible wheel/sdist evidence, SBOM policy, tenant isolation, advisory-only astrodynamics, durable workflows, disabled Oya safety, local backup/restore qualification, and local staging smoke evidence.

The machine-readable source of this statement is `docs/qualification/final-release-manifest.json`. It binds every pre-C20 checkpoint and qualification document to a SHA-256 digest. A passing local gate proves only the stated local production-grade contract.

## Mandatory boundaries

- `PRODUCTION_RELEASE=BLOCKED`
- `DOMAIN_REVIEW_REQUIRED`
- `LEGAL_REVIEW_REQUIRED`
- `LIVE_NASA_DATA=NOT_ACTIVATED`
- `OYA_STATUS=DISABLED`
- `HUMAN_RELEASE_AUTHORITY=MANDATORY`
- Spacecraft command, telecommand, uplink and autonomous maneuver paths remain permanently prohibited.

No production readiness, scientific approval, legal compliance, live-provider qualification, paid capacity, production signing, penetration-test completion, operational RPO/RTO, production SLO, or deployment claim is made.
