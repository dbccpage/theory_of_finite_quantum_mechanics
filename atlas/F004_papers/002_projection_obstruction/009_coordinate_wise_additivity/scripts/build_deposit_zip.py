#!/usr/bin/env python3
"""Build a deterministic archive from the exact manifest-bound payload."""

from __future__ import annotations

import sys
from pathlib import Path

if __package__:
    from .regen_sha256sums import EXCLUDED_DIRS, EXCLUDED_NAMES, EXCLUDED_SUFFIXES
    from .release_contract import (
        ReleaseContractError,
        build_archive,
        sha256_of,
        verify_tree_and_manifests,
    )
else:
    from regen_sha256sums import (  # type: ignore[no-redef, import-not-found]
        EXCLUDED_DIRS,
        EXCLUDED_NAMES,
        EXCLUDED_SUFFIXES,
    )
    from release_contract import (  # type: ignore[no-redef, import-not-found]
        ReleaseContractError,
        build_archive,
        sha256_of,
        verify_tree_and_manifests,
    )


ROOT = Path(__file__).resolve().parent.parent
ARCHIVE_NAME = "coordinate_wise_additivity_2026-10-02.zip"
ZIP_DATE = (2026, 10, 2, 12, 0, 0)


def main(argv: list[str]) -> int:
    if argv:
        print("usage: build_deposit_zip.py", file=sys.stderr)
        return 2
    try:
        entries = verify_tree_and_manifests(
            ROOT,
            excluded_dirs=EXCLUDED_DIRS,
            excluded_names=EXCLUDED_NAMES,
            excluded_suffixes=EXCLUDED_SUFFIXES,
            archive_name=ARCHIVE_NAME,
        )
        destination = ROOT / ARCHIVE_NAME
        build_archive(
            destination,
            ROOT,
            entries,
            prefix="coordinate_wise_additivity",
            zip_date=ZIP_DATE,
        )
    except (OSError, ReleaseContractError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1

    print(f"BUILT: {destination} ({destination.stat().st_size} bytes, {len(entries)} files)")
    print(f"SHA256: {sha256_of(destination)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
