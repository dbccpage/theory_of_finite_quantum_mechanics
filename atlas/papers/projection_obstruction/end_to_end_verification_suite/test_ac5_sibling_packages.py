"""Test Acceptance Criterion 5: Sibling Packages Qualification.

Verifies:
Every sibling package (001, 006, 007, 008, 009, 033, 034, 035) passes its pytest suite
and its verify_deposit.py / manifest verification gate with exit code 0 and zero SHA-256 mismatches.

AuthorityEffect: None.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

from .checks.manifest_checker import check_manifest
from .config import SIBLING_PACKAGES, PackageSpec


@pytest.mark.parametrize("pkg_id", sorted(SIBLING_PACKAGES.keys()))
def test_ac5_sibling_pytest_suite(pkg_id: str):
    """AC5: Each sibling package passes its automated pytest suite with zero failures."""
    spec = SIBLING_PACKAGES[pkg_id]
    proc = subprocess.run(
        spec.pytest_command,
        cwd=spec.path,
        capture_output=True,
        text=True,
        timeout=180,
    )
    assert proc.returncode == 0, (
        f"Package {spec.name} ({pkg_id}) pytest suite failed with exit code {proc.returncode}:\n"
        f"STDOUT:\n{proc.stdout}\n"
        f"STDERR:\n{proc.stderr}"
    )


@pytest.mark.parametrize("pkg_id", sorted(SIBLING_PACKAGES.keys()))
def test_ac5_sibling_deposit_verifier(pkg_id: str):
    """AC5: Each sibling package passes its deposit verification script with returncode 0."""
    spec = SIBLING_PACKAGES[pkg_id]
    proc = subprocess.run(
        spec.deposit_verifier_command,
        cwd=spec.path,
        capture_output=True,
        text=True,
        timeout=240,
    )
    assert proc.returncode == 0, (
        f"Package {spec.name} ({pkg_id}) deposit verifier failed with exit code {proc.returncode}:\n"
        f"STDOUT:\n{proc.stdout}\n"
        f"STDERR:\n{proc.stderr}"
    )


@pytest.mark.parametrize("pkg_id", sorted(SIBLING_PACKAGES.keys()))
def test_ac5_sibling_manifest_checksums(pkg_id: str):
    """AC5: Direct cryptographic check of SHA256SUMS for each sibling package."""
    spec = SIBLING_PACKAGES[pkg_id]
    manifest_name = "SHA256SUMS"
    res = check_manifest(spec.path, manifest_name)
    assert res.passed, (
        f"Package {spec.name} manifest {manifest_name} check failed:\n"
        f"Missing files: {res.missing_files}\n"
        f"Hash mismatches: {res.mismatches}\n"
        f"Errors: {res.errors}"
    )
