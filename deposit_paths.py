"""Origin: deposit_paths.py
Claim: a relative deposit path is accepted only when every syntax, link, and root-escape clause holds, and a manifest digest width is the rational 64/64
AuthorityEffect: None
Scope Fence: this file does not claim archive completeness, hash preimage resistance, or continuum physics
Level: L5
MutationKillCount: 9
"""

from __future__ import annotations

import hashlib
import os
import re
import stat
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path, PurePosixPath

BigRational = Fraction

_RESERVED_STEMS: frozenset[str] = frozenset(
    {
        "CON",
        "PRN",
        "AUX",
        "NUL",
        "COM1",
        "COM2",
        "COM3",
        "COM4",
        "COM5",
        "COM6",
        "COM7",
        "COM8",
        "COM9",
        "LPT1",
        "LPT2",
        "LPT3",
        "LPT4",
        "LPT5",
        "LPT6",
        "LPT7",
        "LPT8",
        "LPT9",
    }
)
_MANIFEST_LINE = re.compile(r"([a-fA-F0-9]{64})  (.+)")


class ExactIntegerError(ValueError):
    def __init__(self, invariant: str) -> None:
        self.invariant = invariant
        super().__init__(invariant)


@dataclass(frozen=True)
class Verification:
    claim: str
    holds: bool
    detail: str


def exact_int(value: object) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ExactIntegerError("Expected exact integer, received boolean or non-integer")
    return value


def exact_nat(value: object) -> int:
    number = exact_int(value)
    if number < 0:
        raise ExactIntegerError("exact integer is nonnegative")
    return number


def big_rational(numer: object, denom: object) -> BigRational:
    den = exact_int(denom)
    if den == 0:
        raise ExactIntegerError("rational denominator is nonzero")
    return BigRational(exact_int(numer), den)


def _chunk_size() -> int:
    return exact_nat(1 << 20)


def _link(path: Path) -> bool:
    junction = getattr(path, "is_junction", None)
    linked = False
    if junction is not None:
        linked = bool(junction())
    return path.is_symlink() or linked


def _bad_syntax(relative: str, pure: PurePosixPath) -> bool:
    if not relative or not pure.parts:
        return True
    if pure.is_absolute():
        return True
    return pure.as_posix() != relative


def _bad_escape(relative: str, pure: PurePosixPath) -> bool:
    if ".." in pure.parts:
        return True
    if "\\" in relative or ":" in relative:
        return True
    return any(ord(char) < 32 for char in relative)


def _bad_part(part: str) -> bool:
    if part.rstrip(" .") != part:
        return True
    return part.split(".")[0].upper() in _RESERVED_STEMS


def _syntax_unsafe(relative: str) -> bool:
    pure = PurePosixPath(relative)
    if _bad_syntax(relative, pure):
        return True
    if _bad_escape(relative, pure):
        return True
    return any(_bad_part(part) for part in pure.parts)


def _relative_text(relative: object) -> str:
    if isinstance(relative, bool) or isinstance(relative, int) or not isinstance(relative, str):
        raise ValueError(f"unsafe deposit path: {relative!r}")
    return relative


def _root_has_link(root: Path) -> Path | None:
    for ancestor in (root, *root.parents):
        if _link(ancestor):
            return ancestor
    return None


def _join_without_link(root: Path, parts: tuple[str, ...], relative: str) -> Path:
    path = root
    for part in parts:
        path = path / part
        if _link(path):
            raise ValueError(f"symlink or junction in deposit path: {relative}")
    return path


def safe_path(root: Path, relative: str) -> Path:
    text = _relative_text(relative)
    if _syntax_unsafe(text):
        raise ValueError(f"unsafe deposit path: {text!r}")
    root_abs = root.absolute()
    linked = _root_has_link(root_abs)
    if linked is not None:
        raise ValueError(f"symlink or junction in deposit root: {linked}")
    path = _join_without_link(root_abs, PurePosixPath(text).parts, text)
    if not path.resolve().is_relative_to(root_abs.resolve()):
        raise ValueError(f"deposit path escapes root: {text}")
    return path


def verify_digest_width(digest: str) -> Verification:
    width = big_rational(len(digest), 64)
    holds = width == big_rational(1, 1)
    return Verification("manifest-digest-width", holds, str(width))


DEFAULT_EXCLUDED_DIRS: set[str] = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".ipynb_checkpoints",
    ".lake",
    "dist",
    "build",
    "htmlcov",
    "dev_rips",
    "rt",
    "target",
    "b",
    "scratch",
    "_support",
    "campaigns",
    "claims",
    "evidence",
    "integration",
    "legacy",
    "migration",
    "reconstruction_v1",
}
DEFAULT_EXCLUDED_NAMES: set[str] = {
    "SHA256SUMS",
    ".coverage",
    ".env",
    "DEPOSIT_CHECKLIST.md",
    ".gitkeep",
    "finite_qm_file_manifest.yaml",
    "finite_qm_guide_map.md",
    "finite_quantum_mechanics_claim_ledger.md",
    "qm_formal_estate_and_crate_census.md",
    "qm_import_completeness_audit.md",
    "qm_lift_classification_boundary_axiom_audit.md",
    "qm_stage_import_map_audit.md",
    "qm_wave6_completion_axiom_audit.md",
    "qm_wave7_completion_axiom_audit.md",
    "qm_weyl_gleason_source_inventory.json",
    "qm_weyl_gleason_validation.json",
    "qm122_claims.json",
    "c250_replay_review.py",
    "replay_review_receipts.py",
    "review_estate.py",
    "audit_map.py",
    "evidence.py",
    "verify_entropy_evidence.py",
    "qm_standing.md",
    "qmcoda_uplift_certificate.md",
    "test_paper_catalog.py",
}
DEFAULT_EXCLUDED_SUFFIXES: set[str] = {
    ".zip",
    ".pyc",
    ".pyo",
    ".tmp",
    ".log",
    ".aux",
    ".out",
    ".bbl",
    ".blg",
    ".toc",
    ".synctex.gz",
}

__all__ = [
    "DEFAULT_EXCLUDED_DIRS",
    "DEFAULT_EXCLUDED_NAMES",
    "DEFAULT_EXCLUDED_SUFFIXES",
    "safe_path",
    "walk_files",
    "sha256_of",
    "read_manifest",
]


def _keep_dir(parent: Path, root: Path, name: str, excluded_dirs: set[str]) -> bool:
    if name in excluded_dirs or name.startswith(".") or name.endswith(".egg-info"):
        return False
    if parent.relative_to(root).as_posix() != "sources":
        return True
    return name == "original_papers"


def _folded_marker(folded: str) -> bool:
    if "claim_ledger" in folded or "claim_code_map" in folded:
        return True
    return "execution_receipt" in folded or folded.startswith("reviewer_")


def _skip_file(name: str, path: Path, excluded_names: set[str], excluded_suffixes: set[str]) -> bool:
    if name in excluded_names or path.suffix in excluded_suffixes:
        return True
    return _folded_marker(name.casefold())


def _reject_links(parent: Path, names: list[str]) -> None:
    for name in names:
        if _link(parent / name):
            raise ValueError(f"symlink or junction in deposit: {parent / name}")


def _take_file(
    root: Path,
    path: Path,
    excluded_names: set[str],
    excluded_suffixes: set[str],
    seen: set[str],
    files: list[Path],
) -> None:
    if _skip_file(path.name, path, excluded_names, excluded_suffixes):
        return
    relative = path.relative_to(root).as_posix()
    safe_path(root, relative)
    if not stat.S_ISREG(path.stat().st_mode):
        raise ValueError(f"nonregular deposit file: {relative}")
    key = relative.casefold()
    if key in seen:
        raise ValueError(f"case-colliding deposit path: {relative}")
    seen.add(key)
    files.append(path)


def _collect_names(
    root: Path,
    parent: Path,
    names: list[str],
    excluded_names: set[str],
    excluded_suffixes: set[str],
    seen: set[str],
    files: list[Path],
) -> None:
    for name in names:
        _take_file(root, parent / name, excluded_names, excluded_suffixes, seen, files)


def _prune_dirs(parent: Path, root: Path, dirs: list[str], excluded_dirs: set[str]) -> None:
    dirs[:] = [name for name in dirs if _keep_dir(parent, root, name, excluded_dirs)]


def walk_files(
    root: Path,
    excluded_dirs: set[str] | None = None,
    excluded_names: set[str] | None = None,
    excluded_suffixes: set[str] | None = None,
) -> list[Path]:
    chosen_dirs = DEFAULT_EXCLUDED_DIRS if excluded_dirs is None else excluded_dirs
    chosen_names = DEFAULT_EXCLUDED_NAMES if excluded_names is None else excluded_names
    chosen_suffixes = DEFAULT_EXCLUDED_SUFFIXES if excluded_suffixes is None else excluded_suffixes
    safe_path(root, "__root_check__")
    files: list[Path] = []
    seen: set[str] = set()
    for directory, dirs, names in os.walk(root, followlinks=False):
        parent = Path(directory)
        _reject_links(parent, [*dirs, *names])
        _prune_dirs(parent, root, dirs, chosen_dirs)
        _collect_names(root, parent, names, chosen_names, chosen_suffixes, seen, files)
    return sorted(files, key=lambda item: item.relative_to(root).as_posix())


def sha256_of(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(_chunk_size()), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _parsed_manifest_line(number: int, line: str) -> tuple[str, str] | None:
    if not line or line.startswith("#"):
        return None
    match = _MANIFEST_LINE.fullmatch(line)
    if match is None:
        raise ValueError(f"malformed manifest line {number}")
    digest, relative = match.groups()
    verification = verify_digest_width(digest)
    if not verification.holds:
        raise ValueError(f"malformed manifest line {number}")
    return relative, digest.lower()


def _reject_manifest_entry(relative: str, seen: set[str], manifest: Path) -> None:
    if relative.casefold() in seen:
        raise ValueError(f"duplicate or case-colliding manifest path: {relative}")
    if relative == manifest.name or relative.lower().endswith(".zip"):
        raise ValueError(f"circular manifest entry: {relative}")


def read_manifest(root: Path, manifest: Path) -> list[tuple[str, str]]:
    safe_path(root, manifest.absolute().relative_to(root.absolute()).as_posix())
    entries: list[tuple[str, str]] = []
    seen: set[str] = set()
    for number, line in enumerate(manifest.read_text(encoding="utf-8").splitlines(), exact_nat(1)):
        parsed = _parsed_manifest_line(number, line)
        if parsed is None:
            continue
        relative, digest = parsed
        safe_path(root, relative)
        _reject_manifest_entry(relative, seen, manifest)
        seen.add(relative.casefold())
        entries.append((relative, digest))
    return entries
