"""Exact rational number theory, polynomials in Q[x], cyclotomics, and quadratic fields.

AuthorityEffect: None.
"""

from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction
from typing import Dict, List, Optional, Tuple


class NumberTheoryError(Exception):
    pass


@dataclass(frozen=True)
class ExactPolynomial:
    """Univariate polynomial over Q: P(x) = c_0 + c_1 x + ... + c_d x^d."""
    coeffs: Tuple[Fraction, ...]  # lowest to highest degree

    @classmethod
    def from_ints(cls, *ints: int) -> ExactPolynomial:
        return cls(tuple(Fraction(i) for i in ints)).canonical()

    @classmethod
    def zero(cls) -> ExactPolynomial:
        return cls(())

    @classmethod
    def one(cls) -> ExactPolynomial:
        return cls((Fraction(1),))

    @classmethod
    def x(cls) -> ExactPolynomial:
        return cls((Fraction(0), Fraction(1)))

    def canonical(self) -> ExactPolynomial:
        """Strip trailing zeros."""
        c = list(self.coeffs)
        while c and c[-1] == 0:
            c.pop()
        return ExactPolynomial(tuple(c))

    @property
    def degree(self) -> int:
        c = self.canonical()
        if not c.coeffs:
            return -1
        return len(c.coeffs) - 1

    def is_zero(self) -> bool:
        return self.degree < 0

    def leading_coeff(self) -> Fraction:
        c = self.canonical()
        if not c.coeffs:
            return Fraction(0)
        return c.coeffs[-1]

    def __add__(self, other: ExactPolynomial) -> ExactPolynomial:
        deg = max(len(self.coeffs), len(other.coeffs))
        res = [Fraction(0)] * deg
        for i in range(deg):
            c1 = self.coeffs[i] if i < len(self.coeffs) else Fraction(0)
            c2 = other.coeffs[i] if i < len(other.coeffs) else Fraction(0)
            res[i] = c1 + c2
        return ExactPolynomial(tuple(res)).canonical()

    def __sub__(self, other: ExactPolynomial) -> ExactPolynomial:
        deg = max(len(self.coeffs), len(other.coeffs))
        res = [Fraction(0)] * deg
        for i in range(deg):
            c1 = self.coeffs[i] if i < len(self.coeffs) else Fraction(0)
            c2 = other.coeffs[i] if i < len(other.coeffs) else Fraction(0)
            res[i] = c1 - c2
        return ExactPolynomial(tuple(res)).canonical()

    def __mul__(self, other: ExactPolynomial) -> ExactPolynomial:
        if self.is_zero() or other.is_zero():
            return ExactPolynomial.zero()
        deg = len(self.coeffs) + len(other.coeffs) - 1
        res = [Fraction(0)] * deg
        for i, c1 in enumerate(self.coeffs):
            for j, c2 in enumerate(other.coeffs):
                res[i + j] += c1 * c2
        return ExactPolynomial(tuple(res)).canonical()

    def divmod(self, divisor: ExactPolynomial) -> Tuple[ExactPolynomial, ExactPolynomial]:
        """Exact polynomial division with remainder: self = quotient * divisor + remainder."""
        if divisor.is_zero():
            raise ZeroDivisionError("Polynomial division by zero")
        if self.degree < divisor.degree:
            return ExactPolynomial.zero(), self.canonical()

        remainder = list(self.canonical().coeffs)
        quotient = [Fraction(0)] * (self.degree - divisor.degree + 1)
        d_deg = divisor.degree
        d_lead = divisor.leading_coeff()

        while len(remainder) - 1 >= d_deg:
            cur_deg = len(remainder) - 1
            lead = remainder[-1]
            scale = lead / d_lead
            shift = cur_deg - d_deg
            quotient[shift] = scale

            for i, c in enumerate(divisor.canonical().coeffs):
                remainder[shift + i] -= scale * c

            while remainder and remainder[-1] == 0:
                remainder.pop()

        return ExactPolynomial(tuple(quotient)).canonical(), ExactPolynomial(tuple(remainder)).canonical()

    def make_monic(self) -> ExactPolynomial:
        lead = self.leading_coeff()
        if lead == 0:
            return self
        return ExactPolynomial(tuple(c / lead for c in self.coeffs)).canonical()

    def gcd(self, other: ExactPolynomial) -> ExactPolynomial:
        """Monic GCD in Q[x] via Euclidean algorithm."""
        a = self.canonical()
        b = other.canonical()
        while not b.is_zero():
            _, rem = a.divmod(b)
            a, b = b, rem
        return a.make_monic()

    @classmethod
    def cyclotomic(cls, n: int) -> ExactPolynomial:
        """Compute the n-th cyclotomic polynomial Phi_n(x)."""
        if n < 1:
            raise ValueError("n must be >= 1")
        # x^n - 1
        xn_minus_1_coeffs = [-Fraction(1)] + [Fraction(0)] * (n - 1) + [Fraction(1)]
        f = ExactPolynomial(tuple(xn_minus_1_coeffs))
        for d in range(1, n):
            if n % d == 0:
                phi_d = cls.cyclotomic(d)
                f, rem = f.divmod(phi_d)
                assert rem.is_zero()
        return f.make_monic()


@dataclass(frozen=True)
class QuadraticExtension:
    """Element of Q(sqrt(d)): a + b*sqrt(d) with square-free integer d."""
    a: Fraction
    b: Fraction
    d: int

    def __add__(self, other: QuadraticExtension) -> QuadraticExtension:
        assert self.d == other.d
        return QuadraticExtension(self.a + other.a, self.b + other.b, self.d)

    def __mul__(self, other: QuadraticExtension) -> QuadraticExtension:
        assert self.d == other.d
        return QuadraticExtension(
            self.a * other.a + self.b * other.b * self.d,
            self.a * other.b + self.b * other.a,
            self.d,
        )

    def trace(self) -> Fraction:
        return self.a * 2

    def norm(self) -> Fraction:
        return self.a * self.a - self.b * self.b * self.d
