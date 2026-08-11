"""
AILORA configuration — loaded from environment variables.
All secrets must be supplied via environment; never hard-coded.
"""

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings resolved from environment variables."""

    model_config = SettingsConfigDict(
        env_prefix="AILORA_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ── Application ──────────────────────────────────────────────────────────
    app_name: str = "AILORA"
    app_version: str = "0.1.0"
    debug: bool = False
    environment: str = "local"

    # ── Observability ────────────────────────────────────────────────────────
    enable_tracing: bool = False

    # ── Database ─────────────────────────────────────────────────────────────
    database_url: str = "postgresql+psycopg://ailora:ailora@localhost:55432/ailora_db"

    @field_validator("database_url", mode="before")
    @classmethod
    def normalize_database_url(cls, value: object) -> object:
        """Convert provider PostgreSQL URLs to the SQLAlchemy psycopg v3 scheme."""
        if isinstance(value, str) and value.startswith("postgresql://"):
            return value.replace("postgresql://", "postgresql+psycopg://", 1)
        return value

    # ── Security ─────────────────────────────────────────────────────────────
    secret_key: str = "CHANGE_ME_BEFORE_ANY_NON_LOCAL_USE"  # noqa: S105
    access_token_expire_minutes: int = 30
    algorithm: str = "HS256"

    # ── CORS ─────────────────────────────────────────────────────────────────
    allowed_origins: list[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
    ]

    # ── Server ───────────────────────────────────────────────────────────────
    port: int = 8000

    # ── Oya Voice AI ─────────────────────────────────────────────────────────
    enable_oya_voice_service: bool = False  # noqa: S105


settings = Settings()
