import hashlib
import json
import subprocess
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).parents[1]


def test_sbom_is_deterministic_and_contains_complete_locked_inventory(tmp_path: Path) -> None:
    first = tmp_path / "first.json"
    second = tmp_path / "second.json"
    command = [sys.executable, str(ROOT / "scripts/generate_sbom.py")]
    subprocess.run([*command, "--output", str(first)], check=True, cwd=ROOT)
    subprocess.run([*command, "--output", str(second)], check=True, cwd=ROOT)
    assert (
        hashlib.sha256(first.read_bytes()).digest() == hashlib.sha256(second.read_bytes()).digest()
    )
    payload = json.loads(first.read_text())
    components = payload["components"]
    names = {component["name"].lower() for component in components}
    assert {"fastapi", "sqlalchemy", "sgp4"} <= names
    assert payload["bomFormat"] == "CycloneDX"
    assert payload["specVersion"] == "1.6"
    lock = tomllib.loads((ROOT / "uv.lock").read_text())
    expected = {
        (package["name"], package["version"])
        for package in lock["package"]
        if "registry" in package.get("source", {})
    }
    assert {(component["name"], component["version"]) for component in components} == expected
    assert all(component["purl"] == component["bom-ref"] for component in components)
    assert all(component["hashes"] for component in components)
    assert all(
        item["alg"] == "SHA-256" and len(item["content"]) == 64
        for component in components
        for item in component["hashes"]
    )


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
