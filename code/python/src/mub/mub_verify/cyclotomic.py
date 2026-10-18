"""Exact cyclotomic arithmetic over Q(zeta_24) and certified interval enclosures.

AuthorityEffect: None.
stated region only; mints no authority.

In Q(zeta_24), zeta = e^{i pi / 12}.
The minimal polynomial is Phi_24(x) = x^8 - x^4 + 1.
Every element is represented as sum_{k=0}^7 a_k zeta^k with a_k in Q (fractions.Fraction).
Real and imaginary parts decompose into Q + Q*sqrt(2) + Q*sqrt(3) + Q*sqrt(6).
"""

from __future__ import annotations

from fractions import Fraction
from typing import List, Sequence, Tuple

from .interval import RationalInterval


class Cyc24:
    """Exact element of the cyclotomic field Q(zeta_24).

    Represented in the reduced power basis {1, zeta, ..., zeta^7}.
    """

    __slots__ = ("coeffs",)

    def __init__(self, coeffs: Sequence[Fraction | int] | None = None) -> None:
        if coeffs is None:
            self.coeffs: Tuple[Fraction, ...] = tuple(Fraction(0, 1) for _ in range(8))
        else:
            if len(coeffs) != 8:
                raise ValueError("Cyc24 requires exactly 8 coefficients")
            self.coeffs = tuple(
                c if isinstance(c, Fraction) else Fraction(c) for c in coeffs
            )

    @classmethod
    def zero(cls) -> Cyc24:
        return cls()

    @classmethod
    def one(cls) -> Cyc24:
        return cls([Fraction(1, 1)] + [Fraction(0, 1)] * 7)

    @classmethod
    def rat(cls, r: Fraction | int) -> Cyc24:
        """Embed rational number into Q(zeta_24)."""
        frac = r if isinstance(r, Fraction) else Fraction(r)
        return cls([frac] + [Fraction(0, 1)] * 7)

    @classmethod
    def zeta(cls, k: int) -> Cyc24:
        """zeta_24^k = e^{i k pi / 12} for arbitrary integer k."""
        k = k % 24
        sign = 1
        if k >= 12:
            k -= 12
            sign = -1

        c = [Fraction(0, 1)] * 8
        if k < 8:
            c[k] = Fraction(sign, 1)
        elif k == 8:
            c[4] = Fraction(sign, 1)
            c[0] = Fraction(-sign, 1)
        elif k == 9:
            c[5] = Fraction(sign, 1)
            c[1] = Fraction(-sign, 1)
        elif k == 10:
            c[6] = Fraction(sign, 1)
            c[2] = Fraction(-sign, 1)
        elif k == 11:
            c[7] = Fraction(sign, 1)
            c[3] = Fraction(-sign, 1)

        return cls(c)

    def is_zero(self) -> bool:
        return all(c == 0 for c in self.coeffs)

    def add(self, other: Cyc24) -> Cyc24:
        return Cyc24([a + b for a, b in zip(self.coeffs, other.coeffs)])

    def sub(self, other: Cyc24) -> Cyc24:
        return Cyc24([a - b for a, b in zip(self.coeffs, other.coeffs)])

    def neg(self) -> Cyc24:
        return Cyc24([-c for c in self.coeffs])

    def mul_rat(self, r: Fraction | int) -> Cyc24:
        frac = r if isinstance(r, Fraction) else Fraction(r)
        return Cyc24([c * frac for c in self.coeffs])

    def mul(self, other: Cyc24) -> Cyc24:
        prod = [Fraction(0, 1)] * 15
        for i in range(8):
            ai = self.coeffs[i]
            if ai == 0:
                continue
            for j in range(8):
                bj = other.coeffs[j]
                if bj == 0:
                    continue
                prod[i + j] += ai * bj

        res = list(prod[:8])
        for deg in range(14, 7, -1):
            val = prod[deg]
            if val == 0:
                continue
            d1 = deg - 4
            d0 = deg - 8
            if d1 < 8:
                res[d1] += val
            else:
                prod[d1] += val
            if d0 < 8:
                res[d0] -= val
            else:
                prod[d0] -= val

        return Cyc24(res)

    def conj(self) -> Cyc24:
        """Complex conjugate over Q(zeta_24)."""
        a = self.coeffs
        return Cyc24([
            a[0] + a[4],
            a[3],
            a[2],
            a[1],
            -a[4],
            -a[3] - a[7],
            -a[2] - a[6],
            -a[1] - a[5],
        ])

    def abs_sq(self) -> Cyc24:
        """Squared modulus |z|^2 = z * conj(z), which is in Q."""
        return self.mul(self.conj())

    def inv(self) -> Cyc24:
        """Exact multiplicative inverse in Q(zeta_24)."""
        if self.is_zero():
            raise ZeroDivisionError("Cannot invert zero in Q(zeta_24)")
        if all(c == 0 for c in self.coeffs[1:]):
            return Cyc24.rat(Fraction(1, self.coeffs[0]))
        cols: List[List[Fraction]] = []
        for k in range(8):
            zk = Cyc24.zeta(k)
            prod = self.mul(zk)
            cols.append(list(prod.coeffs))
        mat: List[List[Fraction]] = [
            [cols[j][i] for j in range(8)] + [Fraction(1 if i == 0 else 0, 1)]
            for i in range(8)
        ]
        for col in range(8):
            piv = None
            for r in range(col, 8):
                if mat[r][col] != 0:
                    piv = r
                    break
            if piv is None:
                raise ZeroDivisionError("Non-invertible element in Q(zeta_24)")
            mat[col], mat[piv] = mat[piv], mat[col]
            pv = mat[col][col]
            for c in range(col, 9):
                mat[col][c] /= pv
            for r in range(8):
                if r != col and mat[r][col] != 0:
                    factor = mat[r][col]
                    for c in range(col, 9):
                        mat[r][c] -= factor * mat[col][c]
        return Cyc24([mat[i][8] for i in range(8)])

    def div(self, other: Cyc24) -> Cyc24:
        """Exact division self / other in Q(zeta_24)."""
        return self.mul(other.inv())

    def real_imag_decompose(self) -> Tuple[Tuple[Fraction, Fraction, Fraction, Fraction], Tuple[Fraction, Fraction, Fraction, Fraction]]:
        """Exact decomposition of Re(z) and Im(z) in basis {1, sqrt2, sqrt3, sqrt6}.

        Returns ((R0, R2, R3, R6), (I0, I2, I3, I6)).
        """
        q0 = Fraction(0, 1)
        q1 = Fraction(1, 1)
        q1_2 = Fraction(1, 2)
        q1_4 = Fraction(1, 4)
        qm1_4 = Fraction(-1, 4)

        cos_table = [
            (q1, q0, q0, q0),
            (q0, q1_4, q0, q1_4),
            (q0, q0, q1_2, q0),
            (q0, q1_2, q0, q0),
            (q1_2, q0, q0, q0),
            (q0, qm1_4, q0, q1_4),
            (q0, q0, q0, q0),
            (q0, q1_4, q0, qm1_4),
        ]

        sin_table = [
            (q0, q0, q0, q0),
            (q0, qm1_4, q0, q1_4),
            (q1_2, q0, q0, q0),
            (q0, q1_2, q0, q0),
            (q0, q0, q1_2, q0),
            (q0, q1_4, q0, q1_4),
            (q1, q0, q0, q0),
            (q0, q1_4, q0, q1_4),
        ]

        re = [Fraction(0, 1)] * 4
        im = [Fraction(0, 1)] * 4

        for k in range(8):
            ak = self.coeffs[k]
            if ak == 0:
                continue
            c = cos_table[k]
            s = sin_table[k]
            for t in range(4):
                re[t] += ak * c[t]
                im[t] += ak * s[t]

        return (
            (re[0], re[1], re[2], re[3]),
            (im[0], im[1], im[2], im[3]),
        )

    def __repr__(self) -> str:
        terms = []
        for k, c in enumerate(self.coeffs):
            if c != 0:
                terms.append(f"{c}*z^{k}" if k > 0 else f"{c}")
        return " + ".join(terms) if terms else "0"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Cyc24):
            return False
        return self.coeffs == other.coeffs

    def __hash__(self) -> int:
        return hash(self.coeffs)

    def __add__(self, other: Cyc24) -> Cyc24:
        if not isinstance(other, Cyc24):
            return NotImplemented
        return self.add(other)

    def __sub__(self, other: Cyc24) -> Cyc24:
        if not isinstance(other, Cyc24):
            return NotImplemented
        return self.sub(other)

    def __neg__(self) -> Cyc24:
        return self.neg()

    def __mul__(self, other: Cyc24 | Fraction | int) -> Cyc24:
        if isinstance(other, Cyc24):
            return self.mul(other)
        elif isinstance(other, (Fraction, int)):
            return self.mul_rat(other)
        return NotImplemented

    def __rmul__(self, other: Fraction | int) -> Cyc24:
        if isinstance(other, (Fraction, int)):
            return self.mul_rat(other)
        return NotImplemented

    def __pow__(self, power: int) -> Cyc24:
        if not isinstance(power, int):
            return NotImplemented
        if power < 0:
            return self.inv() ** (-power)
        res = Cyc24.one()
        base = self
        p = power
        while p > 0:
            if p % 2 == 1:
                res = res.mul(base)
            base = base.mul(base)
            p //= 2
        return res


def sqrt_rational_interval(n: int, iters: int = 50) -> RationalInterval:
    """Certified rational interval [lo, hi] enclosing sqrt(n) for n >= 1.

    Maintains lo^2 <= n <= hi^2 by exact rational bisection.
    """
    if n < 1:
        raise ValueError("n must be >= 1")
    target = Fraction(n, 1)
    lo = Fraction(1, 1)
    hi = Fraction(n, 1)
    half = Fraction(1, 2)

    for _ in range(iters):
        mid = (lo + hi) * half
        if mid * mid <= target:
            lo = mid
        else:
            hi = mid

    return RationalInterval(lo, hi)


class SqrtBox:
    """Certified rational intervals for sqrt(2), sqrt(3), sqrt(6)."""

    __slots__ = ("sqrt2", "sqrt3", "sqrt6")

    def __init__(self, iters: int = 50) -> None:
        self.sqrt2 = sqrt_rational_interval(2, iters)
        self.sqrt3 = sqrt_rational_interval(3, iters)
        self.sqrt6 = sqrt_rational_interval(6, iters)

    @classmethod
    def standard(cls) -> SqrtBox:
        return cls(iters=50)


def enclose_biquadratic(
    coeffs: Tuple[Fraction, Fraction, Fraction, Fraction],
    sb: SqrtBox,
) -> RationalInterval:
    """Enclose q0 + q2*sqrt2 + q3*sqrt3 + q6*sqrt6 into a RationalInterval."""
    q0, q2, q3, q6 = coeffs
    res = RationalInterval.point(q0)
    if q2 != 0:
        res = res.add(RationalInterval.point(q2).mul(sb.sqrt2))
    if q3 != 0:
        res = res.add(RationalInterval.point(q3).mul(sb.sqrt3))
    if q6 != 0:
        res = res.add(RationalInterval.point(q6).mul(sb.sqrt6))
    return res


def cyc24_interval_enclosure(z: Cyc24, sb: SqrtBox) -> Tuple[RationalInterval, RationalInterval]:
    """Certified rational interval enclosures (Re(z), Im(z))."""
    re_coeffs, im_coeffs = z.real_imag_decompose()
    re_iv = enclose_biquadratic(re_coeffs, sb)
    im_iv = enclose_biquadratic(im_coeffs, sb)
    return re_iv, im_iv
