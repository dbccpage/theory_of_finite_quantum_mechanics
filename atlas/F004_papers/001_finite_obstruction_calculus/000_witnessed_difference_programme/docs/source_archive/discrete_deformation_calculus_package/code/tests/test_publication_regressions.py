"""Publication regressions for exact inputs and the meaning of R's norms."""

from dataclasses import replace
from fractions import Fraction as F
from itertools import combinations

import cochain as c
import pytest
from residual_projection import GraphResidualProjector, XiTiePrecondition, evaluate_xi_tie_break
from structural_lift import FiniteLambdaLedger, FiniteLambdaStep


@pytest.mark.parametrize("bad", [0.5, True, "1", F(-1)])
def test_lambda_rows_and_endpoints_refuse_inexact_or_negative_diagnostics(bad):
    step = FiniteLambdaStep(2, 0, 1, 0, True, True)
    for name in ("before_phi", "before_gamma", "after_phi", "after_gamma"):
        with pytest.raises(ValueError):
            replace(step, **{name: bad})
    ledger = FiniteLambdaLedger.new((2, 0), [step], (1, 0))
    for name in ("initial_phi", "initial_gamma", "terminal_phi", "terminal_gamma"):
        with pytest.raises(ValueError):
            replace(ledger, **{name: bad})
    with pytest.raises(ValueError):
        FiniteLambdaLedger.new((bad, 0), [], (0, 0))
    with pytest.raises(ValueError):
        FiniteLambdaLedger.new((0, 0), [], (bad, 0))


@pytest.mark.parametrize("bad", [1, "False", None])
def test_lambda_flags_are_booleans_instead_of_truthy_claims(bad):
    step = FiniteLambdaStep(2, 0, 1, 0, True, True)
    for name in ("is_descent", "is_valid"):
        with pytest.raises(TypeError, match="must be bool"):
            replace(step, **{name: bad})


def test_lambda_ledger_snapshots_rows_and_normalizes_exact_integer_inputs():
    first = FiniteLambdaStep(2, 0, 1, 0, True, True)
    last = FiniteLambdaStep(1, 0, 0, 0, False, True)
    rows = [first, last]
    # Direct construction must have the same boundary as the convenience constructor.
    ledger = FiniteLambdaLedger(2, 0, rows, 0, 0)
    rows.clear()
    assert ledger.steps == (first, last) and ledger.require_chained()
    assert type(ledger.initial_phi) is F and type(first.before_phi) is F
    with pytest.raises(TypeError, match="FiniteLambdaStep"):
        replace(ledger, steps=(object(),))


@pytest.mark.parametrize("bad", [0.5, True, "1", F(-1)])
def test_xi_primary_diagnostics_have_the_state_exact_nonnegative_domain(bad):
    precondition = XiTiePrecondition(1, 0, 1, 0)
    assert type(precondition.phi1_a) is F and precondition.is_satisfied()
    for name in ("phi1_a", "gamma2_a", "phi1_b", "gamma2_b"):
        with pytest.raises(ValueError):
            replace(precondition, **{name: bad})
        args = dict(candidate_a="a", phi1_a=1, gamma2_a=0, xi_a=2,
                    candidate_b="b", phi1_b=1, gamma2_b=0, xi_b=1)
        args[name] = bad
        with pytest.raises(ValueError):
            evaluate_xi_tie_break(**args)


def test_forest_register_norm_is_not_the_quotient_minimum():
    vertices = tuple("abcd")
    edges = tuple(combinations(vertices, 2))
    cx = c.Complex(vertices, edges)
    x = (F(-1),) * 6
    receipt = GraphResidualProjector(list(vertices), list(edges)).project(dict(zip(edges, x)))
    residual = tuple(receipt.residual_component[e] for e in edges)
    difference = tuple(a - b for a, b in zip(x, residual))
    assert receipt.cycle_coordinates == (F(-1),) * 3
    assert receipt.residual_norm == 3
    assert c.exact_potential(cx, difference) is not None
    assert c.phi1_certificate(cx, x).value == c.phi1_certificate(cx, residual).value == 2
    assert c.gamma2(cx, x) == c.gamma2(cx, residual) == 0
