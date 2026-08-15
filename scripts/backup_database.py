"""Bounded local SQLite backup qualification; never targets production."""

from __future__ import annotations

import argparse
import hashlib
import json
import sqlite3
import zipfile
from pathlib import Path

SCHEMA_VERSION = 1


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _reject(path: Path) -> None:
    if "://" in str(path) or not path.is_file():
        raise ValueError("explicit existing local SQLite file required")


def create_backup(source: Path, destination: Path, tenant_id: str) -> dict[str, object]:
    _reject(source)
    if not tenant_id.strip() or destination.exists():
        raise ValueError("tenant and new destination required")
    with sqlite3.connect(source) as db:
        if db.execute("PRAGMA integrity_check").fetchone() != ("ok",):
            raise ValueError("source integrity failed")
        tables = [
            r[0]
            for r in db.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
            if not r[0].startswith("sqlite_")
        ]
        for table in tables:
            columns_query = f'PRAGMA table_info("{table}")'  # noqa: S608
            columns = {r[1] for r in db.execute(columns_query)}
            if "tenant_id" in columns:
                tenant_query = (
                    f'SELECT DISTINCT tenant_id FROM "{table}" WHERE tenant_id IS NOT NULL'  # noqa: S608
                )
                values = {str(r[0]) for r in db.execute(tenant_query)}
                if values - {tenant_id}:
                    raise ValueError("cross-tenant source rejected")
    data = source.read_bytes()
    manifest = {
        "schema_version": SCHEMA_VERSION,
        "qualification_only": True,
        "tenant_id": tenant_id,
        "database_sha256": _sha(data),
        "tables": tables,
    }
    payload = json.dumps(manifest, sort_keys=True, separators=(",", ":")).encode()
    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_STORED) as archive:
        for name, content in (("manifest.json", payload), ("database.sqlite3", data)):
            info = zipfile.ZipInfo(name, (1980, 1, 1, 0, 0, 0))
            info.external_attr = 0o600 << 16
            archive.writestr(info, content)
    return manifest


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("source", type=Path)
    p.add_argument("destination", type=Path)
    p.add_argument("--tenant-id", required=True)
    a = p.parse_args()
    print(json.dumps(create_backup(a.source, a.destination, a.tenant_id), sort_keys=True))  # noqa: T201


if __name__ == "__main__":
    main()
