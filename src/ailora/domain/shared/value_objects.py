"""
AILORA core domain value objects.

These immutable value objects form the shared kernel used across all bounded
contexts.  They carry no framework dependency and depend only on the Python
standard library and Pydantic for validation.

Design rules:
- Value objects are immutable (frozen Pydantic models).
- Equality is by value, not identity.
- No database columns, no HTTP concern, no business logic beyond self-validation.
- All timestamps stored in UTC; display timezone is the caller's concern.
- Physics-First principle: coordinate frames and epochs are explicit, never implicit.
"""

from __future__ import annotations

import math
from datetime import UTC, datetime
from enum import StrEnum

from pydantic import BaseModel, Field, field_validator, model_validator

# ---------------------------------------------------------------------------
# Epoch
# ---------------------------------------------------------------------------


class EpochScale(StrEnum):
    """Supported time scales for orbital epoch representation."""

    UTC = "UTC"
    TAI = "TAI"
    TT = "TT"
    GPS = "GPS"


class Epoch(BaseModel):
    """
    An unambiguous instant in time with an explicit time scale.

    Used wherever an orbital or event timestamp must be physically meaningful.
    The `utc` property always returns a timezone-aware UTC datetime for storage
    and comparison purposes.

    Attributes:
        iso_utc:    ISO 8601 UTC string representation (YYYY-MM-DDTHH:MM:SS.ffffffZ).
        scale:      The time scale in which the epoch is expressed.
    """

    model_config = {"frozen": True}

    iso_utc: str = Field(
        ...,
        description="ISO 8601 UTC datetime string (YYYY-MM-DDTHH:MM:SS[.ffffff]Z)",
        examples=["2026-08-05T00:00:00.000000Z"],
    )
    scale: EpochScale = Field(
        default=EpochScale.UTC,
        description="Time scale of this epoch (default: UTC)",
    )

    @field_validator("iso_utc")
    @classmethod
    def _validate_iso_utc(cls, v: str) -> str:
        """Verify the string is a valid UTC ISO 8601 datetime."""
        try:
            dt = datetime.fromisoformat(v.rstrip("Z").replace("Z", "+00:00"))
        except ValueError as exc:
            raise ValueError(f"iso_utc must be a valid ISO 8601 datetime: {v!r}") from exc
        # Normalise to UTC-aware string
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=UTC)
        return dt.astimezone(UTC).isoformat().replace("+00:00", "Z")

    @property
    def utc(self) -> datetime:
        """Return a timezone-aware UTC datetime object."""
        return datetime.fromisoformat(self.iso_utc.replace("Z", "+00:00"))

    @classmethod
    def from_datetime(cls, dt: datetime, scale: EpochScale = EpochScale.UTC) -> Epoch:
        """Construct an Epoch from a Python datetime (must be UTC-aware or naive-UTC)."""
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=UTC)
        utc_dt = dt.astimezone(UTC)
        return cls(iso_utc=utc_dt.isoformat().replace("+00:00", "Z"), scale=scale)


# ---------------------------------------------------------------------------
# ReferenceFrame
# ---------------------------------------------------------------------------


class ReferenceFrame(StrEnum):
    """
    Supported coordinate reference frames.

    TEME  — True Equator Mean Equinox (default for TLE-derived vectors)
    GCRF  — Geocentric Celestial Reference Frame (inertial)
    ITRF  — International Terrestrial Reference Frame (Earth-fixed)
    EME2000 — Earth Mean Equator and Equinox of J2000 (J2000)
    """

    TEME = "TEME"
    GCRF = "GCRF"
    ITRF = "ITRF"
    EME2000 = "EME2000"


# ---------------------------------------------------------------------------
# TemporalStamp
# ---------------------------------------------------------------------------


class TemporalStamp(BaseModel):
    """
    A complete temporal context for an observation or event.

    Combines an Epoch (instant in time) with an optional validity window,
    a reference frame declaration, and data provenance metadata.

    Attributes:
        epoch:          The primary instant.
        frame:          The reference frame for any associated spatial data.
        valid_start:    Optional start of validity window (≤ epoch).
        valid_end:      Optional end of validity window (≥ epoch).
        source_label:   Human-readable provenance label (e.g. "NORAD TLE 2026-08-05").
    """

    model_config = {"frozen": True}

    epoch: Epoch
    frame: ReferenceFrame = Field(
        default=ReferenceFrame.TEME,
        description="Reference frame for associated spatial data",
    )
    valid_start: Epoch | None = Field(
        default=None,
        description="Start of validity window — must be ≤ epoch if provided",
    )
    valid_end: Epoch | None = Field(
        default=None,
        description="End of validity window — must be ≥ epoch if provided",
    )
    source_label: str = Field(
        default="",
        max_length=256,
        description="Human-readable provenance label for this timestamp",
    )

    @model_validator(mode="after")
    def _validate_validity_window(self) -> TemporalStamp:
        """Ensure valid_start ≤ epoch ≤ valid_end when both are provided."""
        if self.valid_start is not None and self.valid_start.utc > self.epoch.utc:
            raise ValueError("valid_start must be ≤ epoch")
        if self.valid_end is not None and self.valid_end.utc < self.epoch.utc:
            raise ValueError("valid_end must be ≥ epoch")
        if (
            self.valid_start is not None
            and self.valid_end is not None
            and self.valid_start.utc > self.valid_end.utc
        ):
            raise ValueError("valid_start must be ≤ valid_end")
        return self


# ---------------------------------------------------------------------------
# CartesianState
# ---------------------------------------------------------------------------


class CartesianState(BaseModel):
    """
    A Cartesian position/velocity state vector in a specified reference frame.

    All components are in SI units (metres, metres-per-second).
    Used as input to propagation and conjunction screening algorithms.

    Attributes:
        stamp:  Temporal context (epoch + frame).
        x_m:    Position X component (metres).
        y_m:    Position Y component (metres).
        z_m:    Position Z component (metres).
        vx_ms:  Velocity X component (m/s).
        vy_ms:  Velocity Y component (m/s).
        vz_ms:  Velocity Z component (m/s).
    """

    model_config = {"frozen": True}

    stamp: TemporalStamp
    x_m: float = Field(..., description="Position X in metres")
    y_m: float = Field(..., description="Position Y in metres")
    z_m: float = Field(..., description="Position Z in metres")
    vx_ms: float = Field(..., description="Velocity X in m/s")
    vy_ms: float = Field(..., description="Velocity Y in m/s")
    vz_ms: float = Field(..., description="Velocity Z in m/s")

    @property
    def position_magnitude_m(self) -> float:
        """Euclidean magnitude of the position vector (metres)."""
        return math.sqrt(self.x_m**2 + self.y_m**2 + self.z_m**2)

    @property
    def velocity_magnitude_ms(self) -> float:
        """Euclidean magnitude of the velocity vector (m/s)."""
        return math.sqrt(self.vx_ms**2 + self.vy_ms**2 + self.vz_ms**2)


# ---------------------------------------------------------------------------
# OrbitalRegime
# ---------------------------------------------------------------------------

_LEO_ALT_MAX_KM = 2_000.0
_GEO_ALT_KM = 35_786.0
_GEO_TOLERANCE_KM = 200.0
_MEO_UPPER_KM = _GEO_ALT_KM + _GEO_TOLERANCE_KM  # MEO upper bound (exclusive of GEO band)


class OrbitalRegime(StrEnum):
    """
    Orbital regime classification.

    Per Prompt 01 and project-identity.yaml:
    Active regimes: LEO · MEO · GEO · HEO.
    """

    LEO = "LEO"  # Low Earth Orbit   (< 2 000 km altitude)
    MEO = "MEO"  # Medium Earth Orbit (2 000 – 35 786 km)
    GEO = "GEO"  # Geostationary Orbit (~35 786 km ± 200 km)
    HEO = "HEO"  # Highly Elliptical Orbit (defined by eccentricity, not altitude)
    UNKNOWN = "UNKNOWN"

    @classmethod
    def from_altitude_km(cls, altitude_km: float) -> OrbitalRegime:
        """
        Classify an orbital regime from altitude (km above Earth's surface).

        Note: HEO cannot be reliably inferred from a single altitude value;
        this method returns UNKNOWN for altitudes well above GEO.
        """
        if altitude_km < 0:
            return cls.UNKNOWN
        if altitude_km <= _LEO_ALT_MAX_KM:
            return cls.LEO
        # GEO band check (applies before MEO upper bound)
        if abs(altitude_km - _GEO_ALT_KM) <= _GEO_TOLERANCE_KM:
            return cls.GEO
        if altitude_km <= _MEO_UPPER_KM:
            return cls.MEO
        return cls.UNKNOWN
