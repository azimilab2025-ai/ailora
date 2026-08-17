"""Deterministic offline conversion of native SGP4 TEME states to AILORA GCRF.

Astropy's GCRS frame is the concrete realization used for the project-level GCRF
contract. Position and velocity are transformed together at one UTC epoch. The
operation is advisory-only and uses the pinned, bundled IERS-A/B dataset without
runtime downloads.
"""

from __future__ import annotations

import hashlib
import importlib.metadata
import json
import math
import re
import threading
from collections.abc import Iterator, Sequence
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Final

import astropy.units as u
from astropy.coordinates import GCRS, TEME, CartesianDifferential, CartesianRepresentation
from astropy.time import Time
from astropy.utils import iers

Vector3 = tuple[float, float, float]

_DIGEST: Final[re.Pattern[str]] = re.compile(r"^[0-9a-f]{64}$")
_TRANSFORM_LOCK: Final = threading.RLock()
_EXPECTED_ASTROPY_VERSION: Final[str] = "8.0.1"
_EXPECTED_IERS_DATA_VERSION: Final[str] = "0.2026.8.10.0.32.39"
_ALGORITHM_ID: Final[str] = "ASTROPY_TEME_TO_GCRS_GCRF"
_ALGORITHM_VERSION: Final[str] = "1"


class FrameTransformationError(ValueError):
    """A bounded TEME-to-GCRF transformation contract violation."""


@dataclass(frozen=True, slots=True)
class FrameTransformResult:
    epoch: datetime
    position_km: Vector3
    velocity_km_s: Vector3
    source_frame: str
    target_frame: str
    frame_realization: str
    distance_unit: str
    velocity_unit: str
    algorithm_id: str
    algorithm_version: str
    astropy_version: str
    iers_data_version: str
    iers_source: str
    iers_mjd_start: float
    iers_mjd_end: float
    eop_status: str
    input_digest: str
    iers_data_digest: str
    transformation_digest: str
    advisory_only: bool

    def __post_init__(self) -> None:
        if self.epoch.tzinfo is None or self.epoch.utcoffset() is None:
            raise ValueError("epoch must be timezone-aware")
        values = (
            *self.position_km,
            *self.velocity_km_s,
            self.iers_mjd_start,
            self.iers_mjd_end,
        )
        if not all(math.isfinite(value) for value in values):
            raise ValueError("transformation result must contain finite values")
        if self.source_frame != "TEME":
            raise ValueError("source_frame must be TEME")
        if self.target_frame != "GCRF":
            raise ValueError("target_frame must be GCRF")
        if self.frame_realization != "ASTROPY_GCRS":
            raise ValueError("frame_realization must be ASTROPY_GCRS")
        if self.distance_unit != "km" or self.velocity_unit != "km/s":
            raise ValueError("transformation units must be km and km/s")
        for digest in (self.input_digest, self.iers_data_digest, self.transformation_digest):
            if not _DIGEST.fullmatch(digest):
                raise ValueError("transformation digests must be lowercase SHA-256")
        if self.advisory_only is not True:
            raise ValueError("transformation must remain advisory-only")


def _canonical_digest(payload: dict[str, object]) -> str:
    encoded = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _validated_vector(values: Sequence[float], label: str) -> Vector3:
    if len(values) != 3:
        raise FrameTransformationError(f"{label} must contain exactly three components")
    vector = (float(values[0]), float(values[1]), float(values[2]))
    if not all(math.isfinite(value) for value in vector):
        raise FrameTransformationError(f"{label} must contain finite values")
    return vector


def _canonical_epoch(epoch: datetime) -> datetime:
    if epoch.tzinfo is None or epoch.utcoffset() is None:
        raise FrameTransformationError("epoch must be timezone-aware")
    return epoch.astimezone(UTC)


@contextmanager
def _offline_iers_policy() -> Iterator[None]:
    with (
        iers.conf.set_temp("auto_download", False),
        iers.conf.set_temp("auto_max_age", None),
        iers.conf.set_temp("iers_degraded_accuracy", "error"),
    ):
        yield


def _status_label(status: int) -> str:
    labels = {
        int(iers.FROM_IERS_B): "IERS_B_FINAL",
        int(iers.FROM_IERS_A): "IERS_A_INTERPOLATED",
        int(iers.FROM_IERS_A_PREDICTION): "IERS_A_PREDICTION",
    }
    if status in labels:
        return labels[status]
    if status == int(iers.TIME_BEFORE_IERS_RANGE):
        return "BEFORE_RANGE"
    if status == int(iers.TIME_BEYOND_IERS_RANGE):
        return "BEYOND_RANGE"
    return f"UNKNOWN_{status}"


class OfflineTemeToGcrfTransformer:
    """Transform one complete TEME state using pinned offline Earth-orientation data."""

    def __init__(self) -> None:
        astropy_version = importlib.metadata.version("astropy")
        iers_data_version = importlib.metadata.version("astropy-iers-data")
        if astropy_version != _EXPECTED_ASTROPY_VERSION:
            raise FrameTransformationError(f"astropy version must be {_EXPECTED_ASTROPY_VERSION}")
        if iers_data_version != _EXPECTED_IERS_DATA_VERSION:
            raise FrameTransformationError(
                f"astropy-iers-data version must be {_EXPECTED_IERS_DATA_VERSION}"
            )
        self._astropy_version = astropy_version
        self._iers_data_version = iers_data_version

    def transform(
        self,
        position_km: Sequence[float],
        velocity_km_s: Sequence[float],
        epoch: datetime,
    ) -> FrameTransformResult:
        position = _validated_vector(position_km, "position")
        velocity = _validated_vector(velocity_km_s, "velocity")
        canonical_epoch = _canonical_epoch(epoch)
        input_digest = _canonical_digest(
            {
                "epoch": canonical_epoch.isoformat(),
                "position_km": position,
                "source_frame": "TEME",
                "velocity_km_s": velocity,
            }
        )

        with _TRANSFORM_LOCK, _offline_iers_policy():
            table = iers.IERS_A.read(file=iers.IERS_A_FILE)
            iers_path = Path(iers.IERS_A_FILE)
            if not iers_path.is_file():
                raise FrameTransformationError("pinned IERS data file is unavailable")
            iers_digest = hashlib.sha256(iers_path.read_bytes()).hexdigest()
            mjd_start = float(table["MJD"][0].value)
            mjd_end = float(table["MJD"][-1].value)
            obstime = Time(canonical_epoch, scale="utc")
            epoch_mjd = float(obstime.mjd)
            if not mjd_start <= epoch_mjd <= mjd_end:
                raise FrameTransformationError(
                    "epoch is outside the pinned IERS range; degraded accuracy is forbidden"
                )

            _ut1_value, ut1_status_raw = table.ut1_utc(obstime, return_status=True)
            _pm_x, _pm_y, pm_status_raw = table.pm_xy(obstime, return_status=True)
            ut1_status = int(ut1_status_raw)
            pm_status = int(pm_status_raw)
            if ut1_status < 0 or pm_status < 0:
                raise FrameTransformationError(
                    "epoch is outside the pinned IERS range; degraded accuracy is forbidden"
                )

            with iers.earth_orientation_table.set(table):
                representation = CartesianRepresentation(
                    list(position) * u.km,
                    differentials=CartesianDifferential(list(velocity) * u.km / u.s),
                )
                teme = TEME(representation, obstime=obstime)
                gcrs = teme.transform_to(GCRS(obstime=obstime))
                transformed_position = tuple(
                    float(gcrs.cartesian.xyz[index].to_value(u.km)) for index in range(3)
                )
                differential = gcrs.cartesian.differentials["s"]
                transformed_velocity = tuple(
                    float(differential.d_xyz[index].to_value(u.km / u.s)) for index in range(3)
                )

        position_result: Vector3 = (
            transformed_position[0],
            transformed_position[1],
            transformed_position[2],
        )
        velocity_result: Vector3 = (
            transformed_velocity[0],
            transformed_velocity[1],
            transformed_velocity[2],
        )
        eop_status = f"UT1:{_status_label(ut1_status)};PM:{_status_label(pm_status)}"
        transformation_digest = _canonical_digest(
            {
                "algorithm_id": _ALGORITHM_ID,
                "algorithm_version": _ALGORITHM_VERSION,
                "astropy_version": self._astropy_version,
                "eop_status": eop_status,
                "frame_realization": "ASTROPY_GCRS",
                "iers_data_digest": iers_digest,
                "iers_data_version": self._iers_data_version,
                "input_digest": input_digest,
                "position_km": position_result,
                "target_frame": "GCRF",
                "velocity_km_s": velocity_result,
            }
        )
        return FrameTransformResult(
            epoch=canonical_epoch,
            position_km=position_result,
            velocity_km_s=velocity_result,
            source_frame="TEME",
            target_frame="GCRF",
            frame_realization="ASTROPY_GCRS",
            distance_unit="km",
            velocity_unit="km/s",
            algorithm_id=_ALGORITHM_ID,
            algorithm_version=_ALGORITHM_VERSION,
            astropy_version=self._astropy_version,
            iers_data_version=self._iers_data_version,
            iers_source=iers_path.name,
            iers_mjd_start=mjd_start,
            iers_mjd_end=mjd_end,
            eop_status=eop_status,
            input_digest=input_digest,
            iers_data_digest=iers_digest,
            transformation_digest=transformation_digest,
            advisory_only=True,
        )
