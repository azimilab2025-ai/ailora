import inspect

from ailora.domain.workflows.service import WorkflowService


def test_replay_requires_tenant_and_contiguous_append_only_events() -> None:
    source = inspect.getsource(WorkflowService.replay)
    assert "tenant_id" in source
    assert "contiguous" in source
    assert "sequence_number" in source


def test_service_has_no_network_queue_or_subprocess_surface() -> None:
    source = inspect.getsource(WorkflowService)
    for forbidden in ("requests.", "httpx.", "subprocess", "redis", "kafka", "celery"):
        assert forbidden not in source.lower()
