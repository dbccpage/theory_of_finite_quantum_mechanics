"""Exact Gaussian rational arithmetic for the finite channel checker.

AuthorityEffect: None. Floating inputs retain their exact binary values.
"""
from __future__ import annotations

import numbers
from dataclasses import dataclass
from fractions import Fraction


@dataclass(frozen=True, eq=False)
class Gaussian:
    real: Fraction = Fraction(0)
    imag: Fraction = Fraction(0)

    @staticmethod
    def of(value: object) -> Gaussian:
        if isinstance(value, Gaussian):
            return value
        if isinstance(value, numbers.Complex) and not isinstance(value, numbers.Real):
            return Gaussian(Fraction(float(value.real)), Fraction(float(value.imag)))
        if isinstance(value, (int, str, Fraction)):
            return Gaussian(Fraction(value), Fraction(0))
        if isinstance(value, (float, numbers.Real)):
            return Gaussian(Fraction(float(value)), Fraction(0))
        return Gaussian(Fraction(str(value)), Fraction(0))

    def __add__(self, other: object) -> Gaussian:
        other_g = self.of(other)
        return Gaussian(self.real + other_g.real, self.imag + other_g.imag)

    __radd__ = __add__

    def __neg__(self) -> Gaussian:
        return Gaussian(-self.real, -self.imag)

    def __sub__(self, other: object) -> Gaussian:
        return self + -self.of(other)

    def __rsub__(self, other: object) -> Gaussian:
        return self.of(other) + -self

    def __mul__(self, other: object) -> Gaussian:
        other_g = self.of(other)
        return Gaussian(
            self.real * other_g.real - self.imag * other_g.imag,
            self.real * other_g.imag + self.imag * other_g.real,
        )

    __rmul__ = __mul__

    def conjugate(self) -> Gaussian:
        return Gaussian(self.real, -self.imag)

    def __truediv__(self, other: object) -> Gaussian:
        other_g = self.of(other)
        norm = other_g.real * other_g.real + other_g.imag * other_g.imag
        if norm == 0:
            raise ZeroDivisionError("zero Gaussian rational")
        value = self * other_g.conjugate()
        return Gaussian(value.real / norm, value.imag / norm)

    def __rtruediv__(self, other: object) -> Gaussian:
        return self.of(other) / self

    def __eq__(self, other: object) -> bool:
        try:
            other_g = self.of(other)
        except (ValueError, TypeError):
            return False
        return self.real == other_g.real and self.imag == other_g.imag

    def __getitem__(self, idx: int) -> Fraction:
        if idx == 0:
            return self.real
        if idx == 1:
            return self.imag
        raise IndexError(f"Gaussian index out of range: {idx}")

    def __bool__(self) -> bool:
        return bool(self.real or self.imag)

    def __complex__(self) -> complex:
        return complex(float(self.real), float(self.imag))

    def __float__(self) -> float:
        if self.imag:
            raise ValueError("non-real determinant")
        return float(self.real)


__all__ = ["Gaussian"]
