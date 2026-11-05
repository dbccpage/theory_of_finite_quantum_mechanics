#!/usr/bin/env python3
"""Deterministically (re)generate or verify the PO-035 deposit checksum manifest."""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

from release_custody import files, regular

MANIFEST_NAME = "SHA256SUMS"


def package_root() -> Path:
    return Path(__file__).resolve().parent.parent


def iter_files(root: Path) -> list[Path]:
    return [path for path in files(root) if path.relative_to(root).as_posix() != MANIFEST_NAME]


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def render(root: Path) -> str:
    lines = [f"{sha256_of(p)}  {p.relative_to(root).as_posix()}" for p in iter_files(root)]
    return "\n".join(lines) + "\n"


def main(argv: list[str]) -> int:
    root = package_root()
    manifest = root / MANIFEST_NAME
    if manifest.exists() or manifest.is_symlink():
        regular(manifest, root)
    fresh = render(root)
    if "--check" in argv:
        if not manifest.is_file():
            print(f"FAIL: {MANIFEST_NAME} is missing from {root}")
            return 1
        committed = manifest.read_bytes().decode("utf-8")
        if committed == fresh:
            n = fresh.count("\n")
            print(f"OK: {MANIFEST_NAME} matches the tree ({n} files)")
            return 0
        committed_map = _parse(committed)
        fresh_map = _parse(fresh)
        for path in sorted(set(committed_map) | set(fresh_map)):
            a, b = committed_map.get(path), fresh_map.get(path)
            if a is None:
                print(f"FAIL: not listed in {MANIFEST_NAME}: {path}")
            elif b is None:
                print(f"FAIL: listed but absent from tree: {path}")
            elif a != b:
                print(f"FAIL: hash mismatch: {path}")
            return 1
    manifest.write_bytes(fresh.encode("utf-8"))
    print(f"wrote {MANIFEST_NAME}: {fresh.count(chr(10))} files")
    return 0


def _parse(text: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for line in text.splitlines():
        line = line.rstrip("\r")
        if not line.strip():
            continue
        digest, _, path = line.partition("  ")
        out[path] = digest
    return out


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
