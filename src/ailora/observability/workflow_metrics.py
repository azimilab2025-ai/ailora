"""Bounded-cardinality workflow telemetry and secret-safe fields."""

from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass, field
from typing import Final

_SECRET: Final = re.compile(r"(?i)(authorization|password|token|secret|api[_-]?key)")
_ALLOWED_STATES: Final = frozenset(
    {"PENDING", "RUNNING", "RETRY_WAIT", "SUCCEEDED", "FAILED", "CANCELLED"}
)
_ALLOWED_OUTCOMES: Final = frozenset(
    {"accepted", "duplicate", "succeeded", "failed", "cancelled", "retry"}
)


def redact_fields(fields: dict[str, object]) -> dict[str, object]:
    return {key: "[REDACTED]" if _SECRET.search(key) else value for key, value in fields.items()}


@dataclass(slots=True)
class WorkflowMetrics:
    _counts: Counter[tuple[str, str]] = field(default_factory=Counter)

    def record(self, *, state: str, outcome: str) -> None:
        if state not in _ALLOWED_STATES or outcome not in _ALLOWED_OUTCOMES:
            raise ValueError("workflow metric label is outside bounded vocabulary")
        self._counts[(state, outcome)] += 1

    def snapshot(self) -> dict[tuple[str, str], int]:
        return dict(self._counts)
