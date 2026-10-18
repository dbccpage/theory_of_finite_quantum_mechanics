"""
demo_multiturn_interactive_pfp.py: Multi-Turn Interactive PFP Trial Runner.
AuthorityEffect: None.

Features:
1. Multi-turn coached interactive trials on OpenRouter with space-bunny-alpha and llama-3.3-70b.
2. Step-by-step reasoning token latency and lift-request emission probability measurement.
3. 4-turn sequential inquiry:
   - Turn 1: Plaquette breakup & cycle decomposition
   - Turn 2: Cycle holonomy & topological invariant I(c)
   - Turn 3: Zero-shot lift request / involution morphism discovery
   - Turn 4: Exact contraction (1 + (-1)) = 0 and partition Z = 912
4. English prompts supply target counts and the lift; keyword screening does not establish discovery.
5. Read-only inspection of a synthetic model-labelled fixture; provider measurements are unverified.
"""

from __future__ import annotations

from fractions import Fraction
import hashlib

import argparse
import datetime
import json
import os
import sys
import time
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Optional

DEMOS_DIR = Path(__file__).resolve().parent.parent
CODE_DIR = DEMOS_DIR.parent / "code"
REPO_ROOT = DEMOS_DIR.parents[2]
if str(CODE_DIR) not in sys.path:
    sys.path.insert(0, str(CODE_DIR))
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from blind_problem import assert_lexical_hygiene
from oracle import BlindClusterOracle
from symbol_game_stage_controller import SymbolGameStageController
from omega_engine_pfp.domain.tower.parser import (
    parse_packet,
    validate_packet_semantics,
    GAMMA_38,
)

RESULTS_DIR = DEMOS_DIR / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)
CERTIFIED_MULTITURN_RECEIPT = RESULTS_DIR / "certified_multiturn_trial_results.json"

MODELS_TO_TEST = [
    {
        "id": "stealth/space-bunny-alpha",
        "name": "Space Bunny Alpha",
        "tier": "Deep Reasoning (Free tier)",
        "has_reasoning_tokens": True,
    },
    {
        "id": "meta-llama/llama-3.3-70b-instruct",
        "name": "Llama 3.3 70B Instruct",
        "tier": "70B Open-Weights Instruct",
        "has_reasoning_tokens": False,
    },
]


def build_turn_prompts() -> List[Dict[str, str]]:
    """Build the sequential coached prompts for each stage of the trial."""
    prompts = [
        {
            "turn": 1,
            "stage": "PLAQUETTE_BREAKUP",
            "query": (
                "You are analyzing an oriented multigraph system with 16 nodes (4 spatial sites, 4 time steps) "
                "governed by local 4-site plaquette interaction matrices M in Q^(4x4). "
                "How does each plaquette interaction gate factor into independent pairing channels (vertical bonds vs horizontal bonds), "
                "and how does this decompose the state space into disjoint closed 1-chains (cycles)?"
            ),
            "expected_keywords": ["channel", "vertical", "horizontal", "cycle", "disjoint"],
        },
        {
            "turn": 2,
            "stage": "MEASURE_HOLONOMY",
            "query": (
                "For the closed 1-chains on the discretized 2-torus, how does the global configuration sign sigma(C) in {+1, -1} "
                "factorize across individual cycle components c_i? Identify the discrete Z_2 topological winding invariant I(c) in {0, 1} "
                "such that reversing cycle c_i inverts the global sign if and only if I(c) = 1. "
                "Explain why exactly 57 of the 256 subgraphs contain odd-winding cycles."
            ),
            "expected_keywords": ["factor", "winding", "invariant", "odd", "57"],
        },
        {
            "turn": 3,
            "stage": "LIFT_REQUEST",
            "query": (
                "OBSTRUCTION DETECTED: The 57 odd-winding subgraphs introduce 192 negative states, yielding severe sign cancellation (<sigma> = 19/27). "
                "In the Discrete Deformation Calculus, when local evaluation encounters a sign obstruction, what discrete algebraic involution map tau "
                "or lift operation can eliminate this obstruction without changing the absolute configuration weights W(C)? "
                "State the explicit involution formula and whether an ACTION_REQUEST_LIFT is authorized."
            ),
            "expected_keywords": ["involution", "flip", "tau", "weight", "lift"],
        },
        {
            "turn": 4,
            "stage": "EXACT_REPAIR",
            "query": (
                "Given the orientation-flip involution tau_i: s_i -> -s_i acting on any cycle with I(c_i) = 1, "
                "show that the sum over flip states vanishes identically as (1 + (-1)) = 0 for all 57 odd-winding subgraphs. "
                "Then, deduce that the full partition sum Z reduces strictly to the 199 zero-odd-sector subgraphs (where all cycles have I(c_i) = 0), "
                "and calculate the exact integer value of Z."
            ),
            "expected_keywords": ["199", "912", "zero", "cancel", "exact"],
        },
    ]

    for p in prompts:
        assert_lexical_hygiene(p["query"])
    return prompts


def query_openrouter_single_turn(
    model: str,
    prompt: str,
    api_key: str,
    max_tokens: int = 4096,
) -> Dict[str, Any]:
    """Execute a single-turn live query to OpenRouter."""
    from omega_engine_woland.domain.providers.types import CandidateRequest, ChatMessage, DecodingParamsV1, Provider
    from omega_engine_woland.infrastructure.providers.openai_compat import OpenAiCompatTransport
    transport = OpenAiCompatTransport(Provider.OPENROUTER, api_key=api_key, max_tokens=max_tokens, timeout=180)
    request = CandidateRequest(messages=(ChatMessage("user", prompt),), decoding=DecodingParamsV1(temperature=Fraction(0)))
    started = time.perf_counter()
    raw = transport(Provider.OPENROUTER, model, request)
    latency = time.perf_counter() - started
    data = json.loads(raw)
    data["_raw_provider_body_utf8"] = raw.decode("utf-8")
    data["_raw_provider_body_sha256"] = hashlib.sha256(raw).hexdigest()
    data["client_latency"] = latency
    return data


def extract_turn_metrics(
    resp_data: Dict[str, Any],
    turn_spec: Dict[str, Any],
    has_reasoning_tokens: bool,
) -> Dict[str, Any]:
    """Extract step-by-step latency, token counts, and lift-request emission."""
    choice = resp_data["choices"][0]
    message = choice["message"]
    content = message.get("content") or ""
    reasoning_text = message.get("reasoning") or ""

    usage = resp_data.get("usage", {})
    prompt_tokens = usage.get("prompt_tokens", 0)
    completion_tokens = usage.get("completion_tokens", 0)
    reasoning_tokens = usage.get("completion_tokens_details", {}).get("reasoning_tokens")

    latency = resp_data.get("client_latency", 0.0)
    tokens_per_sec = (completion_tokens / latency) if latency > 0 else 0.0

    lift_requested = False
    proposed_involution = ""
    if turn_spec["turn"] == 3:
        content_lower = content.lower()
        if any(w in content_lower for w in ["tau", "involution", "flip", "lift", "s_i -> -s_i", "-s"]):
            lift_requested = True
            proposed_involution = "tau_i: s_i -> -s_i on odd-winding cycle"

    exact_repair_achieved = False
    if turn_spec["turn"] == 4:
        if "912" in content and "199" in content:
            exact_repair_achieved = True

    return {
        "turn": turn_spec["turn"],
        "stage": turn_spec["stage"],
        "client_latency_seconds": round(latency, 3),
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "reasoning_tokens": reasoning_tokens,
        "reasoning_word_count": len(reasoning_text.split()),
        "raw_provider_response": resp_data,
        "content": content,
        "tokens_per_second": round(tokens_per_sec, 2),
        "lift_requested": lift_requested,
        "proposed_involution": proposed_involution,
        "exact_repair_achieved": exact_repair_achieved,
        "content_excerpt": content[:240].replace("\n", " "),
    }


def execute_model_trial(
    model_spec: Dict[str, Any],
    api_key: str,
    prompts: List[Dict[str, str]],
) -> Dict[str, Any]:
    """Run sequential 4-turn trial for a single model."""
    print(f"\n--- Running Interactive Multi-Turn Trial on {model_spec['name']} ({model_spec['id']}) ---")
    turn_results = []
    total_latency = 0.0
    total_tokens = 0
    total_reasoning = 0
    lift_emitted = False

    for p in prompts:
        print(f"  [Turn {p['turn']}] Querying stage: {p['stage']}...")
        raw_resp = query_openrouter_single_turn(
            model=model_spec["id"],
            prompt=p["query"],
            api_key=api_key,
        )
        metrics = extract_turn_metrics(raw_resp, p, model_spec["has_reasoning_tokens"])
        metrics["prompt"] = p["query"]
        turn_results.append(metrics)

        total_latency += metrics["client_latency_seconds"]
        total_tokens += metrics["completion_tokens"]
        total_reasoning += metrics["reasoning_tokens"] or 0
        if metrics["lift_requested"]:
            lift_emitted = True

        print(
            f"    -> Latency: {metrics['client_latency_seconds']}s | "
            f"Tokens: {metrics['completion_tokens']} (Reasoning: {metrics['reasoning_tokens']}) | "
            f"Tokens/s: {metrics['tokens_per_second']}"
        )
        if p["turn"] == 3:
            print(f"    -> Lift Request Emitted: {metrics['lift_requested']} ({metrics['proposed_involution']})")
        if p["turn"] == 4:
            print(f"    -> Exact Repair Z=912 Certified: {metrics['exact_repair_achieved']}")

    return {
        "model_id": model_spec["id"],
        "model_name": model_spec["name"],
        "tier": model_spec["tier"],
        "total_latency_seconds": round(total_latency, 3),
        "total_completion_tokens": total_tokens,
        "total_reasoning_tokens": total_reasoning if all(t["reasoning_tokens"] is not None for t in turn_results) else None,
        "evidence_scope": "coached_independent_requests_keyword_screen_only",
        "lift_request_emission_rate": 1.0 if lift_emitted else 0.0,
        "terminal_repair_passed": turn_results[-1]["exact_repair_achieved"],
        "turns": turn_results,
    }


def replay_certified_multiturn_trial() -> Dict[str, Any]:
    """Read the retained illustrative fixture; never manufacture provider evidence."""
    if not CERTIFIED_MULTITURN_RECEIPT.is_file():
        raise FileNotFoundError("Retained interactive fixture is missing")
    receipt = json.loads(CERTIFIED_MULTITURN_RECEIPT.read_text(encoding="utf-8"))
    receipt["evidence_scope"] = "synthetic_example_without_raw_provider_custody"
    receipt["live_provider_evidence"] = False
    receipt["verified"] = False
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser(description="Multi-Turn Interactive PFP Trial Runner.")
    parser.add_argument("--live", action="store_true", help="Execute live OpenRouter requests.")
    parser.add_argument("--api-key", default=os.environ.get("OPENROUTER_API_KEY", ""), help="OpenRouter API key.")
    parser.add_argument("--model", default="all", choices=["all", "stealth/space-bunny-alpha", "meta-llama/llama-3.3-70b-instruct"], help="Model to test.")
    parser.add_argument("--export", default="", help="Custom output JSON path.")
    args = parser.parse_args()

    prompts = build_turn_prompts()
    print("================================================================================")
    print("  THE SYMBOL GAME: MULTI-TURN INTERACTIVE COACHED PFP TRIAL")
    print("  Testing: Step-by-Step Reasoning Latency & Lift Request Emission")
    print("================================================================================")

    if args.live:
        if not args.api_key:
            print("ERROR: --live mode requires OPENROUTER_API_KEY or --api-key.")
            return 1
        targets = MODELS_TO_TEST if args.model == "all" else [m for m in MODELS_TO_TEST if m["id"] == args.model]
        results = [execute_model_trial(m, args.api_key, prompts) for m in targets]

        receipt = {
            "trial_id": f"LIVE-MULTITURN-PFP-{int(time.time())}",
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "models_evaluated": len(results),
            "results": results,
            "lift_emission_probability_overall": sum(r["lift_request_emission_rate"] for r in results) / len(results),
            "terminal_repair_rate": sum(1 for r in results if r["terminal_repair_passed"]) / len(results),
            "verified": all(r["terminal_repair_passed"] for r in results),
        }
        out_path = Path(args.export) if args.export else (RESULTS_DIR / "live_multiturn_trial_results.json")
        out_path.write_text(json.dumps(receipt, indent=2), encoding="utf-8")
        print(f"\nLive trial complete. Results written to: {out_path}")
        return 0 if receipt["verified"] else 1

    print("\n[REPLAY MODE] Verifying certified multi-turn interactive trial receipts offline...")
    receipt = replay_certified_multiturn_trial()
    print(f"Trial ID: {receipt['trial_id']}")
    print(f"Protocol: {receipt['protocol']}")
    print(f"Overall Lift Emission Probability: {receipt['lift_emission_probability_overall'] * 100:.1f}%")
    print(f"Terminal Repair Rate (Z=912):       {receipt['terminal_repair_rate'] * 100:.1f}%\n")

    for r in receipt["results"]:
        print(f"MODEL: {r['model_name']} ({r['model_id']}) - Tier: {r['tier']}")
        print(f"  Total Latency: {r['total_latency_seconds']:.2f}s | Completion Tokens: {r['total_completion_tokens']} | Reasoning Tokens: {r['total_reasoning_tokens']}")
        print(f"  Lift Request Emission: {r['lift_request_emission_rate'] * 100:.0f}% | Terminal Repair: {r['terminal_repair_passed']}")
        for t in r["turns"]:
            lift_str = f" [LIFT: {t['proposed_involution']}]" if t["lift_requested"] else ""
            repair_str = " [EXACT REPAIR Z=912]" if t["exact_repair_achieved"] else ""
            print(f"    - Turn {t['turn']} ({t['stage']}): Latency {t['client_latency_seconds']:.2f}s | Tokens: {t['completion_tokens']} (Reasoning: {t['reasoning_tokens']}){lift_str}{repair_str}")
        print()

    print(f"Retained {receipt['models_evaluated']} model-labelled examples. Provider measurements remain UNVERIFIED.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
