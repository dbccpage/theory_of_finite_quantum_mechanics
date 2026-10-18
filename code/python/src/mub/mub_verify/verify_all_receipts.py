"""Automated Verification Suite for All MUB(6) Certified JSON Receipts.

AuthorityEffect: None.
Firewall Line: `stated region only; mints no authority`

Audits all certified JSON receipts against the canonical manifest:
- Validates manifest schema, metadata, and firewall statements.
- Computes and verifies exact SHA-256 digests against manifest entries.
- Strictly forbids floating-point representations (zero-float policy, exact rational only).
- Verifies formal certificate verification status and firewall adherence.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys
from typing import Any, Dict, List, Optional, Union

EXPECTED_MANIFEST_VERSION = "1.0.0"
EXPECTED_PROJECT = "MUB(6)"
EXPECTED_AUTHORITY_EFFECT = "None"
EXPECTED_FIREWALL_LINE = "stated region only; mints no authority"
EXPECTED_TOTAL_RECEIPTS = 11
EXPECTED_RECEIPT_REGISTRY = [
    ('Phase 4 Decisive Bifurcation', 'mub_decisive_bifurcation_terminal_receipt.json', 'omega.mub6.decisive_bifurcation_terminal_receipt.v1'),
    ('Target A10', 'mub_target_a10_global_cover_receipt.json', 'omega.mub.target-a10-global-cover.v1'),
    ('Target A11', 'mub_target_a11_orbit_exhaustiveness_receipt.json', 'omega.mub.target-a11-orbit-exhaustiveness.v1'),
    ('Target A12', 'mub_target_a12_smale_sentry_receipt.json', 'omega.mub.target-a12-smale-sentry.v1'),
    ('Target A13', 'mub_target_a13_grand_synthesis_receipt.json', 'omega.mub.target-a13-grand-synthesis.v1'),
    ('Target A2', 'mub_target_a2_deltoid_cusp_receipt.json', 'omega.mub.target-a2-deltoid-cusp.v1'),
    ('Target A8', 'mub_target_a8_collar_boundary_receipt.json', 'omega.mub.target-a8-collar-boundary.v1'),
    ('Target A9', 'mub_target_a9_haagerup_receipt.json', 'omega.mub.target-a9-haagerup.v1'),
    ('Target B1', 'mub_target_b1_continuous_chaining_receipt.json', 'mub.target_b1_continuous_chaining_receipt.v1'),
    ('Target B2', 'mub_target_b2_global_gluing_receipt.json', 'mub.target_b2_global_gluing_receipt.v1'),
    ('Target B3', 'mub_target_b3_manifold_integration_receipt.json', 'mub.target_b3_manifold_integration_receipt.v1'),
]



class ReceiptVerificationError(Exception):
    """Raised when receipt verification fails."""
    pass


def assert_no_float(obj: Any, path: str = "$") -> None:
    """Recursively traverse a JSON data structure and assert zero float values.

    Args:
        obj: The object to inspect.
        path: Path string for informative error tracking.

    Raises:
        TypeError: If any floating-point number is encountered.
    """
    if isinstance(obj, float):
        raise TypeError(f"Floating-point value forbidden at {path}: {obj!r}")
    elif isinstance(obj, dict):
        for k, v in obj.items():
            assert_no_float(v, f"{path}.{k}")
    elif isinstance(obj, (list, tuple)):
        for idx, item in enumerate(obj):
            assert_no_float(item, f"{path}[{idx}]")


def _forbid_float_token(token: str) -> None:
    """JSON parser hook to strictly reject any float literal during parsing."""
    raise ValueError(f"Floating-point token '{token}' strictly forbidden in exact receipt JSON")


def load_and_validate_receipt(filepath: Path) -> Dict[str, Any]:
    """Read and parse a certified receipt JSON file with strict float rejection.

    Args:
        filepath: Path to the receipt JSON file.

    Returns:
        Parsed JSON dictionary.

    Raises:
        ReceiptVerificationError: If the file is missing, invalid JSON, or contains floats.
    """
    if not filepath.is_file():
        raise ReceiptVerificationError(f"Receipt file does not exist: {filepath}")

    raw_bytes = filepath.read_bytes()

    try:
        data = json.loads(raw_bytes.decode("utf-8"), parse_float=_forbid_float_token)
    except Exception as exc:
        raise ReceiptVerificationError(f"Failed to parse JSON in {filepath.name}: {exc}") from exc

    try:
        assert_no_float(data, path=filepath.name)
    except TypeError as exc:
        raise ReceiptVerificationError(f"Float validation failure in {filepath.name}: {exc}") from exc

    return data


def verify_all_receipts(
    artifacts_dir: Optional[Union[Path, str]] = None,
    manifest_path: Optional[Union[Path, str]] = None,
) -> Dict[str, Any]:
    """Verify all certified receipts against the canonical manifest.

    Args:
        artifacts_dir: Directory containing receipt JSON files. Defaults to repo 'artifacts/'.
        manifest_path: Path to manifest.json. Defaults to 'artifacts/manifest.json'.

    Returns:
        Summary dictionary: {"all_passed": bool, "receipts_verified": int, "errors": List[str]}
    """
    if artifacts_dir is None:
        # The paper's own artifacts: code/mub_verify/ -> paper root.
        resolved_artifacts = Path(__file__).resolve().parents[2] / "artifacts"
    else:
        resolved_artifacts = Path(artifacts_dir)

    if manifest_path is None:
        resolved_manifest = resolved_artifacts / "manifest.json"
    else:
        resolved_manifest = Path(manifest_path)

    errors: List[str] = []
    receipts_verified = 0

    if not resolved_manifest.is_file():
        errors.append(f"Manifest file not found at: {resolved_manifest}")
        return {
            "all_passed": False,
            "receipts_verified": 0,
            "errors": errors,
        }

    # Load and validate manifest
    try:
        raw_manifest_bytes = resolved_manifest.read_bytes()
        manifest_data = json.loads(
            raw_manifest_bytes.decode("utf-8"), parse_float=_forbid_float_token
        )
        assert_no_float(manifest_data, path="manifest.json")
    except Exception as exc:
        errors.append(f"Failed to parse manifest {resolved_manifest}: {exc}")
        return {
            "all_passed": False,
            "receipts_verified": 0,
            "errors": errors,
        }

    # Manifest metadata validation
    if manifest_data.get("manifest_version") != EXPECTED_MANIFEST_VERSION:
        errors.append(
            f"Invalid manifest_version: expected '{EXPECTED_MANIFEST_VERSION}', "
            f"got '{manifest_data.get('manifest_version')}'"
        )
    if manifest_data.get("project") != EXPECTED_PROJECT:
        errors.append(
            f"Invalid project: expected '{EXPECTED_PROJECT}', "
            f"got '{manifest_data.get('project')}'"
        )
    if manifest_data.get("authority_effect") != EXPECTED_AUTHORITY_EFFECT:
        errors.append(
            f"Invalid authority_effect: expected '{EXPECTED_AUTHORITY_EFFECT}', "
            f"got '{manifest_data.get('authority_effect')}'"
        )
    if manifest_data.get("firewall_line") != EXPECTED_FIREWALL_LINE:
        errors.append(
            f"Invalid firewall_line in manifest: expected '{EXPECTED_FIREWALL_LINE}', "
            f"got '{manifest_data.get('firewall_line')}'"
        )
    if not isinstance(manifest_data.get("timestamp"), str) or not manifest_data.get("timestamp"):
        errors.append("Manifest missing valid ISO-8601 timestamp")

    receipts_list = manifest_data.get("receipts")
    if not isinstance(receipts_list, list):
        errors.append(f"Manifest 'receipts' must be a list, got {type(receipts_list).__name__}")
        return {
            "audit_type": "FILE_INTEGRITY_AND_METADATA_AUDIT",
            "mathematical_theorem_replay_dispatched": False,
            "theorem_replay_status": "MISSING_MATHEMATICAL_REPLAY_DISPATCH",
            "missing_replay_obligations": [
                "Target A12",
                "Target A13",
                "Target B1",
                "Target B2",
                "Target B3",
            ],
            "all_passed": False,
            "receipts_verified": 0,
            "errors": errors,
        }

    if len(receipts_list) != EXPECTED_TOTAL_RECEIPTS:
        errors.append(
            f"Expected {EXPECTED_TOTAL_RECEIPTS} receipts in manifest, found {len(receipts_list)}"
        )
    if manifest_data.get("total_receipts") != EXPECTED_TOTAL_RECEIPTS:
        errors.append(
            f"Expected total_receipts {EXPECTED_TOTAL_RECEIPTS}, found {manifest_data.get('total_receipts')}"
        )

    actual_registry = [(e.get("target"), e.get("filename"), e.get("schema_version"))
                       for e in receipts_list if isinstance(e, dict)]
    if len(actual_registry) != len(receipts_list) or set(actual_registry) != set(EXPECTED_RECEIPT_REGISTRY) or len(set(actual_registry)) != len(actual_registry):
        return {
            "audit_type": "FILE_INTEGRITY_AND_METADATA_AUDIT",
            "mathematical_theorem_replay_dispatched": False,
            "theorem_replay_status": "MISSING_MATHEMATICAL_REPLAY_DISPATCH",
            "missing_replay_obligations": [
                "Target A12",
                "Target A13",
                "Target B1",
                "Target B2",
                "Target B3",
            ],
            "all_passed": False,
            "receipts_verified": 0,
            "errors": errors + ["Receipt registry mismatch or duplicate"],
        }

    # Verification of individual receipts
    for idx, entry in enumerate(receipts_list):
        target = entry.get("target")
        filename = entry.get("filename")
        expected_sha256 = entry.get("sha256")
        expected_schema = entry.get("schema_version")
        manifest_verified = entry.get("verified")
        arithmetic = entry.get("arithmetic")
        entry_firewall = entry.get("firewall_line")

        entry_prefix = f"Receipt[{idx}] ({target} / {filename})"

        if not filename:
            errors.append(f"{entry_prefix}: Missing filename")
            continue

        receipt_file = (resolved_artifacts / filename).resolve()
        if not receipt_file.is_relative_to(resolved_artifacts.resolve()):
            errors.append(f"{entry_prefix}: receipt path outside artifacts root")
            continue
        if not receipt_file.is_file():
            errors.append(f"{entry_prefix}: File not found at {receipt_file}")
            continue

        # Check raw SHA-256 (with canonical LF normalization for Windows line-ending resilience)
        raw_receipt_bytes = receipt_file.read_bytes()
        actual_sha256 = hashlib.sha256(raw_receipt_bytes).hexdigest()
        if actual_sha256 != expected_sha256:
            # Check if difference is strictly due to platform CRLF line-ending conversion
            norm_sha256 = hashlib.sha256(raw_receipt_bytes.replace(b"\r\n", b"\n")).hexdigest()
            if norm_sha256 == expected_sha256:
                actual_sha256 = norm_sha256
        if actual_sha256 != expected_sha256:
            errors.append(
                f"{entry_prefix}: SHA-256 digest mismatch. "
                f"Expected {expected_sha256}, got {actual_sha256}"
            )
            continue

        # Load and float-check receipt data
        try:
            receipt_data = load_and_validate_receipt(receipt_file)
        except ReceiptVerificationError as exc:
            errors.append(f"{entry_prefix}: {exc}")
            continue

        # Validate schema version
        receipt_schema = receipt_data.get("schema_version")
        if receipt_schema != expected_schema:
            errors.append(
                f"{entry_prefix}: Schema mismatch. "
                f"Manifest specifies '{expected_schema}', receipt has '{receipt_schema}'"
            )

        # Validate verified flag
        receipt_verified = receipt_data.get("verified")
        if receipt_verified is not True:
            errors.append(f"{entry_prefix}: Receipt verified status is not True ({receipt_verified!r})")
        if manifest_verified is not True:
            errors.append(f"{entry_prefix}: Manifest verified flag is not True ({manifest_verified!r})")

        # Validate arithmetic mode
        if arithmetic != "exact rational / cyclotomic":
            errors.append(
                f"{entry_prefix}: Manifest arithmetic must be 'exact rational / cyclotomic', got '{arithmetic}'"
            )

        # Validate firewall statement in entry and in receipt
        if entry_firewall != EXPECTED_FIREWALL_LINE:
            errors.append(
                f"{entry_prefix}: Manifest entry firewall mismatch: expected '{EXPECTED_FIREWALL_LINE}', "
                f"got '{entry_firewall}'"
            )

        receipt_firewall = receipt_data.get("firewall") or receipt_data.get("firewall_line")
        if receipt_firewall != EXPECTED_FIREWALL_LINE:
            errors.append(
                f"{entry_prefix}: Receipt body firewall mismatch: expected '{EXPECTED_FIREWALL_LINE}', "
                f"got '{receipt_firewall}'"
            )

        # Check that receipt is not an empty 3-field stub and contains mathematical payload
        math_payload_keys = [
            k for k in receipt_data.keys()
            if k not in ("schema_version", "verified", "firewall", "firewall_line", "authority_effect", "project")
        ]
        if not math_payload_keys or len(receipt_data) <= 3:
            errors.append(
                f"{entry_prefix}: Receipt contains no mathematical certificate payload (only {list(receipt_data.keys())})"
            )
            continue

        receipts_verified += 1

    all_passed = (len(errors) == 0) and (receipts_verified == EXPECTED_TOTAL_RECEIPTS)

    return {
        "audit_type": "FILE_INTEGRITY_AND_METADATA_AUDIT",
        "mathematical_theorem_replay_dispatched": False,
        "theorem_replay_status": "MISSING_MATHEMATICAL_REPLAY_DISPATCH",
        "missing_replay_obligations": [
            "Target A12",
            "Target A13",
            "Target B1",
            "Target B2",
            "Target B3",
        ],
        "all_passed": all_passed,
        "receipts_verified": receipts_verified,
        "errors": errors,
    }


def main() -> None:
    """CLI execution entrypoint."""
    print("=" * 80)
    print("MUB(6) CERTIFIED RECEIPT COMPREHENSIVE VERIFICATION SUITE")
    print("AuthorityEffect: None")
    print(f"Firewall Line: {EXPECTED_FIREWALL_LINE}")
    print("=" * 80)

    artifacts_dir = Path(__file__).resolve().parents[2] / "artifacts"
    manifest_path = artifacts_dir / "manifest.json"

    print(f"Artifacts Directory : {artifacts_dir}")
    print(f"Manifest Path       : {manifest_path}")
    print("-" * 80)

    summary = verify_all_receipts(artifacts_dir=artifacts_dir, manifest_path=manifest_path)

    print(f"Total Receipts Verified: {summary['receipts_verified']} / {EXPECTED_TOTAL_RECEIPTS}")
    print(f"All Checks Passed      : {summary['all_passed']}")

    if summary["errors"]:
        print("\nERRORS ENCOUNTERED:")
        for err in summary["errors"]:
            print(f"  [ERROR] {err}")
        print("=" * 80)
        sys.exit(1)
    else:
        print(f"\nSUCCESS: All {EXPECTED_TOTAL_RECEIPTS} certified receipts validated 100% cleanly.")
        print("  - Zero floating-point tokens detected (exact rational/cyclotomic only).")
        print("  - Exact SHA-256 checksums match canonical manifest.")
        print("  - Schema versions, verification flags, and epistemic firewalls verified.")
        print("=" * 80)
        sys.exit(0)


if __name__ == "__main__":
    main()
