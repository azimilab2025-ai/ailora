"""AILORA configuration loaded and validated from environment variables."""

from enum import StrEnum
from ipaddress import ip_address
from urllib.parse import urlsplit

from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

_DEFAULT_SECRET = "CHANGE_ME_BEFORE_ANY_NON_LOCAL_USE"  # noqa: S105
_PLACEHOLDER_SECRETS = {
    "",
    "change-me",
    "changeme",
    "development-only-secret",
    _DEFAULT_SECRET.casefold(),
}


class Environment(StrEnum):
    """Supported runtime environments."""

    LOCAL = "local"
    TEST = "test"
    INTEGRATION = "integration"
    STAGING = "staging"
    PRODUCTION = "production"


class Settings(BaseSettings):
    """Application settings resolved from environment variables."""

    model_config = SettingsConfigDict(
        env_prefix="AILORA_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = "AILORA"
    app_version: str = "0.1.0"
    debug: bool = False
    environment: Environment = Environment.LOCAL

    enable_tracing: bool = False
    enable_live_space_data_provider: bool = False
    celestrak_base_url: str = "https://celestrak.org"
    celestrak_timeout_seconds: float = Field(default=5.0, ge=0.1, le=30.0)
    celestrak_max_response_bytes: int = Field(default=131_072, ge=1, le=1_048_576)

    runtime_read_only: bool = True
    security_headers_enabled: bool = True
    outbound_https_only: bool = True
    outbound_allowed_hosts: list[str] = []
    rate_limit_requests_per_minute: int = Field(default=120, ge=1, le=10_000)

    database_url: str = "postgresql+psycopg://ailora:ailora@localhost:55432/ailora_db"
    database_pool_size: int = Field(default=5, ge=1, le=50)
    database_max_overflow: int = Field(default=10, ge=0, le=100)
    database_pool_timeout_seconds: float = Field(default=5.0, gt=0, le=60)
    database_pool_recycle_seconds: int = Field(default=1800, ge=30)
    database_probe_timeout_seconds: float = Field(default=3.0, gt=0, le=30)
    database_statement_timeout_ms: int = Field(default=10_000, ge=100, le=120_000)
    database_lock_timeout_ms: int = Field(default=2_000, ge=50, le=30_000)
    database_idle_transaction_timeout_ms: int = Field(
        default=15_000,
        ge=1_000,
        le=120_000,
    )

    secret_key: str = _DEFAULT_SECRET  # noqa: S105
    access_token_expire_minutes: int = Field(default=30, ge=1, le=1440)
    algorithm: str = "HS256"

    allowed_origins: list[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
    ]

    port: int = Field(default=8000, ge=1, le=65535)

    api_max_body_bytes: int = Field(default=1_048_576, ge=1, le=16_777_216)
    api_request_timeout_seconds: float = Field(default=15.0, ge=0.05, le=120)
    api_max_page_size: int = Field(default=100, ge=1, le=500)

    enable_oya_voice_service: bool = False  # noqa: S105

    @field_validator("database_url", mode="before")
    @classmethod
    def normalize_database_url(cls, value: object) -> object:
        """Convert provider PostgreSQL URLs to the SQLAlchemy psycopg v3 scheme."""
        if isinstance(value, str) and value.startswith("postgresql://"):
            return value.replace("postgresql://", "postgresql+psycopg://", 1)
        return value

    @field_validator("celestrak_base_url")
    @classmethod
    def validate_celestrak_base_url(cls, value: str) -> str:
        """Require the canonical credential-free CelesTrak HTTPS origin."""
        candidate = value.strip().rstrip("/")
        parsed = urlsplit(candidate)
        if (
            parsed.scheme != "https"
            or parsed.hostname != "celestrak.org"
            or parsed.username
            or parsed.password
            or parsed.port is not None
            or parsed.path not in {"", "/"}
            or parsed.query
            or parsed.fragment
        ):
            raise ValueError("CelesTrak base URL must be canonical https://celestrak.org")
        return candidate

    @field_validator("outbound_allowed_hosts")
    @classmethod
    def validate_outbound_allowed_hosts(cls, hosts: list[str]) -> list[str]:
        """Require explicit external DNS hostnames for application egress."""
        normalized: list[str] = []

        for host in hosts:
            candidate = host.strip().lower().rstrip(".")

            if (
                not candidate
                or candidate == "*"
                or candidate == "localhost"
                or candidate.endswith(".local")
                or any(token in candidate for token in (":", "/", "@", "[", "]"))
            ):
                raise ValueError(
                    "outbound allowlist entries must be explicit external DNS hostnames"
                )

            try:
                ip_address(candidate)
            except ValueError:
                pass
            else:
                raise ValueError("outbound allowlist entries must not be IP-address literals")

            labels = candidate.split(".")
            if len(labels) < 2 or any(
                not label
                or len(label) > 63
                or label.startswith("-")
                or label.endswith("-")
                or not all(ch.isalnum() or ch == "-" for ch in label)
                for label in labels
            ):
                raise ValueError("outbound allowlist entries must be valid DNS hostnames")

            normalized.append(candidate)

        if len(normalized) != len(set(normalized)):
            raise ValueError("outbound allowlist entries must not contain duplicates")

        return normalized

    @field_validator("allowed_origins")
    @classmethod
    def validate_allowed_origins(cls, origins: list[str]) -> list[str]:
        """Reject ambiguous, duplicate, wildcard, or path-bearing CORS origins."""
        normalized: list[str] = []

        for origin in origins:
            candidate = origin.strip().rstrip("/")

            if not candidate or candidate == "*":
                raise ValueError("CORS origins must be explicit and non-empty")

            parsed = urlsplit(candidate)

            if (
                parsed.scheme not in {"http", "https"}
                or not parsed.hostname
                or parsed.username
                or parsed.password
                or parsed.query
                or parsed.fragment
                or parsed.path not in {"", "/"}
            ):
                raise ValueError("CORS origins must be scheme-and-host origins only")

            normalized.append(candidate)

        if len(normalized) != len(set(normalized)):
            raise ValueError("CORS origins must not contain duplicates")

        return normalized

    @model_validator(mode="after")
    def validate_deployed_environment(self) -> "Settings":
        """Fail closed for unsafe staging or production configuration."""
        if self.environment not in {
            Environment.STAGING,
            Environment.PRODUCTION,
        }:
            return self

        secret = self.secret_key.strip()

        if len(secret) < 32 or secret.casefold() in _PLACEHOLDER_SECRETS:
            raise ValueError(
                "staging and production require a non-placeholder secret of at least 32 characters"
            )

        if self.debug:
            raise ValueError("debug mode is forbidden in staging and production")

        if not self.runtime_read_only:
            raise ValueError(
                "production runtime_read_only must stay enabled as "
                "candidate hardening, not as a blanket POST deny"
            )

        if not self.security_headers_enabled:
            raise ValueError("production security headers must remain enabled")

        if not self.outbound_https_only:
            raise ValueError("production outbound transport must remain HTTPS-only")

        if (
            self.enable_live_space_data_provider
            and "celestrak.org" not in self.outbound_allowed_hosts
        ):
            raise ValueError(
                "CelesTrak live-provider activation requires "
                "celestrak.org in the outbound allowlist"
            )

        insecure_origins = [
            origin for origin in self.allowed_origins if not origin.startswith("https://")
        ]
        if insecure_origins:
            raise ValueError("staging and production CORS origins must use HTTPS")

        return self


settings = Settings()
