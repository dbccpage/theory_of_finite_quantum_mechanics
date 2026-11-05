"""Source-bound producer/checker for finite process composition."""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any, Mapping

from hermitianization.model import GaussianRational
from state_effect_readout.model import gmatrix, identity

from .model import (
    EnsembleState,
    KrausProcess,
    apply_process,
    branch_probability,
    compose_process,
    conditioned_branch,
    exact_standard_real_hadamard_available,
    identity_instrument_single,
    identity_instrument_split,
    phase_s_gate,
    tensor_process,
    unitary_process,
    x_gate,
)


def _canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _q(value: Fraction) -> str:
    return str(value)


def _g(value: GaussianRational) -> dict[str, str]:
    return {"re": _q(value.re), "im": _q(value.im)}


def _m(value) -> list[list[dict[str, str]]]:
    return [[_g(entry) for entry in row] for row in value]


def reference_problem() -> dict[str, Any]:
    return {
        "plus_factor": [[[1, 0], [1, 0]], [[0, 0], [0, 0]]],
        "basis_zero_factor": [[[1, 0], [0, 0]], [[0, 0], [0, 0]]],
        "measurement_operators": [
            [[[1, 0], [0, 0]], [[0, 0], [0, 0]]],
            [[[0, 0], [0, 0]], [[0, 0], [1, 0]]],
        ],
    }


def produce(problem: Mapping[str, Any]) -> dict[str, Any]:
    plus = EnsembleState((gmatrix(problem["plus_factor"]),))
    basis_zero = EnsembleState((gmatrix(problem["basis_zero_factor"]),))
    x = unitary_process(x_gate())
    s = unitary_process(phase_s_gate())
    sequential = apply_process(apply_process(basis_zero, x), s)
    composite = apply_process(basis_zero, compose_process(x, s))
    measurement = KrausProcess(tuple(gmatrix(op) for op in problem["measurement_operators"]))
    probabilities = tuple(branch_probability(plus, measurement, i) for i in range(2))
    conditioned = tuple(conditioned_branch(plus, measurement, i) for i in range(2))
    single = identity_instrument_single(2)
    split = identity_instrument_split(2)
    single_output = apply_process(plus, single)
    split_output = apply_process(plus, split)
    split_probabilities = tuple(branch_probability(plus, split, i) for i in range(2))
    tensor = tensor_process(x, unitary_process(identity(2)))
    tensor_input = EnsembleState((gmatrix([
        [1, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ]),))
    tensor_output = apply_process(tensor_input, tensor)
    incomplete_rejected = False
    try:
        KrausProcess((gmatrix(problem["measurement_operators"][0]),))
    except ValueError:
        incomplete_rejected = True
    return {
        "schema": "wdp-finite-process-composition/v1",
        "problem_sha256": hashlib.sha256(_canonical(problem)).hexdigest(),
        "sequential": {
            "sequential_density": _m(sequential.density),
            "composite_density": _m(composite.density),
            "equal": sequential.density == composite.density,
            "mass_preserved": sequential.total_mass == basis_zero.total_mass,
        },
        "measurement": {
            "probabilities": [_q(value) for value in probabilities],
            "sum": _q(sum(probabilities, Fraction(0))),
            "conditioned_densities": [
                _m(branch.density) if branch is not None else None for branch in conditioned
            ],
        },
        "instrument_nonselection": {
            "single_output": _m(single_output.density),
            "split_output": _m(split_output.density),
            "unconditioned_equal": single_output.density == split_output.density,
            "single_branch_probabilities": ["1"],
            "split_branch_probabilities": [_q(value) for value in split_probabilities],
            "labelled_reports_differ": split_probabilities != (Fraction(1),),
        },
        "tensor": {
            "dimension": tensor.dimension,
            "input_mass": _q(tensor_input.total_mass),
            "output_mass": _q(tensor_output.total_mass),
            "output_density": _m(tensor_output.density),
        },
        "gate_boundary": {
            "x_exact": True,
            "phase_s_exact": True,
            "standard_real_hadamard_exact_over_q_i": exact_standard_real_hadamard_available(),
            "missing_scalar_for_standard_real_representative": "sqrt(1/2)",
            "gaussian_rational_phase_multiple": "(1+i)/2 * [[1,1],[1,-1]]",
        },
        "refusals": {"incomplete_process_rejected": incomplete_rejected},
        "scope": {
            "derived": [
                "complete finite Kraus-family trace preservation",
                "sequential branch composition",
                "conditioned branch states",
                "finite tensor product of certified processes",
            ],
            "not_derived": [
                "physical process or outcome-label selection",
                "standard real Hadamard over Q(i)",
                "approximate gate universality",
                "Bell locality or continuum dynamics",
            ],
        },
    }


def check(problem: Mapping[str, Any], receipt: Mapping[str, Any]) -> None:
    expected = produce(problem)
    if receipt != expected:
        raise ValueError("receipt does not replay from the bound problem")
    if not receipt["sequential"]["equal"] or not receipt["sequential"]["mass_preserved"]:
        raise ValueError("sequential/composite process mismatch")
    if receipt["measurement"]["sum"] != "1":
        raise ValueError("measurement branches are not normalized")
    instrument = receipt["instrument_nonselection"]
    if not instrument["unconditioned_equal"] or not instrument["labelled_reports_differ"]:
        raise ValueError("instrument-label nonselection control collapsed")
    if receipt["tensor"]["input_mass"] != receipt["tensor"]["output_mass"]:
        raise ValueError("tensor process did not preserve mass")
    if receipt["gate_boundary"]["standard_real_hadamard_exact_over_q_i"]:
        raise ValueError("false exact Hadamard admitted over Q(i)")
    if not all(receipt["refusals"].values()):
        raise ValueError("incomplete process was not refused")


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
    print("finite-process-composition replay: PASS")


if __name__ == "__main__":
    main()
