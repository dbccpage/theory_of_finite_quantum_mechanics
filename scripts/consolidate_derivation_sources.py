"""Verify the 2026-11-05 source consolidation; no deletion on replay.

The manifest records the source bytes before relocation. Historical packages keep
their bytes; editorial changes to active manuscripts are recorded separately.
AuthorityEffect: None. Hashes establish custody, not mathematical correctness.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "docs/maintenance/source_consolidation/source_consolidation_manifest.json"


def verify() -> list[str]:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    errors = []
    destinations = set()
    for item in data["files"]:
        target = (ROOT / item["destination"]).resolve()
        if not target.is_relative_to(ROOT) or not target.is_file():
            errors.append(f"missing or escaped destination: {item['destination']}")
            continue
        if item["destination"] in destinations:
            errors.append(f"duplicate destination: {item['destination']}")
        destinations.add(item["destination"])
        expected = item.get("edited_sha256", item["sha256"])
        if hashlib.sha256(target.read_bytes()).hexdigest() != expected:
            errors.append(f"changed bytes: {item['destination']}")
    for old in data["retired_directories"]:
        if (ROOT / old).exists():
            errors.append(f"retired directory still exists: {old}")
    return errors


def main() -> int:
    argparse.ArgumentParser(description=__doc__).parse_args()
    errors = verify()
    for error in errors:
        print("FAIL", error)
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    print(f"source files={len(data['files'])}; custody failures={len(errors)}")
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
