"""Fail-closed scientific configuration and reproducibility manifests.

The manifest is deliberately an offline evidence contract.  It records the exact
scientific registry, runtime, tolerance profile and source commit used for an
execution, but it cannot authorize operational or production use.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Final, cast

SCHEMA: Final[str] = "AILORA-SCIENTIFIC-REPRODUCIBILITY-V1"
LOCAL_STATUS: Final[str] = "LOCAL_REPRODUCIBILITY_EVIDENCE_NOT_OPERATIONAL_QUALIFICATION"
DRIFT_MODE: Final[str] = "FAIL_CLOSED"
SUPPORTED_PYTHON: Final[tuple[str, ...]] = ("3.11", "3.12")
REQUIRED_NAMESPACES: Final[frozenset[str]] = frozenset(
    {"algorithm", "configuration", "dataset", "runtime", "tolerance"}
)

_IDENTIFIER = re.compile(r"^[a-z][a-z0-9_.-]{2,63}$")
_DIGEST = re.compile(r"^[0-9a-f]{64}$")
_COMMIT = re.compile(r"^[0-9a-f]{40}$")
_MUTABLE_VERSIONS = frozenset({"head", "latest", "main", "master", "unversioned"})


class ReproducibilityError(ValueError):
    """Raised when reproducibility evidence is incomplete or inconsistent."""


def _require_identifier(value: str, field: str) -> None:
    if not _IDENTIFIER.fullmatch(value):
        raise ReproducibilityError(f"{field} must be a stable lowercase identifier")


def _require_version(value: str) -> None:
    if not value or len(value) > 128 or any(character.isspace() for character in value):
        raise ReproducibilityError("registry version must be nonempty and whitespace-free")
    if value.casefold() in _MUTABLE_VERSIONS:
        raise ReproducibilityError("mutable registry versions are forbidden")


def _canonical_bytes(value: object) -> bytes:
    try:
        return json.dumps(
            value,
            allow_nan=False,
            ensure_ascii=True,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise ReproducibilityError("manifest contains non-canonical data") from exc


def _digest(value: object) -> str:
    return hashlib.sha256(_canonical_bytes(value)).hexdigest()


@dataclass(frozen=True, slots=True)
class ScientificRegistryEntry:
    namespace: str
    component_id: str
    version: str
    content_sha256: str

    def __post_init__(self) -> None:
        if self.namespace not in REQUIRED_NAMESPACES:
            raise ReproducibilityError("registry namespace is not approved")
        _require_identifier(self.component_id, "component_id")
        _require_version(self.version)
        if not _DIGEST.fullmatch(self.content_sha256):
            raise ReproducibilityError("registry content digest must be lowercase SHA-256")


@dataclass(frozen=True, slots=True)
class ToleranceSetting:
    name: str
    value: float
    unit: str

    def __post_init__(self) -> None:
        _require_identifier(self.name, "tolerance name")
        if not math.isfinite(self.value) or self.value < 0.0:
            raise ReproducibilityError("tolerance values must be finite and nonnegative")
        if (
            not self.unit
            or len(self.unit) > 32
            or any(character.isspace() for character in self.unit)
        ):
            raise ReproducibilityError("tolerance unit must be explicit and whitespace-free")


@dataclass(frozen=True, slots=True)
class ScientificToleranceProfile:
    profile_id: str
    settings: tuple[ToleranceSetting, ...]
    drift_mode: str = DRIFT_MODE

    def __post_init__(self) -> None:
        _require_identifier(self.profile_id, "profile_id")
        if self.drift_mode != DRIFT_MODE:
            raise ReproducibilityError("scientific drift mode must remain fail-closed")
        if not self.settings:
            raise ReproducibilityError("at least one tolerance setting is required")
        names = [setting.name for setting in self.settings]
        if len(names) != len(set(names)):
            raise ReproducibilityError("tolerance setting names must be unique")
        if not any(setting.value > 0.0 for setting in self.settings):
            raise ReproducibilityError("at least one tolerance must be positive")


@dataclass(frozen=True, slots=True)
class ScientificExecutionContext:
    execution_id: str
    observed_at_utc: datetime
    source_commit: str
    python_version: str
    platform_id: str
    random_seed: int
    advisory_only: bool = True
    production_authorized: bool = False

    def __post_init__(self) -> None:
        _require_identifier(self.execution_id, "execution_id")
        if self.observed_at_utc.tzinfo is None or self.observed_at_utc.utcoffset() is None:
            raise ReproducibilityError("observed_at_utc must be timezone-aware")
        object.__setattr__(self, "observed_at_utc", self.observed_at_utc.astimezone(UTC))
        if not _COMMIT.fullmatch(self.source_commit):
            raise ReproducibilityError("source_commit must be a complete lowercase Git SHA")
        if self.python_version not in SUPPORTED_PYTHON:
            raise ReproducibilityError("python version is outside the declared runtime matrix")
        _require_identifier(self.platform_id, "platform_id")
        if isinstance(self.random_seed, bool) or not 0 <= self.random_seed <= 2**63 - 1:
            raise ReproducibilityError("random_seed must be an explicit nonnegative 63-bit integer")
        if self.advisory_only is not True or self.production_authorized is not False:
            raise ReproducibilityError("scientific evidence cannot authorize production use")


@dataclass(frozen=True, slots=True)
class ReproducibilityComparison:
    status: str
    accepted: bool
    expected_fingerprint: str
    observed_fingerprint: str
    drift_fields: tuple[str, ...]


def _registry_payload(entries: tuple[ScientificRegistryEntry, ...]) -> list[dict[str, str]]:
    if not entries:
        raise ReproducibilityError("scientific registry cannot be empty")
    identities = [(entry.namespace, entry.component_id) for entry in entries]
    if len(identities) != len(set(identities)):
        raise ReproducibilityError("scientific registry identities must be unique")
    namespaces = {entry.namespace for entry in entries}
    missing = REQUIRED_NAMESPACES - namespaces
    if missing:
        raise ReproducibilityError(f"scientific registry namespaces missing: {sorted(missing)}")
    ordered = sorted(entries, key=lambda entry: (entry.namespace, entry.component_id))
    return [
        {
            "component_id": entry.component_id,
            "content_sha256": entry.content_sha256,
            "namespace": entry.namespace,
            "version": entry.version,
        }
        for entry in ordered
    ]


def _tolerance_payload(profile: ScientificToleranceProfile) -> dict[str, object]:
    settings = sorted(profile.settings, key=lambda setting: setting.name)
    return {
        "drift_mode": profile.drift_mode,
        "profile_id": profile.profile_id,
        "settings": [
            {"name": setting.name, "unit": setting.unit, "value": setting.value}
            for setting in settings
        ],
    }


def create_scientific_execution_manifest(
    entries: tuple[ScientificRegistryEntry, ...],
    tolerance_profile: ScientificToleranceProfile,
    context: ScientificExecutionContext,
) -> str:
    """Create deterministic, digest-bound local scientific execution evidence."""

    registry = _registry_payload(entries)
    tolerance = _tolerance_payload(tolerance_profile)
    execution = {
        "execution_id": context.execution_id,
        "observed_at_utc": context.observed_at_utc.isoformat().replace("+00:00", "Z"),
        "platform_id": context.platform_id,
        "python_version": context.python_version,
        "random_seed": context.random_seed,
        "source_commit": context.source_commit,
    }
    scientific_inputs = {
        "platform_id": context.platform_id,
        "python_version": context.python_version,
        "random_seed": context.random_seed,
        "registry": registry,
        "runtime_matrix": {"python": list(SUPPORTED_PYTHON)},
        "source_commit": context.source_commit,
        "tolerance_profile": tolerance,
    }
    payload: dict[str, object] = {
        "advisory_only": True,
        "execution": execution,
        "production_authorized": False,
        "registry": registry,
        "runtime_matrix": {"python": list(SUPPORTED_PYTHON)},
        "schema": SCHEMA,
        "scientific_fingerprint": _digest(scientific_inputs),
        "status": LOCAL_STATUS,
        "tolerance_profile": tolerance,
    }
    return _canonical_bytes({"payload": payload, "sha256": _digest(payload)}).decode("utf-8")


def _expect_dict(value: object, field: str) -> dict[str, object]:
    if not isinstance(value, dict) or not all(isinstance(key, str) for key in value):
        raise ReproducibilityError(f"{field} must be an object")
    return cast(dict[str, object], value)


def _parse_manifest(document: str) -> dict[str, object]:
    try:
        envelope_value: object = json.loads(document)
    except (json.JSONDecodeError, TypeError) as exc:
        raise ReproducibilityError("manifest must be valid JSON") from exc
    envelope = _expect_dict(envelope_value, "envelope")
    if set(envelope) != {"payload", "sha256"}:
        raise ReproducibilityError("manifest envelope shape is invalid")
    payload = _expect_dict(envelope["payload"], "payload")
    supplied_digest = envelope["sha256"]
    if not isinstance(supplied_digest, str) or supplied_digest != _digest(payload):
        raise ReproducibilityError("manifest digest mismatch")
    return payload


def verify_scientific_execution_manifest(document: str) -> dict[str, object]:
    """Verify cryptographic integrity and reconstruct every fail-closed boundary."""

    payload = _parse_manifest(document)
    expected_keys = {
        "advisory_only",
        "execution",
        "production_authorized",
        "registry",
        "runtime_matrix",
        "schema",
        "scientific_fingerprint",
        "status",
        "tolerance_profile",
    }
    if set(payload) != expected_keys:
        raise ReproducibilityError("manifest payload shape is invalid")
    if (
        payload["schema"] != SCHEMA
        or payload["status"] != LOCAL_STATUS
        or payload["advisory_only"] is not True
        or payload["production_authorized"] is not False
        or payload["runtime_matrix"] != {"python": list(SUPPORTED_PYTHON)}
    ):
        raise ReproducibilityError("manifest qualification boundary is invalid")

    execution = _expect_dict(payload["execution"], "execution")
    if set(execution) != {
        "execution_id",
        "observed_at_utc",
        "platform_id",
        "python_version",
        "random_seed",
        "source_commit",
    }:
        raise ReproducibilityError("execution context shape is invalid")
    try:
        observed_at = datetime.fromisoformat(
            str(execution["observed_at_utc"]).replace("Z", "+00:00")
        )
        context = ScientificExecutionContext(
            execution_id=str(execution["execution_id"]),
            observed_at_utc=observed_at,
            source_commit=str(execution["source_commit"]),
            python_version=str(execution["python_version"]),
            platform_id=str(execution["platform_id"]),
            random_seed=cast(int, execution["random_seed"]),
        )
    except (TypeError, ValueError) as exc:
        raise ReproducibilityError("execution context is invalid") from exc

    registry_value = payload["registry"]
    if not isinstance(registry_value, list):
        raise ReproducibilityError("registry must be an array")
    entries: list[ScientificRegistryEntry] = []
    for raw_entry in registry_value:
        entry = _expect_dict(raw_entry, "registry entry")
        if set(entry) != {"component_id", "content_sha256", "namespace", "version"}:
            raise ReproducibilityError("registry entry shape is invalid")
        entries.append(
            ScientificRegistryEntry(
                namespace=str(entry["namespace"]),
                component_id=str(entry["component_id"]),
                version=str(entry["version"]),
                content_sha256=str(entry["content_sha256"]),
            )
        )
    canonical_registry = _registry_payload(tuple(entries))
    if registry_value != canonical_registry:
        raise ReproducibilityError("registry order is not canonical")

    tolerance = _expect_dict(payload["tolerance_profile"], "tolerance_profile")
    if set(tolerance) != {"drift_mode", "profile_id", "settings"}:
        raise ReproducibilityError("tolerance profile shape is invalid")
    raw_settings = tolerance["settings"]
    if not isinstance(raw_settings, list):
        raise ReproducibilityError("tolerance settings must be an array")
    settings: list[ToleranceSetting] = []
    for raw_setting in raw_settings:
        setting = _expect_dict(raw_setting, "tolerance setting")
        if set(setting) != {"name", "unit", "value"}:
            raise ReproducibilityError("tolerance setting shape is invalid")
        value = setting["value"]
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ReproducibilityError("tolerance value must be numeric")
        settings.append(
            ToleranceSetting(
                name=str(setting["name"]),
                value=float(value),
                unit=str(setting["unit"]),
            )
        )
    profile = ScientificToleranceProfile(
        profile_id=str(tolerance["profile_id"]),
        settings=tuple(settings),
        drift_mode=str(tolerance["drift_mode"]),
    )
    canonical_tolerance = _tolerance_payload(profile)
    if tolerance != canonical_tolerance:
        raise ReproducibilityError("tolerance order is not canonical")

    scientific_inputs = {
        "platform_id": context.platform_id,
        "python_version": context.python_version,
        "random_seed": context.random_seed,
        "registry": canonical_registry,
        "runtime_matrix": {"python": list(SUPPORTED_PYTHON)},
        "source_commit": context.source_commit,
        "tolerance_profile": canonical_tolerance,
    }
    fingerprint = payload["scientific_fingerprint"]
    if not isinstance(fingerprint, str) or fingerprint != _digest(scientific_inputs):
        raise ReproducibilityError("scientific fingerprint mismatch")
    return payload


def compare_scientific_execution_manifests(
    expected_document: str,
    observed_document: str,
) -> ReproducibilityComparison:
    """Compare scientific inputs while ignoring execution identity and observation time."""

    expected = verify_scientific_execution_manifest(expected_document)
    observed = verify_scientific_execution_manifest(observed_document)
    expected_execution = _expect_dict(expected["execution"], "execution")
    observed_execution = _expect_dict(observed["execution"], "execution")
    fields: list[str] = []
    for field in ("source_commit", "python_version", "platform_id", "random_seed"):
        if expected_execution[field] != observed_execution[field]:
            fields.append(field)
    if expected["registry"] != observed["registry"]:
        fields.append("registry")
    if expected["runtime_matrix"] != observed["runtime_matrix"]:
        fields.append("runtime_matrix")
    if expected["tolerance_profile"] != observed["tolerance_profile"]:
        fields.append("tolerance_profile")
    accepted = not fields
    return ReproducibilityComparison(
        status="MATCH" if accepted else "DRIFT_REJECTED",
        accepted=accepted,
        expected_fingerprint=str(expected["scientific_fingerprint"]),
        observed_fingerprint=str(observed["scientific_fingerprint"]),
        drift_fields=tuple(fields),
    )
