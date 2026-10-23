"""Reproduce the CD-12 defect in the preserved, unmodified discipline code."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from argparse import ArgumentParser
from importlib.machinery import SourceFileLoader
from pathlib import Path


def audit() -> dict[str, object]:
    root = Path(__file__).resolve().parents[1]
    relative = "docs/source_archive/coda_discipline_core.py.txt"
    path = root / relative
    source = next(row for row in json.loads((root / "source_manifest.json").read_text(
        encoding="utf-8"))["sources"] if row["preserved_path"] == relative)
    if hashlib.sha256(path.read_bytes()).hexdigest() != source["sha256"]:
        raise ValueError("historical discipline source hash mismatch")
    loader = SourceFileLoader("coda_legacy_discipline", str(path))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load spec from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    embedding = module.FaithfulGroupoidEmbedding(module.make_z2_groupoid())
    left, right = embedding.embed_morphism("e"), embedding.embed_morphism("g")
    same = (
        left.p1 is right.p1
        and left.p2 is right.p2
        and left.mid_size == right.mid_size
        and left.left_map == right.left_map
        and left.right_map == right.right_map
        and left.ext_cost == right.ext_cost
    )
    if not same:
        raise AssertionError("the preserved source no longer reproduces the collision")
    return {
        "source": relative,
        "source_arrows": ["e", "g"],
        "distinct_arrows": True,
        "identical_span_data": same,
        "legacy_checker_reports_faithful": embedding.check_faithfulness(),
        "verdict": "Not faithful: distinct parallel arrows have identical span data",
        "target_status": "OPEN",
        "authority_effect": "None",
    }


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    text = json.dumps(audit(), indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")
