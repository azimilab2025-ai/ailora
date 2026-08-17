# AILORA Command 13 — Recovery Qualification Contract

Baseline: `0d527f2101883f2e4e75880f97539c736c56a90f`

## Status

`RECOVERY_MEASUREMENT_CONTRACT_IMPLEMENTED_MANAGED_PITR_DRILL_PENDING`

This command defines deterministic evidence for isolated recovery drills. It does not access a
provider, create a backup, restore a database, execute an Alembic migration, provision PITR,
approve numerical objectives, invoke Render, or claim production recoverability.

## Implemented recovery boundary

- A timezone-aware monotonic timeline binds recovery point, incident declaration, write fencing,
  restore start, integrity validation, validated serving and reconciliation completion.
- Observed RPO measures possible data-loss time from selected recovery point to incident
  declaration. Observed RTO ends at validated serving. Observed RCO ends after reconciliation.
- Evidence is accepted only for the exact `isolated-local-recovery-drill` environment and can
  never authorize production recovery.
- Seven mandatory checks cover database integrity, tenant isolation, schema head,
  authorization/revocation, deletion suppression, audit integrity and validated serving.
- Unknown or missing checks, non-local evidence references, naïve timestamps, non-monotonic
  stages, non-isolated restore and production-authority claims fail closed.
- The canonical observation is deterministic and SHA-256 bound. Verification rejects digest,
  schema, status, environment, authority, check-set and objective tampering.
- RPO, RTO and RCO objectives remain explicitly `null`; business-impact analysis and authorized
  operational ownership must establish targets outside this command.

## Verification

Twenty-five focused tests cover metric semantics, timezone enforcement, all monotonic stage
boundaries, mandatory and unknown checks, isolation, authority, evidence references, deterministic
serialization, digest tampering, boundary tampering and malformed envelopes. The targeted recovery
and assurance set passes 32 tests. The complete repository suite passes with 898 tests and 88.66%
statement coverage.

## Deployment and production gates

- A Manual Deploy must not be used to discover whether backup, PITR, `pgcrypto`, roles or rollback
  authority exist. Those prerequisites require explicit read-only verification first.
- Revisions `0013_postgres_tenant_rls` and `0014_audit_integrity` remain source-verified but have not
  been executed against production PostgreSQL by this program.
- Provision an approved PITR-capable managed PostgreSQL topology and protected recovery identity.
- Execute independently reviewed restore, concurrency, rollback, failover and failback drills with
  representative data and retain immutable evidence.
- Establish objectives through business-impact analysis, then compare observed production-like
  RPO, validated-serving RTO and reconciliation RCO against those approved objectives.

ENT-007 remains `PARTIAL`. Local recovery evidence and measurement semantics do not satisfy the
external managed-PITR, production-topology, independent-review or release-acceptance gates.
