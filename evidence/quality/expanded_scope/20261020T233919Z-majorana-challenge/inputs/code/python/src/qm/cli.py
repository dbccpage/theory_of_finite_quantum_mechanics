"""Command line entrypoint for finite quantum computations and evidence inspection."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .api import claims, list_suites, run_json, run_suite


def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(prog="finite-qm")
    commands = parser.add_subparsers(dest="command", required=True)
    listing = commands.add_parser("list", help="List the bundled computational suites")
    listing.add_argument("--json", action="store_true")
    run = commands.add_parser("run", help="Run a suite using its bundled fixture or an exact JSON input")
    run.add_argument("suite", choices=list_suites())
    run.add_argument("--input", type=Path)
    run.add_argument("--json", action="store_true")
    claim = commands.add_parser("claims", help="Show source-linked claim dispositions")
    claim.add_argument("paper", choices=["qm122"])
    claim.add_argument("--json", action="store_true")
    evidence = commands.add_parser("evidence", help="Verify a source manifest at its recorded Git revision")
    evidence.add_argument("action", choices=["check", "bets"])
    evidence.add_argument("manifest", type=Path, nargs="?")
    evidence.add_argument("--revision", help="Recorded full Git commit, required for bet verification")
    evidence.add_argument("--project-root", type=Path, required=True)
    evidence.add_argument("--json", action="store_true")
    lean = commands.add_parser("lean-replay", help="Build the preserved QM_122 Lean target at its pinned toolchain")
    lean.add_argument("--project-root", type=Path, required=True)
    lean.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.command == "list":
            result = list_suites()
        elif args.command == "run":
            result = run_json(args.suite, args.input.read_text(encoding="utf-8")) if args.input else run_suite(args.suite)
        elif args.command == "claims":
            result = claims(args.paper)
        else:
            from .evidence import check_manifest, replay_lean, verify_bets
            if args.command == "lean-replay":
                result = replay_lean(args.project_root)
            elif args.action == "bets":
                if not args.revision:
                    raise ValueError("PINNED_COMMIT_REQUIRED: use --revision")
                result = verify_bets(args.project_root, args.revision)
            else:
                if args.manifest is None:
                    raise ValueError("SOURCE_MANIFEST_REQUIRED")
                result = check_manifest(args.project_root, args.manifest)
        if args.command == "list" and not args.json:
            print("\n".join(result))
        elif args.command == "claims" and not args.json:
            for row in result["claims"]:
                print(f"{row['id']}: {row['disposition']}\n  {row['source_statement']}")
        else:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0
    except (ValueError, OSError, RuntimeError) as error:
        print(str(error), file=sys.stderr)
        return 2
