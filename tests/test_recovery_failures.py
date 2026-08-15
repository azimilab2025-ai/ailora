import sqlite3
import zipfile
from pathlib import Path

import pytest
from scripts.backup_database import create_backup
from scripts.restore_database import restore_backup


def _backup(tmp_path: Path) -> Path:
    db = tmp_path / "a.db"
    with sqlite3.connect(db) as c:
        c.execute("CREATE TABLE t (tenant_id TEXT)")
        c.execute("INSERT INTO t VALUES ('tenant-a')")
    out = tmp_path / "a.zip"
    create_backup(db, out, "tenant-a")
    return out


def test_wrong_tenant_and_existing_destination_fail_closed(tmp_path: Path) -> None:
    backup = _backup(tmp_path)
    with pytest.raises(ValueError, match="tenant"):
        restore_backup(backup, tmp_path / "r.db", "tenant-b")
    existing = tmp_path / "exists.db"
    existing.write_text("preserve")
    with pytest.raises(ValueError):
        restore_backup(backup, existing, "tenant-a")
    assert existing.read_text() == "preserve"


def test_tamper_is_rejected_without_output(tmp_path: Path) -> None:
    backup = _backup(tmp_path)
    bad = tmp_path / "bad.zip"
    with zipfile.ZipFile(backup) as z:
        manifest = z.read("manifest.json")
        data = z.read("database.sqlite3") + b"x"
    with zipfile.ZipFile(bad, "w") as z:
        z.writestr("manifest.json", manifest)
        z.writestr("database.sqlite3", data)
    target = tmp_path / "target.db"
    with pytest.raises(ValueError, match="digest"):
        restore_backup(bad, target, "tenant-a")
    assert not target.exists()
