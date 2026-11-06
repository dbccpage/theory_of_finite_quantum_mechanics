"""Verify the GR-002 source and theorem inventory without trusting the authoring tool."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "manifest.json"
THEOREM_RE = re.compile(r"^theorem\s+([A-Za-z0-9_']+)", re.MULTILINE)
AXIOM_REPORT_RE = re.compile(r"^#print axioms\s+([A-Za-z0-9_']+)", re.MULTILINE)


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_hash(path: Path, expected: str, problems: list[str]) -> None:
    if not path.is_file():
        problems.append(f"missing pinned file: {path.relative_to(ROOT)}")
        return
    actual = sha256(path)
    if actual != expected:
        problems.append(
            f"hash mismatch: {path.relative_to(ROOT)} expected {expected}, got {actual}"
        )


def main() -> int:
    data = json.loads(
        MANIFEST.read_text(encoding="utf-8"),
        object_pairs_hook=reject_duplicate_keys,
    )
    problems: list[str] = []

    root_record = data["root"]
    root_path = ROOT / root_record["path"]
    check_hash(root_path, root_record["sha256"], problems)
    root_text = root_path.read_text(encoding="utf-8")

    records = data["modules"]
    recorded_paths = {record["path"] for record in records}
    actual_paths = {
        path.relative_to(ROOT).as_posix() for path in (ROOT / "GR002").glob("*.lean")
    }
    if recorded_paths != actual_paths:
        problems.append(
            f"module census mismatch: recorded={sorted(recorded_paths)}, "
            f"actual={sorted(actual_paths)}"
        )

    report_count = 0
    for record in records:
        path = ROOT / record["path"]
        check_hash(path, record["sha256"], problems)
        text = path.read_text(encoding="utf-8")
        declared = THEOREM_RE.findall(text)
        reported = AXIOM_REPORT_RE.findall(text)
        inventoried = record["theorems"]
        if declared != inventoried:
            problems.append(
                f"theorem census mismatch in {record['path']}: "
                f"manifest={inventoried}, source={declared}"
            )
        if reported != declared:
            problems.append(
                f"axiom-report census mismatch in {record['path']}: "
                f"declared={declared}, reported={reported}"
            )
        report_count += len(reported)

        module_name = record["path"].removesuffix(".lean").replace("/", ".")
        if f"import {module_name}" not in root_text:
            problems.append(f"root does not import {module_name}")

    if report_count != data["report_count"]:
        problems.append(
            f"report count mismatch: manifest={data['report_count']}, source={report_count}"
        )

    for key, relative in {
        "lake_manifest_sha256": "lake-manifest.json",
        "lakefile_sha256": "lakefile.lean",
        "lean_toolchain_sha256": "lean-toolchain",
    }.items():
        check_hash(ROOT / relative, data["package_pins"][key], problems)

    if problems:
        for problem in problems:
            print(f"FAIL: {problem}")
        return 1

    print(
        f"OK: {len(records)} modules, {report_count} theorem reports, "
        "all source/package hashes match"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
