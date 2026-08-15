#!/usr/bin/env python3
"""Emit deterministic local qualification evidence without performance claims."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from ailora.performance.benchmark import summarize_samples
from ailora.performance.budgets import PerformanceBudget


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    report = summarize_samples((12.0, 15.0, 18.0, 22.0, 30.0), 20.0, 96.0, 25.0, 5, 1024)
    violations = PerformanceBudget().violations(report)
    payload = {
        "schema_version": 1,
        "qualification_only": True,
        "violations": violations,
        "report": report.as_dict(),
    }
    arguments.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return int(bool(violations))


if __name__ == "__main__":
    raise SystemExit(main())
