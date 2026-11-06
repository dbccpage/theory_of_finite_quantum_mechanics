# -*- coding: utf-8 -*-
"""
Certified Rational Interval Arithmetic for Real-Valued Physical Variables.

AuthorityEffect: None.

Implements CODA Layer 5 (Q: The Continuum) interval calculus using strictly
exact rational arithmetic (fractions.Fraction). Every real-valued physical
observable is represented not by an IEEE float, but by a verified rational
interval [lo, hi] in Q x Q with lo <= hi and certified width hi - lo < epsilon.

Floats and booleans in scalar numerical positions are strictly forbidden and
raise TypeError.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import math
from typing import Any, Tuple, Union


def _validate_exact_rational(val: Any, name: str = "value") -> Fraction:
    """Accept Fraction, int, or numeric string; strictly reject float and bool."""
    if isinstance(val, bool):
        raise TypeError(f"{name} must be an exact rational or integer, got bool")
    if isinstance(val, float) or (
        getattr(val, "dtype", None) is not None and "float" in str(val.dtype).lower()
    ):
        raise TypeError(
            f"{name} must be an exact rational or integer, got float (floats strictly forbidden)"
        )
    if isinstance(val, Fraction):
        return val
    if isinstance(val, int):
        return Fraction(val)
    if isinstance(val, str):
        try:
            return Fraction(val)
        except (ValueError, ZeroDivisionError) as exc:
            raise TypeError(
                f"{name} string could not be converted to exact rational: {exc}"
            ) from exc
    raise TypeError(
        f"{name} must be an exact rational or integer, got {type(val).__name__}"
    )


def _validate_exact_int(val: Any, name: str = "integer") -> int:
    """Accept int; strictly reject float and bool."""
    if isinstance(val, bool):
        raise TypeError(f"{name} must be an integer, got bool")
    if isinstance(val, float) or (
        getattr(val, "dtype", None) is not None and "float" in str(val.dtype).lower()
    ):
        raise TypeError(f"{name} must be an integer, got float")
    if not isinstance(val, int):
        raise TypeError(f"{name} must be an integer, got {type(val).__name__}")
    return val


@dataclass(frozen=True)
class RationalInterval:
    """A closed rational interval [lo, hi] in Q x Q representing a real quantity.
    
    Invariants:
      lo <= hi (fail-closed if violated).
    """

    lo: Fraction
    hi: Fraction

    def __init__(self, lo: Any, hi: Any | None = None) -> None:
        left = _validate_exact_rational(lo, "lo")
        right = left if hi is None else _validate_exact_rational(hi, "hi")
        if left > right:
            raise ValueError(f"Interval lower bound {left} exceeds upper bound {right}")
        object.__setattr__(self, "lo", left)
        object.__setattr__(self, "hi", right)

    @classmethod
    def from_point(cls, point: Any, radius: Any = Fraction(0)) -> RationalInterval:
        """Create interval [point - radius, point + radius]."""
        p = _validate_exact_rational(point, "point")
        r = _validate_exact_rational(radius, "radius")
        if r < 0:
            raise ValueError(f"Radius must be non-negative, got {r}")
        return cls(p - r, p + r)

    @property
    def width(self) -> Fraction:
        """Total width: hi - lo >= 0."""
        return self.hi - self.lo

    @property
    def midpoint(self) -> Fraction:
        """Center: (lo + hi) / 2."""
        return (self.lo + self.hi) / 2

    @property
    def radius(self) -> Fraction:
        """Half-width: (hi - lo) / 2."""
        return (self.hi - self.lo) / 2

    def contains(self, x: Any) -> bool:
        """True iff point x lies in [lo, hi]."""
        val = _validate_exact_rational(x, "x")
        return self.lo <= val <= self.hi

    def contains_interval(self, other: RationalInterval) -> bool:
        """True iff other is entirely contained inside self."""
        if not isinstance(other, RationalInterval):
            raise TypeError(f"Expected RationalInterval, got {type(other).__name__}")
        return self.lo <= other.lo and other.hi <= self.hi

    def intersects(self, other: RationalInterval) -> bool:
        """True iff self and other have a non-empty intersection."""
        if not isinstance(other, RationalInterval):
            raise TypeError(f"Expected RationalInterval, got {type(other).__name__}")
        return not (self.hi < other.lo or other.hi < self.lo)

    def intersect(self, other: RationalInterval) -> RationalInterval:
        """Intersection of two intervals. Raises ValueError if disjoint."""
        if not self.intersects(other):
            raise ValueError(f"Intervals {self} and {other} are disjoint")
        return RationalInterval(max(self.lo, other.lo), min(self.hi, other.hi))

    def hull(self, other: RationalInterval) -> RationalInterval:
        """Convex hull containing both intervals."""
        if not isinstance(other, RationalInterval):
            raise TypeError(f"Expected RationalInterval, got {type(other).__name__}")
        return RationalInterval(min(self.lo, other.lo), max(self.hi, other.hi))

    def is_width_less_than(self, epsilon: Any) -> bool:
        """True iff width < epsilon."""
        eps = _validate_exact_rational(epsilon, "epsilon")
        return self.width < eps

    # --- Interval Arithmetic Overloads ---

    def __neg__(self) -> RationalInterval:
        return RationalInterval(-self.hi, -self.lo)

    def __pos__(self) -> RationalInterval:
        return self

    def __abs__(self) -> RationalInterval:
        if self.lo >= 0:
            return self
        if self.hi <= 0:
            return -self
        return RationalInterval(Fraction(0), max(abs(self.lo), abs(self.hi)))

    def __add__(self, other: Any) -> RationalInterval:
        if isinstance(other, RationalInterval):
            return RationalInterval(self.lo + other.lo, self.hi + other.hi)
        val = _validate_exact_rational(other, "addition operand")
        return RationalInterval(self.lo + val, self.hi + val)

    def __radd__(self, other: Any) -> RationalInterval:
        return self.__add__(other)

    def __sub__(self, other: Any) -> RationalInterval:
        if isinstance(other, RationalInterval):
            return RationalInterval(self.lo - other.hi, self.hi - other.lo)
        val = _validate_exact_rational(other, "subtraction operand")
        return RationalInterval(self.lo - val, self.hi - val)

    def __rsub__(self, other: Any) -> RationalInterval:
        val = _validate_exact_rational(other, "subtraction operand")
        return RationalInterval(val - self.hi, val - self.lo)

    def __mul__(self, other: Any) -> RationalInterval:
        if isinstance(other, RationalInterval):
            p1 = self.lo * other.lo
            p2 = self.lo * other.hi
            p3 = self.hi * other.lo
            p4 = self.hi * other.hi
            return RationalInterval(min(p1, p2, p3, p4), max(p1, p2, p3, p4))
        val = _validate_exact_rational(other, "multiplication operand")
        p1 = self.lo * val
        p2 = self.hi * val
        return RationalInterval(min(p1, p2), max(p1, p2))

    def __rmul__(self, other: Any) -> RationalInterval:
        return self.__mul__(other)

    def __truediv__(self, other: Any) -> RationalInterval:
        if isinstance(other, RationalInterval):
            if other.contains(Fraction(0)):
                raise ZeroDivisionError(f"Cannot divide by interval containing zero: {other}")
            d1 = self.lo / other.lo
            d2 = self.lo / other.hi
            d3 = self.hi / other.lo
            d4 = self.hi / other.hi
            return RationalInterval(min(d1, d2, d3, d4), max(d1, d2, d3, d4))
        val = _validate_exact_rational(other, "division operand")
        if val == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        d1 = self.lo / val
        d2 = self.hi / val
        return RationalInterval(min(d1, d2), max(d1, d2))

    def __rtruediv__(self, other: Any) -> RationalInterval:
        val = _validate_exact_rational(other, "division operand")
        return RationalInterval(val, val) / self

    def __pow__(self, power: Any) -> RationalInterval:
        p = _validate_exact_int(power, "power exponent")
        if p == 0:
            return RationalInterval(Fraction(1), Fraction(1))
        if p < 0:
            return RationalInterval(Fraction(1), Fraction(1)) / (self ** (-p))
        if p % 2 == 1:
            return RationalInterval(self.lo ** p, self.hi ** p)
        # Even power: non-negative minimum if interval straddles 0
        if self.contains(Fraction(0)):
            return RationalInterval(Fraction(0), max(self.lo ** p, self.hi ** p))
        return RationalInterval(min(self.lo ** p, self.hi ** p), max(self.lo ** p, self.hi ** p))

    def __repr__(self) -> str:
        return f"RationalInterval([{self.lo}, {self.hi}], width={self.width})"

    def to_float_tuple(self) -> Tuple[float, float]:
        """Convert to (float, float) for logging/visualization only. AuthorityEffect: None."""
        return float(self.lo), float(self.hi)


# --- Certified Elementary Functions & Transcendentals on Rational Intervals ---

def rational_heron_sqrt_bounds(val: Fraction, steps: int = 15) -> Tuple[Fraction, Fraction]:
    """Certified rational lower and upper bounds for sqrt(val) where val >= 0.
    
    Proof:
      Let y_0 >= sqrt(val).
      Heron's iteration y_{k+1} = (y_k + val / y_k) / 2 satisfies:
        y_{k+1}^2 - val = (y_k - val / y_k)^2 / 4 >= 0 ==> y_{k+1} >= sqrt(val).
      Furthermore, val / y_{k+1} <= sqrt(val).
      Thus [val / y_k, y_k] is an exact, certified enclosure of sqrt(val) in Q x Q.
    """
    if val < 0:
        raise ValueError(f"Cannot compute square root of negative rational: {val}")
    if val == 0:
        return Fraction(0), Fraction(0)
    if val == 1:
        return Fraction(1), Fraction(1)

    # Initial upper bound y_0 >= sqrt(val)
    y = max(Fraction(1), val)
    if y * y == val:
        return y, y

    for _ in range(steps):
        y = (y + val / y) / 2
        if y * y == val:
            return y, y

    lower = val / y
    upper = y
    if lower > upper:
        lower, upper = upper, lower
    return lower, upper


def sqrt_interval(interval: RationalInterval, steps: int = 20) -> RationalInterval:
    """Certified rational interval square root for non-negative intervals.
    
    For I = [lo, hi] with 0 <= lo <= hi:
      sqrt(I) subseteq [lower_bound(sqrt(lo)), upper_bound(sqrt(hi))].
    """
    if interval.lo < 0:
        raise ValueError(f"Cannot take sqrt of interval with negative values: {interval}")
    lo_lower, _ = rational_heron_sqrt_bounds(interval.lo, steps=steps)
    _, hi_upper = rational_heron_sqrt_bounds(interval.hi, steps=steps)
    return RationalInterval(lo_lower, hi_upper)


def exp_interval(interval: RationalInterval, order: int = 20) -> RationalInterval:
    """Certified rational interval exponential for [lo, hi].
    
    Uses Taylor polynomial sum_{k=0}^N x^k / k! with certified Lagrange remainder.
    Since exp is strictly increasing on R, exp([lo, hi]) = [exp(lo), exp(hi)].
    
    For a rational point x:
      If x >= 0:
        exp(x) >= sum_{k=0}^N x^k / k! (since all subsequent terms > 0).
        exp(x) <= sum_{k=0}^N x^k / k! + Remainder(x, N).
      If x < 0:
        exp(x) = 1 / exp(|x|).
        Lower bound = 1 / upper_bound(exp(|x|)).
        Upper bound = 1 / lower_bound(exp(|x|)).
    """
    order = _validate_exact_int(order, "Taylor order")
    if order < 1:
        raise ValueError("Taylor order must be >= 1")

    def _exp_point_bounds(x: Fraction) -> Tuple[Fraction, Fraction]:
        if x == 0:
            return Fraction(1), Fraction(1)
        if x < 0:
            pos_lo, pos_hi = _exp_point_bounds(-x)
            return Fraction(1) / pos_hi, Fraction(1) / pos_lo

        # x > 0:
        # Taylor sum S_N = sum_{k=0}^N x^k / k!
        terms = [Fraction(1)]
        current = Fraction(1)
        for k in range(1, order + 1):
            current = (current * x) / k
            terms.append(current)
        s_n = sum(terms)
        
        # Certified upper bound on remainder:
        # R_N(x) = sum_{k=N+1}^infty x^k / k! <= (x^{N+1} / (N+1)!) * 1 / (1 - x / (N+2))
        # Valid whenever N + 2 > x.
        # If N + 2 <= x, we increase effective N for remainder calculation.
        rem_denom = order + 2 - x
        if rem_denom <= 0:
            # Fallback safe over-bound using ceiling of x
            ceil_x = math.ceil(float(x))
            # e^x <= 3^{ceil_x}
            three_pow = Fraction(3 ** ceil_x)
            last_term = terms[-1] * x / (order + 1)
            rem = last_term * three_pow
        else:
            term_next = terms[-1] * x / (order + 1)
            rem = term_next * Fraction(order + 2) / rem_denom

        lower = s_n
        upper = s_n + rem
        return lower, upper

    lo_lower, _ = _exp_point_bounds(interval.lo)
    _, hi_upper = _exp_point_bounds(interval.hi)
    return RationalInterval(lo_lower, hi_upper)


def ln_interval_around_one(u_interval: RationalInterval, order: int = 30) -> RationalInterval:
    """Certified interval natural log ln(1 + u) for |u| < 1 using alternating series.
    
    ln(1 + u) = sum_{k=1}^infty (-1)^{k-1} u^k / k.
    For 0 <= u < 1, alternating series Leibniz criterion:
      sum_{k=1}^{2M} (-1)^{k-1} u^k / k <= ln(1+u) <= sum_{k=1}^{2M-1} (-1)^{k-1} u^k / k.
    """
    order = _validate_exact_int(order, "Taylor order")
    # Pointwise bounds for monotonically increasing ln(x)
    def _ln_point(u: Fraction) -> Tuple[Fraction, Fraction]:
        if u <= -1:
            raise ValueError(f"u must be > -1, got {u}")
        if u == 0:
            return Fraction(0), Fraction(0)
        
        # When 0 < u < 1:
        if 0 < u < 1:
            terms = [Fraction(0)]
            curr = Fraction(1)
            for k in range(1, order + 1):
                curr = curr * u
                terms.append(curr / k)
            # Alternating sums
            s_even = sum((-1)**(k-1) * terms[k] for k in range(1, (order // 2) * 2 + 1))
            s_odd = sum((-1)**(k-1) * terms[k] for k in range(1, (order // 2) * 2))
            return min(s_even, s_odd), max(s_even, s_odd)
        
        # For general u > 0, we can use ln(y) = 2 sum_{k=0}^M (1/(2k+1)) * ((y-1)/(y+1))^{2k+1}
        # with y = 1 + u > 0. Let z = (y - 1)/(y + 1) = u / (u + 2) in (0, 1).
        y = 1 + u
        z = (y - 1) / (y + 1)
        z2 = z * z
        curr_z = z
        partial = Fraction(0)
        for k in range(order):
            partial += curr_z / (2 * k + 1)
            curr_z *= z2
        lower = 2 * partial
        # Remainder: sum_{k=M}^infty z^{2k+1}/(2k+1) <= (z^{2M+1}/(2M+1)) / (1 - z^2)
        rem = 2 * (curr_z / (2 * order + 1)) / (1 - z2)
        return lower, lower + rem

    lo_lower, _ = _ln_point(u_interval.lo)
    _, hi_upper = _ln_point(u_interval.hi)
    return RationalInterval(lo_lower, hi_upper)


def certified_pi_enclosure(terms: int = 12) -> RationalInterval:
    """Certified rational interval enclosure for pi using Machin's formula:
      pi/4 = 4 arctan(1/5) - arctan(1/239)
    with exact alternating series remainder bounds.
    """
    def _arctan_alternating_bounds(x: Fraction, n_terms: int) -> Tuple[Fraction, Fraction]:
        # arctan(x) = sum_{k=0}^infty (-1)^k x^{2k+1} / (2k+1)
        # For 0 < x < 1, S_{2m-1} < arctan(x) < S_{2m}
        curr = x
        x2 = x * x
        s_even = Fraction(0)
        s_odd = Fraction(0)
        total = Fraction(0)
        for k in range(2 * n_terms):
            term = curr / (2 * k + 1)
            if k % 2 == 0:
                total += term
            else:
                total -= term
            if k == 2 * n_terms - 2:
                s_odd = total
            if k == 2 * n_terms - 1:
                s_even = total
            curr *= x2
        return min(s_odd, s_even), max(s_odd, s_even)

    lo1, hi1 = _arctan_alternating_bounds(Fraction(1, 5), terms)
    lo2, hi2 = _arctan_alternating_bounds(Fraction(1, 239), terms)

    # 4 * (4 * arctan(1/5) - arctan(1/239))
    pi_lo = 4 * (4 * lo1 - hi2)
    pi_hi = 4 * (4 * hi1 - lo2)
    return RationalInterval(pi_lo, pi_hi)


def _ln_positive_rational(x: Fraction, order: int = 25) -> Tuple[Fraction, Fraction]:
    """Exact rational enclosure of ln(x) for x > 0 using power-of-2 range reduction."""
    if x <= 0:
        raise ValueError(f"x must be > 0, got {x}")
    if x == 1:
        return Fraction(0), Fraction(0)
    if x < 1:
        inv_lo, inv_hi = _ln_positive_rational(Fraction(1) / x, order=order)
        return -inv_hi, -inv_lo

    # x > 1: range reduction x = 2^k * curr where curr in [1, 2)
    k = 0
    curr = x
    while curr >= 2:
        curr /= 2
        k += 1

    # curr in [1, 2) ==> z = (curr - 1)/(curr + 1) in [0, 1/3)
    z = (curr - 1) / (curr + 1)
    z2 = z * z
    curr_z = z
    partial = Fraction(0)
    for m in range(order):
        partial += curr_z / (2 * m + 1)
        curr_z *= z2
    ln_curr_lo = 2 * partial
    rem = 2 * (curr_z / (2 * order + 1)) / (1 - z2)
    ln_curr_hi = ln_curr_lo + rem

    # ln(2) computation with z = 1/3
    z2_two = Fraction(1, 3)
    z2_sq = Fraction(1, 9)
    curr_z2 = z2_two
    partial2 = Fraction(0)
    for m in range(order):
        partial2 += curr_z2 / (2 * m + 1)
        curr_z2 *= z2_sq
    ln_2_lo = 2 * partial2
    rem2 = 2 * (curr_z2 / (2 * order + 1)) / (1 - z2_sq)
    ln_2_hi = ln_2_lo + rem2

    # ln(x) = k * ln(2) + ln(curr)
    total_lo = k * ln_2_lo + ln_curr_lo
    total_hi = k * ln_2_hi + ln_curr_hi
    return total_lo, total_hi


def certified_ln_interval(interval: RationalInterval, order: int = 30) -> RationalInterval:
    """Certified interval natural log ln(x) for x in [lo, hi] with lo > 0."""
    if interval.lo <= 0:
        raise ValueError(f"Natural log requires strictly positive lower bound, got {interval.lo}")
    lo_lower, _ = _ln_positive_rational(interval.lo, order=order)
    _, hi_upper = _ln_positive_rational(interval.hi, order=order)
    return RationalInterval(lo_lower, hi_upper)


__all__ = [
    "RationalInterval",
    "_validate_exact_rational",
    "_validate_exact_int",
    "rational_heron_sqrt_bounds",
    "sqrt_interval",
    "exp_interval",
    "ln_interval_around_one",
    "certified_ln_interval",
    "certified_pi_enclosure",
]
