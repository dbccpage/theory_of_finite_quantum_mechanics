"""Check the vendored H3V7N5QF tree against origin/main blob ids.

AuthorityEffect: None. A match says the bytes equal the pin. It is not a proof
of a manuscript claim.

    python omega_engine_education/documentation/005_genesis_ongoing/code/check_h3_pin.py
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

PIN_COMMIT = "5d9488324ce976817987bd83a28d901371cfc073"
HERE = Path(__file__).resolve().parent
PIN_FILE = HERE / "h3_origin_main_5d948832.lstree"


def repo_root() -> Path:
    for parent in HERE.parents:
        if (parent / ".git").exists():
            return parent
    raise SystemExit("repository root not found")


def paper_root() -> Path:
    return (
        repo_root()
        / "omega_engine_atlas"
        / "coda_atlas"
        / "papers"
        / "finite_obstruction_calculus"
        / "genesis_ongoing"
    )


class PinError(Exception):
    """The pin list is not a unique path-to-blob table."""


def blob_sha1(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def parse_pin(text: str) -> dict[str, str]:
    rows: dict[str, str] = {}
    for line_no, line in enumerate(text.splitlines(), start=1):
        sha, separator, path = line.partition("\t")
        if separator == "" or sha == "" or path == "":
            raise PinError(f"pin line {line_no} is not sha<TAB>path")
        if path in rows:
            raise PinError(f"duplicate pin path {path}")
        rows[path] = sha
    return rows


def load_pin() -> dict[str, str]:
    return parse_pin(PIN_FILE.read_text(encoding="utf-8"))


def differences() -> list[str]:
    try:
        expected = load_pin()
    except PinError as exc:
        return [str(exc)]
    root = paper_root()
    found: dict[str, str] = {}
    for file in root.rglob("*"):
        if not file.is_file():
            continue
        found[file.relative_to(root).as_posix()] = blob_sha1(file.read_bytes())
    problems: list[str] = []
    for path in sorted(set(expected) - set(found)):
        problems.append(f"missing {path}")
    for path in sorted(set(found) - set(expected)):
        problems.append(f"extra {path}")
    for path in sorted(set(expected) & set(found)):
        if expected[path] != found[path]:
            problems.append(f"mismatch {path}")
    return problems


def main() -> int:
    problems = differences()
    if problems:
        print(f"pin {PIN_COMMIT} failed: {len(problems)}")
        for row in problems[:30]:
            print(row)
        return 1
    print(f"pin {PIN_COMMIT} exact {len(load_pin())} blobs")
    return 0


if __name__ == "__main__":
    sys.exit(main())
