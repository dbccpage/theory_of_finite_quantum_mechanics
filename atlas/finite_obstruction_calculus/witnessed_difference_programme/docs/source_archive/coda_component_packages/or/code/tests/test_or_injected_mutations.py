# -*- coding: utf-8 -*-
"""
test_or_injected_mutations.py: Injected-fault regression mutants for CODA-OR decision procedures.

Three differential regression checks:
1. mutant_skip_empty_sieve: simulates treating envelope membership as standing with empty support.
2. mutant_closed_means_exact: simulates treating any closed defect (d1*delta = 0) as exact.
3. mutant_l2_residual: computes the squared least-squares residual (Euclidean L2 squared norm)
   instead of the exact L1 quotient distance, confirming that Section 6A distinguishes the two metrics.
"""

from __future__ import annotations

from coda_or_core import (
    R_EMPTY_SUPPORT,
    ComparisonObject,
    EnrichedEnvironment,
    SquareStatus,
    SupportSieve,
    classify_diagram_square,
    evaluate_comparison_authority,
)
from sympy import Matrix, Rational


def _h1_tear_env() -> EnrichedEnvironment:
    # d0 is the zero column, so im d0 is {0}; ker d1 is spanned by (1,-1).
    return EnrichedEnvironment(
        dim_c0=1,
        dim_c1=2,
        dim_c2=1,
        d0=Matrix([[0], [0]]),
        d1=Matrix([[1, 1]]),
    )


def mutant_skip_empty_sieve(obj: ComparisonObject) -> bool:
    """Treat envelope membership as standing even with an empty support sieve."""
    return bool(obj.descent_d and obj.verifier_v and obj.terminalizer_tau)


def mutant_closed_means_exact(raw_defect, env: EnrichedEnvironment) -> SquareStatus:
    """If d1*delta=0, call the square exact even when leftover is positive."""
    vec = Matrix(raw_defect)
    if vec.cols != 1:
        vec = vec.T
    if vec.is_zero_matrix:
        return SquareStatus.STRICT_COMMUTE
    d1_delta = env.d1 * vec
    if d1_delta.is_zero_matrix:
        return SquareStatus.WEAK_COMMUTE_CERTIFIED
    return SquareStatus.OPEN_DIAGRAM_OBSTRUCTION


def mutant_l2_squared_residual(repair_map, cochain) -> Rational:
    """Compute the squared least-squares residual (squared Euclidean norm) instead of L1 quotient distance."""
    matrix = Matrix(repair_map)
    x = Matrix(cochain)
    gram = matrix.T * matrix
    coeff = gram.inv() * (matrix.T * x)
    residual = x - matrix * coeff
    return sum((entry ** 2 for entry in residual), start=Rational(0))


def test_mutant_skip_empty_sieve_killed() -> None:
    obj = ComparisonObject(
        object_id="limit_demo",
        weight_class="W",
        support_sieve=SupportSieve(target_object_id="limit_demo", arrows=()),
        descent_d="d",
        verifier_v="v",
        terminalizer_tau="tau",
    )
    real = evaluate_comparison_authority(obj)
    mutant_inhabits = mutant_skip_empty_sieve(obj)
    assert real.inhabited is False
    assert real.refusal_code == R_EMPTY_SUPPORT
    assert mutant_inhabits is True
    assert mutant_inhabits is not real.inhabited


def test_mutant_closed_means_exact_killed_on_h1_tear() -> None:
    env = _h1_tear_env()
    defect = Matrix([[1], [-1]])
    real = classify_diagram_square(defect, env)
    mutant_status = mutant_closed_means_exact(defect, env)
    assert real.status == SquareStatus.H1_DIAGRAM_TEAR
    assert real.quotient_distance == Rational(2)
    assert mutant_status == SquareStatus.WEAK_COMMUTE_CERTIFIED
    assert mutant_status != real.status


def test_mutant_l2_residual_killed_on_column_instance() -> None:
    repair_map = Matrix([[1], [1], [1]])
    cochain = Matrix([[0], [0], [10]])
    env = EnrichedEnvironment(
        dim_c0=1,
        dim_c1=3,
        dim_c2=1,
        d0=repair_map,
        d1=Matrix([[0, 0, 0]]),
    )
    real = classify_diagram_square(cochain, env)
    mutant_value = mutant_l2_squared_residual(repair_map, cochain)
    assert real.quotient_distance == Rational(10)
    assert mutant_value == Rational(200, 3)
    assert real.quotient_distance != mutant_value
