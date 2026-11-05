"""Offline source-bound replay. Run with --write PATH or --check PATH."""

from __future__ import annotations

import argparse
import hashlib
import json
import stat
from dataclasses import asdict
from pathlib import Path

from .checker import check
from .examples import graph_pocket, qubit_countermodel, reference_problems
from .model import strict_json
from .propose import propose


def regular_parents(path: Path) -> None:
    for parent in path.absolute().parents:
        metadata = parent.lstat()
        if not stat.S_ISDIR(metadata.st_mode) or getattr(metadata, "st_file_attributes", 0) & 0x400:
            raise ValueError(f"non-regular replay directory: {parent}")


def regular_bytes(path: Path) -> bytes:
    regular_parents(path)
    metadata = path.lstat()
    if not stat.S_ISREG(metadata.st_mode) or getattr(metadata, "st_file_attributes", 0) & 0x400:
        raise ValueError(f"non-regular replay input: {path}")
    return path.read_bytes()


def source_hashes() -> dict[str, str]:
    code = Path(__file__).absolute().parents[1]
    names = [
        "certified_preservers/__init__.py",
        "certified_preservers/model.py",
        "certified_preservers/checker.py",
        "certified_preservers/propose.py",
        "certified_preservers/examples.py",
        "certified_preservers/replay.py",
        "hermitianization/model.py",
        "state_effect_readout/model.py",
    ]
    return {name: hashlib.sha256(regular_bytes(code / name)).hexdigest() for name in names}


def produce() -> dict:
    records = {}
    for name, problem in reference_problems().items():
        proposal = propose(problem)
        result = check(problem, proposal["certificate"])
        if proposal["status"] != "PROPOSED" or result.status != "VERIFIED":
            raise ValueError(f"reference example failed: {name}: {result}")
        records[name] = {"problem": problem, "proposal": proposal, "check": asdict(result)}
    return {
        "schema": "wdp.preserver.replay.v1",
        "sources": source_hashes(),
        "records": records,
        "qubit_countermodel": qubit_countermodel(),
        "pockets": [graph_pocket(3), graph_pocket(4)],
        "authority_effect": "None",
    }


def replay(path: Path) -> dict:
    initial_bytes = regular_bytes(path)
    retained = strict_json(initial_bytes.decode("utf-8"))
    expected_keys = {
        "schema",
        "sources",
        "records",
        "qubit_countermodel",
        "pockets",
        "authority_effect",
    }
    if type(retained) is not dict or set(retained) != expected_keys:
        raise ValueError("malformed replay envelope")
    if retained["schema"] != "wdp.preserver.replay.v1" or retained["sources"] != source_hashes():
        raise ValueError("replay source binding failed")
    problems = reference_problems()
    if set(retained["records"]) != set(problems):
        raise ValueError("reference task coverage changed")
    for name, record in retained["records"].items():
        if record["problem"] != problems[name]:
            raise ValueError(f"wrong original task: {name}")
        candidate = record["proposal"]["certificate"]
        actual = check(record["problem"], candidate)
        if actual.status != "VERIFIED" or asdict(actual) != record["check"]:
            raise ValueError(f"submitted witness/receipt failed: {name}")
        # Proposal accounting is reproduced separately after submitted-witness checking.
        if record["proposal"] != propose(record["problem"]):
            raise ValueError(f"proposal/resource record changed: {name}")
    if retained["qubit_countermodel"] != qubit_countermodel():
        raise ValueError("countermodel replay failed")
    if retained["pockets"] != [graph_pocket(3), graph_pocket(4)]:
        raise ValueError("bounded graph pocket replay failed")
    if retained["authority_effect"] != "None":
        raise ValueError("mathematical receipt cannot grant authority")
    if retained["sources"] != source_hashes() or regular_bytes(path) != initial_bytes:
        raise ValueError("replay source or control changed during checking")
    return {"status": "VERIFIED", "episodes": len(problems), "pockets": 2, "model_calls": 0}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--write", type=Path)
    group.add_argument("--check", type=Path)
    args = parser.parse_args()
    if args.write:
        args.write.parent.mkdir(parents=True, exist_ok=True)
        regular_parents(args.write)
        if args.write.exists() or args.write.is_symlink():
            regular_bytes(args.write)
        args.write.write_text(
            json.dumps(produce(), indent=2) + "\n", encoding="utf-8", newline="\n"
        )
        print(json.dumps(replay(args.write), sort_keys=True))
    else:
        print(json.dumps(replay(args.check), sort_keys=True))


if __name__ == "__main__":
    main()
