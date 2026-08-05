"""
AILORA configuration — loaded from environment variables.
All secrets must be supplied via environment; never hard-coded.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings resolved from environment variables."""

    model_config = SettingsConfigDict(
        env_prefix="AILORA_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # ── Application ──────────────────────────────────────────────────────────
    app_name: str = "AILORA"
    app_version: str = "0.1.0"
    debug: bool = False
    environment: str = "local"

    # ── Database (TBD — resolved during PHASE_1) ─────────────────────────────
    database_url: str = "postgresql+psycopg://ailora:ailora@localhost:5432/ailora_db"

    # ── Security ─────────────────────────────────────────────────────────────
    secret_key: str = "CHANGE_ME_BEFORE_ANY_NON_LOCAL_USE"  # noqa: S105
    access_token_expire_minutes: int = 30
    algorithm: str = "HS256"

    # ── CORS ─────────────────────────────────────────────────────────────────
    allowed_origins: list[str] = ["http://localhost:3000", "http://localhost:8000"]


settings = Settings()
