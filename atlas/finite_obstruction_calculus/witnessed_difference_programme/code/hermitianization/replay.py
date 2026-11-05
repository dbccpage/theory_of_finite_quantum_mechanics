"""Source-bound producer/checker for finite rational Hermitianization."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path
from typing import Any, Mapping

from .model import (
    GaussianRational,
    complex_scalar_action,
    gram_matrix,
    hermitian_pairing,
    matrix,
    matvec,
    require_hermitianization,
    scale_matrix,
    validate_hermitianization,
    vector,
)


def _canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _nonnegative_int(value: object, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"{name} must be a nonnegative integer")
    return value


def _q(value: Fraction) -> str:
    return str(value)


def _g(value: GaussianRational) -> dict[str, str]:
    return {"re": _q(value.re), "im": _q(value.im)}


def _v(value: tuple[Fraction, ...]) -> list[str]:
    return [_q(entry) for entry in value]


def reference_problem() -> dict[str, Any]:
    return {
        "observer_rows": [[1, 0, 0, 0], [0, 1, 0, 0]],
        "complex_structure": [
            [0, -1, 0, 0],
            [1, 0, 0, 0],
            [0, 0, 0, -1],
            [0, 0, 1, 0],
        ],
        "left": [1, 2, 3, -1],
        "right": [-2, 1, 0, 4],
        "scalar": ["2", "-1"],
        "blind_difference": [0, 0, 1, -1],
        "enumeration_bound": 1,
        "incompatible_observer_rows": [[1, 0], [0, 2]],
        "plane_complex_structure": [[0, -1], [1, 0]],
    }


def produce(problem: Mapping[str, Any]) -> dict[str, Any]:
    observer = matrix(problem["observer_rows"])
    j = matrix(problem["complex_structure"])
    check = require_hermitianization(observer, j)
    g = gram_matrix(observer)
    x = vector(problem["left"])
    y = vector(problem["right"])
    if len(x) != check.dimension or len(y) != check.dimension:
        raise ValueError("submitted vectors do not inhabit the checked carrier")
    scalar = GaussianRational.of(*problem["scalar"])
    hx_y = hermitian_pairing(g, j, x, y)
    hz_x_y = hermitian_pairing(g, j, complex_scalar_action(scalar, j, x), y)
    expected_left = scalar.conjugate() * hx_y
    hx_zy = hermitian_pairing(g, j, x, complex_scalar_action(scalar, j, y))
    expected_right = scalar * hx_y
    self_x = hermitian_pairing(g, j, x, x)
    blind = vector(problem["blind_difference"])
    blind_report = matvec(observer, blind)
    blind_pairings = [hermitian_pairing(g, j, blind, basis) for basis in (
        tuple(Fraction(1 if i == k else 0) for i in range(check.dimension))
        for k in range(check.dimension)
    )]
    bound = _nonnegative_int(problem["enumeration_bound"], "enumeration_bound")
    radical_cases = 0
    radical_matches_kernel = True
    self_values_nonnegative = True
    for raw in itertools.product(range(-bound, bound + 1), repeat=check.dimension):
        candidate = vector(raw)
        report_zero = all(value == 0 for value in matvec(observer, candidate))
        self_pair = hermitian_pairing(g, j, candidate, candidate)
        radical_matches_kernel &= (self_pair == GaussianRational.of(0)) == report_zero
        self_values_nonnegative &= self_pair.im == 0 and self_pair.re >= 0
        radical_cases += 1
    opposite_j = scale_matrix(Fraction(-1), j)
    opposite_check = require_hermitianization(observer, opposite_j)
    e0 = vector([1, 0, 0, 0])
    e1 = vector([0, 1, 0, 0])
    positive_orientation = hermitian_pairing(g, j, e0, e1)
    negative_orientation = hermitian_pairing(g, opposite_j, e0, e1)
    bad_observer = matrix(problem["incompatible_observer_rows"])
    plane_j = matrix(problem["plane_complex_structure"])
    bad = validate_hermitianization(bad_observer, plane_j)
    return {
        "schema": "wdp-finite-hermitianization/v1",
        "problem_sha256": hashlib.sha256(_canonical(problem)).hexdigest(),
        "admission": {
            "dimension": check.dimension,
            "complex_square": check.complex_square,
            "gram_symmetric": check.gram_symmetric,
            "skew_adjoint": check.skew_adjoint,
            "isometry": check.isometry,
        },
        "pairing": {
            "h_left_right": _g(hx_y),
            "h_scalar_left_right": _g(hz_x_y),
            "conjugate_scalar_times_h": _g(expected_left),
            "h_left_scalar_right": _g(hx_zy),
            "scalar_times_h": _g(expected_right),
            "left_self": _g(self_x),
        },
        "radical": {
            "blind_report": _v(blind_report),
            "blind_basis_pairings": [_g(value) for value in blind_pairings],
            "enumerated_cases": radical_cases,
            "self_null_matches_observer_kernel": radical_matches_kernel,
            "self_values_nonnegative_real": self_values_nonnegative,
        },
        "orientation_nonselection": {
            "opposite_admitted": opposite_check.accepted,
            "positive": _g(positive_orientation),
            "negative": _g(negative_orientation),
            "pairings_differ": positive_orientation != negative_orientation,
        },
        "incompatible_control": {
            "complex_square": bad.complex_square,
            "skew_adjoint": bad.skew_adjoint,
            "isometry": bad.isometry,
            "accepted": bad.accepted,
        },
        "scope": {
            "derived": [
                "Gaussian-rational action from supplied J",
                "Hermitian form from supplied compatible Gram form",
                "Hermitian radical equals real-form radical",
                "exact finite rejection of incompatible J and observer data",
            ],
            "not_derived": [
                "selection of J or complex orientation",
                "norm or Hilbert completion",
                "Born probabilities",
                "states, dynamics, or physical realization",
            ],
        },
    }


def check(problem: Mapping[str, Any], receipt: Mapping[str, Any]) -> None:
    expected = produce(problem)
    if receipt != expected:
        raise ValueError("receipt does not replay from the bound problem")
    if not all(receipt["admission"][key] for key in (
        "complex_square", "gram_symmetric", "skew_adjoint", "isometry"
    )):
        raise ValueError("accepted package failed a Hermitianization law")
    pairing = receipt["pairing"]
    if pairing["h_scalar_left_right"] != pairing["conjugate_scalar_times_h"]:
        raise ValueError("first slot is not conjugate linear")
    if pairing["h_left_scalar_right"] != pairing["scalar_times_h"]:
        raise ValueError("second slot is not linear")
    if pairing["left_self"]["im"] != "0" or Fraction(pairing["left_self"]["re"]) < 0:
        raise ValueError("diagonal Hermitian value is not nonnegative real")
    radical = receipt["radical"]
    if not radical["self_null_matches_observer_kernel"]:
        raise ValueError("enumerated Hermitian self-null set differs from observer kernel")
    if not radical["self_values_nonnegative_real"]:
        raise ValueError("enumerated diagonal values violated positivity or reality")
    if not receipt["orientation_nonselection"]["pairings_differ"]:
        raise ValueError("orientation nonselection counterexample collapsed")
    if receipt["incompatible_control"]["accepted"]:
        raise ValueError("incompatible observer/J pair was accepted")


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
    print("finite-hermitianization replay: PASS")


if __name__ == "__main__":
    main()
