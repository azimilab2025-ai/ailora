"""
AILORA Oya Voice AI — Provider-Neutral Interfaces and Type Definitions.

STATUS: PROTOTYPE PHASE — INTERFACES ONLY, NO IMPLEMENTATION.

These interfaces define the contracts that a future Oya provider adapter
must satisfy.  They are provider-neutral and do not reference any specific
vendor SDK, URL, or pricing structure.

TBD items (require explicit authorization and vendor documentation):
  - Specific vendor SDK methods and authentication mechanisms.
  - Audio streaming protocol and format.
  - Webhook signature verification algorithm.
  - Latency SLO and provider-specific circuit breaker thresholds.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import StrEnum

# ---------------------------------------------------------------------------
# Session and event types
# ---------------------------------------------------------------------------


class OyaSessionState(StrEnum):
    """Voice session lifecycle states."""

    IDLE = "IDLE"
    CONNECTING = "CONNECTING"
    ACTIVE = "ACTIVE"
    DEGRADED = "DEGRADED"  # Fallback to text chat
    CLOSED = "CLOSED"
    ERROR = "ERROR"


class OyaFallbackMode(StrEnum):
    """Fallback behavior when voice is unavailable."""

    TEXT_CHAT = "TEXT_CHAT"        # Graceful degradation to standard text interface
    DISABLED = "DISABLED"          # Feature unavailable; user notified


@dataclass(frozen=True)
class OyaSessionConfig:
    """
    Configuration for a single Oya voice session.

    All sensitive values (api_key, etc.) are resolved server-side.
    Never expose credentials to clients.
    """

    tenant_id: str
    user_id: str
    language: str = "en"           # BCP-47 language tag
    fallback_mode: OyaFallbackMode = OyaFallbackMode.TEXT_CHAT
    max_duration_seconds: int = 300


@dataclass(frozen=True)
class OyaSessionResult:
    """Result of a voice session operation."""

    session_id: str
    state: OyaSessionState
    is_advisory: bool = True       # Voice outputs remain advisory-only
    fallback_applied: bool = False
    error_message: str = ""


# ---------------------------------------------------------------------------
# Abstract adapter interface
# ---------------------------------------------------------------------------


class OyaVoiceAdapter(ABC):
    """
    Provider-neutral interface for Oya Voice AI operations.

    Implementations must:
    - Never make network calls when is_active() returns False.
    - Always fall back gracefully to text chat.
    - Never expose credentials to clients or logs.
    - Enforce session quotas and timeouts.
    """

    @abstractmethod
    def is_active(self) -> bool:
        """Return True only when the service is configured and production-active."""

    @abstractmethod
    async def start_session(self, config: OyaSessionConfig) -> OyaSessionResult:
        """
        Start a voice session.

        Must return a DEGRADED/TEXT_CHAT result without network calls
        when is_active() is False.
        """

    @abstractmethod
    async def end_session(self, session_id: str) -> None:
        """End a voice session cleanly."""

    @abstractmethod
    async def health_check(self) -> dict[str, object]:
        """Return service health telemetry (no sensitive data)."""
