"""Fail-closed restore for local qualification backups."""

from __future__ import annotations

import argparse
import hashlib
import json
import sqlite3
import zipfile
from pathlib import Path


def restore_backup(source: Path, destination: Path, expected_tenant: str) -> dict[str, object]:
    if "://" in str(source) or not source.is_file() or destination.exists():
        raise ValueError("local backup and new destination required")
    with zipfile.ZipFile(source) as archive:
        if sorted(archive.namelist()) != ["database.sqlite3", "manifest.json"]:
            raise ValueError("unexpected backup content")
        manifest = json.loads(archive.read("manifest.json"))
        data = archive.read("database.sqlite3")
    if manifest.get("schema_version") != 1 or manifest.get("tenant_id") != expected_tenant:
        raise ValueError("schema or tenant mismatch")
    if hashlib.sha256(data).hexdigest() != manifest.get("database_sha256"):
        raise ValueError("backup digest mismatch")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(data)
    try:
        with sqlite3.connect(destination) as db:
            if db.execute("PRAGMA integrity_check").fetchone() != ("ok",):
                raise ValueError("restored integrity failed")
            for table in manifest.get("tables", []):
                columns_query = f'PRAGMA table_info("{table}")'  # noqa: S608
                columns = {r[1] for r in db.execute(columns_query)}
                if "tenant_id" in columns:
                    tenant_query = (
                        f'SELECT DISTINCT tenant_id FROM "{table}" WHERE tenant_id IS NOT NULL'  # noqa: S608
                    )
                    values = {str(r[0]) for r in db.execute(tenant_query)}
                    if values - {expected_tenant}:
                        raise ValueError("restored cross-tenant content")
    except Exception:
        destination.unlink(missing_ok=True)
        raise
    return {"qualification_only": True, "tenant_id": expected_tenant, "integrity": "PASS"}


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("source", type=Path)
    p.add_argument("destination", type=Path)
    p.add_argument("--expected-tenant", required=True)
    a = p.parse_args()
    print(json.dumps(restore_backup(a.source, a.destination, a.expected_tenant), sort_keys=True))  # noqa: T201


if __name__ == "__main__":
    main()
