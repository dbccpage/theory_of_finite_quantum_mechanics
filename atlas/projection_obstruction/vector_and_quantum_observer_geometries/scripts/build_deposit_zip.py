#!/usr/bin/env python3
"""Build the publishable archive from the pinned set, and nothing else.

The deposit IS the SHA256SUMS-pinned file list.
"""

from __future__ import annotations

import hashlib
import re
import sys
import zipfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "SHA256SUMS"
RELEASE_DATE = "2026-09-21"
ARCHIVE_NAME = f"vector_and_quantum_observer_geometries_{RELEASE_DATE}.zip"
ZIP_DATE = (2026, 9, 21, 12, 0, 0)


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


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
        or ".lake" in pure.parts
        or "b" in pure.parts
        or "p" in pure.parts
    )
    candidate = root_dir.joinpath(*pure.parts)
    try:
        candidate.resolve().relative_to(root_dir.resolve())
    except ValueError:
        unsafe = True
    if candidate.is_symlink():
        unsafe = True
    if unsafe:
        raise ValueError(
            f"SHA256SUMS line {lineno} has unsafe path {relative!r}"
        )
    return candidate


def parse_manifest(
    manifest_path: Path = MANIFEST, root_dir: Path = ROOT
) -> list[tuple[str, str]]:
    if not manifest_path.is_file():
        raise ValueError("SHA256SUMS is missing; run scripts/regen_sha256sums.py first")
    entries: list[tuple[str, str]] = []
    seen: set[str] = set()
    for lineno, raw in enumerate(manifest_path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line:
            continue
        parts = line.split(None, 1)
        if len(parts) != 2 or re.fullmatch(r"[0-9a-fA-F]{64}", parts[0]) is None:
            raise ValueError(f"SHA256SUMS line {lineno} is malformed: {raw!r}")
        relative = parts[1].strip().lstrip("*")
        _validated_manifest_path(relative, lineno, root_dir)
        key = relative.casefold()
        if key in seen:
            raise ValueError(f"SHA256SUMS lists {relative} more than once")
        seen.add(key)
        entries.append((relative, parts[0].lower()))
    return entries


def main(argv: list[str]) -> int:
    try:
        entries = parse_manifest()
    except ValueError as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1

    out_path = ROOT / ARCHIVE_NAME
    if "--out" in argv:
        idx = argv.index("--out")
        if idx + 1 < len(argv):
            out_path = Path(argv[idx + 1]).resolve()

    mismatches: list[str] = []
    for relative, expected in entries:
        path = ROOT / relative
        if not path.is_file():
            mismatches.append(f"missing: {relative}")
            continue
        actual = sha256_of(path)
        if actual != expected:
            mismatches.append(f"hash mismatch: {relative} (expected {expected}, got {actual})")

    if mismatches:
        print("FAIL: manifest does not match tree; re-run scripts/regen_sha256sums.py", file=sys.stderr)
        for m in mismatches:
            print(f"  {m}", file=sys.stderr)
        return 1

    manifest_bytes = MANIFEST.read_bytes()
    manifest_alt = ROOT / "MANIFEST.sha256"
    manifest_alt_bytes = manifest_alt.read_bytes() if manifest_alt.exists() else None

    with zipfile.ZipFile(out_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        info_m = zipfile.ZipInfo(filename="SHA256SUMS", date_time=ZIP_DATE)
        info_m.external_attr = 0o644 << 16
        archive.writestr(info_m, manifest_bytes)

        if manifest_alt_bytes:
            info_alt = zipfile.ZipInfo(filename="MANIFEST.sha256", date_time=ZIP_DATE)
            info_alt.external_attr = 0o644 << 16
            archive.writestr(info_alt, manifest_alt_bytes)

        for relative, _ in entries:
            path = ROOT / relative
            data = path.read_bytes()
            info = zipfile.ZipInfo(filename=relative, date_time=ZIP_DATE)
            info.external_attr = 0o644 << 16
            archive.writestr(info, data)

    print(f"Wrote {len(entries) + (2 if manifest_alt_bytes else 1)} members to {out_path.name} ({out_path.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
