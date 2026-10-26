"""Projection hypotheses, constructor boundaries, and certificate fail-closed checks."""
from types import SimpleNamespace

import coda_a_core as a
import numpy as np
import pytest
from sympy import Matrix, Rational, symbols


def test_exact_scalar_and_dimension_boundaries():
    assert a._validate_exact_rational("2/3", "x") == Rational(2, 3)
    for invalid in ["not rational", object()]:
        with pytest.raises(TypeError):
            a._validate_exact_rational(invalid, "x")
    assert a._validate_exact_int(0, "n") == 0
    with pytest.raises(ValueError):
        a._validate_exact_int(-1, "n")
    with pytest.raises(TypeError):
        a._validate_exact_int(np.float64(1), "n")
    assert a.residual(Matrix.zeros(2), Matrix([[1, 2]])) == Matrix([1, 2])
    with pytest.raises(ValueError, match="column vector"):
        a.residual(Matrix.eye(2), Matrix.eye(2))
    with pytest.raises(ValueError, match="square"):
        a.is_projection(Matrix([[1, 2]]))


@pytest.mark.parametrize("transport, source, target", [
    (Matrix.eye(2), Matrix([[1, 0]]), Matrix.eye(2)),
    (Matrix.eye(2), Matrix.eye(2), Matrix([[1, 0]])),
    (Matrix([[1, 0]]), Matrix.eye(3), Matrix.eye(1)),
    (Matrix([[1, 0]]), Matrix.eye(2), Matrix.eye(2)),
])
def test_transport_requires_matching_linear_spaces(transport, source, target):
    with pytest.raises(ValueError):
        a.maps_commute(transport, source, target)


def test_nonprojection_residual_is_not_promised_to_be_in_kernel():
    correction = Matrix([[0, 1], [0, 0]])
    residual = a.residual(correction, Matrix([0, 1]))
    assert correction * residual == Matrix([1, 0])
    with pytest.raises(ValueError, match="idempotence"):
        a.induced_quotient_section(correction, Matrix([0, 1]))


def test_quotient_factor_rejects_wrong_domain_and_untrusted_solver(monkeypatch):
    with pytest.raises(ValueError, match="domain dimension"):
        a.quotient_universal_factor(Matrix([[1, 0]]), Matrix([[1]]))
    monkeypatch.setattr(type(Matrix.eye(1)), "gauss_jordan_solve", lambda self, other: (Matrix([[symbols("t")]]), Matrix.zeros(0, 1)))
    with pytest.raises(ValueError, match="not unique"):
        a.quotient_universal_factor(Matrix([[1]]), Matrix([[1]]))
    monkeypatch.setattr(type(Matrix.eye(1)), "gauss_jordan_solve", lambda self, other: (Matrix([[0]]), Matrix.zeros(0, 1)))
    with pytest.raises(ArithmeticError, match="factorization failed"):
        a.quotient_universal_factor(Matrix([[1]]), Matrix([[1]]))


@pytest.mark.parametrize("changes", [dict(packet_id=1), dict(terminalizer_id=1), dict(replayable="False")])
def test_authority_evidence_requires_typed_fields(changes):
    fields = dict(packet_id="p", terminalizer_id="t", replayable=True)
    fields.update(changes)
    with pytest.raises(TypeError):
        a.AuthEvidence(**fields)


def test_residual_outcome_types_and_administrative_absence():
    fields = dict(classification=a.ResidualTerminalClass.CLOSURE_ABSORBED, residual_class_id="r", defect_vector=None, quotient_distance=0, is_closed=True)
    for change, error in [(dict(classification="ClosureAbsorbed"), TypeError), (dict(is_closed=1), TypeError), (dict(is_closed=False), ValueError), (dict(classification=a.ResidualTerminalClass.LIFT_REQUIRED), ValueError)]:
        with pytest.raises(error):
            a.ResidualOutcome(**(fields | change))
    assert a.ResidualOutcome(**fields).defect_vector is None
    assert a.ResidualOutcome(**(fields | dict(classification=a.ResidualTerminalClass.LIFT_REQUIRED, quotient_distance=None))).quotient_distance is None


def test_classifier_checks_dimensions_and_supports_absent_or_empty_d1():
    with pytest.raises(ValueError, match="d0 rows"):
        a.classify_closure_attempt(Matrix.zeros(1, 0), None, Matrix([0, 0]))
    for d1 in [None, Matrix.zeros(0, 2)]:
        outcome = a.classify_closure_attempt(Matrix.zeros(2, 0), d1, Matrix([1, 0]))
        assert outcome.classification is a.ResidualTerminalClass.CLOSED_RESIDUAL


@pytest.mark.parametrize("verified,distance,match", [(False, 1, "verification failed"), (True, -1, "negative quotient")])
def test_classifier_rejects_corrupt_solver_receipts(monkeypatch, verified, distance, match):
    fake = SimpleNamespace(verify=lambda: verified, distance=Rational(distance))
    monkeypatch.setattr(a.LinearRepairProblem, "quotient_l1_distance", lambda self, cochain: fake)
    with pytest.raises(ArithmeticError, match=match):
        a.classify_closure_attempt(Matrix.eye(1), None, Matrix([1]))
