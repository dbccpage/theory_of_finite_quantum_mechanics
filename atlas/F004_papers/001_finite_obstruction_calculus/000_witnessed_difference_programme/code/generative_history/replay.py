"""Deterministic producer/checker for the foundational history examples."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping

from .model import (
    Edge,
    History,
    Question,
    Signature,
    bounded_context_counterexample,
    edge_counts,
    expected_endpoint_boundary,
    vertex_boundary,
)


def _canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _nonnegative_int(value: object, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"{name} must be a nonnegative integer")
    return value


def reference_problem() -> dict[str, Any]:
    return {
        "objects": ["o"],
        "edges": [
            {"name": "a", "source": "o", "target": "o"},
            {"name": "b", "source": "o", "target": "o"},
        ],
        "left": {"source": "o", "target": "o", "edges": []},
        "right": {"source": "o", "target": "o", "edges": ["a"]},
        "questions": [
            {
                "name": "exact-b",
                "source": "o",
                "target": "o",
                "kind": "exact_word",
                "argument": ["b"],
            }
        ],
        "max_context_length": 1,
    }


def _decode(problem: Mapping[str, Any]) -> tuple[Signature, History, History, tuple[Question, ...]]:
    signature = Signature(
        tuple(problem["objects"]),
        tuple(Edge(**edge) for edge in problem["edges"]),
    )
    left = History(
        problem["left"]["source"],
        problem["left"]["target"],
        tuple(problem["left"]["edges"]),
    )
    right = History(
        problem["right"]["source"],
        problem["right"]["target"],
        tuple(problem["right"]["edges"]),
    )
    questions = tuple(Question(**question) for question in problem["questions"])
    return signature, left, right, questions


def produce(problem: Mapping[str, Any]) -> dict[str, Any]:
    signature, left, right, questions = _decode(problem)
    witness = bounded_context_counterexample(
        signature,
        left,
        right,
        questions,
        _nonnegative_int(problem["max_context_length"], "max_context_length"),
    )
    ordered_left = History("o", "o", ("a", "b"))
    ordered_right = History("o", "o", ("b", "a"))
    return {
        "schema": "wdp-generative-history/v1",
        "problem_sha256": hashlib.sha256(_canonical(problem)).hexdigest(),
        "context_counterexample": witness,
        "boundary": {
            "actual": vertex_boundary(signature, ordered_left),
            "expected": expected_endpoint_boundary(signature, ordered_left),
        },
        "abelianization_counterexample": {
            "left": list(ordered_left.edges),
            "right": list(ordered_right.edges),
            "left_counts": edge_counts(ordered_left),
            "right_counts": edge_counts(ordered_right),
            "ordered_equal": ordered_left.edges == ordered_right.edges,
        },
    }


def check(problem: Mapping[str, Any], receipt: Mapping[str, Any]) -> None:
    expected = produce(problem)
    if receipt != expected:
        raise ValueError("receipt does not replay from the bound problem")
    witness = receipt["context_counterexample"]
    if witness is None or witness["left_answer"] == witness["right_answer"]:
        raise ValueError("missing distinguishing context")
    if receipt["boundary"]["actual"] != receipt["boundary"]["expected"]:
        raise ValueError("history boundary does not telescope")
    counterexample = receipt["abelianization_counterexample"]
    if counterexample["left_counts"] != counterexample["right_counts"]:
        raise ValueError("counterexample does not have equal occurrence counts")
    if counterexample["ordered_equal"]:
        raise ValueError("counterexample did not retain an order distinction")


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
    print("generative-history replay: PASS")


if __name__ == "__main__":
    main()
