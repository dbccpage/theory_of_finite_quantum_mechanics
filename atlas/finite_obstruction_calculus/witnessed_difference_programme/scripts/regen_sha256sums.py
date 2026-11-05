#!/usr/bin/env python3
"""Deterministically (re)generate or verify the deposit checksum manifest.

AuthorityEffect: None. A hash match is not a proof of any mathematical claim;
it certifies only that the bytes on disk are the bytes that were hashed.
"""

from __future__ import annotations

import hashlib
import os
import stat
import sys
from pathlib import Path

MANIFEST_NAME = "MANIFEST.sha256"
SUMS_NAME = "SHA256SUMS"

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
    ".hypothesis",
    "dist",
    "build",
    "htmlcov",
    "target",
    "node_modules",
    # Lake writes object code, IR and traces into the package's `buildDir`,
    # which `lean4/lakefile.lean` sets to "b". Those are build outputs, not
    # deposit members. `scratch/` is pytest's tmp area.
    "b",
    "scratch",
}
ROOT_SCOPED_DIRS = {"b", "build", "dist", "node_modules", "target"}
EXCLUDED_DIR_PATHS = (
    ROOT_SCOPED_DIRS
    | {f"lean4/{name}" for name in ROOT_SCOPED_DIRS}
    | {f"code/rust/{name}" for name in ROOT_SCOPED_DIRS}
    | {"code/coda_application/build", "code/coda_application/dist"}
)
EXCLUDED_SUFFIXES = {
    ".pyc",
    ".pyo",
    ".tmp",
    ".zip",
    ".aux",
    ".toc",
    ".out",
    ".synctex.gz",
    ".log",
}
EXCLUDED_NAMES = {
    ".coverage",
    "coverage.json",
    "coverage.xml",
    "mutation-results.xml",
    ".DS_Store",
    "Thumbs.db",
    "DEPOSIT_CHECKLIST.md",
    "STAGE_1_REPORT.md",
    "STAGE_2_REPORT.md",
    "paper_composition_manifest.json",
    "paper_composition_manifest.yaml",
    "paper_composition_receipt.json",
}


def package_root() -> Path:
    return Path(__file__).resolve().parent.parent


def iter_files(root: Path) -> list[Path]:
    out: list[Path] = []
    _regular(root, directory=True)
    for control in (root / MANIFEST_NAME, root / SUMS_NAME):
        if control.exists() or control.is_symlink():
            _regular(control)
    for directory, names, filenames in os.walk(root, onerror=_traversal_error, followlinks=False):
        current = Path(directory)
        kept = []
        for name in names:
            child = current / name
            _regular(child, directory=True)
            relative = child.relative_to(root).as_posix()
            if (
                name not in EXCLUDED_DIRS - ROOT_SCOPED_DIRS
                and relative not in EXCLUDED_DIR_PATHS
                and not name.endswith(".egg-info")
            ):
                kept.append(name)
        names[:] = kept
        for name in filenames:
            p = current / name
            _regular(p)
            if (p.relative_to(root).as_posix() not in {"witnessed_difference_programme.aux", "witnessed_difference_programme.toc", "witnessed_difference_programme.log"}
                    and any(p.name.endswith(suffix) for suffix in EXCLUDED_SUFFIXES)):
                continue
            if p.name in EXCLUDED_NAMES or p.name.startswith(".coverage"):
                continue
            # Only the root control files are excluded. Archived packages under
            # docs/ carry their own MANIFEST.sha256 and SHA256SUMS as payload.
            if current == root and name in (MANIFEST_NAME, SUMS_NAME):
                continue
            out.append(p)
    out.sort(key=lambda p: p.relative_to(root).as_posix().encode("utf-8"))
    return out


def _regular(path: Path, directory: bool = False) -> None:
    metadata = path.lstat()
    expected = stat.S_ISDIR if directory else stat.S_ISREG
    if not expected(metadata.st_mode) or getattr(metadata, "st_file_attributes", 0) & 0x400:
        raise ValueError(f"non-regular checksum entry: {path}")


def _traversal_error(error: OSError) -> None:
    raise ValueError(f"checksum traversal failed: {error}") from error


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def render(root: Path) -> str:
    lines = [f"{sha256_of(p)}  {p.relative_to(root).as_posix()}" for p in iter_files(root)]
    return "\n".join(lines) + "\n"


def render_sums(root: Path, manifest: Path) -> str:
    """SHA256SUMS = every deposit file, plus MANIFEST.sha256 itself."""
    lines = [f"{sha256_of(p)}  {p.relative_to(root).as_posix()}" for p in iter_files(root)]
    lines.append(f"{sha256_of(manifest)}  {MANIFEST_NAME}")
    lines.sort(key=lambda s: s.partition("  ")[2])
    return "\n".join(lines) + "\n"


def main(argv: list[str]) -> int:
    root = package_root()
    manifest = root / MANIFEST_NAME
    sums = root / SUMS_NAME
    fresh = render(root)
    if "--check" in argv:
        problems: list[str] = []
        if not manifest.is_file():
            problems.append(f"{MANIFEST_NAME} is missing from {root}")
        elif manifest.read_bytes().decode("utf-8") != fresh:
            problems.append(f"{MANIFEST_NAME} does not match tree")
        if not sums.is_file():
            problems.append(f"{SUMS_NAME} is missing from {root}")
        elif not problems:
            if sums.read_bytes().decode("utf-8") != render_sums(root, manifest):
                problems.append(f"{SUMS_NAME} does not match tree")
        for p in problems:
            print(f"FAIL: {p}")
        if problems:
            return 1
        n = fresh.count("\n")
        print(f"OK: {MANIFEST_NAME} ({n} files) and {SUMS_NAME} ({n + 1}) match the tree")
        return 0
    manifest.write_bytes(fresh.encode("utf-8"))
    sums.write_bytes(render_sums(root, manifest).encode("utf-8"))
    print(
        f"wrote {MANIFEST_NAME} ({fresh.count(chr(10))} entries) "
        f"and {SUMS_NAME} ({fresh.count(chr(10)) + 1} entries)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
