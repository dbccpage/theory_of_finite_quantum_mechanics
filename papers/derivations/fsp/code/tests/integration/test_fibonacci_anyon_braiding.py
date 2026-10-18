"""
test_fibonacci_anyon_braiding.py — Integration tests for non-abelian Fibonacci anyon braiding,
pentagon consistency, quantum state leakage, and GIN mode indexing.

AuthorityEffect: None.
Reference: sealed-derivation-v1 (3100c4e)
"""

from __future__ import annotations

import math
from pathlib import Path
import sys

import pytest

code_dir = Path(__file__).resolve().parent.parent.parent
if str(code_dir) not in sys.path:
    sys.path.insert(0, str(code_dir))

from fibonacci_anyon_braiding import FibonacciAnyonBraidingEngine, FibonacciAnyonModel


def test_golden_ratio_quantum_dimensions() -> None:
    """Verifies golden ratio quantum dimensions and total quantum dimension."""
    model = FibonacciAnyonModel()
    d_1, d_tau, total_d = model.compute_quantum_dimensions()

    phi = (1.0 + math.sqrt(5.0)) / 2.0
    assert abs(d_1 - 1.0) < 1e-12
    assert abs(d_tau - phi) < 1e-12
    # Fundamental Fibonacci relation: d_tau^2 = d_tau + 1
    assert abs(d_tau**2 - (d_tau + 1.0)) < 1e-12
    # Total dimension: D = sqrt(1 + phi^2) = sqrt(2 + phi)
    assert abs(total_d - math.sqrt(2.0 + phi)) < 1e-12


def test_f_matrix_orthogonality_and_pentagon_axiom() -> None:
    """Verifies F-matrix is orthogonal involution and satisfies Mac Lane pentagon equation."""
    model = FibonacciAnyonModel()
    f = model.get_f_matrix()

    # F is symmetric and real
    assert abs(f[0][1] - f[1][0]) < 1e-12
    # F^2 == I
    f2_00 = f[0][0]**2 + f[0][1]**2
    f2_01 = f[0][0] * f[0][1] + f[0][1] * f[1][1]
    f2_11 = f[1][0]**2 + f[1][1]**2
    assert abs(f2_00 - 1.0) < 1e-12
    assert abs(f2_01 - 0.0) < 1e-12
    assert abs(f2_11 - 1.0) < 1e-12

    # Mac Lane pentagon axiom across all 4-anyon fusion trees
    pentagon_err = model.verify_pentagon_equation()
    assert pentagon_err < 1e-12


def test_artin_braid_relations_and_non_commutativity() -> None:
    """Verifies braid relation sigma_1 sigma_2 sigma_1 == sigma_2 sigma_1 sigma_2 and [sigma_1, sigma_2] != 0."""
    model = FibonacciAnyonModel()

    # Exact braid relation
    braid_err = model.verify_artin_braid_relation()
    assert braid_err < 1e-12

    # Non-commutativity: [sigma_1, sigma_2] != 0
    _, comm_norm = model.compute_commutator()
    assert comm_norm > 1.5
    assert abs(comm_norm - 1.798907) < 1e-3


def test_non_contractible_commutator_cochain_holonomy() -> None:
    """Verifies non-contractibility of commutator loop holonomy and positive curvature Gamma_2."""
    model = FibonacciAnyonModel()
    hol, dist, is_contractible, gamma_2 = model.compute_commutator_holonomy()

    assert not is_contractible
    assert dist > 1.5
    assert gamma_2 > 1.5
    assert abs(dist - 1.798907) < 1e-3


def test_quantum_state_leakage_under_scalar_projection() -> None:
    """Verifies that scalar projection P_0 = |0><0| suffers exact quantum state leakage phi^-1."""
    model = FibonacciAnyonModel()
    leakage = model.compute_quantum_state_leakage()

    # Exact closed-form value: phi^-1 = (sqrt(5) - 1) / 2 approx 0.618034
    expected_leakage = (math.sqrt(5.0) - 1.0) / 2.0
    assert abs(leakage - expected_leakage) < 1e-12


def test_schur_lemma_involution_obstruction_and_open_sign_routing() -> None:
    """Verifies Schur's Lemma involution obstruction and deterministic BQNF routing to OpenSignObstruction."""
    model = FibonacciAnyonModel()
    norm_xi, is_obstructed = model.evaluate_involution_obstruction()
    assert is_obstructed
    assert norm_xi > 2.0

    engine = FibonacciAnyonBraidingEngine(in_memory=True)
    receipt = engine.audit_fibonacci_braiding(model)
    engine.close()

    assert not receipt.is_holonomy_contractible
    assert receipt.cochain_curvature_gamma_2 > 0.0
    assert receipt.schur_lemma_involution_obstructed
    assert receipt.uncancelled_defect_mass_phi_1 > 2.0
    assert receipt.terminal_route == "OpenSignObstruction"


def test_gin_mode_posting_list_resolution() -> None:
    """Verifies relational SQLite GIN mode posting list queries."""
    model = FibonacciAnyonModel()
    engine = FibonacciAnyonBraidingEngine(in_memory=True)
    receipt = engine.audit_fibonacci_braiding(model)

    # Check posting index contains expected modes
    assert 1 in engine.posting_index  # Vacuum channel |0>
    assert 2 in engine.posting_index  # Non-abelian channel |1>
    assert 3 in engine.posting_index  # sigma_1 loop
    assert 4 in engine.posting_index  # sigma_2 loop
    assert 5 in engine.posting_index  # commutator cycle

    # Query SQLite database directly
    c = engine.conn.cursor()
    c.execute("SELECT COUNT(*) FROM FermionConfigurations WHERE model_name = ?;", (model.model_id,))
    cfg_count = c.fetchone()[0]
    assert cfg_count == 2

    c.execute("SELECT COUNT(*) FROM GinModePostingList WHERE mode_id = 5;")
    comm_mode_count = c.fetchone()[0]
    assert comm_mode_count == 2  # Both configurations share the commutator cycle boundary

    engine.close()
