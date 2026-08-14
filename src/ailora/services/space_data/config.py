from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import urlparse


@dataclass(frozen=True, slots=True)
class ProviderConfig:
    enabled: bool = False
    provider_id: str = "CELESTRAK"
    provider_version: str = "gp-v1"
    base_url: str = "https://celestrak.org"
    allowed_host: str = "celestrak.org"
    timeout_seconds: float = 5.0
    max_response_bytes: int = 131_072
    allowed_content_types: tuple[str, ...] = ("text/plain", "text/csv")
    attribution_text: str = "CelesTrak source attribution required"

    def __post_init__(self) -> None:
        parsed = urlparse(self.base_url)
        if parsed.scheme != "https" or parsed.hostname != self.allowed_host:
            raise ValueError("base_url must be an allowlisted HTTPS origin")
        if parsed.username is not None or parsed.password is not None or parsed.port is not None:
            raise ValueError("base_url must not contain credentials or a nondefault port")
        if parsed.path not in {"", "/"} or parsed.params or parsed.query or parsed.fragment:
            raise ValueError("base_url must not include path, query, or fragment")
        if not 0.1 <= self.timeout_seconds <= 30.0:
            raise ValueError("timeout_seconds is outside the bounded range")
        if not 1 <= self.max_response_bytes <= 1_048_576:
            raise ValueError("max_response_bytes is outside the bounded range")
        if not self.allowed_content_types:
            raise ValueError("allowed_content_types must not be empty")
