from __future__ import annotations

import uuid
from datetime import UTC, datetime

import pytest

from ailora.services.astrodynamics.config import AstrodynamicsConfig
from ailora.services.astrodynamics.models import PropagationRequest, TLEInput

LINE1 = "1 00005U 58002B   00179.78495062  .00000023  00000-0  28098-4 0  4753"
LINE2 = "2 00005  34.2682 348.7242 1859667 331.7664  19.3264 10.82419157413667"
EPOCH = datetime(2000, 6, 27, 18, 50, 19, 733568, tzinfo=UTC)


def test_config_has_bounded_advisory_defaults() -> None:
    config = AstrodynamicsConfig()
    assert config.advisory_only is True
    assert config.max_days_from_tle_epoch == 14.0


def test_config_rejects_unbounded_window_and_non_wgs72() -> None:
    with pytest.raises(ValueError):
        AstrodynamicsConfig(max_days_from_tle_epoch=31.0)
    with pytest.raises(ValueError):
        AstrodynamicsConfig(gravity_model="WGS84")


def test_request_is_immutable_and_canonicalizes_utc() -> None:
    request = PropagationRequest(
        request_id=uuid.uuid4(),
        tle=TLEInput("VANGUARD 1", LINE1, LINE2),
        target_epoch=EPOCH,
        purpose="advisory propagation",
    )
    assert request.target_epoch.tzinfo is UTC
    with pytest.raises(AttributeError):
        request.purpose = "changed"  # type: ignore[misc]


def test_request_rejects_naive_epoch_and_bad_purpose() -> None:
    tle = TLEInput("VANGUARD 1", LINE1, LINE2)
    with pytest.raises(ValueError, match="timezone-aware"):
        PropagationRequest(uuid.uuid4(), tle, EPOCH.replace(tzinfo=None), "advisory")
    with pytest.raises(ValueError, match="purpose"):
        PropagationRequest(uuid.uuid4(), tle, EPOCH, "")
