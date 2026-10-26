"""Exact finite carriers for the three corrected premises.

R2 is the length-4 occupation ring at Euclidean time 0, not a volume limit.
R3 is the n=2 sharp pair. An external scalar is not an input.
R4 identifies Q(i) with Q(i) tensor Q(i) by multiplication. Balance does not
force pure-tensor multiplicativity. No continuum or Born-uniqueness claim.
"""

from __future__ import annotations

from fractions import Fraction


def _occupation_two_a(length: int, site: int) -> tuple[int, ...]:
    if length < 4 or length % 2 != 0:
        raise ValueError("ring length must be even and at least 4")
    if not 0 <= site < length:
        raise ValueError("site is outside the ring")
    sign = -1 if site % 2 else 1
    return tuple(
        sign * (2 * ((state >> site) & 1) - 1) for state in range(1 << length)
    )


def _r2() -> tuple[int, Fraction, Fraction, Fraction]:
    diagonal = _occupation_two_a(4, 0)
    states = len(diagonal)
    if states != 16:
        raise RuntimeError("L=4 occupation basis is not 16 states")
    if diagonal[0] != -1 or diagonal[1] != 1:
        raise RuntimeError("a_0 is not n_0 - 1/2 on the occupation basis")
    if any(entry * entry != 1 for entry in diagonal):
        raise RuntimeError("(2 a_0)^2 is not the identity")
    covariance = Fraction(1, 4)
    if any(Fraction(entry * entry, 4) != covariance for entry in diagonal):
        raise RuntimeError("on-site square is not I/4")
    theta = Fraction(-1, 96)
    ratio_e_mu = Fraction(1)
    signed_q = 96 * theta * ratio_e_mu
    signed_factor = (1 + signed_q) / (1 - signed_q)
    absolute_ratio = 96 * abs(theta) * ratio_e_mu
    if signed_factor >= covariance:
        raise RuntimeError("signed factor no longer fails to bound the covariance")
    if absolute_ratio != 1:
        raise RuntimeError("absolute ratio left the selected endpoint")
    return states, covariance, signed_factor, absolute_ratio


def _matmul_trace(
    left: tuple[tuple[Fraction, ...], ...],
    right: tuple[tuple[Fraction, ...], ...],
) -> Fraction:
    n = len(left)
    if n == 0 or any(len(row) != n for row in left):
        raise ValueError("trace expects a nonempty square")
    if len(right) != n or any(len(row) != n for row in right):
        raise ValueError("trace expects factors of one dimension")
    total = Fraction(0)
    for i in range(n):
        for k in range(n):
            total += left[i][k] * right[k][i]
    return total


def _sharp_effects(n: int) -> tuple[tuple[tuple[Fraction, ...], ...], tuple[tuple[Fraction, ...], ...]]:
    one = Fraction(1)
    zero = Fraction(0)
    accept = tuple(
        tuple(one if i == j == 0 else zero for j in range(n))
        for i in range(n)
    )
    reject = tuple(
        tuple(one if i == j and i != 0 else zero for j in range(n))
        for i in range(n)
    )
    for i in range(n):
        for j in range(n):
            expected = one if i == j else zero
            if accept[i][j] + reject[i][j] != expected:
                raise RuntimeError("sharp effects do not sum to I")
    return accept, reject


def sharp_readout(
    n: int, weight: Fraction, *, external: Fraction | None = None
) -> Fraction:
    """Readout on the n=2 sharp pair. Another carrier's scalar is refused."""
    if external is not None:
        raise ValueError("the separate n=1 value is not an input")
    if n != 2:
        raise ValueError("this carrier is the n=2 sharp pair")
    weight = Fraction(weight)
    if not 0 <= weight <= 1:
        raise ValueError("weight must lie in [0, 1]")
    accept, reject = _sharp_effects(n)
    born = _matmul_trace(accept, accept)
    mixed = sum((accept[i][i] for i in range(n)), Fraction(0)) / n
    rejected = _matmul_trace(accept, reject)
    mixed_reject = sum((reject[i][i] for i in range(n)), Fraction(0)) / n
    value = weight * born + (1 - weight) * mixed
    complement = weight * rejected + (1 - weight) * mixed_reject
    if born != 1 or rejected != 0 or value + complement != 1:
        raise RuntimeError("n=2 sharp pair is not a normalized readout")
    if not 0 <= value <= 1:
        raise RuntimeError("n=2 readout left the unit interval")
    return value


def _r3() -> Fraction:
    value = sharp_readout(2, Fraction(1, 2))
    undeformed = sharp_readout(2, Fraction(1))
    if value != Fraction(3, 4) or undeformed != 1 or value == undeformed:
        raise RuntimeError("n=2 sharp pair no longer separates lambda=1/2")
    return value


class _Gauss:
    __slots__ = ("re", "im")

    def __init__(self, re: Fraction | int, im: Fraction | int = 0) -> None:
        self.re = Fraction(re)
        self.im = Fraction(im)

    def __mul__(self, other: _Gauss) -> _Gauss:
        return _Gauss(
            self.re * other.re - self.im * other.im,
            self.re * other.im + self.im * other.re,
        )

    def conjugate(self) -> _Gauss:
        return _Gauss(self.re, -self.im)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, _Gauss) and self.re == other.re and self.im == other.im


def _pairing(scale: int, left: _Gauss, right: _Gauss) -> _Gauss:
    return _Gauss(scale) * left.conjugate() * right


def _r4() -> tuple[Fraction, Fraction, Fraction]:
    one = _Gauss(1)
    imaginary = _Gauss(0, 1)
    samples = (one, imaginary, _Gauss(Fraction(2, 3), Fraction(-3, 5)))
    for scale in (1, 2):
        for left in samples:
            for right in samples:
                if (imaginary * left) * right != left * (imaginary * right):
                    raise RuntimeError("multiplication does not balance")
                balanced = (imaginary * left) * right
                other = left * (imaginary * right)
                if _pairing(scale, balanced, one) != _pairing(scale, other, one):
                    raise RuntimeError("pairing does not descend through balance")
                formed = left * right
                square = _pairing(scale, formed, formed)
                if square.im != 0 or square.re <= 0:
                    raise RuntimeError("pairing is not positive on the sample")
                if _pairing(scale, formed, one) != _pairing(scale, one, formed).conjugate():
                    raise RuntimeError("pairing is not Hermitian")
    norm_one = _pairing(1, one, one)
    norm_two = _pairing(2, one, one)
    unit_product = one.conjugate() * one * one.conjugate() * one
    if norm_one != _Gauss(1) or norm_two != _Gauss(2) or unit_product != _Gauss(1):
        raise RuntimeError("unit pure-tensor squared norms left 1 and 2")
    if norm_two == unit_product or norm_one != unit_product:
        raise RuntimeError("multiplicativity split left scale 1")
    return norm_one.re, norm_two.re, unit_product.re


def witness() -> dict[str, int | Fraction]:
    states, covariance, signed_factor, absolute_ratio = _r2()
    norm_one, norm_two, unit_product = _r4()
    return {
        "r2_states": states,
        "r2_covariance": covariance,
        "r2_signed_factor": signed_factor,
        "r2_absolute_ratio": absolute_ratio,
        "r3_readout": _r3(),
        "r4_norm_one": norm_one,
        "r4_norm_two": norm_two,
        "r4_unit_product": unit_product,
    }


def refuse_absolute_endpoint() -> None:
    """q=1 is outside q<1. Refusal is the domain statement, not a tail bound."""
    ratio = witness()["r2_absolute_ratio"]
    if type(ratio) is not Fraction:
        raise TypeError("absolute ratio must be rational")
    if not ratio < 1:
        raise ValueError("need 96 |theta| e^mu < 1")
