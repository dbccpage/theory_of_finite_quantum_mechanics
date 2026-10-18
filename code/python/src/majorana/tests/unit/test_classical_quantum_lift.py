from __future__ import annotations
"""Unit test suite for Classical L1 <-> Quantum L2 Up/Down Functor Lift and Row-Sparsity.

Direct Python verification of Lean 4 theorems in:
- `classical_quantum_lift.lean`: `QuantumL2Amplitude.round_trip_idempotency`
- `row_sparsity_descent.lean`: `RowAction.phase_interference_exists`
"""


import numpy as np
import pytest

from omega_engine.crates.lift import (
    ClassicalL1Density,
    QuantumL2State,
    up_functor_lift,
    down_functor_shadow,
    verify_round_trip_idempotency,
    check_row_sparsity,
    verify_phase_interference_contradiction,
)


def test_up_down_functor_round_trip_idempotency():
    """Verify Lean 4 theorem round_trip_idempotency: Shadow(Lift(p, phase)) == p."""
    probs = [0.4, 0.25, 0.35]
    density = ClassicalL1Density(probabilities=probs)
    phases = [0.0, np.pi / 4, -np.pi / 3]

    assert verify_round_trip_idempotency(density, phases)


def test_row_sparsity_classification():
    """Verify check_row_sparsity for sparse vs dense transformation matrices."""
    perm_matrix = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=float)
    report_perm = check_row_sparsity(perm_matrix)
    assert report_perm.is_row_sparse is True
    assert report_perm.interference_detected is False

    dense_matrix = np.array([[1, 1], [1, -1]], dtype=float) / np.sqrt(2)
    report_dense = check_row_sparsity(dense_matrix)
    assert report_dense.is_row_sparse is False
    assert report_dense.interference_detected is True


def test_phase_interference_contradiction_dense_matrix():
    """Verify Lean 4 theorem phase_interference_exists: dense unitary creates phase-dependent L1 output density."""
    h_matrix = np.array([[1, 1], [1, -1]], dtype=float) / np.sqrt(2)
    p = [0.5, 0.5]
    ph1 = [0.0, 0.0]
    ph2 = [0.0, np.pi]

    has_interference = verify_phase_interference_contradiction(h_matrix, p, ph1, ph2)
    assert has_interference is True



