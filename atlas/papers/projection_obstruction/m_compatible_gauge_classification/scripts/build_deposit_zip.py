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
RELEASE_DATE = "2026-09-20"
ARCHIVE_NAME = f"m_compatible_gauge_classification_{RELEASE_DATE}.zip"
ZIP_DATE = (2026, 9, 20, 12, 0, 0)


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
            raise ValueError(f"SHA256SUMS line {lineno}: invalid format: {line!r}")
        digest, rel = parts[0].lower(), parts[1].lstrip("*")
        _validated_manifest_path(rel, lineno, root_dir)
        if rel in seen:
            raise ValueError(f"SHA256SUMS line {lineno}: duplicate entry {rel!r}")
        seen.add(rel)
        entries.append((digest, rel))
    return entries


def build_archive(
    entries: list[tuple[str, str]],
    dest: Path,
    root_dir: Path = ROOT,
    zip_stem: str = "m_compatible_gauge_classification",
) -> None:
    temp_zip = dest.with_suffix(".tmp.zip")
    if temp_zip.exists():
        temp_zip.unlink()

    with zipfile.ZipFile(temp_zip, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for expected_digest, rel in entries:
            src = root_dir / rel
            if not src.is_file():
                raise FileNotFoundError(f"Pinned file is missing from disk: {rel}")
            actual_digest = sha256_of(src)
            if actual_digest != expected_digest:
                raise ValueError(
                    f"Digest mismatch for {rel}: disk={actual_digest} manifest={expected_digest}"
                )
            archive_path = f"{zip_stem}/{rel}"
            info = zipfile.ZipInfo(archive_path, date_time=ZIP_DATE)
            info.external_attr = 0o100644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3  # Unix
            zf.writestr(info, src.read_bytes())

        # Also place the manifest inside the archive
        manifest_path = f"{zip_stem}/SHA256SUMS"
        info = zipfile.ZipInfo(manifest_path, date_time=ZIP_DATE)
        info.external_attr = 0o100644 << 16
        info.compress_type = zipfile.ZIP_DEFLATED
        info.create_system = 3
        zf.writestr(info, (root_dir / "SHA256SUMS").read_bytes())

        # Also place verify_deposit.py if present and not already in entries
        vd_src = root_dir / "verify_deposit.py"
        if vd_src.is_file() and not any(rel == "verify_deposit.py" for _, rel in entries):
            info = zipfile.ZipInfo(f"{zip_stem}/verify_deposit.py", date_time=ZIP_DATE)
            info.external_attr = 0o100755 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            zf.writestr(info, vd_src.read_bytes())

    temp_zip.replace(dest)


def main() -> int:
    entries = parse_manifest()
    archive_path = ROOT / ARCHIVE_NAME
    build_archive(entries, archive_path)
    print(f"BUILT: {archive_path} ({archive_path.stat().st_size} bytes, {len(entries)} files)")
    print(f"SHA256: {sha256_of(archive_path)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
