"""
AILORA P1-03: Core Domain Value Object Tests.

Validates Epoch, TemporalStamp, CartesianState, and OrbitalRegime
value objects for correctness, immutability, and validation behaviour.

No database, network, or framework dependency is required.
"""

from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from ailora.domain.shared.value_objects import (
    CartesianState,
    Epoch,
    EpochScale,
    OrbitalRegime,
    ReferenceFrame,
    TemporalStamp,
)

# ─── Epoch ────────────────────────────────────────────────────────────────────


class TestEpoch:
    def test_valid_epoch_creation(self) -> None:
        e = Epoch(iso_utc="2026-08-05T12:00:00.000000Z")
        assert e.iso_utc == "2026-08-05T12:00:00+00:00Z" or "2026-08-05T12:00:00" in e.iso_utc

    def test_epoch_utc_property_is_aware(self) -> None:
        e = Epoch(iso_utc="2026-08-05T00:00:00Z")
        assert e.utc.tzinfo is not None
        assert e.utc.tzinfo == UTC or str(e.utc.tzinfo) in ("UTC", "+00:00")

    def test_epoch_from_datetime(self) -> None:
        dt = datetime(2026, 8, 5, 0, 0, 0, tzinfo=UTC)
        e = Epoch.from_datetime(dt)
        assert "2026-08-05" in e.iso_utc
        assert e.scale == EpochScale.UTC

    def test_epoch_from_naive_datetime_defaults_to_utc(self) -> None:
        dt = datetime(2026, 8, 5, 0, 0, 0)
        e = Epoch.from_datetime(dt)
        assert e.utc.tzinfo is not None

    def test_epoch_invalid_iso_raises(self) -> None:
        with pytest.raises(ValidationError):
            Epoch(iso_utc="not-a-date")

    def test_epoch_immutable(self) -> None:
        e = Epoch(iso_utc="2026-08-05T00:00:00Z")
        with pytest.raises((ValidationError, TypeError)):
            e.iso_utc = "2026-08-06T00:00:00Z"  # type: ignore[misc]

    def test_epoch_scale_default_utc(self) -> None:
        e = Epoch(iso_utc="2026-08-05T00:00:00Z")
        assert e.scale == EpochScale.UTC

    def test_epoch_custom_scale(self) -> None:
        e = Epoch(iso_utc="2026-08-05T00:00:00Z", scale=EpochScale.GPS)
        assert e.scale == EpochScale.GPS

    def test_epoch_equality_by_value(self) -> None:
        e1 = Epoch(iso_utc="2026-08-05T00:00:00Z")
        e2 = Epoch(iso_utc="2026-08-05T00:00:00Z")
        assert e1 == e2

    def test_epoch_ordering_via_utc(self) -> None:
        e1 = Epoch(iso_utc="2026-08-05T00:00:00Z")
        e2 = Epoch(iso_utc="2026-08-06T00:00:00Z")
        assert e1.utc < e2.utc


# ─── TemporalStamp ────────────────────────────────────────────────────────────


class TestTemporalStamp:
    _epoch = Epoch(iso_utc="2026-08-05T12:00:00Z")
    _before = Epoch(iso_utc="2026-08-05T11:00:00Z")
    _after = Epoch(iso_utc="2026-08-05T13:00:00Z")

    def test_basic_creation(self) -> None:
        ts = TemporalStamp(epoch=self._epoch)
        assert ts.epoch == self._epoch
        assert ts.frame == ReferenceFrame.TEME

    def test_frame_override(self) -> None:
        ts = TemporalStamp(epoch=self._epoch, frame=ReferenceFrame.GCRF)
        assert ts.frame == ReferenceFrame.GCRF

    def test_valid_window(self) -> None:
        ts = TemporalStamp(
            epoch=self._epoch,
            valid_start=self._before,
            valid_end=self._after,
        )
        assert ts.valid_start == self._before
        assert ts.valid_end == self._after

    def test_valid_start_after_epoch_raises(self) -> None:
        with pytest.raises(ValidationError):
            TemporalStamp(epoch=self._epoch, valid_start=self._after)

    def test_valid_end_before_epoch_raises(self) -> None:
        with pytest.raises(ValidationError):
            TemporalStamp(epoch=self._epoch, valid_end=self._before)

    def test_valid_start_after_valid_end_raises(self) -> None:
        with pytest.raises(ValidationError):
            TemporalStamp(
                epoch=self._epoch,
                valid_start=self._after,
                valid_end=self._before,
            )

    def test_immutable(self) -> None:
        ts = TemporalStamp(epoch=self._epoch)
        with pytest.raises((ValidationError, TypeError)):
            ts.frame = ReferenceFrame.ITRF  # type: ignore[misc]

    def test_source_label(self) -> None:
        ts = TemporalStamp(epoch=self._epoch, source_label="NORAD TLE 2026-08-05")
        assert ts.source_label == "NORAD TLE 2026-08-05"

    def test_source_label_max_length(self) -> None:
        with pytest.raises(ValidationError):
            TemporalStamp(epoch=self._epoch, source_label="x" * 257)


# ─── CartesianState ───────────────────────────────────────────────────────────


class TestCartesianState:
    _stamp = TemporalStamp(epoch=Epoch(iso_utc="2026-08-05T00:00:00Z"))

    def test_basic_creation(self) -> None:
        cs = CartesianState(
            stamp=self._stamp,
            x_m=7_000_000.0, y_m=0.0, z_m=0.0,
            vx_ms=0.0, vy_ms=7_500.0, vz_ms=0.0,
        )
        assert cs.x_m == 7_000_000.0

    def test_position_magnitude(self) -> None:
        cs = CartesianState(
            stamp=self._stamp,
            x_m=3.0, y_m=4.0, z_m=0.0,
            vx_ms=0.0, vy_ms=0.0, vz_ms=0.0,
        )
        assert abs(cs.position_magnitude_m - 5.0) < 1e-9

    def test_velocity_magnitude(self) -> None:
        cs = CartesianState(
            stamp=self._stamp,
            x_m=0.0, y_m=0.0, z_m=0.0,
            vx_ms=3.0, vy_ms=4.0, vz_ms=0.0,
        )
        assert abs(cs.velocity_magnitude_ms - 5.0) < 1e-9

    def test_immutable(self) -> None:
        cs = CartesianState(
            stamp=self._stamp,
            x_m=1.0, y_m=2.0, z_m=3.0,
            vx_ms=0.0, vy_ms=0.0, vz_ms=0.0,
        )
        with pytest.raises((ValidationError, TypeError)):
            cs.x_m = 999.0  # type: ignore[misc]

    def test_zero_vector(self) -> None:
        cs = CartesianState(
            stamp=self._stamp,
            x_m=0.0, y_m=0.0, z_m=0.0,
            vx_ms=0.0, vy_ms=0.0, vz_ms=0.0,
        )
        assert cs.position_magnitude_m == 0.0
        assert cs.velocity_magnitude_ms == 0.0


# ─── OrbitalRegime ────────────────────────────────────────────────────────────


class TestOrbitalRegime:
    def test_leo_classification(self) -> None:
        assert OrbitalRegime.from_altitude_km(400.0) == OrbitalRegime.LEO
        assert OrbitalRegime.from_altitude_km(1999.9) == OrbitalRegime.LEO

    def test_meo_classification(self) -> None:
        assert OrbitalRegime.from_altitude_km(20_200.0) == OrbitalRegime.MEO

    def test_geo_classification(self) -> None:
        assert OrbitalRegime.from_altitude_km(35_786.0) == OrbitalRegime.GEO
        assert OrbitalRegime.from_altitude_km(35_900.0) == OrbitalRegime.GEO

    def test_above_geo_is_unknown(self) -> None:
        assert OrbitalRegime.from_altitude_km(50_000.0) == OrbitalRegime.UNKNOWN

    def test_negative_altitude_is_unknown(self) -> None:
        assert OrbitalRegime.from_altitude_km(-1.0) == OrbitalRegime.UNKNOWN

    def test_zero_altitude_is_leo(self) -> None:
        assert OrbitalRegime.from_altitude_km(0.0) == OrbitalRegime.LEO

    def test_enum_values(self) -> None:
        regimes = {r.value for r in OrbitalRegime}
        assert {"LEO", "MEO", "GEO", "HEO", "UNKNOWN"}.issubset(regimes)


# ─── ReferenceFrame ───────────────────────────────────────────────────────────


class TestReferenceFrame:
    def test_all_frames_defined(self) -> None:
        frames = {f.value for f in ReferenceFrame}
        assert {"TEME", "GCRF", "ITRF", "EME2000"}.issubset(frames)

    def test_teme_is_default_for_temporal_stamp(self) -> None:
        ts = TemporalStamp(epoch=Epoch(iso_utc="2026-08-05T00:00:00Z"))
        assert ts.frame == ReferenceFrame.TEME
