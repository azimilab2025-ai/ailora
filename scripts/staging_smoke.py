"""Offline release-candidate configuration smoke probe."""

from __future__ import annotations

import json
from pathlib import Path


def probe(root: Path) -> dict[str, object]:
    required = {
        "Dockerfile": ["USER ailora", "HEALTHCHECK"],
        "docker-compose.yml": ["service_healthy", "127.0.0.1"],
        "render.yaml": ['autoDeployTrigger: "off"', "healthCheckPath: /health/live"],
        ".env.example": ["AILORA_ENABLE_OYA_VOICE_SERVICE=false", "AILORA_ENVIRONMENT=local"],
    }
    checks = {
        name: all(marker in (root / name).read_text() for marker in markers)
        for name, markers in required.items()
    }
    return {
        "qualification_only": True,
        "network_actions": "NONE",
        "deployment_actions": "NONE",
        "checks": checks,
        "status": "PASS" if all(checks.values()) else "FAIL",
    }


def main() -> None:
    report = probe(Path.cwd())
    print(json.dumps(report, sort_keys=True))  # noqa: T201
    raise SystemExit(0 if report["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
