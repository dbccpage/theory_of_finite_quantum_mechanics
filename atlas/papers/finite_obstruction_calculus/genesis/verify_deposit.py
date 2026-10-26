#!/usr/bin/env python3
"""One-command verifier for the research paper deposit.

Deterministic, two-way verification:
1. Every file listed in SHA256SUMS exists and matches its recorded hash.
2. Sweep: no unrecorded non-excluded file is present in the deposit tree.
3. Fail-closed symlink rejection: rejects any unauthorized symlink.
4. Structural artifacts are present and non-empty.
5. All local test files pass (or the --test selection).
6. Native Rust/Python replay and Lean wire/search replay pass.
7. Optional (--lean): additionally compile the full theorem/axiom census.
8. Optional (--archive): the selected outer ZIP matches the canonical release.
9. Repeat integrity checks after mutable test/native/Lean subprocesses.
Use --integrity-only for a tree/manifest/archive check without runtime replay.
"""

from __future__ import annotations

import argparse
import hashlib
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "code"))
from deposit_paths import read_manifest, safe_path, walk_files

from tools.rebuild_release import validate

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
EXCLUDED_SUFFIXES = {".zip", ".pyc", ".pyo", ".tmp", ".log"}

REQUIRED_PATTERNS = (
    "*_monograph.md",
    "*_change_log.md",
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

        # Check required structural files/patterns
        for pattern in REQUIRED_PATTERNS:
            if "/" in pattern:
                target = ROOT / pattern
                if not target.is_file() or not target.stat().st_size:
                    errors.append(f"Required file missing or empty: {pattern}")
            else:
                matches = list(ROOT.glob(pattern))
                if pattern == "*_monograph.md" and not matches:
                    matches = [
                        p for p in ROOT.glob("*.md")
                        if p.name.lower() not in ("readme.md", "review_scope.md")
                        and not p.name.endswith(("_change_log.md", "_claim_ledger.md", "_supplement.md", "supplement.md"))
                    ]
                if pattern == "*_change_log.md" and not matches:
                    matches = list(ROOT.glob("paper_change_log.md"))
                if not matches or not any(m.stat().st_size > 0 for m in matches):
                    errors.append(f"Required file pattern missing or empty: {pattern}")
    except (OSError, ValueError) as error:
        errors.append(str(error))
    return errors


def check_tests(targets: list[str]) -> list[str]:
    if not targets:
        tests_dir = ROOT / "code" / "tests"
        if tests_dir.is_dir():
            targets = [p.relative_to(ROOT).as_posix() for p in tests_dir.glob("test_*.py")]
    if not targets:
        return ["No test files found in code/tests/"]
    errors: list[str] = []
    for target in targets:
        try:
            path = safe_path(ROOT, target)
            if not target.startswith("code/tests/test_") or path.suffix != ".py" or not path.is_file():
                raise ValueError(f"Invalid test target: {target}")
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
        except (OSError, ValueError, subprocess.TimeoutExpired) as error:
            errors.append(str(error))
    return errors


def check_lean() -> list[str]:
    """Compile and rediscover the entire population with per-module axiom policy."""
    run = subprocess.run(
        [sys.executable, str(ROOT / "tools/census.py")], cwd=ROOT,
        capture_output=True, text=True, encoding="utf-8", timeout=300, check=False,
    )
    if run.returncode:
        return [run.stdout + run.stderr]
    print(run.stdout.strip())
    return []



def check_release(selected_archive: Path | None) -> list[str]:
    return check_manifest(ROOT / "SHA256SUMS") + validate(
        ROOT, selected_archive, check_archive=selected_archive is not None
    )


def controls_snapshot(selected_archive: Path | None) -> dict[str, str]:
    paths = [ROOT / "MANIFEST.sha256", ROOT / "SHA256SUMS"]
    if selected_archive is not None:
        paths.append(selected_archive)
    return {str(path): sha256_of(path) for path in paths}


def check_native() -> list[str]:
    try:
        native = subprocess.run(
            [sys.executable, str(ROOT / "code/verify_package.py")], cwd=ROOT,
            capture_output=True, text=True, timeout=180, check=False,
        )
        if native.returncode:
            return ["Native mathematical replay failed: " + native.stdout + native.stderr]
    except (OSError, subprocess.TimeoutExpired) as error:
        return [f"Native mathematical replay did not complete: {error}"]
    print(native.stdout.strip())
    return []


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify paper deposit package.")
    parser.add_argument("--lean", action="store_true", help="Add the full Lean theorem/axiom census; normal native replay already requires Lean.")
    parser.add_argument("--archive", type=Path, help="Exact dated outer ZIP to compare with this package tree.")
    parser.add_argument("--integrity-only", action="store_true", help="Check tree, manifests and selected ZIP without tests or native replay.")
    parser.add_argument("--test", action="append", default=[], help="Named test file; repeat as needed.")
    args = parser.parse_args()
    if args.integrity_only and (args.lean or args.test):
        parser.error("--integrity-only cannot be combined with --lean or --test")
    selected_archive = args.archive.absolute() if args.archive is not None else None

    all_errors: list[str] = []

    manifest_errors = check_release(selected_archive)
    all_errors.extend(manifest_errors)
    if manifest_errors:
        print(f"FAIL: Integrity checks failed ({len(manifest_errors)} issues):")
        for err in manifest_errors:
            print(f"  - {err}")
    else:
        print("OK: Both manifests and two-way tree sweep passed.")
        if selected_archive is not None:
            print(f"OK: Selected archive matches canonical release: {selected_archive}")

    if manifest_errors:
        print(f"\nVerification FAILED with {len(all_errors)} errors.")
        return 1
    initial_controls = controls_snapshot(selected_archive)
    if args.integrity_only:
        print(f"Scope: integrity only; selected archive={selected_archive is not None}; no runtime replay.")
        print("\nVerification PASSED.")
        return 0

    def recheck_after_subprocess() -> None:
        errors = check_release(selected_archive)
        if not errors and controls_snapshot(selected_archive) != initial_controls:
            errors.append("Release controls changed during requested checks")
        all_errors.extend(errors)
        for error in errors:
            print(f"FAIL: {error}")

    targets = args.test or [
        path.relative_to(ROOT).as_posix()
        for path in sorted((ROOT / "code/tests").glob("test_*.py"))
    ]
    test_errors: list[str] = []
    for selection in [[target] for target in targets] or [[]]:
        test_errors.extend(check_tests(selection))
        recheck_after_subprocess()
    all_errors.extend(test_errors)
    for error in test_errors:
        print(f"FAIL: {error}")
    if not test_errors:
        print("OK: custody and mathematical tests passed.")

    native_errors = check_native()
    recheck_after_subprocess()
    all_errors.extend(native_errors)
    for error in native_errors:
        print(f"FAIL: {error}")
    if not native_errors:
        print("OK: native Rust/Python and Lean wire/search replay passed.")

    if args.lean:
        try:
            lean_errors = check_lean()
        except (OSError, subprocess.TimeoutExpired) as error:
            lean_errors = [f"Lean verification did not complete: {error}"]
        recheck_after_subprocess()
        all_errors.extend(lean_errors)
        if lean_errors:
            print("FAIL: Lean checks failed.")
            for err in lean_errors:
                print(f"  - {err}")
        else:
            print("OK: Lean proofs and axiom census verified.")

    final_errors = check_release(selected_archive)
    all_errors.extend(final_errors)
    for error in final_errors:
        print(f"FAIL: {error}")
    if not final_errors and controls_snapshot(selected_archive) != initial_controls:
        all_errors.append("Release controls changed during requested checks")
        print("FAIL: Release controls changed during requested checks")
    elif not final_errors:
        print("OK: Release bytes unchanged after requested checks.")

    if all_errors:
        print(f"\nVerification FAILED with {len(all_errors)} errors.")
        return 1

    print(f"Scope: tests and native replay; full Lean census={args.lean}; selected archive={selected_archive is not None}.")
    print("\nVerification PASSED.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
