from __future__ import annotations

import importlib.metadata
import math
import socket
import urllib.request
from datetime import UTC, datetime, timedelta, timezone
from pathlib import Path
from typing import NoReturn

import astropy.units as u
import pytest
from astropy.coordinates import GCRS, TEME, CartesianDifferential, CartesianRepresentation
from astropy.time import Time
from astropy.utils import iers

from ailora.services.astrodynamics.frame_transform import (
    FrameTransformationError,
    OfflineTemeToGcrfTransformer,
)

EPOCH = datetime(2000, 6, 27, 18, 50, 19, 733568, tzinfo=UTC)
POSITION_KM = (7022.46529266, -1400.08296755, 0.03995155)
VELOCITY_KM_S = (1.893841015, 6.405893759, 4.534807250)


def transformer() -> OfflineTemeToGcrfTransformer:
    return OfflineTemeToGcrfTransformer()


def norm(vector: tuple[float, float, float]) -> float:
    return math.sqrt(sum(component * component for component in vector))


def test_dependency_versions_are_exactly_pinned() -> None:
    assert importlib.metadata.version("astropy") == "8.0.1"
    assert importlib.metadata.version("astropy-iers-data") == "0.2026.8.10.0.32.39"


def test_vallado_teme_vector_transforms_to_truthfully_labeled_gcrf() -> None:
    result = transformer().transform(POSITION_KM, VELOCITY_KM_S, EPOCH)
    assert result.source_frame == "TEME"
    assert result.target_frame == "GCRF"
    assert result.frame_realization == "ASTROPY_GCRS"
    assert result.distance_unit == "km"
    assert result.velocity_unit == "km/s"
    assert result.advisory_only is True
    assert result.position_km != pytest.approx(POSITION_KM, abs=1e-9)
    assert norm(result.position_km) == pytest.approx(norm(POSITION_KM), abs=2e-6)
    assert all(math.isfinite(value) for value in (*result.position_km, *result.velocity_km_s))


def test_repeated_transform_is_bitwise_deterministic() -> None:
    service = transformer()
    first = service.transform(POSITION_KM, VELOCITY_KM_S, EPOCH)
    second = service.transform(POSITION_KM, VELOCITY_KM_S, EPOCH)
    assert first == second
    assert len(first.input_digest) == 64
    assert len(first.iers_data_digest) == 64
    assert len(first.transformation_digest) == 64


def test_equivalent_timezone_instant_is_identical() -> None:
    offset = timezone(timedelta(hours=3, minutes=30))
    shifted = EPOCH.astimezone(offset)
    assert transformer().transform(POSITION_KM, VELOCITY_KM_S, EPOCH) == transformer().transform(
        POSITION_KM, VELOCITY_KM_S, shifted
    )


def test_roundtrip_recovers_native_teme_position_and_velocity() -> None:
    result = transformer().transform(POSITION_KM, VELOCITY_KM_S, EPOCH)
    obstime = Time(EPOCH, scale="utc")
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
        recovered = GCRS(representation, obstime=obstime).transform_to(TEME(obstime=obstime))
    recovered_position = tuple(
        float(recovered.cartesian.xyz[index].to_value(u.km)) for index in range(3)
    )
    differential = recovered.cartesian.differentials["s"]
    recovered_velocity = tuple(
        float(differential.d_xyz[index].to_value(u.km / u.s)) for index in range(3)
    )
    assert recovered_position == pytest.approx(POSITION_KM, abs=3e-6)
    assert recovered_velocity == pytest.approx(VELOCITY_KM_S, abs=3e-9)


def test_no_network_is_attempted_during_construction_or_transform(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def blocked(*_args: object, **_kwargs: object) -> NoReturn:
        raise AssertionError("network access is forbidden during frame transformation")

    monkeypatch.setattr(socket, "create_connection", blocked)
    monkeypatch.setattr(urllib.request, "urlopen", blocked)
    result = transformer().transform(POSITION_KM, VELOCITY_KM_S, EPOCH)
    assert result.target_frame == "GCRF"


def test_unsupported_epoch_is_rejected_without_degraded_accuracy() -> None:
    unsupported = datetime(1970, 1, 1, tzinfo=UTC)
    with pytest.raises(FrameTransformationError, match="outside the pinned IERS range"):
        transformer().transform(POSITION_KM, VELOCITY_KM_S, unsupported)


@pytest.mark.parametrize(
    ("position", "velocity", "epoch", "message"),
    [
        ((1.0, 2.0), VELOCITY_KM_S, EPOCH, "exactly three"),
        (POSITION_KM, (1.0, 2.0), EPOCH, "exactly three"),
        ((math.nan, 0.0, 0.0), VELOCITY_KM_S, EPOCH, "finite"),
        (POSITION_KM, VELOCITY_KM_S, EPOCH.replace(tzinfo=None), "timezone-aware"),
    ],
)
def test_invalid_inputs_are_rejected(
    position: tuple[float, ...],
    velocity: tuple[float, ...],
    epoch: datetime,
    message: str,
) -> None:
    with pytest.raises(FrameTransformationError, match=message):
        transformer().transform(position, velocity, epoch)


def test_iers_provenance_and_epoch_coverage_are_recorded() -> None:
    result = transformer().transform(POSITION_KM, VELOCITY_KM_S, EPOCH)
    epoch_mjd = Time(EPOCH, scale="utc").mjd
    assert result.iers_source == "finals2000A.all"
    assert result.iers_mjd_start <= epoch_mjd <= result.iers_mjd_end
    assert result.eop_status.startswith("UT1:")
    assert ";PM:" in result.eop_status
    assert result.astropy_version == "8.0.1"
    assert result.iers_data_version == "0.2026.8.10.0.32.39"


def test_source_contains_no_runtime_download_or_http_client_path() -> None:
    source = (
        Path("src/ailora/services/astrodynamics/frame_transform.py")
        .read_text(encoding="utf-8")
        .lower()
    )
    assert "download_file" not in source
    assert "urlopen" not in source
    assert "import httpx" not in source
    assert "import requests" not in source
    assert 'auto_download", false' in source
