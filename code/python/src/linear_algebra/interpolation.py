"""Newton divided-difference interpolation over Q.

Origin: code/python/src/linear_algebra/interpolation.py
Claim: the interpolant recovers every node value, and agrees with the Neville recurrence at one extra abscissa.
AuthorityEffect: None.
"""
from fractions import Fraction
from typing import List, Sequence, Tuple

from .matrix import ExactMatrix
from .scalars import GaussianRational, Q, q


class InterpolationError(Exception):
    """Nodes were repeated, jagged, or not rational."""


def _fraction(value) -> Fraction:
    if isinstance(value, GaussianRational):
        raise InterpolationError("interpolation in this module is over Q, not Q(i)")
    try:
        return Fraction(value)
    except (TypeError, ValueError) as exc:
        raise InterpolationError(f"value {value!r} is not rational") from exc


def divided_differences(xs: Sequence[object], ys: Sequence[object]) -> List[Fraction]:
    """Return Newton coefficients c_0, ..., c_{n-1} for the nodes in the given order."""
    if len(xs) != len(ys):
        raise InterpolationError(f"got {len(xs)} abscissae and {len(ys)} ordinates")
    if not xs:
        raise InterpolationError("interpolation needs at least one node")
    nodes = [_fraction(x) for x in xs]
    if len(set(nodes)) != len(nodes):
        raise InterpolationError("abscissae must be distinct")
    table = [_fraction(y) for y in ys]
    coeffs = [table[0]]
    for order in range(1, len(nodes)):
        next_column = []
        for i in range(len(nodes) - order):
            span = nodes[i + order] - nodes[i]
            next_column.append((table[i + 1] - table[i]) / span)
        table = next_column
        coeffs.append(table[0])
    return coeffs


def newton_eval(xs: Sequence[object], coeffs: Sequence[Fraction], x: object) -> Fraction:
    """Evaluate c0 + c1(x-x0) + c2(x-x0)(x-x1) + ... by nested multiplication."""
    if len(coeffs) != len(xs):
        raise InterpolationError(f"got {len(xs)} nodes and {len(coeffs)} Newton coefficients")
    nodes = [_fraction(node) for node in xs]
    abscissa = _fraction(x)
    acc = Fraction(coeffs[-1])
    for index in range(len(coeffs) - 2, -1, -1):
        acc = acc * (abscissa - nodes[index]) + coeffs[index]
    return acc


def neville_eval(xs: Sequence[object], ys: Sequence[object], x: object) -> Fraction:
    """Evaluate the same interpolant by the Neville recurrence, without building coefficients."""
    nodes = [_fraction(node) for node in xs]
    column = [_fraction(y) for y in ys]
    abscissa = _fraction(x)
    for width in range(1, len(nodes)):
        next_column = []
        for i in range(len(nodes) - width):
            left = nodes[i]
            right = nodes[i + width]
            next_column.append(((abscissa - left) * column[i + 1] - (abscissa - right) * column[i]) / (right - left))
        column = next_column
    return column[0]


def interpolation_node_defect(xs: Sequence[object], ys: Sequence[object]) -> Fraction:
    """Sum of absolute errors at the nodes. Both Newton and Neville are required to agree off the nodes."""
    coeffs = divided_differences(xs, ys)
    defect = Fraction(0)
    for node, ordinate in zip(xs, ys):
        defect += abs(newton_eval(xs, coeffs, node) - _fraction(ordinate))
    if len(xs) >= 1:
        probe = _fraction(xs[0]) + Fraction(1, 2)
        if newton_eval(xs, coeffs, probe) != neville_eval(xs, ys, probe):
            raise InterpolationError("Newton and Neville evaluations disagree")
    return defect


def vandermonde_solution(xs: Sequence[object], ys: Sequence[object]) -> ExactMatrix:
    """Solve the Vandermonde system and return the monomial coefficients as a column."""
    nodes = [_fraction(x) for x in xs]
    values = [_fraction(y) for y in ys]
    rows = []
    for node in nodes:
        power = Fraction(1)
        row = []
        for _ in nodes:
            row.append(power)
            power *= node
        rows.append(row)
    solved = ExactMatrix.from_rows(rows).inverse() * ExactMatrix.from_rows([[value] for value in values])
    return solved


__all__ = [
    "ExactMatrix",
    "GaussianRational",
    "Q",
    "q",
    "InterpolationError",
    "divided_differences",
    "newton_eval",
    "neville_eval",
    "interpolation_node_defect",
    "vandermonde_solution",
]
