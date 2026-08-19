from __future__ import annotations

import math
import re
from dataclasses import dataclass
from datetime import UTC, datetime

from ailora.services.astrodynamics.models import (
    AstrodynamicsFrame,
    DistanceUnit,
    VelocityUnit,
)

Matrix3 = tuple[
    tuple[float, float, float],
    tuple[float, float, float],
    tuple[float, float, float],
]
Matrix6 = tuple[tuple[float, ...], ...]

_DIGEST = re.compile(r"^[0-9a-f]{64}$")
_SYMMETRY_TOLERANCE = 1e-12
_PSD_TOLERANCE = 1e-12


class CovarianceError(ValueError):
    """A fail-closed covariance contract violation."""


@dataclass(frozen=True, slots=True)
class CovarianceContract:
    matrix: Matrix6
    epoch: datetime
    frame: AstrodynamicsFrame
    distance_unit: DistanceUnit
    velocity_unit: VelocityUnit
    source_digest: str
    source_revision: str
    matrix_meaning: str
    coordinate_basis: str
    confidence_interpretation: str
    correlation_scope: str
    confidence_scale: float = 1.0
    state_ordering: tuple[str, ...] = ("x", "y", "z", "vx", "vy", "vz")

    def __post_init__(self) -> None:
        if self.epoch.tzinfo is None or self.epoch.utcoffset() is None:
            raise CovarianceError("covariance epoch must be timezone-aware")
        object.__setattr__(self, "epoch", self.epoch.astimezone(UTC))
        if self.frame is not AstrodynamicsFrame.TEME:
            raise CovarianceError("covariance frame must be TEME")
        if self.distance_unit is not DistanceUnit.KILOMETER:
            raise CovarianceError("covariance distance unit must be km")
        if self.velocity_unit is not VelocityUnit.KILOMETER_PER_SECOND:
            raise CovarianceError("covariance velocity unit must be km/s")
        if self.state_ordering != ("x", "y", "z", "vx", "vy", "vz"):
            raise CovarianceError("covariance state ordering must be x,y,z,vx,vy,vz")
        if not _DIGEST.fullmatch(self.source_digest):
            raise CovarianceError("source_digest must be a lowercase SHA-256 digest")
        if not self.source_revision.strip() or len(self.source_revision) > 128:
            raise CovarianceError("source_revision must be explicit")
        if self.matrix_meaning != "STATE_ERROR_COVARIANCE":
            raise CovarianceError("matrix_meaning must be STATE_ERROR_COVARIANCE")
        if self.coordinate_basis != "CARTESIAN_TEME":
            raise CovarianceError("coordinate_basis must be CARTESIAN_TEME")
        if self.confidence_interpretation != "ONE_SIGMA":
            raise CovarianceError("confidence_interpretation must be ONE_SIGMA")
        if self.correlation_scope != "OBJECT_INTERNAL_ONLY":
            raise CovarianceError("correlation_scope must be OBJECT_INTERNAL_ONLY")
        if not math.isfinite(self.confidence_scale) or self.confidence_scale <= 0.0:
            raise CovarianceError("confidence_scale must be positive and finite")
        if len(self.matrix) != 6 or any(len(row) != 6 for row in self.matrix):
            raise CovarianceError("covariance matrix must be 6x6")
        if not all(math.isfinite(value) for row in self.matrix for value in row):
            raise CovarianceError("covariance matrix must contain finite values")
        for row in range(6):
            for column in range(row + 1, 6):
                scale = max(1.0, abs(self.matrix[row][column]), abs(self.matrix[column][row]))
                if abs(self.matrix[row][column] - self.matrix[column][row]) > (
                    _SYMMETRY_TOLERANCE * scale
                ):
                    raise CovarianceError("covariance matrix must be symmetric")
        if not _is_positive_semidefinite(self.matrix):
            raise CovarianceError("covariance matrix must be positive semidefinite")

    @property
    def position_block(self) -> Matrix3:
        return (
            (self.matrix[0][0], self.matrix[0][1], self.matrix[0][2]),
            (self.matrix[1][0], self.matrix[1][1], self.matrix[1][2]),
            (self.matrix[2][0], self.matrix[2][1], self.matrix[2][2]),
        )

    @property
    def numerical_health(self) -> str:
        return "FINITE_SYMMETRIC_PSD;CONDITION_NUMBER_NOT_COMPUTED"


@dataclass(frozen=True, slots=True)
class ConservativeUncertaintyBound:
    radius_km: float
    lower_miss_distance_km: float
    upper_miss_distance_km: float
    sigma_multiplier: float
    method: str = "TRACE_BOUND_V1"
    independence_assumed: bool = True


def _is_positive_semidefinite(matrix: Matrix6) -> bool:
    factors = [[0.0] * 6 for _ in range(6)]
    diagonal = [0.0] * 6
    scale = max(1.0, max(abs(value) for row in matrix for value in row))
    tolerance = _PSD_TOLERANCE * scale
    for column in range(6):
        pivot = matrix[column][column] - sum(
            factors[column][k] * factors[column][k] * diagonal[k] for k in range(column)
        )
        if pivot < -tolerance:
            return False
        if abs(pivot) <= tolerance:
            diagonal[column] = 0.0
            for row in range(column + 1, 6):
                residual = matrix[row][column] - sum(
                    factors[row][k] * factors[column][k] * diagonal[k] for k in range(column)
                )
                if abs(residual) > tolerance:
                    return False
        else:
            diagonal[column] = pivot
            for row in range(column + 1, 6):
                residual = matrix[row][column] - sum(
                    factors[row][k] * factors[column][k] * diagonal[k] for k in range(column)
                )
                factors[row][column] = residual / pivot
    return True


def combine_position_covariances(
    primary: CovarianceContract,
    secondary: CovarianceContract,
    *,
    target_epoch: datetime,
    epoch_tolerance_seconds: float,
    independence_assumed: bool,
) -> Matrix3:
    if not independence_assumed:
        raise CovarianceError("cross-correlation is unavailable; independence must be explicit")
    if target_epoch.tzinfo is None or target_epoch.utcoffset() is None:
        raise CovarianceError("target_epoch must be timezone-aware")
    if not math.isfinite(epoch_tolerance_seconds) or epoch_tolerance_seconds < 0.0:
        raise CovarianceError("epoch_tolerance_seconds must be finite and nonnegative")
    canonical_target = target_epoch.astimezone(UTC)
    for covariance in (primary, secondary):
        delta = abs((covariance.epoch - canonical_target).total_seconds())
        if delta > epoch_tolerance_seconds:
            raise CovarianceError("covariance epoch is not aligned with TCA")
    first = primary.position_block
    second = secondary.position_block
    return (
        (first[0][0] + second[0][0], first[0][1] + second[0][1], first[0][2] + second[0][2]),
        (first[1][0] + second[1][0], first[1][1] + second[1][1], first[1][2] + second[1][2]),
        (first[2][0] + second[2][0], first[2][1] + second[2][1], first[2][2] + second[2][2]),
    )


def conservative_trace_bound(
    relative_position_covariance: Matrix3,
    *,
    nominal_miss_distance_km: float,
    sigma_multiplier: float,
) -> ConservativeUncertaintyBound:
    values = tuple(value for row in relative_position_covariance for value in row)
    if not all(math.isfinite(value) for value in values):
        raise CovarianceError("relative position covariance must be finite")
    if not math.isfinite(nominal_miss_distance_km) or nominal_miss_distance_km < 0.0:
        raise CovarianceError("nominal miss distance must be finite and nonnegative")
    if not math.isfinite(sigma_multiplier) or sigma_multiplier <= 0.0:
        raise CovarianceError("sigma_multiplier must be positive and finite")
    trace = sum(relative_position_covariance[index][index] for index in range(3))
    if trace < -_PSD_TOLERANCE:
        raise CovarianceError("relative position covariance trace must be nonnegative")
    radius = sigma_multiplier * math.sqrt(max(0.0, trace))
    return ConservativeUncertaintyBound(
        radius_km=radius,
        lower_miss_distance_km=max(0.0, nominal_miss_distance_km - radius),
        upper_miss_distance_km=nominal_miss_distance_km + radius,
        sigma_multiplier=sigma_multiplier,
    )


def propagate_covariance(
    contract: CovarianceContract,
    stm: Matrix6,
    dt_seconds: float,
) -> CovarianceContract:
    """Apply a 6x6 state transition matrix and advance epoch. Fail-closed."""
    if not math.isfinite(dt_seconds) or dt_seconds < 0.0:
        raise CovarianceError("dt_seconds must be finite and non-negative")
    if len(stm) != 6 or any(len(row) != 6 for row in stm):
        raise CovarianceError("STM must be 6x6")
    if not all(math.isfinite(v) for row in stm for v in row):
        raise CovarianceError("STM must contain only finite values")

    # P' = STM @ P @ STM.T  (pure Python, no numpy dependency)
    p = contract.matrix
    # first STM @ P
    tmp = [[sum(stm[i][k] * p[k][j] for k in range(6)) for j in range(6)] for i in range(6)]
    # then tmp @ STM.T
    new_matrix = tuple(
        tuple(sum(tmp[i][k] * stm[j][k] for k in range(6)) for j in range(6)) for i in range(6)
    )
    new_epoch = contract.epoch + __import__("datetime").timedelta(seconds=dt_seconds)
    return CovarianceContract(
        matrix=new_matrix,
        epoch=new_epoch,
        frame=contract.frame,
        distance_unit=contract.distance_unit,
        velocity_unit=contract.velocity_unit,
        source_digest=contract.source_digest,
        source_revision=contract.source_revision,
        matrix_meaning=contract.matrix_meaning,
        coordinate_basis=contract.coordinate_basis,
        confidence_interpretation=contract.confidence_interpretation,
        correlation_scope=contract.correlation_scope,
        confidence_scale=contract.confidence_scale,
        state_ordering=contract.state_ordering,
    )


def transform_covariance_frame(
    contract: CovarianceContract,
    target_frame: AstrodynamicsFrame,
    rotation_matrix: Matrix3,
) -> CovarianceContract:
    """Rotate position/velocity blocks with a 3x3 matrix. Fail-closed."""
    if len(rotation_matrix) != 3 or any(len(row) != 3 for row in rotation_matrix):
        raise CovarianceError("rotation_matrix must be 3x3")
    if not all(math.isfinite(v) for row in rotation_matrix for v in row):
        raise CovarianceError("rotation_matrix must contain only finite values")
    # For this bounded implementation we only accept same-frame or explicit TEME preservation
    # Full multi-frame scientific transform remains external-gate.
    if target_frame != contract.frame:
        raise CovarianceError(
            "cross-frame transform requires qualified rotation path (external gate)"
        )
    return contract


def assess_conditioning(contract: CovarianceContract) -> str:
    """Return explicit numerical-health label. Never silent on ill-conditioning."""
    return contract.numerical_health


def check_staleness(
    contract: CovarianceContract,
    now: datetime,
    max_age_seconds: float,
) -> None:
    """Raise if covariance is older than allowed bound."""
    if not math.isfinite(max_age_seconds) or max_age_seconds < 0.0:
        raise CovarianceError("max_age_seconds must be finite and non-negative")
    if now.tzinfo is None:
        raise CovarianceError("now must be timezone-aware")
    age = (now - contract.epoch).total_seconds()
    if age > max_age_seconds:
        raise CovarianceError(f"covariance is stale: age={age}s exceeds max_age={max_age_seconds}s")
