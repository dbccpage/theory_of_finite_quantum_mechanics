# -*- coding: utf-8 -*-
"""
Adversarial tests for CODA's exact-arithmetic discipline.

Claims under attack: value_objects.py ("Pure immutable objects with strict value
equality, fail-closed validation, and zero float tolerance";
validate_exact_rational "rejecting floats and non-exact primitives"), the
ExactRational / DualWitness value objects, and the numerator-sign tests that
Layers 6 and 8 use as proxies for the sign of a rational.

AuthorityEffect: None.
"""

from __future__ import annotations

from decimal import Decimal
from fractions import Fraction

import pytest
import sympy
from sympy import Float, Matrix, Rational

from coda_application.domain.entities import ResidualPair, TerminalKind
from coda_application.domain.layers.layer5_q import Layer5Q
from coda_application.domain.layers.layer6_a import Layer6A
from coda_application.domain.layers.layer8_fda import Layer8FDA
from coda_application.domain.value_objects import (
    DualWitness,
    ExactRational,
    FirewallDecision,
    validate_exact_rational,
)
from coda_application.tests.adversarial._support import make_problem, rejects
from coda_application.application import evaluate_coda_pipeline

ONE = ExactRational(1, 1)


# ------------------------------------------------------- float smuggling


# FIXED 2026-09-23 (was BREAK EXA-01: sympy.Float is not a Python float, so 0.1 is admitted as 3602879701896397/36028797018963968)
def test_sympy_float_rejected():
    assert rejects(lambda: validate_exact_rational(Float(0.1)), TypeError)


# FIXED 2026-09-23 (was BREAK EXA-02: high-precision sympy.Float is admitted the same way)
def test_high_precision_sympy_float_rejected():
    assert rejects(lambda: validate_exact_rational(Float("0.1", 50)), TypeError)


# FIXED 2026-09-23 (was BREAK EXA-03: str(0.1 + 0.2) launders a float rounding artifact into an 'exact' 30000000000000004/10^17)
def test_float_repr_string_rejected():
    assert rejects(lambda: validate_exact_rational(str(0.1 + 0.2)), TypeError)


# FIXED 2026-09-23 (was BREAK EXA-04: a Python float inside a sympy Matrix becomes sympy.Float; the float cochain is AUTHORIZED)
def test_float_cochain_not_authorized():
    problem = make_problem(defect_cochain=Matrix([0.1, -0.1]), fda_license_granted=True)
    try:
        out = evaluate_coda_pipeline(problem)
    except TypeError:
        return
    assert out.terminal_kind != TerminalKind.AUTHORIZED


# FIXED 2026-09-23 (was BREAK EXA-05: sympy.Float enclosure bounds pass Layer 5's exact validation)
def test_float_enclosure_bounds_rejected():
    problem = make_problem(enclosure_interval=(Float(0.1), Float(0.3)))
    assert rejects(lambda: Layer5Q.evaluate(problem), TypeError)


# FIXED 2026-09-23 (was BREAK EXA-06: sympy.Float section values pass Layer 2/4 exact validation)
def test_float_section_values_rejected():
    problem = make_problem(local_sections={"U0": (Float(0.1),), "U1": (Float(0.2),)})
    try:
        out = evaluate_coda_pipeline(problem)
    except TypeError:
        return
    assert out.terminal_kind == TerminalKind.REFUSED


def test_python_float_rejected():
    """HELD: a bare Python float is refused."""
    assert rejects(lambda: validate_exact_rational(0.1), TypeError)


def test_numpy_float64_rejected():
    """HELD: numpy.float64 subclasses float and is refused."""
    np = pytest.importorskip("numpy")
    assert rejects(lambda: validate_exact_rational(np.float64(0.1)), TypeError)


def test_numpy_float32_rejected():
    """HELD: numpy.float32 is refused through the coercion error path."""
    np = pytest.importorskip("numpy")
    assert rejects(lambda: validate_exact_rational(np.float32(0.1)), TypeError)


def test_decimal_refused_conservatively():
    """HELD: Decimal is refused (conservative, even though Decimal('0.1') is exact)."""
    assert rejects(lambda: validate_exact_rational(Decimal("0.1")), TypeError)


def test_bool_rejected():
    """HELD: bool is refused even though it is an int subclass."""
    assert rejects(lambda: validate_exact_rational(True), TypeError)


def test_numpy_bool_rejected():
    """HELD: numpy.bool_ is refused."""
    np = pytest.importorskip("numpy")
    assert rejects(lambda: validate_exact_rational(np.True_), TypeError)


def test_fraction_admitted_exactly():
    """HELD: fractions.Fraction is exact and is admitted unchanged."""
    assert validate_exact_rational(Fraction(1, 3)) == Rational(1, 3)


def test_irrationals_and_infinities_rejected():
    """HELD: sqrt(2), pi, oo, nan and zoo are all refused."""
    for value in (sympy.sqrt(2), sympy.pi, sympy.oo, sympy.nan, sympy.zoo):
        assert rejects(lambda v=value: validate_exact_rational(v), TypeError), value


def test_huge_rational_round_trips():
    """HELD: 10^5000 / 3 survives the ExactRational round trip."""
    big = Rational(10**5000, 3)
    assert ExactRational.from_rational(big).sympy_rational == big


# ------------------------------------------------- value-object integrity


# FIXED 2026-09-23 (was BREAK EXA-07: ExactRational(1,2) != ExactRational(2,4): 'strict value equality' is field equality)
def test_exact_rational_value_equality():
    assert ExactRational(1, 2) == ExactRational(2, 4)


# FIXED 2026-09-23 (was BREAK EXA-08: equal rationals hash apart: a set holds both 1/2 and 2/4)
def test_exact_rational_hash_consistency():
    assert len({ExactRational(1, 2), ExactRational(2, 4)}) == 1


# FIXED 2026-09-23 (was BREAK EXA-09: ExactRational(1.5, 1) is constructed and silently becomes 3/2)
def test_exact_rational_rejects_float_field():
    assert rejects(lambda: ExactRational(1.5, 1), TypeError, ValueError)


# FIXED 2026-09-23 (was BREAK EXA-10: ExactRational(True, 1) is constructed)
def test_exact_rational_rejects_bool_field():
    assert rejects(lambda: ExactRational(True, 1), TypeError, ValueError)


# FIXED 2026-09-23 (was BREAK EXA-11: ExactRational('1', '2') is constructed; to_tuple() returns strings)
def test_exact_rational_rejects_str_fields():
    assert rejects(lambda: ExactRational("1", "2"), TypeError, ValueError)


def test_exact_rational_zero_denominator_rejected():
    """HELD: a zero denominator is refused."""
    assert rejects(lambda: ExactRational(1, 0), ZeroDivisionError)


# FIXED 2026-09-23 (was BREAK EXA-12: Layer 6 tests numerator > 0: ExactRational(-1,-2) = 1/2 is reported as a vanishing residue)
def test_layer6_sign_uses_value_not_numerator():
    rec, has_residual = Layer6A.evaluate(make_problem(), ExactRational(-1, -2), ExactRational(0, 1))
    assert has_residual is True


# FIXED 2026-09-23 (was BREAK EXA-13: Layer 8 tests numerator > 0: Phi_1 = (-1)/(-2) = 1/2 is AUTHORIZED under license)
def test_layer8_sign_uses_value_not_numerator():
    _rec, decision, token = Layer8FDA.evaluate(
        make_problem(fda_license_granted=True), ExactRational(-1, -2), ExactRational(0, 1), refused_by_or=False
    )
    assert decision != FirewallDecision.PERMIT_AUTHORIZED and token is None


# FIXED 2026-09-23 (was BREAK EXA-14: Layer 7 tests gamma2.numerator > 0: Gamma_2 = (-3)/(-1) = 3 passes the cocycle sieve)
def test_layer7_sign_uses_value_not_numerator():
    from coda_application.domain.layers.layer7_or import Layer7OR

    _rec, refused = Layer7OR.evaluate(make_problem(), ExactRational(-3, -1))
    assert refused is True


def test_residual_pair_zero_with_negative_denominator():
    """HELD: 0/-5 is still recognised as zero."""
    assert ResidualPair(ExactRational(0, -5), ExactRational(0, 7)).is_exact_zero


# -------------------------------------------------------- DualWitness


# FIXED 2026-09-23 (was BREAK EXA-15: DualWitness accepts a (1, 0) entry; to_matrix() yields zoo instead of refusing)
def test_dual_witness_rejects_zero_denominator():
    assert rejects(
        lambda: DualWitness(witness_vector=((1, 0),), pairing_value=ONE),
        ZeroDivisionError,
        ValueError,
        TypeError,
    )


# FIXED 2026-09-23 (was BREAK EXA-16: DualWitness accepts float entries ((0.5, 1),))
def test_dual_witness_rejects_float_entries():
    assert rejects(
        lambda: DualWitness(witness_vector=((0.5, 1),), pairing_value=ONE),
        TypeError,
        ValueError,
    )


def test_native_evaluator_checks_dual_bound_without_norm_metadata():
    """Zero cochain isolates dual feasibility from pairing and annihilation."""
    from coda_application.infrastructure.native_functional_adapter import NativeFunctionalEvaluator

    evaluator = NativeFunctionalEvaluator()
    for entry, accepted in ((1, True), (5, False)):
        candidate = DualWitness(witness_vector=((entry, 1),), pairing_value=ExactRational(0, 1))
        assert evaluator.verify_repair(
            [{}], 1, [Fraction(0)], [Fraction(0)], candidate.fractions, Fraction(0)
        ) is accepted


# FIXED 2026-09-23 (was BREAK EXA-18: a Matrix with float entries flows into the anomalon fingerprint path and crashes (.p missing))
def test_float_matrix_entries_do_not_crash_fingerprinting():
    from coda_application.domain.anomalon_registry import AnomalonRegistry

    try:
        AnomalonRegistry().register_anomalon(
            problem_id="f",
            phi1=ONE,
            gamma2=ExactRational(0, 1),
            d0=Matrix([[1.0], [-1.0]]),
            d1=Matrix.zeros(1, 2),
            defect=Matrix([1, 1]),
            dual_witness=None,
        )
    except (ValueError, TypeError):
        pass  # a typed refusal is the acceptable fail-closed outcome
