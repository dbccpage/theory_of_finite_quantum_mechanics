"""Tests for the Cochain Holonomy Bridge linking PO-034 to PO-035 and Cycles 005-007.

AuthorityEffect: None.
"""

from __future__ import annotations

import math

import numpy as np
import pytest

from coda_higher_cell.cochain_holonomy_bridge import (
    build_3simplex_cell_complex,
    compute_boundary_face_holonomies,
    compute_quotient_stickiness_lp,
    evaluate_cochain_holonomy_bridge,
    evaluate_discrete_continuum_membrane,
    evaluate_hamiltonian_defect_velocity,
    map_edge_interactions_to_cochain,
)
from coda_higher_cell.k_cell_retraction import embed_local_operator
from coda_higher_cell.simplicial_complex import simplicial_coboundary_matrix

X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z_OP = np.array([[1, 0], [0, -1]], dtype=complex)
RHO0 = np.array([[1.0, 0.0], [0.0, 0.0]], dtype=complex)
RHO_PLUS = np.array([[0.5, 0.5], [0.5, 0.5]], dtype=complex)


def test_single_site_hamiltonian_has_zero_defect_velocity():
    """Single-site Hamiltonians generate purely tangent perturbations with zero defect speed."""
    dims = [2, 2, 2, 2]
    rhos = [RHO0, RHO_PLUS, RHO0, RHO_PLUS]

    # Sum of 1-local operators
    h_single = sum(
        embed_local_operator(op, [site], dims)
        for site, op in enumerate([X, Y, Z_OP, X])
    )

    res = evaluate_hamiltonian_defect_velocity(h_single, rhos, dims)

    assert res.defect_velocity_nu == pytest.approx(0.0, abs=1e-10)
    assert res.normal_norm == pytest.approx(0.0, abs=1e-10)
    assert res.tangent_norm > 0.0
    assert res.marginal_preservation_passed is True
    assert res.normal_annihilation_passed is True
    for trace_val in res.single_site_marginal_traces_normal:
        assert trace_val == pytest.approx(0.0, abs=1e-10)


def test_two_site_interaction_defect_and_marginal_annihilation():
    """2-site entangling interaction generates nu > 0 while single-site marginals vanish.

    This directly demonstrates Cycle 007's no-signalling core: local single-site
    measurements cannot detect the instantaneous entangling defect velocity.
    """
    dims = [2, 2, 2, 2]
    rhos = [RHO0] * 4

    # 2-site interaction on sites (1, 2)
    h_local = np.kron(X, X)
    h12 = embed_local_operator(h_local, [1, 2], dims)

    res = evaluate_hamiltonian_defect_velocity(h12, rhos, dims)

    # Entangling velocity is strictly positive
    assert res.defect_velocity_nu == pytest.approx(2.0, abs=1e-10)
    assert res.normal_norm == pytest.approx(2.0, abs=1e-10)
    assert res.tangent_norm == pytest.approx(0.0, abs=1e-10)

    # All single-site marginals of Q(Z) vanish identically
    assert res.marginal_preservation_passed is True
    assert res.normal_annihilation_passed is True
    for trace_val in res.single_site_marginal_traces_normal:
        assert trace_val == pytest.approx(0.0, abs=1e-10)


def test_3simplex_cochain_mapping_and_face_holonomies():
    """Simplicial 3-simplex cell maps 2-site interaction bonds to boundary face holonomies."""
    k_cell = build_3simplex_cell_complex()

    assert k_cell.num_simplices(0) == 4
    assert k_cell.num_simplices(1) == 6
    assert k_cell.num_simplices(2) == 4
    assert k_cell.num_simplices(3) == 1

    # Isolated bond on edge (1, 2)
    couplings = {(1, 2): 1.5}
    delta = map_edge_interactions_to_cochain(k_cell, couplings)

    assert delta.shape == (6,)
    # Edge (1, 2) is at index 3 in [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
    assert delta[3] == 1.5

    # Compute boundary face holonomies Gamma_2 = d^1 delta
    gamma2 = compute_boundary_face_holonomies(k_cell, delta)
    assert gamma2.shape == (4,)

    # Faces are: 0: (0, 1, 2), 1: (0, 1, 3), 2: (0, 2, 3), 3: (1, 2, 3)
    # Edge (1, 2) is incident to face 0 and face 3, but not face 1 or face 2
    assert abs(gamma2[0]) > 0.0
    assert abs(gamma2[3]) > 0.0
    assert gamma2[1] == pytest.approx(0.0, abs=1e-14)
    assert gamma2[2] == pytest.approx(0.0, abs=1e-14)

    # Check Bianchi identity d^1 @ d^0 == 0
    d0 = simplicial_coboundary_matrix(k_cell, 0)
    d1 = simplicial_coboundary_matrix(k_cell, 1)
    assert np.allclose(d1 @ d0, 0.0, atol=1e-14)


def test_gauge_invariance_and_quotient_stickiness():
    """Pure gauge 0-cochains produce zero face holonomy; loops produce irreducible stickiness."""
    k_cell = build_3simplex_cell_complex()
    d0 = simplicial_coboundary_matrix(k_cell, 0)
    d1 = simplicial_coboundary_matrix(k_cell, 1)

    # Pure gauge configuration: delta = d^0 alpha (local site rotations)
    alpha = np.array([0.2, -0.4, 0.1, 0.3], dtype=np.float64)
    pure_gauge_delta = d0 @ alpha

    stickiness_gauge = compute_quotient_stickiness_lp(d0, pure_gauge_delta, d1)
    assert stickiness_gauge.is_pure_gauge is True
    assert stickiness_gauge.quotient_residual == pytest.approx(0.0, abs=1e-10)
    assert stickiness_gauge.curvature_residual == pytest.approx(0.0, abs=1e-10)
    assert stickiness_gauge.status == "AUTHORIZED"

    # Non-gauge configuration: closed loop with non-zero circulation on triangle (0, 1, 2)
    # Edges: (0, 1) -> +1.0, (1, 2) -> +1.0, (0, 2) -> -1.0 gives circulation = 3.0
    loop_couplings = {(0, 1): 1.0, (1, 2): 1.0, (0, 2): -1.0}
    loop_delta = map_edge_interactions_to_cochain(k_cell, loop_couplings)

    stickiness_loop = compute_quotient_stickiness_lp(d0, loop_delta, d1)
    assert stickiness_loop.is_pure_gauge is False
    assert stickiness_loop.quotient_residual > 0.0
    assert stickiness_loop.curvature_residual > 0.0
    assert stickiness_loop.status == "REFUSAL"


def test_defect_speed_to_holonomy_rate_bound():
    """Defect velocity nu bounds face circulation accumulation."""
    k_cell = build_3simplex_cell_complex()
    dims = [2, 2, 2, 2]
    rhos = [RHO0] * 4

    h_local = np.kron(X, X)
    edge_hams = {
        (0, 1): 0.5 * h_local,
        (1, 2): 0.8 * h_local,
        (0, 2): 0.3 * h_local,
    }

    report = evaluate_cochain_holonomy_bridge(k_cell, edge_hams, rhos, dims)

    assert report.defect_velocity_total > 0.0
    assert report.max_face_holonomy_rate > 0.0
    assert len(report.edge_cochain) == 6
    assert len(report.face_holonomies) == 4
    assert report.terminal_status in {"AUTHORIZED", "OBSTRUCTED", "REFUSAL"}

    # Individual bond defects bound the face circulation
    faces = k_cell.get_simplices(2)
    edges = k_cell.get_simplices(1)
    edge_idx = {e: i for i, e in enumerate(edges)}

    for f_idx, face in enumerate(faces):
        u, v, w = face
        face_edges = [(u, v), (v, w), (u, w)]
        sum_bond_speeds = sum(abs(report.edge_cochain[edge_idx[e]]) for e in face_edges)
        face_holonomy = abs(report.face_holonomies[f_idx])
        assert face_holonomy <= sum_bond_speeds + 1e-10


def test_discrete_continuum_membrane_firewall():
    """Cycle 006 torsion exclusion firewall rejects continuum identification without membrane."""
    # Without declared membrane contract: REFUSAL
    refused = evaluate_discrete_continuum_membrane(p=1, q=4, require_membrane_contract=True)
    assert refused.membrane_authorized is False
    assert refused.status == "REFUSAL"
    assert "CONTINUUM_MEMBRANE_REQUIRED" in (refused.refusal_reason or "")
    assert "2*pi*Z" in (refused.refusal_reason or "")

    # With declared Level-Q membrane contract: AUTHORIZED
    authorized = evaluate_discrete_continuum_membrane(
        p=1,
        q=4,
        require_membrane_contract=True,
        custom_membrane={"contract": "Level-Q-Membrane-v1", "carrier": "Q/Z"},
    )
    assert authorized.membrane_authorized is True
    assert authorized.status == "AUTHORIZED"
    assert authorized.continuous_phase_angle == pytest.approx(math.pi / 2.0)
    assert authorized.refusal_reason is None


def test_input_guards_fail_closed():
    """Bridge functions fail closed on malformed or non-Hermitian inputs."""
    dims = [2, 2, 2, 2]
    rhos = [RHO0] * 4

    # Non-Hermitian operator on 2 sites (shape 4x4)
    non_hermitian = np.kron(X, np.array([[1, 2], [3, 4]], dtype=complex))
    h_bad = embed_local_operator(non_hermitian, [0, 1], dims)

    with pytest.raises(ValueError, match="Hamiltonian must be Hermitian"):
        evaluate_hamiltonian_defect_velocity(h_bad, rhos, dims)

    # Missing edge in simplicial complex
    k_cell = build_3simplex_cell_complex()
    with pytest.raises(ValueError, match="not found in simplicial complex"):
        map_edge_interactions_to_cochain(k_cell, {(0, 99): 1.0})

    # Non-positive denominator
    with pytest.raises(ValueError, match="q must be an integer >= 1"):
        evaluate_discrete_continuum_membrane(p=1, q=0)
