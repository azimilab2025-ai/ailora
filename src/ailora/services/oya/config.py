"""
AILORA Oya Voice AI — Configuration and Feature Flag.

STATUS: Production-Grade PHASE — SERVICE DISABLED / NON-BILLABLE.

All configuration defaults ensure the Oya service is completely disabled
and non-billable during production-grade, development, test, and challenge phases.

Activation requires:
  1. AILORA_ENABLE_OYA_VOICE_SERVICE=true  (explicit opt-in)
  2. Non-empty AILORA_OYA_API_KEY           (production credential)
  3. AILORA_OYA_ENVIRONMENT=production      (environment gate)

If any condition is missing or invalid the service remains DISABLED.
This is fail-closed configuration: missing/invalid prerequisites disable Oya.

Secrets:
  OYA_API_KEY and OYA_WEBHOOK_SECRET must be supplied via environment only.
  They must never appear in source code, logs, tests, fixtures, or documentation.
"""

from __future__ import annotations

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class OyaSettings(BaseSettings):
    """
    Oya Voice AI service configuration.

    All defaults are safe for production-grade/development (service disabled).
    Production activation requires all three gate conditions.
    """

    model_config = SettingsConfigDict(
        env_prefix="AILORA_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ── Feature flag (master switch) ─────────────────────────────────────────
    enable_oya_voice_service: bool = False  # MUST remain False unless production gate met

    # ── Provider configuration (TBD — provider-neutral placeholders) ─────────
    oya_api_key: str = ""  # Must be set in production only
    oya_base_url: str = ""  # TBD — vendor-specific URL
    oya_webhook_secret: str = ""  # TBD — vendor-specific webhook verification
    oya_environment: str = "production-grade"  # Set to "production" only with revenue gate

    # ── Safety limits ─────────────────────────────────────────────────────────
    oya_session_timeout_seconds: int = 30
    oya_max_sessions_per_tenant: int = 10
    oya_max_audio_duration_seconds: int = 300  # 5 minutes per session

    @model_validator(mode="after")
    def _enforce_fail_closed(self) -> OyaSettings:
        """
        Fail-closed validation: disable Oya if production gate conditions are not met.

        If enable_oya_voice_service=True but the production credentials and
        environment are not configured, reset to disabled.
        """
        if self.enable_oya_voice_service:
            # All three gate conditions must be satisfied for activation
            gate_ok = bool(self.oya_api_key.strip()) and self.oya_environment == "production"
            if not gate_ok:
                # Fail-closed: disable rather than raise
                object.__setattr__(self, "enable_oya_voice_service", False)
        return self

    @property
    def is_active(self) -> bool:
        """Return True only when Oya is fully configured and active."""
        return (
            self.enable_oya_voice_service
            and bool(self.oya_api_key.strip())
            and self.oya_environment == "production"
        )


# Singleton instance for the application
oya_settings = OyaSettings()
