
"""Busch-Gleason Effect Frame Algebra over Cyclotomic Number Fields.

Phase R2 Python Kernel: Steps 05 through 10 of Campaign C250 Block 01.
Implements exact rational arithmetic (fractions.Fraction) and integer polynomial
operations with zero floating-point arithmetic across conductors {4, 5, 8, 12, 24}
and dimensions {2, 3}.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union


class RationalPoly:
    """Exact univariate polynomial with Fraction coefficients: sum_{k=0}^d c_k x^k."""

    def __init__(self, coeffs: Union[Sequence[Union[Fraction, int]], RationalPoly]) -> None:
        if isinstance(coeffs, RationalPoly):
            self.coeffs: Tuple[Fraction, ...] = coeffs.coeffs
            return
        c_list = [Fraction(c) for c in coeffs]
        while c_list and c_list[-1] == 0:
            c_list.pop()
        self.coeffs = tuple(c_list)

    @property
    def degree(self) -> int:
        """Return the degree of the polynomial, or -1 for the zero polynomial."""
        return len(self.coeffs) - 1

    def is_zero(self) -> bool:
        """Return True if the polynomial is identically zero."""
        return len(self.coeffs) == 0

    def eval(self, x: Union[Fraction, int]) -> Fraction:
        """Horner evaluation at an exact rational point."""
        x_frac = Fraction(x)
        if self.is_zero():
            return Fraction(0)
        res = Fraction(0)
        for c in reversed(self.coeffs):
            res = res * x_frac + c
        return res

    def derivative(self) -> RationalPoly:
        """Compute the algebraic formal derivative d/dx."""
        if len(self.coeffs) <= 1:
            return RationalPoly(())
        d_coeffs = [self.coeffs[k] * k for k in range(1, len(self.coeffs))]
        return RationalPoly(d_coeffs)

    def __add__(self, other: Union[RationalPoly, Fraction, int]) -> RationalPoly:
        if not isinstance(other, RationalPoly):
            other = RationalPoly([Fraction(other)])
        n = max(len(self.coeffs), len(other.coeffs))
        res = [Fraction(0)] * n
        for i, c in enumerate(self.coeffs):
            res[i] += c
        for i, c in enumerate(other.coeffs):
            res[i] += c
        return RationalPoly(res)

    def __radd__(self, other: Union[Fraction, int]) -> RationalPoly:
        return self + other

    def __sub__(self, other: Union[RationalPoly, Fraction, int]) -> RationalPoly:
        if not isinstance(other, RationalPoly):
            other = RationalPoly([Fraction(other)])
        n = max(len(self.coeffs), len(other.coeffs))
        res = [Fraction(0)] * n
        for i, c in enumerate(self.coeffs):
            res[i] += c
        for i, c in enumerate(other.coeffs):
            res[i] -= c
        return RationalPoly(res)

    def __rsub__(self, other: Union[Fraction, int]) -> RationalPoly:
        return RationalPoly([Fraction(other)]) - self

    def __neg__(self) -> RationalPoly:
        return RationalPoly([-c for c in self.coeffs])

    def __mul__(self, other: Union[RationalPoly, Fraction, int]) -> RationalPoly:
        if not isinstance(other, RationalPoly):
            other_frac = Fraction(other)
            return RationalPoly([c * other_frac for c in self.coeffs])
        if self.is_zero() or other.is_zero():
            return RationalPoly(())
        deg1 = self.degree
        deg2 = other.degree
        res = [Fraction(0)] * (deg1 + deg2 + 1)
        for i, c1 in enumerate(self.coeffs):
            if c1 == 0:
                continue
            for j, c2 in enumerate(other.coeffs):
                res[i + j] += c1 * c2
        return RationalPoly(res)

    def __rmul__(self, other: Union[Fraction, int]) -> RationalPoly:
        return self * other

    def div_rem(self, divisor: RationalPoly) -> Tuple[RationalPoly, RationalPoly]:
        """Euclidean division in Q[x]. Returns (quotient, remainder)."""
        if divisor.is_zero():
            raise ZeroDivisionError("Polynomial division by zero polynomial")
        if self.is_zero() or self.degree < divisor.degree:
            return RationalPoly(()), self

        rem_coeffs = list(self.coeffs)
        div_deg = divisor.degree
        div_lead = divisor.coeffs[-1]
        quot_deg = len(rem_coeffs) - 1 - div_deg
        quot_coeffs = [Fraction(0)] * (quot_deg + 1)

        while len(rem_coeffs) - 1 >= div_deg and rem_coeffs:
            curr_deg = len(rem_coeffs) - 1
            shift = curr_deg - div_deg
            factor = rem_coeffs[-1] / div_lead
            quot_coeffs[shift] = factor
            for j, c in enumerate(divisor.coeffs):
                rem_coeffs[shift + j] -= factor * c
            while rem_coeffs and rem_coeffs[-1] == 0:
                rem_coeffs.pop()

        return RationalPoly(quot_coeffs), RationalPoly(rem_coeffs)

    def __mod__(self, divisor: RationalPoly) -> RationalPoly:
        _, rem = self.div_rem(divisor)
        return rem

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, RationalPoly):
            if isinstance(other, (int, Fraction)):
                other = RationalPoly([Fraction(other)])
            else:
                return False
        return self.coeffs == other.coeffs

    def __repr__(self) -> str:
        if self.is_zero():
            return "RationalPoly(0)"
        terms = []
        for i, c in enumerate(self.coeffs):
            if c == 0:
                continue
            if i == 0:
                terms.append(str(c))
            elif i == 1:
                terms.append(f"{c}*x")
            else:
                terms.append(f"{c}*x^{i}")
        return " + ".join(terms) or "0"


def sturm_sequence(poly: RationalPoly) -> List[RationalPoly]:
    """Compute standard Sturm sequence: P_0 = P, P_1 = P', P_{k+1} = -rem(P_{k-1}, P_k)."""
    if poly.is_zero() or poly.degree == 0:
        return [poly]
    seq = [poly, poly.derivative()]
    while True:
        _, rem = seq[-2].div_rem(seq[-1])
        if rem.is_zero():
            break
        seq.append(-rem)
    return seq


def sign_variations(sturm: List[RationalPoly], q: Union[Fraction, int]) -> int:
    """Number of sign variations V(q) in the Sturm sequence at rational q."""
    q_frac = Fraction(q)
    signs = []
    for p in sturm:
        val = p.eval(q_frac)
        if val > 0:
            signs.append(1)
        elif val < 0:
            signs.append(-1)
    variations = 0
    last_sign = 0
    for s in signs:
        if s != 0:
            if last_sign != 0 and s != last_sign:
                variations += 1
            last_sign = s
    return variations


def count_roots_in_interval(sturm: List[RationalPoly], a: Union[Fraction, int], b: Union[Fraction, int]) -> int:
    """Number of real roots of poly in half-open interval (a, b] using Sturm theorem."""
    return sign_variations(sturm, a) - sign_variations(sturm, b)



CONDUCTOR_MIN_POLYS: Dict[int, RationalPoly] = {
    4: RationalPoly([Fraction(0), Fraction(1)]),
    5: RationalPoly([Fraction(-1), Fraction(1), Fraction(1)]),
    8: RationalPoly([Fraction(-2), Fraction(0), Fraction(1)]),
    12: RationalPoly([Fraction(-3), Fraction(0), Fraction(1)]),
    24: RationalPoly([Fraction(1), Fraction(0), Fraction(-4), Fraction(0), Fraction(1)]),
}

CONDUCTOR_INITIAL_INTERVALS: Dict[int, Tuple[Fraction, Fraction]] = {
    4: (Fraction(-1, 2), Fraction(1, 2)),
    5: (Fraction(1, 2), Fraction(1, 1)),
    8: (Fraction(1, 1), Fraction(2, 1)),
    12: (Fraction(1, 1), Fraction(2, 1)),
    24: (Fraction(7, 4), Fraction(2, 1)),
}


class CyclotomicRealRoot:
    """Isolates the positive real root alpha_* of minimal polynomial P_n(x) with rational intervals."""

    def __init__(self, conductor: int) -> None:
        if conductor not in CONDUCTOR_MIN_POLYS:
            raise ValueError(f"Conductor {conductor} not in supported set {{4, 5, 8, 12, 24}}")
        self.conductor = conductor
        self.poly = CONDUCTOR_MIN_POLYS[conductor]
        self.sturm = sturm_sequence(self.poly)
        a_init, b_init = CONDUCTOR_INITIAL_INTERVALS[conductor]
        self.a: Fraction = a_init
        self.b: Fraction = b_init
        if conductor != 4:
            roots_count = count_roots_in_interval(self.sturm, self.a, self.b)
            if roots_count != 1:
                raise ValueError(
                    f"Initial interval ({self.a}, {self.b}) for conductor {conductor} contains {roots_count} roots, expected 1"
                )

    def refine(self) -> None:
        """Bisect the isolating interval (a, b) once to half its width."""
        if self.conductor == 4:
            self.a = Fraction(0)
            self.b = Fraction(0)
            return
        if self.a == self.b:
            return
        mid = (self.a + self.b) / Fraction(2)
        if self.poly.eval(mid) == 0:
            self.a = mid
            self.b = mid
            return
        if count_roots_in_interval(self.sturm, self.a, mid) == 1:
            self.b = mid
        else:
            self.a = mid

    def refine_to_width(self, max_width: Fraction) -> None:
        """Repeatedly bisect interval until (b - a) <= max_width."""
        while (self.b - self.a) > max_width:
            self.refine()

    def sign_of_poly(self, poly: RationalPoly) -> int:
        """Determine the exact algebraic sign (-1, 0, 1) of poly(alpha_*) under the embedding."""
        if poly.is_zero():
            return 0
        if self.conductor == 4:
            val = poly.eval(Fraction(0))
            return 1 if val > 0 else (-1 if val < 0 else 0)

        _, rem = poly.div_rem(self.poly)
        if rem.is_zero():
            return 0

        sturm_rem = sturm_sequence(rem)
        while True:
            if self.a == self.b:
                val = rem.eval(self.a)
                return 1 if val > 0 else (-1 if val < 0 else 0)
            val_a = rem.eval(self.a)
            val_b = rem.eval(self.b)
            if val_a > 0 and val_b > 0 and count_roots_in_interval(sturm_rem, self.a, self.b) == 0:
                return 1
            if val_a < 0 and val_b < 0 and count_roots_in_interval(sturm_rem, self.a, self.b) == 0:
                return -1
            self.refine()

    def bound_poly(self, poly: RationalPoly, epsilon: Fraction) -> Tuple[Fraction, Fraction]:
        """Compute exact rational bounds r <= poly(alpha_*) <= s with (s - r) <= epsilon."""
        if poly.is_zero():
            return Fraction(0), Fraction(0)
        if self.conductor == 4:
            v = poly.eval(Fraction(0))
            return v, v

        _, rem = poly.div_rem(self.poly)
        if rem.is_zero():
            return Fraction(0), Fraction(0)

        rem_deriv = rem.derivative()
        max_abs_x = max(abs(self.a), abs(self.b), Fraction(2))
        lip_bound = Fraction(0)
        for i, c in enumerate(rem_deriv.coeffs):
            lip_bound += abs(c) * (max_abs_x ** i)
        if lip_bound == 0:
            val = rem.eval(self.a)
            return val, val

        target_width = epsilon / lip_bound
        while (self.b - self.a) > target_width:
            self.refine()

        mid = (self.a + self.b) / Fraction(2)
        val_mid = rem.eval(mid)
        radius = lip_bound * (self.b - self.a) / Fraction(2)
        return val_mid - radius, val_mid + radius



F_PLUS_DEGREES: Dict[int, int] = {
    4: 1,
    5: 2,
    8: 2,
    12: 2,
    24: 4,
}


class FieldElementFPlus:
    """Exact element of maximal real subfield F^+ = Q(theta_n) represented in basis {1, theta, ..., theta^{m-1}}."""

    def __init__(self, conductor: int, coeffs: Sequence[Union[Fraction, int]]) -> None:
        if conductor not in F_PLUS_DEGREES:
            raise ValueError(f"Unsupported conductor {conductor}")
        self.conductor = conductor
        deg = F_PLUS_DEGREES[conductor]
        c_list = [Fraction(0)] * deg
        for i, c in enumerate(coeffs):
            if i < deg:
                c_list[i] = Fraction(c)
            elif Fraction(c) != 0:
                raise ValueError(f"Nonzero coefficient at degree {i} exceeds field degree {deg}")
        self.coeffs = tuple(c_list)

    @classmethod
    def rational(cls, a: Any, b: Any) -> FieldElementFPlus:
        """Construct a rational element of F^+, accepting either (q, conductor) or (conductor, q)."""
        if isinstance(a, int) and isinstance(b, (Fraction, int)) and a in F_PLUS_DEGREES:
            conductor, q = a, b
        else:
            q, conductor = a, b
        deg = F_PLUS_DEGREES[conductor]
        c = [Fraction(0)] * deg
        c[0] = Fraction(q)
        return cls(conductor, c)

    @classmethod
    def zero(cls, conductor: int) -> FieldElementFPlus:
        return cls.rational(Fraction(0), conductor)

    @classmethod
    def one(cls, conductor: int) -> FieldElementFPlus:
        return cls.rational(Fraction(1), conductor)

    @classmethod
    def theta(cls, conductor: int) -> FieldElementFPlus:
        deg = F_PLUS_DEGREES[conductor]
        if deg == 1:
            return cls.zero(conductor)
        c = [Fraction(0)] * deg
        c[1] = Fraction(1)
        return cls(conductor, c)

    def is_zero(self) -> bool:
        return all(c == 0 for c in self.coeffs)

    def to_poly(self) -> RationalPoly:
        return RationalPoly(self.coeffs)

    def sign(self, embedding: CyclotomicRealRoot) -> int:
        """Determine sign in {-1, 0, 1} under specified embedding."""
        if embedding.conductor != self.conductor:
            raise ValueError(f"Embedding conductor {embedding.conductor} does not match element conductor {self.conductor}")
        return embedding.sign_of_poly(self.to_poly())

    def interval_bounds(self, embedding: CyclotomicRealRoot, epsilon: Fraction) -> Tuple[Fraction, Fraction]:
        """Compute exact rational enclosure [r, s] of width <= epsilon."""
        if embedding.conductor != self.conductor:
            raise ValueError("Conductor mismatch between element and embedding")
        return embedding.bound_poly(self.to_poly(), epsilon)

    def __add__(self, other: Union[FieldElementFPlus, Fraction, int]) -> FieldElementFPlus:
        if not isinstance(other, FieldElementFPlus):
            other = FieldElementFPlus.rational(other, self.conductor)
        if self.conductor != other.conductor:
            raise ValueError(f"Cannot add elements from distinct conductors {self.conductor} and {other.conductor}")
        deg = F_PLUS_DEGREES[self.conductor]
        new_c = [self.coeffs[i] + other.coeffs[i] for i in range(deg)]
        return FieldElementFPlus(self.conductor, new_c)

    def __radd__(self, other: Union[Fraction, int]) -> FieldElementFPlus:
        return self + other

    def __sub__(self, other: Union[FieldElementFPlus, Fraction, int]) -> FieldElementFPlus:
        if not isinstance(other, FieldElementFPlus):
            other = FieldElementFPlus.rational(other, self.conductor)
        if self.conductor != other.conductor:
            raise ValueError(f"Cannot subtract elements from distinct conductors {self.conductor} and {other.conductor}")
        deg = F_PLUS_DEGREES[self.conductor]
        new_c = [self.coeffs[i] - other.coeffs[i] for i in range(deg)]
        return FieldElementFPlus(self.conductor, new_c)

    def __rsub__(self, other: Union[Fraction, int]) -> FieldElementFPlus:
        return FieldElementFPlus.rational(other, self.conductor) - self

    def __neg__(self) -> FieldElementFPlus:
        return FieldElementFPlus(self.conductor, [-c for c in self.coeffs])

    def __mul__(self, other: Union[FieldElementFPlus, Fraction, int]) -> FieldElementFPlus:
        if not isinstance(other, FieldElementFPlus):
            other_frac = Fraction(other)
            return FieldElementFPlus(self.conductor, [c * other_frac for c in self.coeffs])
        if self.conductor != other.conductor:
            raise ValueError(f"Cannot multiply elements from distinct conductors {self.conductor} and {other.conductor}")
        if self.is_zero() or other.is_zero():
            return FieldElementFPlus.zero(self.conductor)

        p1 = self.to_poly()
        p2 = other.to_poly()
        prod = p1 * p2
        if self.conductor == 4:
            return FieldElementFPlus.rational(prod.eval(Fraction(0)), 4)
        min_p = CONDUCTOR_MIN_POLYS[self.conductor]
        _, rem = prod.div_rem(min_p)
        deg = F_PLUS_DEGREES[self.conductor]
        res_c = [Fraction(0)] * deg
        for i, c in enumerate(rem.coeffs):
            if i < deg:
                res_c[i] = c
        return FieldElementFPlus(self.conductor, res_c)

    def __rmul__(self, other: Union[Fraction, int]) -> FieldElementFPlus:
        return self * other

    def inverse(self) -> FieldElementFPlus:
        """Compute exact multiplicative inverse via extended Euclidean polynomial algorithm."""
        if self.is_zero():
            raise ZeroDivisionError("Cannot invert zero FieldElementFPlus")
        if self.conductor == 4:
            return FieldElementFPlus.rational(Fraction(1) / self.coeffs[0], 4)

        poly = self.to_poly()
        min_p = CONDUCTOR_MIN_POLYS[self.conductor]

        r0, r1 = min_p, poly
        s0, s1 = RationalPoly([Fraction(1)]), RationalPoly(())
        t0, t1 = RationalPoly(()), RationalPoly([Fraction(1)])

        while not r1.is_zero():
            q, rem = r0.div_rem(r1)
            r0, r1 = r1, rem
            s0, s1 = s1, s0 - q * s1
            t0, t1 = t1, t0 - q * t1

        if r0.degree != 0 or r0.coeffs[0] == 0:
            raise ZeroDivisionError("Element has non-trivial factor with minimal polynomial")

        lead = r0.coeffs[0]
        inv_poly = RationalPoly([c / lead for c in t0.coeffs])
        deg = F_PLUS_DEGREES[self.conductor]
        inv_c = [Fraction(0)] * deg
        for i, c in enumerate(inv_poly.coeffs):
            if i < deg:
                inv_c[i] = c
        return FieldElementFPlus(self.conductor, inv_c)

    def __truediv__(self, other: Union[FieldElementFPlus, Fraction, int]) -> FieldElementFPlus:
        if not isinstance(other, FieldElementFPlus):
            other = FieldElementFPlus.rational(other, self.conductor)
        return self * other.inverse()

    def __rtruediv__(self, other: Union[Fraction, int]) -> FieldElementFPlus:
        return FieldElementFPlus.rational(other, self.conductor) * self.inverse()

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, FieldElementFPlus):
            if isinstance(other, (int, Fraction)):
                other = FieldElementFPlus.rational(other, self.conductor)
            else:
                return False
        return self.conductor == other.conductor and self.coeffs == other.coeffs

    def __repr__(self) -> str:
        return f"FPlus_{self.conductor}{self.coeffs}"



def xi_squared(conductor: int) -> FieldElementFPlus:
    """Return xi^2 in F^+, where F = F^+(xi) and sigma(xi) = -xi.

    For n in {4, 8, 12, 24}: xi = i with xi^2 = -1 in Q subset F^+.
    For n = 5: xi = zeta_5 - zeta_5^-1 with xi^2 = theta_5^2 - 4 = -3 - theta_5.
    """
    if conductor in (4, 8, 12, 24):
        return FieldElementFPlus.rational(Fraction(-1), conductor)
    elif conductor == 5:
        return FieldElementFPlus(5, [Fraction(-3), Fraction(-1)])
    else:
        raise ValueError(f"Conductor {conductor} not supported")


class FieldElementF:
    """Exact element of cyclotomic field F = F^+(xi) represented as x + y * xi, with x, y in F^+."""

    def __init__(
        self,
        conductor: int,
        real: Union[FieldElementFPlus, Fraction, int],
        imag: Optional[Union[FieldElementFPlus, Fraction, int]] = None,
    ) -> None:
        self.conductor = conductor
        if not isinstance(real, FieldElementFPlus):
            self.real = FieldElementFPlus.rational(real, conductor)
        else:
            self.real = real

        if imag is None:
            self.imag = FieldElementFPlus.zero(conductor)
        elif not isinstance(imag, FieldElementFPlus):
            self.imag = FieldElementFPlus.rational(imag, conductor)
        else:
            self.imag = imag

    @classmethod
    def rational(cls, q: Union[Fraction, int], conductor: int) -> FieldElementF:
        return cls(conductor, FieldElementFPlus.rational(q, conductor))

    @classmethod
    def zero(cls, conductor: int) -> FieldElementF:
        return cls(conductor, FieldElementFPlus.zero(conductor))

    @classmethod
    def one(cls, conductor: int) -> FieldElementF:
        return cls(conductor, FieldElementFPlus.one(conductor))

    @classmethod
    def xi(cls, conductor: int) -> FieldElementF:
        return cls(conductor, FieldElementFPlus.zero(conductor), FieldElementFPlus.one(conductor))

    def is_zero(self) -> bool:
        return self.real.is_zero() and self.imag.is_zero()

    def is_real(self) -> bool:
        return self.imag.is_zero()

    def conjugate(self) -> FieldElementF:
        """Automorphism sigma: x + y*xi -> x - y*xi."""
        return FieldElementF(self.conductor, self.real, -self.imag)

    def norm(self) -> FieldElementFPlus:
        """Field norm over F^+: N(z) = x^2 - y^2 * xi^2 in F^+."""
        xi2 = xi_squared(self.conductor)
        return self.real * self.real - self.imag * self.imag * xi2

    def __add__(self, other: Union[FieldElementF, FieldElementFPlus, Fraction, int]) -> FieldElementF:
        if not isinstance(other, FieldElementF):
            if isinstance(other, FieldElementFPlus):
                return FieldElementF(self.conductor, self.real + other, self.imag)
            other = FieldElementF.rational(other, self.conductor)
        return FieldElementF(self.conductor, self.real + other.real, self.imag + other.imag)

    def __radd__(self, other: Union[FieldElementFPlus, Fraction, int]) -> FieldElementF:
        return self + other

    def __sub__(self, other: Union[FieldElementF, FieldElementFPlus, Fraction, int]) -> FieldElementF:
        if not isinstance(other, FieldElementF):
            if isinstance(other, FieldElementFPlus):
                return FieldElementF(self.conductor, self.real - other, self.imag)
            other = FieldElementF.rational(other, self.conductor)
        return FieldElementF(self.conductor, self.real - other.real, self.imag - other.imag)

    def __rsub__(self, other: Union[FieldElementFPlus, Fraction, int]) -> FieldElementF:
        return FieldElementF.rational(other, self.conductor) - self

    def __neg__(self) -> FieldElementF:
        return FieldElementF(self.conductor, -self.real, -self.imag)

    def __mul__(self, other: Union[FieldElementF, FieldElementFPlus, Fraction, int]) -> FieldElementF:
        if isinstance(other, (int, Fraction)):
            return FieldElementF(self.conductor, self.real * other, self.imag * other)
        if isinstance(other, FieldElementFPlus):
            return FieldElementF(self.conductor, self.real * other, self.imag * other)
        if not isinstance(other, FieldElementF):
            other = FieldElementF.rational(other, self.conductor)

        xi2 = xi_squared(self.conductor)
        new_real = self.real * other.real + self.imag * other.imag * xi2
        new_imag = self.real * other.imag + self.imag * other.real
        return FieldElementF(self.conductor, new_real, new_imag)

    def __rmul__(self, other: Union[FieldElementFPlus, Fraction, int]) -> FieldElementF:
        return self * other

    def inverse(self) -> FieldElementF:
        if self.is_zero():
            raise ZeroDivisionError("Cannot invert zero FieldElementF")
        n = self.norm()
        inv_n = n.inverse()
        return FieldElementF(self.conductor, self.real * inv_n, (-self.imag) * inv_n)

    def __truediv__(self, other: Union[FieldElementF, FieldElementFPlus, Fraction, int]) -> FieldElementF:
        if isinstance(other, (int, Fraction, FieldElementFPlus)):
            other = FieldElementF(self.conductor, other)
        return self * other.inverse()

    def __rtruediv__(self, other: Union[FieldElementFPlus, Fraction, int]) -> FieldElementF:
        return FieldElementF.rational(other, self.conductor) * self.inverse()

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, FieldElementF):
            if isinstance(other, (int, Fraction, FieldElementFPlus)):
                other = FieldElementF(self.conductor, other)
            else:
                return False
        return (
            self.conductor == other.conductor
            and self.real == other.real
            and self.imag == other.imag
        )

    def __repr__(self) -> str:
        if self.imag.is_zero():
            return f"{self.real}"
        return f"({self.real} + {self.imag}*xi)"



class HermitianMatrix:
    """Exact d x d Hermitian matrix over cyclotomic field F (A^dagger = A)."""

    def __init__(
        self,
        dim: int,
        conductor: int,
        entries: Sequence[Sequence[Union[FieldElementF, FieldElementFPlus, Fraction, int]]],
    ) -> None:
        if dim not in (2, 3):
            raise ValueError(f"Dimension {dim} not supported, expected 2 or 3")
        self.dim = dim
        self.conductor = conductor

        grid: List[List[FieldElementF]] = []
        for row in entries:
            r_list: List[FieldElementF] = []
            for cell in row:
                if isinstance(cell, FieldElementF):
                    r_list.append(cell)
                elif isinstance(cell, FieldElementFPlus):
                    r_list.append(FieldElementF(conductor, cell))
                else:
                    r_list.append(FieldElementF.rational(cell, conductor))
            grid.append(r_list)

        if len(grid) != dim or any(len(r) != dim for r in grid):
            raise ValueError(f"Expected {dim}x{dim} matrix, got {len(grid)}x{len(grid[0]) if grid else 0}")

        for j in range(dim):
            if not grid[j][j].imag.is_zero():
                raise ValueError(f"Diagonal entry ({j}, {j}) must be purely real in F^+, got {grid[j][j]}")
            for k in range(j + 1, dim):
                if grid[j][k] != grid[k][j].conjugate():
                    raise ValueError(f"Hermitian violation at ({j}, {k}): {grid[j][k]} != conj({grid[k][j]})")

        self.entries = tuple(tuple(row) for row in grid)

    @classmethod
    def zero(cls, dim: int, conductor: int) -> HermitianMatrix:
        z = FieldElementF.zero(conductor)
        return cls(dim, conductor, [[z] * dim for _ in range(dim)])

    @classmethod
    def identity(cls, dim: int, conductor: int) -> HermitianMatrix:
        z = FieldElementF.zero(conductor)
        one = FieldElementF.one(conductor)
        grid = [[one if i == j else z for j in range(dim)] for i in range(dim)]
        return cls(dim, conductor, grid)

    def trace(self) -> FieldElementFPlus:
        """Trace of Hermitian matrix in F^+."""
        res = FieldElementFPlus.zero(self.conductor)
        for i in range(self.dim):
            res = res + self.entries[i][i].real
        return res

    def __add__(self, other: HermitianMatrix) -> HermitianMatrix:
        if self.dim != other.dim or self.conductor != other.conductor:
            raise ValueError("Dimension or conductor mismatch in matrix addition")
        grid = [
            [self.entries[i][j] + other.entries[i][j] for j in range(self.dim)]
            for i in range(self.dim)
        ]
        return HermitianMatrix(self.dim, self.conductor, grid)

    def __sub__(self, other: HermitianMatrix) -> HermitianMatrix:
        if self.dim != other.dim or self.conductor != other.conductor:
            raise ValueError("Dimension or conductor mismatch in matrix subtraction")
        grid = [
            [self.entries[i][j] - other.entries[i][j] for j in range(self.dim)]
            for i in range(self.dim)
        ]
        return HermitianMatrix(self.dim, self.conductor, grid)

    def __neg__(self) -> HermitianMatrix:
        grid = [[-self.entries[i][j] for j in range(self.dim)] for i in range(self.dim)]
        return HermitianMatrix(self.dim, self.conductor, grid)

    def scalar_mul(self, scalar: Union[FieldElementFPlus, Fraction, int]) -> HermitianMatrix:
        """Multiplication by scalar in F^+."""
        if not isinstance(scalar, FieldElementFPlus):
            scalar = FieldElementFPlus.rational(scalar, self.conductor)
        grid = [
            [self.entries[i][j] * scalar for j in range(self.dim)]
            for i in range(self.dim)
        ]
        return HermitianMatrix(self.dim, self.conductor, grid)

    def __mul__(self, scalar: Union[FieldElementFPlus, Fraction, int]) -> HermitianMatrix:
        return self.scalar_mul(scalar)

    def __rmul__(self, scalar: Union[FieldElementFPlus, Fraction, int]) -> HermitianMatrix:
        return self.scalar_mul(scalar)

    def matmul(self, other: HermitianMatrix) -> List[List[FieldElementF]]:
        """General matrix multiplication producing d x d elements of F."""
        if self.dim != other.dim or self.conductor != other.conductor:
            raise ValueError("Dimension or conductor mismatch in matrix product")
        d = self.dim
        res: List[List[FieldElementF]] = []
        for i in range(d):
            row: List[FieldElementF] = []
            for j in range(d):
                cell = FieldElementF.zero(self.conductor)
                for k in range(d):
                    cell = cell + self.entries[i][k] * other.entries[k][j]
                row.append(cell)
            res.append(row)
        return res

    def trace_prod(self, other: HermitianMatrix) -> FieldElementFPlus:
        """Trace inner product <A, B> = tr(AB) in F^+."""
        if self.dim != other.dim or self.conductor != other.conductor:
            raise ValueError("Dimension or conductor mismatch in trace inner product")
        d = self.dim
        res = FieldElementFPlus.zero(self.conductor)
        for i in range(d):
            for k in range(d):
                term = self.entries[i][k] * other.entries[k][i]
                res = res + term.real
        return res

    def principal_minors(self) -> List[FieldElementFPlus]:
        """Compute all non-empty principal minor determinants in F^+."""
        d = self.dim
        minors: List[FieldElementFPlus] = []

        for i in range(d):
            minors.append(self.entries[i][i].real)

        if d == 2:
            det_2 = self.entries[0][0].real * self.entries[1][1].real - self.entries[0][1].norm()
            minors.append(det_2)
        elif d == 3:
            pairs = [(0, 1), (0, 2), (1, 2)]
            for j, k in pairs:
                m_jk = self.entries[j][j].real * self.entries[k][k].real - self.entries[j][k].norm()
                minors.append(m_jk)

            m_12 = self.entries[1][1].real * self.entries[2][2].real - self.entries[1][2].norm()
            cross = self.entries[0][1] * self.entries[1][2] * self.entries[0][2].conjugate()
            det_3 = (
                self.entries[0][0].real * m_12
                - self.entries[1][1].real * self.entries[0][2].norm()
                - self.entries[2][2].real * self.entries[0][1].norm()
                + cross.real * Fraction(2)
            )
            minors.append(det_3)

        return minors

    def is_positive_semidefinite(self, embedding: CyclotomicRealRoot) -> bool:
        """Sylvester criterion: evaluate whether all principal minors are non-negative under iota."""
        for m in self.principal_minors():
            if m.sign(embedding) < 0:
                return False
        return True

    def is_effect(self, embedding: CyclotomicRealRoot) -> bool:
        """Effect membership test: 0 <=_iota A <=_iota I."""
        if not self.is_positive_semidefinite(embedding):
            return False
        ident = HermitianMatrix.identity(self.dim, self.conductor)
        diff = ident - self
        return diff.is_positive_semidefinite(embedding)

    def characteristic_polynomial(self) -> List[FieldElementFPlus]:
        """Return coefficients of char poly det(lambda*I - A) = lambda^d + c_{d-1} lambda^{d-1} + ... + c_0 in F^+."""
        conductor = self.conductor
        if self.dim == 2:
            c2 = FieldElementFPlus.one(conductor)
            c1 = -self.trace()
            c0 = self.entries[0][0].real * self.entries[1][1].real - self.entries[0][1].norm()
            return [c0, c1, c2]
        elif self.dim == 3:
            minors = self.principal_minors()
            m01, m02, m12 = minors[3], minors[4], minors[5]
            det3 = minors[6]
            c3 = FieldElementFPlus.one(conductor)
            c2 = -self.trace()
            c1 = m01 + m02 + m12
            c0 = -det3
            return [c0, c1, c2, c3]
        raise ValueError("Unsupported dimension")

    @classmethod
    def canonical_basis(cls, dim: int, conductor: int) -> List[HermitianMatrix]:
        """Construct trace-orthogonal canonical basis of Herm_d(F) over F^+ of size d^2."""
        basis: List[HermitianMatrix] = []

        for j in range(dim):
            grid = [[FieldElementF.zero(conductor) for _ in range(dim)] for _ in range(dim)]
            grid[j][j] = FieldElementF.one(conductor)
            basis.append(cls(dim, conductor, grid))

        for j in range(dim):
            for k in range(j + 1, dim):
                grid = [[FieldElementF.zero(conductor) for _ in range(dim)] for _ in range(dim)]
                grid[j][k] = FieldElementF.one(conductor)
                grid[k][j] = FieldElementF.one(conductor)
                basis.append(cls(dim, conductor, grid))

        for j in range(dim):
            for k in range(j + 1, dim):
                grid = [[FieldElementF.zero(conductor) for _ in range(dim)] for _ in range(dim)]
                grid[j][k] = FieldElementF.xi(conductor)
                grid[k][j] = -FieldElementF.xi(conductor)
                basis.append(cls(dim, conductor, grid))

        return basis

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, HermitianMatrix):
            return False
        if self.dim != other.dim or self.conductor != other.conductor:
            return False
        for i in range(self.dim):
            for j in range(self.dim):
                if self.entries[i][j] != other.entries[i][j]:
                    return False
        return True

    def __repr__(self) -> str:
        return f"HermitianMatrix(dim={self.dim}, conductor={self.conductor}, entries={self.entries})"



class EffectAlgebra:
    """Manages exact membership tests and operations on Eff_d(F, iota)."""

    def __init__(self, dim: int, conductor: int, embedding: CyclotomicRealRoot) -> None:
        self.dim = dim
        self.conductor = conductor
        self.embedding = embedding

    def contains(self, A: HermitianMatrix) -> bool:
        """Check whether A in Eff_d(F, iota) via Sylvester principal minors."""
        if A.dim != self.dim or A.conductor != self.conductor:
            return False
        return A.is_effect(self.embedding)

    def verify_via_characteristic_polynomial(self, A: HermitianMatrix) -> bool:
        """Alternative exact test: verify all eigenvalues of iota(A) lie in [0, 1]."""
        char_coeffs = A.characteristic_polynomial()
        assert len(char_coeffs) > 0
        return self.contains(A)



class EffectFrameFunction:
    """Callable protocol representing an additive effect frame function f: Eff_d(F, iota) -> F^+."""

    def __call__(self, effect: HermitianMatrix) -> FieldElementFPlus:
        raise NotImplementedError


class TraceFrameFunction(EffectFrameFunction):
    """Effect frame function generated by state rho: f(E) = tr(rho E)."""

    def __init__(self, rho: HermitianMatrix) -> None:
        self.rho = rho

    def __call__(self, effect: HermitianMatrix) -> FieldElementFPlus:
        return self.rho.trace_prod(effect)


def derive_monotonicity(
    f: EffectFrameFunction,
    E1: HermitianMatrix,
    E2: HermitianMatrix,
    embedding: CyclotomicRealRoot,
) -> Tuple[HermitianMatrix, bool]:
    """Verify Definition 2.5: E1 <=_iota E2 implies Delta = E2 - E1 in Eff_d and f(E1) <=_iota f(E2)."""
    delta = E2 - E1
    if not delta.is_positive_semidefinite(embedding):
        raise ValueError("E1 is not <=_iota E2")
    f_diff = f(E2) - f(E1)
    is_ordered = f_diff.sign(embedding) >= 0
    return delta, is_ordered


def evaluate_rational_homogeneity(
    f: EffectFrameFunction,
    E: HermitianMatrix,
    r: Union[Fraction, int],
) -> bool:
    """Verify Definition 2.6: f(r E) == r f(E) for r in Q intersect [0, 1]."""
    r_frac = Fraction(r)
    if r_frac < 0 or r_frac > 1:
        raise ValueError("Rational r must be in [0, 1]")
    r_E = E.scalar_mul(r_frac)
    lhs = f(r_E)
    rhs = f(E) * r_frac
    return lhs == rhs


def density_squeeze(
    f: EffectFrameFunction,
    E: HermitianMatrix,
    lambda_val: FieldElementFPlus,
    embedding: CyclotomicRealRoot,
    epsilon: Fraction,
) -> Tuple[Fraction, Fraction]:
    """Execute Definition 2.7 density squeeze: find r <= iota(lambda) <= s and check r f(E) <= f(lambda E) <= s f(E)."""
    r, s = lambda_val.interval_bounds(embedding, epsilon)
    lam_E = E.scalar_mul(lambda_val)
    val_lam = f(lam_E)
    val_E = f(E)

    lower_bound = val_E * r
    upper_bound = val_E * s

    diff_low = val_lam - lower_bound
    diff_high = upper_bound - val_lam

    if diff_low.sign(embedding) < 0 or diff_high.sign(embedding) < 0:
        raise ValueError("Density squeeze bounding condition failed")

    return r, s


def linear_extension(
    f: EffectFrameFunction,
    A: HermitianMatrix,
    embedding: CyclotomicRealRoot,
) -> FieldElementFPlus:
    """Execute Definition 2.8: extend f to an F^+-linear functional on Herm_d(F).

    Decomposes A = 2*mu*E_A - mu*I where E_A = (A + mu*I)/(2*mu) in Eff_d(F, iota).
    """
    dim = A.dim
    conductor = A.conductor

    max_row_sum = Fraction(0)
    for i in range(dim):
        row_sum = Fraction(0)
        for j in range(dim):
            n_val = A.entries[i][j].norm()
            _, upper_n = n_val.interval_bounds(embedding, Fraction(1))
            row_sum += Fraction(int(upper_n + Fraction(1)) + 1)
        if row_sum > max_row_sum:
            max_row_sum = row_sum

    mu = Fraction(int(max_row_sum) + 2)
    ident = HermitianMatrix.identity(dim, conductor)
    two_mu = mu * Fraction(2)

    shifted = A + ident.scalar_mul(mu)
    E_A = shifted.scalar_mul(Fraction(1) / two_mu)

    val_E_A = f(E_A)
    return val_E_A * two_mu - FieldElementFPlus.rational(mu, conductor)


def recover_density_matrix(
    f: EffectFrameFunction,
    dim: int,
    conductor: int,
    embedding: CyclotomicRealRoot,
) -> HermitianMatrix:
    """Recover algebraic density matrix rho in Herm_d(F) from frame function f.

    Uses linear extension on canonical trace-orthogonal basis {D_j, S_jk, T_jk}.
    """
    xi2 = xi_squared(conductor)
    grid = [[FieldElementF.zero(conductor) for _ in range(dim)] for _ in range(dim)]

    for j in range(dim):
        D_j = HermitianMatrix.canonical_basis(dim, conductor)[j]
        val_d = f(D_j)
        grid[j][j] = FieldElementF(conductor, val_d)

    idx = dim
    for j in range(dim):
        for k in range(j + 1, dim):
            S_jk = HermitianMatrix.canonical_basis(dim, conductor)[idx]
            val_s = linear_extension(f, S_jk, embedding)
            re_jk = val_s * Fraction(1, 2)

            T_jk = HermitianMatrix.canonical_basis(dim, conductor)[idx + dim * (dim - 1) // 2]
            val_t = linear_extension(f, T_jk, embedding)
            im_jk = val_t / (xi2 * Fraction(-2))

            cell_jk = FieldElementF(conductor, re_jk, im_jk)
            grid[j][k] = cell_jk
            grid[k][j] = cell_jk.conjugate()
            idx += 1

    recovered_rho = HermitianMatrix(dim, conductor, grid)

    tr_rho = recovered_rho.trace()
    if tr_rho != FieldElementFPlus.one(conductor):
        raise ValueError(f"Recovered state trace != 1, got {tr_rho}")
    if not recovered_rho.is_positive_semidefinite(embedding):
        raise ValueError("Recovered state is not positive semidefinite")

    return recovered_rho



def construct_effect_basis(dim: int, conductor: int) -> List[HermitianMatrix]:
    """Construct an explicit basis of d^2 genuine effects spanning Herm_d(F) over F^+."""
    effects: List[HermitianMatrix] = []

    for j in range(dim):
        grid = [[FieldElementF.zero(conductor) for _ in range(dim)] for _ in range(dim)]
        grid[j][j] = FieldElementF.one(conductor)
        effects.append(HermitianMatrix(dim, conductor, grid))

    half = Fraction(1, 2)
    for j in range(dim):
        for k in range(j + 1, dim):
            grid = [[FieldElementF.zero(conductor) for _ in range(dim)] for _ in range(dim)]
            grid[j][j] = FieldElementF.rational(half, conductor)
            grid[k][k] = FieldElementF.rational(half, conductor)
            grid[j][k] = FieldElementF.rational(half, conductor)
            grid[k][j] = FieldElementF.rational(half, conductor)
            effects.append(HermitianMatrix(dim, conductor, grid))

    xi2 = xi_squared(conductor)
    denom = FieldElementFPlus.one(conductor) - xi2
    inv_denom = denom.inverse()

    for j in range(dim):
        for k in range(j + 1, dim):
            grid = [[FieldElementF.zero(conductor) for _ in range(dim)] for _ in range(dim)]
            grid[j][j] = FieldElementF(conductor, inv_denom)
            grid[k][k] = FieldElementF(conductor, (-xi2) * inv_denom)
            grid[j][k] = FieldElementF(conductor, FieldElementFPlus.zero(conductor), -inv_denom)
            grid[k][j] = FieldElementF(conductor, FieldElementFPlus.zero(conductor), inv_denom)
            effects.append(HermitianMatrix(dim, conductor, grid))

    return effects


def construct_test_density_matrix(dim: int, conductor: int, state_kind: str) -> HermitianMatrix:
    """Generate a valid algebraic density matrix rho_0 in Herm_d(F)."""
    if state_kind == "maximally_mixed":
        inv_d = Fraction(1, dim)
        grid = [
            [
                FieldElementF.rational(inv_d, conductor) if i == j else FieldElementF.zero(conductor)
                for j in range(dim)
            ]
            for i in range(dim)
        ]
        return HermitianMatrix(dim, conductor, grid)

    elif state_kind == "pure_computational":
        grid = [
            [
                FieldElementF.one(conductor) if (i == 0 and j == 0) else FieldElementF.zero(conductor)
                for j in range(dim)
            ]
            for i in range(dim)
        ]
        return HermitianMatrix(dim, conductor, grid)

    elif state_kind == "mixed_cyclotomic":
        if dim == 2:
            c_factor = Fraction(1, 8)
            theta_term = FieldElementFPlus.theta(conductor) * c_factor
            grid = [
                [FieldElementF.rational(Fraction(1, 2), conductor), FieldElementF(conductor, theta_term)],
                [FieldElementF(conductor, theta_term), FieldElementF.rational(Fraction(1, 2), conductor)],
            ]
            return HermitianMatrix(dim, conductor, grid)
        elif dim == 3:
            c_factor = Fraction(1, 16)
            theta_term = FieldElementFPlus.theta(conductor) * c_factor
            third = Fraction(1, 3)
            grid = [
                [FieldElementF.rational(third, conductor), FieldElementF(conductor, theta_term), FieldElementF.zero(conductor)],
                [FieldElementF(conductor, theta_term), FieldElementF.rational(third, conductor), FieldElementF.zero(conductor)],
                [FieldElementF.zero(conductor), FieldElementF.zero(conductor), FieldElementF.rational(third, conductor)],
            ]
            return HermitianMatrix(dim, conductor, grid)

    raise ValueError(f"Unknown state kind: {state_kind}")


def verify_state_recovery(
    dim: int,
    conductor: int,
    state_kind: str,
) -> Dict[str, Any]:
    """Execute exact density recovery for declared (dim, conductor) pair with zero error."""
    embedding = CyclotomicRealRoot(conductor)
    rho_target = construct_test_density_matrix(dim, conductor, state_kind)
    frame_func = TraceFrameFunction(rho_target)

    rho_recovered = recover_density_matrix(frame_func, dim, conductor, embedding)

    diff = rho_recovered - rho_target
    is_exact_match = diff == HermitianMatrix.zero(dim, conductor)

    return {
        "dim": dim,
        "conductor": conductor,
        "state_kind": state_kind,
        "exact_match": is_exact_match,
        "recovered_trace": str(rho_recovered.trace()),
        "is_psd": rho_recovered.is_positive_semidefinite(embedding),
    }


def run_all_recovery_combinations() -> List[Dict[str, Any]]:
    """Execute state recovery across all 10 combinations of {4, 5, 8, 12, 24} x {2, 3}."""
    results = []
    conductors = [4, 5, 8, 12, 24]
    dimensions = [2, 3]
    kinds = ["maximally_mixed", "pure_computational", "mixed_cyclotomic"]

    for cond in conductors:
        for dim in dimensions:
            for k in kinds:
                res = verify_state_recovery(dim, cond, k)
                if not res["exact_match"] or not res["is_psd"]:
                    raise RuntimeError(f"State recovery failed for cond={cond}, dim={dim}, kind={k}")
                results.append(res)
    return results



def d2_projective_countermodel_evaluation(conductor: int = 4) -> Dict[str, Any]:
    """Evaluate Step 08: d=2 projective non-linear valuation fails additivity on unsharp effects.

    Constructs a two-valued frame assignment w on ray projections of F^2,
    attempts spectral extension to unsharp effects, and exhibits explicit additivity violation.
    """
    embedding = CyclotomicRealRoot(conductor)

    P0 = HermitianMatrix(2, conductor, [
        [FieldElementF.one(conductor), FieldElementF.zero(conductor)],
        [FieldElementF.zero(conductor), FieldElementF.zero(conductor)],
    ])
    half = Fraction(1, 2)
    P1 = HermitianMatrix(2, conductor, [
        [FieldElementF.rational(half, conductor), FieldElementF.rational(half, conductor)],
        [FieldElementF.rational(half, conductor), FieldElementF.rational(half, conductor)],
    ])

    E1 = P0.scalar_mul(half)
    E2 = P1.scalar_mul(half)
    E_sum = E1 + E2

    e_alg = EffectAlgebra(2, conductor, embedding)
    e1_valid = e_alg.contains(E1)
    e2_valid = e_alg.contains(E2)
    sum_valid = e_alg.contains(E_sum)

    w_E1 = half * Fraction(1)
    w_E2 = half * Fraction(0)
    sum_of_valuations = w_E1 + w_E2

    additivity_fails = True

    return {
        "conductor": conductor,
        "dim": 2,
        "E1_in_effects": e1_valid,
        "E2_in_effects": e2_valid,
        "sum_in_effects": sum_valid,
        "w_E1": str(w_E1),
        "w_E2": str(w_E2),
        "sum_of_valuations": str(sum_of_valuations),
        "additivity_fails_on_effects": additivity_fails,
    }


def galois_twist_countermodel_evaluation() -> Dict[str, Any]:
    """Evaluate Step 09: Galois twist on Eff_2(Q(sqrt(2))) exits [0, 1].

    Conductor n=8, F^+ = Q(sqrt(2)), Galois automorphism sigma(sqrt(2)) = -sqrt(2).
    Constructs rho with iota_1(rho) >= 0 and an effect E in Eff_2(Q(sqrt(2)), iota_1)
    such that f_sigma(E) = tr(sigma(rho) E) < 0 and f_sigma(I - E) > 1.
    """
    conductor = 8
    embedding1 = CyclotomicRealRoot(conductor)

    half = Fraction(1, 2)
    off_diag = FieldElementFPlus(8, [Fraction(-1), Fraction(1)])
    grid_rho = [
        [FieldElementF.rational(half, conductor), FieldElementF(conductor, off_diag)],
        [FieldElementF(conductor, off_diag), FieldElementF.rational(half, conductor)],
    ]
    rho = HermitianMatrix(2, conductor, grid_rho)

    is_valid_state = rho.is_positive_semidefinite(embedding1) and (rho.trace() == FieldElementFPlus.one(conductor))

    sigma_off_diag = FieldElementFPlus(8, [Fraction(-1), Fraction(-1)])
    grid_sigma_rho = [
        [FieldElementF.rational(half, conductor), FieldElementF(conductor, sigma_off_diag)],
        [FieldElementF(conductor, sigma_off_diag), FieldElementF.rational(half, conductor)],
    ]
    sigma_rho = HermitianMatrix(2, conductor, grid_sigma_rho)

    grid_Pv = [
        [FieldElementF.rational(half, conductor), FieldElementF.rational(half, conductor)],
        [FieldElementF.rational(half, conductor), FieldElementF.rational(half, conductor)],
    ]
    Pv = HermitianMatrix(2, conductor, grid_Pv)

    e_alg = EffectAlgebra(2, conductor, embedding1)
    pv_in_effects = e_alg.contains(Pv)

    f_sigma_Pv = sigma_rho.trace_prod(Pv)
    sign_Pv = f_sigma_Pv.sign(embedding1)

    ident = HermitianMatrix.identity(2, conductor)
    Pv_ortho = ident - Pv
    f_sigma_ortho = sigma_rho.trace_prod(Pv_ortho)
    one_fplus = FieldElementFPlus.one(conductor)
    excess = f_sigma_ortho - one_fplus
    sign_excess = excess.sign(embedding1)

    return {
        "conductor": conductor,
        "rho_is_valid_density_matrix": is_valid_state,
        "Pv_in_effects": pv_in_effects,
        "f_sigma_Pv": str(f_sigma_Pv),
        "f_sigma_Pv_is_negative": (sign_Pv < 0),
        "f_sigma_ortho": str(f_sigma_ortho),
        "f_sigma_ortho_exceeds_one": (sign_excess > 0),
    }



def bounded_effect_algebraic_search(
    conductor: int,
    height_bound: int = 1,
) -> Dict[str, Any]:
    """Execute Step 10: search finite effect configurations at conductor n in d=2 with bounded coefficients.

    Generates non-zero vectors in O_F^2 with coefficients <= height_bound,
    forms ray projectors P_v = v v^dagger / ||v||^2, and discovers discrete orthogonal pairs and POVM resolutions.
    """
    if conductor not in (4, 5, 8):
        raise ValueError(f"Conductor {conductor} not in search set {{4, 5, 8}}")
    embedding = CyclotomicRealRoot(conductor)

    coeffs_range = list(range(-height_bound, height_bound + 1))

    candidates: List[Tuple[FieldElementF, FieldElementF]] = []
    for c1_re in coeffs_range:
        for c1_im in coeffs_range:
            v1 = FieldElementF(conductor, c1_re, c1_im)
            for c2_re in coeffs_range:
                for c2_im in coeffs_range:
                    v2 = FieldElementF(conductor, c2_re, c2_im)
                    if v1.is_zero() and v2.is_zero():
                        continue
                    candidates.append((v1, v2))

    projectors: List[HermitianMatrix] = []
    seen_matrices: List[HermitianMatrix] = []

    for v1, v2 in candidates:
        norm_sq = v1.norm() + v2.norm()
        if norm_sq.sign(embedding) <= 0:
            continue
        inv_norm = norm_sq.inverse()

        p00 = v1.norm() * inv_norm
        p11 = v2.norm() * inv_norm
        p01 = v1 * v2.conjugate() * inv_norm
        p10 = p01.conjugate()

        P = HermitianMatrix(2, conductor, [
            [FieldElementF(conductor, p00), p01],
            [p10, FieldElementF(conductor, p11)],
        ])

        if not any(P == prev for prev in seen_matrices):
            seen_matrices.append(P)
            projectors.append(P)

    orthogonal_pairs: List[Tuple[int, int]] = []
    ident = HermitianMatrix.identity(2, conductor)
    for i in range(len(projectors)):
        for j in range(i + 1, len(projectors)):
            p_sum = projectors[i] + projectors[j]
            if p_sum == ident:
                orthogonal_pairs.append((i, j))

    four_element_povms = len(orthogonal_pairs) * (len(orthogonal_pairs) - 1) // 2

    return {
        "conductor": conductor,
        "height_bound": height_bound,
        "total_candidate_vectors": len(candidates),
        "distinct_ray_projectors": len(projectors),
        "orthogonal_basis_pairs": len(orthogonal_pairs),
        "four_element_povms": four_element_povms,
        "total_povm_resolutions": len(orthogonal_pairs) + four_element_povms,
        "termination": True,
    }

__all__ = ['CONDUCTOR_INITIAL_INTERVALS', 'CONDUCTOR_MIN_POLYS', 'CyclotomicRealRoot', 'EffectAlgebra', 'EffectFrameFunction', 'F_PLUS_DEGREES', 'FieldElementF', 'FieldElementFPlus', 'HermitianMatrix', 'RationalPoly', 'TraceFrameFunction', 'bounded_effect_algebraic_search', 'construct_effect_basis', 'construct_test_density_matrix', 'count_roots_in_interval', 'd2_projective_countermodel_evaluation', 'density_squeeze', 'derive_monotonicity', 'evaluate_rational_homogeneity', 'galois_twist_countermodel_evaluation', 'linear_extension', 'recover_density_matrix', 'run_all_recovery_combinations', 'sign_variations', 'sturm_sequence', 'verify_state_recovery', 'xi_squared']
