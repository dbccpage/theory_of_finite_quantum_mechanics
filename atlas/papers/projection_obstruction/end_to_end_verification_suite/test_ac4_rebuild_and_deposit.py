"""Test Acceptance Criterion 4: Rebuild Artifacts and Deposit Verification for PO-000.

Verifies:
projection_obstruction.tex, projection_obstruction.pdf, MANIFEST.sha256, SHA256SUMS,
dist/projection_obstruction_v6.9.18.zip, and sidecar are rebuilt, and
python verify_deposit.py (both --integrity-only and full verification) exits 0 with zero mismatches.

AuthorityEffect: None.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pytest

from .checks.manifest_checker import check_manifest
from .config import PO000_DIR


def test_ac4_rebuilt_artifacts_present():
    """AC4: Verify all rebuilt publication artifacts exist on disk."""
    required_artifacts = [
        PO000_DIR / "projection_obstruction.tex",
        PO000_DIR / "projection_obstruction.pdf",
        PO000_DIR / "MANIFEST.sha256",
        PO000_DIR / "SHA256SUMS",
    ]
    for art in required_artifacts:
        assert art.is_file(), f"Required publication artifact missing: {art}"

    # Check release archive and sidecar in dist/
    dist_dir = PO000_DIR / "dist"
    archives = sorted(dist_dir.glob("projection_obstruction_v*.zip"))
    assert len(archives) >= 1, f"No release archive found in {dist_dir}"

    archive = archives[0]
    sidecar = archive.with_suffix(archive.suffix + ".sha256")
    assert sidecar.is_file(), f"Release archive sidecar missing: {sidecar}"

    # Sidecar integrity check
    sidecar_content = sidecar.read_text(encoding="utf-8").strip()
    sidecar_hash, _, sidecar_name = sidecar_content.partition("  ")
    archive_hash = hashlib.sha256(archive.read_bytes()).hexdigest()
    assert sidecar_hash == archive_hash, (
        f"Sidecar digest mismatch for {archive.name}: expected {archive_hash}, got {sidecar_hash}"
    )


def test_ac4_manifest_integrity_check():
    """AC4: Direct cryptographic check of SHA256SUMS and MANIFEST.sha256 in PO-000."""
    res_sums = check_manifest(PO000_DIR, "SHA256SUMS")
    assert res_sums.passed, (
        f"SHA256SUMS verification failed:\n"
        f"Missing: {res_sums.missing_files}\nMismatches: {res_sums.mismatches}\nErrors: {res_sums.errors}"
    )

    res_manifest = check_manifest(PO000_DIR, "MANIFEST.sha256")
    assert res_manifest.passed, (
        f"MANIFEST.sha256 verification failed:\n"
        f"Missing: {res_manifest.missing_files}\nMismatches: {res_manifest.mismatches}\nErrors: {res_manifest.errors}"
    )


def test_ac4_verify_deposit_integrity_only():
    """AC4: verify_deposit.py --integrity-only exits 0 with zero mismatches."""
    cmd = [sys.executable, "verify_deposit.py", "--integrity-only"]
    proc = subprocess.run(cmd, cwd=PO000_DIR, capture_output=True, text=True, timeout=60)
    assert proc.returncode == 0, (
        f"verify_deposit.py --integrity-only failed with exit code {proc.returncode}:\n"
        f"STDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}"
    )
    assert "FAIL:" not in proc.stdout, f"verify_deposit.py reported FAIL:\n{proc.stdout}"


def test_ac4_verify_deposit_full():
    """AC4: Full verify_deposit.py exits 0 with zero mismatches."""
    cmd = [sys.executable, "verify_deposit.py"]
    proc = subprocess.run(cmd, cwd=PO000_DIR, capture_output=True, text=True, timeout=300)
    assert proc.returncode == 0, (
        f"Full verify_deposit.py failed with exit code {proc.returncode}:\n"
        f"STDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}"
    )
    assert "FAIL:" not in proc.stdout, f"verify_deposit.py reported FAIL:\n{proc.stdout}"
