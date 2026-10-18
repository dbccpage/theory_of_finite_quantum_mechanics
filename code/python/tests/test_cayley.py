"""Tests for ComplexRational, ComplexMatrix, and Cayley unitary charts."""

import pytest
from fractions import Fraction
from src.lie_theory.cayley import (
    ComplexRational,
    ComplexMatrix,
    cayley_unitary,
    cayley_generator,
    pauli_matrices,
)


def test_complex_rational_arithmetic():
    z1 = ComplexRational(1, 2)  # 1 + 2i
    z2 = ComplexRational(3, -4)  # 3 - 4i

    assert z1 + z2 == ComplexRational(4, -2)
    assert z1 - z2 == ComplexRational(-2, 6)
    # (1 + 2i)(3 - 4i) = 3 - 4i + 6i + 8 = 11 + 2i
    assert z1 * z2 == ComplexRational(11, 2)
    # Division
    assert (z1 * z2) / z2 == z1
    assert z1.norm_sq() == Fraction(5)
    assert z1.conjugate() == ComplexRational(1, -2)


def test_pauli_matrices():
    sx, sy, sz = pauli_matrices()

    # All Pauli matrices are Hermitian
    assert sx.is_hermitian()
    assert sy.is_hermitian()
    assert sz.is_hermitian()

    # Pauli squares are identity
    id2 = ComplexMatrix.identity(2)
    assert sx.multiply(sx)._data == id2._data
    assert sy.multiply(sy)._data == id2._data
    assert sz.multiply(sz)._data == id2._data


def test_cayley_unitary_and_roundtrip():
    sx, sy, sz = pauli_matrices()

    # Cayley transform of sz with tau = 1
    u = cayley_unitary(sz, 1)
    assert u.is_unitary()

    # Inverse Cayley transform returns generator sz
    h_recovered = cayley_generator(u)
    assert h_recovered.is_hermitian()
    for i in range(2):
        for j in range(2):
            assert h_recovered[i][j] == sz[i][j]


def test_cayley_scaled_generator():
    sx, sy, sz = pauli_matrices()
    # Scaled Pauli matrix 2*sz
    h2 = sz.scale(ComplexRational(2))
    assert h2.is_hermitian()

    u = cayley_unitary(h2, 1)
    assert u.is_unitary()

    h_rec = cayley_generator(u)
    for i in range(2):
        for j in range(2):
            assert h_rec[i][j] == h2[i][j]
