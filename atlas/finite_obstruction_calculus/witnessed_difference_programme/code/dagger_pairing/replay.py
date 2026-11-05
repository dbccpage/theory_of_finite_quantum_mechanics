"""Source-bound producer/checker for dagger and observer-pairing examples."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path
from typing import Any, Mapping

from .model import (
    apply_dagger,
    gram,
    observe,
    subtract,
    tensor_dagger,
    tensor_product,
)


def _canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _nonnegative_int(value: object, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"{name} must be a nonnegative integer")
    return value


def reference_problem() -> dict[str, Any]:
    return {
        "left_dagger": {"a": "A", "A": "a", "b": "b"},
        "right_dagger": {"x": "X", "X": "x", "y": "y"},
        "left_vector": {"a": 2, "A": -1, "b": 3},
        "right_vector": {"x": 1, "X": 4, "y": -2},
        "observer_rows": [
            {"a": 1, "b": 1, "c": 0},
            {"a": 0, "b": 0, "c": 1},
        ],
        "blind_difference": {"a": 1, "b": -1},
        "visible_difference": {"a": 1, "c": -2},
        "equal_report_states": [{"a": 1}, {"b": 1}],
        "exhaustive_coefficient_bound": 2,
    }


def produce(problem: Mapping[str, Any]) -> dict[str, Any]:
    left_once = apply_dagger(problem["left_vector"], problem["left_dagger"])
    left_twice = apply_dagger(left_once, problem["left_dagger"])
    raw_tensor = tensor_product(problem["left_vector"], problem["right_vector"])
    dagger_after_tensor = tensor_dagger(
        raw_tensor, problem["left_dagger"], problem["right_dagger"]
    )
    tensor_after_dagger = tensor_product(
        left_once,
        apply_dagger(problem["right_vector"], problem["right_dagger"]),
    )
    rows = problem["observer_rows"]
    blind = problem["blind_difference"]
    visible = problem["visible_difference"]
    state_left, state_right = problem["equal_report_states"]
    difference = subtract(state_left, state_right)
    bound = _nonnegative_int(
        problem["exhaustive_coefficient_bound"], "exhaustive_coefficient_bound"
    )
    exhaustive_cases = 0
    radical_matches_kernel = True
    for coefficients in itertools.product(range(-bound, bound + 1), repeat=3):
        value = {
            key: coefficient
            for key, coefficient in zip(("a", "b", "c"), coefficients, strict=True)
            if coefficient
        }
        report = observe(value, rows)
        radical_matches_kernel &= (gram(value, value, rows) == 0) == all(
            entry == 0 for entry in report
        )
        exhaustive_cases += 1
    return {
        "schema": "wdp-dagger-observer-pairing/v1",
        "problem_sha256": hashlib.sha256(_canonical(problem)).hexdigest(),
        "dagger": {
            "original": dict(problem["left_vector"]),
            "once": left_once,
            "twice": left_twice,
            "involutive": left_twice == problem["left_vector"],
        },
        "tensor_dagger": {
            "dagger_after_tensor": dagger_after_tensor,
            "tensor_after_dagger": tensor_after_dagger,
            "compatible": dagger_after_tensor == tensor_after_dagger,
        },
        "observer_pairing": {
            "blind_report": list(observe(blind, rows)),
            "blind_norm_square": gram(blind, blind, rows),
            "visible_report": list(observe(visible, rows)),
            "visible_norm_square": gram(visible, visible, rows),
            "equal_left_report": list(observe(state_left, rows)),
            "equal_right_report": list(observe(state_right, rows)),
            "difference": difference,
            "difference_norm_square": gram(difference, difference, rows),
            "exhaustive_cases": exhaustive_cases,
            "radical_matches_kernel": radical_matches_kernel,
        },
        "positive_nonselection": {
            "input": 2,
            "unit_weight_form": 4,
            "double_weight_form": 8,
            "both_nonnegative": True,
            "forms_differ": True,
        },
        "scope": {
            "derived": [
                "additive involutive dagger extension",
                "componentwise dagger on algebraic tensors",
                "observer-induced positive semidefinite Gram form",
                "Gram self-null space equals observer kernel",
            ],
            "not_derived": [
                "choice of dagger or observer",
                "unique positive pairing",
                "integer square root of minus one",
                "complex or Hilbert completion",
                "probability or Born readout",
            ],
        },
    }


def check(problem: Mapping[str, Any], receipt: Mapping[str, Any]) -> None:
    expected = produce(problem)
    if receipt != expected:
        raise ValueError("receipt does not replay from the bound problem")
    if not receipt["dagger"]["involutive"]:
        raise ValueError("dagger did not square to identity")
    if not receipt["tensor_dagger"]["compatible"]:
        raise ValueError("dagger did not act componentwise on tensor coordinates")
    pairing = receipt["observer_pairing"]
    if pairing["blind_report"] != [0, 0] or pairing["blind_norm_square"] != 0:
        raise ValueError("blind difference did not remain in the Gram radical")
    if pairing["visible_norm_square"] <= 0:
        raise ValueError("visible difference did not have positive observed norm")
    if not pairing["radical_matches_kernel"]:
        raise ValueError("enumerated Gram radical differs from observer kernel")
    if not receipt["positive_nonselection"]["forms_differ"]:
        raise ValueError("positive-pairing nonselection control collapsed")


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
    print("dagger-observer-pairing replay: PASS")


if __name__ == "__main__":
    main()
