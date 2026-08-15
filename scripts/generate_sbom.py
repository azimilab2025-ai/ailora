#!/usr/bin/env python3
"""Generate a deterministic direct-dependency CycloneDX JSON inventory."""

from __future__ import annotations

import argparse
import json
import re
import tomllib
from pathlib import Path


def dependency_name(requirement: str) -> str:
    match = re.match(r"[A-Za-z0-9_.-]+", requirement)
    if match is None:
        raise ValueError("invalid dependency requirement")
    return match.group(0)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--project", type=Path, default=Path("pyproject.toml"))
    arguments = parser.parse_args()
    project = tomllib.loads(arguments.project.read_text())
    metadata = project["project"]
    requirements = metadata.get("dependencies", [])
    components = [
        {
            "type": "library",
            "name": dependency_name(value),
            "scope": "required",
            "properties": [{"name": "requirement", "value": value}],
        }
        for value in sorted(requirements, key=str.casefold)
    ]
    payload = {
        "bomFormat": "CycloneDX",
        "specVersion": "1.5",
        "serialNumber": "urn:uuid:00000000-0000-0000-0000-000000000000",
        "version": 1,
        "metadata": {
            "component": {
                "type": "application",
                "name": metadata["name"],
                "version": metadata["version"],
            }
        },
        "components": components,
    }
    arguments.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
