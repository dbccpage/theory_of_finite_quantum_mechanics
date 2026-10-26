"""Retain one free Space Bunny proposal; evaluate only declared finite witnesses.

The model's prose is retained for review and receives no blanket proof credit.
No model code is requested or executed. Credentials are explicit and transient.
"""

from __future__ import annotations

import argparse
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from pfp_calculus.live_run import ENDPOINTS_URL, MODEL, free_endpoints
from pfp_calculus.replay import digest

ROOT = Path(__file__).resolve().parent


def frozen_inputs() -> dict:
    return {
        "observation": {
            "states": [str(x) for x in range(1, 9)], "visible": ["*"] * 8,
            "query": ["1", "1", "2", "2", "3", "3", "4", "4"],
            "instruments": [
                {"name": "A", "outcomes": ["0", "1", "0", "1", "0", "0", "1", "1"], "cost": "1"},
                {"name": "B", "outcomes": ["0", "0", "1", "1", "0", "0", "0", "0"], "cost": "3"},
                {"name": "C", "outcomes": ["0", "0", "0", "0", "0", "0", "1", "1"], "cost": "3"},
            ]},
        "unsafe_transfer": {
            "source": {"id": "S", "carrier": ["0", "1"], "valid": ["0"], "profile": {"kind": "finite_validity"}},
            "target": {"id": "T", "carrier": ["0", "1"], "valid": ["1"], "profile": {"kind": "finite_validity"}},
            "adapter": {"0": "0", "1": "1"}, "outside_domain": "not_applicable",
            "rules": [{"id": "D", "rejects": ["1"]}], "pool": ["0", "1"]},
        "original_claims_to_reject": {"observation_fixed_cost": "7", "observation_adaptive_cost": "4",
                                      "transfer_rule_admitted": True, "transfer_rejected": ["1"]},
    }


def packet() -> dict:
    system = (
        "PFP TWO-LEVEL REPAIR CONTRACT. You propose corrected mathematics and finite witnesses. "
        "AuthorityEffect is None. The host independently replays your submitted witnesses. "
        "Do not change frozen tasks, silently replace original negative controls, or claim code ran. "
        "No executable code. Return one JSON object with the exact structure described below. "
        "Use string state labels and canonical rational strings for costs. Preserve candidate_id."
    )
    corrections = [
        "Universal antibody transfer is safe iff alpha(G_T) is contained in G_S. Source soundness alone is insufficient; each accumulated rule needs universal adapter evidence or its own target-soundness evidence.",
        "The printed observation table is infeasible: states1 and5 have identical full readings but different query answers. Preserve it as a negative control. Repair ONLY the eight readings of A; keep states,p,q,B,C and all costs frozen.",
        "The initial report p is already observed: overall adaptive worst cost is max over p-fibers of V(fiber), not generally V(X).",
        "Decoder condition is q constant on report fibers. If p-prime coarsens p then unresolved(p) subset unresolved(p-prime), and optimum(p)<=optimum(p-prime). Hitting hyperedges are instrument sets E_u={i:i distinguishes pairu}.",
        "A cover proves feasibility only. Every cheaper fixed subset needs an uncovered-pair certificate or other exhaustive lower bound. LP dual dominates the disjoint-support packing bound.",
        "Polynomial truncation pi<=k fails differentiation already on F=x^(k+1), at derivative degreek. With identity task-data adapter restrict degree<=k. Degree bounds do not make a rational carrier finite.",
        "Individually certified target-sound antibodies compose by union. Certified incremental invariants may support checking; uncertified survivor sets do not.",
        "One-sided validity preservation differs from fiber constancy. Certificates may be exhaustive or algebraic; metadata equality is insufficient.",
        "Savings hv-Ng-C0 is conditional on declared costs and named pools. Dimensions imply no hit probabilities. A singleton source rule can have many preimages. Comparing costs requires stated inequalities, and differentiation costs may already include verification.",
        "Correct examples: d0(0,1,0)=(1,-1,0) for the declared triangle convention. Nonzero circulation pairing proves nonexactness; tolerance rejection needs a bound exceeding epsilon. Approximate recovery requires existence of the declared decoder."
    ]
    structure = {
        "candidate_id": "wdp-repair-space-bunny-001", "authority_effect": "None",
        "revised_statements": "array of exactly10 concise strings, one for each correction; state hypotheses and limitations",
        "observation_repair": {
            "A": "array of8 strings, each0 or1; ONLY this original instrument row can change",
            "fixed_suite": "array of instrument names A/B/C",
            "fixed_cost": "canonical rational string",
            "cheaper_subsets": "array of {suite:[names],uncovered_pair:[state1,state2]} listing EVERY subset of the three instruments with cost strictly below fixed_cost",
            "adaptive_cost": "canonical rational string",
            "adaptive_tree": "recursive JSON node: either {query:query_label}, or {measure:instrument_name,branches:{outcome_label:child_node,...}}; branches exhaust actual outcomes; leaves correct for all remaining states",
            "adaptive_lower_bound": "object {state:state_label,forcing_pairs:[{other:state_label,instrument:instrument_name},...]}; each named pair differs in q and ONLY the named instrument separates it. Distinct forced instruments on this state's path must have total cost equal to adaptive_cost"
        },
        "antibody_repair": {
            "repair_kind": "adapter OR rule; change exactly one of these, while all source/target data remain frozen",
            "adapter": "complete object mapping target labels0,1 to source labels0,1",
            "D": "array of source rejection labels",
            "claimed_rejected": "array of target labels rejected by transferred D",
            "soundness_reason": "concise explanation of universal adapter or per-rule target evidence"
        },
        "verifier_specification": "concise prose specifying independent checks, no executable code"
    }
    user = {"task": "Repair the ten issues and give compact certificates that the host can check unchanged. Find a repaired observation instance with fixed optimum7 and adaptive optimum4, if possible. Supply the actual suite, all cheaper-subset witnesses, adaptive decision tree and forcing lower bound. For transfer, repair sound accumulation by changing only the adapter or only D; source/target tasks remain fixed.",
            "frozen_inputs": frozen_inputs(), "adversarial_review": corrections,
            "worked_example_distinct_from_tasks": {"states": ["a", "b"], "q": ["red", "blue"],
                                                  "measurement": ["0", "1"], "cost": "2",
                                                  "tree": {"measure": "probe", "branches": {"0": {"query": "red"}, "1": {"query": "blue"}}}},
            "required_response_structure": structure}
    return {"authority_effect": "None", "system_prompt": system,
            "user_prompt": json.dumps(user, indent=2), "dispatch": {"model": MODEL, "max_tokens": 4096,
              "temperature": 0, "max_requests": 1, "allow_fallbacks": False, "response_format": {"type": "json_object"}}}


def run(env_file: Path, run_dir: Path) -> dict:
    from omega_engine_operations.domain.rop.result import Err
    from omega_engine_woland.domain.types import CandidateRequest, DecodingParamsV1
    from omega_engine_woland.infrastructure.openrouter_transport import openrouter_transport

    run_dir.mkdir(parents=True, exist_ok=False)
    pfp = packet()
    raw_packet = (json.dumps(pfp, indent=2) + "\n").encode("utf-8")
    for name in ("packet.json", "packet.yaml"):
        (run_dir / name).write_bytes(raw_packet)
    with urllib.request.urlopen(ENDPOINTS_URL, timeout=30) as handle:
        raw_metadata = handle.read(1_000_001)
    if len(raw_metadata) > 1_000_000:
        raise ValueError("ENDPOINT_METADATA_TOO_LARGE")
    (run_dir / "endpoint_metadata.json").write_bytes(raw_metadata)
    free_endpoints(json.loads(raw_metadata))
    request = CandidateRequest(system=pfp["system_prompt"], user=pfp["user_prompt"],
                               decoding=DecodingParamsV1(temperature=0, response_format={"type": "json_object"},
                                                        allow_fallbacks=False, require_parameters=True))
    request.check_payload_ceiling()
    transport = openrouter_transport(env_file=env_file, environ={}, timeout=60)
    if isinstance(transport, Err):
        raise ValueError("CONFIGURATION_REFUSAL: " + transport.error.code)
    (run_dir / "dispatch_started.json").write_text(json.dumps({"authority_effect": "None", "model": MODEL,
          "time_utc": datetime.now(timezone.utc).isoformat(), "max_requests": 1, "max_tokens": 4096,
          "runner_sha256": digest(Path(__file__).read_bytes()), "packet_sha256": digest(raw_packet)}), encoding="utf-8")
    raw_response = transport.value(MODEL, request, 4096)
    (run_dir / "provider_response.json").write_bytes(raw_response)
    response = json.loads(raw_response)
    usage = response.get("usage") or {}
    cost = usage.get("cost", usage.get("total_cost"))
    receipt = {"authority_effect": "None", "model_requested": MODEL, "model_reported": response.get("model"),
               "generation_id": response.get("id"), "raw_usage": usage, "provider_reported_cost_usd": cost,
               "billing_status": "PROVIDER_REPORTED" if cost is not None else "UNKNOWN",
               "provider_response_sha256": digest(raw_response), "packet_sha256": digest(raw_packet)}
    (run_dir / "usage_receipt.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    return receipt


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["assemble", "run"])
    parser.add_argument("--env-file", type=Path)
    parser.add_argument("--run-dir", type=Path)
    args = parser.parse_args()
    if args.mode == "assemble":
        print(json.dumps(packet(), indent=2))
    else:
        if args.env_file is None or args.run_dir is None:
            parser.error("explicit env-file and fresh run-dir required")
        receipt = run(args.env_file, args.run_dir)
        print(json.dumps({key: receipt[key] for key in ("model_reported", "generation_id", "provider_reported_cost_usd", "billing_status")}))
