"""Exact rational and Gaussian rational scalar fields with SHA-256 hash witnesses."""
from fractions import Fraction
import hashlib
from typing import Union

class GaussianRational:
    __slots__ = ("real", "imag")

    def __init__(self, real: Union[int, Fraction, "GaussianRational"], imag: Union[int, Fraction] = 0):
        if isinstance(real, GaussianRational):
            self.real = real.real
            self.imag = real.imag
        else:
            self.real = Fraction(real)
            self.imag = Fraction(imag)

    @staticmethod
    def zero() -> "GaussianRational":
        return GaussianRational(0, 0)

    @staticmethod
    def one() -> "GaussianRational":
        return GaussianRational(1, 0)

    @staticmethod
    def i() -> "GaussianRational":
        return GaussianRational(0, 1)

    def is_zero(self) -> bool:
        return self.real == 0 and self.imag == 0

    def conjugate(self) -> "GaussianRational":
        return GaussianRational(self.real, -self.imag)

    def norm_sq(self) -> Fraction:
        return self.real * self.real + self.imag * self.imag

    def __add__(self, other: Union["GaussianRational", Fraction, int]) -> "GaussianRational":
        if isinstance(other, GaussianRational):
            return GaussianRational(self.real + other.real, self.imag + other.imag)
        return GaussianRational(self.real + Fraction(other), self.imag)

    def __radd__(self, other: Union[Fraction, int]) -> "GaussianRational":
        return self.__add__(other)

    def __sub__(self, other: Union["GaussianRational", Fraction, int]) -> "GaussianRational":
        if isinstance(other, GaussianRational):
            return GaussianRational(self.real - other.real, self.imag - other.imag)
        return GaussianRational(self.real - Fraction(other), self.imag)

    def __rsub__(self, other: Union[Fraction, int]) -> "GaussianRational":
        return GaussianRational(Fraction(other) - self.real, -self.imag)

    def __mul__(self, other: Union["GaussianRational", Fraction, int]) -> "GaussianRational":
        if isinstance(other, GaussianRational):
            return GaussianRational(
                self.real * other.real - self.imag * other.imag,
                self.real * other.imag + self.imag * other.real
            )
        f = Fraction(other)
        return GaussianRational(self.real * f, self.imag * f)

    def __rmul__(self, other: Union[Fraction, int]) -> "GaussianRational":
        return self.__mul__(other)

    def __truediv__(self, other: Union["GaussianRational", Fraction, int]) -> "GaussianRational":
        if isinstance(other, GaussianRational):
            denom = other.norm_sq()
            if denom == 0:
                raise ZeroDivisionError("Division by zero in Gaussian rational field")
            num = self * other.conjugate()
            return GaussianRational(num.real / denom, num.imag / denom)
        f = Fraction(other)
        if f == 0:
            raise ZeroDivisionError("Division by zero in rational field")
        return GaussianRational(self.real / f, self.imag / f)

    def __neg__(self) -> "GaussianRational":
        return GaussianRational(-self.real, -self.imag)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, GaussianRational):
            return self.real == other.real and self.imag == other.imag
        if isinstance(other, (int, Fraction)):
            return self.imag == 0 and self.real == other
        return False

    def __hash__(self) -> int:
        return hash((self.real, self.imag))

    def __repr__(self) -> str:
        if self.imag == 0:
            return f"{self.real}"
        if self.real == 0:
            return f"{self.imag}i"
        sign = "+" if self.imag > 0 else "-"
        return f"({self.real} {sign} {abs(self.imag)}i)"

    def canonical_bytes(self) -> bytes:
        return f"{self.real.numerator}/{self.real.denominator}+{self.imag.numerator}/{self.imag.denominator}i".encode("utf-8")

    def sha256(self) -> str:
        return hashlib.sha256(self.canonical_bytes()).hexdigest()

def q(n: int, d: int = 1) -> Fraction:
    return Fraction(n, d)

Q = Fraction
