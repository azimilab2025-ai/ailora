"""
AILORA Oya Voice AI — No-Op / Mock Adapter.

STATUS: Production-Grade PHASE — NO NETWORK CALLS, NON-BILLABLE.

This adapter implements the OyaVoiceAdapter interface with a pure no-op
implementation.  It is always disabled (is_active() returns False) and
never makes any network calls, charges, or external requests.

This is the default adapter used during production-grade, development, test,
and challenge phases.

A production adapter (with real vendor SDK integration) will only be
implemented after:
  1. The revenue gate condition is met.
  2. Explicit authorization from Amin Azimi.
  3. Vendor documentation and API access are confirmed.
"""

from __future__ import annotations

import uuid

from ailora.services.oya.config import oya_settings
from ailora.services.oya.interfaces import (
    OyaFallbackMode,
    OyaSessionConfig,
    OyaSessionResult,
    OyaSessionState,
    OyaVoiceAdapter,
)


class NoOpOyaAdapter(OyaVoiceAdapter):
    """
    No-operation Oya adapter.

    All methods return safe production-grade-phase responses without any network
    call, billable action, or external side effect.
    """

    def is_active(self) -> bool:
        """Always returns False in production-grade mode."""
        return oya_settings.is_active

    async def start_session(self, config: OyaSessionConfig) -> OyaSessionResult:
        """
        Return a DEGRADED/fallback result — never makes a network call.

        Falls back to TEXT_CHAT in production-grade mode.
        """
        if self.is_active():
            # This path is unreachable in production-grade — fail-closed guard
            raise RuntimeError(  # noqa: TRY004
                "NoOpOyaAdapter must never be used with an active production service. "
                "Use the production adapter instead."
            )
        return OyaSessionResult(
            session_id=str(uuid.uuid4()),
            state=OyaSessionState.DEGRADED,
            is_advisory=True,
            fallback_applied=True,
            error_message=(
                "Oya Voice AI is disabled in production-grade phase. "
                "Falling back to text chat. "
                "Activate by meeting the production revenue gate."
            ),
        )

    async def end_session(self, session_id: str) -> None:
        """No-op end session — nothing to close in production-grade mode."""

    async def health_check(self) -> dict[str, object]:
        """Return safe health telemetry — no sensitive data."""
        return {
            "service": "oya_voice",
            "status": "disabled",
            "phase": "production-grade",
            "is_active": False,
            "fallback_mode": OyaFallbackMode.TEXT_CHAT.value,
            "note": "Oya is disabled during production-grade phase.",
        }


# Default adapter instance — always no-op in production-grade
default_oya_adapter: OyaVoiceAdapter = NoOpOyaAdapter()
