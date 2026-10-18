"""Newton divided-difference interpolation over Q, checked against Neville.

Origin: code/rust/src/linear_algebra/interpolation.rs, which states that for
distinct nodes the Neville recurrence evaluates the unique interpolating
polynomial, and that the calculation does not supply a function remainder.
Claim: urn:omega:fqm:linear-algebra:newton-neville:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/tests/test_interpolation.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 5; AST Sonar cognitive complexity max 4; AST nesting depth max 2; lizard 1.24.1 cyclomatic complexity max 5.
Scope Fence: certify_interpolant checks the rational nodes it is given. Newton
divided differences and the Neville recurrence must agree off the nodes, and
the Newton form must recover every node value. The Vandermonde column is the
monomial form of the same nodes. This file does not propagate intervals, does
not certify a Wilsonian continuum limit, and does not admit floats or Q(i).
"""

from __future__ import annotations

from fractions import Fraction
from typing import Mapping, Sequence

from .matrix import ExactMatrix, MatrixError
from .scalars import GaussianRational


class InterpolationError(MatrixError):
    """One violated interpolation invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> InterpolationError:
    return InterpolationError(invariant, parameters)


def _refuse_float(value: object, role: str) -> None:
    if isinstance(value, float):
        raise _fail("float refused at the public boundary", role=role, received="float")


def _require_entry(value: object, role: str) -> Fraction:
    _refuse_float(value, role)
    if type(value) is bool:
        raise _fail("boolean refused where a rational entry was required", role=role)
    if isinstance(value, GaussianRational):
        raise _fail("Gaussian rational refused; interpolation in this module is over Q", role=role)
    if isinstance(value, Fraction):
        return value
    if type(value) is int:
        return Fraction(value)
    raise _fail("value is not an exact rational", role=role, received=type(value).__name__)


def _rationals(values: Sequence[object], role: str) -> list[Fraction]:
    return [_require_entry(value, f"{role}[{index}]") for index, value in enumerate(values)]


def _require_nonempty(nodes: Sequence[Fraction]) -> None:
    if not nodes:
        raise _fail("interpolation needs at least one node", count=0)


def _require_same_length(left: int, right: int, role: str) -> None:
    if left != right:
        raise _fail(role, left=left, right=right)


def _next_column(nodes: Sequence[Fraction], table: Sequence[Fraction], order: int) -> list[Fraction]:
    column: list[Fraction] = []
    for index in range(len(nodes) - order):
        span = nodes[index + order] - nodes[index]
        if span == 0:
            raise _fail("abscissae must be distinct", index=index, order=order)
        column.append((table[index + 1] - table[index]) / span)
    return column


def _newton_coefficients(nodes: Sequence[Fraction], values: Sequence[Fraction]) -> list[Fraction]:
    table = list(values)
    coeffs = [table[0]]
    for order in range(1, len(nodes)):
        table = _next_column(nodes, table, order)
        coeffs.append(table[0])
    return coeffs


def divided_differences(xs: Sequence[object], ys: Sequence[object]) -> list[Fraction]:
    """Return Newton coefficients c_0, ..., c_{n-1}."""
    nodes = _rationals(xs, "abscissa")
    values = _rationals(ys, "ordinate")
    _require_same_length(len(nodes), len(values), "abscissa count does not match the ordinates")
    _require_nonempty(nodes)
    return _newton_coefficients(nodes, values)


def _horner(nodes: Sequence[Fraction], coeffs: Sequence[Fraction], abscissa: Fraction) -> Fraction:
    acc = coeffs[-1]
    for index in range(len(coeffs) - 2, -1, -1):
        acc = acc * (abscissa - nodes[index]) + coeffs[index]
    return acc


def newton_eval(xs: Sequence[object], coeffs: Sequence[object], x: object) -> Fraction:
    """Evaluate the Newton form by nested multiplication."""
    nodes = _rationals(xs, "node")
    rational = _rationals(coeffs, "coeff")
    _require_same_length(len(nodes), len(rational), "coefficient count does not match the nodes")
    _require_nonempty(nodes)
    return _horner(nodes, rational, _require_entry(x, "abscissa"))


def _neville_step(
    nodes: Sequence[Fraction],
    column: Sequence[Fraction],
    abscissa: Fraction,
    width: int,
) -> list[Fraction]:
    nxt: list[Fraction] = []
    for index in range(len(nodes) - width):
        left = nodes[index]
        right = nodes[index + width]
        span = right - left
        if span == 0:
            raise _fail("Neville nodes must be distinct", index=index, width=width)
        step = ((abscissa - left) * column[index + 1] - (abscissa - right) * column[index]) / span
        nxt.append(step)
    return nxt


def neville_eval(xs: Sequence[object], ys: Sequence[object], x: object) -> Fraction:
    """Evaluate the interpolant by the Neville recurrence."""
    nodes = _rationals(xs, "node")
    column = _rationals(ys, "ordinate")
    _require_same_length(len(nodes), len(column), "Neville sample count does not match")
    _require_nonempty(nodes)
    abscissa = _require_entry(x, "abscissa")
    for width in range(1, len(nodes)):
        column = _neville_step(nodes, column, abscissa, width)
    return column[0]


def _node_mass(xs: Sequence[object], ys: Sequence[object], coeffs: Sequence[Fraction]) -> Fraction:
    defect = Fraction(0)
    for node, ordinate in zip(xs, ys):
        gap = newton_eval(xs, list(coeffs), node) - _require_entry(ordinate, "ordinate")
        defect += abs(gap)
    return defect


def _require_agreement(newton: Fraction, neville: Fraction, abscissa: Fraction) -> None:
    if newton != neville:
        raise _fail(
            "Newton and Neville evaluations disagree",
            abscissa=str(abscissa),
            newton=str(newton),
            neville=str(neville),
        )


def _require_zero_defect(defect: Fraction) -> None:
    if defect != 0:
        raise _fail("Newton node defect is nonzero", defect=str(defect))


def interpolation_node_defect(xs: Sequence[object], ys: Sequence[object]) -> Fraction:
    """Absolute node error. Newton and Neville must agree one half-step off the first node."""
    nodes = _rationals(xs, "abscissa")
    _require_nonempty(nodes)
    coeffs = divided_differences(xs, ys)
    defect = _node_mass(xs, ys, coeffs)
    probe = nodes[0] + Fraction(1, 2)
    _require_agreement(newton_eval(xs, coeffs, probe), neville_eval(xs, ys, probe), probe)
    _require_zero_defect(defect)
    return defect


def _vandermonde_rows(nodes: Sequence[Fraction]) -> list[list[Fraction]]:
    rows: list[list[Fraction]] = []
    for node in nodes:
        power = Fraction(1)
        row: list[Fraction] = []
        for _ in nodes:
            row.append(power)
            power *= node
        rows.append(row)
    return rows


def _solve_vandermonde(rows: Sequence[Sequence[Fraction]], values: Sequence[Fraction]) -> ExactMatrix:
    try:
        inverse = ExactMatrix.from_rows(rows).inverse()
    except ValueError as exc:
        raise _fail("Vandermonde matrix is singular", nodes=len(values)) from exc
    return inverse * ExactMatrix.from_rows([[value] for value in values])


def vandermonde_solution(xs: Sequence[object], ys: Sequence[object]) -> ExactMatrix:
    """Return the monomial coefficients as a column."""
    nodes = _rationals(xs, "abscissa")
    values = _rationals(ys, "ordinate")
    _require_same_length(len(nodes), len(values), "Vandermonde sample count does not match")
    _require_nonempty(nodes)
    _newton_coefficients(nodes, values)
    return _solve_vandermonde(_vandermonde_rows(nodes), values)


def certify_interpolant(xs: Sequence[object], ys: Sequence[object]) -> tuple[Fraction, ...]:
    """Return the Newton coefficients after the node and Neville checks."""
    coeffs = divided_differences(xs, ys)
    _require_zero_defect(interpolation_node_defect(xs, ys))
    return tuple(coeffs)


__all__ = [
    "ExactMatrix",
    "InterpolationError",
    "certify_interpolant",
    "divided_differences",
    "interpolation_node_defect",
    "neville_eval",
    "newton_eval",
    "vandermonde_solution",
]
