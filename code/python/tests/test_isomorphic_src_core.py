"""Unit tests verifying parity between Python src/ and Rust src/ exact algebra engines."""

from fractions import Fraction
import pytest

from src.linear_algebra import ExactMatrix, GaussianRational
from src.homology import Carrier
from src.qm import DensityOperator


def test_exact_rational_rref_and_rank():
    rows = [
        [Fraction(1), Fraction(2), Fraction(3)],
        [Fraction(4), Fraction(5), Fraction(6)],
        [Fraction(7), Fraction(8), Fraction(9)],
    ]
    mat = ExactMatrix.from_rows(rows)
    assert mat.rank() == 2

    k = mat.kernel_basis()
    assert len(k) == 1
    null_vec = k[0]
    prod = mat.mul_vec(null_vec)
    assert prod == [Fraction(0), Fraction(0), Fraction(0)]


def test_exact_determinant_and_inverse():
    rows = [
        [Fraction(1), Fraction(2)],
        [Fraction(3), Fraction(4)],
    ]
    mat = ExactMatrix.from_rows(rows)
    assert mat.determinant() == Fraction(-2)

    inv = mat.inverse()
    expected = ExactMatrix.from_rows([
        [Fraction(-2), Fraction(1)],
        [Fraction(3, 2), Fraction(-1, 2)],
    ])
    assert inv == expected
    assert mat * inv == ExactMatrix.identity(2)


def test_gaussian_rational_unitary():
    # Pauli-Y: [[0, -i], [i, 0]]
    rows = [
        [GaussianRational(0, 0), GaussianRational(0, -1)],
        [GaussianRational(0, 1), GaussianRational(0, 0)],
    ]
    py_mat = ExactMatrix.from_rows(rows)
    assert py_mat.is_hermitian()
    assert py_mat.is_unitary()


def test_homology_carrier_parity():
    # Triangle cycle
    d0_rows = [
        [Fraction(-1), Fraction(1), Fraction(0)],
        [Fraction(0), Fraction(-1), Fraction(1)],
        [Fraction(1), Fraction(0), Fraction(-1)],
    ]
    d0 = ExactMatrix.from_rows(d0_rows)
    d1_rows = [[Fraction(1), Fraction(1), Fraction(1)]]
    d1 = ExactMatrix.from_rows(d1_rows)
    weights = [Fraction(1), Fraction(1), Fraction(1)]

    carrier = Carrier(3, 3, 1, d0, d1, weights)
    assert carrier.rank_d0() == 2
    assert carrier.rank_d1() == 1
    assert carrier.dim_q1() == 1
    assert carrier.dim_h1() == 0


def test_density_operator_and_observable():
    # Pure qubit state |0><0|
    rows = [
        [GaussianRational(1, 0), GaussianRational(0, 0)],
        [GaussianRational(0, 0), GaussianRational(0, 0)],
    ]
    mat = ExactMatrix.from_rows(rows)
    rho = DensityOperator(mat)
    assert rho.purity() == Fraction(1)

    # Pauli-Z
    sigma_z = ExactMatrix.from_rows([
        [GaussianRational(1, 0), GaussianRational(0, 0)],
        [GaussianRational(0, 0), GaussianRational(-1, 0)],
    ])
    assert rho.expectation(sigma_z) == GaussianRational(1, 0)