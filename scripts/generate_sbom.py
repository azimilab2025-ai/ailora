#!/usr/bin/env python3
"""Generate a deterministic CycloneDX inventory from the complete uv lock."""

from __future__ import annotations

import argparse
import json
import tomllib
from pathlib import Path


def _purl(name: str, version: str) -> str:
    return f"pkg:pypi/{name.replace('_', '-').lower()}@{version}"


def _hashes(package: dict[str, object]) -> list[dict[str, str]]:
    artifacts: list[object] = []
    if "sdist" in package:
        artifacts.append(package["sdist"])
    wheels = package.get("wheels", [])
    if isinstance(wheels, list):
        artifacts.extend(wheels)
    values: set[str] = set()
    for artifact in artifacts:
        if not isinstance(artifact, dict):
            continue
        raw = artifact.get("hash")
        if isinstance(raw, str) and raw.startswith("sha256:"):
            values.add(raw.removeprefix("sha256:"))
    return [{"alg": "SHA-256", "content": value} for value in sorted(values)]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--project", type=Path, default=Path("pyproject.toml"))
    arguments = parser.parse_args()
    project = tomllib.loads(arguments.project.read_text())
    metadata = project["project"]
    lock_path = arguments.project.with_name("uv.lock")
    lock = tomllib.loads(lock_path.read_text())
    packages = lock.get("package", [])
    if not isinstance(packages, list):
        raise ValueError("uv.lock package inventory is invalid")
    components: list[dict[str, object]] = []
    for package in packages:
        if not isinstance(package, dict) or package.get("name") == metadata["name"]:
            continue
        source = package.get("source")
        if not isinstance(source, dict) or "registry" not in source:
            continue
        name = str(package["name"])
        version = str(package["version"])
        component: dict[str, object] = {
            "bom-ref": _purl(name, version),
            "type": "library",
            "name": name,
            "version": version,
            "purl": _purl(name, version),
            "properties": [
                {"name": "ailora:locked", "value": "true"},
                {"name": "ailora:registry", "value": str(source["registry"])},
            ],
        }
        hashes = _hashes(package)
        if not hashes:
            raise ValueError(f"locked package {name} has no SHA-256 artifact hashes")
        component["hashes"] = hashes
        components.append(component)
    components.sort(key=lambda item: str(item["bom-ref"]))
    payload = {
        "bomFormat": "CycloneDX",
        "specVersion": "1.6",
        "serialNumber": "urn:uuid:00000000-0000-0000-0000-000000000000",
        "version": 1,
        "metadata": {
            "component": {
                "type": "application",
                "name": metadata["name"],
                "version": metadata["version"],
                "bom-ref": _purl(metadata["name"], metadata["version"]),
                "purl": _purl(metadata["name"], metadata["version"]),
            }
        },
        "components": components,
    }
    arguments.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
