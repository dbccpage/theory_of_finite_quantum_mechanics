"""Typed square signs, truthful schemas, and local policy failures."""

from dataclasses import replace

import numpy as np
import pytest
from coda_higher_cell.bicomplex_ddc import (
    DoubleBicomplex,
    bicomplex_curvature_tensor,
    ddc_trace_sequence_evaluation,
    semigroup_defect_tensor,
)
from coda_higher_cell.prime_triad_bridge import (
    PrimeTriadCarrier,
    adapter_loss_ledger,
    can_continue_predicate,
    prime_triad_carrier_declaration,
)
from coda_higher_cell.simplicial_complex import SimplicialComplex


def carrier(**updates):
    return replace(
        PrimeTriadCarrier(
            "cell",
            2,
            (0, 1, 2),
            0.5,
            0.05,
            True,
            50,
            "boundary:triangle",
            "observation:fixed-B",
            "witness:example",
            "state:current",
        ),
        **updates,
    )


def test_commuting_double_complex_is_nilpotent():
    double = DoubleBicomplex(SimplicialComplex([(0, 1, 2)]), num_memory_grades=4)
    for p in range(3):
        for q in range(2):
            assert np.array_equal(
                double.vertical_differential(p, q + 1) @ double.vertical_differential(p, q),
                np.zeros((double.complex.num_simplices(p),) * 2),
            )
        h = double.horizontal_coboundary(p)
        c = bicomplex_curvature_tensor(
            h, h, double.vertical_differential(p, 0), double.vertical_differential(p + 1, 0)
        )
        assert np.allclose(c, 0)


def test_noncommuting_square_and_totalized_sign():
    h, v0, v1 = np.array([[1.0, -1.0]]), np.eye(2), np.array([[2.0]])
    c = bicomplex_curvature_tensor(h, h, v0, v1)
    assert np.array_equal(c, -h)
    # Block order: (0,0), (1,0), (0,1), (1,1), sizes 2,1,2,1.
    total = np.zeros((6, 6))
    total[2:3, 0:2] = h
    total[3:5, 0:2] = v0
    total[5:6, 2:3] = -v1  # (-1)^p on p=1
    total[5:6, 3:5] = h
    assert np.array_equal((total @ total)[5:6, 0:2], c)
    # Starting at odd horizontal degree reverses the mixed block.
    total[3:5, 0:2] = -v0
    total[5:6, 2:3] = v1
    assert np.array_equal((total @ total)[5:6, 0:2], -c)


def test_semigroup_coefficient_checks_tangency_and_inputs():
    p = np.array([[1.0, 1.0], [0.0, 0.0]])  # genuinely oblique
    a = np.array([[0.0, 1.0], [1.0, 0.0]])
    n = np.array([-1.0, 1.0])
    result, flag = semigroup_defect_tensor(p, a, n, np.zeros(2))
    assert flag and np.array_equal(result, p @ a @ n)
    _, flag = semigroup_defect_tensor(p, a, n, np.array([0.0, 1.0]))
    assert not flag
    with pytest.raises(ValueError):
        semigroup_defect_tensor(p, a, np.ones(2), np.zeros(2))
    with pytest.raises(ValueError):
        semigroup_defect_tensor(2 * np.eye(2), a, n, np.zeros(2))


def test_ddc_schema_never_claims_a_verified_receipt():
    receipt = ddc_trace_sequence_evaluation("triangle", 1.5)
    assert receipt["trace_sequence"] == ["E", "R", "C", "Lambda", "D", "M", "T"]
    assert receipt["schema_complete"] and not receipt["receipt_verified"]
    assert all(row["status"] == "NOT_EVALUATED" for row in receipt["trace_log"])
    limited = ddc_trace_sequence_evaluation("triangle", 1.5, budget=3)
    assert limited["budget_used"] == 3 and not limited["schema_complete"]


def test_carrier_declaration_requires_evidence_identifiers():
    assert prime_triad_carrier_declaration(carrier())["declaration_valid"]
    missing = carrier(observation_map_id=None)
    assert not prime_triad_carrier_declaration(missing)["declaration_valid"]
    assert "HALT_MISSING_DECLARATION" in can_continue_predicate(missing, 4)[1]


def test_adapter_loss_requires_aligned_operators():
    z = np.diag([1, -1])
    assert adapter_loss_ledger(z, [-z]) == pytest.approx(4)
    assert adapter_loss_ledger(z, [z]) == 0
    assert adapter_loss_ledger(z, []) == pytest.approx(2)
    with pytest.raises(ValueError):
        adapter_loss_ledger(z, [np.eye(3)])
    with pytest.raises(ValueError):
        adapter_loss_ledger(1.5, [0.9])


@pytest.mark.parametrize(
    "updates,reason",
    [
        ({"residual_norm": 0}, "HALT_ZERO_RESIDUAL"),
        ({"dimension_k": 4, "simplex": (0, 1, 2, 3, 4)}, "HALT_DIMENSION_CAP"),
        ({"adapter_loss": 1e-8}, "HALT_STAGNATION"),
        ({"budget_remaining": 0}, "HALT_BUDGET_DEPLETION"),
        ({"witness_verified": False}, "HALT_UNVERIFIED_PROMOTION"),
    ],
)
def test_prime_stop_policies(updates, reason):
    allowed, message = can_continue_predicate(carrier(**updates), 4)
    assert not allowed and reason in message


def test_cycle_requires_declared_complete_state_identity():
    c = carrier()
    assert can_continue_predicate(c, 4, history_residuals=[0.5] * 4)[0]
    assert not can_continue_predicate(c, 4, history_states=["state:current"])[0]
    assert can_continue_predicate(c, 4, history_states=["cell"])[0]
    assert can_continue_predicate(carrier(state_fingerprint=None), 4, history_states=["cell"])[0]


@pytest.mark.parametrize(
    "updates",
    [
        {"dimension_k": 3},
        {"simplex": (0, 0, 2)},
        {"residual_norm": np.nan},
        {"adapter_loss": -1},
        {"budget_remaining": -1},
        {"witness_verified": "yes"},
        {"observation_map_id": ""},
        {"carrier_id": ""},
    ],
)
def test_invalid_carriers(updates):
    with pytest.raises(ValueError):
        carrier(**updates)


def test_invalid_square_and_schema_inputs():
    with pytest.raises(ValueError):
        bicomplex_curvature_tensor(np.ones((1, 2)), np.ones((2, 3)), np.eye(2), np.eye(1))
    with pytest.raises(ValueError):
        ddc_trace_sequence_evaluation("triangle", np.nan)
    with pytest.raises(ValueError):
        ddc_trace_sequence_evaluation("triangle", 1, -1)
    with pytest.raises(ValueError):
        DoubleBicomplex(SimplicialComplex([]), 0)
