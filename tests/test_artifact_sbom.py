import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parents[1]


def test_sbom_is_deterministic_and_contains_direct_dependencies(tmp_path: Path) -> None:
    first = tmp_path / "first.json"
    second = tmp_path / "second.json"
    command = [sys.executable, str(ROOT / "scripts/generate_sbom.py")]
    subprocess.run([*command, "--output", str(first)], check=True, cwd=ROOT)
    subprocess.run([*command, "--output", str(second)], check=True, cwd=ROOT)
    assert (
        hashlib.sha256(first.read_bytes()).digest() == hashlib.sha256(second.read_bytes()).digest()
    )
    payload = json.loads(first.read_text())
    names = {component["name"].lower() for component in payload["components"]}
    assert {"fastapi", "sqlalchemy", "sgp4"} <= names
    assert payload["bomFormat"] == "CycloneDX"


def test_sbom_contains_no_credentials(tmp_path: Path) -> None:
    output = tmp_path / "sbom.json"
    subprocess.run(
        [sys.executable, str(ROOT / "scripts/generate_sbom.py"), "--output", str(output)],
        check=True,
        cwd=ROOT,
    )
    lowered = output.read_text().lower()
    assert "api_key" not in lowered
    assert "webhook_secret" not in lowered
