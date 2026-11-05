"""Create or replay the retained Source-25 execution and selected 3-witnesses."""
from __future__ import annotations

import argparse
import copy
import json
import sys
from pathlib import Path

PAPER = next(p for p in Path(__file__).resolve().parents if (p / "witnessed_difference_programme.md").exists())
sys.path.insert(0, str(PAPER))
from scripts import check_causal_execution as causal  # noqa: E402
from scripts import check_causal_three_cells as cells  # noqa: E402

HERE = Path(__file__).resolve().parent


def build_cases(problem: dict, execution: dict) -> list[dict]:
    cases = []
    for kind, before, after, target in (
        ("backtrack", [0, 0], [], [0, 1, 2, 3]),
        ("square", [0, 2], [2, 0], [1, 0, 3, 2]),
        ("braid", [0, 1, 0], [1, 0, 1], [2, 1, 0, 3]),
    ):
        request = {"schema": "wdp-causal-three-request-v1", "source_order": [0, 1, 2, 3],
                   "target_order": target, "source_word": before, "target_word": after}
        witness = cells.assemble_three(problem, request,
            [{"kind": kind, "offset": 0, "before": before, "after": after}], execution)
        del witness["execution"]  # Shared exact certificate is retained once.
        cases.append({"name": kind, "request": request, "execution_sha256": causal.digest(execution),
                      "certificate": witness})
    return cases


def replay(native: causal.NativeOwner, payload: dict) -> dict:
    causal.fields(payload, {"schema", "execution_problem", "execution", "three_problem", "three_execution", "three_cases"}, "fixture bundle")
    causal.require(payload["schema"] == "wdp-causal-fixtures-v1", "unknown fixture bundle")
    receipts = {"execution": causal.verify_certificate(payload["execution_problem"], payload["execution"], native)}
    for case in payload["three_cases"]:
        causal.fields(case, {"name", "request", "execution_sha256", "certificate"}, "3-fixture")
        causal.require(case["execution_sha256"] == causal.digest(payload["three_execution"]), "stale 3-execution reference")
        witness = {**case["certificate"], "execution": payload["three_execution"]}
        receipts[case["name"]] = cells.verify_three(payload["three_problem"], case["request"], witness, native)
    causal.require(set(receipts) == {"execution", "backtrack", "square", "braid"}, "missing local relation")
    refused = []

    def must_refuse(name, action):
        try:
            action()
        except (causal.CertificateRefusal, ValueError) as error:
            refused.append({"name": name, "status": "REFUSE", "reason": str(error)})
        else:
            raise AssertionError(f"negative control accepted: {name}")

    impossible = copy.deepcopy(payload["three_problem"])
    impossible["events"] = [{"tag": "impossible-remove", "kind": "remove", "relation": "r",
                             "tokens": ["origin", "origin"], "predecessors": []}]
    must_refuse("valid_poset_impossible_remove", lambda: causal.produce_certificate(impossible, native))
    bad = copy.deepcopy(payload["execution"])
    bad["histories"][0]["frames"][1]["native_to_frame"] = [0, 1]
    must_refuse("changed_token_alignment", lambda: causal.verify_certificate(payload["execution_problem"], bad, native))
    braid = next(c for c in payload["three_cases"] if c["name"] == "braid")
    changed = copy.deepcopy(braid["certificate"])
    changed["replacements"][0]["offset"] = 1
    changed["execution"] = payload["three_execution"]
    must_refuse("incorrect_replacement_offset", lambda: cells.verify_three(payload["three_problem"], braid["request"], changed, native))
    changed_boundary = copy.deepcopy(braid["certificate"])
    changed_boundary["target_history_sha256"] = changed_boundary["source_history_sha256"]
    changed_boundary["execution"] = payload["three_execution"]
    must_refuse("changed_framed_boundary", lambda: cells.verify_three(payload["three_problem"], braid["request"], changed_boundary, native))
    comparable = copy.deepcopy(payload["three_problem"])
    comparable["events"][1]["predecessors"] = ["birth-b"]
    comparable_execution = causal.produce_certificate(comparable, native)
    must_refuse("comparable_event_braid", lambda: cells.assemble_three(comparable, braid["request"], braid["certificate"]["replacements"], comparable_execution))
    return {"schema": "wdp-causal-replay-v1", "authority_effect": "None", "status": "PASS",
            "fixture_sha256": causal.digest(payload), "native_binding": native.binding,
            "accepted": receipts, "negative_controls": refused,
            "scope": "supplied finite families and selected local relations only"}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("create", "check"))
    parser.add_argument("--fixtures", type=Path, default=HERE / "execution_fixtures.json")
    parser.add_argument("--output", type=Path)
    causal.arguments(parser)
    args = parser.parse_args()
    native = causal.NativeOwner(args.native_bin, args.native_build_receipt, args.source_root)
    if args.command == "create":
        causal.require(not args.fixtures.exists(), "refusing fixture overwrite")
        problem = causal.read_json(HERE / "five_edit_problem.json")
        three = causal.read_json(HERE / "antichain_problem.json")
        execution = causal.produce_certificate(three, native)
        payload = {"schema": "wdp-causal-fixtures-v1", "execution_problem": problem,
                   "execution": causal.produce_certificate(problem, native), "three_problem": three,
                   "three_execution": execution, "three_cases": build_cases(three, execution)}
    else:
        payload = causal.read_json(args.fixtures)
    receipt = replay(native, payload)
    if args.command == "create":
        args.fixtures.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    if args.output:
        causal.require(not args.output.exists(), "refusing replay receipt overwrite")
        args.output.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(causal.encoded(receipt))


if __name__ == "__main__":
    main()
