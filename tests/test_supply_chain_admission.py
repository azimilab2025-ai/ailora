from __future__ import annotations

import base64
import copy
import hashlib
from dataclasses import replace
from datetime import UTC, datetime, timedelta, timezone

import pytest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from ailora.security.supply_chain import (
    DECISION,
    PROVENANCE_PREDICATE,
    SCHEMA,
    AdmissionDecision,
    ScanEvidence,
    ScanKind,
    ScanOutcome,
    SignedSupplyChainManifest,
    SupplyChainAdmissionError,
    SupplyChainManifest,
    VexAssertion,
    VexStatus,
    canonical_json,
    sha256_hex,
    verify_signed_manifest,
)

NOW = datetime(2026, 8, 17, 8, 0, tzinfo=UTC)
ARTIFACT_DIGEST = "a" * 64
PRIVATE_KEY = Ed25519PrivateKey.from_private_bytes(bytes(range(1, 33)))
PUBLIC_KEY = PRIVATE_KEY.public_key().public_bytes(
    encoding=serialization.Encoding.Raw,
    format=serialization.PublicFormat.Raw,
)
KEY_ID = "ailora-test-signing-key-v1"
BUILDER_ID = "github.com/azimilab2025-ai/ailora/actions/build-v1"


def scans(
    *,
    artifact_digest: str = ARTIFACT_DIGEST,
    outcome: ScanOutcome = ScanOutcome.PASS,
) -> tuple[ScanEvidence, ...]:
    return tuple(
        ScanEvidence(
            kind=kind,
            scanner_id=f"ailora.local/{kind.value.lower()}",
            scanner_version="1.0.0",
            artifact_digest=artifact_digest,
            result_digest=hashlib.sha256(kind.value.encode()).hexdigest(),
            outcome=outcome,
            findings_count=0 if outcome is ScanOutcome.PASS else 1,
        )
        for kind in ScanKind
    )


def manifest(**overrides: object) -> SupplyChainManifest:
    values: dict[str, object] = {
        "artifact_reference": f"ghcr.io/azimilab2025-ai/ailora@sha256:{ARTIFACT_DIGEST}",
        "source_commit": "b" * 40,
        "builder_id": BUILDER_ID,
        "build_type": "ailora.build/python-wheel-v1",
        "sbom_digest": "c" * 64,
        "vex_digest": "d" * 64,
        "provenance_digest": "e" * 64,
        "source_environment": "build",
        "target_environment": "staging",
        "issued_at": NOW - timedelta(minutes=1),
        "expires_at": NOW + timedelta(hours=1),
        "scans": scans(),
        "vex_assertions": (
            VexAssertion(
                vulnerability_id="CVE-2026-12345",
                component_purl="pkg:pypi/example@1.0.0",
                status=VexStatus.NOT_AFFECTED,
                statement_digest="f" * 64,
                justification="vulnerable code path is not present",
            ),
        ),
    }
    values.update(overrides)
    return SupplyChainManifest(**values)  # type: ignore[arg-type]


def sign(value: SupplyChainManifest, private_key: Ed25519PrivateKey = PRIVATE_KEY):
    payload = value.payload()
    payload_bytes = canonical_json(payload)
    signature = base64.urlsafe_b64encode(private_key.sign(payload_bytes)).decode().rstrip("=")
    return SignedSupplyChainManifest(
        payload=payload,
        manifest_digest=sha256_hex(payload_bytes),
        key_id=KEY_ID,
        algorithm="Ed25519",
        signature=signature,
    )


def verify(envelope: SignedSupplyChainManifest) -> AdmissionDecision:
    return verify_signed_manifest(
        envelope,
        trusted_public_keys={KEY_ID: PUBLIC_KEY},
        trusted_builder_ids=frozenset({BUILDER_ID}),
        now=NOW,
    )


def resign_payload(payload: dict[str, object]) -> SignedSupplyChainManifest:
    payload_bytes = canonical_json(payload)
    signature = base64.urlsafe_b64encode(PRIVATE_KEY.sign(payload_bytes)).decode().rstrip("=")
    return SignedSupplyChainManifest(
        payload=payload,
        manifest_digest=sha256_hex(payload_bytes),
        key_id=KEY_ID,
        algorithm="Ed25519",
        signature=signature,
    )


def test_valid_signed_manifest_is_verified_without_deployment_authority() -> None:
    result = verify(sign(manifest()))
    assert result.status == DECISION
    assert result.artifact_digest == ARTIFACT_DIGEST
    assert result.source_commit == "b" * 40
    assert result.target_environment == "staging"
    assert result.production_authorized is False


def test_manifest_is_canonical_and_order_independent() -> None:
    first = manifest()
    second = replace(first, scans=tuple(reversed(first.scans)))
    assert first.payload() == second.payload()
    assert first.manifest_digest() == second.manifest_digest()


def test_schema_and_provenance_predicate_are_exact() -> None:
    value = manifest()
    assert value.schema == SCHEMA
    assert value.provenance_predicate == PROVENANCE_PREDICATE


@pytest.mark.parametrize(
    "reference",
    [
        "ghcr.io/azimilab2025-ai/ailora:latest",
        "ghcr.io/azimilab2025-ai/ailora:1.0.0",
        "GHCR.IO/AILORA@sha256:" + "a" * 64,
        "ghcr.io/ailora@sha256:short",
    ],
)
def test_mutable_or_invalid_artifact_references_are_rejected(reference: str) -> None:
    with pytest.raises(SupplyChainAdmissionError, match="immutable"):
        manifest(artifact_reference=reference)


@pytest.mark.parametrize("source_commit", ["main", "HEAD", "a" * 39, "A" * 40])
def test_source_commit_requires_full_lowercase_sha(source_commit: str) -> None:
    with pytest.raises(SupplyChainAdmissionError, match="Git SHA"):
        manifest(source_commit=source_commit)


@pytest.mark.parametrize("label", ["sbom_digest", "vex_digest", "provenance_digest"])
def test_evidence_digests_are_required(label: str) -> None:
    with pytest.raises(SupplyChainAdmissionError, match="SHA-256"):
        manifest(**{label: "invalid"})


def test_all_four_scan_kinds_are_required_exactly_once() -> None:
    with pytest.raises(SupplyChainAdmissionError, match="every required scan"):
        manifest(scans=scans()[:-1])
    duplicated = (*scans(), scans()[0])
    with pytest.raises(SupplyChainAdmissionError, match="every required scan"):
        manifest(scans=duplicated)


def test_scan_must_be_bound_to_promoted_artifact() -> None:
    with pytest.raises(SupplyChainAdmissionError, match="different artifact"):
        verify(sign(manifest(scans=scans(artifact_digest="9" * 64))))


@pytest.mark.parametrize("outcome", [ScanOutcome.FAIL, ScanOutcome.INCOMPLETE])
def test_failed_or_incomplete_scan_is_denied(outcome: ScanOutcome) -> None:
    with pytest.raises(SupplyChainAdmissionError, match="must pass"):
        verify(sign(manifest(scans=scans(outcome=outcome))))


def test_pass_scan_cannot_hide_findings() -> None:
    original = scans()[0]
    with pytest.raises(SupplyChainAdmissionError, match="zero findings"):
        replace(original, findings_count=1)


@pytest.mark.parametrize("version", ["latest", "main", "HEAD", " "])
def test_scanner_version_must_be_immutable(version: str) -> None:
    with pytest.raises(SupplyChainAdmissionError, match="immutable"):
        replace(scans()[0], scanner_version=version)


@pytest.mark.parametrize("status", [VexStatus.KNOWN_AFFECTED, VexStatus.UNDER_INVESTIGATION])
def test_unresolved_vex_status_is_denied(status: VexStatus) -> None:
    assertion = replace(manifest().vex_assertions[0], status=status)
    with pytest.raises(SupplyChainAdmissionError, match="unresolved"):
        verify(sign(manifest(vex_assertions=(assertion,))))


def test_fixed_vex_status_is_admissible() -> None:
    assertion = replace(manifest().vex_assertions[0], status=VexStatus.FIXED)
    assert verify(sign(manifest(vex_assertions=(assertion,)))).status == DECISION


def test_vex_requires_component_statement_and_justification() -> None:
    assertion = manifest().vex_assertions[0]
    with pytest.raises(SupplyChainAdmissionError, match="component_purl"):
        replace(assertion, component_purl="example")
    with pytest.raises(SupplyChainAdmissionError, match="SHA-256"):
        replace(assertion, statement_digest="bad")
    with pytest.raises(SupplyChainAdmissionError, match="justification"):
        replace(assertion, justification=" ")


def test_rebuild_between_environments_is_forbidden() -> None:
    with pytest.raises(SupplyChainAdmissionError, match="rebuild"):
        manifest(rebuild_between_environments=True)


def test_manifest_can_never_grant_production_authority() -> None:
    with pytest.raises(SupplyChainAdmissionError, match="production authority"):
        manifest(production_authorized=True)


def test_production_target_still_returns_no_deployment_authority() -> None:
    result = verify(sign(manifest(target_environment="production")))
    assert result.target_environment == "production"
    assert result.production_authorized is False
    assert result.status == DECISION


def test_manifest_validity_is_bounded_and_utc() -> None:
    with pytest.raises(SupplyChainAdmissionError, match="24 hours"):
        manifest(expires_at=NOW + timedelta(days=2))
    with pytest.raises(SupplyChainAdmissionError, match="expressed in UTC"):
        manifest(issued_at=NOW.astimezone(timezone(timedelta(hours=2))))
    with pytest.raises(SupplyChainAdmissionError, match="timezone-aware"):
        manifest(issued_at=NOW.replace(tzinfo=None))


@pytest.mark.parametrize(
    "verification_time",
    [NOW - timedelta(hours=2), NOW + timedelta(hours=2)],
)
def test_not_yet_valid_or_expired_manifest_is_denied(verification_time: datetime) -> None:
    envelope = sign(manifest())
    with pytest.raises(SupplyChainAdmissionError, match="not currently valid"):
        verify_signed_manifest(
            envelope,
            trusted_public_keys={KEY_ID: PUBLIC_KEY},
            trusted_builder_ids=frozenset({BUILDER_ID}),
            now=verification_time,
        )


def test_untrusted_builder_is_denied() -> None:
    with pytest.raises(SupplyChainAdmissionError, match="builder identity"):
        verify_signed_manifest(
            sign(manifest()),
            trusted_public_keys={KEY_ID: PUBLIC_KEY},
            trusted_builder_ids=frozenset({"github.com/another/builder"}),
            now=NOW,
        )


def test_untrusted_key_is_denied() -> None:
    with pytest.raises(SupplyChainAdmissionError, match="not trusted"):
        verify_signed_manifest(
            sign(manifest()),
            trusted_public_keys={},
            trusted_builder_ids=frozenset({BUILDER_ID}),
            now=NOW,
        )


def test_signature_from_wrong_key_is_denied() -> None:
    other = Ed25519PrivateKey.generate()
    with pytest.raises(SupplyChainAdmissionError, match="signature verification"):
        verify(sign(manifest(), other))


def test_payload_tampering_without_resigning_is_denied() -> None:
    original = sign(manifest())
    payload = copy.deepcopy(original.payload)
    payload["target_environment"] = "production"
    tampered = replace(original, payload=payload)
    with pytest.raises(SupplyChainAdmissionError, match="digest mismatch"):
        verify(tampered)


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("schema", "AILORA-SUPPLY-CHAIN-ADMISSION-V2", "schema"),
        ("provenance_predicate", "https://example.invalid", "predicate"),
        ("production_authorized", True, "production authority"),
        ("rebuild_between_environments", True, "rebuild"),
    ],
)
def test_boundary_tampering_is_denied_even_when_resigned(
    field: str, value: object, message: str
) -> None:
    payload = copy.deepcopy(manifest().payload())
    payload[field] = value
    with pytest.raises(SupplyChainAdmissionError, match=message):
        verify(resign_payload(payload))


def test_extra_or_missing_payload_field_is_denied() -> None:
    extra = copy.deepcopy(manifest().payload())
    extra["deployment_approved"] = True
    with pytest.raises(SupplyChainAdmissionError, match="fields are not exact"):
        verify(resign_payload(extra))
    missing = copy.deepcopy(manifest().payload())
    del missing["sbom_digest"]
    with pytest.raises(SupplyChainAdmissionError, match="fields are not exact"):
        verify(resign_payload(missing))
    non_boolean = copy.deepcopy(manifest().payload())
    non_boolean["production_authorized"] = "false"
    with pytest.raises(SupplyChainAdmissionError, match="malformed"):
        verify(resign_payload(non_boolean))
    non_boolean = copy.deepcopy(manifest().payload())
    non_boolean["rebuild_between_environments"] = 0
    with pytest.raises(SupplyChainAdmissionError, match="malformed"):
        verify(resign_payload(non_boolean))


def test_manifest_digest_is_exposed_in_decision() -> None:
    envelope = sign(manifest())
    assert verify(envelope).manifest_digest == envelope.manifest_digest
