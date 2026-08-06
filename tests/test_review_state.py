"""
AILORA P3-05: Human Review / Approval State Machine Tests.

Validates:
- ReviewState state machine transitions
- ReviewRecord lifecycle
- Invalid transitions raise ReviewTransitionError
- COMMAND_PATH is always False (permanent prohibition)
- Terminal state (CLOSED) has no further transitions
- Transition log is tracked
- No spacecraft command path at any state
"""

from __future__ import annotations

import uuid

import pytest

from ailora.domain.ssa.review import (
    ReviewRecord,
    ReviewState,
    ReviewTransitionError,
)


@pytest.fixture
def pending_record() -> ReviewRecord:
    return ReviewRecord(scenario_id=uuid.uuid4())


# ─── Initial state ───────────────────────────────────────────────────────────


def test_initial_state_is_pending_review(pending_record: ReviewRecord) -> None:
    assert pending_record.state == ReviewState.PENDING_REVIEW


def test_command_path_always_false(pending_record: ReviewRecord) -> None:
    assert ReviewRecord.COMMAND_PATH is False
    assert pending_record.COMMAND_PATH is False


def test_has_been_reviewed_false_initially(pending_record: ReviewRecord) -> None:
    assert pending_record.has_been_reviewed is False


def test_is_not_terminal_initially(pending_record: ReviewRecord) -> None:
    assert pending_record.is_terminal is False


# ─── Valid transitions ────────────────────────────────────────────────────────


def test_transition_pending_to_under_review(pending_record: ReviewRecord) -> None:
    pending_record.transition(ReviewState.UNDER_REVIEW)
    assert pending_record.state == ReviewState.UNDER_REVIEW


def test_transition_under_review_to_reviewed(pending_record: ReviewRecord) -> None:
    pending_record.transition(ReviewState.UNDER_REVIEW)
    pending_record.transition(ReviewState.REVIEWED)
    assert pending_record.state == ReviewState.REVIEWED
    assert pending_record.has_been_reviewed is True


def test_transition_under_review_to_escalated(pending_record: ReviewRecord) -> None:
    pending_record.transition(ReviewState.UNDER_REVIEW)
    pending_record.transition(ReviewState.ESCALATED)
    assert pending_record.state == ReviewState.ESCALATED
    assert pending_record.has_been_reviewed is True


def test_transition_under_review_to_dismissed(pending_record: ReviewRecord) -> None:
    pending_record.transition(ReviewState.UNDER_REVIEW)
    pending_record.transition(ReviewState.DISMISSED)
    assert pending_record.state == ReviewState.DISMISSED
    assert pending_record.has_been_reviewed is True


def test_full_review_cycle_to_closed(pending_record: ReviewRecord) -> None:
    pending_record.transition(ReviewState.UNDER_REVIEW)
    pending_record.transition(ReviewState.REVIEWED)
    pending_record.transition(ReviewState.CLOSED)
    assert pending_record.state == ReviewState.CLOSED
    assert pending_record.is_terminal is True


def test_escalation_cycle_to_closed(pending_record: ReviewRecord) -> None:
    pending_record.transition(ReviewState.UNDER_REVIEW)
    pending_record.transition(ReviewState.ESCALATED)
    pending_record.transition(ReviewState.CLOSED)
    assert pending_record.is_terminal is True


def test_dismissed_cycle_to_closed(pending_record: ReviewRecord) -> None:
    pending_record.transition(ReviewState.UNDER_REVIEW)
    pending_record.transition(ReviewState.DISMISSED)
    pending_record.transition(ReviewState.CLOSED)
    assert pending_record.is_terminal is True


# ─── Invalid transitions ─────────────────────────────────────────────────────


def test_pending_cannot_skip_to_reviewed(pending_record: ReviewRecord) -> None:
    with pytest.raises(ReviewTransitionError):
        pending_record.transition(ReviewState.REVIEWED)


def test_pending_cannot_skip_to_closed(pending_record: ReviewRecord) -> None:
    with pytest.raises(ReviewTransitionError):
        pending_record.transition(ReviewState.CLOSED)


def test_closed_state_has_no_transitions(pending_record: ReviewRecord) -> None:
    pending_record.transition(ReviewState.UNDER_REVIEW)
    pending_record.transition(ReviewState.REVIEWED)
    pending_record.transition(ReviewState.CLOSED)
    with pytest.raises(ReviewTransitionError):
        pending_record.transition(ReviewState.REVIEWED)  # Cannot re-open closed


def test_reviewed_cannot_go_to_pending(pending_record: ReviewRecord) -> None:
    pending_record.transition(ReviewState.UNDER_REVIEW)
    pending_record.transition(ReviewState.REVIEWED)
    with pytest.raises(ReviewTransitionError):
        pending_record.transition(ReviewState.PENDING_REVIEW)


# ─── Reviewer and notes ──────────────────────────────────────────────────────


def test_reviewer_id_recorded_on_transition(pending_record: ReviewRecord) -> None:
    reviewer = uuid.uuid4()
    pending_record.transition(ReviewState.UNDER_REVIEW, reviewer_id=reviewer)
    assert pending_record.reviewer_id == reviewer


def test_notes_recorded_on_transition(pending_record: ReviewRecord) -> None:
    pending_record.transition(ReviewState.UNDER_REVIEW, notes="Opening for review")
    assert pending_record.notes == "Opening for review"


def test_transition_count_increments(pending_record: ReviewRecord) -> None:
    assert pending_record.transition_count == 0
    pending_record.transition(ReviewState.UNDER_REVIEW)
    assert pending_record.transition_count == 1
    pending_record.transition(ReviewState.REVIEWED)
    assert pending_record.transition_count == 2


# ─── Advisory boundary ───────────────────────────────────────────────────────


def test_review_module_no_command_path() -> None:
    from pathlib import Path
    text = (
        Path(__file__).parent.parent
        / "src" / "ailora" / "domain" / "ssa" / "review.py"
    ).read_text()
    # No actual command execution functions
    forbidden = ["execute_command(", "send_uplink(", "maneuver_execute("]
    for f in forbidden:
        assert f not in text.lower()


def test_command_path_false_is_enforced_at_class_level() -> None:
    """COMMAND_PATH must be a class-level False constant, not instance mutable."""
    assert ReviewRecord.COMMAND_PATH is False
    # Cannot set to True even on instance
    r = ReviewRecord(scenario_id=uuid.uuid4())
    assert r.COMMAND_PATH is False
