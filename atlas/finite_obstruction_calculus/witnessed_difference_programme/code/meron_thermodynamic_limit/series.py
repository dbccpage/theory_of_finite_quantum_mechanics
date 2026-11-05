"""Exact Taylor series in theta of finite-volume Euclidean correlations.

For integer matrices K4 = 4K, X = sx * x and Y = sy * y the function
  G(theta, u) = Tr(e^{-(1-u) theta K} x e^{-u theta K} y) / Tr e^{-theta K}
is returned as a list ``out[n]`` of polynomials in u (lists of Fractions), the
coefficient of theta^n. Every product is checked against int64 overflow, and
the final sums are Python integers.
"""

from __future__ import annotations

from fractions import Fraction
from math import comb, factorial

import numpy as np

_LIMIT = 1 << 62


def _require_int64(*arrays: np.ndarray) -> None:
    """Refuse operands that are not int64.

    A float matrix would turn the traces inexact silently; an unsigned or narrower
    integer matrix promotes (int64 @ uint64 is float64) or wraps below the 2**62
    bound the overflow checks assume.
    """
    for a in arrays:
        if not isinstance(a, np.ndarray) or a.dtype != np.int64:
            raise TypeError("exact series need int64 numpy arrays")


def _magnitude(a: np.ndarray) -> int:
    # Convert extrema before abs: abs(np.int64(-2**63)) wraps negative.
    return max(abs(int(a.min(initial=0))), abs(int(a.max(initial=0))))


def _order(order: int) -> None:
    if type(order) is not int or order < 0:
        raise ValueError("Taylor order must be a nonnegative integer")


def _matmul(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    _require_int64(a, b)
    if a.ndim != 2 or b.ndim != 2 or a.shape[1] != b.shape[0]:
        raise ValueError("matrix product dimensions differ")
    bound = _magnitude(a) * _magnitude(b) * a.shape[1]
    if bound >= _LIMIT:
        raise OverflowError("int64 product bound exceeded; reduce the order")
    return a @ b


def powers(k4: np.ndarray, order: int) -> list[np.ndarray]:
    _require_int64(k4)
    _order(order)
    if k4.ndim != 2 or k4.shape[0] != k4.shape[1] or k4.shape[0] == 0:
        raise ValueError("Hamiltonian must be a nonempty square matrix")
    out = [np.eye(k4.shape[0], dtype=np.int64)]
    for _ in range(order):
        out.append(_matmul(out[-1], k4))
    return out


def _scaled(m: np.ndarray, op: np.ndarray) -> np.ndarray:
    """m @ op, with a 1-d ``op`` read as a diagonal matrix (column scaling)."""
    _require_int64(m, op)
    if m.ndim != 2 or op.ndim not in (1, 2) or m.shape[1] != op.shape[0]:
        raise ValueError("operator dimensions differ")
    if op.ndim == 1:
        if _magnitude(m) * _magnitude(op) >= _LIMIT:
            raise OverflowError("int64 product bound exceeded; reduce the order")
        return m * op[None, :]
    return _matmul(m, op)


def _trace_of_product(left: np.ndarray, right: np.ndarray) -> int:
    """Tr(left @ right) as a Python integer."""
    _require_int64(left, right)
    if left.ndim != 2 or right.ndim != 2 or left.shape != right.T.shape:
        raise ValueError("trace product requires paired matrix dimensions")
    bound = _magnitude(left) * _magnitude(right) * left.shape[0] * left.shape[1]
    if bound < _LIMIT:
        return int(np.sum(left * right.T))
    return int(np.sum(left.astype(object) * right.T.astype(object)))


def trace_table(pw, x, y, order):
    """T[p][q] = Tr(K4^p X K4^q Y) for p + q <= order, as Python integers."""
    _order(order)
    if len(pw) <= order:
        raise ValueError("not enough supplied matrix powers")
    table = [[0] * (order + 1) for _ in range(order + 1)]
    rights = [_scaled(pw[q], y) for q in range(order + 1)]
    for p in range(order + 1):
        left = _scaled(pw[p], x)
        for q in range(order + 1 - p):
            table[p][q] = _trace_of_product(left, rights[q])
    return table


def partition_traces(pw):
    return [int(np.trace(m.astype(object))) for m in pw]


def series(table, ztr, order, scale, *, normalise=True):
    """Coefficients of theta^n as polynomials in u; ``scale`` = sx * sy."""
    _order(order)
    if type(scale) not in (int, Fraction) or scale == 0:
        raise ValueError("nonzero exact rational scale required")
    num = [[Fraction(0)] * (order + 1) for _ in range(order + 1)]
    for p in range(order + 1):
        for q in range(order + 1 - p):
            n = p + q
            c = Fraction((-1) ** n * table[p][q], 4**n * factorial(p) * factorial(q) * scale)
            for k in range(p + 1):
                num[n][k + q] += c * (-1) ** k * comb(p, k)
    if normalise:
        z = [Fraction((-1) ** n * ztr[n], 4**n * factorial(n)) for n in range(order + 1)]
    else:
        z = [Fraction(1)] + [Fraction(0)] * order
    inv = [Fraction(0)] * (order + 1)
    inv[0] = 1 / z[0]
    for n in range(1, order + 1):
        inv[n] = -sum(z[j] * inv[n - j] for j in range(1, n + 1)) / z[0]
    out = []
    for n in range(order + 1):
        poly = [Fraction(0)] * (order + 1)
        for j in range(n + 1):
            for k in range(order + 1):
                poly[k] += num[j][k] * inv[n - j]
        out.append(poly)
    return out


def correlation(k4, x, y, order, scale, *, pw=None, normalise=True):
    pw = powers(k4, order) if pw is None else pw
    return series(trace_table(pw, x, y, order), partition_traces(pw), order, scale,
                  normalise=normalise)


def add(a, b):
    return [[p + q for p, q in zip(ra, rb)] for ra, rb in zip(a, b)]


def scale_series(a, c):
    return [[c * p for p in row] for row in a]


def zero_series(order):
    return [[Fraction(0)] * (order + 1) for _ in range(order + 1)]


def fourier(poly, m):
    """Integral over [0,1] of poly(u) e^{-i omega u}, omega = 2 pi m.

    m = 0: {0: integral}. m != 0: a dict power -> coefficient of t^power, t = 1/(i omega).
    """
    if type(m) is not int or any(type(c) not in (int, Fraction) for c in poly):
        raise ValueError("Fourier mode must be an integer and coefficients exact rationals")
    if m == 0:
        return {0: sum(Fraction(c) / (k + 1) for k, c in enumerate(poly))}
    integrals = [{}]
    for k in range(1, len(poly)):
        d = {1: Fraction(-1)}
        for pw_, c in integrals[k - 1].items():
            d[pw_ + 1] = d.get(pw_ + 1, Fraction(0)) + k * c
        integrals.append(d)
    res = {}
    for k, c in enumerate(poly):
        for pw_, v in integrals[k].items():
            res[pw_] = res.get(pw_, Fraction(0)) + c * v
    return {p: v for p, v in res.items() if v}


def first_order(coeffs):
    """Least n with a nonzero theta^n polynomial, or None."""
    for n, poly in enumerate(coeffs):
        if any(poly):
            return n
    return None
