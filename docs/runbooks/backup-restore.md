# Backup and restore runbook

Status: `LOCAL_QUALIFICATION_ONLY`; production execution requires `PRODUCTION_AUTHORIZATION_REQUIRED`.

The local SQLite qualification tool creates a deterministic, tenant-bound archive containing an integrity digest. It rejects mixed-tenant sources, existing destinations, malformed archives, digest mismatch, schema mismatch, and tenant mismatch. It never accepts a database URL. Production PostgreSQL backup format, schedule, encryption, retention, key custody, access control and deletion-tombstone reapplication remain external operational design gates.

Local drill: create an isolated SQLite fixture, run `scripts/backup_database.py`, then restore into a new path with `scripts/restore_database.py`. Record observed start/end timestamps as local RPO/RTO evidence; never generalize these measurements to production.
