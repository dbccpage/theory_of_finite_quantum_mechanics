"""Exact solver examples and certificate corruption regressions."""
from dataclasses import FrozenInstanceError, replace
from fractions import Fraction

import cochain_presentation as cp
import pytest
from sympy import Float, Matrix, Rational, Symbol, sqrt


@pytest.mark.parametrize("value, expected", [(2, Rational(2)), (Fraction(2, 3), Rational(2, 3)),
                                             ("2/3", Rational(2, 3)), (Rational(-1, 2), Rational(-1, 2))])
def test_exact_scalar_inputs(value, expected):
    assert cp._as_exact_rational(value) == expected


@pytest.mark.parametrize("value", [True, 1.5, Float(1.5), sqrt(2), Symbol("x"), object()])
def test_nonexact_scalar_inputs(value):
    with pytest.raises(TypeError):
        cp._as_exact_rational(value)


@pytest.mark.parametrize("repair, cochain, distance", [
    (Matrix.zeros(0, 0), Matrix.zeros(0, 1), 0),
    (Matrix.zeros(3, 0), Matrix([-2, 0, 3]), 5),
    (Matrix.eye(2), Matrix([3, -2]), 0),
    (Matrix([[1, 1], [0, 0]]), Matrix([2, 0]), 0),
    (Matrix([[1, 1], [0, 0]]), Matrix([0, 1]), 1),
    (Matrix([[0, 1], [0, -1], [0, 0]]), Matrix([2, -2, 1]), 1),
    (Matrix([[1], [2]]), Matrix([0, 2]), 1),
])
def test_primal_dual_certificates_cover_rank_and_boundary_cases(repair, cochain, distance):
    problem = cp.LinearRepairProblem(repair)
    q = problem.quotient_l1_distance(cochain)
    assert q.verify() and q.distance == distance
    exact = problem.exactness_certificate(cochain)
    assert exact.verify() and exact.is_exact_coboundary == (distance == 0)
    assert q.snapshot().verify()


def test_membership_witnesses_and_wrong_shape_reject():
    problem = cp.LinearRepairProblem(Matrix([[1], [-1]]))
    exact = problem.exactness_certificate(Matrix([2, -2]))
    assert not replace(exact, witness=None).verify()
    nonexact = problem.exactness_certificate(Matrix([1, 1]))
    assert not replace(nonexact, separating_pairing=None).verify()
    assert not replace(nonexact, separating_left_kernel_vector=None).verify()
    assert not replace(nonexact, separating_pairing=0).verify()
    for method in (problem.exactness_certificate, problem.quotient_l1_distance):
        with pytest.raises(ValueError, match="cochain has shape"):
            method(Matrix([[1, 2]]))
    assert not cp.exact_equal(Matrix([1]), Matrix([1, 2]))


@pytest.mark.parametrize("field, value", [
    ("repair_map", object()), ("cochain", Matrix([[1, 1]])),
    ("repair_witness", Matrix([0, 0])), ("residual", Matrix([0])),
    ("dual_witness", Matrix([0])), ("distance", True),
    ("distance", Float(2)), ("distance", "2"), ("distance", sqrt(2)),
    ("dual_pairing", False), ("cochain", Matrix([Float(1), 1])),
    ("cochain", Matrix([sqrt(2), 1])),
    ("residual", Matrix([0, 0])), ("distance", Rational(3)),
    ("dual_witness", Matrix([1, -1])),
    ("dual_witness", Matrix([2, 2])),
    ("dual_pairing", Rational(3)),
])
def test_corrupt_quotient_certificates_reject(field, value):
    valid = cp.LinearRepairProblem(Matrix([[1], [-1]])).quotient_l1_distance(Matrix([1, 1]))
    assert valid.verify()
    assert not replace(valid, **{field: value}).verify()


def test_certificate_is_immutable_and_detached_from_input():
    cochain = Matrix([1, 1])
    q = cp.LinearRepairProblem(Matrix([[1], [-1]])).quotient_l1_distance(cochain)
    copy = q.snapshot()
    cochain[0] = 99
    assert copy.verify() and copy.cochain == Matrix([1, 1])
    with pytest.raises(FrozenInstanceError):
        copy.distance = Rational(99)
    with pytest.raises(TypeError):
        copy.residual[0] = 99


def test_solver_refuses_corrupted_backend_results(monkeypatch):
    problem = cp.LinearRepairProblem(Matrix([[1], [-1]]))
    with monkeypatch.context() as context:
        context.setattr(cp.ExactnessCertificate, "verify", lambda _: False)
        with pytest.raises(ArithmeticError, match="exactness certificate"):
            problem.exactness_certificate(Matrix([2, -2]))
    with monkeypatch.context() as context:
        context.setattr(cp, "_exact_l1_dual_vertex", lambda *_: (Matrix([0, 0]), Rational(99)))
        with pytest.raises(ArithmeticError, match="optima disagree"):
            problem.quotient_l1_distance(Matrix([1, 1]))
    with monkeypatch.context() as context:
        context.setattr(cp.QuotientDistanceCertificate, "verify", lambda _: False)
        with pytest.raises(ArithmeticError, match="quotient certificate"):
            problem.quotient_l1_distance(Matrix([1, 1]))
    with pytest.raises(ArithmeticError, match="independent-column"):
        cp._independent_column_indices(Matrix.zeros(2, 2), 1)
    # Enumeration unexpectedly empty must fail, never manufacture a certificate.
    with monkeypatch.context() as context:
        context.setattr(cp, "_independent_column_indices", lambda *_: (0,))
        context.setattr(cp, "combinations", lambda *_: iter(()))
        with pytest.raises(ArithmeticError, match="no candidates"):
            cp._exact_l1_primal_vertex(problem.d0, Matrix([1, 1]))
        with pytest.raises(ArithmeticError, match="no dual"):
            cp._exact_l1_dual_vertex(problem.d0, Matrix([1, 1]))

