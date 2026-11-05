"""Source-bound producer/checker for the finite state/effect readout."""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any, Mapping

from hermitianization.model import GaussianRational

from .model import (
    BinaryEffectFactor,
    StateFactor,
    add,
    born_numerator,
    born_probability,
    complement_probability,
    depolarized_probability,
    gmatrix,
    gram,
    identity,
    phase_scale,
    trace,
    trace_probability,
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
        "state_factor": [[[1, 0], [1, 0]], [[0, 0], [0, 0]]],
        "accept_factor": [[[1, 0], [0, 0]], [[0, 0], [0, 0]]],
        "reject_factor": [[[0, 0], [0, 0]], [[0, 0], [1, 0]]],
        "phase": ["3/5", "4/5"],
        "depolarization_weight": "1/2",
        "sharp_state_factor": [[[1, 0], [0, 0]], [[0, 0], [0, 0]]],
        "incomplete_reject_factor": [[[1, 0], [0, 0]], [[0, 0], [0, 0]]],
    }


def produce(problem: Mapping[str, Any]) -> dict[str, Any]:
    state = StateFactor(gmatrix(problem["state_factor"]))
    effect = BinaryEffectFactor(
        gmatrix(problem["accept_factor"]), gmatrix(problem["reject_factor"])
    )
    p = born_probability(state, effect)
    q = complement_probability(state, effect)
    trace_p = trace_probability(state, effect)
    phase = GaussianRational.of(*problem["phase"])
    phase_state = StateFactor(phase_scale(phase, state.factor))
    phase_p = born_probability(phase_state, effect)
    weight = Fraction(problem["depolarization_weight"])
    alternate = depolarized_probability(state, effect, weight)
    complement_effect = BinaryEffectFactor(effect.reject, effect.accept)
    alternate_complement = depolarized_probability(state, complement_effect, weight)
    sharp_state = StateFactor(gmatrix(problem["sharp_state_factor"]))
    sharp_p = born_probability(sharp_state, effect)
    sharp_alternate = depolarized_probability(sharp_state, effect, weight)
    incomplete_rejected = False
    try:
        BinaryEffectFactor(
            gmatrix(problem["accept_factor"]),
            gmatrix(problem["incomplete_reject_factor"]),
        )
    except ValueError:
        incomplete_rejected = True
    zero_state_rejected = False
    try:
        StateFactor(gmatrix([[[0, 0], [0, 0]], [[0, 0], [0, 0]]]))
    except ValueError:
        zero_state_rejected = True
    return {
        "schema": "wdp-finite-state-effect-readout/v1",
        "problem_sha256": hashlib.sha256(_canonical(problem)).hexdigest(),
        "state": {
            "factor": _m(state.factor),
            "density": _m(state.density),
            "trace": _g(trace(state.density)),
            "denominator": _q(state.denominator),
        },
        "effect": {
            "accept": _m(effect.effect),
            "reject": _m(effect.complement),
            "sum": _m(add(effect.effect, effect.complement)),
            "identity": _m(identity(effect.dimension)),
        },
        "readout": {
            "accept_numerator": _q(born_numerator(state, effect.accept)),
            "accept_probability": _q(p),
            "reject_probability": _q(q),
            "sum": _q(p + q),
            "trace_probability": _q(trace_p),
            "in_unit_interval": 0 <= p <= 1 and 0 <= q <= 1,
        },
        "phase_control": {
            "phase_norm": _q(phase.norm()),
            "density_unchanged": phase_state.density == state.density,
            "probability_unchanged": phase_p == p,
        },
        "readout_nonselection": {
            "weight": _q(weight),
            "base_probability": _q(p),
            "alternate_probability": _q(alternate),
            "alternate_complement": _q(alternate_complement),
            "sharp_base": _q(sharp_p),
            "sharp_alternate": _q(sharp_alternate),
            "both_binary_normalized": alternate + alternate_complement == 1,
            "distinct_on_sharp_input": sharp_p != sharp_alternate,
        },
        "refusals": {
            "zero_state_rejected": zero_state_rejected,
            "incomplete_effect_rejected": incomplete_rejected,
        },
        "scope": {
            "derived": [
                "positive normalized Gram-factor states",
                "complete binary Gram-factor effects",
                "exact trace/Frobenius readout equality",
                "probabilities in the rational unit interval",
            ],
            "not_derived": [
                "selection of the trace/Born readout",
                "coverage of every rational positive matrix",
                "physical state or effect interpretation",
                "dynamics, locality, or continuum reconstruction",
            ],
        },
    }


def check(problem: Mapping[str, Any], receipt: Mapping[str, Any]) -> None:
    expected = produce(problem)
    if receipt != expected:
        raise ValueError("receipt does not replay from the bound problem")
    if receipt["state"]["trace"] != {"re": "1", "im": "0"}:
        raise ValueError("state is not trace normalized")
    if receipt["effect"]["sum"] != receipt["effect"]["identity"]:
        raise ValueError("effect factors do not resolve the identity")
    readout = receipt["readout"]
    if readout["sum"] != "1" or not readout["in_unit_interval"]:
        raise ValueError("binary readout is not normalized in [0,1]")
    if readout["accept_probability"] != readout["trace_probability"]:
        raise ValueError("factor readout differs from the trace pairing")
    if not all(receipt["phase_control"][key] for key in (
        "density_unchanged", "probability_unchanged"
    )):
        raise ValueError("unit phase changed the admitted state/readout")
    if not receipt["readout_nonselection"]["both_binary_normalized"]:
        raise ValueError("alternate binary readout is not normalized")
    if not receipt["readout_nonselection"]["distinct_on_sharp_input"]:
        raise ValueError("readout nonselection control collapsed")
    if not all(receipt["refusals"].values()):
        raise ValueError("malformed state/effect input was not refused")


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
    print("finite-state-effect-readout replay: PASS")


if __name__ == "__main__":
    main()
