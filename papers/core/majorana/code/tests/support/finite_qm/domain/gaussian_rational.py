"""Exact Gaussian rational arithmetic for the finite channel checker.

AuthorityEffect: None. Floating inputs retain their exact binary values.
"""
from dataclasses import dataclass
from fractions import Fraction
import numbers

@dataclass(frozen=True, eq=False)
class Gaussian:
    real: Fraction = Fraction(0)
    imag: Fraction = Fraction(0)

    @staticmethod
    def of(value):
        if isinstance(value, Gaussian): return value
        if isinstance(value, numbers.Complex) and not isinstance(value, numbers.Real):
            return Gaussian(Fraction(float(value.real)), Fraction(float(value.imag)))
        return Gaussian(Fraction(value), Fraction(0))

    def __add__(self, other):
        other=self.of(other)
        return Gaussian(self.real+other.real,self.imag+other.imag)
    __radd__=__add__

    def __neg__(self): return Gaussian(-self.real,-self.imag)
    def __sub__(self, other): return self + -self.of(other)
    def __rsub__(self, other): return self.of(other) + -self

    def __mul__(self, other):
        other=self.of(other)
        return Gaussian(self.real*other.real-self.imag*other.imag,
                        self.real*other.imag+self.imag*other.real)
    __rmul__=__mul__

    def conjugate(self): return Gaussian(self.real,-self.imag)
    def __truediv__(self, other):
        other=self.of(other)
        norm=other.real*other.real+other.imag*other.imag
        if norm==0: raise ZeroDivisionError('zero Gaussian rational')
        value=self*other.conjugate()
        return Gaussian(value.real/norm,value.imag/norm)
    def __rtruediv__(self, other): return self.of(other)/self

    def __eq__(self, other):
        try: other=self.of(other)
        except (ValueError,TypeError): return False
        return self.real==other.real and self.imag==other.imag
    def __getitem__(self, idx: int) -> Fraction:
        if idx == 0: return self.real
        if idx == 1: return self.imag
        raise IndexError(f"Gaussian index out of range: {idx}")
    def __bool__(self): return bool(self.real or self.imag)
    def __complex__(self): return complex(float(self.real),float(self.imag))
    def __float__(self):
        if self.imag: raise ValueError('non-real determinant')
        return float(self.real)

__all__ = ['Gaussian']
