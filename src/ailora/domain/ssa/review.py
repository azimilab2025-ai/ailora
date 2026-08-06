"""
AILORA Human Review and Approval State Machine.

Implements the human-in-the-loop approval workflow for conjunction risk
assessments.  This module provides the state machine for tracking whether
a human operator has reviewed an advisory output.

PERMANENT PROHIBITION:
  No approval state in this module creates, enables, or initiates any
  spacecraft command, telecommand, uplink, maneuver execution, or flight
  control path.  These paths are permanently denied (E9/APR-X/INC-0/HARD_DENY).

The approval state has ONLY these effects:
  - Records that a human operator has reviewed an advisory assessment.
  - Marks the assessment as human-reviewed in the audit trail.
  - Enables further analysis or advisory workflows if desired.

Nothing in this module is an operational clearance.
"""

from __future__ import annotations

import uuid
from enum import StrEnum

# ---------------------------------------------------------------------------
# Review state
# ---------------------------------------------------------------------------


class ReviewState(StrEnum):
    """
    State machine for human review of a conjunction risk assessment.

    PENDING_REVIEW   — Assessment produced, awaiting human review.
    UNDER_REVIEW     — A human operator has opened the assessment.
    REVIEWED         — Human operator has marked assessment as reviewed.
    ESCALATED        — Operator has flagged for additional attention.
    DISMISSED        — Operator has dismissed (not actioned) the assessment.
    CLOSED           — Assessment cycle is complete; no further action.
    """

    PENDING_REVIEW = "PENDING_REVIEW"
    UNDER_REVIEW = "UNDER_REVIEW"
    REVIEWED = "REVIEWED"
    ESCALATED = "ESCALATED"
    DISMISSED = "DISMISSED"
    CLOSED = "CLOSED"


# Valid state transitions (directed graph)
_ALLOWED_TRANSITIONS: dict[ReviewState, set[ReviewState]] = {
    ReviewState.PENDING_REVIEW: {ReviewState.UNDER_REVIEW},
    ReviewState.UNDER_REVIEW: {
        ReviewState.REVIEWED,
        ReviewState.ESCALATED,
        ReviewState.DISMISSED,
    },
    ReviewState.REVIEWED: {ReviewState.CLOSED, ReviewState.ESCALATED},
    ReviewState.ESCALATED: {ReviewState.REVIEWED, ReviewState.CLOSED},
    ReviewState.DISMISSED: {ReviewState.CLOSED},
    ReviewState.CLOSED: set(),  # Terminal state — no further transitions
}


class ReviewTransitionError(ValueError):
    """Raised when an invalid state transition is attempted."""


# ---------------------------------------------------------------------------
# Review record
# ---------------------------------------------------------------------------


class ReviewRecord:
    """
    A human review record for a conjunction risk assessment.

    Tracks the lifecycle of human review without creating any command path.

    Attributes:
        record_id:          Unique identifier for this review record.
        scenario_id:        The scenario being reviewed.
        state:              Current review state.
        reviewer_id:        User ID of the reviewing operator (if known).
        notes:              Operator-provided review notes (advisory text only).
        COMMAND_PATH:       Always False — permanently denied.
    """

    # Class-level constant: no command path ever
    COMMAND_PATH: bool = False

    def __init__(
        self,
        scenario_id: uuid.UUID,
        initial_state: ReviewState = ReviewState.PENDING_REVIEW,
    ) -> None:
        self.record_id = uuid.uuid4()
        self.scenario_id = scenario_id
        self.state = initial_state
        self.reviewer_id: uuid.UUID | None = None
        self.notes: str = ""
        self._transition_log: list[tuple[ReviewState, ReviewState]] = []

    def transition(
        self,
        new_state: ReviewState,
        reviewer_id: uuid.UUID | None = None,
        notes: str = "",
    ) -> None:
        """
        Transition to a new review state.

        Args:
            new_state:    Target state.
            reviewer_id:  Operator performing the transition.
            notes:        Optional advisory notes.

        Raises:
            ReviewTransitionError: If the transition is not allowed.
        """
        allowed = _ALLOWED_TRANSITIONS.get(self.state, set())
        if new_state not in allowed:
            raise ReviewTransitionError(
                f"Transition from {self.state!r} to {new_state!r} is not allowed. "
                f"Allowed transitions: {sorted(s.value for s in allowed)}"
            )
        old_state = self.state
        self.state = new_state
        if reviewer_id is not None:
            self.reviewer_id = reviewer_id
        if notes:
            self.notes = notes
        self._transition_log.append((old_state, new_state))

    @property
    def is_terminal(self) -> bool:
        """Return True if no further transitions are possible."""
        return self.state == ReviewState.CLOSED

    @property
    def has_been_reviewed(self) -> bool:
        """Return True if a human operator has reviewed this assessment."""
        return self.state in (
            ReviewState.REVIEWED,
            ReviewState.ESCALATED,
            ReviewState.DISMISSED,
            ReviewState.CLOSED,
        )

    @property
    def transition_count(self) -> int:
        return len(self._transition_log)

    def __repr__(self) -> str:
        return (
            f"ReviewRecord("
            f"record_id={self.record_id!r}, "
            f"state={self.state!r}, "
            f"has_been_reviewed={self.has_been_reviewed})"
        )
