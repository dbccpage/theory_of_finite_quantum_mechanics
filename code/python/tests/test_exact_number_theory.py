"""Tests for exact polynomial algebra, cyclotomics, and quadratic fields."""

from fractions import Fraction
from src.number_theory.exact_number_theory import (
    ExactPolynomial,
    QuadraticExtension,
)


def test_polynomial_arithmetic():
    # p1 = x + 1, p2 = x - 1
    p1 = ExactPolynomial.from_ints(1, 1)
    p2 = ExactPolynomial.from_ints(-1, 1)

    # p1 * p2 = x^2 - 1
    prod = p1 * p2
    assert prod.coeffs == (Fraction(-1), Fraction(0), Fraction(1))

    # divmod: (x^2 - 1) / (x - 1) = x + 1 remainder 0
    q, rem = prod.divmod(p2)
    assert q == p1
    assert rem.is_zero()


def test_cyclotomic_polynomials():
    # Phi_1(x) = x - 1
    phi1 = ExactPolynomial.cyclotomic(1)
    assert phi1.coeffs == (Fraction(-1), Fraction(1))

    # Phi_2(x) = x + 1
    phi2 = ExactPolynomial.cyclotomic(2)
    assert phi2.coeffs == (Fraction(1), Fraction(1))

    # Phi_3(x) = x^2 + x + 1
    phi3 = ExactPolynomial.cyclotomic(3)
    assert phi3.coeffs == (Fraction(1), Fraction(1), Fraction(1))

    # Phi_4(x) = x^2 + 1
    phi4 = ExactPolynomial.cyclotomic(4)
    assert phi4.coeffs == (Fraction(1), Fraction(0), Fraction(1))

    # Phi_6(x) = x^2 - x + 1
    phi6 = ExactPolynomial.cyclotomic(6)
    assert phi6.coeffs == (Fraction(1), Fraction(-1), Fraction(1))


def test_euclidean_gcd():
    # gcd(x^2 - 1, x^2 - 2x + 1) = x - 1
    p1 = ExactPolynomial.from_ints(-1, 0, 1)      # x^2 - 1
    p2 = ExactPolynomial.from_ints(1, -2, 1)      # (x - 1)^2
    g = p1.gcd(p2)
    assert g.coeffs == (Fraction(-1), Fraction(1)) # x - 1


def test_quadratic_field_norm_and_trace():
    # alpha = 3 + 2 sqrt(5) in Q(sqrt(5))
    alpha = QuadraticExtension(Fraction(3), Fraction(2), 5)
    assert alpha.trace() == Fraction(6)
    # norm = 3^2 - 5*(2^2) = 9 - 20 = -11
    assert alpha.norm() == Fraction(-11)

    # Conjugate alpha_bar = 3 - 2 sqrt(5)
    alpha_bar = QuadraticExtension(Fraction(3), Fraction(-2), 5)
    prod = alpha * alpha_bar
    assert prod.b == Fraction(0)
    assert prod.a == Fraction(-11)
