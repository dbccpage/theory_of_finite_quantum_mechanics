"""Canonical payload inventory, non-circular manifests, and release archive.

MANIFEST.sha256 hashes the payload; SHA256SUMS hashes that same payload and
MANIFEST.sha256. Neither lists itself or a ZIP. The ZIP includes both manifests.
Archive compression can vary with zlib; member paths and bytes are the contract.
"""

from __future__ import annotations

import hashlib
import os
import re
import stat
import zipfile
from pathlib import Path, PurePosixPath

PACKAGE = Path(__file__).resolve().parents[1]
MANIFEST = "MANIFEST.sha256"
SUMS = "SHA256SUMS"
ARCHIVE = "discrete_deformation_calculus_2026-10-03.zip"
ARCHIVE_ROOT = "discrete_deformation_calculus_1.0.3"
ZIP_TIME = (2026, 10, 3, 12, 0, 0)
SCRATCH_DIRS = {"__pycache__", ".pytest_cache", ".ipynb_checkpoints", ".lake",
                ".git", ".venv", "venv", ".mypy_cache", ".ruff_cache", "htmlcov"}
SCRATCH_FILES = {".coverage"}
SCRATCH_PATHS = {"lean4/b", "code/ddc/ddc_core.egg-info"}


def canonical_path(name: str) -> str:
    path = PurePosixPath(name)
    if (not name or "\\" in name or ":" in name or path.is_absolute()
            or path.as_posix() != name or any(p in ("", ".", "..") for p in name.split("/"))
            or any(ord(c) < 32 for c in name)):
        raise ValueError(f"unsafe deposit path: {name!r}")
    return name


def regular(path: Path, *, directory: bool = False) -> None:
    info = path.lstat()
    if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & 0x400:
        raise ValueError(f"symlink or reparse point in deposit: {path.name}")
    expected = stat.S_ISDIR if directory else stat.S_ISREG
    if not expected(info.st_mode):
        raise ValueError(f"nonregular deposit entry: {path.name}")


def deposit_files(root: Path = PACKAGE) -> list[str]:
    regular(root, directory=True)
    files: list[str] = []
    for current, dirs, names in os.walk(root, followlinks=False):
        folder = Path(current)
        for name in dirs:
            regular(folder / name, directory=True)
        dirs[:] = [name for name in dirs if name not in SCRATCH_DIRS
                   and (folder / name).relative_to(root).as_posix() not in SCRATCH_PATHS]
        for name in names:
            path = folder / name
            regular(path)
            relative = canonical_path(path.relative_to(root).as_posix())
            if relative == ARCHIVE or name in SCRATCH_FILES or name.startswith(".coverage."):
                continue
            if path.suffix.lower() == ".zip":
                raise ValueError(f"unexpected ZIP archive in payload: {relative}")
            if len(str(path.absolute())) > 250:
                raise ValueError(f"deposit path exceeds 250 characters: {relative}")
            files.append(relative)
    return sorted(files, key=lambda s: s.encode("utf-8"))


def sha256_of(path: Path) -> str:
    regular(path)
    return hashlib.sha256(path.read_bytes()).hexdigest()


def render_sums(root: Path, names: list[str]) -> str:
    return "".join(f"{sha256_of(root / canonical_path(name))}  {name}\n" for name in names)


def parse_sums(path: Path) -> dict[str, str]:
    regular(path)
    entries: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  (.+)", line)
        if not match:
            raise ValueError(f"invalid checksum line in {path.name}")
        digest, name = match.groups()
        canonical_path(name)
        if name in entries:
            raise ValueError(f"duplicate checksum path: {name}")
        entries[name] = digest
    if list(entries) != sorted(entries, key=lambda s: s.encode("utf-8")):
        raise ValueError(f"checksum paths are not sorted in {path.name}")
    return entries


def manifest_names(root: Path = PACKAGE) -> list[str]:
    return [name for name in deposit_files(root) if name not in (MANIFEST, SUMS)]


def verify_hashes(root: Path = PACKAGE) -> list[str]:
    problems: list[str] = []
    try:
        payload = manifest_names(root)
        manifest = parse_sums(root / MANIFEST)
        sums = parse_sums(root / SUMS)
        expected = sorted(payload + [MANIFEST], key=lambda s: s.encode("utf-8"))
        if list(manifest) != payload or list(sums) != expected:
            return ["manifest file set differs from the payload inventory"]
        for listing, entries in ((MANIFEST, manifest), (SUMS, sums)):
            for name, digest in entries.items():
                if sha256_of(root / name) != digest:
                    problems.append(f"{listing}: {name} hash mismatch")
    except (ValueError, OSError, UnicodeError) as error:
        problems.append(str(error))
    return problems


def build_archive(destination: Path, root: Path = PACKAGE) -> None:
    problems = verify_hashes(root)
    if problems:
        raise ValueError("cannot archive an unverified payload: " + "; ".join(problems))
    names = deposit_files(root)
    if destination.exists():
        regular(destination)
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name in names:
            info = zipfile.ZipInfo(f"{ARCHIVE_ROOT}/{name}", date_time=ZIP_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = (stat.S_IFREG | 0o644) << 16
            archive.writestr(info, (root / name).read_bytes(), compresslevel=9)


def verify_archive(path: Path, root: Path = PACKAGE) -> list[str]:
    regular(path)
    expected = {f"{ARCHIVE_ROOT}/{name}": root / name for name in deposit_files(root)}
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        if len(names) != len(set(names)) or set(names) != set(expected):
            return ["archive member set differs from the verified payload"]
        for info in archive.infolist():
            canonical_path(info.filename)
            if info.create_system != 3 or not stat.S_ISREG(info.external_attr >> 16):
                return [f"nonregular archive member: {info.filename}"]
            if archive.read(info) != expected[info.filename].read_bytes():
                return [f"archive member differs from payload: {info.filename}"]
    return []
