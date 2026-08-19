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


class GovernanceError(ValueError):
    """Fail-closed governance contract error."""

    def __init__(self, detail: str) -> None:
        super().__init__(detail.strip()[:256] or "GOVERNANCE_ERROR")


@dataclass(frozen=True, slots=True)
class LegalStatusRecord:
    """Bounded legal status evidence. Fail-closed."""

    provider_id: str
    legal_status: str
    effective_from: datetime
    evidence_digest: str

    def __post_init__(self) -> None:
        if not self.provider_id.strip() or len(self.provider_id) > 128:
            raise GovernanceError("provider_id must be explicit and bounded")
        if self.legal_status not in {"ACTIVE", "SUSPENDED", "REVOKED", "UNKNOWN"}:
            raise GovernanceError("legal_status must be ACTIVE|SUSPENDED|REVOKED|UNKNOWN")
        if not re.fullmatch(r"[0-9a-f]{64}", self.evidence_digest):
            raise GovernanceError("evidence_digest must be lowercase SHA-256")


@dataclass(frozen=True, slots=True)
class FreshnessTaxonomy:
    """Freshness taxonomy label. Advisory only."""

    source_class: str
    max_age_seconds: int
    poisoning_risk_class: str

    def __post_init__(self) -> None:
        if not self.source_class.strip() or len(self.source_class) > 64:
            raise GovernanceError("source_class must be explicit")
        if self.max_age_seconds < 0:
            raise GovernanceError("max_age_seconds must be non-negative")
        if self.poisoning_risk_class not in {"LOW", "MEDIUM", "HIGH", "CRITICAL"}:
            raise GovernanceError("poisoning_risk_class must be LOW|MEDIUM|HIGH|CRITICAL")


@dataclass(frozen=True, slots=True)
class PoisoningDefenseSignal:
    """Poisoning defense signal. Advisory only, never auto-remediate."""

    signal_id: str
    detected_at: datetime
    severity: str
    mitigation_action: str

    def __post_init__(self) -> None:
        if not self.signal_id.strip() or len(self.signal_id) > 128:
            raise GovernanceError("signal_id must be explicit")
        if self.severity not in {"LOW", "MEDIUM", "HIGH", "CRITICAL"}:
            raise GovernanceError("severity must be LOW|MEDIUM|HIGH|CRITICAL")
        if not self.mitigation_action.strip():
            raise GovernanceError("mitigation_action must be explicit")


@dataclass(frozen=True, slots=True)
class ProviderChangeMonitorSnapshot:
    """Provider change monitor snapshot. Advisory only."""

    provider_id: str
    last_change_epoch: datetime
    change_digest: str
    monitor_status: str

    def __post_init__(self) -> None:
        if not self.provider_id.strip() or len(self.provider_id) > 128:
            raise GovernanceError("provider_id must be explicit")
        if not re.fullmatch(r"[0-9a-f]{64}", self.change_digest):
            raise GovernanceError("change_digest must be lowercase SHA-256")
        if self.monitor_status not in {"WATCHING", "ALERT", "PAUSED", "UNKNOWN"}:
            raise GovernanceError("monitor_status must be WATCHING|ALERT|PAUSED|UNKNOWN")
