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
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from enum import StrEnum
from pathlib import Path
from typing import Final

import astropy.units as u
import erfa
from astropy.coordinates import (
    GCRS,
    ITRS,
    TEME,
    CartesianDifferential,
    CartesianRepresentation,
)
from astropy.time import Time
from astropy.utils import iers

Vector3 = tuple[float, float, float]

_DIGEST: Final[re.Pattern[str]] = re.compile(r"^[0-9a-f]{64}$")
_TRANSFORM_LOCK: Final = threading.RLock()
_EXPECTED_ASTROPY_VERSION: Final[str] = "8.0.1"
_EXPECTED_IERS_DATA_VERSION: Final[str] = "0.2026.8.10.0.32.39"
_EXPECTED_PYERFA_VERSION: Final[str] = "2.0.1.5"
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


def _canonical_digest(payload: object) -> str:
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


class ScientificTimeScale(StrEnum):
    """Explicit time scales admitted by the bounded ENT-012 contract."""

    UTC = "UTC"
    TAI = "TAI"
    TT = "TT"
    UT1 = "UT1"


@dataclass(frozen=True, slots=True)
class TimeScaleValue:
    """One instant represented explicitly in one scientific time scale."""

    scale: ScientificTimeScale
    isot: str
    jd1: float
    jd2: float
    mjd: float

    def __post_init__(self) -> None:
        if not self.isot:
            raise ValueError("time-scale representation must be non-empty")
        if not all(math.isfinite(value) for value in (self.jd1, self.jd2, self.mjd)):
            raise ValueError("time-scale values must be finite")


@dataclass(frozen=True, slots=True)
class EarthOrientationLineage:
    """Pinned EOP identity, range, status and values used for one qualification."""

    source: str
    data_version: str
    data_digest: str
    mjd_start: float
    mjd_end: float
    ut1_minus_utc_seconds: float
    polar_motion_x_arcsec: float
    polar_motion_y_arcsec: float
    ut1_status: str
    polar_motion_status: str
    lineage_digest: str

    def __post_init__(self) -> None:
        if self.source != "finals2000A.all":
            raise ValueError("EOP source must be the pinned finals2000A.all dataset")
        if self.data_version != _EXPECTED_IERS_DATA_VERSION:
            raise ValueError("EOP data version does not match the pinned runtime")
        for numeric_value in (
            self.mjd_start,
            self.mjd_end,
            self.ut1_minus_utc_seconds,
            self.polar_motion_x_arcsec,
            self.polar_motion_y_arcsec,
        ):
            if not math.isfinite(numeric_value):
                raise ValueError("EOP lineage values must be finite")
        if self.mjd_start >= self.mjd_end:
            raise ValueError("EOP lineage range is invalid")
        if not self.ut1_status.startswith("IERS_") or not self.polar_motion_status.startswith(
            "IERS_"
        ):
            raise ValueError("EOP lineage cannot contain degraded or unknown status")
        for digest_value in (self.data_digest, self.lineage_digest):
            if not _DIGEST.fullmatch(digest_value):
                raise ValueError("EOP lineage digests must be lowercase SHA-256")


@dataclass(frozen=True, slots=True)
class LeapSecondLineage:
    """Pinned PyERFA leap-second table identity and epoch offset."""

    source: str
    pyerfa_version: str
    table_digest: str
    record_count: int
    first_record: tuple[int, int, float]
    last_record: tuple[int, int, float]
    tai_minus_utc_seconds: float
    lineage_digest: str

    def __post_init__(self) -> None:
        if self.source != "PYERFA_EMBEDDED_TABLE":
            raise ValueError("leap-second source must be the embedded PyERFA table")
        if self.pyerfa_version != _EXPECTED_PYERFA_VERSION:
            raise ValueError("PyERFA version does not match the pinned runtime")
        if self.record_count <= 0:
            raise ValueError("leap-second table must be non-empty")
        if not math.isfinite(self.tai_minus_utc_seconds) or self.tai_minus_utc_seconds <= 0:
            raise ValueError("TAI-UTC offset must be finite and positive")
        for value in (self.table_digest, self.lineage_digest):
            if not _DIGEST.fullmatch(value):
                raise ValueError("leap-second lineage digests must be lowercase SHA-256")


@dataclass(frozen=True, slots=True)
class ItrfTransformResult:
    """Earth-fixed ITRF candidate realized by pinned Astropy ITRS."""

    epoch: datetime
    position_km: Vector3
    velocity_km_s: Vector3
    source_frame: str
    target_frame: str
    frame_realization: str
    distance_unit: str
    velocity_unit: str
    transformation_digest: str

    def __post_init__(self) -> None:
        if self.epoch.tzinfo is None or self.epoch.utcoffset() is None:
            raise ValueError("ITRF epoch must be timezone-aware")
        if self.source_frame != "TEME" or self.target_frame != "ITRF":
            raise ValueError("ITRF result must represent a TEME-to-ITRF conversion")
        if self.frame_realization != "ASTROPY_ITRS":
            raise ValueError("ITRF realization must be ASTROPY_ITRS")
        if self.distance_unit != "km" or self.velocity_unit != "km/s":
            raise ValueError("ITRF units must be km and km/s")
        if not all(math.isfinite(value) for value in (*self.position_km, *self.velocity_km_s)):
            raise ValueError("ITRF result must contain finite values")
        if not _DIGEST.fullmatch(self.transformation_digest):
            raise ValueError("ITRF transformation digest must be lowercase SHA-256")


@dataclass(frozen=True, slots=True)
class TimeAndItrfQualification:
    """Local ENT-012 evidence without independent scientific authority."""

    source_epoch_utc: datetime
    time_scales: tuple[TimeScaleValue, ...]
    tt_minus_tai_seconds: float
    eop_lineage: EarthOrientationLineage
    leap_second_lineage: LeapSecondLineage
    itrf: ItrfTransformResult
    regression_fixture_classification: str
    independent_truth_verified: bool
    qualification_digest: str
    advisory_only: bool

    def __post_init__(self) -> None:
        expected_scales = tuple(ScientificTimeScale)
        if tuple(value.scale for value in self.time_scales) != expected_scales:
            raise ValueError("time scales must be exactly UTC, TAI, TT and UT1")
        if self.tt_minus_tai_seconds != 32.184:
            raise ValueError("TT-TAI must use the defined 32.184 second offset")
        if self.regression_fixture_classification != "PINNED_SAME_ENGINE_REGRESSION":
            raise ValueError("qualification must remain a same-engine regression fixture")
        if self.independent_truth_verified is not False:
            raise ValueError("independent truth remains externally gated")
        if self.advisory_only is not True:
            raise ValueError("time and frame qualification must remain advisory-only")
        if not _DIGEST.fullmatch(self.qualification_digest):
            raise ValueError("qualification digest must be lowercase SHA-256")


def _time_scale_value(value: Time, scale: ScientificTimeScale) -> TimeScaleValue:
    scaled = getattr(value, scale.value.lower())
    scaled.precision = 9
    return TimeScaleValue(
        scale=scale,
        isot=str(scaled.isot),
        jd1=float(scaled.jd1),
        jd2=float(scaled.jd2),
        mjd=float(scaled.mjd),
    )


class OfflineTimeScaleItrfQualifier:
    """Build pinned UTC/TAI/TT/UT1, EOP, leap-second and ITRF local evidence."""

    def __init__(self) -> None:
        versions = {
            "astropy": (_EXPECTED_ASTROPY_VERSION, importlib.metadata.version("astropy")),
            "astropy-iers-data": (
                _EXPECTED_IERS_DATA_VERSION,
                importlib.metadata.version("astropy-iers-data"),
            ),
            "pyerfa": (_EXPECTED_PYERFA_VERSION, importlib.metadata.version("pyerfa")),
        }
        mismatches = [name for name, (expected, actual) in versions.items() if expected != actual]
        if mismatches:
            raise FrameTransformationError(
                "pinned scientific dependency mismatch: " + ",".join(mismatches)
            )
        self._astropy_version = versions["astropy"][1]
        self._iers_data_version = versions["astropy-iers-data"][1]
        self._pyerfa_version = versions["pyerfa"][1]

    def qualify(
        self,
        position_km: Sequence[float],
        velocity_km_s: Sequence[float],
        epoch: datetime,
    ) -> TimeAndItrfQualification:
        position = _validated_vector(position_km, "position")
        velocity = _validated_vector(velocity_km_s, "velocity")
        canonical_epoch = _canonical_epoch(epoch)

        with _TRANSFORM_LOCK, _offline_iers_policy():
            iers_path = Path(iers.IERS_A_FILE)
            if not iers_path.is_file():
                raise FrameTransformationError("pinned IERS data file is unavailable")
            iers_digest = hashlib.sha256(iers_path.read_bytes()).hexdigest()
            table = iers.IERS_A.read(file=iers_path)
            mjd_start = float(table["MJD"][0].value)
            mjd_end = float(table["MJD"][-1].value)

            leap_table = iers.LeapSeconds.from_erfa()
            leap_records = [
                {
                    "year": int(row["year"]),
                    "month": int(row["month"]),
                    "tai_utc": float(row["tai_utc"]),
                }
                for row in leap_table
            ]
            if not leap_records:
                raise FrameTransformationError("pinned leap-second table is empty")
            leap_table_digest = _canonical_digest(leap_records)

            obstime = Time(canonical_epoch, scale="utc", precision=9)
            epoch_mjd = float(obstime.mjd)
            if not mjd_start <= epoch_mjd <= mjd_end:
                raise FrameTransformationError(
                    "epoch is outside the pinned IERS range; degraded accuracy is forbidden"
                )

            with iers.earth_orientation_table.set(table):
                time_scales = tuple(
                    _time_scale_value(obstime, scale) for scale in ScientificTimeScale
                )
                ut1_value, ut1_status_raw = table.ut1_utc(obstime, return_status=True)
                pm_x, pm_y, pm_status_raw = table.pm_xy(obstime, return_status=True)
                ut1_status = int(ut1_status_raw)
                pm_status = int(pm_status_raw)
                if ut1_status < 0 or pm_status < 0:
                    raise FrameTransformationError(
                        "epoch is outside the pinned IERS range; degraded accuracy is forbidden"
                    )

                source = TEME(
                    CartesianRepresentation(
                        list(position) * u.km,
                        differentials=CartesianDifferential(list(velocity) * u.km / u.s),
                    ),
                    obstime=obstime,
                )
                transformed = source.transform_to(ITRS(obstime=obstime))
                transformed_position = tuple(
                    float(transformed.cartesian.xyz[index].to_value(u.km)) for index in range(3)
                )
                differential = transformed.cartesian.differentials["s"]
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
        fraction_of_day = (
            canonical_epoch.hour * 3600
            + canonical_epoch.minute * 60
            + canonical_epoch.second
            + canonical_epoch.microsecond / 1_000_000
        ) / 86400.0
        tai_minus_utc = float(
            erfa.dat(
                canonical_epoch.year,
                canonical_epoch.month,
                canonical_epoch.day,
                fraction_of_day,
            )
        )

        eop_payload = {
            "source": iers_path.name,
            "data_version": self._iers_data_version,
            "data_digest": iers_digest,
            "mjd_start": mjd_start,
            "mjd_end": mjd_end,
            "ut1_minus_utc_seconds": float(ut1_value.to_value(u.s)),
            "polar_motion_x_arcsec": float(pm_x.to_value(u.arcsec)),
            "polar_motion_y_arcsec": float(pm_y.to_value(u.arcsec)),
            "ut1_status": _status_label(ut1_status),
            "polar_motion_status": _status_label(pm_status),
        }
        eop_lineage = EarthOrientationLineage(
            source=iers_path.name,
            data_version=self._iers_data_version,
            data_digest=iers_digest,
            mjd_start=mjd_start,
            mjd_end=mjd_end,
            ut1_minus_utc_seconds=float(ut1_value.to_value(u.s)),
            polar_motion_x_arcsec=float(pm_x.to_value(u.arcsec)),
            polar_motion_y_arcsec=float(pm_y.to_value(u.arcsec)),
            ut1_status=_status_label(ut1_status),
            polar_motion_status=_status_label(pm_status),
            lineage_digest=_canonical_digest(eop_payload),
        )
        first_leap = leap_records[0]
        last_leap = leap_records[-1]
        leap_payload = {
            "source": "PYERFA_EMBEDDED_TABLE",
            "pyerfa_version": self._pyerfa_version,
            "table_digest": leap_table_digest,
            "record_count": len(leap_records),
            "first_record": (
                first_leap["year"],
                first_leap["month"],
                first_leap["tai_utc"],
            ),
            "last_record": (
                last_leap["year"],
                last_leap["month"],
                last_leap["tai_utc"],
            ),
            "tai_minus_utc_seconds": tai_minus_utc,
        }
        leap_lineage = LeapSecondLineage(
            source="PYERFA_EMBEDDED_TABLE",
            pyerfa_version=self._pyerfa_version,
            table_digest=leap_table_digest,
            record_count=len(leap_records),
            first_record=(
                int(first_leap["year"]),
                int(first_leap["month"]),
                float(first_leap["tai_utc"]),
            ),
            last_record=(
                int(last_leap["year"]),
                int(last_leap["month"]),
                float(last_leap["tai_utc"]),
            ),
            tai_minus_utc_seconds=tai_minus_utc,
            lineage_digest=_canonical_digest(leap_payload),
        )
        itrf_payload = {
            "epoch": canonical_epoch.isoformat(),
            "position_km": position_result,
            "velocity_km_s": velocity_result,
            "source_frame": "TEME",
            "target_frame": "ITRF",
            "frame_realization": "ASTROPY_ITRS",
            "distance_unit": "km",
            "velocity_unit": "km/s",
            "astropy_version": self._astropy_version,
            "eop_lineage_digest": eop_lineage.lineage_digest,
            "leap_second_lineage_digest": leap_lineage.lineage_digest,
        }
        itrf = ItrfTransformResult(
            epoch=canonical_epoch,
            position_km=position_result,
            velocity_km_s=velocity_result,
            source_frame="TEME",
            target_frame="ITRF",
            frame_realization="ASTROPY_ITRS",
            distance_unit="km",
            velocity_unit="km/s",
            transformation_digest=_canonical_digest(itrf_payload),
        )
        qualification_payload = {
            "source_epoch_utc": canonical_epoch.isoformat(),
            "time_scales": [asdict(value) for value in time_scales],
            "tt_minus_tai_seconds": 32.184,
            "eop_lineage": asdict(eop_lineage),
            "leap_second_lineage": asdict(leap_lineage),
            "itrf": {
                "epoch": itrf.epoch.isoformat(),
                "position_km": itrf.position_km,
                "velocity_km_s": itrf.velocity_km_s,
                "source_frame": itrf.source_frame,
                "target_frame": itrf.target_frame,
                "frame_realization": itrf.frame_realization,
                "distance_unit": itrf.distance_unit,
                "velocity_unit": itrf.velocity_unit,
                "transformation_digest": itrf.transformation_digest,
            },
            "regression_fixture_classification": "PINNED_SAME_ENGINE_REGRESSION",
            "independent_truth_verified": False,
            "advisory_only": True,
        }
        return TimeAndItrfQualification(
            source_epoch_utc=canonical_epoch,
            time_scales=time_scales,
            tt_minus_tai_seconds=32.184,
            eop_lineage=eop_lineage,
            leap_second_lineage=leap_lineage,
            itrf=itrf,
            regression_fixture_classification="PINNED_SAME_ENGINE_REGRESSION",
            independent_truth_verified=False,
            qualification_digest=_canonical_digest(qualification_payload),
            advisory_only=True,
        )
