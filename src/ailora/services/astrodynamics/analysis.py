from __future__ import annotations

import hashlib
import json
import math
from dataclasses import dataclass
from enum import StrEnum

from ailora.services.astrodynamics.covariance import (
    ConservativeUncertaintyBound,
    CovarianceContract,
    combine_position_covariances,
    conservative_trace_bound,
)
from ailora.services.astrodynamics.tca import TcaResult


class SafeScientificLabel(StrEnum):
    BOUNDED_SEPARATION_ABOVE_THRESHOLD = "BOUNDED_SEPARATION_ABOVE_THRESHOLD"
    POTENTIAL_CONJUNCTION_REVIEW_REQUIRED = "POTENTIAL_CONJUNCTION_REVIEW_REQUIRED"
    UNCERTAINTY_UNAVAILABLE_REVIEW_REQUIRED = "UNCERTAINTY_UNAVAILABLE_REVIEW_REQUIRED"


@dataclass(frozen=True, slots=True)
class ConjunctionAnalysisConfig:
    advisory_threshold_km: float = 10.0
    sigma_multiplier: float = 3.0
    covariance_epoch_tolerance_seconds: float = 0.001

    def __post_init__(self) -> None:
        values = (
            self.advisory_threshold_km,
            self.sigma_multiplier,
            self.covariance_epoch_tolerance_seconds,
        )
        if not all(math.isfinite(value) for value in values):
            raise ValueError("analysis configuration must be finite")
        if self.advisory_threshold_km <= 0.0 or self.sigma_multiplier <= 0.0:
            raise ValueError("threshold and sigma multiplier must be positive")
        if self.covariance_epoch_tolerance_seconds < 0.0:
            raise ValueError("covariance epoch tolerance must be nonnegative")


@dataclass(frozen=True, slots=True)
class BoundedConjunctionAssessment:
    tca: TcaResult
    label: SafeScientificLabel
    uncertainty: ConservativeUncertaintyBound | None
    advisory_threshold_km: float
    algorithm_id: str
    algorithm_version: str
    configuration_digest: str
    limitations: tuple[str, ...]
    collision_probability: None = None
    advisory_only: bool = True
    independent_verification_status: str = "NOT_VERIFIED_DEFERRED_TO_C12"


def assess_bounded_conjunction(
    tca: TcaResult,
    config: ConjunctionAnalysisConfig,
    *,
    primary_covariance: CovarianceContract | None = None,
    secondary_covariance: CovarianceContract | None = None,
    independence_assumed: bool = False,
) -> BoundedConjunctionAssessment:
    if (primary_covariance is None) != (secondary_covariance is None):
        raise ValueError("both covariance contracts are required together")
    uncertainty: ConservativeUncertaintyBound | None = None
    limitations = [
        "ADVISORY_ONLY",
        "BOUNDED_SEARCH_NOT_GLOBAL_OPTIMUM_PROOF",
        "COLLISION_PROBABILITY_NOT_COMPUTED",
        "TCA_PHYSICAL_TIME_UNCERTAINTY_UNAVAILABLE",
        "INDEPENDENT_VERIFICATION_DEFERRED_TO_C12",
    ]
    if primary_covariance is None or secondary_covariance is None:
        label = SafeScientificLabel.UNCERTAINTY_UNAVAILABLE_REVIEW_REQUIRED
        limitations.append("COVARIANCE_UNAVAILABLE")
    else:
        combined = combine_position_covariances(
            primary_covariance,
            secondary_covariance,
            target_epoch=tca.tca_epoch,
            epoch_tolerance_seconds=config.covariance_epoch_tolerance_seconds,
            independence_assumed=independence_assumed,
        )
        uncertainty = conservative_trace_bound(
            combined,
            nominal_miss_distance_km=tca.miss_distance_km,
            sigma_multiplier=config.sigma_multiplier,
        )
        limitations.append("PRIMARY_SECONDARY_INDEPENDENCE_ASSUMED")
        if uncertainty.lower_miss_distance_km <= config.advisory_threshold_km:
            label = SafeScientificLabel.POTENTIAL_CONJUNCTION_REVIEW_REQUIRED
        else:
            label = SafeScientificLabel.BOUNDED_SEPARATION_ABOVE_THRESHOLD
    payload: dict[str, object] = {
        "advisory_threshold_km": config.advisory_threshold_km,
        "covariance_epoch_tolerance_seconds": config.covariance_epoch_tolerance_seconds,
        "sigma_multiplier": config.sigma_multiplier,
    }
    digest = hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    return BoundedConjunctionAssessment(
        tca=tca,
        label=label,
        uncertainty=uncertainty,
        advisory_threshold_km=config.advisory_threshold_km,
        algorithm_id="BOUNDED_CONJUNCTION_ANALYSIS",
        algorithm_version="1.0.0",
        configuration_digest=digest,
        limitations=tuple(limitations),
    )
