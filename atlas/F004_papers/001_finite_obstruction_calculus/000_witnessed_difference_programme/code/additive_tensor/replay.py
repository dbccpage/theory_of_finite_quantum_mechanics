"""Source-bound producer and checker for additive/tensor completion examples."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping

from .model import (
    add_signed,
    alternative_counts,
    bilinear_value,
    determinant_2x2,
    fold_signed,
    negate_signed,
    normalize_signed,
    tensor_product,
)


def _canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def reference_problem() -> dict[str, Any]:
    return {
        "left_generators": ["a", "b"],
        "right_generators": ["x", "y"],
        "alternative_words": [["a", "b", "a"], ["a", "a", "b"]],
        "signed_pair": {"positive": ["a", "b"], "negative": ["a"]},
        "generator_values": {"a": 2, "b": -3},
        "left_vector": {"a": 2, "b": -1},
        "right_vector": {"x": 1, "y": 3},
        "basis_bilinear_values": {"a|x": 2, "a|y": -1, "b|x": 4, "b|y": 5},
        "nonfactorable_tensor": {"a|x": 1, "b|y": 1},
    }


def produce(problem: Mapping[str, Any]) -> dict[str, Any]:
    first, second = problem["alternative_words"]
    first_counts = alternative_counts(first)
    second_counts = alternative_counts(second)
    signed = normalize_signed(
        problem["signed_pair"]["positive"], problem["signed_pair"]["negative"]
    )
    left = problem["left_vector"]
    right = problem["right_vector"]
    tensor = tensor_product(left, right)
    direct = bilinear_value(left, right, problem["basis_bilinear_values"])
    factored = fold_signed(tensor, problem["basis_bilinear_values"])
    cancelled = add_signed(signed, negate_signed(signed))
    return {
        "schema": "wdp-additive-tensor/v1",
        "problem_sha256": hashlib.sha256(_canonical(problem)).hexdigest(),
        "alternative": {
            "first_word": list(first),
            "second_word": list(second),
            "first_counts": first_counts,
            "second_counts": second_counts,
            "commutative_equal": first_counts == second_counts,
            "ordered_equal": list(first) == list(second),
        },
        "signed_completion": {
            "normal_form": signed,
            "fold_value": fold_signed(signed, problem["generator_values"]),
            "self_plus_negative": cancelled,
        },
        "tensor": {
            "coordinates": tensor,
            "direct_bilinear_value": direct,
            "factor_value": factored,
            "factorization_equal": direct == factored,
        },
        "nonfactorable": {
            "coordinates": dict(problem["nonfactorable_tensor"]),
            "determinant": determinant_2x2(
                problem["nonfactorable_tensor"], ("a", "b"), ("x", "y")
            ),
        },
        "scope": {
            "derived": [
                "free finite commutative alternatives",
                "integer signed completion",
                "algebraic biadditive tensor factorization",
            ],
            "not_derived": [
                "complex scalars",
                "involution",
                "positivity",
                "norm or Hilbert completion",
                "probability or Born readout",
            ],
        },
    }


def check(problem: Mapping[str, Any], receipt: Mapping[str, Any]) -> None:
    expected = produce(problem)
    if receipt != expected:
        raise ValueError("receipt does not replay from the bound problem")
    alternative = receipt["alternative"]
    if not alternative["commutative_equal"] or alternative["ordered_equal"]:
        raise ValueError("alternative example did not isolate order erasure")
    if receipt["signed_completion"]["self_plus_negative"]:
        raise ValueError("signed inverse failed to cancel")
    tensor = receipt["tensor"]
    if not tensor["factorization_equal"]:
        raise ValueError("bilinear map did not factor through submitted tensor coordinates")
    if receipt["nonfactorable"]["determinant"] == 0:
        raise ValueError("nonfactorable tensor witness has zero determinant")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("produce", "check"))
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args()
    problem = reference_problem()
    if args.command == "produce":
        body = json.dumps(produce(problem), indent=2, sort_keys=True) + "\n"
        if args.receipt:
            args.receipt.write_text(body, encoding="utf-8", newline="\n")
        else:
            print(body, end="")
        return
    if not args.receipt:
        parser.error("check requires --receipt")
    receipt = json.loads(args.receipt.read_text(encoding="utf-8"))
    check(problem, receipt)
    print("additive-tensor replay: PASS")


if __name__ == "__main__":
    main()
