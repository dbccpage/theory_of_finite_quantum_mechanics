"""Four-site host replay and coached independent Gamma38 response checks.

Both prompts and replies use Gamma38. Offline candidates are supplied by the
host fixture; transport acceptance does not demonstrate model discovery.
AuthorityEffect: None.
"""
from __future__ import annotations

from fractions import Fraction

import argparse
import hashlib
import json
import os
import sys
import urllib.request
from pathlib import Path
from typing import Any, Dict

DEMOS_DIR = Path(__file__).resolve().parent.parent
CODE_DIR = DEMOS_DIR.parent / "code"
REPO_ROOT = next(p for p in DEMOS_DIR.parents if (p / "omega_engine_pfp").is_dir())
for path in (CODE_DIR, REPO_ROOT):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from blind_problem import assert_lexical_hygiene
from symbol_game_stage_controller import SymbolGameStageController
from omega_engine_pfp.domain.tower.parser import (
    parse_packet, serialize_packet, validate_packet_semantics, GAMMA_38,
)

from omega_engine_pfp.use_cases.llm_turn import CreateTurnUseCase, SubmitCandidateUseCase

RESULTS_DIR = DEMOS_DIR / "results"
CERTIFIED_SYMBOLIC_RECEIPT = RESULTS_DIR / "certified_pure_symbolic_results.json"
SYMBOLIC_DAG_TRACE = RESULTS_DIR / "symbol_game_pure_wire_dag.jsonl"

WIRE_TURNS = [
    {
        "turn": 1,
        "stage": "PLAQUETTE_BREAKUP",
        "input_wire": "op<<11>op<<1><10000>>op<<10><0><1>>>",
        "wire_prompt": "op<<11>op<<1><10000>>op<<10><0><1>>>",
        "grammar_prompt": "op<<11>op<<1><10000>>op<<10><0><1>>>",
        "expected_response_wire": "op<<101><10><0><1><10>>",
        "action": "PROBE_PLAQUETTES",
    },
    {
        "turn": 2,
        "stage": "MEASURE_HOLONOMY",
        "input_wire": "op<<101><10><0><1><10>>",
        "wire_prompt": "op<<101><10><0><1><10>>",
        "grammar_prompt": "op<<101><10><0><1><10>>",
        "expected_response_wire": "op<<100><>op<<11>op<<1><10>>op<<1><11>>>>",
        "action": "MEASURE_HOLONOMY",
    },
    {
        "turn": 3,
        "stage": "LIFT_REQUEST",
        "input_wire": "op<<100><>op<<11>op<<1><10>>op<<1><11>>>>",
        "wire_prompt": "op<<100><>op<<11>op<<1><10>>op<<1><11>>>>",
        "grammar_prompt": "op<<100><>op<<11>op<<1><10>>op<<1><11>>>>",
        "expected_response_wire": "op<<1100><liftreq>>",
        "action": "REQUEST_LIFT",
    },
    {
        "turn": 4,
        "stage": "EXACT_REPAIR",
        "input_wire": "op<<0><><0><1>>",
        "wire_prompt": "op<<0><><0><1>>",
        "grammar_prompt": "op<<0><><0><1>>",
        "expected_response_wire": "op<<10010><0><1110010000><1>>",
        "action": "CERTIFY_EXACT_REPAIR",
    },
]


def assert_wire_purity(wire: str) -> bool:
    for character in wire:
        if character not in GAMMA_38:
            raise ValueError(f"Illegal non-Gamma38 character {character!r}")
    packet = parse_packet(wire)
    validate_packet_semantics(packet)
    if serialize_packet(packet) != wire:
        raise ValueError("Wire roundtrip mismatch")
    return True


def source_hashes() -> Dict[str, str]:
    paths = [Path(__file__), CODE_DIR / "symbol_game_stage_controller.py", CODE_DIR / "meron_exact_model.py"]
    return {path.relative_to(REPO_ROOT).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest() for path in paths}


def execute_pure_symbolic_offline_replay(output_dir: Path | None = None) -> Dict[str, Any]:
    """Compute the host fixture; write only to an explicitly selected directory."""
    controller = SymbolGameStageController(sites=4)
    try:
        nodes = controller.run_pipeline()
        seen = set()
        for node in nodes:
            assert_wire_purity(node["gamma38_wire"])
            if not set(node["parent_ids"]).issubset(seen):
                raise ValueError("DAG parent order is invalid")
            seen.add(node["node_id"])
        terminal = nodes[-1]["payload"]
        value = terminal["exact_partition_z"]
        trace = terminal["transfer_matrix_trace"]
        if value != trace or nodes[-1]["gamma38_wire"] != WIRE_TURNS[-1]["expected_response_wire"]:
            raise ValueError("Host partition, transfer trace, and terminal fixture disagree")
        turn_receipts = []
        run_roots = []
        for turn in WIRE_TURNS:
            assert_wire_purity(turn["wire_prompt"])
            run_root = CreateTurnUseCase().execute(
                task_id=f"fsp-meron-turn-{turn['turn']}",
                objective=f"Symbolic Meron turn {turn['turn']} stage {turn['stage']}",
                prompt_body=turn["wire_prompt"],
            )
            updated, candidate, content = SubmitCandidateUseCase().execute(
                run_root=run_root, candidate_id=f"candidate-meron-turn-{turn['turn']}",
                producer_id="fsp_pure_symbolic_runner", reply_text=turn["expected_response_wire"],
            )
            if candidate.candidate_id not in updated.candidate_ids or content.content_id not in updated.content_ids:
                raise ValueError("Turn artifact membership is invalid")
            if updated.terminal_status != "TransportValidated":
                raise ValueError("Turn transport validation failed")
            run_roots.append(updated.to_dict())
            turn_receipts.append({"turn": turn["turn"], "stage": turn["stage"],
                "input_wire": turn["input_wire"], "wire_prompt": turn["wire_prompt"],
                "grammar_prompt": turn["grammar_prompt"], "response_wire": turn["expected_response_wire"],
                "action": turn["action"], "gamma38_pure": True,
                "run_root_id": updated.run_root_id, "candidate_id": candidate.candidate_id,
                "content_id": content.content_id, "terminal_status": updated.terminal_status})
        receipt = {
            "receipt_id": "CERT-PURE-SYMBOLIC-PFP-2026-10-02",
            "protocol": "Pure Gamma38 Symbolic Wire Dialog",
            "evidence_scope": "deterministic_host_fixture",
            "live_provider_evidence": False,
            "prompt_scope": "wire-only independent requests; offline responses are supplied fixtures",
            "source_sha256": source_hashes(),
            "alphabet_size": len(GAMMA_38),
            "nodes_generated": len(nodes),
            "terminal_action": nodes[-1]["action"],
            "exact_partition_binary": bin(value)[2:],
            "exact_partition_integer": value,
            "transfer_matrix_trace": trace,
            "duality_gap": value - trace,
            "verified": value == trace,
            "turns": turn_receipts,
            "run_roots": run_roots,
        }
        if output_dir is not None:
            output_dir.mkdir(parents=True, exist_ok=True)
            (output_dir / CERTIFIED_SYMBOLIC_RECEIPT.name).write_bytes((json.dumps(receipt, indent=2) + "\n").encode())
            (output_dir / SYMBOLIC_DAG_TRACE.name).write_bytes("".join(json.dumps(n) + "\n" for n in nodes).encode())
        return receipt
    finally:
        controller.con.close()


def query_openrouter_wire_turn(model: str, prompt: str, api_key: str) -> Dict[str, Any]:
    assert_wire_purity(prompt)
    from omega_engine_woland.domain.providers.types import CandidateRequest, ChatMessage, DecodingParamsV1, Provider
    from omega_engine_woland.infrastructure.providers.openai_compat import OpenAiCompatTransport
    transport = OpenAiCompatTransport(Provider.OPENROUTER, api_key=api_key, max_tokens=120, timeout=60)
    request = CandidateRequest(messages=(ChatMessage("user", prompt),), decoding=DecodingParamsV1(temperature=Fraction(0)))
    started = time.perf_counter()
    raw = transport(Provider.OPENROUTER, model, request)
    latency = time.perf_counter() - started
    data = json.loads(raw)
    data["_raw_provider_body_utf8"] = raw.decode("utf-8")
    data["_raw_provider_body_sha256"] = hashlib.sha256(raw).hexdigest()
    return data


def run_live_symbolic_trial(model: str, api_key: str) -> Dict[str, Any]:
    results = []
    for turn in WIRE_TURNS:
        assert_lexical_hygiene(turn["grammar_prompt"])
        response = query_openrouter_wire_turn(model, turn["grammar_prompt"], api_key)
        raw_reply = response["choices"][0]["message"].get("content") or ""
        wire = raw_reply
        try:
            pure = assert_wire_purity(wire)
        except (ValueError, TypeError):
            pure = False
        passed = pure and wire == turn["expected_response_wire"]
        results.append({"turn": turn["turn"], "stage": turn["stage"], "prompt": turn["grammar_prompt"],
            "raw_provider_response": response, "raw_reply": raw_reply, "emitted_wire": wire,
            "expected_wire": turn["expected_response_wire"], "is_gamma38_pure": pure, "passed": passed})
    return {"model": model, "evidence_scope": "wire_only_independent_response_check",
        "prompt_contains_answer": False, "source_sha256": source_hashes(),
        "all_turns_passed": all(t["passed"] for t in results), "turns": results}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--api-key", default=os.environ.get("OPENROUTER_API_KEY", ""))
    parser.add_argument("--model", default="stealth/space-bunny-alpha")
    parser.add_argument("--output-directory", type=Path)
    args = parser.parse_args()
    if args.live:
        if not args.api_key:
            parser.error("--live requires an API key")
        result = run_live_symbolic_trial(args.model, args.api_key)
        if args.output_directory:
            args.output_directory.mkdir(parents=True, exist_ok=True)
            (args.output_directory / "live_wire_trial.json").write_bytes((json.dumps(result, indent=2) + "\n").encode())
        print(json.dumps(result, indent=2))
        return 0 if result["all_turns_passed"] else 1
    result = execute_pure_symbolic_offline_replay(args.output_directory)
    print(json.dumps(result, indent=2))
    return 0 if result["verified"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
