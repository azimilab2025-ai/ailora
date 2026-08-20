from __future__ import annotations

import re
from collections import Counter
from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import StrEnum
from math import ceil, isfinite
from types import MappingProxyType


class WorkflowOutcome(StrEnum):
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    INDETERMINATE = "INDETERMINATE"


class ScientificOutcome(StrEnum):
    VERIFIED = "VERIFIED"
    DEGRADED = "DEGRADED"
    INDETERMINATE = "INDETERMINATE"
    FAILED = "FAILED"


class AlertLevel(StrEnum):
    NONE = "NONE"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"


_ALLOWED_DIMENSIONS = frozenset({"operation", "workflow_kind", "environment"})


@dataclass(frozen=True, slots=True)
class SLOPolicy:
    availability_target: float = 0.999
    latency_target_ms: int = 2_000
    warning_burn_rate: float = 2.0
    critical_burn_rate: float = 10.0

    def __post_init__(self) -> None:
        if not 0.0 < self.availability_target < 1.0:
            raise ValueError("availability_target must be strictly between zero and one")
        if self.latency_target_ms <= 0:
            raise ValueError("latency_target_ms must be positive")
        if not 0.0 < self.warning_burn_rate < self.critical_burn_rate:
            raise ValueError("burn thresholds must be positive and strictly ordered")


@dataclass(frozen=True, slots=True)
class WorkflowObservation:
    outcome: WorkflowOutcome
    scientific_outcome: ScientificOutcome
    latency_ms: int
    dimensions: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.latency_ms < 0:
            raise ValueError("latency_ms cannot be negative")
        dimensions = dict(self.dimensions)
        if not set(dimensions).issubset(_ALLOWED_DIMENSIONS):
            raise ValueError("observation contains an unbounded dimension")
        if any(not value or len(value) > 64 for value in dimensions.values()):
            raise ValueError("dimension values must be non-empty and bounded")
        object.__setattr__(self, "dimensions", MappingProxyType(dimensions))


@dataclass(frozen=True, slots=True)
class SLOSnapshot:
    total: int
    availability: float
    latency_compliance: float
    error_budget_remaining: float
    burn_rate: float
    scientific_counts: Mapping[str, int]


@dataclass(frozen=True, slots=True)
class SyntheticProbe:
    probe_id: str
    observed_at: datetime
    succeeded: bool
    advisory_only: bool = True

    def __post_init__(self) -> None:
        if not self.probe_id or len(self.probe_id) > 64:
            raise ValueError("probe_id must be non-empty and bounded")
        if self.observed_at.tzinfo is None or self.observed_at.utcoffset() is None:
            raise ValueError("observed_at must be timezone-aware")
        if not self.advisory_only:
            raise ValueError("synthetic probes cannot create operational authority")

    def is_healthy(self, *, now: datetime, max_age: timedelta) -> bool:
        if now.tzinfo is None or now.utcoffset() is None or max_age <= timedelta(0):
            raise ValueError("health evaluation requires aware time and positive max_age")
        age = now - self.observed_at
        return self.succeeded and timedelta(0) <= age <= max_age


class WorkflowSLOMonitor:
    """Bounded in-memory aggregation contract for later exporter wiring."""

    def __init__(self, policy: SLOPolicy | None = None) -> None:
        self._policy = policy or SLOPolicy()
        self._observations: list[WorkflowObservation] = []

    def observe(self, observation: WorkflowObservation) -> None:
        self._observations.append(observation)

    def snapshot(self) -> SLOSnapshot:
        total = len(self._observations)
        if total == 0:
            return SLOSnapshot(0, 1.0, 1.0, 1.0, 0.0, MappingProxyType({}))
        successes = sum(item.outcome is WorkflowOutcome.SUCCEEDED for item in self._observations)
        fast = sum(item.latency_ms <= self._policy.latency_target_ms for item in self._observations)
        availability = successes / total
        error_rate = 1.0 - availability
        allowed_error_rate = 1.0 - self._policy.availability_target
        burn_rate = error_rate / allowed_error_rate
        consumed_fraction = error_rate / allowed_error_rate
        scientific = Counter(item.scientific_outcome.value for item in self._observations)
        values = MappingProxyType(dict(sorted(scientific.items())))
        metrics = (availability, fast / total, burn_rate, consumed_fraction)
        if any(not isfinite(value) for value in metrics):
            raise RuntimeError("non-finite SLO calculation")
        return SLOSnapshot(
            total=total,
            availability=availability,
            latency_compliance=fast / total,
            error_budget_remaining=max(0.0, 1.0 - consumed_fraction),
            burn_rate=burn_rate,
            scientific_counts=values,
        )

    def alert_level(self) -> AlertLevel:
        burn_rate = self.snapshot().burn_rate
        if burn_rate >= self._policy.critical_burn_rate:
            return AlertLevel.CRITICAL
        if burn_rate >= self._policy.warning_burn_rate:
            return AlertLevel.WARNING
        return AlertLevel.NONE

    def p95_latency_ms(self) -> int | None:
        if not self._observations:
            return None
        values = sorted(item.latency_ms for item in self._observations)
        return values[max(0, ceil(len(values) * 0.95) - 1)]


class SloContractError(ValueError):
    """Fail-closed SLO / shadow-pilot contract error."""

    def __init__(self, detail: str) -> None:
        super().__init__(detail.strip()[:256] or "SLO_CONTRACT_ERROR")


@dataclass(frozen=True, slots=True)
class FrozenCriteriaRecord:
    """Frozen release criteria evidence. Fail-closed."""

    criteria_id: str
    version: str
    rules_digest: str
    approved_by: str

    def __post_init__(self) -> None:
        if not self.criteria_id.strip() or not self.version.strip() or not self.approved_by.strip():
            raise SloContractError("criteria_id, version, approved_by must be explicit")
        if not re.fullmatch(r"[0-9a-f]{64}", self.rules_digest):
            raise SloContractError("rules_digest must be lowercase SHA-256")


@dataclass(frozen=True, slots=True)
class ShadowComparisonEvidence:
    """Advisory shadow comparison evidence. No live pilot claim."""

    comparison_id: str
    tenant_scope: str
    baseline_digest: str
    candidate_digest: str
    matched: bool

    def __post_init__(self) -> None:
        if not self.comparison_id.strip() or not self.tenant_scope.strip():
            raise SloContractError("comparison_id and tenant_scope must be explicit")
        if not re.fullmatch(r"[0-9a-f]{64}", self.baseline_digest):
            raise SloContractError("baseline_digest must be lowercase SHA-256")
        if not re.fullmatch(r"[0-9a-f]{64}", self.candidate_digest):
            raise SloContractError("candidate_digest must be lowercase SHA-256")


@dataclass(frozen=True, slots=True)
class IncidentDrillEvidence:
    """Controlled incident drill evidence. Advisory only."""

    drill_id: str
    scenario: str
    outcome: str
    evidence_digest: str

    def __post_init__(self) -> None:
        if not self.drill_id.strip() or not self.scenario.strip():
            raise SloContractError("drill_id and scenario must be explicit")
        if self.outcome not in {"PASSED", "FAILED", "PARTIAL"}:
            raise SloContractError("outcome must be PASSED|FAILED|PARTIAL")
        if not re.fullmatch(r"[0-9a-f]{64}", self.evidence_digest):
            raise SloContractError("evidence_digest must be lowercase SHA-256")


@dataclass(frozen=True, slots=True)
class SyntheticMonitorResult:
    """Local synthetic monitor result. No network claim."""

    monitor_id: str
    probe_kind: str
    success: bool
    latency_ms: int

    def __post_init__(self) -> None:
        if not self.monitor_id.strip() or not self.probe_kind.strip():
            raise SloContractError("monitor_id and probe_kind must be explicit")
        if self.latency_ms < 0:
            raise SloContractError("latency_ms must be >= 0")
