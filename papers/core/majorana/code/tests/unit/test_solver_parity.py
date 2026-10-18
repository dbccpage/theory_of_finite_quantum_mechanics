"""Cross-language parity for the Phi-1 L1 boundary solver.

Rust is the PROD face and generates the fixture; this file is the check that
the Python mirror still agrees with it. Both the solutions and the refusal
classes are compared, because the two implementations first diverged in
refusal behaviour, not in arithmetic: Python validated the carrier and Rust did
not, so a malformed carrier that Python refused cleanly panicked in Rust on an
out-of-range node index.

Regenerate the fixture from the Rust side, never by hand:

    cargo test -j 1 -p omega_solvers --test solver_parity -- --ignored regenerate

Integers travel as decimal strings. The values are small, but i128 exceeds what
a JSON number round-trips reliably, and a fixture that quietly loses precision
at the boundary is worse than no fixture.

AuthorityEffect: None. Two implementations agreeing is evidence, not proof.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from omega_engine.crates.solver.solv_phi1_l1_boundary import (
    Boundary1,
    BoundaryEdge,
    solve_l1_boundary,
)
from omega_engine.crates.type.network_simplex_error import NetworkSimplexError

FIXTURE = (
    Path(__file__).resolve().parents[1]
    / "crates_rs"
    / "omega_solvers"
    / "tests"
    / "fixtures"
    / "phi1_l1_boundary_parity.json"
)


def _load() -> dict:
    if not FIXTURE.exists():
        pytest.fail(
            f"parity fixture missing at {FIXTURE}. Generate it from Rust:\n"
            "  cargo test -j 1 -p omega_solvers --test solver_parity -- --ignored regenerate"
        )
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def _cases() -> list[dict]:
    return _load()["cases"]


def _ids() -> list[str]:
    return [c["name"] for c in _cases()]


def _boundary(case: dict) -> Boundary1:
    return Boundary1(
        num_vertices=int(case["num_vertices"]),
        edges=[
            BoundaryEdge(tail=int(e["tail"]), head=int(e["head"]), weight=int(e["weight"]))
            for e in case["edges"]
        ],
    )


def _refusal_payload(err: NetworkSimplexError) -> dict[str, str]:
    """The payload as the Rust generator writes it: every value a decimal string."""
    return {key: str(value) for key, value in err.data.items()}


def test_the_fixture_is_the_expected_schema() -> None:
    fixture = _load()
    assert fixture["schema"] == "omega.parity.phi1_l1_boundary.v1"
    assert fixture["cases"], "an empty fixture would pass every parity test below"


@pytest.mark.parametrize("case", _cases(), ids=_ids())
def test_python_matches_the_rust_solver(case: dict) -> None:
    boundary = _boundary(case)
    x = [int(v) for v in case["x"]]
    expected = case["outcome"]

    if "err" in expected:
        with pytest.raises(NetworkSimplexError) as caught:
            solve_l1_boundary(boundary, x)
        assert caught.value.kind == expected["err"]["class"], (
            f"{case['name']}: Rust refuses with {expected['err']['class']}, "
            f"Python refuses with {caught.value.kind}"
        )
        assert _refusal_payload(caught.value) == expected["err"]["payload"], (
            f"{case['name']}: same refusal class, different payload"
        )
        return

    solution = solve_l1_boundary(boundary, x)
    ok = expected["ok"]

    assert str(solution.objective) == ok["objective"], (
        f"{case['name']}: objective differs. The objective is the part of the "
        f"solution that is uniquely determined, so a mismatch here is a real "
        f"disagreement rather than a tie broken differently."
    )
    assert [str(v) for v in solution.z] == ok["z"]
    assert [str(v) for v in solution.vertex_potential] == ok["vertex_potential"]
    assert [str(v) for v in solution.reduced_costs] == ok["reduced_costs"]


def test_the_fixture_still_covers_every_refusal_class_python_can_raise() -> None:
    """Guards against the fixture drifting into success-only coverage.

    The divergence this file exists to catch was in refusal classification, so a
    fixture that stopped exercising refusals would keep passing while losing the
    thing it was written for.
    """
    classes = {
        c["outcome"]["err"]["class"] for c in _cases() if "err" in c["outcome"]
    }
    assert {
        "UnbalancedDemand",
        "DemandLengthMismatch",
        "NegativeWeight",
        "InvalidCarrier",
    } <= classes, f"fixture no longer exercises every refusal class; has {sorted(classes)}"


def test_a_malformed_carrier_refuses_rather_than_raising_indexerror() -> None:
    """The specific defect, pinned on the Python side too.

    Python was already correct here; this asserts it stays correct, so that a
    future simplification of `_validate_boundary` cannot quietly reintroduce the
    crash that Rust had.
    """
    boundary = Boundary1(num_vertices=2, edges=[BoundaryEdge(tail=0, head=7, weight=1)])
    with pytest.raises(NetworkSimplexError) as caught:
        solve_l1_boundary(boundary, [1, -1])
    assert caught.value.kind == NetworkSimplexError.INVALID_CARRIER
