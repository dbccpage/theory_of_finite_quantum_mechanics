"""Regular-file release custody; no mathematical or publication authority."""
from __future__ import annotations

import hashlib
import json
import os
import re
import stat
from pathlib import Path

CACHE_DIRS = {".git", ".venv", "venv", "__pycache__", ".pytest_cache",
              ".hypothesis", ".mypy_cache", ".ruff_cache", ".ipynb_checkpoints", ".lake"}
ROOT_OUTPUT_DIRS = {"dist", "build", "htmlcov"}
IGNORED_SUFFIXES = {".pyc", ".pyo", ".zip", ".sha256"}
ROOT_OUTPUT_FILES = {".coverage", "projection_obstruction.aux",
                     "projection_obstruction.log", "projection_obstruction.toc",
                     "paper_composition_manifest.json", "paper_composition_manifest.yaml",
                     "paper_composition_receipt.json"}


def regular(path: Path, root: Path | None = None) -> None:
    """Refuse links/reparse points on the file and every retained ancestor."""
    current = path
    while True:
        info = current.lstat()
        if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & 0x400:
            raise ValueError(f"non-regular release path (link/reparse): {current}")
        expected = stat.S_ISREG if current == path else stat.S_ISDIR
        if not expected(info.st_mode):
            raise ValueError(f"non-regular release path: {current}")
        if root is None or current == root:
            break
        if current.parent == current:
            raise ValueError(f"release path is outside root: {path}")
        current = current.parent


def traversal_error(error: OSError) -> None:
    raise error


def files(root: Path) -> list[Path]:
    result = []
    seen: dict[str, str] = {}
    for directory, directories, names in os.walk(root, onerror=traversal_error, followlinks=False):
        parent = Path(directory)
        retained = []
        for name in sorted(directories):
            child = parent / name
            if name in CACHE_DIRS or (parent == root and name in ROOT_OUTPUT_DIRS):
                continue
            info = child.lstat()
            if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & 0x400:
                raise ValueError(f"linked retained directory: {child}")
            retained.append(name)
        directories[:] = retained
        for name in sorted(names):
            child = parent / name
            if child.suffix in IGNORED_SUFFIXES or name == "lake-manifest.json":
                continue
            if parent == root and name in ROOT_OUTPUT_FILES:
                continue
            regular(child, root)
            for index in range(1, len(child.relative_to(root).parts) + 1):
                component = "/".join(child.relative_to(root).parts[:index])
                old = seen.setdefault(component.casefold(), component)
                if old != component:
                    raise ValueError(f"case-colliding release paths: {old}, {component}")
            result.append(child)
    return sorted(result, key=lambda path: path.relative_to(root).as_posix())


def snapshot(root: Path, *, include_manifest: bool = True) -> dict[str, str]:
    return {path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in files(root) if include_manifest or path.name != "SHA256SUMS"}


def unchanged(root: Path, initial: dict[str, str]) -> None:
    if snapshot(root) != initial:
        raise ValueError("release tree changed after initial verification")


def identity(root: Path) -> dict[str, str]:
    path = root / "release_identity.json"
    regular(path, root)
    value = json.loads(path.read_text(encoding="utf-8"))
    for key in ("manuscript_version", "code_version", "release_version"):
        if not isinstance(value.get(key), str) or re.fullmatch(r"\d+\.\d+\.\d+", value[key]) is None:
            raise ValueError(f"invalid release identity: {key}")
    project = re.search(r'^version\s*=\s*"([^"]+)"', (root / "pyproject.toml").read_text(encoding="utf-8"), re.M)
    if project is None or project.group(1) != value["code_version"]:
        raise ValueError("code version differs from pyproject.toml")
    if value["manuscript_version"] != value["release_version"]:
        raise ValueError("manuscript and release versions differ")
    manuscript = (root / "projection_obstruction.md").read_text(encoding="utf-8")
    try:
        from omega_engine_atlas.coda_atlas._kits.paper_header_schema import parse_paper_header
    except ImportError:
        if value["manuscript_version"] not in manuscript or value["release_date"] not in manuscript:
            raise ValueError("manuscript frontmatter differs from release identity")
    else:
        hdr, _body = parse_paper_header(manuscript, strict=False)
        if hdr.version.lstrip("v") != value["manuscript_version"].lstrip("v") or value["release_date"] not in hdr.date:
            raise ValueError("manuscript frontmatter differs from release identity")
    return value
