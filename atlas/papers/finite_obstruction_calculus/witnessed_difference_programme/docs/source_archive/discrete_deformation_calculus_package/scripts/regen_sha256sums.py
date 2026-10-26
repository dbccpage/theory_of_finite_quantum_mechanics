"""Write both non-circular manifests, verify them, then build the archive.

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
    manifest_names,
    render_sums,
    verify_hashes,
)


def main() -> int:
    (PACKAGE / MANIFEST).write_text(render_sums(PACKAGE, manifest_names()), encoding="utf-8", newline="\n")
    names = sorted(manifest_names() + [MANIFEST], key=lambda s: s.encode("utf-8"))
    (PACKAGE / SUMS).write_text(render_sums(PACKAGE, names), encoding="utf-8", newline="\n")
    problems = verify_hashes()
    if problems:
        raise ValueError("; ".join(problems))
    build_archive(PACKAGE / ARCHIVE)
    print(f"{MANIFEST}: {len(manifest_names())} files; {ARCHIVE} built; {SUMS}: {len(names)} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
