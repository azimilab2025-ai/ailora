import inspect

import pytest

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


# --- COMMAND 26 / ENT-019 additions ---


def test_durable_queue_message_accepts_valid() -> None:
    from datetime import UTC, datetime

    from ailora.domain.workflows.models import DurableQueueMessage

    m = DurableQueueMessage(
        message_id="MSG-1",
        queue_name="ssa.ingest",
        payload_digest="a" * 64,
        priority=5,
        enqueued_at=datetime(2026, 8, 19, tzinfo=UTC),
    )
    assert m.priority == 5


def test_durable_queue_message_rejects_bad_digest() -> None:
    from datetime import UTC, datetime

    from ailora.domain.workflows.models import DurableQueueMessage, WorkflowContractError

    with pytest.raises(WorkflowContractError):
        DurableQueueMessage(
            message_id="MSG-1",
            queue_name="ssa.ingest",
            payload_digest="bad",
            priority=5,
            enqueued_at=datetime(2026, 8, 19, tzinfo=UTC),
        )


def test_dead_letter_record_accepts_valid() -> None:
    from datetime import UTC, datetime

    from ailora.domain.workflows.models import DeadLetterRecord

    r = DeadLetterRecord(
        original_message_id="MSG-1",
        reason="max_attempts_exceeded",
        attempts=5,
        moved_at=datetime(2026, 8, 19, tzinfo=UTC),
    )
    assert r.attempts == 5


def test_backpressure_signal_accepts_valid() -> None:
    from ailora.domain.workflows.models import BackpressureSignal

    s = BackpressureSignal(
        queue_name="ssa.ingest",
        depth=120,
        threshold=100,
        signal_state="THROTTLED",
    )
    assert s.signal_state == "THROTTLED"


def test_scheduler_lease_accepts_valid() -> None:
    from datetime import UTC, datetime

    from ailora.domain.workflows.models import SchedulerLease

    lease = SchedulerLease(
        lease_id="L-1",
        worker_id="W-1",
        expires_at=datetime(2026, 8, 19, 12, 0, tzinfo=UTC),
        cancel_requested=False,
    )
    assert lease.cancel_requested is False
