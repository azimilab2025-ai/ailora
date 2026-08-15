from __future__ import annotations

import hashlib
import json
import math
import re
import uuid
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from enum import StrEnum

from ailora.services.astrodynamics.models import (
    AstrodynamicsFrame,
    DistanceUnit,
    PropagationRequest,
    PropagationResult,
    TLEInput,
    VelocityUnit,
)
from ailora.services.astrodynamics.service import AstrodynamicsService

Vector3 = tuple[float, float, float]
_DIGEST = re.compile(r"^[0-9a-f]{64}$")


class TcaErrorCode(StrEnum):
    INVALID_INPUT = "INVALID_INPUT"
    NONFINITE_STATE = "NONFINITE_STATE"
    EVALUATION_BUDGET_EXHAUSTED = "EVALUATION_BUDGET_EXHAUSTED"
    NOT_CONVERGED = "NOT_CONVERGED"


class TcaAnalysisError(RuntimeError):
    def __init__(self, code: TcaErrorCode, detail: str) -> None:
        super().__init__(detail.strip()[:256] or code.value)
        self.code = code


class TcaConvergenceStatus(StrEnum):
    CONVERGED = "CONVERGED"
    ENDPOINT_MINIMUM = "ENDPOINT_MINIMUM"


@dataclass(frozen=True, slots=True)
class TcaSearchConfig:
    coarse_intervals: int = 48
    max_iterations: int = 64
    max_evaluations: int = 128
    time_tolerance_seconds: float = 0.001
    distance_tolerance_km: float = 1e-9

    def __post_init__(self) -> None:
        if not 4 <= self.coarse_intervals <= 10_000:
            raise ValueError("coarse_intervals must be within [4, 10000]")
        if not 1 <= self.max_iterations <= 1_000:
            raise ValueError("max_iterations must be within [1, 1000]")
        if self.max_evaluations < self.coarse_intervals + 3:
            raise ValueError("max_evaluations cannot cover the configured search")
        if not math.isfinite(self.time_tolerance_seconds) or not (
            0.0 < self.time_tolerance_seconds <= 60.0
        ):
            raise ValueError("time_tolerance_seconds must be within (0, 60]")
        if not math.isfinite(self.distance_tolerance_km) or self.distance_tolerance_km <= 0.0:
            raise ValueError("distance_tolerance_km must be positive and finite")


@dataclass(frozen=True, slots=True)
class TcaSearchRequest:
    request_id: uuid.UUID
    primary_tle: TLEInput
    secondary_tle: TLEInput
    search_start: datetime
    search_end: datetime
    purpose: str

    def __post_init__(self) -> None:
        for value in (self.search_start, self.search_end):
            if value.tzinfo is None or value.utcoffset() is None:
                raise ValueError("TCA search epochs must be timezone-aware")
        start = self.search_start.astimezone(UTC)
        end = self.search_end.astimezone(UTC)
        if end <= start:
            raise ValueError("TCA search_end must be after search_start")
        if not self.purpose.strip() or len(self.purpose) > 256:
            raise ValueError("purpose is invalid")
        object.__setattr__(self, "search_start", start)
        object.__setattr__(self, "search_end", end)


@dataclass(frozen=True, slots=True)
class TcaResult:
    request_id: uuid.UUID
    tca_epoch: datetime
    miss_distance_km: float
    relative_position_km: Vector3
    relative_velocity_km_s: Vector3
    frame: AstrodynamicsFrame
    distance_unit: DistanceUnit
    velocity_unit: VelocityUnit
    status: TcaConvergenceStatus
    evaluation_count: int
    iteration_count: int
    search_start: datetime
    search_end: datetime
    time_tolerance_seconds: float
    distance_tolerance_km: float
    algorithm_id: str
    algorithm_version: str
    propagator_algorithm_id: str
    propagator_version: str
    input_digest: str
    configuration_digest: str
    time_uncertainty_seconds: None = None
    advisory_only: bool = True

    def __post_init__(self) -> None:
        values = (
            self.miss_distance_km,
            *self.relative_position_km,
            *self.relative_velocity_km_s,
            self.time_tolerance_seconds,
            self.distance_tolerance_km,
        )
        if not all(math.isfinite(value) for value in values):
            raise ValueError("TCA result must contain finite values")
        if self.miss_distance_km < 0.0:
            raise ValueError("miss distance must be nonnegative")
        if self.frame is not AstrodynamicsFrame.TEME:
            raise ValueError("TCA result frame must remain TEME")
        if self.distance_unit is not DistanceUnit.KILOMETER:
            raise ValueError("TCA distance unit must remain km")
        if self.velocity_unit is not VelocityUnit.KILOMETER_PER_SECOND:
            raise ValueError("TCA velocity unit must remain km/s")
        if not _DIGEST.fullmatch(self.input_digest) or not _DIGEST.fullmatch(
            self.configuration_digest
        ):
            raise ValueError("TCA provenance digests must be lowercase SHA-256")
        if self.advisory_only is not True:
            raise ValueError("TCA result must remain advisory-only")


@dataclass(frozen=True, slots=True)
class _Candidate:
    offset_seconds: float
    distance_squared: float
    primary: PropagationResult
    secondary: PropagationResult


def _digest(payload: dict[str, object]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode(
        "utf-8"
    )
    return hashlib.sha256(encoded).hexdigest()


class TcaAnalyzer:
    def __init__(self, propagation: AstrodynamicsService, config: TcaSearchConfig) -> None:
        self._propagation = propagation
        self._config = config

    def find(self, request: TcaSearchRequest) -> TcaResult:
        duration = (request.search_end - request.search_start).total_seconds()
        evaluations = 0

        def evaluate(offset_seconds: float) -> _Candidate:
            nonlocal evaluations
            if evaluations >= self._config.max_evaluations:
                raise TcaAnalysisError(
                    TcaErrorCode.EVALUATION_BUDGET_EXHAUSTED,
                    "TCA objective evaluation budget was exhausted",
                )
            evaluations += 1
            epoch = request.search_start + timedelta(seconds=offset_seconds)
            primary = self._propagation.propagate(
                PropagationRequest(
                    uuid.uuid5(request.request_id, f"primary:{offset_seconds:.9f}"),
                    request.primary_tle,
                    epoch,
                    request.purpose,
                )
            )
            secondary = self._propagation.propagate(
                PropagationRequest(
                    uuid.uuid5(request.request_id, f"secondary:{offset_seconds:.9f}"),
                    request.secondary_tle,
                    epoch,
                    request.purpose,
                )
            )
            relative = tuple(
                primary.position_km[index] - secondary.position_km[index] for index in range(3)
            )
            squared = sum(component * component for component in relative)
            if not math.isfinite(squared):
                raise TcaAnalysisError(
                    TcaErrorCode.NONFINITE_STATE, "TCA objective became nonfinite"
                )
            return _Candidate(offset_seconds, squared, primary, secondary)

        step = duration / self._config.coarse_intervals
        coarse = [evaluate(index * step) for index in range(self._config.coarse_intervals + 1)]
        best_coarse = self._best_candidate(coarse)
        best_index = coarse.index(best_coarse)
        if best_index in {0, len(coarse) - 1}:
            return self._result(
                request,
                coarse[best_index],
                TcaConvergenceStatus.ENDPOINT_MINIMUM,
                evaluations,
                0,
            )

        left = coarse[best_index - 1].offset_seconds
        right = coarse[best_index + 1].offset_seconds
        ratio = (math.sqrt(5.0) - 1.0) / 2.0
        c_offset = right - ratio * (right - left)
        d_offset = left + ratio * (right - left)
        c = evaluate(c_offset)
        d = evaluate(d_offset)
        iterations = 0
        converged = False
        while iterations < self._config.max_iterations:
            if right - left <= self._config.time_tolerance_seconds:
                converged = True
                break
            iterations += 1
            if (c.distance_squared, c.offset_seconds) <= (d.distance_squared, d.offset_seconds):
                right = d.offset_seconds
                d = c
                c_offset = right - ratio * (right - left)
                c = evaluate(c_offset)
            else:
                left = c.offset_seconds
                c = d
                d_offset = left + ratio * (right - left)
                d = evaluate(d_offset)
        if not converged:
            raise TcaAnalysisError(
                TcaErrorCode.NOT_CONVERGED,
                "TCA refinement did not converge within the configured iteration limit",
            )
        midpoint = evaluate((left + right) / 2.0)
        candidates = (coarse[best_index], c, d, midpoint)
        best = self._best_candidate(candidates)
        return self._result(
            request,
            best,
            TcaConvergenceStatus.CONVERGED,
            evaluations,
            iterations,
        )

    def _result(
        self,
        request: TcaSearchRequest,
        candidate: _Candidate,
        status: TcaConvergenceStatus,
        evaluations: int,
        iterations: int,
    ) -> TcaResult:
        primary = candidate.primary
        secondary = candidate.secondary
        if (
            primary.algorithm_id != secondary.algorithm_id
            or primary.algorithm_version != secondary.algorithm_version
        ):
            raise TcaAnalysisError(
                TcaErrorCode.INVALID_INPUT,
                "primary and secondary propagation profiles must match",
            )
        relative_position = tuple(
            primary.position_km[index] - secondary.position_km[index] for index in range(3)
        )
        relative_velocity = tuple(
            primary.velocity_km_s[index] - secondary.velocity_km_s[index] for index in range(3)
        )
        input_digest = _digest(
            {
                "primary_line1": request.primary_tle.line1,
                "primary_line2": request.primary_tle.line2,
                "secondary_line1": request.secondary_tle.line1,
                "secondary_line2": request.secondary_tle.line2,
                "search_start": request.search_start.isoformat(),
                "search_end": request.search_end.isoformat(),
            }
        )
        configuration_digest = _digest(
            {
                "coarse_intervals": self._config.coarse_intervals,
                "distance_tolerance_km": self._config.distance_tolerance_km,
                "max_evaluations": self._config.max_evaluations,
                "max_iterations": self._config.max_iterations,
                "time_tolerance_seconds": self._config.time_tolerance_seconds,
            }
        )
        return TcaResult(
            request_id=request.request_id,
            tca_epoch=primary.target_epoch,
            miss_distance_km=math.sqrt(candidate.distance_squared),
            relative_position_km=(relative_position[0], relative_position[1], relative_position[2]),
            relative_velocity_km_s=(
                relative_velocity[0],
                relative_velocity[1],
                relative_velocity[2],
            ),
            frame=AstrodynamicsFrame.TEME,
            distance_unit=DistanceUnit.KILOMETER,
            velocity_unit=VelocityUnit.KILOMETER_PER_SECOND,
            status=status,
            evaluation_count=evaluations,
            iteration_count=iterations,
            search_start=request.search_start,
            search_end=request.search_end,
            time_tolerance_seconds=self._config.time_tolerance_seconds,
            distance_tolerance_km=self._config.distance_tolerance_km,
            algorithm_id="BOUNDED_TCA_SEARCH",
            algorithm_version="1.0.0",
            propagator_algorithm_id=primary.algorithm_id,
            propagator_version=primary.algorithm_version,
            input_digest=input_digest,
            configuration_digest=configuration_digest,
        )

    def _best_candidate(self, candidates: list[_Candidate] | tuple[_Candidate, ...]) -> _Candidate:
        best = candidates[0]
        for candidate in candidates[1:]:
            distance_delta = abs(
                math.sqrt(candidate.distance_squared) - math.sqrt(best.distance_squared)
            )
            if candidate.distance_squared < best.distance_squared and (
                distance_delta > self._config.distance_tolerance_km
            ):
                best = candidate
            elif distance_delta <= self._config.distance_tolerance_km and (
                candidate.offset_seconds < best.offset_seconds
            ):
                best = candidate
        return best
