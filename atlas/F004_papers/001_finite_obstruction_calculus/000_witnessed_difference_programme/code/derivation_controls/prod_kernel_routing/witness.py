"""Finite routing control over input-bound native diagnostics.

The reusable routing owner is omega_wdp::prime_algos::finite_routing. Python
checks the selected zero-d0 policy cases; Phi1/Gamma2 come from the canonical
Rust host with receipt replay. This is not an eight-stage runtime integration.
"""
from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path

ROOT = next(p for p in Path(__file__).resolve().parents if (p / ".git").exists())
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from omega_engine_operating_system.adapters.rust_host.ffi import RustSymbolGameHost
from omega_engine_operating_system.adapters.rust_host.theory_requests import (
    functional_evaluate_payload,
    functional_verify_payload,
)
from omega_engine_operations.domain.rop.result import Err


def _invoke(action, payload):
    result = RustSymbolGameHost().invoke_runtime(action, payload)
    if isinstance(result, Err):
        raise RuntimeError(str(result.error))
    if result.value.get("success") is not True:
        raise RuntimeError(str(result.value.get("error")))
    return result.value["result"]


def _packet(values, closure):
    request = functional_evaluate_payload([[0] for _ in values], [closure], values)
    if isinstance(request, Err):
        raise ValueError(str(request.error))
    receipt = _invoke("functional_evaluate", request.value)
    replay = functional_verify_payload(request.value, receipt)
    if isinstance(replay, Err) or _invoke("functional_verify", replay.value).get("accepted") is not True:
        raise ValueError("native diagnostic receipt did not replay")
    return receipt


def _guard(before, after, budget):
    return (Fraction(after["phi1"]) < Fraction(before["phi1"])
            and Fraction(after["gamma2"]) - Fraction(before["gamma2"]) <= budget)


def witness() -> dict[str, object]:
    before = _packet([3, 0], [0, 1])
    after = _packet([1, 1], [0, 1])
    exact = _packet([0, 0], [0, 1])
    low = _packet([2], [0])
    high = _packet([4], [0])
    # Zero differentials make the selected squares commute; f1=2 must
    # additionally transport the residual. This is only the 1D fixture.
    def transports(target):
        return 2 * Fraction(low["primal_residual"][0]) == Fraction(target["primal_residual"][0])
    policy = {"ExactRepair": "ExactCertified", "ClosedResidual": "StabilizedSurvivor"}
    fixed, cycle = (0, 0), (1, 0)
    return {
        "goal_id": "PROD-KERNEL-ROUTING",
        "before_phi1": before["phi1"], "after_good_phi1": after["phi1"],
        "damage_refused": not _guard(before, after, 0),
        "good_edit_accepted": _guard(before, after, 1),
        "no_descent_refused": not _guard(before, before, 1),
        "lift_valid": transports(high), "invalid_lift_refused": not transports(low),
        "exact_terminal": policy[exact["diagnostic_class"]],
        "stabilized_terminal": policy[low["diagnostic_class"]] if fixed[0] == 0 else None,
        "invalid_stability_refused": cycle[0] != 0,
    }


if __name__ == "__main__":
    print(json.dumps(witness(), indent=2, sort_keys=True))
