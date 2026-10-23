"""Write MANIFEST.sha256, build the deposit archive, then write SHA256SUMS.

Run after every content change: ``python scripts/regen_sha256sums.py``.
AuthorityEffect: None.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from deposit_files import (  # noqa: E402
    ARCHIVE,
    MANIFEST,
    PACKAGE,
    SUMS,
    build_archive,
    deposit_files,
    manifest_names,
    render_sums,
)


def main() -> int:
    (PACKAGE / MANIFEST).write_text(render_sums(PACKAGE, manifest_names()), encoding="utf-8", newline="\n")
    build_archive(PACKAGE / ARCHIVE)
    names = [n for n in deposit_files() if n != SUMS]
    (PACKAGE / SUMS).write_text(render_sums(PACKAGE, names), encoding="utf-8", newline="\n")
    print(f"{MANIFEST}: {len(manifest_names())} files; {ARCHIVE} built; {SUMS}: {len(names)} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
