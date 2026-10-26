#!/usr/bin/env python3
"""Validate or refresh named F005 packages with the canonical release builder.

Keeping only this package-name CLI here prevents a second date and ZIP policy
from drifting away from the shared paper template.
"""

from __future__ import annotations

import argparse
import importlib.util
import re
from pathlib import Path

CANONICAL = (
    Path(__file__).resolve().parents[2]
    / "_kits/paper_template/tools/rebuild_release.py"
)
SPEC = importlib.util.spec_from_file_location("canonical_f005_release", CANONICAL)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Cannot load canonical release builder: {CANONICAL}")
release = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(release)

ROOT = Path(__file__).resolve().parents[1]
ZIP_DATE = release.ZIP_DATE
sha256_file = release.sha256_file
refresh = release.refresh
archive_path = release.archive_path
validate = release.validate


def package_path(name: str) -> Path:
    if not re.fullmatch(r"[a-z][a-z0-9_]*", name):
        raise ValueError(f"invalid package name: {name}")
    package = ROOT / name
    if not package.is_dir():
        raise ValueError(f"unknown package: {name}")
    return package


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("packages", nargs="+", help="F005 package directory names")
    parser.add_argument("--check", action="store_true")
    parser.add_argument(
        "--include", action="append", default=[],
        help="package-relative file to add deliberately to each release set",
    )
    args = parser.parse_args()
    if args.check and args.include:
        parser.error("--include cannot be combined with --check")
    failed = False
    for name in args.packages:
        try:
            package = package_path(name)
            if not args.check:
                refresh(package, tuple(args.include))
            errors = validate(package)
        except (OSError, UnicodeError, ValueError) as error:
            errors = [str(error)]
        if errors:
            failed = True
            for error in errors:
                print(f"FAIL {name}: {error}")
        else:
            print(f"OK {name}: manifests and deterministic ZIP agree")
    return int(failed)


if __name__ == "__main__":
    raise SystemExit(main())
