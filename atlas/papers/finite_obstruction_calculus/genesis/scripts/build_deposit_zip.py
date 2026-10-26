#!/usr/bin/env python3
"""Build and validate the exact dated archive from the two pinned manifests."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "SHA256SUMS"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "code"))
from deposit_paths import read_manifest

from tools.rebuild_release import (
    _is_reparse,
    _regular_control,
    release_date,
    sha256_file,
    validate,
    zip_date_from_name,
)
from tools.rebuild_release import (
    build_archive as write_archive,
)


def default_archive_name() -> str:
    return f"{ROOT.name}_{release_date(ROOT).isoformat()}.zip"


def parse_manifest(manifest_path: Path = MANIFEST, root: Path = ROOT) -> list[tuple[str, str]]:
    return read_manifest(root, manifest_path)


def build_archive(out: Path, entries: list[tuple[str, str]]) -> None:
    """Use the existing canonical writer; retain the declared release date."""
    if zip_date_from_name(ROOT, out)[:3] != tuple(release_date(ROOT).timetuple()[:3]):
        raise ValueError("archive output date differs from declared publication_date")
    if out.exists() or _is_reparse(out):
        _regular_control(out)
    members = sorted(entries + [("SHA256SUMS", sha256_file(MANIFEST))])
    out.parent.mkdir(parents=True, exist_ok=True)
    write_archive(ROOT, out, members)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, help="Exact dated release ZIP path; defaults to the declared publication date.")
    args = parser.parse_args(argv)
    try:
        problems = validate(ROOT, check_archive=False)
        if problems:
            raise ValueError("; ".join(problems))
        entries = parse_manifest()
        out = args.out if args.out is not None else ROOT / default_archive_name()
        build_archive(out, entries)
        problems = validate(ROOT, selected_archive=out)
        if problems:
            raise ValueError("; ".join(problems))
    except (OSError, UnicodeError, ValueError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print(f"wrote and verified {out} -- {len(entries) + 1} files, {out.stat().st_size / 1024:.0f} KB")
    print("contains exactly the pinned set; fixed metadata and complete canonical ZIP bytes checked.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
