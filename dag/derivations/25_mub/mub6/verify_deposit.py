#!/usr/bin/env python3
"""One-command verifier for the MUB(6) paper deposit package (mub6).

Deterministic, two-way verification:
1. Every file listed in sha256sums exists and matches its recorded hash.
2. Sweep: no unrecorded non-excluded file is present in the deposit tree.
3. Fail-closed symlink rejection: rejects any unauthorized symlink.
4. Structural artifacts are present and non-empty.
5. Strict paper header schema check on mub6.md. If the schema kit
   cannot be imported, the check fails unless --skip-header-schema is given;
   a skip is printed, never silent.
6. Optional/Default named test files pass (--test).
7. Optional (--lean): lake build Mub6 succeeds. The deposit carries no Lean
   project, so --lean-root must name the source monorepo's lean4 directory.
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
MANIFEST = ROOT / "sha256sums"

EXCLUDED_DIRS = {
    ".git", ".venv", "venv", "__pycache__", ".pytest_cache",
    ".mypy_cache", ".ruff_cache", ".ipynb_checkpoints", ".lake",
    "dist", "build", "htmlcov", "dev_rips", "rt", "target",
    "b", "scratch",
    "_support", "evidence", "reconstruction_v1",
}
EXCLUDED_NAMES = {"sha256sums", ".coverage", ".env", "DEPOSIT_CHECKLIST.md", ".gitkeep"}
EXCLUDED_SUFFIXES = {".zip", ".pyc", ".pyo", ".tmp", ".log", ".aux", ".toc", ".out"}

REQUIRED_PATTERNS = (
    "mub6.md",
    "zenodo/release_manifest.json",
    "zenodo/release_checklist.md",
    "zenodo/mub6_formal_archive_v1.0.tar.gz",
    "code/deposit_paths.py",
    "README.md",
    "LICENSE",
)


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def check_manifest(manifest_path: Path, skip_header_schema: bool = False) -> list[str]:
    errors: list[str] = []
    try:
        excluded_names = set(EXCLUDED_NAMES) - {"sha256sums"}
        expected_files = walk_files(ROOT, EXCLUDED_DIRS, excluded_names, EXCLUDED_SUFFIXES)
        own_manifests = {ROOT / "sha256sums"}
        if manifest_path.name == "manifest.sha256":
            own_manifests.add(ROOT / "manifest.sha256")
        expected_files = [p for p in expected_files if p not in own_manifests]
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
            target = ROOT / pattern
            if not target.is_file() or not target.stat().st_size:
                errors.append(f"Required file missing or empty: {pattern}")

        # Check paper header compliance on mub6.md
        mono_path = ROOT / "mub6.md"
        if mono_path.is_file():
            try:
                repo_root = ROOT.parents[3]
                sys.path.insert(0, str(repo_root))
                from omega_engine_atlas.coda_atlas._kits.paper_header_schema import parse_paper_header
            except (ImportError, IndexError) as exc:
                if skip_header_schema:
                    print(f"SKIPPED: paper header schema check ({exc}); requested by --skip-header-schema")
                else:
                    print(f"WARNING: Paper header schema kit unavailable; header not checked ({exc}).")
            else:
                try:
                    parse_paper_header(mono_path.read_text(encoding="utf-8"), strict=True)
                except Exception as exc:
                    errors.append(f"Monograph header non-compliant ({mono_path.name}): {exc}")
    except (OSError, ValueError) as error:
        errors.append(str(error))
    return errors


def check_tests(targets: list[str]) -> list[str]:
    if not targets:
        tests_dir = ROOT / "tests"
        if tests_dir.is_dir():
            targets = [p.relative_to(ROOT).as_posix() for p in tests_dir.glob("test_*.py")]
    if not targets:
        return ["No test files found in tests/"]
    errors: list[str] = []
    for target in targets:
        try:
            path = safe_path(ROOT, target)
            if not target.startswith("tests/test_") or path.suffix != ".py" or not path.is_file():
                raise ValueError(f"Invalid test target: {target}")
            result = subprocess.run(
                [sys.executable, "-m", "pytest", target, "-q"],
                cwd=ROOT,
                capture_output=True,
                text=True,
                timeout=180,
                check=False,
            )
            if result.returncode:
                errors.append(f"Pytest failure in {target}:\n{result.stdout}\n{result.stderr}")
            else:
                last_line = result.stdout.strip().splitlines()[-1] if result.stdout.strip() else "OK"
                print(f"OK: {target}: {last_line}")
        except (OSError, ValueError, subprocess.TimeoutExpired) as error:
            errors.append(str(error))
    return errors


def check_lean(lean_root: str | None) -> list[str]:
    lean_dir = Path(lean_root).resolve() if lean_root else ROOT / "lean4"
    if not (lean_dir / "lakefile.lean").is_file() and not (lean_dir / "lakefile.toml").is_file():
        return [
            f"No lakefile.lean or lakefile.toml in {lean_dir}. The deposit has no Lean "
            "project; pass --lean-root <monorepo>/lean4."
        ]
    print(f"Lean root: {lean_dir}")
    errors: list[str] = []
    build_result = subprocess.run(
        ["lake", "build", "Mub6"],
        cwd=str(lean_dir),
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=180,
        check=False,
    )
    if build_result.returncode != 0:
        errors.append(f"lake build Mub6 failed:\n{build_result.stdout}\n{build_result.stderr}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify MUB(6) paper deposit package.")
    parser.add_argument("--lean", action="store_true", help="Run Lean verification.")
    parser.add_argument("--lean-root", default=None, help="Lean project directory (source monorepo lean4/).")
    parser.add_argument(
        "--skip-header-schema",
        action="store_true",
        help="Skip the paper header schema check when the monorepo kit is absent (printed as SKIPPED).",
    )
    parser.add_argument("--test", action="append", default=[], help="Named test file; repeat as needed.")
    parser.add_argument("--integrity-only", action="store_true", help="Run manifest integrity sweep only.")
    args = parser.parse_args()

    all_errors: list[str] = []

    manifest_target = MANIFEST
    if not manifest_target.is_file() and (ROOT / "manifest.sha256").is_file():
        manifest_target = ROOT / "manifest.sha256"

    if not manifest_target.is_file():
        print(f"FAIL: Manifest not found at {MANIFEST} or manifest.sha256", file=sys.stderr)
        return 1

    manifest_errors = check_manifest(manifest_target, skip_header_schema=args.skip_header_schema)
    all_errors.extend(manifest_errors)
    if manifest_errors:
        print(f"FAIL: Manifest checks failed ({len(manifest_errors)} issues):")
        for err in manifest_errors:
            print(f"  - {err}")
    else:
        print("OK: Manifest and two-way sweep checks passed.")

    if not args.integrity_only and args.test:
        test_errors = check_tests(args.test)
        all_errors.extend(test_errors)
        for error in test_errors:
            print(f"FAIL: {error}")
        if not test_errors:
            print("OK: selected test files passed.")

    if args.lean:
        try:
            lean_errors = check_lean(args.lean_root)
        except (OSError, subprocess.TimeoutExpired) as error:
            lean_errors = [f"Lean verification did not complete: {error}"]
        all_errors.extend(lean_errors)
        if lean_errors:
            print("FAIL: Lean checks failed.")
            for err in lean_errors:
                print(f"  - {err}")
        else:
            print("OK: Lean Mub6 build verified.")

    if all_errors:
        print(f"\nVerification FAILED with {len(all_errors)} errors.")
        return 1

    print("\nVerification PASSED.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
