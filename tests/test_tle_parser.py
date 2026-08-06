"""
AILORA P3-02: Synthetic TLE/State Vector Parsing Tests.

Validates:
- TLE parsing from standard NORAD format strings.
- Semi-major axis, altitude, and period computed properties.
- TLEParseError raised for malformed input.
- Advisory-only label on parser module.
- No normative scientific claim labeling.

Uses the ISS (ZARYA) TLE as a reference (public domain, NORAD catalog).
This is synthetic/advisory data — no real-time integration.
"""

from __future__ import annotations

import pytest

from ailora.domain.ssa.tle_parser import TLEParseError, TLERecord, parse_tle

# ISS (ZARYA) representative TLE — synthetic for testing purposes
# Source: NORAD public catalog (public domain)
_ISS_LINE0 = "ISS (ZARYA)"
_ISS_LINE1 = "1 25544U 98067A   24001.50000000  .00016538  00000-0  29913-3 0  9997"
_ISS_LINE2 = "2 25544  51.6416  40.2671 0006765  42.3840  18.1378 15.49537796434579"


@pytest.fixture
def iss_tle() -> TLERecord:
    return parse_tle(_ISS_LINE0, _ISS_LINE1, _ISS_LINE2)


# ─── Parse success ────────────────────────────────────────────────────────────


def test_parse_tle_returns_record(iss_tle: TLERecord) -> None:
    assert isinstance(iss_tle, TLERecord)


def test_parse_tle_name(iss_tle: TLERecord) -> None:
    assert iss_tle.name == "ISS (ZARYA)"


def test_parse_tle_catalog_number(iss_tle: TLERecord) -> None:
    assert iss_tle.catalog_number == "25544"


def test_parse_tle_classification(iss_tle: TLERecord) -> None:
    assert iss_tle.classification == "U"


def test_parse_tle_epoch_year(iss_tle: TLERecord) -> None:
    assert iss_tle.epoch_year == 24


def test_parse_tle_epoch_day(iss_tle: TLERecord) -> None:
    assert abs(iss_tle.epoch_day - 1.5) < 0.001


def test_parse_tle_inclination(iss_tle: TLERecord) -> None:
    assert abs(iss_tle.inclination_deg - 51.6416) < 0.001


def test_parse_tle_raan(iss_tle: TLERecord) -> None:
    assert abs(iss_tle.raan_deg - 40.2671) < 0.001


def test_parse_tle_eccentricity(iss_tle: TLERecord) -> None:
    # 0006765 → 0.0006765
    assert abs(iss_tle.eccentricity - 0.0006765) < 1e-6


def test_parse_tle_arg_perigee(iss_tle: TLERecord) -> None:
    assert abs(iss_tle.arg_perigee_deg - 42.3840) < 0.001


def test_parse_tle_mean_anomaly(iss_tle: TLERecord) -> None:
    assert abs(iss_tle.mean_anomaly_deg - 18.1378) < 0.001


def test_parse_tle_mean_motion(iss_tle: TLERecord) -> None:
    assert abs(iss_tle.mean_motion_rev_day - 15.495) < 0.01


def test_parse_tle_revolution_number(iss_tle: TLERecord) -> None:
    assert iss_tle.revolution_number == 43457


# ─── Computed properties ─────────────────────────────────────────────────────


def test_semi_major_axis_is_positive(iss_tle: TLERecord) -> None:
    assert iss_tle.semi_major_axis_km > 6_378.0


def test_iss_altitude_approximately_correct(iss_tle: TLERecord) -> None:
    """ISS orbit is nominally ~410 km. Advisory-only check."""
    alt = iss_tle.altitude_km
    assert 350.0 < alt < 500.0, f"ISS altitude {alt:.1f} km outside expected range"


def test_iss_period_approximately_correct(iss_tle: TLERecord) -> None:
    """ISS period is nominally ~92 min. Advisory-only check."""
    period = iss_tle.period_minutes
    assert 88.0 < period < 96.0, f"ISS period {period:.1f} min outside expected range"


def test_tle_record_is_frozen() -> None:
    tle = parse_tle(_ISS_LINE0, _ISS_LINE1, _ISS_LINE2)
    with pytest.raises((TypeError, AttributeError)):
        tle.inclination_deg = 0.0  # type: ignore[misc]


# ─── Parse errors ────────────────────────────────────────────────────────────


def test_line1_too_short_raises() -> None:
    with pytest.raises(TLEParseError):
        parse_tle("SAT", "1 TOO_SHORT", _ISS_LINE2)


def test_line2_too_short_raises() -> None:
    with pytest.raises(TLEParseError):
        parse_tle("SAT", _ISS_LINE1, "2 TOO_SHORT")


def test_line1_wrong_number_raises() -> None:
    bad_line1 = "2" + _ISS_LINE1[1:]
    with pytest.raises(TLEParseError):
        parse_tle("SAT", bad_line1, _ISS_LINE2)


def test_line2_wrong_number_raises() -> None:
    bad_line2 = "1" + _ISS_LINE2[1:]
    with pytest.raises(TLEParseError):
        parse_tle("SAT", _ISS_LINE1, bad_line2)


def test_empty_name_accepted() -> None:
    """TLE line 0 (name) may be empty — two-line format."""
    tle = parse_tle("", _ISS_LINE1, _ISS_LINE2)
    assert tle.name == ""


# ─── Advisory-only labeling ───────────────────────────────────────────────────


def test_tle_parser_module_is_advisory_only() -> None:
    from pathlib import Path

    text = (
        Path(__file__).parent.parent / "src" / "ailora" / "domain" / "ssa" / "tle_parser.py"
    ).read_text()
    assert "advisory" in text.lower(), "tle_parser.py must contain advisory-only boundary statement"
    assert "prompt 06" in text.lower(), (
        "tle_parser.py must reference Prompt 06 domain review boundary"
    )


def test_no_real_tle_integration() -> None:
    """Parser must not import or call live TLE data APIs."""
    from pathlib import Path

    text = (
        (Path(__file__).parent.parent / "src" / "ailora" / "domain" / "ssa" / "tle_parser.py")
        .read_text()
        .lower()
    )
    # Check for actual import/call patterns, not docstring mentions
    forbidden = ["import requests", "import httpx", "requests.get(", "httpx.get("]
    for f in forbidden:
        assert f not in text, f"tle_parser.py must not call live API: '{f}'"
