"""Deterministic benchmark summaries; no paid or external workload execution."""

from __future__ import annotations

import hashlib
import json
import os
import platform
from dataclasses import asdict, dataclass
from math import ceil


@dataclass(frozen=True)
class BenchmarkEnvironment:
    dataset_name: str
    python_version: str
    machine: str
    cpu_count: int

    @classmethod
    def capture(cls, dataset_name: str) -> BenchmarkEnvironment:
        return cls(dataset_name, platform.python_version(), platform.machine(), os.cpu_count() or 1)


@dataclass(frozen=True)
class BenchmarkReport:
    p50_ms: float
    p95_ms: float
    p99_ms: float
    throughput_per_second: float
    memory_mib: float
    cpu_percent: float
    query_count: int
    artifact_size_bytes: int
    dataset_digest: str
    environment: BenchmarkEnvironment

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


def _percentile(values: tuple[float, ...], percentile: float) -> float:
    index = max(0, ceil(percentile * len(values)) - 1)
    return values[index]


def summarize_samples(
    latency_ms: tuple[float, ...],
    throughput_per_second: float,
    memory_mib: float,
    cpu_percent: float,
    query_count: int,
    artifact_size_bytes: int,
    environment: BenchmarkEnvironment | None = None,
) -> BenchmarkReport:
    if not latency_ms or any(value < 0 for value in latency_ms):
        raise ValueError("latency samples must be non-empty and non-negative")
    numeric = (throughput_per_second, memory_mib, cpu_percent)
    if any(value < 0 for value in numeric) or query_count < 0 or artifact_size_bytes < 0:
        raise ValueError("benchmark metrics must be non-negative")
    ordered = tuple(sorted(float(value) for value in latency_ms))
    canonical = json.dumps(ordered, separators=(",", ":")).encode()
    digest = hashlib.sha256(canonical).hexdigest()
    return BenchmarkReport(
        _percentile(ordered, 0.50),
        _percentile(ordered, 0.95),
        _percentile(ordered, 0.99),
        float(throughput_per_second),
        float(memory_mib),
        float(cpu_percent),
        query_count,
        artifact_size_bytes,
        digest,
        environment or BenchmarkEnvironment.capture("bounded-local-fixture-v1"),
    )
