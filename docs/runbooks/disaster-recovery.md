# Disaster recovery runbook

Status: `LOCAL_QUALIFICATION_ONLY`; any real incident action requires `PRODUCTION_AUTHORIZATION_REQUIRED`.

Decision order: detect and preserve evidence; declare incident owner; contain writes; classify tenant/data impact; select verified recovery point; restore only into isolation; reapply deletion/revocation state; validate schema, integrity, tenant isolation, security and advisory boundaries; obtain human release approval; then reconcile evidence.

Escalation roles remain external gates: incident commander, database owner, security/privacy owner, legal reviewer, scientific owner and business release authority. Unknown scope, missing key authority, failed integrity, residency conflict or incomplete deletion replay means fail closed.
