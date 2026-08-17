"""Fail-closed, provider-neutral supply-chain evidence admission.

The module verifies a signed, content-addressed evidence manifest.  It does not
build, sign, publish, promote, deploy, or confer production authority.
"""

from __future__ import annotations

import base64
import hashlib
import json
import math
import re
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from enum import StrEnum
from typing import Final

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

SCHEMA: Final[str] = "AILORA-SUPPLY-CHAIN-ADMISSION-V1"
DECISION: Final[str] = "EVIDENCE_VERIFIED_NOT_DEPLOYMENT_AUTHORIZATION"
SIGNATURE_ALGORITHM: Final[str] = "Ed25519"
PROVENANCE_PREDICATE: Final[str] = "https://slsa.dev/provenance/v1"

_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_SHA256_REF = re.compile(r"^[a-z0-9][a-z0-9._/-]{1,199}@sha256:[0-9a-f]{64}$")
_GIT_SHA = re.compile(r"^[0-9a-f]{40}$")
_IDENTIFIER = re.compile(r"^[a-z0-9][a-z0-9._:/-]{2,199}$")
_KEY_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{2,127}$")


class SupplyChainAdmissionError(ValueError):
    """A supply-chain evidence or signature contract violation."""


class ScanKind(StrEnum):
    SAST = "SAST"
    SCA = "SCA"
    CONTAINER = "CONTAINER"
    SECRET_HISTORY = "SECRET_HISTORY"  # noqa: S105 - evidence category, not a secret


class ScanOutcome(StrEnum):
    PASS = "PASS"  # noqa: S105 - verification outcome, not a password
    FAIL = "FAIL"
    INCOMPLETE = "INCOMPLETE"


class VexStatus(StrEnum):
    NOT_AFFECTED = "NOT_AFFECTED"
    FIXED = "FIXED"
    KNOWN_AFFECTED = "KNOWN_AFFECTED"
    UNDER_INVESTIGATION = "UNDER_INVESTIGATION"


def canonical_json(value: object) -> bytes:
    """Return the one accepted JSON representation for digests and signatures."""

    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("utf-8")


def sha256_hex(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _require_digest(value: str, label: str) -> None:
    if not _SHA256.fullmatch(value):
        raise SupplyChainAdmissionError(f"{label} must be a lowercase SHA-256 digest")


def _utc(value: datetime, label: str) -> datetime:
    offset = value.utcoffset()
    if value.tzinfo is None or offset is None:
        raise SupplyChainAdmissionError(f"{label} must be timezone-aware")
    canonical = value.astimezone(UTC)
    if offset.total_seconds() != 0:
        raise SupplyChainAdmissionError(f"{label} must be expressed in UTC")
    return canonical


@dataclass(frozen=True, slots=True)
class ScanEvidence:
    kind: ScanKind
    scanner_id: str
    scanner_version: str
    artifact_digest: str
    result_digest: str
    outcome: ScanOutcome
    findings_count: int

    def __post_init__(self) -> None:
        if not _IDENTIFIER.fullmatch(self.scanner_id):
            raise SupplyChainAdmissionError("scanner_id is invalid")
        if not self.scanner_version.strip() or self.scanner_version.lower() in {
            "latest",
            "main",
            "head",
        }:
            raise SupplyChainAdmissionError("scanner_version must be immutable")
        _require_digest(self.artifact_digest, "scan artifact_digest")
        _require_digest(self.result_digest, "scan result_digest")
        if self.findings_count < 0:
            raise SupplyChainAdmissionError("findings_count must be nonnegative")
        if self.outcome is ScanOutcome.PASS and self.findings_count != 0:
            raise SupplyChainAdmissionError("passing scan must have zero findings")


@dataclass(frozen=True, slots=True)
class VexAssertion:
    vulnerability_id: str
    component_purl: str
    status: VexStatus
    statement_digest: str
    justification: str

    def __post_init__(self) -> None:
        if not re.fullmatch(r"(?:CVE|GHSA)-[A-Za-z0-9-]{4,64}", self.vulnerability_id):
            raise SupplyChainAdmissionError("vulnerability_id is invalid")
        if not self.component_purl.startswith("pkg:") or len(self.component_purl) > 512:
            raise SupplyChainAdmissionError("component_purl is invalid")
        _require_digest(self.statement_digest, "VEX statement_digest")
        if not self.justification.strip() or len(self.justification) > 512:
            raise SupplyChainAdmissionError("VEX justification is required")


@dataclass(frozen=True, slots=True)
class SupplyChainManifest:
    artifact_reference: str
    source_commit: str
    builder_id: str
    build_type: str
    sbom_digest: str
    vex_digest: str
    provenance_digest: str
    source_environment: str
    target_environment: str
    issued_at: datetime
    expires_at: datetime
    scans: tuple[ScanEvidence, ...]
    vex_assertions: tuple[VexAssertion, ...]
    rebuild_between_environments: bool = False
    production_authorized: bool = False
    schema: str = SCHEMA
    provenance_predicate: str = PROVENANCE_PREDICATE

    def __post_init__(self) -> None:
        if not _SHA256_REF.fullmatch(self.artifact_reference):
            raise SupplyChainAdmissionError(
                "artifact_reference must be immutable name@sha256:digest"
            )
        if not _GIT_SHA.fullmatch(self.source_commit):
            raise SupplyChainAdmissionError("source_commit must be a full lowercase Git SHA")
        if not _IDENTIFIER.fullmatch(self.builder_id):
            raise SupplyChainAdmissionError("builder_id is invalid")
        if not _IDENTIFIER.fullmatch(self.build_type):
            raise SupplyChainAdmissionError("build_type is invalid")
        for label, value in (
            ("sbom_digest", self.sbom_digest),
            ("vex_digest", self.vex_digest),
            ("provenance_digest", self.provenance_digest),
        ):
            _require_digest(value, label)
        if self.source_environment not in {"build", "staging"}:
            raise SupplyChainAdmissionError("source_environment is invalid")
        if self.target_environment not in {"staging", "production"}:
            raise SupplyChainAdmissionError("target_environment is invalid")
        if self.source_environment == self.target_environment:
            raise SupplyChainAdmissionError("promotion environments must differ")
        issued_at = _utc(self.issued_at, "issued_at")
        expires_at = _utc(self.expires_at, "expires_at")
        if expires_at <= issued_at:
            raise SupplyChainAdmissionError("expires_at must follow issued_at")
        if (expires_at - issued_at).total_seconds() > 86400:
            raise SupplyChainAdmissionError("manifest validity must not exceed 24 hours")
        required_scans = set(ScanKind)
        actual_scans = {scan.kind for scan in self.scans}
        if len(self.scans) != len(required_scans) or actual_scans != required_scans:
            raise SupplyChainAdmissionError("every required scan kind must appear exactly once")
        if self.rebuild_between_environments is not False:
            raise SupplyChainAdmissionError("promotion rebuild is forbidden")
        if self.production_authorized is not False:
            raise SupplyChainAdmissionError("manifest cannot grant production authority")
        if self.schema != SCHEMA:
            raise SupplyChainAdmissionError("manifest schema is unsupported")
        if self.provenance_predicate != PROVENANCE_PREDICATE:
            raise SupplyChainAdmissionError("SLSA provenance predicate is unsupported")
        object.__setattr__(self, "issued_at", issued_at)
        object.__setattr__(self, "expires_at", expires_at)

    @property
    def artifact_digest(self) -> str:
        return self.artifact_reference.rsplit("sha256:", 1)[1]

    def payload(self) -> dict[str, object]:
        return {
            "artifact_reference": self.artifact_reference,
            "build_type": self.build_type,
            "builder_id": self.builder_id,
            "expires_at": self.expires_at.isoformat(),
            "issued_at": self.issued_at.isoformat(),
            "production_authorized": self.production_authorized,
            "provenance_digest": self.provenance_digest,
            "provenance_predicate": self.provenance_predicate,
            "rebuild_between_environments": self.rebuild_between_environments,
            "sbom_digest": self.sbom_digest,
            "scans": [asdict(scan) for scan in sorted(self.scans, key=lambda item: item.kind)],
            "schema": self.schema,
            "source_commit": self.source_commit,
            "source_environment": self.source_environment,
            "target_environment": self.target_environment,
            "vex_assertions": [
                asdict(assertion)
                for assertion in sorted(
                    self.vex_assertions,
                    key=lambda item: (item.vulnerability_id, item.component_purl),
                )
            ],
            "vex_digest": self.vex_digest,
        }

    def manifest_digest(self) -> str:
        return sha256_hex(canonical_json(self.payload()))


@dataclass(frozen=True, slots=True)
class SignedSupplyChainManifest:
    payload: dict[str, object]
    manifest_digest: str
    key_id: str
    algorithm: str
    signature: str

    def __post_init__(self) -> None:
        _require_digest(self.manifest_digest, "manifest_digest")
        if not _KEY_ID.fullmatch(self.key_id):
            raise SupplyChainAdmissionError("key_id is invalid")
        if self.algorithm != SIGNATURE_ALGORITHM:
            raise SupplyChainAdmissionError("signature algorithm is unsupported")
        try:
            decoded = base64.urlsafe_b64decode(self.signature + "=" * (-len(self.signature) % 4))
        except ValueError as exc:
            raise SupplyChainAdmissionError("signature encoding is invalid") from exc
        if len(decoded) != 64:
            raise SupplyChainAdmissionError("Ed25519 signature must be 64 bytes")


@dataclass(frozen=True, slots=True)
class AdmissionDecision:
    status: str
    artifact_digest: str
    manifest_digest: str
    source_commit: str
    target_environment: str
    production_authorized: bool


def _scan_from(value: object) -> ScanEvidence:
    if not isinstance(value, dict):
        raise SupplyChainAdmissionError("scan evidence must be an object")
    try:
        return ScanEvidence(
            kind=ScanKind(value["kind"]),
            scanner_id=str(value["scanner_id"]),
            scanner_version=str(value["scanner_version"]),
            artifact_digest=str(value["artifact_digest"]),
            result_digest=str(value["result_digest"]),
            outcome=ScanOutcome(value["outcome"]),
            findings_count=int(value["findings_count"]),
        )
    except (KeyError, TypeError, ValueError) as exc:
        raise SupplyChainAdmissionError("scan evidence is malformed") from exc


def _vex_from(value: object) -> VexAssertion:
    if not isinstance(value, dict):
        raise SupplyChainAdmissionError("VEX assertion must be an object")
    try:
        return VexAssertion(
            vulnerability_id=str(value["vulnerability_id"]),
            component_purl=str(value["component_purl"]),
            status=VexStatus(value["status"]),
            statement_digest=str(value["statement_digest"]),
            justification=str(value["justification"]),
        )
    except (KeyError, TypeError, ValueError) as exc:
        raise SupplyChainAdmissionError("VEX assertion is malformed") from exc


def _manifest_from(payload: dict[str, object]) -> SupplyChainManifest:
    try:
        scans = payload["scans"]
        assertions = payload["vex_assertions"]
        if not isinstance(scans, list) or not isinstance(assertions, list):
            raise TypeError
        rebuild = payload["rebuild_between_environments"]
        production_authorized = payload["production_authorized"]
        if type(rebuild) is not bool or type(production_authorized) is not bool:
            raise TypeError
        return SupplyChainManifest(
            artifact_reference=str(payload["artifact_reference"]),
            source_commit=str(payload["source_commit"]),
            builder_id=str(payload["builder_id"]),
            build_type=str(payload["build_type"]),
            sbom_digest=str(payload["sbom_digest"]),
            vex_digest=str(payload["vex_digest"]),
            provenance_digest=str(payload["provenance_digest"]),
            source_environment=str(payload["source_environment"]),
            target_environment=str(payload["target_environment"]),
            issued_at=datetime.fromisoformat(str(payload["issued_at"])),
            expires_at=datetime.fromisoformat(str(payload["expires_at"])),
            scans=tuple(_scan_from(scan) for scan in scans),
            vex_assertions=tuple(_vex_from(assertion) for assertion in assertions),
            rebuild_between_environments=rebuild,
            production_authorized=production_authorized,
            schema=str(payload["schema"]),
            provenance_predicate=str(payload["provenance_predicate"]),
        )
    except (KeyError, TypeError, ValueError) as exc:
        if isinstance(exc, SupplyChainAdmissionError):
            raise
        raise SupplyChainAdmissionError("manifest payload is malformed") from exc


def verify_signed_manifest(
    envelope: SignedSupplyChainManifest,
    *,
    trusted_public_keys: dict[str, bytes],
    trusted_builder_ids: frozenset[str],
    now: datetime,
) -> AdmissionDecision:
    """Verify evidence, signature and immutable promotion without authorizing deployment."""

    now_utc = _utc(now, "now")
    if set(envelope.payload) != {
        "artifact_reference",
        "build_type",
        "builder_id",
        "expires_at",
        "issued_at",
        "production_authorized",
        "provenance_digest",
        "provenance_predicate",
        "rebuild_between_environments",
        "sbom_digest",
        "scans",
        "schema",
        "source_commit",
        "source_environment",
        "target_environment",
        "vex_assertions",
        "vex_digest",
    }:
        raise SupplyChainAdmissionError("manifest payload fields are not exact")
    payload_bytes = canonical_json(envelope.payload)
    actual_digest = sha256_hex(payload_bytes)
    if actual_digest != envelope.manifest_digest:
        raise SupplyChainAdmissionError("manifest digest mismatch")
    public_key_bytes = trusted_public_keys.get(envelope.key_id)
    if public_key_bytes is None:
        raise SupplyChainAdmissionError("signing key is not trusted")
    try:
        public_key = Ed25519PublicKey.from_public_bytes(public_key_bytes)
        signature = base64.urlsafe_b64decode(
            envelope.signature + "=" * (-len(envelope.signature) % 4)
        )
        public_key.verify(signature, payload_bytes)
    except (InvalidSignature, ValueError) as exc:
        raise SupplyChainAdmissionError("manifest signature verification failed") from exc

    manifest = _manifest_from(envelope.payload)
    if manifest.builder_id not in trusted_builder_ids:
        raise SupplyChainAdmissionError("builder identity is not trusted")
    if not manifest.issued_at <= now_utc < manifest.expires_at:
        raise SupplyChainAdmissionError("manifest is not currently valid")
    for scan in manifest.scans:
        if scan.artifact_digest != manifest.artifact_digest:
            raise SupplyChainAdmissionError("scan is bound to a different artifact")
        if scan.outcome is not ScanOutcome.PASS:
            raise SupplyChainAdmissionError("all required scans must pass")
    unresolved = {
        VexStatus.KNOWN_AFFECTED,
        VexStatus.UNDER_INVESTIGATION,
    }
    if any(assertion.status in unresolved for assertion in manifest.vex_assertions):
        raise SupplyChainAdmissionError("VEX contains unresolved vulnerability status")
    if not math.isfinite((manifest.expires_at - now_utc).total_seconds()):
        raise SupplyChainAdmissionError("manifest validity is invalid")
    return AdmissionDecision(
        status=DECISION,
        artifact_digest=manifest.artifact_digest,
        manifest_digest=envelope.manifest_digest,
        source_commit=manifest.source_commit,
        target_environment=manifest.target_environment,
        production_authorized=False,
    )
