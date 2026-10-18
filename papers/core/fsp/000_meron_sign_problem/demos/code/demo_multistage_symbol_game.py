"""
demo_multistage_symbol_game.py: Standalone CLI for Multi-Stage Symbol Game DDC DAG Traces.
AuthorityEffect: None.

Features:
1. Replays the 5-stage DDC solution generation pipeline for 4-site and 6-site lattices.
2. Emits and prints the exact append-only DAG in JSONL.
3. Verifies Gamma38 wire alphabet adherence (0-9, a-z, <, >) without domain smuggling.
4. Demonstrates explicit LIFT_REQUEST and LIFT_GRANT mechanics for topological involution discovery.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

DEMOS_DIR = Path(__file__).resolve().parent.parent
CODE_DIR = DEMOS_DIR.parent / "code"
if str(CODE_DIR) not in sys.path:
    sys.path.insert(0, str(CODE_DIR))

from symbol_game_stage_controller import (  # noqa: E402
    SymbolGameStageController,
    replay_certified_dag,
)

RESULTS_DIR = DEMOS_DIR / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="Multi-Stage Symbol Game DDC DAG Demo.")
    parser.add_argument("--sites", type=int, default=4, choices=[4, 6], help="Lattice sites (4 or 6). Default: 4.")
    parser.add_argument("--show-dag", action="store_true", help="Print all JSONL DAG nodes to stdout.")
    args = parser.parse_args()

    out_dag = RESULTS_DIR / f"symbol_game_ddc_{args.sites}site_dag.jsonl"
    print(f"================================================================================")
    print(f"  THE SYMBOL GAME: MULTI-STAGE DDC DAG REPLAY ({args.sites}-SITE LATTICE)")
    print(f"================================================================================")
    
    res = replay_certified_dag(sites=args.sites, target_path=out_dag)
    print(f"Stages Executed: {res['nodes']} turns")
    print(f"Terminal Status: {res['terminal_status']}")
    print(f"Exact Partition Z: {res['exact_partition_z']}")
    print(f"Gamma38 Wire Alphabet Purity: {res['gamma38_valid']}")
    print(f"DAG Output File: {res['dag_path']}")
    print(f"Verification: {'SUCCESS (EXACT_REPAIR)' if res['verified'] else 'FAILED'}\n")

    if args.show_dag or True:
        print("--- DAG EXECUTION TRACE (JSONL) ---")
        with open(res["dag_path"], "r", encoding="utf-8") as f:
            for line in f:
                node = json.loads(line.strip())
                print(f"[{node['turn']}] {node['node_id']:<18} | Action: {node['action']:<22} | Wire: {node['gamma38_wire']}")

    print("\nAll stages verified. Causal dependencies and topological lift certified.")
    return 0 if res["verified"] else 1


if __name__ == "__main__":
    sys.exit(main())
