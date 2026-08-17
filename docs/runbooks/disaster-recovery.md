# Disaster recovery runbook

Status: `LOCAL_QUALIFICATION_ONLY`; any real incident action requires `PRODUCTION_AUTHORIZATION_REQUIRED`.

Decision order: detect and preserve evidence; declare incident owner; contain writes; classify tenant/data impact; select verified recovery point; restore only into isolation; reapply deletion/revocation state; validate schema, integrity, tenant isolation, security and advisory boundaries; obtain human release approval; then reconcile evidence.

The recovery clock remains active through validation: RTO stops only after validated serving, and
RCO stops only after policy, deletion/revocation, audit and derived-state reconciliation. A process
starting or a database accepting connections is not recovered service evidence.

Before any deployment that can execute `alembic upgrade head`, confirm an authorized current
recovery point, managed PITR status, separately pre-provisioned `pgcrypto`, approved database
roles and credential custody, migration owner, rollback decision criteria and post-migration
validation. Missing evidence means stop; do not use deployment itself as a recovery rehearsal.

Escalation roles remain external gates: incident commander, database owner, security/privacy owner, legal reviewer, scientific owner and business release authority. Unknown scope, missing key authority, failed integrity, residency conflict or incomplete deletion replay means fail closed.
