"""
AILORA Synthetic TLE and State Vector Parser.

Parses Two-Line Element sets (TLE) into structured orbital parameters.
This implementation is SYNTHETIC and ADVISORY-ONLY:

Scientific boundary (Prompt 06):
  All outputs are labeled Advisory, Bounded, PHY-C1 (non-normative) until the
  independent qualified Astrodynamics domain review (Prompt 06 CSIP-EO-RS-STAGE-20)
  is completed.  No computed value from this module may be labeled Normative,
  Qualified, or Operationally Authoritative.

Data integrity:
  TLE data must carry DataProvenance records.
  Real TLE data from NASA/CelesTrak requires separate data-access agreements
  and is NOT integrated here.  All demo inputs must use SYNTHETIC data.

No spacecraft command path — permanently denied.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

# ---------------------------------------------------------------------------
# TLE parsing constants
# ---------------------------------------------------------------------------

_EARTH_MU_KM3_S2 = 398_600.4418   # Earth gravitational parameter (km³/s²)
_EARTH_RADIUS_KM = 6_378.137       # Earth equatorial radius (km)
_TWOPI = 2.0 * math.pi


# ---------------------------------------------------------------------------
# Parsed TLE record
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class TLERecord:
    """
    Structured representation of a parsed Two-Line Element set.

    All angle fields are in degrees; mean_motion is in revolutions/day.
    Parsing is SYNTHETIC/ADVISORY-only — see module docstring.

    Fields follow the NORAD TLE standard format:
    https://celestrak.org/NORAD/documentation/tle-fmt.php
    """

    # Metadata
    name: str                      # Satellite name (from TLE line 0)
    catalog_number: str            # NORAD catalog number (field 2, line 1)
    epoch_year: int                # Two-digit epoch year
    epoch_day: float               # Day of epoch year (fractional)
    classification: str            # U = Unclassified

    # Keplerian elements (mean elements — SGP4 mean motion model)
    inclination_deg: float         # Inclination (degrees)
    raan_deg: float                # Right ascension of ascending node (degrees)
    eccentricity: float            # Eccentricity (dimensionless, 0–1)
    arg_perigee_deg: float         # Argument of perigee (degrees)
    mean_anomaly_deg: float        # Mean anomaly at epoch (degrees)
    mean_motion_rev_day: float     # Mean motion (revolutions/day)
    revolution_number: int         # Revolution number at epoch

    # Drag / ballistic coefficient
    bstar_drag: float              # BSTAR drag term (Earth radii⁻¹)

    # Computed from mean motion
    @property
    def semi_major_axis_km(self) -> float:
        """
        Compute semi-major axis (km) from mean motion.

        Formula: a = (µ / n²)^(1/3)  where n is mean motion in rad/s.
        Advisory-only — not normatively validated.
        """
        n_rad_s = (self.mean_motion_rev_day * _TWOPI) / 86_400.0
        return float((_EARTH_MU_KM3_S2 / (n_rad_s * n_rad_s)) ** (1.0 / 3.0))

    @property
    def altitude_km(self) -> float:
        """
        Estimate mean altitude above Earth's surface (km).

        Advisory-only — assumes circular orbit approximation.
        """
        return self.semi_major_axis_km - _EARTH_RADIUS_KM

    @property
    def period_minutes(self) -> float:
        """Orbital period in minutes."""
        return 1_440.0 / self.mean_motion_rev_day


# ---------------------------------------------------------------------------
# TLE parser
# ---------------------------------------------------------------------------


class TLEParseError(ValueError):
    """Raised when a TLE string cannot be parsed."""


def parse_tle(line0: str, line1: str, line2: str) -> TLERecord:
    """
    Parse a Three-line TLE (name + line1 + line2) into a TLERecord.

    This parser handles the standard NORAD TLE format.
    It is SYNTHETIC and ADVISORY-ONLY — see module docstring.

    Args:
        line0: Satellite name (may be empty for two-line format).
        line1: TLE line 1.
        line2: TLE line 2.

    Returns:
        Parsed TLERecord.

    Raises:
        TLEParseError: If any line fails format validation.
    """
    line1 = line1.strip()
    line2 = line2.strip()
    name = line0.strip()

    if len(line1) < 69:
        raise TLEParseError(f"TLE line 1 too short ({len(line1)} chars, expected ≥69)")
    if len(line2) < 69:
        raise TLEParseError(f"TLE line 2 too short ({len(line2)} chars, expected ≥69)")
    if not line1.startswith("1 "):
        raise TLEParseError("TLE line 1 must start with '1 '")
    if not line2.startswith("2 "):
        raise TLEParseError("TLE line 2 must start with '2 '")

    try:
        # Line 1 fields
        catalog_number = line1[2:7].strip()
        classification = line1[7]
        epoch_year = int(line1[18:20])
        epoch_day = float(line1[20:32])
        # BSTAR drag: stored as ±.NNNNN±NN → ±0.NNNNN × 10^±NN
        bstar_str = line1[53:61].strip()
        bstar_drag = _parse_decimal_point(bstar_str)

        # Line 2 fields
        inclination_deg = float(line2[8:16])
        raan_deg = float(line2[17:25])
        eccentricity = float("0." + line2[26:33].strip())
        arg_perigee_deg = float(line2[34:42])
        mean_anomaly_deg = float(line2[43:51])
        mean_motion_rev_day = float(line2[52:63])
        revolution_number = int(line2[63:68].strip() or "0")

    except (ValueError, IndexError) as exc:
        raise TLEParseError(f"TLE parse error: {exc}") from exc

    return TLERecord(
        name=name,
        catalog_number=catalog_number,
        classification=classification,
        epoch_year=epoch_year,
        epoch_day=epoch_day,
        bstar_drag=bstar_drag,
        inclination_deg=inclination_deg,
        raan_deg=raan_deg,
        eccentricity=eccentricity,
        arg_perigee_deg=arg_perigee_deg,
        mean_anomaly_deg=mean_anomaly_deg,
        mean_motion_rev_day=mean_motion_rev_day,
        revolution_number=revolution_number,
    )


def _parse_decimal_point(s: str) -> float:
    """
    Parse the NORAD implied-decimal-point notation.

    Format: ±NNNNN±NN  (no leading decimal, exponent at end)
    Examples:  ' 00000-0' → 0.0,  ' 16538-3' → 0.00016538
    """
    s = s.strip().replace(" ", "")
    if not s or s in ("00000-0", "+00000-0", "-00000-0"):
        return 0.0
    try:
        # Find the last occurrence of + or - as the exponent sign
        # Standard form: ±NNNNN±EE
        sign = 1.0
        if s.startswith("-"):
            sign = -1.0
            s = s[1:]
        elif s.startswith("+"):
            s = s[1:]

        # Find the exponent sign (last + or -)
        exp_pos = max(s.rfind("+"), s.rfind("-"))
        if exp_pos <= 0:
            return float(s) * sign

        mantissa = float("0." + s[:exp_pos])
        exponent = int(s[exp_pos:])
        return sign * mantissa * (10.0**exponent)
    except (ValueError, IndexError):
        return 0.0
