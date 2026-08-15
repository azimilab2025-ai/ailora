from pathlib import Path

from scripts.staging_smoke import probe


def test_offline_smoke_contract() -> None:
    report = probe(Path(__file__).parents[1])
    assert report["status"] == "PASS"
    assert report["network_actions"] == "NONE" and report["deployment_actions"] == "NONE"


def test_runbooks_preserve_external_authority_gates() -> None:
    root = Path(__file__).parents[1]
    text = "\n".join(
        (root / p).read_text()
        for p in [
            "docs/runbooks/backup-restore.md",
            "docs/runbooks/disaster-recovery.md",
            "docs/runbooks/deployment-rollback.md",
        ]
    )
    assert "PRODUCTION_AUTHORIZATION_REQUIRED" in text and "LOCAL_QUALIFICATION_ONLY" in text
