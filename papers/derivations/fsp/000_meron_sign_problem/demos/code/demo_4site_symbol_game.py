#!/usr/bin/env python3
"""demo_4site_symbol_game.py: Demonstration & Replay of the 4-site Meron Fermion Sign Problem.

AuthorityEffect: None.

Usage:
  # Replay all 4 certified models offline (zero cost, zero network):
  python demo_4site_symbol_game.py

  # Run live against OpenRouter (requires OPENROUTER_API_KEY):
  python demo_4site_symbol_game.py --live --model stealth/space-bunny-alpha
  python demo_4site_symbol_game.py --live --model meta-llama/llama-3.3-70b-instruct
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

DEMO_DIR = Path(__file__).resolve().parent
CODE_DIR = DEMO_DIR.parents[1] / "code"
if str(CODE_DIR) not in sys.path:
    sys.path.insert(0, str(CODE_DIR))

from antibody_miner import AntibodyMiner
from oracle import BlindClusterOracle
from symbol_game_pfp import (
    RESULTS_DIR,
    STRUCTURAL_GUARDS,
    build_pfp_prompt_4site,
    query_openrouter_live,
    replay_certified_ladder,
)

DEMO_RESULTS_DIR = DEMO_DIR.parent / "results"


def main() -> int:
    parser = argparse.ArgumentParser(description="Demo: 4-Site Meron Symbol Game PFP Replay & Live Runner.")
    parser.add_argument("--live", action="store_true", help="Run a live OpenRouter query instead of offline replay.")
    parser.add_argument("--model", default="stealth/space-bunny-alpha", help="Model ID for live query.")
    parser.add_argument("--api-key", default=os.environ.get("OPENROUTER_API_KEY", ""), help="OpenRouter API Key.")
    parser.add_argument("--tokens", type=int, default=8192, help="Max tokens for live query.")
    args = parser.parse_args()

    print("==========================================================================")
    print("  THE SYMBOL GAME: 4-SITE MERON FERMION SIGN PROBLEM DEMO")
    print("  Model: Chandrasekharan & Wiese 1D Perimeter Loop Hamiltonian (q=3)")
    print("  Ground Truth: 256 Subgraphs, 1,296 States, Z = 912, Avg Sign = 19/27")
    print("==========================================================================")

    if args.live:
        if not args.api_key:
            print("\n[ERROR] --live requires an OpenRouter API key.")
            print("Provide it via --api-key <KEY> or export OPENROUTER_API_KEY in your environment.")
            return 1

        print(f"\n[LIVE MODE] Dispatching prompt to OpenRouter model: {args.model}")
        oracle = BlindClusterOracle()
        miner = AntibodyMiner(oracle)
        prompt = build_pfp_prompt_4site(oracle)
        print(f"  Prompt Length: {len(prompt)} characters")
        print("  Awaiting completion...")

        data = query_openrouter_live(args.model, prompt, args.api_key, max_tokens=args.tokens)
        latency = data.get("client_latency", 0)
        msg = data["choices"][0]["message"]
        content = msg.get("content") or ""
        reasoning = msg.get("reasoning") or ""
        text_to_eval = content if content.strip() else reasoning

        eval_res, _ = miner.evaluate_and_mine(text_to_eval, STRUCTURAL_GUARDS)
        print(f"\n[LIVE RESULT] Received in {latency:.2f}s | Score: {eval_res['score']}/4 (Perfect: {eval_res['perfect']})")
        print("\nRubric Verification:")
        for fb in eval_res["feedback"]:
            print(f"  {fb}")
        print("\nModel Cancellation Mechanism Output:")
        try:
            parsed = json.loads(text_to_eval.strip())
            print(f"  \"{parsed.get('cancellation_mechanism')}\"")
        except Exception:
            print(f"  {text_to_eval[:300]}...")
        return 0 if eval_res["perfect"] else 1

    results_path = DEMO_RESULTS_DIR if DEMO_RESULTS_DIR.exists() else RESULTS_DIR
    print(f"\n[REPLAY MODE] Verifying certified model ladder results offline from:\n  {results_path}\n")
    report = replay_certified_ladder(results_path)

    print(f"{'STATUS':<10} {'MODEL ID':<38} {'TIER':<30} {'LATENCY':<10}")
    print("-" * 90)
    for r in report["results"]:
        status = "PASS 4/4" if r["perfect"] else f"FAIL ({r['score']}/4)"
        print(f"{status:<10} {r['model']:<38} {r['tier']:<30} {r['latency']:.2f}s")
    print("-" * 90)
    print(f"All {report['models_tested']} models certified perfect 4/4: {report['all_perfect']}")
    print("\nAnyone who downloads this paper deposit can reproduce this exact offline receipt,")
    print("or run live with their own API key via: python demo_4site_symbol_game.py --live")
    return 0 if report["all_perfect"] else 1


if __name__ == "__main__":
    sys.exit(main())
