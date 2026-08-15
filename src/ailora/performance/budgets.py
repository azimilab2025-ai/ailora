"""Explicit local performance, capacity, and artifact budgets."""

from __future__ import annotations

from dataclasses import dataclass

from ailora.performance.benchmark import BenchmarkReport


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
