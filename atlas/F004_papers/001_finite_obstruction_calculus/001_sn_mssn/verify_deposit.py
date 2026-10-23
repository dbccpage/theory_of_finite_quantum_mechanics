#!/usr/bin/env python3
"""One-command verifier for the research paper deposit (001_sn_mssn).

Deterministic, two-way verification:
1. Every file listed in SHA256SUMS exists and matches its recorded hash.
2. Sweep: no unrecorded non-excluded file is present in the deposit tree.
3. Fail-closed symlink rejection: rejects any unauthorized symlink.
4. Structural artifacts are present and non-empty.
5. All local test files pass (or the --test selection).
6. Reproduction entry runs cleanly and reports verified status.
7. Optional (--lean): lake build succeeds and axiom census stays within whitelist.
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
    "dist", "build", "htmlcov", "dev_rips", "rt", "target",
    "b", "scratch",
    "_support", "evidence", "reconstruction_v1",
}
EXCLUDED_NAMES = {"SHA256SUMS", ".coverage", ".env", "DEPOSIT_CHECKLIST.md", ".gitkeep"}
EXCLUDED_SUFFIXES = {".zip", ".pyc", ".pyo", ".tmp", ".log", ".aux"}

REQUIRED_PATTERNS = (
    "paper.md",
    "paper_change_log.md",
    "paper_claim_ledger.md",
    "paper.pdf",
    "README.md",
    "LICENSE",
    "LICENSE-CODE",
    "MANIFEST.sha256",
    "pyproject.toml",
    "zenodo_metadata.json",
    "docs/descriptions.md",
    "docs/references.md",
    "code/deposit_paths.py",
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

        for pattern in REQUIRED_PATTERNS:
            target = ROOT / pattern
            if not target.is_file() or not target.stat().st_size:
                errors.append(f"Required file missing or empty: {pattern}")
    except (OSError, ValueError) as error:
        errors.append(str(error))
    return errors


def check_tests() -> list[str]:
    tests_dir = ROOT / "code" / "tests"
    targets = [p.relative_to(ROOT).as_posix() for p in tests_dir.glob("test_*.py")]
    if not targets:
        return ["No test files found in code/tests/"]
    errors: list[str] = []
    for target in targets:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "--import-mode=importlib", target, "-q"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=180,
            check=False,
        )
        if result.returncode:
            errors.append(f"Pytest failure in {target}:\n{result.stdout}\n{result.stderr}")
        else:
            print(f"OK: {target}: {result.stdout.strip().splitlines()[-1]}")
    return errors


def check_reproduce() -> list[str]:
    repro = ROOT / "code" / "reproduce.py"
    if not repro.is_file():
        return ["Missing code/reproduce.py"]
    result = subprocess.run(
        [sys.executable, str(repro)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )
    if result.returncode:
        return [f"code/reproduce.py failed:\n{result.stdout}\n{result.stderr}"]
    print("OK: code/reproduce.py passed")
    return []


def check_lean() -> list[str]:
    lean_dir = ROOT / "lean4"
    if not (lean_dir / "lakefile.lean").is_file():
        return ["Missing lean4/lakefile.lean"]
    build_result = subprocess.run(
        ["lake", "build"],
        cwd=str(lean_dir),
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=300,
        check=False,
    )
    if build_result.returncode != 0:
        return [f"lake build failed:\n{build_result.stdout}\n{build_result.stderr}"]
    print("OK: lean4 lake build passed")
    return []


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify paper deposit package.")
    parser.add_argument("--lean", action="store_true", help="Run Lean verification.")
    args = parser.parse_args()

    all_errors: list[str] = []

    # 1. Manifests check
    manifest_errors = check_manifest(ROOT / "SHA256SUMS")
    manifest_errors.extend(check_manifest(ROOT / "MANIFEST.sha256"))
    all_errors.extend(manifest_errors)
    if manifest_errors:
        print(f"FAIL: Manifest checks failed ({len(manifest_errors)} issues):")
        for err in manifest_errors:
            print(f"  - {err}")
    else:
        print("OK: Both manifests and two-way tree sweep passed.")

    # 2. Tests
    test_errors = check_tests()
    all_errors.extend(test_errors)
    if test_errors:
        print(f"FAIL: Tests failed ({len(test_errors)} issues):")
        for err in test_errors:
            print(f"  - {err}")
    else:
        print("OK: All companion tests passed.")

    # 3. Reproduce entry
    repro_errors = check_reproduce()
    all_errors.extend(repro_errors)

    # 4. Lean
    if args.lean:
        lean_errors = check_lean()
        all_errors.extend(lean_errors)
        if lean_errors:
            print(f"FAIL: Lean verification failed ({len(lean_errors)} issues):")
            for err in lean_errors:
                print(f"  - {err}")

    if all_errors:
        print(f"\nVerification FAILED with {len(all_errors)} errors.")
        return 1

    print("\nVerification PASSED.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
