#!/usr/bin/env python3
"""One-command verifier for the research paper deposit.

Deterministic, two-way verification:
1. Every file listed in SHA256SUMS exists and matches its recorded hash.
2. Sweep: no unrecorded non-excluded file is present in the deposit tree.
3. Fail-closed symlink rejection: rejects any unauthorized symlink.
4. Structural artifacts are present and non-empty.
5. Verification of the companion test suite: the package end-to-end tests,
   plus the custody tests the manuscript cites when the repository checkout
   that holds the Rust workspace and Lean project is present.
"""

from __future__ import annotations

import argparse
import hashlib
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "code"))
from deposit_paths import (
    DEFAULT_EXCLUDED_DIRS,
    DEFAULT_EXCLUDED_NAMES,
    DEFAULT_EXCLUDED_SUFFIXES,
    read_manifest,
    safe_path,
    walk_files,
)

ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "SHA256SUMS"

EXCLUDED_DIRS = DEFAULT_EXCLUDED_DIRS
EXCLUDED_NAMES = DEFAULT_EXCLUDED_NAMES
EXCLUDED_SUFFIXES = DEFAULT_EXCLUDED_SUFFIXES

REQUIRED_PATTERNS = (
    "finite_quantum_mechanics.md",
    "finite_quantum_mechanics.pdf",
    "finite_quantum_mechanics_change_log.md",
    "README.md",
    "LICENSE",
    "LICENSE-CODE",
    "pyproject.toml",
    "zenodo_metadata.json",
    "docs/descriptions.md",
    "docs/references.md",
    "code/deposit_paths.py",
)

E2E_DIRS = ("tests/e2e", "code/python/tests/e2e")
CUSTODY_TESTS = (
    "tests/legacy/unit/test_source_inventory.py",
    "tests/legacy/unit/test_retained_sources.py",
    "tests/legacy/unit/test_publication_status.py",
    "tests/legacy/unit/test_claim_ledger.py",
    "tests/legacy/unit/test_gap_register.py",
    "tests/legacy/unit/test_cochain.py",
)
PACKAGE_PATH = ("omega_engine_atlas", "coda_atlas", "F004_papers", "006_finite_qm")


def repository_checkout() -> Path | None:
    """Return the repository root when this deposit sits at its recorded path."""
    if ROOT.parts[-len(PACKAGE_PATH):] != PACKAGE_PATH:
        return None
    candidate = ROOT.parents[len(PACKAGE_PATH) - 1]
    if not (candidate / "omega_engine" / "crates_rs" / "Cargo.toml").is_file():
        return None
    return candidate


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def check_manifest(manifest_path: Path) -> list[str]:
    errors: list[str] = []
    try:
        excluded_names = set(EXCLUDED_NAMES)
        if manifest_path.name == "MANIFEST.sha256":
            excluded_names.add("MANIFEST.sha256")
        expected_files = walk_files(ROOT, EXCLUDED_DIRS, excluded_names, EXCLUDED_SUFFIXES)
        entries = read_manifest(ROOT, manifest_path)
        recorded = {relative for relative, _ in entries}
        for relative, digest in entries:
            path = safe_path(ROOT, relative)
            if not path.is_file():
                errors.append(f"Recorded file missing: {relative}")
            elif sha256_of(path) != digest:
                errors.append(f"Hash mismatch: {relative}")
        expected = {path.relative_to(ROOT).as_posix() for path in expected_files}
        for relative in sorted(expected - recorded):
            errors.append(f"Unrecorded deposit file: {relative}")
        for relative in sorted(recorded - expected):
            errors.append(f"Excluded file listed in manifest: {relative}")

        # Check required structural files/patterns
        for pattern in REQUIRED_PATTERNS:
            if "/" in pattern:
                target = ROOT / pattern
                if not target.is_file() or not target.stat().st_size:
                    errors.append(f"Required file missing or empty: {pattern}")
            else:
                matches = list(ROOT.glob(pattern))
                if not matches or not any(m.stat().st_size > 0 for m in matches):
                    errors.append(f"Required file pattern missing or empty: {pattern}")
        originals = list((ROOT / "sources" / "original_papers").glob("*/*.md"))
        if len(originals) != 67:
            errors.append(
                "Expected 67 original source manuscripts in "
                f"sources/original_papers, found {len(originals)}"
            )
    except (OSError, ValueError) as error:
        errors.append(str(error))
    return errors


def default_test_targets() -> tuple[list[str], list[str]]:
    """Return (targets to run, custody targets not run for lack of a checkout)."""
    targets: list[str] = []
    for relative in E2E_DIRS:
        tests_dir = ROOT / relative
        if tests_dir.is_dir():
            targets = sorted(
                p.relative_to(ROOT).as_posix()
                for p in tests_dir.glob("test_*.py")
                if p.name not in EXCLUDED_NAMES
            )
            break
    if repository_checkout() is None:
        return targets, list(CUSTODY_TESTS)
    return targets + list(CUSTODY_TESTS), []


def check_tests(targets: list[str]) -> list[str]:
    if not targets:
        return ["No test files found in tests/e2e/"]
    errors: list[str] = []
    for target in targets:
        try:
            path = safe_path(ROOT, target)
            if not target.endswith(".py") or not path.is_file():
                raise ValueError(f"Invalid test target: {target}")
            with tempfile.TemporaryDirectory(prefix="finite-qm-pytest-") as temporary:
                junit = Path(temporary) / "results.xml"
                result = subprocess.run(
                    [sys.executable, "-m", "pytest", target, "-q",
                     "-o", "xfail_strict=true", f"--junitxml={junit}"],
                    cwd=ROOT,
                    capture_output=True,
                    text=True,
                    timeout=180,
                    check=False,
                )
                if result.returncode:
                    errors.append(f"Pytest failure in {target}:\n{result.stdout}\n{result.stderr}")
                    continue
                report = ET.parse(junit).getroot()
                cases = list(report.iter("testcase"))
                if report.tag not in {"testsuite", "testsuites"} or not cases:
                    raise ValueError(f"No test-case evidence in {target}")
                if any(case.find(tag) is not None for case in cases
                       for tag in ("failure", "error", "skipped")):
                    raise ValueError(f"Selected tests failed or skipped in {target}")
        except (OSError, ValueError, ET.ParseError, subprocess.TimeoutExpired) as error:
            errors.append(str(error))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify paper deposit package.")
    parser.add_argument("--test", action="append", default=[], help="Named test file; repeat as needed.")
    args = parser.parse_args()

    all_errors: list[str] = []

    manifest_target = MANIFEST
    if not manifest_target.is_file() and (ROOT / "MANIFEST.sha256").is_file():
        manifest_target = ROOT / "MANIFEST.sha256"

    if not manifest_target.is_file():
        all_errors.append(f"Manifest not found: {manifest_target}")
    else:
        manifest_errors = check_manifest(manifest_target)
        all_errors.extend(manifest_errors)
        if manifest_errors:
            print(f"FAIL: Manifest checks failed ({len(manifest_errors)} issues):")
            for err in manifest_errors:
                print(f"  - {err}")
        else:
            print("OK: Manifest and two-way sweep checks passed.")

    not_run: list[str] = []
    targets = args.test
    if not targets:
        targets, not_run = default_test_targets()
    test_errors = check_tests(targets)
    all_errors.extend(test_errors)
    for error in test_errors:
        print(f"FAIL: {error}")
    if not test_errors:
        print(f"OK: Companion tests passed ({len(targets)} files).")
    for target in not_run:
        print(f"NOT RUN: {target} needs the repository checkout (README, Reproduction scope).")

    if all_errors:
        print(f"\nVerification FAILED with {len(all_errors)} errors.")
        return 1

    if not_run:
        print("\nVerification PASSED for the standalone scope only: manifest and end-to-end tests.")
    else:
        print("\nVerification PASSED.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
