"""Replay selected P.17 backtrack, square and braid certificates on native runs.

Each submitted replacement preserves two fixed, proof-relevant history
boundaries. All intermediate orders have fresh Rust execution evidence. Distinct
3-certificates are retained; this checker supplies no equivalence of them.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

if __package__:
    from .check_causal_execution import (
        NativeOwner,
        admit_problem,
        arguments,
        digest,
        fields,
        natural,
        read_json,
        require,
        same,
        verify_certificate,
    )
else:
    from check_causal_execution import (
        NativeOwner,
        admit_problem,
        arguments,
        digest,
        fields,
        natural,
        read_json,
        require,
        same,
        verify_certificate,
    )


def replay_word(problem: dict, execution: dict, source: list[int], word: list[int]) -> dict:
    events, before = admit_problem(problem)
    require(type(word) is list and len(word) <= 1000, "swap-word bound")
    histories = {tuple(h["order"]): h for h in execution["histories"]}
    require(type(source) is list and all(type(e) is int for e in source), "source order type")
    current = list(source)
    require(tuple(current) in histories, "source order has no native history")
    orders, swaps = [current.copy()], []
    for position in word:
        natural(position, "swap position")
        require(position + 1 < len(current), "swap position outside history")
        left, right = current[position:position + 2]
        ideal = sum(1 << e for e in current[:position])
        require(not (before[left] & ~ideal or before[right] & ~ideal),
                "swap involves comparable/unavailable occurrences")
        old = histories[tuple(current)]
        current[position], current[position + 1] = right, left
        require(tuple(current) in histories, "intermediate order lacks native admissibility")
        new = histories[tuple(current)]
        require(same(old["frames"][position]["boundary"], new["frames"][position]["boundary"]),
                "swap source frame changed")
        require(same(old["frames"][position + 2]["boundary"], new["frames"][position + 2]["boundary"]),
                "swap target frame changed")
        require(same(old["protected_total"], new["protected_total"]), "swap changes protected price")
        swaps.append({"position": position, "ideal": ideal,
                      "occurrences": [events[left]["tag"], events[right]["tag"]],
                      "source_history_sha256": digest(old), "target_history_sha256": digest(new),
                      "source_frame": old["frames"][position]["boundary"],
                      "target_frame": old["frames"][position + 2]["boundary"]})
        orders.append(current.copy())
    return {"word": word, "orders": orders, "swaps": swaps,
            "source_history_sha256": digest(histories[tuple(source)]),
            "target_history_sha256": digest(histories[tuple(current)])}


def replacement_kind(before: list[int], after: list[int]) -> str:
    require(type(before) is list and type(after) is list, "replacement sides must be arrays")
    for value in before + after:
        natural(value, "replacement generator")
    short, long = sorted((before, after), key=len)
    if not short and len(long) == 2 and long[0] == long[1]:
        return "backtrack"
    if len(before) == len(after) == 2 and abs(before[0] - before[1]) > 1 and after == before[::-1]:
        return "square"
    if len(before) == len(after) == 3 and before[0] == before[2] and abs(before[0] - before[1]) == 1:
        if after == [before[1], before[0], before[1]]:
            return "braid"
    raise ValueError("not a declared P.17 local relation")


def assemble_three(problem: dict, request: dict, replacements: list[dict], execution: dict) -> dict:
    """Construct proposed evidence; acceptance additionally calls native replay."""
    fields(request, {"schema", "source_order", "target_order", "source_word", "target_word"}, "3-boundary request")
    require(request["schema"] == "wdp-causal-three-request-v1", "unknown 3-boundary request")
    require(type(request["target_order"]) is list and all(type(e) is int for e in request["target_order"]),
            "target order type")
    require(type(replacements) is list and len(replacements) <= 1000, "replacement bound")
    current = request["source_word"]
    proof = replay_word(problem, execution, request["source_order"], current)
    require(same(proof["orders"][-1], request["target_order"]), "source proof changes fixed boundary history")
    first_boundary = (proof["source_history_sha256"], proof["target_history_sha256"])
    proofs = [proof]
    for replacement in replacements:
        fields(replacement, {"kind", "offset", "before", "after"}, "local replacement")
        offset = natural(replacement["offset"], "replacement offset")
        before, after = replacement["before"], replacement["after"]
        require(replacement_kind(before, after) == replacement["kind"], "replacement kind mismatch")
        require(offset <= len(current) and offset + len(before) <= len(current), "replacement offset outside word")
        require(same(current[offset:offset + len(before)], before), "replacement offset does not match submitted side")
        current = current[:offset] + after + current[offset + len(before):]
        proof = replay_word(problem, execution, request["source_order"], current)
        require(same(proof["orders"][-1], request["target_order"]), "replacement changes target history")
        require((proof["source_history_sha256"], proof["target_history_sha256"]) == first_boundary,
                "replacement changes actual framed boundaries")
        proofs.append(proof)
    require(same(current, request["target_word"]), "replacement sequence misses target proof")
    return {"schema": "wdp-causal-three-v1", "authority_effect": "None",
            "problem_sha256": digest(problem), "request_sha256": digest(request),
            "execution": execution, "replacements": replacements, "proofs": proofs,
            "source_history_sha256": first_boundary[0], "target_history_sha256": first_boundary[1],
            "scope": "selected local 3-witness; distinct certificates are not identified"}


def verify_three(problem: dict, request: dict, certificate: dict, native: NativeOwner) -> dict:
    require(type(certificate) is dict and "execution" in certificate and "replacements" in certificate,
            "3-certificate missing evidence")
    execution_receipt = verify_certificate(problem, certificate["execution"], native)
    expected = assemble_three(problem, request, certificate["replacements"], certificate["execution"])
    require(same(certificate, expected), "3-certificate differs from checked replacement replay")
    return {"status": "PASS", "authority_effect": "None", "certificate_sha256": digest(certificate),
            "replacements": len(certificate["replacements"]), "fresh_native_replay": True,
            "native_histories": execution_receipt["histories"]}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("problem", type=Path)
    parser.add_argument("request", type=Path)
    parser.add_argument("certificate", type=Path)
    arguments(parser)
    args = parser.parse_args()
    native = NativeOwner(args.native_bin, args.native_build_receipt, args.source_root)
    receipt = verify_three(read_json(args.problem), read_json(args.request), read_json(args.certificate), native)
    print(json.dumps(receipt, sort_keys=True))


if __name__ == "__main__":
    main()
