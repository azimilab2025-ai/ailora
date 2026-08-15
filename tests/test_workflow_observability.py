import pytest

from ailora.observability.workflow_metrics import WorkflowMetrics, redact_fields


def test_secret_fields_are_redacted() -> None:
    safe = redact_fields(
        {"authorization": "Bearer hidden", "tenant": "bounded", "api_key": "hidden"}
    )
    assert safe == {"authorization": "[REDACTED]", "tenant": "bounded", "api_key": "[REDACTED]"}


def test_metrics_have_bounded_vocabulary() -> None:
    metrics = WorkflowMetrics()
    metrics.record(state="FAILED", outcome="failed")
    assert metrics.snapshot() == {("FAILED", "failed"): 1}
    with pytest.raises(ValueError):
        metrics.record(state="tenant-123", outcome="failed")
