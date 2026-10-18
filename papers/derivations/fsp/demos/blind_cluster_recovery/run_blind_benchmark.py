#!/usr/bin/env python3
"""
run_blind_benchmark.py — Multi-Model Blind Cluster Recovery Benchmark Harness

Evaluates 5 experimental arms across multiple model scales on OpenRouter:
  - 70B Scale: meta-llama/llama-3.3-70b-instruct
  - ~500B MoE: deepseek/deepseek-v4-flash-0731 & z-ai/glm-5.3-flash
  - 770B MoE: tencent/hy4-preview
  - 1T+ Frontier: qwen/qwen3.7-max

AuthorityEffect: None.
Firewall: Strict lexical hygiene; zero physics keywords; configured-price ceiling $1.50.
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import os
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from omega_engine_projects.fsp.demos.blind_cluster_recovery.antibody_miner import (
    AntibodyMiner,
)
from omega_engine_projects.fsp.demos.blind_cluster_recovery.blind_problem import (
    assert_lexical_hygiene,
    generate_blind_problem_packet,
)
from omega_engine_projects.fsp.demos.blind_cluster_recovery.oracle import (
    BlindClusterOracle,
)
from omega_engine_projects.fsp.demos.blind_cluster_recovery.prompt_builder import (
    JSON_SCHEMA_ARM1,
    build_prompt_arm1_constrained_decoding,
    build_prompt_arm2_attention_masking,
    build_prompt_arm3_hieroglyphics,
    build_prompt_arm4_immune_round,
    build_prompt_arm5_hybrid,
)

MODEL_PRICING = {
    "meta-llama/llama-3.3-70b-instruct": (0.12, 0.30),
    "deepseek/deepseek-v4-flash-0731": (0.04, 0.10),
    "z-ai/glm-5.3-flash": (0.075, 0.25),
    "tencent/hy4-preview": (0.30, 0.60),
    "qwen/qwen3.7-max": (0.40, 1.20),
}


class BudgetExceededError(RuntimeError):
    """Raised before a request that could exceed the configured spend ceiling."""


class BudgetGuard:
    """Enforce a configured-price ceiling using conservative request reservations."""

    def __init__(self, ceiling_usd: float = 1.50) -> None:
        if ceiling_usd <= 0:
            raise ValueError("ceiling_usd must be positive")
        self.ceiling_usd = ceiling_usd
        self.total_spent = 0.0
        self.reserved_usd = 0.0
        self.call_history: list[dict] = []

    def reserve_call(self, model: str, prompt: str, max_output_tokens: int) -> float:
        """Reserve a byte-bounded worst-case request cost before network I/O."""
        p_in, p_out = MODEL_PRICING.get(model, (0.20, 0.60))
        input_token_bound = len(prompt.encode("utf-8"))
        reservation = (input_token_bound * p_in + max_output_tokens * p_out) / 1e6
        projected = self.total_spent + self.reserved_usd + reservation
        if projected > self.ceiling_usd:
            raise BudgetExceededError(
                "BUDGET CEILING: refusing request because the configured-price "
                f"upper bound ${projected:.4f} exceeds ${self.ceiling_usd:.2f}."
            )
        self.reserved_usd += reservation
        return reservation

    def record_call(
        self,
        model: str,
        in_tok: int,
        out_tok: int,
        latency: float,
        reservation: float,
    ) -> float:
        p_in, p_out = MODEL_PRICING.get(model, (0.20, 0.60))
        cost = (in_tok * p_in + out_tok * p_out) / 1e6
        self.reserved_usd = max(0.0, self.reserved_usd - reservation)
        self.total_spent += cost
        self.call_history.append(
            {
                "model": model,
                "in_tokens": in_tok,
                "out_tokens": out_tok,
                "latency_sec": latency,
                "cost_usd": cost,
                "cumulative_spent_usd": self.total_spent,
            }
        )
        if self.total_spent + self.reserved_usd > self.ceiling_usd:
            raise BudgetExceededError(
                f"BUDGET CEILING BREACH: accounted spend ${self.total_spent:.4f} "
                f"exceeds configured ceiling ${self.ceiling_usd:.2f}."
            )
        return cost


def query_openrouter(
    model: str,
    prompt: str,
    api_key: str,
    budget_guard: BudgetGuard,
    dry_run: bool = False,
    response_schema: dict | None = None,
    max_retries: int = 2,
) -> tuple[str, dict]:
    """Execute a single model query against OpenRouter API with retries and bounds."""
    assert_lexical_hygiene(prompt)

    if dry_run:
        mock_response = json.dumps(
            {
                "cycle_independence": True,
                "cycle_parity_invariant_found": True,
                "cancellation_mechanism": "Flipping any odd cycle inverts global sign, forcing 1 + (-1) = 0 cancellation.",
                "zero_odd_sector_subgraphs": 199,
                "exact_partition_z": 912,
                "scratchpad": "Dry run mock scratchpad: 199 zero-meron graphs sum to 912.",
            }
        )
        return mock_response, {"in_tokens": 100, "out_tokens": 50, "cost": 0.0, "latency": 0.05}

    try:
        import requests
    except ImportError as exc:
        raise RuntimeError(
            'Live runs require the benchmark dependencies: pip install -e ".[bench]"'
        ) from exc

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/dbccpage/the_symbol_game",
        "X-Title": "Symbol Game Blind Cluster Recovery",
    }

    body = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2,
        "max_tokens": 3000,
    }

    if response_schema:
        body["response_format"] = {
            "type": "json_schema",
            "json_schema": {
                "name": "cluster_recovery_solution",
                "strict": True,
                "schema": response_schema,
            },
        }

    last_err = None
    for attempt in range(max_retries + 1):
        reservation = budget_guard.reserve_call(
            model=model,
            prompt=prompt,
            max_output_tokens=body["max_tokens"],
        )
        try:
            t0 = time.time()
            resp = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=body,
                timeout=(15, 60),
            )
            latency = time.time() - t0

            if resp.status_code != 200:
                raise RuntimeError(f"OpenRouter API error {resp.status_code}: {resp.text[:300]}")

            data = resp.json()
            msg = data["choices"][0]["message"]
            content = msg.get("content") or msg.get("reasoning") or ""
            usage = data.get("usage", {})
            in_tok = (
                usage.get("prompt_tokens")
                if usage.get("prompt_tokens") is not None
                else (len(prompt) // 4)
            )
            out_tok = (
                usage.get("completion_tokens")
                if usage.get("completion_tokens") is not None
                else (len(content) // 4)
            )

            cost = budget_guard.record_call(model, in_tok, out_tok, latency, reservation)
            return content, {
                "in_tokens": in_tok,
                "out_tokens": out_tok,
                "cost": cost,
                "latency": latency,
            }
        except BudgetExceededError:
            raise
        except Exception as e:
            last_err = e
            if attempt < max_retries:
                print(f"      [Retry {attempt + 1}/{max_retries}] due to: {e}", flush=True)
                time.sleep(2)
            else:
                raise last_err from None


def collect_runtime_errors(value: object, path: str = "arms") -> list[str]:
    """Collect harness/runtime errors without treating model parse failures as crashes."""
    errors: list[str] = []
    if isinstance(value, dict):
        error = value.get("error")
        if isinstance(error, str):
            errors.append(f"{path}: {error}")
        for key, nested in value.items():
            if key != "error":
                errors.extend(collect_runtime_errors(nested, f"{path}.{key}"))
    elif isinstance(value, list):
        for index, nested in enumerate(value):
            errors.extend(collect_runtime_errors(nested, f"{path}[{index}]"))
    return errors


def load_api_key(env_file: Path | None) -> str:
    """Load an explicitly requested dotenv file, then read the provider key."""
    if env_file is not None:
        try:
            from dotenv import load_dotenv
        except ImportError as exc:
            raise RuntimeError(
                'Using --env-file requires the benchmark dependencies: pip install -e ".[bench]"'
            ) from exc
        load_dotenv(env_file)
    return os.getenv("OPENROUTER_API_KEY", "")


def write_json(path: Path, value: object) -> bytes:
    """Write deterministic UTF-8/LF JSON and return the exact artifact bytes."""
    payload = json.dumps(value, indent=2, sort_keys=True).encode("utf-8")
    path.write_bytes(payload)
    return payload


def run_arm1_baseline(
    models: list[str],
    packet: dict,
    miner: AntibodyMiner,
    api_key: str,
    budget: BudgetGuard,
    dry_run: bool,
) -> dict:
    """Run Arm 1: Constrained JSON Decoding."""
    prompt = build_prompt_arm1_constrained_decoding(packet)
    results = {}

    for model in models:
        print(f"  [Arm 1: Constrained JSON] Running {model}...")
        try:
            raw_text, meta = query_openrouter(
                model=model,
                prompt=prompt,
                api_key=api_key,
                budget_guard=budget,
                dry_run=dry_run,
                response_schema=JSON_SCHEMA_ARM1,
            )
            eval_res, _ = miner.evaluate_and_mine(raw_text, [])
            results[model] = {
                "score": eval_res["score"],
                "perfect": eval_res["perfect"],
                "feedback": eval_res["feedback"],
                "metadata": meta,
                "parsed": miner.parse_proposer_response(raw_text),
            }
            print(
                f"    => Score: {eval_res['score']}/4 | Cost: ${meta['cost']:.5f} | Latency: {meta['latency']:.1f}s"
            )
        except Exception as e:
            print(f"    => Error: {e}")
            results[model] = {"error": str(e)}

    return results


def run_arm2_attention_masking(
    models: list[str],
    packet: dict,
    miner: AntibodyMiner,
    api_key: str,
    budget: BudgetGuard,
    dry_run: bool,
) -> dict:
    """Run Arm 2: Attention Distractor-Key Masking."""
    prompt = build_prompt_arm2_attention_masking(packet)
    results = {}

    for model in models:
        print(f"  [Arm 2: Distractor Masking] Running {model}...")
        try:
            raw_text, meta = query_openrouter(
                model=model,
                prompt=prompt,
                api_key=api_key,
                budget_guard=budget,
                dry_run=dry_run,
                response_schema=JSON_SCHEMA_ARM1,
            )
            eval_res, _ = miner.evaluate_and_mine(raw_text, [])
            results[model] = {
                "score": eval_res["score"],
                "perfect": eval_res["perfect"],
                "feedback": eval_res["feedback"],
                "metadata": meta,
                "parsed": miner.parse_proposer_response(raw_text),
            }
            print(
                f"    => Score: {eval_res['score']}/4 | Cost: ${meta['cost']:.5f} | Latency: {meta['latency']:.1f}s"
            )
        except Exception as e:
            print(f"    => Error: {e}")
            results[model] = {"error": str(e)}

    return results


def run_arm3_hieroglyphics(
    models: list[str],
    packet: dict,
    miner: AntibodyMiner,
    api_key: str,
    budget: BudgetGuard,
    dry_run: bool,
) -> dict:
    """Run Arm 3: DDC Hieroglyphic Factorization."""
    prompt = build_prompt_arm3_hieroglyphics(packet)
    results = {}

    for model in models:
        print(f"  [Arm 3: DDC Hieroglyphics] Running {model}...")
        try:
            raw_text, meta = query_openrouter(
                model=model,
                prompt=prompt,
                api_key=api_key,
                budget_guard=budget,
                dry_run=dry_run,
                response_schema=JSON_SCHEMA_ARM1,
            )
            eval_res, _ = miner.evaluate_and_mine(raw_text, [])
            results[model] = {
                "score": eval_res["score"],
                "perfect": eval_res["perfect"],
                "feedback": eval_res["feedback"],
                "metadata": meta,
                "parsed": miner.parse_proposer_response(raw_text),
            }
            print(
                f"    => Score: {eval_res['score']}/4 | Cost: ${meta['cost']:.5f} | Latency: {meta['latency']:.1f}s"
            )
        except Exception as e:
            print(f"    => Error: {e}")
            results[model] = {"error": str(e)}

    return results


def run_arm4_immune_loop(
    model: str,
    max_rounds: int,
    packet: dict,
    miner: AntibodyMiner,
    api_key: str,
    budget: BudgetGuard,
    dry_run: bool,
) -> dict:
    """Run Arm 4: Multi-Round Typed Input/Output with Self-Selected Lifts & Antibody Mining."""
    print(f"  [Arm 4: {max_rounds}-Round Immune Mining] Running {model}...")
    antibodies = []
    round_history = []
    converged = False
    total_cost = 0.0

    for rnd in range(1, max_rounds + 1):
        prompt = build_prompt_arm4_immune_round(packet, rnd, antibodies)
        try:
            raw_text, meta = query_openrouter(
                model=model,
                prompt=prompt,
                api_key=api_key,
                budget_guard=budget,
                dry_run=dry_run,
                response_schema=JSON_SCHEMA_ARM1,
            )
            total_cost += meta["cost"]
            eval_res, new_antibodies = miner.evaluate_and_mine(raw_text, antibodies)

            round_entry = {
                "round": rnd,
                "score": eval_res["score"],
                "perfect": eval_res["perfect"],
                "new_antibodies_mined": len(new_antibodies) - len(antibodies),
                "total_antibodies": len(new_antibodies),
                "feedback": eval_res["feedback"],
                "metadata": meta,
            }
            round_history.append(round_entry)
            antibodies = new_antibodies

            print(
                f"    Round {rnd}/{max_rounds}: Score {eval_res['score']}/4 | New Antibodies: {round_entry['new_antibodies_mined']} | Cost: ${meta['cost']:.5f}"
            )

            if eval_res["perfect"]:
                converged = True
                print(f"    >>> CONVERGED at Round {rnd} with perfect 4/4! <<<")
                break

        except Exception as e:
            print(f"    Round {rnd} Error: {e}")
            round_history.append({"round": rnd, "error": str(e)})
            break

    return {
        "model": model,
        "converged": converged,
        "rounds_executed": len(round_history),
        "final_score": round_history[-1].get("score", 0) if round_history else 0,
        "total_cost": total_cost,
        "history": round_history,
        "final_antibodies": antibodies,
    }


def run_arm5_hybrid(
    models: list[str],
    packet: dict,
    miner: AntibodyMiner,
    api_key: str,
    budget: BudgetGuard,
    dry_run: bool,
    accumulated_antibodies: list[dict],
) -> dict:
    """Run Arm 5: Full Hybrid (Hieroglyphics + Distractor Masking + Scratchpad + Antibodies)."""
    prompt = build_prompt_arm5_hybrid(packet, accumulated_antibodies)
    results = {}

    for model in models:
        print(f"  [Arm 5: Full Hybrid] Running {model}...")
        try:
            raw_text, meta = query_openrouter(
                model=model,
                prompt=prompt,
                api_key=api_key,
                budget_guard=budget,
                dry_run=dry_run,
                response_schema=JSON_SCHEMA_ARM1,
            )
            eval_res, _ = miner.evaluate_and_mine(raw_text, accumulated_antibodies)
            results[model] = {
                "score": eval_res["score"],
                "perfect": eval_res["perfect"],
                "feedback": eval_res["feedback"],
                "metadata": meta,
                "parsed": miner.parse_proposer_response(raw_text),
            }
            print(
                f"    => Score: {eval_res['score']}/4 | Cost: ${meta['cost']:.5f} | Latency: {meta['latency']:.1f}s"
            )
        except Exception as e:
            print(f"    => Error: {e}")
            results[model] = {"error": str(e)}

    return results


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(line_buffering=True)
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(line_buffering=True)

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dry-run", action="store_true", help="Run harness with mock responses (no API spend)"
    )
    parser.add_argument(
        "--max-rounds", type=int, default=5, help="Max immune mining rounds for Arm 4"
    )
    parser.add_argument(
        "--budget-ceiling",
        type=float,
        default=1.50,
        help="Configured-price ceiling in USD",
    )
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).parent / "results")
    parser.add_argument(
        "--env-file",
        type=Path,
        default=None,
        help="Optional dotenv file containing OPENROUTER_API_KEY",
    )
    args = parser.parse_args()

    api_key = "" if args.dry_run else load_api_key(args.env_file)

    if not args.dry_run and not api_key:
        print("ERROR: OPENROUTER_API_KEY not found in environment or .env file.")
        sys.exit(1)

    budget = BudgetGuard(ceiling_usd=args.budget_ceiling)
    oracle = BlindClusterOracle()
    miner = AntibodyMiner(oracle)
    packet = generate_blind_problem_packet()

    args.output_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 70)
    print("SYMBOL GAME BLIND CLUSTER RECOVERY BENCHMARK")
    print(f"  Mode: {'DRY RUN (Mock API)' if args.dry_run else 'LIVE OPENROUTER RUN'}")
    print(f"  Budget Ceiling: ${args.budget_ceiling:.2f}")
    print("  Lexical Hygiene: VERIFIED (0 domain keywords leaked)")
    print("=" * 70)

    models_tier1_2 = [
        "meta-llama/llama-3.3-70b-instruct",
        "deepseek/deepseek-v4-flash-0731",
        "z-ai/glm-5.3-flash",
    ]
    frontier_models = [
        "meta-llama/llama-3.3-70b-instruct",
        "tencent/hy4-preview",
        "qwen/qwen3.7-max",
    ]

    master_report = {
        "timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "authority_effect": "None",
        "dry_run": args.dry_run,
        "oracle_ground_truth": {
            "signed_Z": oracle.signed_partition,
            "absolute_Z": oracle.absolute_partition,
            "average_sign": oracle.average_sign,
            "zero_odd_sector_subgraphs": oracle.zero_charge_subgraphs,
        },
        "arms": {},
    }

    print("\n--- PHASE 1: ARM 1 (Constrained JSON Decoding) ---")
    master_report["arms"]["arm1_constrained"] = run_arm1_baseline(
        models_tier1_2, packet, miner, api_key, budget, args.dry_run
    )

    print("\n--- PHASE 2: ARM 2 (Attention Distractor-Key Masking) ---")
    master_report["arms"]["arm2_attention_masking"] = run_arm2_attention_masking(
        models_tier1_2, packet, miner, api_key, budget, args.dry_run
    )

    print("\n--- PHASE 3: ARM 3 (DDC Hieroglyphic Factorization) ---")
    master_report["arms"]["arm3_hieroglyphics"] = run_arm3_hieroglyphics(
        models_tier1_2, packet, miner, api_key, budget, args.dry_run
    )

    print("\n--- PHASE 4: ARM 4 (Multi-Round Immune Mining) ---")
    arm4_results = {}
    for m in [
        "meta-llama/llama-3.3-70b-instruct",
        "deepseek/deepseek-v4-flash-0731",
        "z-ai/glm-5.3-flash",
    ]:
        arm4_results[m] = run_arm4_immune_loop(
            model=m,
            max_rounds=args.max_rounds,
            packet=packet,
            miner=miner,
            api_key=api_key,
            budget=budget,
            dry_run=args.dry_run,
        )
    master_report["arms"]["arm4_immune_mining"] = arm4_results

    accumulated_abs = []
    for r in arm4_results.values():
        for ab in r.get("final_antibodies", []):
            if ab["code"] not in {a["code"] for a in accumulated_abs}:
                accumulated_abs.append(ab)

    print("\n--- PHASE 5: ARM 5 (Full Hybrid on Frontier Models) ---")
    master_report["arms"]["arm5_hybrid"] = run_arm5_hybrid(
        frontier_models, packet, miner, api_key, budget, args.dry_run, accumulated_abs
    )

    master_report["budget_summary"] = {
        "total_calls": len(budget.call_history),
        "total_spent_usd": budget.total_spent,
        "unsettled_reservation_usd": budget.reserved_usd,
        "ceiling_usd": budget.ceiling_usd,
        "call_history": budget.call_history,
    }

    runtime_errors = collect_runtime_errors(master_report["arms"])
    execution_status = "PASS" if not runtime_errors else "INCOMPLETE"
    master_report["execution_summary"] = {
        "status": execution_status,
        "status_scope": "harness_execution",
        "runtime_error_count": len(runtime_errors),
        "runtime_errors": runtime_errors,
    }

    report_path = args.output_dir / "master_evaluation_report.json"
    summary_path = args.output_dir / "summary.json"
    receipt_path = args.output_dir / "receipt.json"

    report_bytes = write_json(report_path, master_report)

    summary_data = {
        "timestamp_utc": master_report["timestamp_utc"],
        "total_spent_usd": budget.total_spent,
        "total_calls": len(budget.call_history),
        "arms_evaluated": list(master_report["arms"].keys()),
        "oracle_target_Z": oracle.signed_partition,
        "status": execution_status,
        "status_scope": "harness_execution",
        "runtime_error_count": len(runtime_errors),
    }
    write_json(summary_path, summary_data)

    receipt_data = {
        "receipt_id": f"REC_FSP_BLIND_{int(time.time())}",
        "authority_effect": "None",
        "sha256": hashlib.sha256(report_bytes).hexdigest(),
        "total_spent": budget.total_spent,
        "status": execution_status,
        "status_scope": "harness_execution",
        "runtime_error_count": len(runtime_errors),
    }
    write_json(receipt_path, receipt_data)

    print("\n" + "=" * 70)
    print("BENCHMARK EXECUTION SUMMARY")
    print(f"  Total API Calls:     {len(budget.call_history)}")
    print(f"  Total Cost Incurred: ${budget.total_spent:.5f}")
    print(f"  Report written to:   {report_path}")
    print(f"  Summary written to:  {summary_path}")
    print(f"  Receipt written to:  {receipt_path}")
    print("=" * 70)


if __name__ == "__main__":
    main()
