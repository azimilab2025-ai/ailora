# AILORA Command 12 — Audit Integrity and Migration Rehearsal

Baseline: `55008315faf360062e5149b54728228342acae82`

## Status

`AUDIT_HASH_CHAIN_AND_MIGRATION_REHEARSAL_IMPLEMENTED_PRODUCTION_POSTGRES_VALIDATION_PENDING`

This command adds source-level tamper evidence, database-enforced append-only controls and an
expand–migrate–contract migration rehearsal. It does not connect to a live database, execute an
upgrade or rollback, install `pgcrypto`, provision a role or credential, invoke Render, or claim
production PostgreSQL qualification.

## Implemented integrity boundary

- Every tenant has an independent monotonically sequenced SHA-256 chain rooted at a fixed genesis
  hash. The canonical payload length-prefixes every security-relevant field by its UTF-8 byte
  length and normalizes timestamps to UTC microsecond precision.
- Authorized list and item reads reconstruct the complete tenant chain and fail closed on a gap,
  cross-tenant splice, predecessor substitution, malformed hash or payload mutation.
- Revision `0014_audit_integrity` follows `0013_postgres_tenant_rls` as the single Alembic head.
- Its explicit expand phase introduces nullable chain columns; migrate performs a deterministic
  tenant-ordered backfill; contract adds non-null, format, uniqueness, append and mutation guards.
- A PostgreSQL `BEFORE INSERT` trigger serializes each tenant with a transaction advisory lock and
  computes the authoritative sequence and digest inside the database.
- A separate trigger rejects every update or delete. Conditional runtime grants remove update and
  delete capability while retaining bounded select and insert access.
- Backfill temporarily changes RLS only inside the migration transaction and restores enabled,
  forced RLS before the contract phase. Any failure rolls back the transaction.
- The migration requires `digest(bytea,text)` to be pre-provisioned and never creates an extension,
  role, password, secret or `BYPASSRLS` privilege.

## Verification

Twenty-eight focused tests cover migration order, PostgreSQL-only execution, pre-provisioned
`pgcrypto`, forced-RLS restoration, per-tenant locking, database hashing, immutable triggers,
least-privilege grants, downgrade boundaries, canonical serialization, deterministic chaining,
payload tampering, sequence gaps, predecessor substitution, cross-tenant splicing and fail-closed
service reads. The targeted audit and assurance set passes 41 tests. The complete repository suite
passes with 873 tests and 88.57% statement coverage.

## Remaining database and release gates

- Provision and independently approve `pgcrypto`, runtime/read-only roles and credential custody.
- Execute upgrade and rollback against a controlled production-like PostgreSQL clone with real
  existing audit volume, concurrent inserts, forced RLS and owner-role observations.
- Verify trigger ownership, advisory-lock behavior, query plans, failure recovery and operational
  latency under representative load.
- Deploy only after explicit acceptance and retain rollback evidence plus independent database and
  security review.

ENT-006 is `VERIFIED_BASELINE` within its declared source-and-repository-test scope. Production
PostgreSQL validation remains an open external gate; no final acceptance or release approval is
inferred.
