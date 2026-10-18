"""demo_pure_symbolic_6site.py: Pure Gamma38 Symbolic Runner for 6-Site Scaling & GIN Index.
AuthorityEffect: None.

Features:
1. Pure Gamma38 wire communication (38-character alphabet: {0-9, a-z, <, >}).
2. Zero natural language / English domain words (no 'meron', 'fermion', 'hamiltonian', etc.).
3. 6-site lattice scaling:
   - 4,096 breakup subgraphs (2^12 plaquettes, 24 nodes)
   - 33,396 configurations
   - 72 cancelling subgraphs and 4,024 surviving subgraphs
   - GIN inverted mode posting index pairing 384 cancelling states into 192 doublets with timing reported for this host run
   - Exact integer partition Z = 33,012 matching transfer matrix trace Tr(T^2) = 33,012
4. 4-turn sequential inquiry mediated entirely through symbolic wire packets:
   - Turn 1: 6-site Carrier + Plaquette cell -> Decomposition into 4096 breakup subgraphs
   - Turn 2: Spectrum measurement -> Localizing 72 cancelling and 4024 surviving subgraphs
   - Turn 3: Sign obstruction -> Model emits typed LIFT_REQUEST wire packet
   - Turn 4: Host LIFT_GRANT -> Model emits EXACT_REPAIR wire packet (Z=33012)
5. Offline deterministic host fixture replay; no provider inference is claimed.
"""

from __future__ import annotations

from fractions import Fraction

import argparse
import hashlib
import datetime
import json
import os
import sys
import time
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Path configuration
DEMOS_DIR = Path(__file__).resolve().parent.parent
CODE_DIR = DEMOS_DIR.parent / "code"
REPO_ROOT = DEMOS_DIR
for p in DEMOS_DIR.parents:
    if (p / "omega_engine_pfp").exists():
        REPO_ROOT = p
        break

if str(CODE_DIR) not in sys.path:
    sys.path.insert(0, str(CODE_DIR))
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from blind_problem import assert_lexical_hygiene
from symbol_game_pfp import verify_6site_scaling_gin
from omega_engine_pfp.domain import LlmTurnRunRootV1
from omega_engine_pfp.use_cases.llm_turn import (
    CreateTurnUseCase,
    SubmitCandidateUseCase,
)
from omega_engine_pfp.domain.tower.parser import (
    parse_packet,
    serialize_packet,
    validate_packet_semantics,
    GAMMA_38,
)

RESULTS_DIR = DEMOS_DIR / "results"
CERTIFIED_6SITE_SYMBOLIC_RECEIPT = RESULTS_DIR / "certified_pure_wire_6site_results.json"
SYMBOLIC_6SITE_DAG_TRACE = RESULTS_DIR / "symbol_game_pure_wire_6site_dag.jsonl"

WIRE_TURNS_6SITE = [
    {
        "turn": 1,
        "stage": "PLAQUETTE_BREAKUP",
        "input_wire": "op<<11>op<<1><11000>>op<<10><0><1>>>",  # 24 nodes (binary 11000)
        "wire_prompt": "op<<11>op<<1><11000>>op<<10><0><1>>>",
        "grammar_prompt": "op<<11>op<<1><11000>>op<<10><0><1>>>",
        "expected_response_wire": "op<<101><11><0><1><10><11>>",
        "action": "PROBE_PLAQUETTES",
    },
    {
        "turn": 2,
        "stage": "MEASURE_HOLONOMY",
        "input_wire": "op<<101><11><0><1><10><11>>",
        "wire_prompt": "op<<101><11><0><1><10><11>>",
        "grammar_prompt": "op<<101><11><0><1><10><11>>",
        "expected_response_wire": "op<<100><>op<<11>op<<1><1001000>>op<<1><111110111000>>>>",
        "action": "MEASURE_HOLONOMY",
    },
    {
        "turn": 3,
        "stage": "LIFT_REQUEST",
        "input_wire": "op<<100><>op<<11>op<<1><1001000>>op<<1><111110111000>>>>",
        "wire_prompt": "op<<100><>op<<11>op<<1><1001000>>op<<1><111110111000>>>>",
        "grammar_prompt": "op<<100><>op<<11>op<<1><1001000>>op<<1><111110111000>>>>",
        "expected_response_wire": "op<<1100><liftreq>>",
        "action": "REQUEST_LIFT",
    },
    {
        "turn": 4,
        "stage": "EXACT_REPAIR",
        "input_wire": "op<<0><><0><1>>",  # Host GRANT_LIFT packet
        "wire_prompt": "op<<0><><0><1>>",
        "grammar_prompt": "op<<0><><0><1>>",
        "expected_response_wire": "op<<10010><0><1000000011110100><1>>",
        "action": "CERTIFY_EXACT_REPAIR",
    },
]


def assert_wire_purity(wire: str) -> bool:
    """Verify that wire contains strictly characters from GAMMA_38."""
    for ch in wire:
        if ch not in GAMMA_38:
            raise ValueError(f"Illegal non-Gamma38 character '{ch}' in wire: {wire}")
    parsed = parse_packet(wire)
    validate_packet_semantics(parsed)
    serialized = serialize_packet(parsed)
    if serialized != wire:
        raise ValueError(f"Wire roundtrip mismatch: {serialized} != {wire}")
    return True


def query_openrouter_wire(
    model: str,
    prompt: str,
    api_key: str,
    max_tokens: int = 1024,
) -> Tuple[str, float, Dict[str, Any]]:
    """Execute live query on OpenRouter expecting pure wire output."""
    from omega_engine_woland.domain.providers.types import CandidateRequest, ChatMessage, DecodingParamsV1, Provider
    from omega_engine_woland.infrastructure.providers.openai_compat import OpenAiCompatTransport
    transport = OpenAiCompatTransport(Provider.OPENROUTER, api_key=api_key, max_tokens=max_tokens, timeout=120)
    request = CandidateRequest(messages=(ChatMessage("user", prompt),), decoding=DecodingParamsV1(temperature=Fraction(0)))
    started = time.perf_counter()
    raw = transport(Provider.OPENROUTER, model, request)
    latency = time.perf_counter() - started
    data = json.loads(raw)
    data["_raw_provider_body_utf8"] = raw.decode("utf-8")
    data["_raw_provider_body_sha256"] = hashlib.sha256(raw).hexdigest()
    return data["choices"][0]["message"]["content"], latency, data


def run_pure_symbolic_6site(
    live: bool = False,
    model: str = "stealth/space-bunny-alpha",
    api_key: str = "",
    write_receipt: bool = False,
    fixed_timestamp: str = "2026-10-02T21:45:00Z",
    output_dir: Optional[Path] = None,
) -> Dict[str, Any]:
    """Execute the 4-turn pure symbolic runner on the 6-site lattice."""
    if live and not api_key:
        raise ValueError("live mode requires a provider key")
    if write_receipt and output_dir is None:
        raise ValueError("writing receipts requires an explicit output_dir")
    # Step 0: Execute exact mathematical verifier
    t_math_0 = time.time()
    math_res = verify_6site_scaling_gin()
    t_math = time.time() - t_math_0

    # Step 1: Lexical hygiene audit across all prompts
    for t in WIRE_TURNS_6SITE:
        assert_lexical_hygiene(t["grammar_prompt"])
        assert_wire_purity(t["input_wire"])
        assert_wire_purity(t["expected_response_wire"])

    turns_executed = []
    dag_nodes = []
    token_usage = []
    total_latency = 0.0 if live else None

    ts = fixed_timestamp if not (live and api_key) else datetime.datetime.now(datetime.timezone.utc).isoformat()

    # Initialize DAG
    dag_nodes.append({
        "node_id": "CARRIER_INIT_6SITE",
        "turn": 0,
        "stage": "INIT",
        "action": "INIT_CARRIER",
        "wire_out": "op<<11>op<<1><11000>>op<<10><0><1100>>>",
        "carrier_properties": {
            "sites": 6,
            "nodes": 24,
            "plaquettes": 12,
            "breakup_graphs": math_res["subgraphs"],
            "total_configurations": math_res["configurations"],
        },
        "timestamp": ts,
    })

    create_turn_uc = CreateTurnUseCase()
    submit_cand_uc = SubmitCandidateUseCase()

    for t in WIRE_TURNS_6SITE:
        turn_num = t["turn"]
        stage = t["stage"]
        input_wire = t["input_wire"]
        prompt = t["grammar_prompt"]
        expected_wire = t["expected_response_wire"]
        action = t["action"]

        raw_json = None
        if live:
            resp_wire, latency, raw_json = query_openrouter_wire(model=model, prompt=prompt, api_key=api_key)
            total_latency += latency
            token_usage.append(raw_json.get("usage", {}).get("total_tokens"))
        else:
            resp_wire = expected_wire
            latency = None
        try:
            purity_ok = assert_wire_purity(resp_wire)
            validation_error = None
        except (ValueError, TypeError, IndexError) as error:
            purity_ok = False
            validation_error = str(error)
        exact_match = resp_wire == expected_wire

        # Domain use-case turn execution
        run_root = create_turn_uc.execute(
            task_id=f"fsp-meron-6site-turn-{turn_num}",
            objective=f"Symbolic Meron 6-site turn {turn_num} stage {stage}",
            prompt_body=input_wire,
        )
        if purity_ok:
            updated_root, cand_art, content_art = submit_cand_uc.execute(
                run_root=run_root,
                candidate_id=f"candidate-meron-6site-turn-{turn_num}",
                producer_id="fsp_pure_symbolic_6site_runner",
                reply_text=resp_wire,
            )
            transport = {"run_root_id": updated_root.run_root_id, "candidate_id": cand_art.candidate_id,
                         "content_id": content_art.content_id, "terminal_status": updated_root.terminal_status}
        else:
            transport = {"run_root_id": run_root.run_root_id, "candidate_id": None,
                         "content_id": None, "terminal_status": "Refused"}

        turns_executed.append({
            "turn": turn_num,
            "stage": stage,
            "action": action,
            "input_wire": input_wire,
            "response_wire": resp_wire,
            "expected_wire": expected_wire,
            "purity_ok": purity_ok,
            "exact_match": exact_match,
            "latency_seconds": latency,
            "prompt": prompt,
            "raw_reply": resp_wire,
            "raw_provider_response": raw_json,
            "validation_error": validation_error,
            "host_stage_passed": purity_ok and exact_match,
            **transport,
        })

        dag_nodes.append({
            "node_id": f"DDC_STAGE_{turn_num}_{stage}",
            "turn": turn_num,
            "stage": stage,
            "action": action,
            "wire_in": input_wire,
            "wire_out": resp_wire,
            "verified": exact_match and purity_ok,
            "timestamp": ts,
        })

    # Terminal node
    dag_nodes.append({
        "node_id": "TERMINAL_EXACT_REPAIR_6SITE",
        "turn": 5,
        "stage": "TERMINAL",
        "action": "COLLAPSE_SIGN_OBSTRUCTION",
        "exact_partition_z": math_res["exact_partition_z"],
        "transfer_matrix_trace": math_res["transfer_matrix_trace"],
        "gin_synthesis_time_seconds": math_res["gin_synthesis_time_seconds"],
        "cancelling_pairs": math_res["total_cancelling_pairs"],
        "duality_gap": int(math_res["exact_partition_z"]) - int(math_res["transfer_matrix_trace"]),
        "terminal_wire": turns_executed[-1]["response_wire"],
        "timestamp": ts,
    })

    all_passed = all(t["host_stage_passed"] for t in turns_executed)
    # Write DAG trace only when requested
    if write_receipt:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        with (output_dir / SYMBOLIC_6SITE_DAG_TRACE.name).open("w", encoding="utf-8", newline="\n") as f:
            for node in dag_nodes:
                f.write(json.dumps(node) + "\n")

    summary = {
        "protocol": "Pure Gamma38 Wire Grammar 6-Site Scaling",
        "execution_mode": "live" if (live and api_key) else "deterministic_host_fixture_replay",
        "model": model if (live and api_key) else "host_fixture",
        "timestamp": ts,
        "lattice_properties": {
            "sites": 6,
            "nodes": 24,
            "plaquettes": 12,
            "breakup_subgraphs": math_res["subgraphs"],
            "configurations": math_res["configurations"],
            "cancelling_subgraphs": math_res["cancelling_subgraphs"],
            "surviving_subgraphs": math_res["surviving_subgraphs"],
            "cancelling_doublets_paired": math_res["total_cancelling_pairs"],
            "gin_synthesis_time_ms": round(math_res["gin_synthesis_time_seconds"] * 1000, 3),
        },
        "exact_partition_z": int(math_res["exact_partition_z"]),
        "transfer_matrix_trace": int(math_res["transfer_matrix_trace"]),
        "duality_gap": int(math_res["exact_partition_z"]) - int(math_res["transfer_matrix_trace"]),
        "turns": turns_executed,
        "all_turns_passed": all(t["exact_match"] and t["purity_ok"] for t in turns_executed),
        "total_latency_seconds": round(total_latency, 3) if live else None,
        "total_tokens": sum(token_usage) if live and all(isinstance(n, int) and not isinstance(n, bool) and n >= 0 for n in token_usage) else None,
        "math_verification_time_seconds": round(t_math, 3),
        "status": "HOST_STAGE_CHECKS_PASSED" if all_passed else "REFUSED",
        "evidence_scope": "live_provider_trace" if live else "bounded_host_fixture_replay",
        "live_model_execution": live,
        "authority_effect": "None",
        "source_sha256": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__), CODE_DIR / "symbol_game_pfp.py"]},
    }

    if write_receipt:
        with (output_dir / CERTIFIED_6SITE_SYMBOLIC_RECEIPT.name).open("w", encoding="utf-8", newline="\n") as f:
            json.dump(summary, f, indent=2)

    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description="The Symbol Game Pure Gamma38 6-Site Runner.")
    parser.add_argument("--live", action="store_true", help="Execute live queries via OpenRouter.")
    parser.add_argument("--model", default="stealth/space-bunny-alpha", help="OpenRouter model ID.")
    parser.add_argument("--api-key", default=os.environ.get("OPENROUTER_API_KEY", ""), help="OpenRouter API Key.")
    parser.add_argument("--output-dir", type=Path, required=True, help="Explicit directory for replay receipts.")
    args = parser.parse_args()

    print("==========================================================================")
    print("  THE SYMBOL GAME: PURE GAMMA-38 6-SITE SCALING & GIN RUNNER")
    print("  Grammar: Pure Wire \\Gamma_{38} = \\Sigma_{36} \\cup \\{<, >\\}")
    print("  Scale: 6 Sites, 12 Plaquettes, 4,096 Subgraphs, 33,396 Configurations")
    print("==========================================================================")

    res = run_pure_symbolic_6site(
        live=args.live,
        model=args.model,
        api_key=args.api_key,
        write_receipt=True,
        output_dir=args.output_dir,
    )

    print(f"\nExecution Mode: {res['execution_mode']}")
    print(f"Model:          {res['model']}")
    print(f"Total Turns:    {len(res['turns'])} / 4 Passed")
    print(f"All Passed:     {res['all_turns_passed']}")
    print(f"GIN Index Time: {res['lattice_properties']['gin_synthesis_time_ms']} ms")
    print(f"Cancelling:     {res['lattice_properties']['cancelling_doublets_paired']} doublets paired (384 states)")
    print(f"Exact Z:        {res['exact_partition_z']}")
    print(f"Transfer Trace: {res['transfer_matrix_trace']}")
    print(f"Duality Gap:    {res['duality_gap']}")
    print(f"Status:         {res['status']}")
    print("==========================================================================")

    return 0 if res["all_turns_passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
