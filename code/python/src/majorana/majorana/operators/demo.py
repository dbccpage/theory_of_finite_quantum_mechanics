from __future__ import annotations
# SPDX-License-Identifier: Apache-2.0


import argparse
import json
import sys
import os
from typing import Any

from demos.ising_demo import run_ising_demo
from demos.tgp_demo import run_tgp_demo
from demos.ambiguity_demo import run_ambiguity_demo
from demos.gallery_demo import run_gallery_demo


_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _root not in sys.path:
    sys.path.insert(0, _root)

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Unified Omega Majorana Parity Operator and Demonstration Orchestrator"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Run all available demonstration suites"
    )
    parser.add_argument(
        "--ising",
        action="store_true",
        help="Run exact cyclotomic Ising Anyon braiding and fusion verifications"
    )
    parser.add_argument(
        "--tgp",
        action="store_true",
        help="Run Topological Gap Protocol parameter sensitivity transport demo"
    )
    parser.add_argument(
        "--ambiguity",
        action="store_true",
        help="Run topological vs trivial local generation carrier ambiguity demo"
    )
    parser.add_argument(
        "--gallery",
        action="store_true",
        help="Run full graph complex gallery (wires, loops, junctions, islands)"
    )

    args = parser.parse_args()

    if not any([args.all, args.ising, args.tgp, args.ambiguity, args.gallery]):
        args.all = True

    results: dict[str, Any] = {}

    if args.all or args.ising:
        print("Executing exact cyclotomic Ising Anyon verifications...")
        results["ising"] = run_ising_demo()

    if args.all or args.tgp:
        print("Executing parameter sensitivity gap protocol transport...")
        results["tgp"] = run_tgp_demo()

    if args.all or args.ambiguity:
        print("Executing topological vs trivial carrier ambiguity resolution...")
        results["ambiguity"] = run_ambiguity_demo()

    if args.all or args.gallery:
        print("Executing full graph complex gallery validation and terminalization...")
        results["gallery"] = run_gallery_demo()

    print("\n==================================================")
    print("           DEMONSTRATION EXECUTION RESULTS        ")
    print("==================================================")
    print(json.dumps(results, indent=2))
    print("==================================================")

    return 0


if __name__ == "__main__":
    sys.exit(main())

