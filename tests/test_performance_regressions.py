import pytest

from ailora.performance.benchmark import summarize_samples
from ailora.performance.budgets import PerformanceBudget, PerformanceRegressionError


def test_every_budget_boundary_is_inclusive() -> None:
    budget = PerformanceBudget()
    samples = (budget.p50_ms,) * 50 + (budget.p95_ms,) * 45 + (budget.p99_ms,) * 5
    report = summarize_samples(
        samples,
        budget.min_throughput_per_second,
        budget.max_memory_mib,
        budget.max_cpu_percent,
        budget.max_query_count,
        budget.max_artifact_size_bytes,
    )
    assert budget.violations(report) == ()


def test_regression_is_explicit_and_machine_readable() -> None:
    budget = PerformanceBudget(max_memory_mib=10.0)
    report = summarize_samples((1.0,), 20.0, 11.0, 1.0, 1, 1)
    assert budget.violations(report) == ("MEMORY_MIB",)
    with pytest.raises(PerformanceRegressionError, match="MEMORY_MIB"):
        budget.assert_within(report)


def test_invalid_samples_fail_closed() -> None:
    with pytest.raises(ValueError, match="latency"):
        summarize_samples((), 1.0, 1.0, 1.0, 1, 1)
