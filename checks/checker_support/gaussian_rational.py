"""Gaussian-rational value object for the independent-checking bounded context."""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction
from .domains import rational
from .boundary import Violation


@dataclass(frozen=True, slots=True, init=False)
class GaussianRational:
    """Invariant: both components are immutable exact Fractions; floats/bools are refused."""

    re: Fraction
    im: Fraction

    def __init__(self, re: object, im: object = 0) -> None:
        object.__setattr__(self, "re", rational(re, "real component"))
        object.__setattr__(self, "im", rational(im, "imaginary component"))

    def __add__(self, other: GaussianRational) -> GaussianRational:
        self._admit_other(other)
        return GaussianRational(self.re + other.re, self.im + other.im)

    def __sub__(self, other: GaussianRational) -> GaussianRational:
        self._admit_other(other)
        return GaussianRational(self.re - other.re, self.im - other.im)

    def __mul__(self, other: GaussianRational) -> GaussianRational:
        self._admit_other(other)
        return GaussianRational(self.re*other.re - self.im*other.im,
                                self.re*other.im + self.im*other.re)

    def mul(self, other: GaussianRational) -> GaussianRational:
        return self * other

    def conj(self) -> GaussianRational:
        return GaussianRational(self.re, -self.im)

    def norm_sq(self) -> Fraction:
        return self.re*self.re + self.im*self.im

    def inv(self) -> GaussianRational:
        norm = self.norm_sq()
        if norm == 0:
            raise Violation("input", "zero Gaussian rational has no inverse")
        return GaussianRational(self.re/norm, -self.im/norm)

    def div(self, other: GaussianRational) -> GaussianRational:
        self._admit_other(other)
        return self * other.inv()

    @staticmethod
    def _admit_other(other: object) -> None:
        if type(other) is not GaussianRational:
            raise Violation("input", "Gaussian arithmetic requires a GaussianRational operand")
