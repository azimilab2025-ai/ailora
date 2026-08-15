import sqlite3
from pathlib import Path

from scripts.backup_database import create_backup
from scripts.restore_database import restore_backup


def _db(path: Path, tenant: str = "tenant-a") -> None:
    with sqlite3.connect(path) as db:
        db.execute("CREATE TABLE records (id INTEGER PRIMARY KEY, tenant_id TEXT, value TEXT)")
        db.execute("INSERT INTO records(tenant_id,value) VALUES (?,?)", (tenant, "evidence"))


def test_deterministic_tenant_scoped_roundtrip(tmp_path: Path) -> None:
    source = tmp_path / "source.db"
    _db(source)
    one = tmp_path / "one.zip"
    two = tmp_path / "two.zip"
    create_backup(source, one, "tenant-a")
    create_backup(source, two, "tenant-a")
    assert one.read_bytes() == two.read_bytes()
    restored = tmp_path / "restored.db"
    report = restore_backup(one, restored, "tenant-a")
    assert report["integrity"] == "PASS"
    with sqlite3.connect(restored) as db:
        assert db.execute("SELECT value FROM records").fetchone() == ("evidence",)


def test_cross_tenant_source_rejected(tmp_path: Path) -> None:
    source = tmp_path / "mixed.db"
    _db(source, "tenant-b")
    import pytest

    with pytest.raises(ValueError, match="cross-tenant"):
        create_backup(source, tmp_path / "x.zip", "tenant-a")
