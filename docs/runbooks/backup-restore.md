# Backup and restore runbook

Status: `LOCAL_OBSERVATION_ONLY`; production execution requires `PRODUCTION_AUTHORIZATION_REQUIRED`.

The local SQLite qualification tool creates a deterministic, tenant-bound archive containing an integrity digest. It rejects mixed-tenant sources, existing destinations, malformed archives, digest mismatch, schema mismatch, and tenant mismatch. It never accepts a database URL. Production PostgreSQL backup format, schedule, encryption, retention, key custody, access control and deletion-tombstone reapplication remain external operational design gates.

Local drill: create an isolated SQLite fixture, run `scripts/backup_database.py`, then restore into
a new path with `scripts/restore_database.py`. Use `ailora.recovery.qualification` to bind the
timeline, required validation checks and local evidence references into a deterministic SHA-256
observation. RPO is the interval from selected recovery point to incident declaration. RTO ends
only at validated serving, not process start. RCO ends after reconciliation is complete.

Every observation requires integrity, tenant-isolation, schema-head, authorization/revocation,
deletion-suppression, audit-integrity and validated-serving checks. Exact recovery objectives
remain `null` until approved through business-impact analysis. Local timings must never be
generalized to a managed PostgreSQL topology or represented as production qualification.
