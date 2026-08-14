from __future__ import annotations

import re
import uuid
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from urllib.parse import urlparse

_DIGEST = re.compile(r"^[0-9a-f]{64}$")


class QualificationState(StrEnum):
    UNQUALIFIED = "UNQUALIFIED"
    QUALIFIED = "QUALIFIED"
    SUSPENDED = "SUSPENDED"
    REVOKED = "REVOKED"


class UnqualifiedProviderError(PermissionError):
    pass


@dataclass(frozen=True, slots=True)
class ProviderQualification:
    qualification_id: uuid.UUID
    provider_id: str
    provider_version: str
    state: QualificationState
    license_name: str
    terms_uri: str
    terms_digest: str
    retrieved_at: datetime
    reviewed_at: datetime
    expires_at: datetime | None
    reviewer_reference: str
    redistribution_permitted: bool
    attribution_text: str

    def __post_init__(self) -> None:
        if urlparse(self.terms_uri).scheme != "https":
            raise ValueError("terms_uri must use HTTPS")
        if not _DIGEST.fullmatch(self.terms_digest):
            raise ValueError("terms_digest must be a lowercase SHA-256 digest")
        for name, value in (
            ("retrieved_at", self.retrieved_at),
            ("reviewed_at", self.reviewed_at),
        ):
            if value.tzinfo is None or value.utcoffset() is None:
                raise ValueError(f"{name} must be timezone-aware")
        if self.expires_at is not None:
            if self.expires_at.tzinfo is None or self.expires_at.utcoffset() is None:
                raise ValueError("expires_at must be timezone-aware")
            if self.expires_at <= self.reviewed_at:
                raise ValueError("expires_at must be after reviewed_at")
        if not self.reviewer_reference.strip() or not self.attribution_text.strip():
            raise ValueError("review and attribution evidence are required")


class QualificationGate:
    def require(self, evidence: ProviderQualification, evaluated_at: datetime) -> None:
        if evaluated_at.tzinfo is None or evaluated_at.utcoffset() is None:
            raise ValueError("evaluated_at must be timezone-aware")
        if evidence.state is not QualificationState.QUALIFIED:
            raise UnqualifiedProviderError("provider is not qualified")
        if evidence.expires_at is not None and evaluated_at >= evidence.expires_at:
            raise UnqualifiedProviderError("provider qualification has expired")
