from __future__ import annotations

import math
import re
from dataclasses import dataclass

from ailora.performance.benchmark import BenchmarkReport

"""Explicit local performance, capacity, and artifact budgets."""


class PerformanceRegressionError(RuntimeError):
    """Raised when one or more explicit qualification budgets are exceeded."""


@dataclass(frozen=True)
class PerformanceBudget:
    p50_ms: float = 50.0
    p95_ms: float = 100.0
    p99_ms: float = 150.0
    min_throughput_per_second: float = 10.0
    max_memory_mib: float = 256.0
    max_cpu_percent: float = 90.0
    max_query_count: int = 25
    max_artifact_size_bytes: int = 25 * 1024 * 1024

    def violations(self, report: BenchmarkReport) -> tuple[str, ...]:
        checks = (
            (report.p50_ms <= self.p50_ms, "P50_MS"),
            (report.p95_ms <= self.p95_ms, "P95_MS"),
            (report.p99_ms <= self.p99_ms, "P99_MS"),
            (report.throughput_per_second >= self.min_throughput_per_second, "THROUGHPUT"),
            (report.memory_mib <= self.max_memory_mib, "MEMORY_MIB"),
            (report.cpu_percent <= self.max_cpu_percent, "CPU_PERCENT"),
            (report.query_count <= self.max_query_count, "QUERY_COUNT"),
            (report.artifact_size_bytes <= self.max_artifact_size_bytes, "ARTIFACT_SIZE"),
        )
        return tuple(name for passed, name in checks if not passed)

    def assert_within(self, report: BenchmarkReport) -> None:
        violations = self.violations(report)
        if violations:
            raise PerformanceRegressionError("performance regression: " + ",".join(violations))


class PerformanceContractError(ValueError):
    """Fail-closed performance/SRE contract error."""

    def __init__(self, detail: str) -> None:
        super().__init__(detail.strip()[:256] or "PERFORMANCE_CONTRACT_ERROR")


@dataclass(frozen=True, slots=True)
class CapacityRunEvidence:
    """Representative capacity run evidence. No live load claim."""

    run_id: str
    object_count: int
    duration_ms: int
    recall_ok: bool
    evidence_digest: str

    def __post_init__(self) -> None:
        if not self.run_id.strip() or len(self.run_id) > 128:
            raise PerformanceContractError("run_id must be explicit and bounded")
        if not (1 <= self.object_count <= 100_000):
            raise PerformanceContractError("object_count must be in [1, 100000]")
        if self.duration_ms < 0:
            raise PerformanceContractError("duration_ms must be non-negative")
        if not re.fullmatch(r"[0-9a-f]{64}", self.evidence_digest):
            raise PerformanceContractError("evidence_digest must be lowercase SHA-256")


@dataclass(frozen=True, slots=True)
class FaultInjectionRecord:
    """Fault injection evidence. Advisory only."""

    injection_id: str
    fault_class: str
    target: str
    injected: bool
    recovered: bool

    def __post_init__(self) -> None:
        if not self.injection_id.strip():
            raise PerformanceContractError("injection_id must be explicit")
        if self.fault_class not in {"TIMEOUT", "ERROR_RATE", "RESOURCE", "OTHER"}:
            raise PerformanceContractError("fault_class invalid")
        if not self.target.strip():
            raise PerformanceContractError("target must be explicit")


@dataclass(frozen=True, slots=True)
class SoakWindowResult:
    """Soak window evidence. Fail-closed."""

    window_id: str
    duration_s: int
    error_count: int
    passed: bool

    def __post_init__(self) -> None:
        if not self.window_id.strip():
            raise PerformanceContractError("window_id must be explicit")
        if self.duration_s <= 0:
            raise PerformanceContractError("duration_s must be positive")
        if self.error_count < 0:
            raise PerformanceContractError("error_count must be non-negative")


@dataclass(frozen=True, slots=True)
class CostGuardrailSnapshot:
    """Cost guardrail snapshot. Advisory; no billing claim."""

    snapshot_id: str
    estimated_units: float
    budget_units: float
    within_budget: bool

    def __post_init__(self) -> None:
        if not self.snapshot_id.strip():
            raise PerformanceContractError("snapshot_id must be explicit")
        if not math.isfinite(self.estimated_units) or self.estimated_units < 0:
            raise PerformanceContractError("estimated_units must be finite and non-negative")
        if not math.isfinite(self.budget_units) or self.budget_units <= 0:
            raise PerformanceContractError("budget_units must be finite and positive")
