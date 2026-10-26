"""Adversarial fuzzing for LP boundary handling, zero division guards, and degenerate cycles.

# Executable finite evidence; AuthorityEffect: None.
"""

from fractions import Fraction
import pytest
from hypothesis import given, settings, strategies as st

from witnessed_difference.cochains import FiniteComplex
from witnessed_difference.exact import as_fraction
from witnessed_difference.obstruction import (
    DEFAULT_PIVOT_BUDGET,
    exact_quotient_l1,
    matrix_quotient_l1,
    solve_standard_lp,
    verify_standard_lp,
)
from witnessed_difference.outcomes import Accepted, RefusalCode, Refused
from native_wdp import NativeWdpRefusal, solve_native_obstruction


def test_adversarial_zero_and_negative_edge_weights():
    """Verify that zero and negative edge weights are cleanly refused without zero division."""
    complex_obj = FiniteComplex(("v0", "v1", "v2"), (("v0", "v1"), ("v1", "v2"), ("v0", "v2")))
    cochain = {("v0", "v1"): Fraction(1), ("v1", "v2"): Fraction(1), ("v0", "v2"): Fraction(0)}

    # Zero weight on one edge
    zero_weights = {("v0", "v1"): 0, ("v1", "v2"): 1, ("v0", "v2"): 1}
    outcome = exact_quotient_l1(complex_obj, cochain, zero_weights)
    assert isinstance(outcome, Refused)
    assert outcome.code == RefusalCode.INVALID_INPUT
    assert "must be positive" in outcome.detail

    # Negative weight on an edge
    neg_weights = {("v0", "v1"): Fraction(-1, 2), ("v1", "v2"): 1, ("v0", "v2"): 1}
    outcome_neg = exact_quotient_l1(complex_obj, cochain, neg_weights)
    assert isinstance(outcome_neg, Refused)
    assert outcome_neg.code == RefusalCode.INVALID_INPUT
    assert "must be positive" in outcome_neg.detail

    # Non-invertible / zero division weight as fraction string
    with pytest.raises(ZeroDivisionError):
        as_fraction("1/0")


def test_adversarial_matrix_quotient_direct_zero_weights():
    """Directly test matrix_quotient_l1 refusing non-positive or zero weights."""
    matrix = [[1, -1, 0], [0, 1, -1], [1, 0, -1]]
    delta = [Fraction(1), Fraction(1), Fraction(0)]

    # Zero weight vector
    zero_w = [Fraction(0), Fraction(1), Fraction(1)]
    outcome = matrix_quotient_l1(matrix, delta, zero_w)
    assert isinstance(outcome, Refused)
    assert outcome.code == RefusalCode.INVALID_INPUT
    assert "positive" in outcome.detail

    # All-zero weights
    all_zero_w = [Fraction(0), Fraction(0), Fraction(0)]
    outcome_all = matrix_quotient_l1(matrix, delta, all_zero_w)
    assert isinstance(outcome_all, Refused)
    assert outcome_all.code == RefusalCode.INVALID_INPUT


def test_adversarial_lp_ratio_test_zero_division_guard():
    """Verify that columns with 0, negative entries, or ratio ties never cause zero division in LP."""
    # A has 0 in pivot columns to test ratio guard
    # Minimize x1 + x2 subject to:
    #  0*x1 + 2*x2 = 4
    #  3*x1 + 0*x2 = 6
    # x1, x2 >= 0
    costs = [Fraction(1), Fraction(1)]
    matrix = [
        [Fraction(0), Fraction(2)],
        [Fraction(3), Fraction(0)],
    ]
    rhs = [Fraction(4), Fraction(6)]

    solved = solve_standard_lp(costs, matrix, rhs)
    assert isinstance(solved, Accepted)
    sol = solved.value
    assert sol.primal == (Fraction(2), Fraction(2))
    assert sol.value == Fraction(4)
    assert verify_standard_lp(costs, matrix, rhs, sol)


def test_adversarial_lp_degenerate_pivot_ties_and_bland_rule():
    """Verify that degenerate basic solutions (rhs = 0) break ties with Bland's rule without cycling."""
    # Classical cycling example (Beale's example) or degenerate rhs = 0
    # Minimize -0.75*x1 + 20*x2 - 0.5*x3 + 6*x4
    # subject to:
    # 0.25*x1 - 8*x2 - x3 + 9*x4 <= 0
    # 0.5*x1 - 12*x2 - 0.5*x3 + 3*x4 <= 0
    # x3 <= 1
    # Over exact rationals with slack variables:
    costs = [
        Fraction(-3, 4), Fraction(20), Fraction(-1, 2), Fraction(6),
        Fraction(0), Fraction(0), Fraction(0),
    ]
    matrix = [
        [Fraction(1, 4), Fraction(-8), Fraction(-1), Fraction(9), Fraction(1), Fraction(0), Fraction(0)],
        [Fraction(1, 2), Fraction(-12), Fraction(-1, 2), Fraction(3), Fraction(0), Fraction(1), Fraction(0)],
        [Fraction(0), Fraction(0), Fraction(1), Fraction(0), Fraction(0), Fraction(0), Fraction(1)],
    ]
    rhs = [Fraction(0), Fraction(0), Fraction(1)]

    # Bland's rule must solve this without infinite cycling or zero division
    solved = solve_standard_lp(costs, matrix, rhs, max_pivots=50)
    assert isinstance(solved, Accepted)
    assert verify_standard_lp(costs, matrix, rhs, solved.value)


def test_adversarial_lp_all_zero_and_singular_matrices():
    """Verify singular and all-zero constraint matrices are handled without unhandled crashes."""
    costs = [Fraction(1), Fraction(1)]
    zero_matrix = [[Fraction(0), Fraction(0)]]

    # Infeasible: 0*x1 + 0*x2 = 5
    rhs_infeasible = [Fraction(5)]
    outcome_inf = solve_standard_lp(costs, zero_matrix, rhs_infeasible)
    assert isinstance(outcome_inf, Refused)
    assert outcome_inf.code == RefusalCode.INFEASIBLE

    # Trivial feasible: 0*x1 + 0*x2 = 0
    rhs_zero = [Fraction(0)]
    outcome_feas = solve_standard_lp(costs, zero_matrix, rhs_zero)
    assert isinstance(outcome_feas, Accepted)
    assert outcome_feas.value.value == Fraction(0)


def test_adversarial_native_rust_zero_division_guard():
    """Verify that native Rust binary cleanly refuses zero denominator input without crash."""
    import json
    import subprocess
    from native_wdp import find_binary

    bin_path = find_binary("solve_wdp_obstruction")
    if bin_path is None:
        pytest.skip("solve_wdp_obstruction binary not found")

    payload = {
        "vertices": ["v0", "v1"],
        "edges": [["v0", "v1"]],
        "cochain": {"v0,v1": "5/0"},
    }
    proc = subprocess.run(
        [str(bin_path)],
        input=json.dumps(payload),
        text=True,
        capture_output=True,
        check=True,
    )
    resp = json.loads(proc.stdout)
    assert resp["status"] == "REFUSE"
    assert "division by zero" in resp["reason"].lower()


@settings(max_examples=30, deadline=None)
@given(
    c0=st.integers(min_value=-10, max_value=10),
    c1=st.integers(min_value=-10, max_value=10),
    a00=st.integers(min_value=-5, max_value=5),
    a01=st.integers(min_value=-5, max_value=5),
    a10=st.integers(min_value=-5, max_value=5),
    a11=st.integers(min_value=-5, max_value=5),
    b0=st.integers(min_value=-10, max_value=10),
    b1=st.integers(min_value=-10, max_value=10),
)
def test_adversarial_randomized_lp_fuzzing(c0, c1, a00, a01, a10, a11, b0, b1):
    """Stress-test randomized LP instances including singular matrices and zero RHS."""
    costs = [Fraction(c0), Fraction(c1)]
    matrix = [
        [Fraction(a00), Fraction(a01)],
        [Fraction(a10), Fraction(a11)],
    ]
    rhs = [Fraction(b0), Fraction(b1)]

    outcome = solve_standard_lp(costs, matrix, rhs, max_pivots=100)
    # Must return a valid Outcome without ZeroDivisionError or uncaught exception
    if isinstance(outcome, Accepted):
        assert verify_standard_lp(costs, matrix, rhs, outcome.value)
    else:
        assert isinstance(outcome, Refused)
        assert outcome.code in {
            RefusalCode.INFEASIBLE,
            RefusalCode.UNBOUNDED,
            RefusalCode.BUDGET_EXHAUSTED,
            RefusalCode.INVALID_INPUT,
        }
