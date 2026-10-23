"""Test Acceptance Criterion 1: Pytest Suite Execution and Manifest Isolation.

Verifies:
In 000_projection_obstruction, python -m pytest code/tests -m "not native_integration" -q --disable-warnings --tb=short
passes with 0 failures, and running pytest does not modify MANIFEST.sha256 or SHA256SUMS in the live package tree.

AuthorityEffect: None.
"""

from __future__ import annotations

import hashlib
import subprocess
import sys
from pathlib import Path

import pytest

from .config import PO000_DIR


def _hash_file_if_exists(path: Path) -> str | None:
    if not path.is_file():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_ac1_pytest_runs_with_zero_failures_and_preserves_manifest_integrity():
    """AC1: Pytest passes with 0 failures and leaves live manifests byte-identical."""
    manifest_sha256_path = PO000_DIR / "MANIFEST.sha256"
    sha256sums_path = PO000_DIR / "SHA256SUMS"

    # Pre-test snapshot
    hash_manifest_before = _hash_file_if_exists(manifest_sha256_path)
    hash_sha256sums_before = _hash_file_if_exists(sha256sums_path)

    cmd = [
        sys.executable,
        "-m",
        "pytest",
        "code/tests",
        "-m",
        "not native_integration",
        "-q",
        "--disable-warnings",
        "--tb=short",
    ]

    proc = subprocess.run(
        cmd,
        cwd=PO000_DIR,
        capture_output=True,
        text=True,
        timeout=180,
    )

    # Post-test snapshot
    hash_manifest_after = _hash_file_if_exists(manifest_sha256_path)
    hash_sha256sums_after = _hash_file_if_exists(sha256sums_path)

    # Manifest custody assertion: running pytest MUST NEVER modify live manifests
    assert hash_manifest_before == hash_manifest_after, (
        f"CRITICAL TEST ISOLATION FAILURE: Running pytest modified {manifest_sha256_path.name}!\n"
        f"Before: {hash_manifest_before}\nAfter:  {hash_manifest_after}"
    )
    assert hash_sha256sums_before == hash_sha256sums_after, (
        f"CRITICAL TEST ISOLATION FAILURE: Running pytest modified {sha256sums_path.name}!\n"
        f"Before: {hash_sha256sums_before}\nAfter:  {hash_sha256sums_after}"
    )

    # Exit code assertion
    assert proc.returncode == 0, (
        f"Pytest suite failed with exit code {proc.returncode}.\n"
        f"STDOUT:\n{proc.stdout}\n"
        f"STDERR:\n{proc.stderr}"
    )


def test_ac1_packaging_tests_use_isolated_directory():
    """AC1 / R3: Specifically verify test_paper_artifacts.py executes packaging builds in isolation."""
    test_file = PO000_DIR / "code" / "tests" / "test_paper_artifacts.py"
    assert test_file.is_file(), "test_paper_artifacts.py not found"

    manifest_sha256_path = PO000_DIR / "MANIFEST.sha256"
    sha256sums_path = PO000_DIR / "SHA256SUMS"

    hash_manifest_before = _hash_file_if_exists(manifest_sha256_path)
    hash_sha256sums_before = _hash_file_if_exists(sha256sums_path)

    cmd = [
        sys.executable,
        "-m",
        "pytest",
        "code/tests/test_paper_artifacts.py",
        "-q",
        "--disable-warnings",
        "--tb=short",
    ]

    proc = subprocess.run(
        cmd,
        cwd=PO000_DIR,
        capture_output=True,
        text=True,
        timeout=60,
    )

    hash_manifest_after = _hash_file_if_exists(manifest_sha256_path)
    hash_sha256sums_after = _hash_file_if_exists(sha256sums_path)

    assert hash_manifest_before == hash_manifest_after, (
        "Running test_paper_artifacts.py directly modified MANIFEST.sha256"
    )
    assert hash_sha256sums_before == hash_sha256sums_after, (
        "Running test_paper_artifacts.py directly modified SHA256SUMS"
    )
    assert proc.returncode == 0, f"test_paper_artifacts.py failed:\n{proc.stdout}\n{proc.stderr}"
