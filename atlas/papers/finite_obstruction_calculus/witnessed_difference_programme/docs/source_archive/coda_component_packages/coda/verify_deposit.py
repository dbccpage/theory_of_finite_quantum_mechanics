#!/usr/bin/env python3
"""One-command verifier for the CODA deposit.

Deterministic, two-way verification:
1. Every file listed in SHA256SUMS exists and matches its recorded hash.
2. Sweep: no extra file is present in the deposit tree that SHA256SUMS does not list.
3. Fail-closed symlink rejection: actively rejects any unauthorized symlink.
4. Required release files are present and non-empty.
5. Optional named test files pass (--test; at most three).
6. Optional (--lean): lake build succeeds and axiom census stays within whitelist.
"""

from __future__ import annotations

import argparse
import hashlib
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "code"))
from deposit_paths import read_manifest, safe_path, walk_files

ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "SHA256SUMS"

EXCLUDED_DIRS = {
    ".git", ".venv", "venv", "__pycache__", ".pytest_cache",
    ".mypy_cache", ".ruff_cache", ".ipynb_checkpoints", ".lake",
    "dist", "build", "htmlcov", "dev_rips", "rt",
    "b", "scratch",
    "_support", "evidence", "reconstruction_v1",
}
EXCLUDED_NAMES = {"SHA256SUMS", ".coverage", "DEPOSIT_CHECKLIST.md", ".gitkeep"}
EXCLUDED_SUFFIXES = {".zip", ".pyc", ".pyo", ".tmp", ".log"}

REQUIRED_FILES = (
    "code/audit_legacy_embedding.py",
    "code/build_claim_index.py",
    "code/build_notebook.py",
    "code/coda_core.py",
    "code/coda_discipline_core.py",
    "code/generate_figures.py",
    "code/replay_notebook.py",
    "code/run_examples.py",
    "code/verify_package.py",
    "code/fixtures/examples.json",
    "code/fixtures/legacy_counterexample.json",
    "code/tests/test_adversarial_obstruction_sheaf.py",
    "code/tests/test_coda_core.py",
    "code/tests/test_coda_discipline.py",
    "coda.md",
    "coda.tex",
    "coda.pdf",
    "coda_claim_ledger.md",
    "coda_change_log.md",
    "docs/descriptions.md",
    "docs/references.md",
    "docs/keywords.md",
    "docs/lean_claim_map.md",
    "docs/validation.md",
    "docs/historical_build_logs.md",
    "jupyter_notebooks/01_coda_walkthrough.ipynb",
    "lean4/AxiomAudit.lean",
    "lean4/Coda.lean",
    "lean4/Boundaries.lean",
    "lean4/Discipline.lean",
    "lean4/DisciplineCore.lean",
    "lean4/Foundations.lean",
    "lean4/lakefile.lean",
    "lean4/lake-manifest.json",
    "lean4/lean-toolchain",
    "lean4/axiom_report.txt",
    "LICENSE",
    "LICENSE-CODE",
    "MANIFEST.sha256",
    "pyproject.toml",
    "requirements.txt",
    "source_manifest.json",
    "claim_index.json",
    "zenodo_metadata.json",
    "README.md",
    "scripts/build_deposit_zip.py",
    "scripts/regen_sha256sums.py",
    "verify_deposit.py",
)

AXIOM_WHITELIST = frozenset({"Quot.sound", "propext", "Classical.choice", "choice"})


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def check_manifest(manifest_path: Path) -> list[str]:
    errors: list[str] = []
    try:
        expected_files = walk_files(ROOT, EXCLUDED_DIRS, EXCLUDED_NAMES, EXCLUDED_SUFFIXES)
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
        for relative in REQUIRED_FILES:
            path = safe_path(ROOT, relative)
            if not path.is_file() or not path.stat().st_size:
                errors.append(f"Required file missing or empty: {relative}")
    except (OSError, ValueError) as error:
        errors.append(str(error))
    return errors


def check_tests(targets: list[str]) -> list[str]:
    if not 1 <= len(targets) <= 3:
        return ["Select one to three named test files"]
    errors: list[str] = []
    for target in targets:
        try:
            path = safe_path(ROOT, target)
            if not target.startswith("code/tests/test_") or path.suffix != ".py" or not path.is_file():
                raise ValueError("Select an existing code/tests/test_*.py file")
            result = subprocess.run([sys.executable, "-m", "pytest", target, "-q"],
                                    cwd=ROOT, capture_output=True, text=True, timeout=180, check=False)
            if result.returncode:
                errors.append(result.stdout + result.stderr)
        except (OSError, ValueError, subprocess.TimeoutExpired) as error:
            errors.append(str(error))
    return errors


def check_lean() -> list[str]:
    lean_dir = ROOT / "lean4"
    if not (lean_dir / "lakefile.lean").is_file():
        return ["Missing lean4/lakefile.lean"]
    errors: list[str] = []
    build_result = subprocess.run(
        ["lake", "build"], cwd=str(lean_dir), capture_output=True, text=True, encoding="utf-8", timeout=60, check=False
    )
    if build_result.returncode != 0:
        errors.append(f"lake build failed:\n{build_result.stdout}\n{build_result.stderr}")
        return errors

    census_result = subprocess.run(
        ["lake", "env", "lean", "AxiomAudit.lean"],
        cwd=str(lean_dir),
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=60,
        check=False,
    )
    if census_result.returncode != 0:
        errors.append(f"axiom census failed:\n{census_result.stdout}\n{census_result.stderr}")
        return errors

    for line in census_result.stdout.splitlines():
        line = line.strip()
        if "depends on axioms:" in line:
            axioms_part = line.split("depends on axioms:")[1].strip()
            axioms_part = axioms_part.strip("[]")
            for ax in axioms_part.split(","):
                ax_name = ax.strip()
                if ax_name and ax_name not in AXIOM_WHITELIST:
                    errors.append(f"Unauthorized axiom dependency: {ax_name} in '{line}'")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify CODA deposit.")
    parser.add_argument("--lean", action="store_true", help="Run Lean verification and axiom audit.")
    parser.add_argument("--test", action="append", default=[], help="Named test file; repeat up to three times.")
    args = parser.parse_args()

    all_errors: list[str] = []

    manifest_errors = check_manifest(MANIFEST)
    all_errors.extend(manifest_errors)
    if manifest_errors:
        print(f"FAIL: Manifest checks failed ({len(manifest_errors)} issues):")
        for err in manifest_errors:
            print(f"  - {err}")
    else:
        print("OK: Manifest and two-way sweep checks passed.")

    if args.test:
        test_errors = check_tests(args.test)
        all_errors.extend(test_errors)
        for error in test_errors:
            print(f"FAIL: {error}")
        if not test_errors:
            print("OK: selected test files passed.")

    if args.lean:
        try:
            lean_errors = check_lean()
        except (OSError, subprocess.TimeoutExpired) as error:
            lean_errors = [f"Lean verification did not complete: {error}"]
        all_errors.extend(lean_errors)
        if lean_errors:
            print("FAIL: Lean checks failed.")
            for err in lean_errors:
                print(f"  - {err}")
        else:
            print("OK: Lean proofs and axiom census verified.")

    if all_errors:
        print(f"\nVerification FAILED with {len(all_errors)} errors.")
        return 1

    print("\nVerification PASSED.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
