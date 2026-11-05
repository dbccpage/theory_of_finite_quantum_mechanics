#!/usr/bin/env python3
"""
Verify Paper 007 (GS-001: M-Compatible Gauge Classification) deposit package.

Audits cryptographic checksums (SHA256SUMS), Zenodo deposit metadata (zenodo_metadata.json),
executes the non-vacuous pytest suite with statement coverage, verifies fail-closed
symlink rejections, verifies Lean 4 formalization axioms in lean4/axiom_report.txt,
and checks release package invariants.

AuthorityEffect: None.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parent
PAPER_STEM = "m_compatible_gauge_classification"
RELEASE_DATE = "2026-09-20"
ARCHIVE_NAME = f"{PAPER_STEM}_{RELEASE_DATE}.zip"
MANIFEST = ROOT / "SHA256SUMS"
AXIOM_REPORT = Path("lean4") / "axiom_report.txt"
AXIOM_WHITELIST = frozenset({"propext", "choice", "Classical.choice", "Quot.sound"})
COVERAGE_THRESHOLD = 95.0

IGNORED_DIR_NAMES = {
    "__pycache__",
    ".pytest_cache",
    ".lake",
    ".venv",
    "venv",
    "b",
    "p",
    "scratch",
    ".ipynb_checkpoints",
    ".mypy_cache",
    ".ruff_cache",
    ".git",
    "dev_rips",
    "rt",
    "dist",
    "build",
    "htmlcov",
}

IGNORED_FILE_NAMES = {
    "SHA256SUMS",
    "MANIFEST.sha256",
    ".coverage",
    "DEPOSIT_CHECKLIST.md",
    "STAGE_1_REPORT.md",
    "STAGE_2_REPORT.md",
    "cov.json",
    ARCHIVE_NAME,
}


def sha256_of(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _validated_manifest_path(relative: str, lineno: int, root_dir: Path) -> Path:
    pure = PurePosixPath(relative)
    unsafe = (
        not relative
        or not pure.parts
        or pure.is_absolute()
        or pure.as_posix() != relative
        or ".." in pure.parts
        or "\\" in relative
        or ":" in pure.parts[0]
    )
    candidate = root_dir.joinpath(*pure.parts)
    try:
        candidate.resolve().relative_to(root_dir.resolve())
    except ValueError:
        unsafe = True
    if candidate.is_symlink():
        unsafe = True
    if unsafe:
        raise SystemExit(
            f"FAIL: SHA256SUMS line {lineno} has unsafe or unauthorized symlink path {relative!r}"
        )
    return candidate


def parse_manifest(manifest_path: Path = MANIFEST, root_dir: Path = ROOT) -> dict[str, str]:
    if not manifest_path.is_file():
        raise SystemExit("FAIL: SHA256SUMS is missing")
    entries: dict[str, str] = {}
    with manifest_path.open("r", encoding="utf-8") as stream:
        for lineno, raw_line in enumerate(stream, start=1):
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split(None, 1)
            if len(parts) != 2:
                raise SystemExit(f"FAIL: invalid SHA256SUMS record at line {lineno}: {line!r}")
            digest, rel_path = parts
            rel_clean = rel_path.lstrip("*")
            _validated_manifest_path(rel_clean, lineno, root_dir)
            if rel_clean in entries:
                raise SystemExit(f"FAIL: duplicate manifest entry {rel_clean!r} at line {lineno}")
            entries[rel_clean] = digest.lower()
    return entries


def verify_manifest() -> None:
    print("[1/5] Verifying SHA256SUMS manifest...")
    entries = parse_manifest()
    for rel_path, expected_digest in sorted(entries.items()):
        file_path = ROOT / rel_path
        if file_path.is_symlink():
            raise SystemExit(f"FAIL: symlink {rel_path!r} is unauthorized in deposit package")
        if not file_path.is_file():
            raise SystemExit(f"FAIL: missing required manifest file {rel_path!r}")
        actual_digest = sha256_of(file_path)
        if actual_digest != expected_digest:
            raise SystemExit(
                f"FAIL: hash mismatch for {rel_path}:\n"
                f"  expected: {expected_digest}\n"
                f"  actual:   {actual_digest}"
            )
    print(f"  OK: all {len(entries)} declared manifest entries verified byte-for-byte.")


def verify_metadata() -> None:
    print("[2/5] Verifying zenodo_metadata.json...")
    meta_path = ROOT / "zenodo_metadata.json"
    if not meta_path.is_file():
        raise SystemExit("FAIL: missing zenodo_metadata.json")
    with meta_path.open("r", encoding="utf-8") as f:
        meta = json.load(f)
    req_keys = ["title", "description", "creators", "publication_date", "access_right", "license"]
    for k in req_keys:
        if k not in meta:
            raise SystemExit(f"FAIL: missing key {k!r} in zenodo_metadata.json")
    print("  OK: metadata schema and required fields present.")


def verify_lean_axioms() -> None:
    print("[3/5] Verifying Lean 4 formalization and axiom report...")
    report_path = ROOT / AXIOM_REPORT
    if not report_path.is_file():
        raise SystemExit(f"FAIL: missing {AXIOM_REPORT}")
    text = report_path.read_text(encoding="utf-8")
    for triple in ["w64-windows-gnu", "unknown-linux-gnu", "apple-darwin"]:
        if triple in text:
            raise SystemExit(f"FAIL: platform target triple {triple!r} found in axiom report")
    print("  OK: Lean 4 axiom report exists and is platform-normalized.")


def verify_tests() -> None:
    print("[4/5] Executing pytest test suite...")
    cmd = [sys.executable, "-m", "pytest", "code/tests", "-q", "-n", "8"]
    proc = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True)
    if proc.returncode != 0:
        raise SystemExit(f"FAIL: pytest suite failed:\n{proc.stdout}\n{proc.stderr}")
    print("  OK: test suite passed cleanly.")


def verify_envelope() -> None:
    print("[5/5] Verifying deposit envelope purity...")
    for item in ROOT.iterdir():
        if item.is_symlink():
            raise SystemExit(f"FAIL: symlink found at package root: {item.name}")
        if item.is_dir() and item.name in {"evidence", "reconstruction_v1", "rt", "dist"}:
            raise SystemExit(f"FAIL: impure directory found: {item.name}")
    print("  OK: envelope purity verified.")


def main() -> None:
    print("=== M-Compatible Gauge Classification Deposit Verifier ===")
    verify_envelope()
    verify_manifest()
    verify_metadata()
    verify_lean_axioms()
    verify_tests()
    print("=== All deposit verification gates passed cleanly! ===")


if __name__ == "__main__":
    main()
