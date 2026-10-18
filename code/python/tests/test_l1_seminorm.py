"""Tests for exact weighted L1 quotient seminorm evaluator."""

import pytest
from fractions import Fraction
from src.functional.l1_seminorm import (
    L1Seminorm,
    ExactPhi1Certificate,
)


def test_zero_certificate():
    boundary = [[Fraction(1)], [Fraction(-1)]]
    weights = [Fraction(1), Fraction(1)]
    semi = L1Seminorm(boundary, weights)

    cert = ExactPhi1Certificate(
        omega=[Fraction(0), Fraction(0)],
        d0=boundary,
        weights=weights,
        alpha=[Fraction(0)],
        primal_residual=[Fraction(0), Fraction(0)],
        dual_witness=[Fraction(0), Fraction(0)],
        reported_value=Fraction(0),
    )
    verified = semi.verify_certificate(cert)
    assert verified.value == Fraction(0)


def test_quotient_projection_reduction():
    # B = [[1], [1]], weights = [1, 1]
    # omega = [2, 0]
    # alpha = [1] => r = [1, -1]
    # z = [1, -1] => B^T z = 1 - 1 = 0
    # Primal cost = 1*|1| + 1*|-1| = 2
    # Dual value = 1*2 + (-1)*0 = 2
    boundary = [[Fraction(1)], [Fraction(1)]]
    weights = [Fraction(1), Fraction(1)]
    semi = L1Seminorm(boundary, weights)

    cert = ExactPhi1Certificate(
        omega=[Fraction(2), Fraction(0)],
        d0=boundary,
        weights=weights,
        alpha=[Fraction(1)],
        primal_residual=[Fraction(1), Fraction(-1)],
        dual_witness=[Fraction(1), Fraction(-1)],
        reported_value=Fraction(2),
    )
    verified = semi.verify_certificate(cert)
    assert verified.value == Fraction(2)


def test_boundary_binding_mismatch():
    boundary = [[Fraction(1)], [Fraction(1)]]
    weights = [Fraction(1), Fraction(1)]
    semi = L1Seminorm(boundary, weights)

    # Different boundary in certificate
    other_boundary = [[Fraction(1)], [Fraction(-1)]]
    cert = ExactPhi1Certificate(
        omega=[Fraction(0), Fraction(0)],
        d0=other_boundary,
        weights=weights,
        alpha=[Fraction(0)],
        primal_residual=[Fraction(0), Fraction(0)],
        dual_witness=[Fraction(0), Fraction(0)],
        reported_value=Fraction(0),
    )
    with pytest.raises(ValueError, match="Boundary binding mismatch"):
        semi.verify_certificate(cert)


def test_dual_orthogonality_violation():
    boundary = [[Fraction(1)], [Fraction(1)]]
    weights = [Fraction(1), Fraction(1)]
    semi = L1Seminorm(boundary, weights)

    # z = [1, 1] => B^T z = 1 + 1 = 2 != 0
    cert = ExactPhi1Certificate(
        omega=[Fraction(2), Fraction(0)],
        d0=boundary,
        weights=weights,
        alpha=[Fraction(1)],
        primal_residual=[Fraction(1), Fraction(-1)],
        dual_witness=[Fraction(1), Fraction(1)],
        reported_value=Fraction(2),
    )
    with pytest.raises(ValueError, match="Dual witness not orthogonal"):
        semi.verify_certificate(cert)
