"""Finite clean-export verification gate in a fresh directory (WDP-DP7-03)."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class CleanExportReceipt:
    status: str
    verified_files: int
    reason: str

def verify_clean_export_manifest(
    declared_hashes: dict[str, str],
    extracted_hashes: dict[str, str],
    referenced_outside_paths: tuple[str, ...] = (),
) -> CleanExportReceipt:
    if not declared_hashes:
        return CleanExportReceipt("REFUSED", 0, "EMPTY_DECLARED_MANIFEST")
    if referenced_outside_paths:
        return CleanExportReceipt("REFUSED", 0, "HERMETIC_ESCAPE_TO_CHECKOUT")
    for rel_path, expected_sha in sorted(declared_hashes.items()):
        if ".." in rel_path.split("/") or rel_path.startswith("/"):
            return CleanExportReceipt("REFUSED", 0, "UNSAFE_MANIFEST_PATH")
        actual_sha = extracted_hashes.get(rel_path)
        if actual_sha != expected_sha:
            return CleanExportReceipt("REFUSED", 0, f"HASH_MISMATCH:{rel_path}")
    if set(extracted_hashes) != set(declared_hashes):
        return CleanExportReceipt("REFUSED", 0, "UNDECLARED_EXTRACTED_FILE")
    return CleanExportReceipt("PASS", len(declared_hashes), "CLEAN_EXPORT_VERIFIED")

def witness_wdp_dp7_03() -> dict[str, object]:
    manifest = {"manuscript.md": "sha256:aaa", "code/witness.py": "sha256:bbb"}
    ok = verify_clean_export_manifest(manifest, dict(manifest))
    escaped = verify_clean_export_manifest(manifest, dict(manifest), ("../checkout_cache.json",))
    return {
        "control_id": "WDP-DP7-03",
        "positive_status": ok.status,
        "verified_files": ok.verified_files,
        "escaped_status": escaped.status,
        "escaped_reason": escaped.reason,
    }
