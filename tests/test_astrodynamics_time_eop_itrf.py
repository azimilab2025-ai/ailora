from __future__ import annotations

import socket
import urllib.request
from dataclasses import replace
from datetime import UTC, datetime, timedelta, timezone
from pathlib import Path
from typing import NoReturn

import astropy.units as u
import pytest
from astropy.coordinates import ITRS, TEME, CartesianDifferential, CartesianRepresentation
from astropy.time import Time
from astropy.utils import iers

from ailora.services.astrodynamics.frame_transform import (
    FrameTransformationError,
    OfflineTimeScaleItrfQualifier,
    ScientificTimeScale,
    TimeAndItrfQualification,
)

EPOCH = datetime(2000, 6, 27, 18, 50, 19, 733568, tzinfo=UTC)
POSITION_KM = (7022.46529266, -1400.08296755, 0.03995155)
VELOCITY_KM_S = (1.893841015, 6.405893759, 4.534807250)
EXPECTED_IERS_DIGEST = "4b828090fc94114168014b61439fa5e6ec0bdfda518075a32baffea90110954d"
EXPECTED_LEAP_DIGEST = "6330bd57c2998057ae64d64ac12280c0b94a4429315c49f66f5e569579e08dec"


@pytest.fixture(scope="module")
def qualified() -> TimeAndItrfQualification:
    return OfflineTimeScaleItrfQualifier().qualify(POSITION_KM, VELOCITY_KM_S, EPOCH)


def test_all_four_time_scales_are_explicit_and_probe_bound(
    qualified: TimeAndItrfQualification,
) -> None:
    values = {value.scale: value for value in qualified.time_scales}
    assert tuple(values) == (
        ScientificTimeScale.UTC,
        ScientificTimeScale.TAI,
        ScientificTimeScale.TT,
        ScientificTimeScale.UT1,
    )
    assert values[ScientificTimeScale.UTC].isot == "2000-06-27T18:50:19.733568000"
    assert values[ScientificTimeScale.TAI].isot == "2000-06-27T18:50:51.733568000"
    assert values[ScientificTimeScale.TT].isot == "2000-06-27T18:51:23.917568000"
    assert values[ScientificTimeScale.UT1].isot == "2000-06-27T18:50:19.938531278"


def test_time_offsets_are_explicit_and_bounded(qualified: TimeAndItrfQualification) -> None:
    assert qualified.leap_second_lineage.tai_minus_utc_seconds == 32.0
    assert qualified.tt_minus_tai_seconds == 32.184
    assert qualified.eop_lineage.ut1_minus_utc_seconds == pytest.approx(0.204963277567, abs=1e-12)


def test_eop_lineage_is_pinned_digest_bound_and_non_degraded(
    qualified: TimeAndItrfQualification,
) -> None:
    lineage = qualified.eop_lineage
    assert lineage.source == "finals2000A.all"
    assert lineage.data_version == "0.2026.8.10.0.32.39"
    assert lineage.data_digest == EXPECTED_IERS_DIGEST
    assert lineage.mjd_start == 41684.0
    assert lineage.mjd_end == 61624.0
    assert lineage.ut1_status == "IERS_B_FINAL"
    assert lineage.polar_motion_status == "IERS_B_FINAL"
    assert lineage.polar_motion_x_arcsec == pytest.approx(0.109406023829, abs=1e-12)
    assert lineage.polar_motion_y_arcsec == pytest.approx(0.284270316663, abs=1e-12)
    assert len(lineage.lineage_digest) == 64


def test_leap_second_lineage_is_explicit_and_pyerfa_bound(
    qualified: TimeAndItrfQualification,
) -> None:
    lineage = qualified.leap_second_lineage
    assert lineage.source == "PYERFA_EMBEDDED_TABLE"
    assert lineage.pyerfa_version == "2.0.1.5"
    assert lineage.table_digest == EXPECTED_LEAP_DIGEST
    assert lineage.record_count == 42
    assert lineage.first_record == (1960, 1, 1.417818)
    assert lineage.last_record == (2017, 1, 37.0)
    assert len(lineage.lineage_digest) == 64


def test_leap_second_boundary_preserves_the_inserted_utc_second() -> None:
    with iers.conf.set_temp("auto_download", False):
        before = Time("2016-12-31T23:59:59", format="isot", scale="utc")
        leap = Time("2016-12-31T23:59:60", format="isot", scale="utc")
        after = Time("2017-01-01T00:00:00", format="isot", scale="utc")
        assert (leap - before).to_value(u.s) == pytest.approx(1.0, abs=1e-9)
        assert (after - leap).to_value(u.s) == pytest.approx(1.0, abs=1e-9)
        assert leap.tai.isot.startswith("2017-01-01T00:00:36")


def test_pinned_same_engine_itrf_regression_is_stable_but_not_independent(
    qualified: TimeAndItrfQualification,
) -> None:
    result = qualified.itrf
    assert result.target_frame == "ITRF"
    assert result.frame_realization == "ASTROPY_ITRS"
    assert result.position_km == pytest.approx(
        (-6198.504083386169, 3585.219411717737, 0.04818041450585745), abs=1e-8
    )
    assert result.velocity_km_s == pytest.approx(
        (-3.592886104925128, -5.00385175763995, 4.534802259424364), abs=1e-11
    )
    assert qualified.regression_fixture_classification == "PINNED_SAME_ENGINE_REGRESSION"
    assert qualified.independent_truth_verified is False
    assert qualified.advisory_only is True


def test_itrf_roundtrip_recovers_native_teme_state(
    qualified: TimeAndItrfQualification,
) -> None:
    obstime = Time(EPOCH, scale="utc")
    result = qualified.itrf
    representation = CartesianRepresentation(
        list(result.position_km) * u.km,
        differentials=CartesianDifferential(list(result.velocity_km_s) * u.km / u.s),
    )
    table = iers.IERS_A.read(file=iers.IERS_A_FILE)
    with (
        iers.conf.set_temp("auto_download", False),
        iers.conf.set_temp("auto_max_age", None),
        iers.conf.set_temp("iers_degraded_accuracy", "error"),
        iers.earth_orientation_table.set(table),
    ):
        recovered = ITRS(representation, obstime=obstime).transform_to(TEME(obstime=obstime))
    recovered_position = tuple(
        float(recovered.cartesian.xyz[index].to_value(u.km)) for index in range(3)
    )
    differential = recovered.cartesian.differentials["s"]
    recovered_velocity = tuple(
        float(differential.d_xyz[index].to_value(u.km / u.s)) for index in range(3)
    )
    assert recovered_position == pytest.approx(POSITION_KM, abs=1e-8)
    assert recovered_velocity == pytest.approx(VELOCITY_KM_S, abs=1e-11)


def test_qualification_is_deterministic_and_timezone_canonical() -> None:
    qualifier = OfflineTimeScaleItrfQualifier()
    offset = timezone(timedelta(hours=3, minutes=30))
    assert qualifier.qualify(POSITION_KM, VELOCITY_KM_S, EPOCH) == qualifier.qualify(
        POSITION_KM, VELOCITY_KM_S, EPOCH.astimezone(offset)
    )


def test_independent_truth_overclaim_is_rejected(
    qualified: TimeAndItrfQualification,
) -> None:
    with pytest.raises(ValueError, match="independent truth remains externally gated"):
        replace(qualified, independent_truth_verified=True)
    with pytest.raises(ValueError, match="same-engine regression"):
        replace(qualified, regression_fixture_classification="INDEPENDENT_TRUTH")


def test_network_is_forbidden_during_time_eop_itrf_qualification(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def blocked(*_args: object, **_kwargs: object) -> NoReturn:
        raise AssertionError("network access is forbidden during qualification")

    monkeypatch.setattr(socket, "create_connection", blocked)
    monkeypatch.setattr(urllib.request, "urlopen", blocked)
    result = OfflineTimeScaleItrfQualifier().qualify(POSITION_KM, VELOCITY_KM_S, EPOCH)
    assert result.itrf.target_frame == "ITRF"


def test_invalid_inputs_and_out_of_range_epochs_fail_closed() -> None:
    qualifier = OfflineTimeScaleItrfQualifier()
    with pytest.raises(FrameTransformationError, match="outside the pinned IERS range"):
        qualifier.qualify(POSITION_KM, VELOCITY_KM_S, datetime(1970, 1, 1, tzinfo=UTC))
    with pytest.raises(FrameTransformationError, match="exactly three"):
        qualifier.qualify((1.0, 2.0), VELOCITY_KM_S, EPOCH)
    with pytest.raises(FrameTransformationError, match="timezone-aware"):
        qualifier.qualify(POSITION_KM, VELOCITY_KM_S, EPOCH.replace(tzinfo=None))


def test_qualification_digests_are_explicit(qualified: TimeAndItrfQualification) -> None:
    assert len(qualified.itrf.transformation_digest) == 64
    assert len(qualified.qualification_digest) == 64
    assert qualified.source_epoch_utc == EPOCH


def test_source_contains_offline_and_no_independent_claim_boundaries() -> None:
    source = Path("src/ailora/services/astrodynamics/frame_transform.py").read_text(
        encoding="utf-8"
    )
    lowered = source.lower()
    assert 'auto_download", false' in lowered
    assert "PINNED_SAME_ENGINE_REGRESSION" in source
    assert "independent truth remains externally gated" in lowered
    assert "ITRS" in source
    for forbidden in ("download_file", "import httpx", "import requests"):
        assert forbidden not in lowered
