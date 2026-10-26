# -*- coding: utf-8 -*-
"""
test_a_t9_retention.py: Theorem A-T9 as restated on 2026-09-23.

The earlier A-T9 related a projection C and a repair map d0 that were never tied
together. Its first clause fails on V = Q, C = I, d0 = d1 = 0, x = 1: there
Phi_1([x]) = 1 and Gamma_2 = 0, yet x - Cx = 0. The restatement adds the hypothesis
im C = im d0 (C projects onto the declared repair space). Under it:

1. Phi_1([x]) > 0  <=>  x not in im d0  <=>  residual(C, x) != 0;
2. residual(C, x - d0 f) = residual(C, x) and Phi_1([x - d0 f]) = Phi_1([x]) for every f.

These tests check the counterexample and both clauses on exact rational instances.

AuthorityEffect: None.
"""

from __future__ import annotations

import random

from cochain_presentation import LinearRepairProblem
from coda_a_core import is_projection, residual
from sympy import Matrix, eye, zeros


def phi1(d0: Matrix, x: Matrix):
    return LinearRepairProblem(d0).quotient_l1_distance(x).distance


def projection_onto_image(d0: Matrix, complement: Matrix) -> Matrix:
    """The projection with image im d0 and kernel span(complement): B diag(I, 0) B^-1."""
    basis = d0.row_join(complement)
    k = d0.cols
    diag = zeros(basis.cols, basis.cols)
    for i in range(k):
        diag[i, i] = 1
    return basis * diag * basis.inv()


def test_unrelated_projection_counterexample():
    """The review's counterexample: without im C = im d0, clause 1 fails."""
    C, d0, d1, x = eye(1), zeros(1, 1), zeros(1, 1), Matrix([1])
    assert is_projection(C)
    assert phi1(d0, x) == 1  # obstructed against the repair space {0}
    assert d1 * x == zeros(1, 1)  # Gamma_2 = 0
    assert residual(C, x) == zeros(1, 1)  # yet the projection leftover vanishes


def test_retention_on_the_running_example():
    """C projects onto im d0 = span(e1): the class of x survives exactly when x_2 != 0."""
    d0 = Matrix([[2], [0]])
    C = Matrix([[1, 0], [0, 0]])
    assert is_projection(C) and C * d0 == d0  # im d0 is inside the fixed set of C
    obstructed, repairable = Matrix([3, 4]), Matrix([3, 0])
    assert phi1(d0, obstructed) == 4 and residual(C, obstructed) == Matrix([0, 4])
    assert phi1(d0, repairable) == 0 and residual(C, repairable) == zeros(2, 1)
    for f in (-3, 0, 1, 7):
        repaired = obstructed - d0 * Matrix([f])
        assert residual(C, repaired) == residual(C, obstructed)
        assert phi1(d0, repaired) == phi1(d0, obstructed)


def test_retention_on_random_compatible_instances():
    """Clauses 1 and 2 on random exact instances with im C = im d0 (n = 3)."""
    rng = random.Random(20260923)
    checked = 0
    while checked < 40:
        k = rng.choice([1, 2])
        d0 = Matrix(3, k, [rng.randint(-2, 2) for _ in range(3 * k)])
        complement = Matrix(3, 3 - k, [rng.randint(-2, 2) for _ in range(3 * (3 - k))])
        if d0.row_join(complement).det() == 0:
            continue
        C = projection_onto_image(d0, complement)
        assert is_projection(C) and C * d0 == d0 and C.rank() == d0.rank()
        x = Matrix([rng.randint(-3, 3) for _ in range(3)])
        distance, leftover = phi1(d0, x), residual(C, x)
        assert (distance > 0) == (leftover != zeros(3, 1))
        f = Matrix([rng.randint(-3, 3) for _ in range(k)])
        assert residual(C, x - d0 * f) == leftover
        assert phi1(d0, x - d0 * f) == distance
        checked += 1
