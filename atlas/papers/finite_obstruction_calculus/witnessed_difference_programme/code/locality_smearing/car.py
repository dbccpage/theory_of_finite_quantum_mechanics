"""Reconstruct the declared L=4 source Hessian, not a continuum simulator.

Insertion convention: Tr(K[N-1] exp(a.z[N-1]/2) ... K[0] exp(a.z[0]/2)).
G is four times the Hessian of log Z. The trace is on all 16 Fock states.
The generator supplies matrices; their congruence witnesses are checked elsewhere.
"""

from __future__ import annotations

from fractions import Fraction

import sympy as sp


def operators():
    identity = sp.eye(16)
    annihilators = []
    for x in range(4):
        matrix = sp.zeros(16)
        for state in range(16):
            if state & (1 << x):
                matrix[state ^ (1 << x), state] = (-1) ** (state & ((1 << x) - 1)).bit_count()
        annihilators.append(matrix)
    number = [c.T * c for c in annihilators]
    observables = [(-1) ** x * (number[x] - identity / 2) for x in range(4)]
    bonds = []
    for x in range(4):
        y = (x + 1) % 4
        bonds.append(
            (
                number[x]
                + number[y]
                - 2 * number[x] * number[y]
                + annihilators[x].T * annihilators[y]
                + annihilators[y].T * annihilators[x]
            )
            / 2
        )
    return identity, observables, bonds


def response(m: int, theta=sp.Rational(1, 10)):
    if type(m) is not int or m < 1:
        raise ValueError("positive integer M required")
    if type(theta) is bool or not isinstance(theta, (int, Fraction, sp.Rational, sp.Symbol)):
        raise ValueError("exact rational temperature or one symbolic parameter required")
    if not isinstance(theta, sp.Symbol):
        theta = sp.Rational(theta)
        if not 0 <= theta <= 1:
            raise ValueError("temperature outside the declared compact profile")
    identity, observables, bonds = operators()
    r = theta / m
    n = 2 * m
    k = [
        (identity + r * bonds[0]) * (identity + r * bonds[2]),
        (identity + r * bonds[1]) * (identity + r * bonds[3]),
    ]
    # segment(lo,hi) = K[hi-1] ... K[lo]. Empty products are identity.
    segments = {}
    for lo in range(n + 1):
        segments[lo, lo] = identity
        for hi in range(lo + 1, n + 1):
            segments[lo, hi] = k[(hi - 1) % 2] * segments[lo, hi - 1]
    trace = segments[0, n].trace()
    diagonal = [[observables[x][s, s] for s in range(16)] for x in range(4)]
    first = []
    for i in range(n):
        cyclic = segments[0, i] * segments[i, n]
        first.extend(
            sum(cyclic[s, s] * diagonal[x][s] for s in range(16)) / trace for x in range(4)
        )
    g = sp.zeros(4 * n)
    for i in range(n):
        for j in range(i, n):
            h = segments[0, i] * segments[j, n]
            middle = segments[i, j]
            weights = [
                (a, b, h[a, b] * middle[b, a])
                for a in range(16)
                for b in range(16)
                if h[a, b] != 0 and middle[b, a] != 0
            ]
            for x in range(4):
                for y in range(4):
                    second = sum(w * diagonal[x][a] * diagonal[y][b] for a, b, w in weights) / trace
                    entry = sp.factor(second - first[4 * i + x] * first[4 * j + y])
                    g[4 * i + x, 4 * j + y] = entry
                    g[4 * j + y, 4 * i + x] = entry
    v = sp.Matrix([(-1) ** j for j in range(n) for _ in range(4)])
    eigenvalue = sp.factor((v.T * g * v)[0] / (4 * n))
    if any(sp.simplify(x) != 0 for x in g * v - eigenvalue * v):
        raise AssertionError("staggered vector is not an eigenvector")
    return {
        "M": m,
        "N": n,
        "theta": theta,
        "step_r": r,
        "partition": sp.factor(trace / (1 + r) ** m),
        "matrix": g,
        "staggered": v,
        "eigenvalue": eigenvalue,
    }


def exchange_cycle():
    """Actual CAR signs for the six legal configuration moves on a star."""
    states = [6, 5, 12, 9, 10, 3, 6]
    moves = [(1, 0), (0, 3), (2, 0), (0, 1), (3, 0), (0, 2)]
    signs = []
    for source, target, (src, dst) in zip(states[:-1], states[1:], moves, strict=True):
        if not source & (1 << src) or source & (1 << dst):
            raise AssertionError("illegal hop")
        interim = source ^ (1 << src)
        sign = (-1) ** (
            (source & ((1 << src) - 1)).bit_count() + (interim & ((1 << dst) - 1)).bit_count()
        )
        if interim | (1 << dst) != target:
            raise AssertionError("changed endpoint")
        signs.append(sign)
    return {"states": states, "moves": moves, "signs": signs, "product": sp.prod(signs)}
