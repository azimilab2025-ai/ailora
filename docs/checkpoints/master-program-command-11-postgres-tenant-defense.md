# AILORA Command 11 — PostgreSQL Tenant Defense

Baseline: `e9ea3ee66a34ca3559e9c51f63ca36c6783c1ac2`

## Status

`POSTGRES_RLS_AND_TRANSACTION_CONTEXT_IMPLEMENTED_PRODUCTION_VALIDATION_PENDING`

This command adds source-level PostgreSQL defense in depth. It does not connect to a live
database, execute the migration, create database roles or credentials, invoke Render, or claim
production qualification.

## Commands 06–10 engineering checkpoint — exactly 100 words

Commands six through ten established asymmetric JWT verification, public JWKS, bounded key rotation, provider-neutral OIDC validation, MFA checks, hardened session replay controls, tenant-bound workload identity, contextual authorization, and enterprise HTTP contracts. Every change remained explicitly bounded: runtime OIDC and workload routing stayed disabled, production credentials were absent, and Render deployment was not invoked. Repository evidence progressed from 710 to 809 passing tests while coverage increased from 87.73% to 88.46%. Remaining risks include production identity-provider integration, operational key custody, durable multi-instance idempotency, tenant end-to-end validation, deployment, and independent security review. These are open gates, not inferred accomplishments or release approval claims.

## Implemented database boundary

- Revision `0013_postgres_tenant_rls` follows `0012_frame_transformations` as one Alembic head.
- Fourteen tables carrying a direct `tenant_id` receive enabled and forced PostgreSQL RLS.
- Every policy uses the transaction-local `app.current_tenant_id` in both `USING` and
  `WITH CHECK`; missing or malformed tenant context fails closed.
- Request tenant, actor and correlation identifiers are reapplied at every SQLAlchemy transaction
  boundary, including after a service-level commit.
- `statement_timeout`, `lock_timeout` and `idle_in_transaction_session_timeout` are bounded by
  validated configuration and applied transaction-locally.
- Grants are limited to the fourteen protected tables and only occur if the separately managed
  `ailora_runtime` or `ailora_readonly` role already exists. The migration never creates a role,
  password, secret or `BYPASSRLS` privilege.
- Non-PostgreSQL migration execution is a deliberate no-op; SQLite repository tests remain valid.

## Verification

Thirty-six focused tests cover the migration chain, exact table scope, safe identifiers,
fail-closed policy expression, forced RLS, symmetric write checks, bounded conditional grants,
non-PostgreSQL behavior, downgrade order, request identity parsing, empty context, transaction
reapplication and timeout configuration. The complete repository suite passes with 845 tests and
88.49% statement coverage.

## Remaining database and release gates

- Provision and independently approve runtime/read-only PostgreSQL roles and credential custody.
- Execute upgrade and rollback rehearsals against a controlled production-like PostgreSQL clone.
- Validate owner-role behavior, connection-pool reuse, concurrency, query plans and operational
  timeouts with real PostgreSQL evidence.
- Extend tenant enforcement to child tables without direct `tenant_id` through verified joins or
  schema changes.
- Complete append-only and tamper-evident audit controls plus expand-migrate-contract rehearsal in
  Command 12.
- Receive explicit deployment, migration, independent security and final release acceptance.

Downgrade disables forced RLS and therefore weakens tenant isolation. It is an emergency rollback
mechanism requiring explicit release authority, not a routine or automatically safe operation.
ENT-006 remains `PARTIAL`; source implementation and repository verification do not satisfy the
external production PostgreSQL gate.
