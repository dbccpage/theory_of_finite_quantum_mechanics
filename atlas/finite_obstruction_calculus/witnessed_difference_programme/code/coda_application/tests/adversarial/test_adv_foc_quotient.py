# -*- coding: utf-8 -*-
"""
Adversarial tests for Layer 1 (CODA-FOC): the exact L1 quotient distance
Phi_1([x]) = min_f ||x - D0 f||_1 and its dual witness y* in ker(D0^T),
||y*||_inf <= 1, <y*, x> = Phi_1.

Claims under attack: README Layer 1 row ("Exact l1 quotient distance ...
mechanical LP dual witnesses"), layer1_foc.py docstring, FOC-T1 (definiteness:
Phi_1 = 0 iff x in im D0), FOC-T2 (strong duality) and FOC-C1 (exact separation).
Adapter comparisons share the canonical owner; fixed expected values supply independent mathematical controls.

AuthorityEffect: None.
"""

from __future__ import annotations

import random

from fractions import Fraction
from witnessed_difference.native_functionals import representative_mass, dual_bound

from sympy import Matrix, Symbol, sqrt
from sympy.matrices.exceptions import ShapeError

from coda_application.infrastructure.native_functional_adapter import NativeFunctionalEvaluator
from coda_application.domain.entities import TerminalKind
from coda_application.domain.layers.layer1_foc import Layer1FOC
from coda_application.infrastructure.exact_solver_adapter import ExactSolverAdapter
from coda_application.tests.adversarial._support import (
    GRAPH_D0,
    foc_phi1,
    make_problem,
)
from coda_application.application import evaluate_coda_pipeline, evaluate_triad_pipeline
from coda_application.application import solve_exact_l1_repair
from coda_application.domain.contracts import ProposalContract

SEED = 20260923

# Two directed 2-cycles through vertex 0: e0 0->1, e1 1->0, e2 0->2, e3 2->0.
TWO_CYCLES_D0 = Matrix([[-1, 1, 0], [1, -1, 0], [-1, 0, 1], [1, 0, -1]])
OPPOSITE_CIRCULATIONS = Matrix([1, 1, -1, -1])

# Two triangles sharing vertex 0, neither a directed cycle.
TWO_TRIANGLES_D0 = Matrix(
    [
        [-1, 1, 0, 0, 0],  # 0 -> 1
        [0, -1, 1, 0, 0],  # 1 -> 2
        [-1, 0, 1, 0, 0],  # 0 -> 2
        [-1, 0, 0, 1, 0],  # 0 -> 3
        [0, 0, 0, -1, 1],  # 3 -> 4
        [-1, 0, 0, 0, 1],  # 0 -> 4
    ]
)


def app_phi1(d0, c):
    return ExactSolverAdapter.compute_quotient_distance(d0, c)[0].sympy_rational


def witness_matrix(d0, c):
    w = ExactSolverAdapter.compute_quotient_distance(d0, c)[1]
    return None if w is None else w.to_matrix()


def pipeline(d0, c, **kw):
    kw.setdefault("d1", Matrix.zeros(1, c.rows))
    return evaluate_coda_pipeline(make_problem(d0=d0, defect_cochain=c, **kw))


# ---------------------------------------------------------------- false zeros


# FIXED 2026-09-23 (was BREAK FOC-01: zero repair column: nullspace()[0] pairs with a zero coordinate, Phi_1 reported 0 (true 5))
def test_zero_repair_column_does_not_hide_defect():
    d0, c = Matrix.zeros(2, 1), Matrix([0, 5])
    assert app_phi1(d0, c) == foc_phi1(d0, c) == 5


# FIXED 2026-09-23 (was BREAK FOC-02: false-zero Phi_1 on an obstructed cochain is promoted to AUTHORIZED under license)
def test_false_zero_is_not_authorized():
    out = pipeline(Matrix.zeros(2, 1), Matrix([0, 5]), fda_license_granted=True)
    assert out.terminal_kind != TerminalKind.AUTHORIZED


# FIXED 2026-09-23 (was BREAK FOC-03: graph path sums disjoint directed cycles with sign +1: opposite circulations cancel to 0 (true 4))
def test_opposite_circulations_do_not_cancel():
    assert app_phi1(TWO_CYCLES_D0, OPPOSITE_CIRCULATIONS) == foc_phi1(TWO_CYCLES_D0, OPPOSITE_CIRCULATIONS) == 4


# FIXED 2026-09-23 (was BREAK FOC-04: Layer 1 diagnoses 'Cochain is in im(d0)' for a cochain the FOC oracle proves obstructed)
def test_layer1_never_claims_image_membership_falsely():
    rec, *_ = Layer1FOC.evaluate(make_problem(d0=TWO_CYCLES_D0, defect_cochain=OPPOSITE_CIRCULATIONS), evaluator=NativeFunctionalEvaluator())
    assert foc_phi1(TWO_CYCLES_D0, OPPOSITE_CIRCULATIONS) > 0
    assert "im(d0)" not in rec.diagnostic_message


# FIXED 2026-09-23 (was BREAK FOC-05: cancelled circulations reach AUTHORIZED: a 4-unit obstruction gets a token)
def test_cancelled_circulations_not_authorized():
    out = pipeline(TWO_CYCLES_D0, OPPOSITE_CIRCULATIONS, fda_license_granted=True)
    assert out.terminal_kind != TerminalKind.AUTHORIZED


# FIXED 2026-09-23 (was BREAK FOC-06: dim ker(D0^T) = 2: only the first basis vector is used, Phi_1 underestimated 1 vs 2)
def test_multidimensional_left_kernel_not_underestimated():
    d0, c = Matrix([[1], [0], [0]]), Matrix([0, 1, 1])
    assert app_phi1(d0, c) == foc_phi1(d0, c) == 2


# FIXED 2026-09-23 (was BREAK FOC-07: dim ker(D0^T) = 2 and the first basis vector annihilates c: Phi_1 = 0 on an obstructed cochain)
def test_multidimensional_left_kernel_false_zero():
    d0, c = Matrix([[1], [0], [0]]), Matrix([0, 0, 1])
    assert app_phi1(d0, c) == foc_phi1(d0, c) == 1


# FIXED 2026-09-23 (was BREAK FOC-08: all-ones repair column: nullspace()[0] = [-1,1,0] misses the leftover, Phi_1 = 0 (true 1))
def test_all_ones_column_false_zero():
    d0, c = Matrix([[1], [1], [1]]), Matrix([1, 1, 0])
    assert app_phi1(d0, c) == foc_phi1(d0, c) == 1


# FIXED 2026-09-23 (was BREAK FOC-09: graph with no directed cycle falls to nullspace()[0]; one of two independent circulations is lost)
def test_two_undirected_triangles_both_counted():
    c = Matrix([1, 0, 0, 1, 0, 0])
    assert app_phi1(TWO_TRIANGLES_D0, c) == foc_phi1(TWO_TRIANGLES_D0, c) == 2


# -------------------------------------------------------------- dual witness


# FIXED 2026-09-23 (was BREAK FOC-10: Phi_1 = |<w, c>| but w is never sign-flipped: <y*, omega> = -1 while Phi_1 = 1)
def test_witness_pairing_equals_phi1_with_sign():
    d0, c = Matrix([[1], [1]]), Matrix([1, 0])
    w = witness_matrix(d0, c)
    assert dual_bound(tuple(tuple(Fraction(x) for x in row) for row in d0.tolist()), d0.cols, tuple(Fraction(x) for x in c), (Fraction(1),)*len(c), tuple(Fraction(x) for x in w)) == app_phi1(d0, c)


# FIXED 2026-09-23 (was BREAK FOC-11: the sign-flipped witness trips CODA's own GUARD_3: a genuine residual is REFUSED, not retained)
def test_genuine_residual_is_retained_not_refused():
    problem = make_problem(d0=Matrix([[1], [1]]), defect_cochain=Matrix([1, 0]))
    _, auth = evaluate_triad_pipeline(ProposalContract(proposer_id="p", problem=problem))
    assert auth.terminal_kind == TerminalKind.CLOSED_RESIDUAL


def test_general_path_witness_annihilates_repairs():
    """HELD: the general-path witness lies in ker(D0^T)."""
    d0, c = Matrix([[1], [1]]), Matrix([1, 0])
    w = witness_matrix(d0, c)
    assert d0.T * w == Matrix.zeros(d0.cols, 1)


def test_graph_path_witness_annihilates_repairs():
    """HELD: the cycle witness lies in ker(D0^T)."""
    w = witness_matrix(TWO_CYCLES_D0, Matrix([1, 1, 1, 1]))
    assert TWO_CYCLES_D0.T * w == Matrix.zeros(3, 1)


def test_general_path_dual_passes_native_feasibility_check():
    """The native checker validates the raw dual and its known pairing."""
    d0, c = Matrix([[2], [1], [0]]), Matrix([0, 0, 3])
    _, witness, _ = ExactSolverAdapter.compute_quotient_distance(d0, c)
    assert witness is not None
    assert dual_bound([[2], [1], [0]], 1, [0, 0, 3], [1, 1, 1], witness.fractions) == 3


def test_antiparallel_pair_matches_oracle():
    """HELD: a single directed 2-cycle is solved exactly."""
    assert app_phi1(GRAPH_D0, Matrix([1, 1])) == foc_phi1(GRAPH_D0, Matrix([1, 1])) == 2


def test_mixed_orientation_single_triangle_matches_oracle():
    """The canonical quotient certificate agrees with the finite triangle control."""
    d0 = Matrix([[-1, 1, 0], [0, -1, 1], [-1, 0, 1]])
    c = Matrix([1, 1, -1])
    assert app_phi1(d0, c) == foc_phi1(d0, c) == 3


def test_zero_row_edge_matches_oracle():
    """HELD: a zero row is an unrepairable coordinate and is charged in full."""
    d0, c = Matrix([[-1, 1], [0, 0]]), Matrix([0, 3])
    assert app_phi1(d0, c) == foc_phi1(d0, c) == 3


def test_scaled_incidence_matches_oracle():
    """HELD: a non-unit incidence matrix takes the general path and is right here."""
    d0 = Matrix([[-2, 2], [2, -2]])
    assert app_phi1(d0, Matrix([1, 0])) == foc_phi1(d0, Matrix([1, 0])) == 1


def test_empty_boundary_is_full_l1_norm():
    """HELD: with no repair columns Layer 1 charges ||omega||_1."""
    c = Matrix([3, -4])
    _, phi1, _, _ = Layer1FOC.evaluate(make_problem(d0=Matrix.zeros(2, 0), defect_cochain=c), evaluator=NativeFunctionalEvaluator())
    assert phi1.sympy_rational == foc_phi1(Matrix.zeros(2, 0), c) == 7


def test_phi1_is_homogeneous():
    """HELD: Phi_1(3x) = 3 Phi_1(x) on the path the app takes."""
    d0, c = Matrix([[1], [1]]), Matrix([1, 0])
    assert app_phi1(d0, 3 * c) == 3 * app_phi1(d0, c)


# FIXED 2026-09-23 (was BREAK FOC-12: Phi_1 changes when edges are re-oriented (row and entry negated); an L1 distance cannot)
def test_phi1_invariant_under_edge_reorientation():
    flip = Matrix.diag(1, -1, 1, -1)
    d0_flipped, c_flipped = flip * TWO_CYCLES_D0, flip * OPPOSITE_CIRCULATIONS
    assert foc_phi1(d0_flipped, c_flipped) == foc_phi1(TWO_CYCLES_D0, OPPOSITE_CIRCULATIONS)
    assert app_phi1(d0_flipped, c_flipped) == app_phi1(TWO_CYCLES_D0, OPPOSITE_CIRCULATIONS)


# ------------------------------------------------------------ shape smuggling


# FIXED 2026-09-23 (was BREAK FOC-13: a cochain longer than d0 has its extra coordinates silently dropped: Phi_1 = 0 for [0,0,100])
def test_extra_cochain_coordinates_are_not_dropped():
    d0, c = GRAPH_D0, Matrix([0, 0, 100])
    out = pipeline(d0, c)
    assert out.terminal_kind == TerminalKind.REFUSED or out.residual_pair.phi1.sympy_rational > 0


# FIXED 2026-09-23 (was BREAK FOC-14: the dropped coordinates reach AUTHORIZED under license)
def test_extra_cochain_coordinates_not_authorized():
    d0, c = GRAPH_D0, Matrix([0, 0, 100])
    try:
        out = pipeline(d0, c, fda_license_granted=True)
    except (ValueError, TypeError, ShapeError):
        return
    assert out.terminal_kind != TerminalKind.AUTHORIZED


# FIXED 2026-09-23 (was BREAK FOC-15: a short cochain crashes the graph solver with IndexError instead of a shape refusal)
def test_short_cochain_is_refused_not_crashed():
    out = pipeline(GRAPH_D0, Matrix([1]))
    assert out.terminal_kind == TerminalKind.REFUSED


# FIXED 2026-09-23 (was BREAK FOC-16: a two-column cochain: column 1 is ignored everywhere, a defect of 7+7 vanishes)
def test_second_cochain_column_not_ignored():
    c = Matrix([[0, 7], [0, 7]])
    out = pipeline(GRAPH_D0, c)
    assert out.terminal_kind == TerminalKind.REFUSED or out.residual_pair.phi1.sympy_rational > 0


# FIXED 2026-09-23 (was BREAK FOC-17: d1 * d0 != 0 is accepted: an exact coboundary is reported with Gamma_2 = 1 and refused)
def test_non_complex_differentials_rejected():
    d1 = Matrix([[1, 0]])  # d1 * GRAPH_D0 = [-1, 1] != 0
    coboundary = GRAPH_D0 * Matrix([0, 1])
    out = pipeline(GRAPH_D0, coboundary, d1=d1)
    assert (out.terminal_kind == TerminalKind.REFUSED and "d1 d0" in out.reason) or (
        out.residual_pair.gamma2.sympy_rational == 0
    )


# FIXED 2026-09-23 (was BREAK FOC-18: d1 of the wrong width raises sympy ShapeError out of the pipeline)
def test_wrong_width_d1_is_refused_not_crashed():
    out = pipeline(GRAPH_D0, Matrix([1, 0]), d1=Matrix.zeros(1, 3))
    assert out.terminal_kind == TerminalKind.REFUSED


# FIXED 2026-09-23 (was BREAK FOC-19: a symbolic cochain entry escapes as TypeError; no terminal is produced)
def test_symbolic_cochain_entry_is_refused_not_crashed():
    out = pipeline(GRAPH_D0, Matrix([Symbol("x"), 0]))
    assert out.terminal_kind == TerminalKind.REFUSED


# FIXED 2026-09-23 (was BREAK FOC-20: an irrational cochain entry escapes as TypeError; no terminal is produced)
def test_irrational_cochain_entry_is_refused_not_crashed():
    out = pipeline(Matrix([[1], [1]]), Matrix([sqrt(2), 0]))
    assert out.terminal_kind == TerminalKind.REFUSED


# --------------------------------------------------- solve_exact_l1_repair


# FIXED 2026-09-23 (was BREAK FOC-21: public solve_exact_l1_repair: with no repair columns it pairs with e_1 only, Phi_1 = 0 (true 4))
def test_l1_repair_use_case_empty_repair_columns():
    d, c = Matrix.zeros(3, 0), Matrix([0, 0, 4])
    assert solve_exact_l1_repair(d, c)[0].sympy_rational == foc_phi1(d, c) == 4


# FIXED 2026-09-23 (was BREAK FOC-22: the returned 'residual' is the raw cochain, whose L1 norm (2) is not the reported distance (0))
def test_l1_repair_residual_norm_equals_distance():
    d, c = Matrix([[1], [1], [1]]), Matrix([1, 1, 0])
    dist, _w, residual = solve_exact_l1_repair(d, c)
    assert representative_mass(tuple(Fraction(x) for x in residual)) == dist.fraction


# FIXED 2026-09-23 (was BREAK FOC-23: use case and adapter disagree on one input: two solvers for one Phi_1)
def test_l1_repair_use_case_agrees_with_adapter():
    assert solve_exact_l1_repair(TWO_CYCLES_D0, OPPOSITE_CIRCULATIONS)[0] == ExactSolverAdapter.compute_quotient_distance(
        TWO_CYCLES_D0, OPPOSITE_CIRCULATIONS
    )[0]


def test_l1_repair_use_case_image_member_is_zero():
    """HELD: an exact coboundary gets distance 0 and a residual of 0."""
    c = GRAPH_D0 * Matrix([2, 5])
    dist, w, residual = solve_exact_l1_repair(GRAPH_D0, c)
    assert dist.sympy_rational == 0 and w is None and residual == Matrix.zeros(2, 1)


# ---------------------------------------------------- seeded differential


def _random_general(rng):
    rows, cols = rng.randint(2, 4), rng.randint(1, 2)
    d0 = Matrix(rows, cols, [rng.randint(-2, 2) for _ in range(rows * cols)])
    c = Matrix([rng.randint(-3, 3) for _ in range(rows)])
    return d0, c


def _random_digraph(rng):
    n_v, n_e = rng.randint(3, 4), rng.randint(3, 5)
    d0 = Matrix.zeros(n_e, n_v)
    for e in range(n_e):
        u, v = rng.sample(range(n_v), 2)
        d0[e, u], d0[e, v] = -1, 1
    c = Matrix([rng.randint(-2, 2) for _ in range(n_e)])
    return d0, c


def _disagreements(generator, n, seed):
    rng = random.Random(seed)
    bad = []
    for _ in range(n):
        d0, c = generator(rng)
        truth, got = foc_phi1(d0, c), app_phi1(d0, c)
        if truth != got:
            bad.append((d0.tolist(), list(c), truth, got))
    return bad


# FIXED 2026-09-23 (was BREAK FOC-24: seeded differential vs FOC oracle on random general complexes: Phi_1 disagrees)
def test_random_general_complexes_match_oracle():
    bad = _disagreements(_random_general, 60, SEED)
    assert not bad, f"{len(bad)}/60 disagree; first: {bad[0]}"


# FIXED 2026-09-23 (was BREAK FOC-25: seeded differential vs FOC oracle on random digraphs: Phi_1 disagrees)
def test_random_digraphs_match_oracle():
    bad = _disagreements(_random_digraph, 40, SEED + 1)
    assert not bad, f"{len(bad)}/40 disagree; first: {bad[0]}"


# FIXED 2026-09-23 (was BREAK FOC-26: seeded differential: obstructed cochains (oracle > 0) reported as Phi_1 = 0)
def test_random_no_false_zeros():
    rng = random.Random(SEED + 2)
    false_zero = []
    for _ in range(60):
        d0, c = (_random_digraph if rng.random() < 0.5 else _random_general)(rng)
        if foc_phi1(d0, c) > 0 and app_phi1(d0, c) == 0:
            false_zero.append((d0.tolist(), list(c)))
    assert not false_zero, f"{len(false_zero)} false zeros; first: {false_zero[0]}"


def test_random_never_overestimates():
    """HELD: every app value is a feasible dual pairing, so it never exceeds the true Phi_1."""
    rng = random.Random(SEED + 3)
    for _ in range(60):
        d0, c = (_random_digraph if rng.random() < 0.5 else _random_general)(rng)
        assert app_phi1(d0, c) <= foc_phi1(d0, c)
