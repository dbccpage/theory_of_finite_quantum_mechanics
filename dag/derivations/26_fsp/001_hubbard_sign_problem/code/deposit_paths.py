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
    reserved = {
        "CON",
        "PRN",
        "AUX",
        "NUL",
        *(f"COM{i}" for i in range(1, 10)),
        *(f"LPT{i}" for i in range(1, 10)),
    }
    if (
        not relative
        or not pure.parts
        or pure.is_absolute()
        or pure.as_posix() != relative
        or ".." in pure.parts
        or "\\" in relative
        or ":" in relative
        or any(ord(c) < 32 for c in relative)
        or any(p.rstrip(" .") != p or p.split(".")[0].upper() in reserved for p in pure.parts)
    ):
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


DEFAULT_EXCLUDED_DIRS: set[str] = {
    ".git", ".venv", "venv", "__pycache__", ".pytest_cache",
    ".mypy_cache", ".ruff_cache", ".ipynb_checkpoints", ".lake",
    "dist", "build", "htmlcov", "dev_rips", "rt", "target",
    "b", "scratch",
    "_support", "evidence", "reconstruction_v1",
}
DEFAULT_EXCLUDED_NAMES: set[str] = {
    "sha256sums", ".coverage", ".env", "DEPOSIT_CHECKLIST.md", ".gitkeep",
    "desktop.ini", "Thumbs.db", ".DS_Store",
}
DEFAULT_EXCLUDED_SUFFIXES: set[str] = {
    ".pyc", ".pyo", ".pyd", ".swp", ".swo", "~", ".bak", ".tmp",
}


def read_manifest(manifest_path: Path) -> dict[str, str]:
    if not manifest_path.is_file():
        raise FileNotFoundError(f"missing manifest: {manifest_path}")
    expected: dict[str, str] = {}
    for lineno, raw in enumerate(manifest_path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        parts = re.split(r"\s+", line, maxsplit=1)
        if len(parts) != 2:
            raise ValueError(f"malformed manifest line {lineno}: {raw!r}")
        digest, rel = parts
        rel = rel.lstrip("*")
        if not re.fullmatch(r"[0-9a-f]{64}", digest):
            raise ValueError(f"malformed digest on line {lineno}: {digest!r}")
        if rel in expected:
            raise ValueError(f"duplicate path in manifest line {lineno}: {rel!r}")
        expected[rel] = digest
    return expected


def walk_files(
    root: Path,
    excluded_dirs: set[str] | None = None,
    excluded_names: set[str] | None = None,
    excluded_suffixes: set[str] | None = None,
) -> list[tuple[str, Path]]:
    dirs = DEFAULT_EXCLUDED_DIRS if excluded_dirs is None else excluded_dirs
    names = DEFAULT_EXCLUDED_NAMES if excluded_names is None else excluded_names
    suffixes = DEFAULT_EXCLUDED_SUFFIXES if excluded_suffixes is None else excluded_suffixes

    out: list[tuple[str, Path]] = []
    root = root.resolve()

    def _walk(curr: Path, rel_parts: tuple[str, ...]) -> None:
        for entry in sorted(os.scandir(curr), key=lambda e: e.name):
            name = entry.name
            if name in names:
                continue
            path = Path(entry.path)
            if _link(path):
                raise ValueError(f"symlink or junction encountered in deposit: {path}")
            if entry.is_dir(follow_symlinks=False):
                if name in dirs:
                    continue
                _walk(path, rel_parts + (name,))
            elif entry.is_file(follow_symlinks=False):
                if any(name.endswith(s) for s in suffixes):
                    continue
                rel = "/".join(rel_parts + (name,))
                safe_path(root, rel)
                out.append((rel, path))

    _walk(root, ())
    return out
