from ailora.performance.benchmark import BenchmarkEnvironment, summarize_samples
from ailora.performance.budgets import PerformanceBudget


def test_percentiles_are_deterministic() -> None:
    report = summarize_samples(
        latency_ms=(10.0, 20.0, 30.0, 40.0, 50.0),
        throughput_per_second=25.0,
        memory_mib=80.0,
        cpu_percent=20.0,
        query_count=4,
        artifact_size_bytes=1024,
        environment=BenchmarkEnvironment("qualification", "3.11", "arm64", 1),
    )
    assert report.p50_ms == 30.0
    assert report.p95_ms == 50.0
    assert report.p99_ms == 50.0
    assert report.dataset_digest


def test_default_budget_accepts_bounded_report() -> None:
    report = summarize_samples((1.0, 2.0, 3.0), 50.0, 64.0, 10.0, 3, 1000)
    assert PerformanceBudget().violations(report) == ()


def test_environment_manifest_has_bounded_cpu_count() -> None:
    environment = BenchmarkEnvironment.capture("local-qualification")
    assert environment.cpu_count >= 1
    assert environment.dataset_name == "local-qualification"
