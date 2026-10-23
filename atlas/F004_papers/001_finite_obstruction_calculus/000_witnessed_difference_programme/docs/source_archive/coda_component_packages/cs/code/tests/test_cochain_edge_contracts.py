"""Exact solver edge cases and independent certificate tamper checks."""
from dataclasses import replace
from fractions import Fraction

import cochain_presentation as cp
import pytest
from sympy import Float, Matrix, Rational, symbols


@pytest.mark.parametrize("value, expected", [(2, Rational(2)), (Fraction(2, 3), Rational(2, 3)), ("2/3", Rational(2, 3)), (Rational(3, 5), Rational(3, 5))])
def test_exact_scalar_inputs(value, expected):
    assert cp._as_exact_rational(value) == expected


@pytest.mark.parametrize("value", [True, 0.5, Float("0.5"), object(), symbols("x")])
def test_inexact_or_symbolic_scalars_are_rejected(value):
    with pytest.raises(TypeError):
        cp._as_exact_rational(value)


def test_exact_equality_checks_shape_and_entries():
    assert not cp.exact_equal(Matrix([1]), Matrix([1, 0]))
    assert not cp.exact_equal(Matrix([1]), Matrix([2]))
    assert cp.exact_equal(Matrix([Rational(2, 3)]), Matrix([Rational(4, 6)]))


@pytest.mark.parametrize("repair, omega, distance", [
    (Matrix.zeros(0, 0), Matrix.zeros(0, 1), 0),
    (Matrix.zeros(3, 0), Matrix([-2, 0, 3]), 5),
    (Matrix.eye(2), Matrix([3, -4]), 0),
    (Matrix([[0, 0], [0, 1], [0, 2]]), Matrix([3, 1, 4]), 4),
    (Matrix([[1], [3], [0]]), Matrix([1, 1, 2]), Rational(8, 3)),
])
def test_degenerate_and_rank_deficient_primal_dual_certificates(repair, omega, distance):
    cert = cp.LinearRepairProblem(repair).quotient_l1_distance(omega)
    assert cert.verify()
    assert cert.distance == distance
    assert cert.dual_pairing == distance


def test_exactness_witness_and_separator_are_independently_checked():
    problem = cp.LinearRepairProblem(Matrix([[1, 1], [0, 0]]))
    exact = problem.exactness_certificate(Matrix([2, 0]))
    assert exact.is_exact_coboundary and exact.verify()
    assert not replace(exact, witness=None).verify()
    assert not replace(exact, witness=Matrix([0, 0])).verify()
    nonexact = problem.exactness_certificate(Matrix([2, 3]))
    assert not nonexact.is_exact_coboundary and nonexact.verify()
    assert not replace(nonexact, separating_left_kernel_vector=None).verify()
    assert not replace(nonexact, separating_pairing=None).verify()
    assert not replace(nonexact, separating_pairing=0).verify()
    assert not replace(nonexact, separating_left_kernel_vector=Matrix([1, 0])).verify()


def test_quotient_certificate_rejects_independent_tampering():
    cert = cp.LinearRepairProblem(Matrix([[1], [0]])).quotient_l1_distance(Matrix([2, 3]))
    corruptions = [
        {"residual": Matrix([0, 4])}, {"distance": 4},
        {"dual_witness": Matrix([0])}, {"dual_witness": Matrix([1, 1])},
        {"dual_witness": Matrix([0, 2])}, {"dual_pairing": 2},
    ]
    for change in corruptions:
        assert not replace(cert, **change).verify()
    empty = cp.LinearRepairProblem(Matrix.zeros(0, 0)).quotient_l1_distance(Matrix.zeros(0, 1))
    assert not replace(empty, dual_pairing=1).verify()


@pytest.mark.parametrize("operation", ["exactness_certificate", "quotient_l1_distance"])
def test_cochain_dimension_mismatch_is_rejected(operation):
    with pytest.raises(ValueError, match="shape"):
        getattr(cp.LinearRepairProblem(Matrix.eye(2)), operation)(Matrix([1]))


def test_inconsistent_rank_claim_cannot_fabricate_a_basis():
    with pytest.raises(ArithmeticError, match="independent-column"):
        cp._independent_column_indices(Matrix.zeros(2, 2), 1)


def test_solver_rechecks_a_corrupted_exactness_certificate(monkeypatch):
    monkeypatch.setattr(cp.ExactnessCertificate, "verify", lambda self: False)
    with pytest.raises(ArithmeticError, match="exactness certificate"):
        cp.LinearRepairProblem(Matrix.eye(1)).exactness_certificate(Matrix([1]))


def test_solver_rejects_disagreeing_primal_dual_receipts(monkeypatch):
    monkeypatch.setattr(cp, "_exact_l1_dual_vertex", lambda a, b: (Matrix([0]), Rational(1)))
    with pytest.raises(ArithmeticError, match="optima disagree"):
        cp.LinearRepairProblem(Matrix.eye(1)).quotient_l1_distance(Matrix([1]))


def test_solver_rechecks_a_corrupted_quotient_certificate(monkeypatch):
    monkeypatch.setattr(cp.QuotientDistanceCertificate, "verify", lambda self: False)
    with pytest.raises(ArithmeticError, match="quotient certificate"):
        cp.LinearRepairProblem(Matrix.eye(1)).quotient_l1_distance(Matrix([1]))
