"""The deposit file set, checksums and the reproducible archive.

``deposit_files`` walks the package and drops build scratch. ``MANIFEST.sha256``
pins every deposit file except itself, ``SHA256SUMS`` and the archive; the
archive holds the manifest's files plus the manifest; ``SHA256SUMS`` pins
everything else, the archive included. Paths are sorted by their UTF-8 bytes.
AuthorityEffect: None.
"""

from __future__ import annotations

import hashlib
import zipfile
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1]
MANIFEST = "MANIFEST.sha256"
SUMS = "SHA256SUMS"
ARCHIVE = "oe_prime_algorithms_1.0.0_deposit.zip"
ARCHIVE_ROOT = "oe_prime_algorithms_1.0.0"
ZIP_TIME = (2026, 9, 26, 12, 0, 0)
SCRATCH_DIRS = {"__pycache__", ".pytest_cache", ".ruff_cache", ".ipynb_checkpoints", ".lake"}
SCRATCH_FILES = {".coverage"}


def _scratch(relative: Path) -> bool:
    parts = relative.parts
    if any(part in SCRATCH_DIRS for part in parts):
        return True
    if parts[:2] == ("lean4", "b"):
        return True
    return relative.name in SCRATCH_FILES


def deposit_files(root: Path = PACKAGE) -> list[str]:
    files = []
    for path in root.rglob("*"):
        if path.is_file():
            relative = path.relative_to(root)
            if not _scratch(relative):
                files.append(relative.as_posix())
    return sorted(files, key=lambda s: s.encode("utf-8"))


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def render_sums(root: Path, names: list[str]) -> str:
    return "".join(f"{sha256_of(root / name)}  {name}\n" for name in names)


def manifest_names(root: Path = PACKAGE) -> list[str]:
    return [n for n in deposit_files(root) if n not in (MANIFEST, SUMS, ARCHIVE)]


def build_archive(destination: Path, root: Path = PACKAGE) -> None:
    names = sorted(manifest_names(root) + [MANIFEST], key=lambda s: s.encode("utf-8"))
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name in names:
            info = zipfile.ZipInfo(f"{ARCHIVE_ROOT}/{name}", date_time=ZIP_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o644 << 16
            archive.writestr(info, (root / name).read_bytes())
