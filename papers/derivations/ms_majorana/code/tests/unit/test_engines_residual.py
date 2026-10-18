r"""
Tests for the residual-geometry engines: phi1_lp, trace_norm_quotient, snf_betti,
l1_l2_boundary.

AuthorityEffect: None.

Every test names the mutation it kills. A test that cannot fail against a plausible wrong
implementation is not defending anything.
"""

import numpy as np
import pytest

from omega_engine.crates.homology_theory.finite_graph import FiniteGraph, path_graph, triangle
from omega_engine.crates.quantum_physics.primitives import SIGMA_X, SIGMA_Z
from omega_engine.crates.functional import l1_l2_boundary as l1l2
from omega_engine.crates.homology_theory import snf_betti as sb
from omega_engine.crates.functional import trace_norm_quotient as tnq
from omega_engine.crates.functional.phi import (
    Phi1Uncertified,
    constant_gauge_sweep_is_a_noop,
    phi1,
    phi1_estimate,
    solve_phi1_dual_witness,
)


def unfilled_cycle(n: int) -> FiniteGraph:
    return FiniteGraph(vertices=list(range(n)), edges=[(i, (i + 1) % n) for i in range(n)])




def test_phi1_vanishes_on_a_tree():
    """A tree has no cycles, so every cochain is exact and Phi_1 = 0.

    Kills an implementation that returns ||omega||_1 without minimizing: the raw norm here
    is 6.0.
    """
    g = path_graph(4)
    omega = np.array([1.0, 2.0, 3.0])
    assert float(np.sum(np.abs(omega))) == pytest.approx(6.0)
    assert phi1(g.vertices, g.edges, omega) == pytest.approx(0.0, abs=1e-9)


def test_phi1_equals_cycle_mass_on_a_harmonic_cochain():
    """The all-ones cochain on a 3-cycle is pure circulation: no gauge can reduce it.

    Kills an implementation that over-minimizes (e.g. one that subtracts the mean).
    """
    g = unfilled_cycle(3)
    assert phi1(g.vertices, g.edges, np.array([1.0, 1.0, 1.0])) == pytest.approx(3.0, abs=1e-7)


def test_phi1_is_invariant_under_adding_a_coboundary():
    """Phi_1 is a function of the CLASS. Adding d0(alpha) must not move it.

    Kills an implementation that measures the representative instead of the class.
    """
    g = unfilled_cycle(4)
    omega = np.array([1.0, -2.0, 0.5, 3.0])
    shifted = omega + g.d0_matrix() @ np.array([0.0, 1.3, -2.2, 4.1])
    assert phi1(g.vertices, g.edges, omega) == pytest.approx(
        phi1(g.vertices, g.edges, shifted), abs=1e-6
    )


def test_phi1_dual_certificate_closes_the_gap():
    """A primal value without a dual witness is an estimate, not a certificate."""
    g = unfilled_cycle(4)
    res = solve_phi1_dual_witness(g.vertices, g.edges, np.array([1.0, -2.0, 0.5, 3.0]))
    assert res["is_certified"] is True
    assert res["duality_gap"] < 1e-6
    assert res["min_l1"] == pytest.approx(res["dual_val"], abs=1e-6)


def test_dual_witness_is_actually_feasible():
    """|phi_e| <= w_e and d0^T phi = 0. Kills a 'dual' that is just the primal residual."""
    g = unfilled_cycle(5)
    omega = np.array([2.0, -1.0, 4.0, 0.0, -3.0])
    res = solve_phi1_dual_witness(g.vertices, g.edges, omega)
    phi = res["dual_phi"]
    assert np.all(np.abs(phi) <= 1.0 + 1e-7)
    assert np.max(np.abs(g.d0_matrix().T @ phi)) < 1e-7


def test_constant_gauge_sweep_provably_finds_nothing():
    """The sibling engine's Phi_1 'minimization' is a no-op, and this shows why.

    d0 of a constant potential is identically zero on every edge, so the swept objective
    never differs from ||omega||_1. Here the sweep reports 11.0 while the true Phi_1 is 3.0.
    Kills any claim that the constant sweep approximates Phi_1.
    """
    g = unfilled_cycle(3)
    omega = g.d0_matrix() @ np.array([0.0, 2.0, 5.0]) + np.array([1.0, 1.0, 1.0])
    rep = constant_gauge_sweep_is_a_noop(g.vertices, g.edges, omega)

    assert rep["max_coboundary_seen_over_sweep"] == pytest.approx(0.0, abs=1e-15)
    assert rep["sweep_found_nothing"] is True
    assert rep["swept_best"] == pytest.approx(rep["raw_l1_norm"])
    assert rep["exact_phi1"] == pytest.approx(3.0, abs=1e-7)
    assert rep["residual_missed_by_sweep"] > 7.0




def test_trace_norm_quotient_is_zero_on_an_exact_coboundary():
    """If delta IS d0(alpha), the residual is exactly repairable.

    Kills an implementation that returns the raw sum of trace norms (6.83 here).
    """
    g = triangle()
    alphas = [SIGMA_X.astype(complex), SIGMA_Z.astype(complex), np.zeros((2, 2), complex)]
    d0 = g.d0_matrix()
    exact = [sum(d0[e, v] * alphas[v] for v in range(3)) for e in range(3)]

    res = tnq.trace_norm_quotient(g, exact)
    assert res["raw_trace_norm_sum"] > 6.0
    assert res["phi_tr"] == pytest.approx(0.0, abs=1e-6)
    assert res["is_exact_repair"] is True


def test_trace_norm_quotient_certifies_with_a_feasible_dual():
    """Primal and dual must meet, with the dual genuinely inside its ball."""
    g = triangle()
    deltas = [SIGMA_X.astype(complex), SIGMA_Z.astype(complex), (SIGMA_X + SIGMA_Z).astype(complex)]
    res = tnq.trace_norm_quotient(g, deltas)
    assert res["dual_feasible"] is True
    assert res["certified"] is True
    assert res["duality_gap"] == pytest.approx(0.0, abs=1e-4)
    assert res["phi_tr"] < res["raw_trace_norm_sum"]


def test_the_two_dual_ball_conventions_differ_by_exactly_two():
    """qm_080 states lambda_max - lambda_min <= 1 (trace DISTANCE); the plain trace norm
    wants ||M||_op <= 1. Mixing them makes a correct dual look like a factor-2 failure.

    Kills a 'fix' that silently rescales one convention into the other.
    """
    m = SIGMA_X.astype(complex)
    assert tnq.dual_ball_slack(m) == pytest.approx(0.0)
    assert tnq.trace_distance_dual_ball_slack(m) == pytest.approx(-1.0)
    ident = tnq.dual_ball_diameter_identity(m)
    assert ident["identity_holds"] is True
    assert ident["diameter"] == pytest.approx(2.0 * ident["op_norm_at_optimal_shift"])




def test_betti_of_a_filled_triangle_is_contractible():
    """A 2-cell fills the loop: b0=1, b1=0, b2=0. Kills a b1 that ignores d1."""
    r = sb.betti_numbers(triangle())
    assert (r["b0"], r["b1"], r["b2"]) == (1, 0, 0)
    assert r["euler_identity_holds"] is True


def test_betti_of_an_unfilled_cycle_has_b1_one():
    """Remove the face and the cycle survives as homology. Kills a b1 pinned to zero."""
    r = sb.betti_numbers(unfilled_cycle(5))
    assert (r["b0"], r["b1"], r["b2"]) == (1, 1, 0)
    assert r["euler_identity_holds"] is True


def test_betti_counts_components():
    """Two disjoint cycles: b0 = 2, b1 = 2. Kills a b0 hardcoded to 1."""
    g = FiniteGraph(
        vertices=list(range(6)),
        edges=[(0, 1), (1, 2), (2, 0), (3, 4), (4, 5), (5, 3)],
    )
    r = sb.betti_numbers(g)
    assert r["b0"] == 2
    assert r["b1"] == 2


def test_snf_recovers_invariant_factors_exactly():
    """SNF of diag-equivalent integer data must give integer invariant factors.

    Kills the broken omega_homology implementation, which returns rounded SINGULAR VALUES
    with U = V = I. For this matrix the singular values are irrational; the invariant
    factors are 1 and 2.
    """
    mat = np.array([[2, 4], [6, 8]], dtype=float)
    factors = sb.smith_normal_form_diagonal(mat)

    assert factors == [2, 4]
    assert abs(np.prod(factors)) == pytest.approx(abs(np.linalg.det(mat)))
    assert factors[1] % factors[0] == 0

    sv = np.sort(np.linalg.svd(mat, compute_uv=False))
    assert not np.allclose(np.sort(np.abs(factors)), sv, atol=1e-6)
    assert not np.allclose(np.sort(np.abs(factors)), np.rint(sv), atol=1e-6)


def test_torsion_is_reported_not_silently_dropped():
    """diag(2,3) has invariant factors (1, 6): the homology carries a Z/6, not Z/2 + Z/3
    read off the diagonal. Kills an implementation that returns the diagonal unchanged."""
    mat = np.array([[2, 0], [0, 3]], dtype=float)
    factors = sb.smith_normal_form_diagonal(mat)
    assert factors == [1, 6]
    assert factors != [2, 3]
    assert abs(np.prod(factors)) == pytest.approx(abs(np.linalg.det(mat)))




def test_prop_e2_bounds_hold_and_both_are_attained():
    """||x||_2 <= ||x||_1 <= sqrt(d)||x||_2, tight on the axes and on equal moduli."""
    axis = l1l2.forgetful_loss_ledger([5.0, 0.0, 0.0])
    assert axis["delta_forgetful"] == pytest.approx(0.0, abs=1e-12)
    assert axis["sharpness_case"] == "axis"

    equal = l1l2.forgetful_loss_ledger([1.0, 1.0, 1.0, 1.0])
    assert equal["norm_l1"] == pytest.approx(np.sqrt(4) * equal["norm_l2"])
    assert equal["sharpness_case"] == "equal_modulus"


def test_prop_e3_quotient_comparison_holds():
    """Phi_2 <= Phi_1 <= sqrt(m) Phi_2 on a real carrier. Kills a swapped inequality."""
    g = unfilled_cycle(3)
    r = l1l2.quotient_comparison(g, np.array([1.0, 1.0, 1.0]))
    assert r["lower_bound_holds"] is True
    assert r["upper_bound_holds"] is True
    assert r["phi2"] <= r["phi1"] + 1e-9


@pytest.mark.parametrize("n", [3, 4, 5, 6, 8, 12])
def test_hodge_inflation_matches_foc004_analytic_value(n):
    """FOC_004 §1.1 item 4 predicts 3 - 2/n on the n-cycle. Measured must match.

    This is an independent numerical check of a published claim, and it is the quantity
    Remark E.3a warns must NOT be confused with the sqrt(d) comparison of optimal values.
    """
    g = unfilled_cycle(n)
    omega = np.zeros(n)
    omega[0] = 1.0
    r = l1l2.hodge_inflation(g, omega)
    assert r["l2_orthogonality_verified"] is True
    assert r["split_costs_more_than_the_whole"] is True
    assert r["inflation_ratio"] == pytest.approx(l1l2.cycle_inflation_prediction(n), abs=1e-9)


def test_delta_is_representative_dependent_but_phi_is_not():
    """The whole dispute in one test: delta moves within a class, Phi_1 and Phi_2 do not.

    So delta cannot by itself be 'the topological debt of the class'. Kills any claim that
    delta is a gauge invariant.
    """
    g = unfilled_cycle(4)
    r = l1l2.delta_is_gauge_dependent(g, np.array([1.0, -2.0, 0.5, 3.0]))
    assert r["delta_moved"] is True
    assert r["phi1_invariant"] is True
    assert r["phi2_invariant"] is True


def test_snf_refuses_non_integral_input_instead_of_rounding():
    """'Exact integer SNF' must not silently answer for a different matrix.

    Pre-fix, [[2.4, 4.6], [6.5, 8.5]] was rounded to [[2, 5], [6, 8]] and returned
    invariant factors [1, 14] for a matrix nobody supplied.
    """
    with pytest.raises(ValueError, match="integral"):
        sb.smith_normal_form_diagonal(np.array([[2.4, 4.6], [6.5, 8.5]]))
    with pytest.raises(ValueError, match="integral"):
        sb.betti_numbers.__globals__["_integer_matrix_rank"](np.array([[0.5]]))

    assert sb.smith_normal_form_diagonal(np.array([[2.0, 4.0], [6.0, 8.0]])) == [2, 4]


def test_phi1_does_not_certify_off_a_failed_solve():
    """is_certified must require BOTH solves to succeed.

    Pre-fix, a failed primal fell back to the raw l1 norm, which on a harmonic cochain
    equals the dual optimum -- so the gap was 0 and is_certified came back True off a solve
    that never ran.
    """
    import scipy.optimize as opt

    g = unfilled_cycle(3)
    real = opt.linprog
    calls = {"n": 0}

    def fail_primal_only(*a, **k):
        calls["n"] += 1
        if calls["n"] == 1:
            class Failed:
                success = False
                x = None
                fun = None
            return Failed()
        return real(*a, **k)

    opt.linprog = fail_primal_only
    try:
        res = solve_phi1_dual_witness(g.vertices, g.edges, np.array([1.0, 1.0, 1.0]))
    finally:
        opt.linprog = real

    assert res["primal_solved"] is False
    assert res["used_fallback"] is True
    assert res["duality_gap"] == pytest.approx(0.0, abs=1e-9)
    assert res["is_certified"] is False


def test_phi1_surfaces_a_weak_duality_violation_instead_of_clamping():
    """dual > primal is impossible; if it happens a solve is wrong and must be visible.

    The gap is no longer clamped to 0, so the signal survives.
    """
    g = unfilled_cycle(4)
    res = solve_phi1_dual_witness(g.vertices, g.edges, np.array([1.0, -2.0, 0.5, 3.0]))
    assert res["weak_duality_violated"] is False
    assert res["duality_gap"] >= -1e-7
    assert set(["primal_solved", "dual_solved", "used_fallback"]).issubset(res)


def test_normalize_refuses_zero_total_mass():
    """W = 0 has no state to normalize to. Kills a silent uniform-distribution fallback."""
    from omega_engine.crates.quantum_physics.diagonal_density import normalize

    with pytest.raises(ValueError, match="W = 0"):
        normalize([0.0, 0.0, 0.0])



