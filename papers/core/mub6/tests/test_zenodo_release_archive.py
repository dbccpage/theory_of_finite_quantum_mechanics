"""Independent Test Suite for Zenodo Release Archive & Checksum Manifest.

AuthorityEffect: None.

Audits:
1. Archive tarball existence and exact SHA-256 matching.
2. Manifest SHA-256 digest validation across 100% of entries.
3. Hermetic dry-run extraction and strict exclusion enforcement.
4. Archive custody separated from the blocked publication disposition.
"""

import gzip
import hashlib
import json
import os
from pathlib import Path
import shutil
import tarfile
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
TARBALL_PATH = REPO_ROOT / "zenodo" / "mub6_formal_archive_v1.0.tar.gz"
SHA256_MANIFEST_PATH = REPO_ROOT / "zenodo" / "release_manifest.sha256"
RELEASE_CHECKLIST_PATH = REPO_ROOT / "zenodo" / "release_checklist.md"
RELEASE_MANIFEST_JSON_PATH = REPO_ROOT / "zenodo" / "release_manifest.json"

FORBIDDEN_DIR_NAMES = {
    ".git",
    ".github",
    "target",
    ".lake",
    "lake-packages",
    "build",
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
    ".agents",
    "scratch",
    "logs",
    ".venv",
    "venv",
}

FORBIDDEN_EXTENSIONS = (
    ".pyc",
    ".pyo",
    ".swp",
    ".swo",
    "~",
    ".tmp",
    ".bak",
    ".log",
    ".pdb",
    ".rs.bk",
)

def compute_sha256(filepath: Path) -> str:
    """Match the builder's raw-byte custody; no line-ending normalization."""
    return hashlib.sha256(filepath.read_bytes()).hexdigest()


def test_tarball_exists_and_matches_digest():
    """Verify that the release tarball exists and matches the recorded digest in manifest and checklist."""
    assert TARBALL_PATH.is_file(), f"Tarball not found at {TARBALL_PATH}"
    assert TARBALL_PATH.stat().st_size > 1_000_000, "Tarball size suspiciously small"

    actual_digest = compute_sha256(TARBALL_PATH)

    # Check manifest.json
    with open(RELEASE_MANIFEST_JSON_PATH, "r", encoding="utf-8") as f:
        manifest_data = json.load(f)
    assert "release_archive" in manifest_data, "Missing 'release_archive' key in release_manifest.json"
    expected_digest_json = manifest_data["release_archive"]["sha256"]
    assert actual_digest == expected_digest_json, (
        f"Tarball digest mismatch with manifest.json: actual {actual_digest} != expected {expected_digest_json}"
    )

    # Check release_checklist.md
    checklist_text = RELEASE_CHECKLIST_PATH.read_text(encoding="utf-8")
    assert actual_digest in checklist_text, (
        f"Tarball digest {actual_digest} not found in {RELEASE_CHECKLIST_PATH}"
    )


def test_release_manifest_sha256_integrity():
    """Check historical members against archived bytes and live envelope files on disk.

    The maintained research tree can supersede an archived gap registry. Requiring
    those two snapshots to agree would force rewriting historical evidence.
    Current-tree integrity is checked separately by verify_deposit.py.
    """
    assert SHA256_MANIFEST_PATH.is_file(), f"SHA-256 manifest not found at {SHA256_MANIFEST_PATH}"

    lines = SHA256_MANIFEST_PATH.read_text(encoding="utf-8").splitlines()
    manifest_data = json.loads(RELEASE_MANIFEST_JSON_PATH.read_text(encoding="utf-8"))
    expected_entries = manifest_data["custody_counts"]["manifest_entry_count"]
    assert len(lines) == expected_entries, (
        f"Expected exactly {expected_entries} entries in release_manifest.sha256, got {len(lines)}"
    )

    non_archive = set(manifest_data["custody_counts"]["non_archive_entries"])
    checked = 0
    with tarfile.open(TARBALL_PATH, "r:gz") as archive:
        for line in lines:
            parts = line.split("  ", 1)
            assert len(parts) == 2, f"Malformed line in manifest: {line}"
            expected_digest, rel_path = parts
            if rel_path in non_archive:
                actual_digest = compute_sha256(REPO_ROOT / rel_path)
            else:
                member = archive.getmember(rel_path)
                assert member.isfile(), f"Nonregular historical member: {rel_path}"
                stream = archive.extractfile(member)
                assert stream is not None
                actual_digest = hashlib.sha256(stream.read()).hexdigest()
            assert actual_digest == expected_digest, (
                f"Digest mismatch for {rel_path}: actual {actual_digest} != expected {expected_digest}"
            )
            checked += 1

    assert checked == len(lines), f"Checked {checked} != {len(lines)} entries"


def test_dry_run_unpack_and_exclusion_audit():
    """Verify that the tarball unpacks cleanly in dry-run with zero forbidden files and exact digest matching."""
    # Parse release_manifest.sha256 for archive files
    lines = SHA256_MANIFEST_PATH.read_text(encoding="utf-8").splitlines()
    manifest_digests = {}
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split("  ", 1)
        if len(parts) == 2:
            manifest_digests[parts[1]] = parts[0]

    extracted_count = 0
    with tarfile.open(TARBALL_PATH, "r:gz") as tar:
        for member in tar.getmembers():
            parts = Path(member.name).parts
            for part in parts:
                assert part not in FORBIDDEN_DIR_NAMES, f"Forbidden directory extracted: {part} in {member.name}"
                assert not part.startswith(".git"), f"Forbidden .git directory extracted: {part} in {member.name}"
            assert not member.name.endswith(FORBIDDEN_EXTENSIONS), f"Forbidden file extension extracted: {member.name}"
            if member.isfile():
                f = tar.extractfile(member)
                assert f is not None, f"Failed to read member {member.name}"
                actual_digest = hashlib.sha256(f.read()).hexdigest()
                expected_digest = manifest_digests.get(member.name)
                assert expected_digest is not None, f"Extracted file {member.name} not found in release_manifest.sha256"
                assert actual_digest == expected_digest, (
                    f"Extracted file {member.name} digest mismatch: {actual_digest} != {expected_digest}"
                )
                extracted_count += 1

    assert extracted_count == len(manifest_digests) - 3, (
        f"Expected {len(manifest_digests) - 3} extracted files matching manifest, got {extracted_count}"
    )
    manifest_data = json.loads(RELEASE_MANIFEST_JSON_PATH.read_text(encoding="utf-8"))
    expected_members = manifest_data["custody_counts"]["archive_file_member_count"]
    assert extracted_count == expected_members, (
        f"Extracted count {extracted_count} != recorded archive_file_member_count {expected_members}"
    )


def test_release_checklist_status():
    """Archive custody must not silently promote unresolved research to approval."""
    text = RELEASE_CHECKLIST_PATH.read_text(encoding="utf-8")
    assert "AuthorityEffect: None" in text
    assert "Phase 6 Publication Release Checklist" in text
    assert "Publication status: BLOCKED" in text
    assert "APPROVED FOR ZENODO RELEASE DEPOSIT" not in text
    manifest = json.loads(RELEASE_MANIFEST_JSON_PATH.read_text(encoding="utf-8"))
    assert manifest["publication_ready"] is False
    assert manifest["publication_status"] == "BLOCKED"
    assert manifest["unresolved_obligations"]
    manuscript = REPO_ROOT / manifest["canonical_manuscript"]["file"]
    assert hashlib.sha256(manuscript.read_bytes()).hexdigest() == (
        manifest["canonical_manuscript"]["hashes"]["sha256_raw"]
    )
