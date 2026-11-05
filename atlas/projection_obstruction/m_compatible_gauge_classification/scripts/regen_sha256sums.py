#!/usr/bin/env python3
"""Deterministically (re)generate or verify the deposit checksum manifest.

A hash match certifies that the bytes on disk match the recorded manifest.
"""

from __future__ import annotations

import hashlib
import os
import sys
from pathlib import Path

MANIFEST_NAME = "SHA256SUMS"

EXCLUDED_DIRS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".ipynb_checkpoints",
    ".lake",
    "b",
    "p",
    "scratch",
    "dist",
    "build",
    "htmlcov",
    "dev_rips",
    "rt",
}

EXCLUDED_SUFFIXES = {".pyc", ".pyo", ".zip", ".sha256"}
EXCLUDED_NAMES = {".coverage", "DEPOSIT_CHECKLIST.md", "STAGE_1_REPORT.md", "STAGE_2_REPORT.md"}


def package_root() -> Path:
    return Path(__file__).resolve().parent.parent


def iter_files(root: Path) -> list[Path]:
    out: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDED_DIRS and not d.startswith(".")]
        dp = Path(dirpath)
        for f in filenames:
            p = dp / f
            if p.is_symlink():
                raise RuntimeError(f"unauthorized symlink detected: {p.relative_to(root)}")
            if not p.is_file():
                continue
            rel = p.relative_to(root)
            if any(part in EXCLUDED_DIRS for part in rel.parts):
                continue
            if p.suffix in EXCLUDED_SUFFIXES:
                continue
            if p.name in EXCLUDED_NAMES:
                continue
            if rel.as_posix() in (MANIFEST_NAME, "MANIFEST.sha256"):
                continue
            out.append(p)
    out.sort(key=lambda p: p.relative_to(root).as_posix())
    return out


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def render(root: Path) -> str:
    lines = [f"{sha256_of(p)}  {p.relative_to(root).as_posix()}" for p in iter_files(root)]
    return "\n".join(lines) + "\n"


def _parse(text: str) -> dict[str, str]:
    out = {}
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split(None, 1)
        if len(parts) == 2:
            out[parts[1].lstrip("*")] = parts[0]
    return out


def main(argv: list[str]) -> int:
    root = package_root()
    manifest = root / MANIFEST_NAME
    manifest_alt = root / "MANIFEST.sha256"
    fresh = render(root)
    if "--check" in argv:
        if not manifest.is_file():
            print(f"FAIL: {MANIFEST_NAME} is missing from {root}")
            return 1
        committed = manifest.read_bytes().decode("utf-8")
        if committed == fresh:
            n = fresh.count("\n")
            print(f"OK: {MANIFEST_NAME} matches byte-for-byte ({n} files, no unmanifested files)")
            return 0
        committed_map = _parse(committed)
        fresh_map = _parse(fresh)
        missing_from_disk = set(committed_map) - set(fresh_map)
        untracked_on_disk = set(fresh_map) - set(committed_map)
        hash_diff = {
            path
            for path in set(committed_map) & set(fresh_map)
            if committed_map[path] != fresh_map[path]
        }
        print("FAIL: manifest mismatch:")
        for path in sorted(missing_from_disk):
            print(f"  missing from disk: {path}")
        for path in sorted(untracked_on_disk):
            print(f"  untracked on disk: {path}")
        for path in sorted(hash_diff):
            print(f"  hash mismatch:     {path}")
        return 1

    manifest.write_bytes(fresh.encode("utf-8"))
    manifest_alt.write_bytes(fresh.encode("utf-8"))
    n = fresh.count("\n")
    print(f"WROTE: {manifest} and {manifest_alt} ({n} files)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
