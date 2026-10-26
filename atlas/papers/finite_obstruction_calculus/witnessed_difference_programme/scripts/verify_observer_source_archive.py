"""Verify the exact original observer corpus retained for offline review.

A source digest verifies custody, not a mathematical adapter theorem. The
separate source-family index records lexical review cues, not a proof that a
finite table implements an arbitrary history function or operator gauge.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import stat
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHA256 = re.compile(r"[0-9a-f]{64}")


def regular(path: Path) -> bytes:
    path = path.absolute()
    for parent in path.parents:
        info = parent.lstat()
        if not stat.S_ISDIR(info.st_mode) or getattr(info, "st_file_attributes", 0) & 0x400:
            raise ValueError(f"non-regular source directory: {parent}")
    info = path.lstat()
    if not stat.S_ISREG(info.st_mode) or getattr(info, "st_file_attributes", 0) & 0x400:
        raise ValueError(f"non-regular source file: {path}")
    return path.read_bytes()


def verify(root: Path = ROOT) -> dict[str, object]:
    provenance = json.loads(regular(root / "source_provenance.json").decode("utf-8"))
    inventory = json.loads(regular(root / "docs" / "legacy_observer_inventory.json").decode("utf-8"))
    originals = provenance["files"]
    observed = inventory["original_files"]
    if len(observed) != len(originals):
        raise ValueError("original observer inventory count differs from provenance")
    paths: set[str] = set()
    total = 0
    lines = []
    for recorded, recovery in zip(originals, observed, strict=True):
        digest = recorded["sha256"]
        path = recorded["path"]
        size = recorded["bytes"]
        if not isinstance(digest, str) or SHA256.fullmatch(digest) is None:
            raise ValueError("invalid original source SHA-256")
        if not isinstance(path, str) or path in paths:
            raise ValueError("invalid or duplicate original source path")
        if type(size) is not int or size < 0:
            raise ValueError("invalid original byte count")
        paths.add(path)
        if recovery["recorded_path"] != path or recovery["recorded_sha256"] != digest:
            raise ValueError(f"original inventory identity drift: {path}")
        member = root / "docs" / "source_archive" / "coda_original_source_snapshot" / f"{digest}.txt"
        if member.is_symlink():
            raise ValueError(f"source archive member must be a regular file: {path}")
        data = regular(member)
        if len(data) != size or hashlib.sha256(data).hexdigest() != digest:
            raise ValueError(f"source archive bytes differ from provenance: {path}")
        total += size
        lines.append((path, f"{path}\t{digest}\t{size}"))
    aggregate = hashlib.sha256("\n".join(line for _, line in sorted(lines)).encode()).hexdigest()
    snapshot = provenance["snapshot"]
    if (len(originals), total, aggregate) != (
        snapshot["file_count"], snapshot["total_bytes"], snapshot["sha256"]
    ):
        raise ValueError("original snapshot aggregate differs from provenance")
    families = inventory["identified_families"]
    genesis = [family for family in families if family["family"] == "six-component genesis"]
    if len(genesis) != 1 or genesis[0]["fields"] != ["M", "U", "p", "rho", "G", "T"]:
        raise ValueError("original Genesis six must retain its actual source vocabulary")
    expected = {
        ("original", "original44", item["path"]): (item["sha256"], item["bytes"])
        for item in originals
    }
    for block in provenance["absorbed_snapshots"]:
        expected.update({
            ("absorbed", block["id"], item["path"]): (item["sha256"], item["bytes"])
            for item in block["files"]
        })
    indexed = {}
    for item in inventory["source_family_index"]:
        key = (item["source_scope"], item["source_id"], item["recorded_path"])
        if key in indexed:
            raise ValueError("duplicate source-family index occurrence")
        indexed[key] = item
    if indexed.keys() != expected.keys() or any(
        (indexed[key]["recorded_sha256"], indexed[key]["bytes"]) != value
        for key, value in expected.items()
    ):
        raise ValueError("source-family index is not bound to every recorded occurrence")
    reviewed = {}
    for item in inventory["semantic_family_review"]:
        key = (item["source_scope"], item["source_id"], item["recorded_path"])
        if key in reviewed or key not in indexed:
            raise ValueError("duplicate or unknown semantic review occurrence")
        if item["recorded_sha256"] != indexed[key]["recorded_sha256"]:
            raise ValueError("semantic review is not bound to its source bytes")
        if item["reviewed_cue_lines"] != [cue["line"] for cue in indexed[key]["definition_cues"]]:
            raise ValueError("semantic review does not cover its indexed definition cues")
        reviewed[key] = item
    cue_records = {key for key, item in indexed.items() if item["definition_cues"]}
    if reviewed.keys() != cue_records:
        raise ValueError("semantic review must cover every indexed cue record")
    return {
        "status": "PASS", "authority_effect": "None", "original_files_checked": len(originals),
        "total_bytes": total, "snapshot_sha256": aggregate,
        "source_occurrences_indexed": len(indexed), "cue_records_reviewed": len(reviewed),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    print(json.dumps(verify(args.root), indent=2))


if __name__ == "__main__":
    main()
