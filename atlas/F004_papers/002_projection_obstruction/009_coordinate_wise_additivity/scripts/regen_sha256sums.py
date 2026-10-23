#!/usr/bin/env python3
"""Deterministically regenerate or verify the two release manifests."""

from __future__ import annotations

import sys
from pathlib import Path

if __package__:
    from .release_contract import (
        ReleaseContractError,
        enumerate_payload,
        render_manifest,
        verify_tree_and_manifests,
    )
else:
    from release_contract import (  # type: ignore[no-redef, import-not-found]
        ReleaseContractError,
        enumerate_payload,
        render_manifest,
        verify_tree_and_manifests,
    )


ROOT = Path(__file__).resolve().parent.parent
ARCHIVE_NAME = "coordinate_wise_additivity_2026-10-02.zip"
EXCLUDED_DIRS = {
    ".git",
    ".venv",
    "venv",
    "lean4/.lake",
    "lean4/b",
    "lean4/p",
    "code/009_coordinate_wise_additivity.egg-info",
}
EXCLUDED_NAMES = {
    ".coverage",
    "cov.json",
}
EXCLUDED_SUFFIXES = {".pyc", ".pyo"}


def main(argv: list[str]) -> int:
    if argv not in ([], ["--check"]):
        print("usage: regen_sha256sums.py [--check]", file=sys.stderr)
        return 2
    try:
        if argv == ["--check"]:
            entries = verify_tree_and_manifests(
                ROOT,
                excluded_dirs=EXCLUDED_DIRS,
                excluded_names=EXCLUDED_NAMES,
                excluded_suffixes=EXCLUDED_SUFFIXES,
                archive_name=ARCHIVE_NAME,
            )
            print(f"OK: both manifests exactly match the tree ({len(entries)} files)")
            return 0

        payload = enumerate_payload(
            ROOT,
            excluded_dirs=EXCLUDED_DIRS,
            excluded_names=EXCLUDED_NAMES,
            excluded_suffixes=EXCLUDED_SUFFIXES,
            archive_name=ARCHIVE_NAME,
        )
        fresh = render_manifest(ROOT, payload)
        (ROOT / "SHA256SUMS").write_bytes(fresh)
        (ROOT / "MANIFEST.sha256").write_bytes(fresh)
        print(f"Updated SHA256SUMS and MANIFEST.sha256 with {len(payload)} files.")
        return 0
    except (OSError, ReleaseContractError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
