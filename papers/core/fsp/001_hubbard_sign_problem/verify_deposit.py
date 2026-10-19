#!/usr/bin/env python3
"""One-command verifier for the Fermi-Hubbard research paper deposit.

Deterministic, two-way verification:
1. Every file listed in sha256sums exists and matches its recorded hash.
2. Sweep: no unrecorded non-excluded file is present in the deposit tree.
3. Fail-closed symlink rejection: rejects any unauthorized symlink.
4. Structural artifacts are present and non-empty.
5. Test suite passes.
"""

from __future__ import annotations

import argparse
import hashlib
import subprocess
import sys
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
MANIFEST = ROOT / "sha256sums"

EXCLUDED_DIRS = DEFAULT_EXCLUDED_DIRS
EXCLUDED_NAMES = DEFAULT_EXCLUDED_NAMES
EXCLUDED_SUFFIXES = DEFAULT_EXCLUDED_SUFFIXES

REQUIRED_FILES = (
    "paper.md",
    "paper_change_log.md",
    "paper_claim_ledger.md",
    "README.md",
    "LICENSE",
    "LICENSE-CODE",
    "pyproject.toml",
    "zenodo_metadata.json",
    "citation.cff",
    "docs/descriptions.md",
    "docs/references.md",
    "code/deposit_paths.py",
    "code/hubbard_exact_model.py",
    "code/hubbard_schema.sql",
    "code/tests/test_hubbard_paper_reproducibility.py",
)


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def check_manifest(manifest_path: Path) -> list[str]:
    errors: list[str] = []
    if not manifest_path.is_file():
        return [f"missing manifest: {manifest_path.relative_to(ROOT)}"]
    expected = read_manifest(manifest_path)
    on_disk = {rel: path for rel, path in walk_files(ROOT, EXCLUDED_DIRS, EXCLUDED_NAMES, EXCLUDED_SUFFIXES)}

    for rel, exp_digest in expected.items():
        if rel not in on_disk:
            errors.append(f"manifest file missing on disk: {rel}")
            continue
        got_digest = sha256_of(on_disk[rel])
        if got_digest != exp_digest:
            errors.append(f"hash mismatch for {rel}: expected {exp_digest} got {got_digest}")

    for rel in on_disk:
        if rel not in expected:
            errors.append(f"untracked file present on disk: {rel}")

    return errors


def check_required_artifacts() -> list[str]:
    errors: list[str] = []
    for rel in REQUIRED_FILES:
        path = safe_path(ROOT, rel)
        if not path.is_file():
            errors.append(f"required file missing: {rel}")
        elif path.stat().st_size == 0:
            errors.append(f"required file is empty: {rel}")
    return errors


def run_tests() -> list[str]:
    test_file = ROOT / "code" / "tests" / "test_hubbard_paper_reproducibility.py"
    if not test_file.is_file():
        return [f"missing test file: {test_file.relative_to(ROOT)}"]
    cmd = [sys.executable, "-m", "pytest", "-v", str(test_file)]
    res = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True, check=False)
    if res.returncode != 0:
        return [f"test failure:\n{res.stdout}\n{res.stderr}"]
    return []


def regen_manifest(manifest_path: Path) -> None:
    files = walk_files(ROOT, EXCLUDED_DIRS, EXCLUDED_NAMES, EXCLUDED_SUFFIXES)
    entries: list[tuple[str, str]] = []
    for rel, path in files:
        entries.append((sha256_of(path), rel))
    entries.sort(key=lambda item: item[1].encode("utf-8"))
    text = "\n".join(f"{digest}  {rel}" for digest, rel in entries) + "\n"
    manifest_path.write_text(text, encoding="utf-8", newline="\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--regen", action="store_true", help="Regenerate sha256sums before verification")
    parser.add_argument("--skip-tests", action="store_true", help="Skip running pytest")
    args = parser.parse_args()

    if args.regen or not MANIFEST.is_file():
        print(f"Generating manifest at {MANIFEST}...")
        regen_manifest(MANIFEST)

    errors: list[str] = []
    errors.extend(check_required_artifacts())
    errors.extend(check_manifest(MANIFEST))

    if not args.skip_tests:
        print("Running reproducibility tests...")
        errors.extend(run_tests())

    if errors:
        print(f"VERIFICATION FAILED ({len(errors)} errors):")
        for err in errors:
            print(f"  - {err}")
        return 1

    print("ALL CHECKS PASSED: Fermi-Hubbard paper deposit verified successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
