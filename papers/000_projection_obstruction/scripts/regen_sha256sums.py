#!/usr/bin/env python3
"""Deterministically regenerate or verify both PO-000 checksum manifests.

AuthorityEffect: None. A hash match is not a proof of any mathematical claim;
it certifies only that the bytes on disk are the bytes that were hashed.

MANIFEST.sha256 covers every regular payload file admitted by release_custody.files,
except both root manifest controls. SHA256SUMS covers that same payload plus
MANIFEST.sha256. Neither manifest covers itself; the dependency is noncircular.
Derived ZIPs, sidecars and local compiler diagnostics are excluded. Retained
links and traversal errors fail closed, including on both manifest controls.

Added in the v6.3 Zenodo republication pass (2026-08-31), replacing a stale
manifest that was an unlabelled fossil of the v6.1 staging tree (16 entries
for files that did not exist, 26 present files unlisted, and 10 hash
mismatches as measured against the working checkout on 2026-08-31 -- 6 of
the 10 were ``.bat`` files, so that last count is checkout-dependent; an
earlier draft said 13, which did not reproduce).
Regenerating this manifest is the FINAL assembly step of a deposit: run it
after every other file has reached its shipped bytes.

Usage (from the package root, Python 3.10+, standard library only):

    python scripts/regen_sha256sums.py            # rewrite both manifests
    python scripts/regen_sha256sums.py --check    # verify both; exit 1 on any drift

Determinism: files are enumerated by ordinal (codepoint) sort of their
POSIX-style relative paths; output lines are ``<sha256>  <path>`` (two
spaces, the GNU coreutils format, so ``sha256sum -c SHA256SUMS`` also works);
the file is written in binary mode with LF line endings only.
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

from release_custody import files, regular

MANIFEST_NAME = "SHA256SUMS"
PAYLOAD_MANIFEST_NAME = "MANIFEST.sha256"
MANIFEST_CONTROLS = frozenset({MANIFEST_NAME, PAYLOAD_MANIFEST_NAME})


def package_root() -> Path:
    return Path(__file__).resolve().parent.parent


def iter_payload_files(root: Path) -> list[Path]:
    return [path for path in files(root)
            if path.relative_to(root).as_posix() not in MANIFEST_CONTROLS]


def iter_files(root: Path) -> list[Path]:
    """Primary-manifest members, including the explicit secondary control."""
    secondary = root / PAYLOAD_MANIFEST_NAME
    regular(secondary, root)
    return sorted([*iter_payload_files(root), secondary],
                  key=lambda path: path.relative_to(root).as_posix())


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def render(root: Path) -> str:
    lines = [f"{sha256_of(p)}  {p.relative_to(root).as_posix()}" for p in iter_files(root)]
    return "\n".join(lines) + "\n"


def render_payload(root: Path) -> str:
    return "".join(f"{sha256_of(p)}  {p.relative_to(root).as_posix()}\n"
                   for p in iter_payload_files(root))


def check_manifests(root: Path) -> list[str]:
    """Check both layers without repairing either, even if the outer hash matches."""
    problems = []
    for name, expected in ((PAYLOAD_MANIFEST_NAME, render_payload), (MANIFEST_NAME, render)):
        path = root / name
        if not path.exists() and not path.is_symlink():
            problems.append(f"{name} is missing")
            continue
        regular(path, root)
        # A missing secondary control already fails; avoid hashing a missing file.
        if name == MANIFEST_NAME and not (root / PAYLOAD_MANIFEST_NAME).is_file():
            continue
        if path.read_bytes() != expected(root).encode("utf-8"):
            problems.append(f"{name} differs from retained payload")
    return problems


def regenerate(root: Path) -> None:
    """Refresh the inner then outer manifest, refusing concurrent payload drift."""
    for name in MANIFEST_CONTROLS:
        path = root / name
        if path.exists() or path.is_symlink():
            regular(path, root)
    initial = render_payload(root)
    (root / PAYLOAD_MANIFEST_NAME).write_bytes(initial.encode("utf-8"))
    (root / MANIFEST_NAME).write_bytes(render(root).encode("utf-8"))
    if render_payload(root) != initial:
        raise ValueError("payload changed during manifest regeneration")
    problems = check_manifests(root)
    if problems:
        raise ValueError("; ".join(problems))


def main(argv: list[str]) -> int:
    root = package_root()
    if "--check" in argv:
        problems = check_manifests(root)
        for problem in problems:
            print(f"FAIL: {problem}")
        if problems:
            return 1
        print(f"OK: both manifests match the tree ({len(iter_payload_files(root))} payload files)")
        return 0
    regenerate(root)
    print(f"wrote {PAYLOAD_MANIFEST_NAME} and {MANIFEST_NAME}: "
          f"{len(iter_payload_files(root))} payload files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
