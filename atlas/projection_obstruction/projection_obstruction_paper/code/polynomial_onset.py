"""Exact rational instances of the finite polynomial onset certificate (§5.16).

The general theorem is a written argument. This module checks the supplied
finite linear flow and polynomial readouts, including the annihilator relation;
zero sampled values or a truncated zero jet are not accepted as certificates.
The monomial coordinates are a basis convention for the symmetric-power lift.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import comb, prod
from typing import Mapping, Sequence

import sympy as sp

MAX_LIFT_DIMENSION = 256


def _rational(value: object) -> sp.Rational:
    if isinstance(value, bool) or not isinstance(value, (int, Fraction, sp.Rational)):
        raise TypeError("exact rational scalar required")
    return sp.Rational(value)


def _matrix(value: object) -> sp.ImmutableMatrix:
    if isinstance(value, sp.MatrixBase):
        return sp.ImmutableMatrix(value.rows, value.cols, [_rational(x) for x in value])
    if not isinstance(value, (list, tuple)):
        raise TypeError("matrix must be a SymPy matrix or a list/tuple of exact scalars")
    if value and isinstance(value[0], (list, tuple)):
        if any(not isinstance(row, (list, tuple)) for row in value):
            raise TypeError("every raw matrix row must be a list or tuple")
        rows = [[_rational(x) for x in row] for row in value]
        return sp.ImmutableMatrix(rows)
    return sp.ImmutableMatrix([_rational(x) for x in value])


def _indices(n: int, degree: int):
    if n == 1:
        yield (degree,)
    else:
        for first in range(degree + 1):
            for rest in _indices(n - 1, degree - first):
                yield (first, *rest)


@dataclass(frozen=True)
class PolynomialLift:
    generator: sp.ImmutableMatrix
    initial: sp.ImmutableMatrix
    readout: sp.ImmutableMatrix
    multi_indices: tuple[tuple[int, ...], ...]


def polynomial_lift(
    generator: object,
    initial: object,
    readouts: Sequence[Mapping[tuple[int, ...], object]],
) -> PolynomialLift:
    """Build z' = Lz and R = Oz from exact rational A, m and polynomial coefficients.

    Readouts map nonnegative integer multi-indices to coefficients. At least one
    coordinate and one readout are required. This finite replay implementation
    refuses lifts exceeding 256 coordinates; the theorem has no such limit.
    """
    a, m = _matrix(generator), _matrix(initial)
    n = a.rows
    if n == 0 or a.cols != n or m.shape != (n, 1) or not readouts:
        raise ValueError("nonempty square generator, matching column and readouts required")
    polynomials = []
    for polynomial in readouts:
        row = {}
        for exponent, coefficient in polynomial.items():
            if (
                not isinstance(exponent, tuple)
                or len(exponent) != n
                or any(type(k) is not int or k < 0 for k in exponent)
            ):
                raise ValueError("nonnegative integer multi-index of ambient dimension required")
            coefficient = _rational(coefficient)
            if coefficient:
                row[exponent] = coefficient
        polynomials.append(row)
    degree = max((sum(e) for row in polynomials for e in row), default=0)
    if comb(n + degree, degree) > MAX_LIFT_DIMENSION:
        raise ValueError("polynomial lift exceeds the declared finite replay dimension budget")
    indices = tuple(e for r in range(degree + 1) for e in _indices(n, r))
    positions = {e: i for i, e in enumerate(indices)}
    size = len(indices)
    lift = sp.zeros(size)
    for row, exponent in enumerate(indices):
        for i, multiplicity in enumerate(exponent):
            if not multiplicity:
                continue
            for j in range(n):
                target = list(exponent)
                target[i] -= 1
                target[j] += 1
                lift[row, positions[tuple(target)]] += multiplicity * a[i, j]
    z = sp.ImmutableMatrix([prod(m[i] ** e[i] for i in range(n)) for e in indices])
    o = sp.ImmutableMatrix([[row.get(e, sp.S.Zero) for e in indices] for row in polynomials])
    return PolynomialLift(sp.ImmutableMatrix(lift), z, o, indices)


@dataclass(frozen=True)
class OnsetCertificate:
    """Untrusted certificate data; verify against the independently supplied model.

    Coefficients of the monic cyclic annihilator are in ascending order.
    Derivatives are O L^j z, without factorial division, for 0 <= j < kappa.
    None denotes persistent zero, and is trusted only after successful replay.
    """

    annihilator: tuple[sp.Rational, ...]
    derivatives: tuple[tuple[sp.Rational, ...], ...]
    first_onset: int | None


def certify_onset(generator: object, initial: object, readouts) -> OnsetCertificate:
    lift = polynomial_lift(generator, initial, readouts)
    operator, z, o = lift.generator, lift.initial, lift.readout
    if o * z != sp.zeros(o.rows, 1):
        raise ValueError("the onset theorem requires f(m) = 0")
    columns = [z]
    for kappa in range(1, operator.rows + 1):
        following = operator * columns[-1]
        basis = sp.Matrix.hstack(*columns)
        if basis.row_join(following).rank() == kappa:
            coefficients, parameters = basis.gauss_jordan_solve(-following)
            if parameters.rows:
                raise ArithmeticError("cyclic columns unexpectedly dependent")
            jets = tuple(tuple(o * v) for v in columns)
            onset = next((j for j, jet in enumerate(jets) if any(jet)), None)
            return OnsetCertificate(tuple(coefficients) + (sp.S.One,), jets, onset)
        columns.append(following)
    raise ArithmeticError("finite-dimensional Krylov space did not close")


def verify_onset(generator: object, initial: object, readouts, claim: OnsetCertificate) -> bool:
    """Replay cyclic independence, vector annihilation, every jet and the claimed onset.

    A scalar recurrence asserted only for the displayed zero jets is insufficient:
    this checks q(L)z = 0 in the entire lifted state space.
    """
    try:
        lift = polynomial_lift(generator, initial, readouts)
        coefficients = tuple(_rational(c) for c in claim.annihilator)
        kappa = len(coefficients) - 1
        operator, z, o = lift.generator, lift.initial, lift.readout
        if not 1 <= kappa <= operator.rows or coefficients[-1] != 1:
            return False
        if o * z != sp.zeros(o.rows, 1):
            return False
        if claim.first_onset is not None and type(claim.first_onset) is not int:
            return False
        columns = [z]
        for _ in range(kappa):
            columns.append(operator * columns[-1])
        if sp.Matrix.hstack(*columns[:-1]).rank() != kappa:
            return False
        relation = sp.zeros(operator.rows, 1)
        for c, v in zip(coefficients, columns):
            relation += c * v
        if relation != sp.zeros(operator.rows, 1):
            return False
        jets = tuple(tuple(o * v) for v in columns[:-1])
        reported = tuple(tuple(_rational(c) for c in jet) for jet in claim.derivatives)
        onset = next((j for j, jet in enumerate(jets) if any(jet)), None)
        return reported == jets and claim.first_onset == onset
    except (TypeError, ValueError, AttributeError, IndexError):
        return False
