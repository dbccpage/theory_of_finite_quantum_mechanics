"""Fail-closed paths shared by deposit verification, manifests and ZIP assembly."""
from __future__ import annotations

import hashlib
import os
import re
import stat
from pathlib import Path, PurePosixPath


def _link(path: Path) -> bool:
    return path.is_symlink() or bool(getattr(path, "is_junction", lambda: False)())


def safe_path(root: Path, relative: str) -> Path:
    pure = PurePosixPath(relative)
    reserved = {"CON", "PRN", "AUX", "NUL", *(f"COM{i}" for i in range(1, 10)),
                *(f"LPT{i}" for i in range(1, 10))}
    if (not relative or not pure.parts or pure.is_absolute() or pure.as_posix() != relative
            or ".." in pure.parts or "\\" in relative or ":" in relative
            or any(ord(c) < 32 for c in relative)
            or any(p.rstrip(" .") != p or p.split(".")[0].upper() in reserved for p in pure.parts)):
        raise ValueError(f"unsafe deposit path: {relative!r}")
    root = root.absolute()
    for ancestor in (root, *root.parents):
        if _link(ancestor):
            raise ValueError(f"symlink or junction in deposit root: {ancestor}")
    path = root
    for part in pure.parts:
        path = path / part
        if _link(path):
            raise ValueError(f"symlink or junction in deposit path: {relative}")
    if not path.resolve().is_relative_to(root.resolve()):
        raise ValueError(f"deposit path escapes root: {relative}")
    return path


def walk_files(root: Path, excluded_dirs: set[str], excluded_names: set[str],
               excluded_suffixes: set[str]) -> list[Path]:
    safe_path(root, "__root_check__")
    files: list[Path] = []
    seen_files: dict[str, str] = {}
    seen_dirs: dict[str, str] = {}
    for directory, dirs, names in os.walk(root, followlinks=False):
        parent = Path(directory)
        # Check every immediate directory before pruning even excluded caches.
        for name in (*dirs, *names):
            if _link(parent / name):
                raise ValueError(f"symlink or junction in deposit: {parent / name}")
        dirs[:] = [name for name in dirs if name not in excluded_dirs
                   and not name.startswith(".") and not name.endswith(".egg-info")]

        for d in dirs:
            dir_path = parent / d
            dir_rel = dir_path.relative_to(root).as_posix()
            d_key = dir_rel.casefold()
            if d_key in seen_files:
                raise ValueError(f"case-colliding deposit path: directory {dir_rel} conflicts with file {seen_files[d_key]}")
            if d_key in seen_dirs and seen_dirs[d_key] != dir_rel:
                raise ValueError(f"case-colliding deposit directory component: {dir_rel} vs {seen_dirs[d_key]}")
            seen_dirs[d_key] = dir_rel

        for name in names:
            path = parent / name
            if name in excluded_names or path.suffix in excluded_suffixes:
                continue
            relative = path.relative_to(root).as_posix()
            safe_path(root, relative)
            file_key = relative.casefold()
            if file_key in seen_files:
                raise ValueError(f"case-colliding deposit path: {relative}")
            if file_key in seen_dirs:
                raise ValueError(f"case-colliding deposit path: {relative} conflicts with directory {seen_dirs[file_key]}")

            pure = PurePosixPath(relative)
            for i in range(1, len(pure.parts)):
                dir_comp = PurePosixPath(*pure.parts[:i]).as_posix()
                comp_key = dir_comp.casefold()
                if comp_key in seen_files:
                    raise ValueError(f"case-colliding deposit path: directory component {dir_comp} conflicts with file {seen_files[comp_key]}")
                if comp_key in seen_dirs and seen_dirs[comp_key] != dir_comp:
                    raise ValueError(f"case-colliding deposit directory component: {dir_comp} vs {seen_dirs[comp_key]}")
                seen_dirs[comp_key] = dir_comp

            if not stat.S_ISREG(path.stat().st_mode):
                raise ValueError(f"nonregular deposit file: {relative}")

            seen_files[file_key] = relative
            files.append(path)
    return sorted(files, key=lambda p: p.relative_to(root).as_posix())


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_manifest(root: Path, manifest: Path) -> list[tuple[str, str]]:
    safe_path(root, manifest.absolute().relative_to(root.absolute()).as_posix())
    entries: list[tuple[str, str]] = []
    seen_files: dict[str, str] = {}
    seen_dirs: dict[str, str] = {}
    for number, line in enumerate(manifest.read_text(encoding="utf-8").splitlines(), 1):
        if not line or line.startswith("#"):
            continue
        match = re.fullmatch(r"([a-fA-F0-9]{64})  (.+)", line)
        if match is None:
            raise ValueError(f"malformed manifest line {number}")
        digest, relative = match.groups()
        safe_path(root, relative)
        file_key = relative.casefold()
        if file_key in seen_files:
            raise ValueError(f"duplicate or case-colliding manifest path: {relative}")
        if file_key in seen_dirs:
            raise ValueError(f"case-colliding manifest path: {relative} conflicts with directory {seen_dirs[file_key]}")
        if relative == manifest.name or relative.lower().endswith(".zip"):
            raise ValueError(f"circular manifest entry: {relative}")

        pure = PurePosixPath(relative)
        for i in range(1, len(pure.parts)):
            dir_comp = PurePosixPath(*pure.parts[:i]).as_posix()
            comp_key = dir_comp.casefold()
            if comp_key in seen_files:
                raise ValueError(f"case-colliding manifest path: directory component {dir_comp} conflicts with file {seen_files[comp_key]}")
            if comp_key in seen_dirs and seen_dirs[comp_key] != dir_comp:
                raise ValueError(f"case-colliding manifest directory component: {dir_comp} vs {seen_dirs[comp_key]}")
            seen_dirs[comp_key] = dir_comp

        seen_files[file_key] = relative
        entries.append((relative, digest.lower()))
    return entries
