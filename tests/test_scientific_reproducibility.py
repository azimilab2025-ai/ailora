from __future__ import annotations

import hashlib
import json
from dataclasses import replace
from datetime import UTC, datetime, timedelta

import pytest

from ailora.services.astrodynamics.reproducibility import (
    DRIFT_MODE,
    LOCAL_STATUS,
    ReproducibilityError,
    ScientificExecutionContext,
    ScientificRegistryEntry,
    ScientificToleranceProfile,
    ToleranceSetting,
    compare_scientific_execution_manifests,
    create_scientific_execution_manifest,
    verify_scientific_execution_manifest,
)

_DIGESTS = [hashlib.sha256(str(index).encode()).hexdigest() for index in range(8)]


def _entries() -> tuple[ScientificRegistryEntry, ...]:
    return (
        ScientificRegistryEntry("runtime", "python-runtime", "3.11.15", _DIGESTS[0]),
        ScientificRegistryEntry("algorithm", "sgp4-propagator", "2.27", _DIGESTS[1]),
        ScientificRegistryEntry("dataset", "iers-a-bundle", "2026.08.10", _DIGESTS[2]),
        ScientificRegistryEntry("configuration", "wgs72-advisory", "1.0.0", _DIGESTS[3]),
        ScientificRegistryEntry("tolerance", "tca-bounded", "1.0.0", _DIGESTS[4]),
    )


def _profile() -> ScientificToleranceProfile:
    return ScientificToleranceProfile(
        profile_id="tca-verification-v1",
        settings=(
            ToleranceSetting("relative-error", 1e-9, "ratio"),
            ToleranceSetting("miss-distance", 0.25, "km"),
            ToleranceSetting("tca-time", 0.001, "s"),
        ),
    )


def _context() -> ScientificExecutionContext:
    return ScientificExecutionContext(
        execution_id="scientific-run-001",
        observed_at_utc=datetime(2026, 8, 17, 8, 0, tzinfo=UTC),
        source_commit="8b3cfd22ba88e65a56b28e95878650878f21469d",
        python_version="3.11",
        platform_id="darwin-arm64",
        random_seed=20260817,
    )


def _manifest(
    *,
    entries: tuple[ScientificRegistryEntry, ...] | None = None,
    profile: ScientificToleranceProfile | None = None,
    context: ScientificExecutionContext | None = None,
) -> str:
    return create_scientific_execution_manifest(
        entries or _entries(),
        profile or _profile(),
        context or _context(),
    )


def test_manifest_is_deterministic_canonical_and_digest_bound() -> None:
    document = _manifest()
    assert document == _manifest(entries=tuple(reversed(_entries())))
    payload = verify_scientific_execution_manifest(document)
    assert payload["status"] == LOCAL_STATUS
    assert payload["advisory_only"] is True
    assert payload["production_authorized"] is False
    assert len(str(payload["scientific_fingerprint"])) == 64


def test_execution_identity_does_not_create_scientific_drift() -> None:
    observed_context = replace(
        _context(),
        execution_id="scientific-run-002",
        observed_at_utc=_context().observed_at_utc + timedelta(hours=1),
    )
    comparison = compare_scientific_execution_manifests(
        _manifest(),
        _manifest(context=observed_context),
    )
    assert comparison.accepted is True
    assert comparison.status == "MATCH"
    assert comparison.drift_fields == ()
    assert comparison.expected_fingerprint == comparison.observed_fingerprint


@pytest.mark.parametrize(
    ("changes", "drift_field"),
    [
        ({"source_commit": "a" * 40}, "source_commit"),
        ({"python_version": "3.12"}, "python_version"),
        ({"platform_id": "linux-x86_64"}, "platform_id"),
        ({"random_seed": 99}, "random_seed"),
    ],
)
def test_runtime_or_source_drift_is_rejected(
    changes: dict[str, object],
    drift_field: str,
) -> None:
    observed = _manifest(context=replace(_context(), **changes))
    comparison = compare_scientific_execution_manifests(_manifest(), observed)
    assert comparison.accepted is False
    assert comparison.status == "DRIFT_REJECTED"
    assert comparison.drift_fields == (drift_field,)


def test_registry_drift_is_rejected() -> None:
    entries = list(_entries())
    entries[0] = replace(entries[0], content_sha256=_DIGESTS[7])
    comparison = compare_scientific_execution_manifests(
        _manifest(),
        _manifest(entries=tuple(entries)),
    )
    assert comparison.drift_fields == ("registry",)


def test_tolerance_drift_is_rejected() -> None:
    settings = list(_profile().settings)
    settings[0] = replace(settings[0], value=1e-8)
    observed_profile = replace(_profile(), settings=tuple(settings))
    comparison = compare_scientific_execution_manifests(
        _manifest(),
        _manifest(profile=observed_profile),
    )
    assert comparison.drift_fields == ("tolerance_profile",)


@pytest.mark.parametrize(
    "missing_namespace", ["algorithm", "configuration", "dataset", "runtime", "tolerance"]
)
def test_every_registry_namespace_is_required(missing_namespace: str) -> None:
    entries = tuple(entry for entry in _entries() if entry.namespace != missing_namespace)
    with pytest.raises(ReproducibilityError, match="namespaces missing"):
        _manifest(entries=entries)


def test_duplicate_registry_identity_is_rejected() -> None:
    with pytest.raises(ReproducibilityError, match="identities must be unique"):
        _manifest(entries=_entries() + (_entries()[0],))


@pytest.mark.parametrize("version", ["latest", "HEAD", "main", "master", "unversioned"])
def test_mutable_registry_version_is_rejected(version: str) -> None:
    with pytest.raises(ReproducibilityError, match="mutable"):
        replace(_entries()[0], version=version)


@pytest.mark.parametrize("digest", ["0" * 63, "G" * 64, "", "sha256:abc"])
def test_invalid_registry_digest_is_rejected(digest: str) -> None:
    with pytest.raises(ReproducibilityError, match="lowercase SHA-256"):
        replace(_entries()[0], content_sha256=digest)


@pytest.mark.parametrize("value", [-1.0, float("inf"), float("nan")])
def test_invalid_tolerance_values_are_rejected(value: float) -> None:
    with pytest.raises(ReproducibilityError, match="finite and nonnegative"):
        ToleranceSetting("invalid-value", value, "km")


def test_duplicate_tolerance_names_are_rejected() -> None:
    setting = ToleranceSetting("same-setting", 1.0, "km")
    with pytest.raises(ReproducibilityError, match="must be unique"):
        ScientificToleranceProfile("duplicate-profile", (setting, setting))


def test_all_zero_tolerance_profile_is_rejected() -> None:
    with pytest.raises(ReproducibilityError, match="must be positive"):
        ScientificToleranceProfile(
            "zero-profile",
            (ToleranceSetting("zero-setting", 0.0, "km"),),
        )


def test_non_fail_closed_drift_mode_is_rejected() -> None:
    with pytest.raises(ReproducibilityError, match="fail-closed"):
        replace(_profile(), drift_mode="WARN_ONLY")
    assert _profile().drift_mode == DRIFT_MODE


@pytest.mark.parametrize(
    ("changes", "message"),
    [
        ({"observed_at_utc": datetime(2026, 8, 17, 8, 0)}, "timezone-aware"),
        ({"source_commit": "abc"}, "complete lowercase Git SHA"),
        ({"python_version": "3.10"}, "runtime matrix"),
        ({"random_seed": -1}, "nonnegative 63-bit"),
        ({"random_seed": True}, "nonnegative 63-bit"),
        ({"advisory_only": False}, "cannot authorize production"),
        ({"production_authorized": True}, "cannot authorize production"),
    ],
)
def test_unsafe_or_incomplete_execution_context_is_rejected(
    changes: dict[str, object],
    message: str,
) -> None:
    with pytest.raises(ReproducibilityError, match=message):
        replace(_context(), **changes)


def test_outer_digest_tampering_is_rejected() -> None:
    envelope = json.loads(_manifest())
    envelope["payload"]["execution"]["random_seed"] = 1
    with pytest.raises(ReproducibilityError, match="digest mismatch"):
        verify_scientific_execution_manifest(json.dumps(envelope))


def test_fingerprint_tampering_is_rejected_even_when_outer_digest_is_recomputed() -> None:
    envelope = json.loads(_manifest())
    envelope["payload"]["scientific_fingerprint"] = "0" * 64
    canonical = json.dumps(
        envelope["payload"],
        allow_nan=False,
        ensure_ascii=True,
        separators=(",", ":"),
        sort_keys=True,
    ).encode()
    envelope["sha256"] = hashlib.sha256(canonical).hexdigest()
    with pytest.raises(ReproducibilityError, match="fingerprint mismatch"):
        verify_scientific_execution_manifest(json.dumps(envelope))


def test_production_boundary_tampering_is_rejected_with_recomputed_digest() -> None:
    envelope = json.loads(_manifest())
    envelope["payload"]["production_authorized"] = True
    canonical = json.dumps(
        envelope["payload"],
        allow_nan=False,
        ensure_ascii=True,
        separators=(",", ":"),
        sort_keys=True,
    ).encode()
    envelope["sha256"] = hashlib.sha256(canonical).hexdigest()
    with pytest.raises(ReproducibilityError, match="qualification boundary"):
        verify_scientific_execution_manifest(json.dumps(envelope))


@pytest.mark.parametrize("document", ["not-json", "[]", "{}", '{"payload":{}}'])
def test_malformed_documents_are_rejected(document: str) -> None:
    with pytest.raises(ReproducibilityError):
        verify_scientific_execution_manifest(document)
