"""Offline commands: python -m faithful_representation examples|replay|verify."""

import argparse
import hashlib
import json
from pathlib import Path

from .core import check, load, replay
from .examples import boundaries, exhaustive_boolean_cases, run_examples


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("examples", "replay", "verify"))
    parser.add_argument("--directory", type=Path, default=Path(__file__).parent / "evidence")
    args = parser.parse_args()
    if args.command == "replay":
        result = replay(args.directory)
        print(json.dumps(result, sort_keys=True))
        return 0 if result["accepted"] else 1
    runs = run_examples()
    summary = {"schema_version": 1, "authority_effect": "None",
               "runs": {name: run["receipt"] for name, run in runs.items()},
               "exhaustive": exhaustive_boolean_cases(), "boundaries": boundaries(),
               "source_sha256": {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                                 for p in sorted(Path(__file__).parent.glob("*.py"))}}
    if args.command == "examples":
        args.directory.mkdir(parents=True, exist_ok=True)
        for name, run in runs.items():
            directory = args.directory / name
            directory.mkdir(exist_ok=True)
            for kind, value in run.items():
                (directory / f"{kind}.json").write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8", newline="\n")
        (args.directory / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8", newline="\n")
    else:
        if load(args.directory / "summary.json") != summary:
            raise SystemExit("source-bound evidence summary differs from recomputation")
        for name, run in runs.items():
            for kind, value in run.items():
                if load(args.directory / name / f"{kind}.json") != value:
                    raise SystemExit(f"changed retained {name}/{kind}")
            if not check(run["problem"], load(args.directory / name / "certificate.json"))["accepted"]:
                raise SystemExit(f"failed retained replay: {name}")
    print(json.dumps({"runs": len(runs), **summary["exhaustive"], "authority_effect": "None"}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
