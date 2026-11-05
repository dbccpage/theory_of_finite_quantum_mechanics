"""Exact replay of the source corpus' three-node vector obstruction example."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import isqrt
from typing import Iterable

from .exact import as_fraction
from .native_functionals import representative_mass, evaluate, encode, decode

ExactScalar = int | str | Fraction
Vector2 = tuple[Fraction, Fraction]


@dataclass(frozen=True)
class VectorObstruction:
    """Exact certificate plus the original six-decimal numerical presentation."""

    circulation: Vector2
    repair_potential: tuple[Vector2, Vector2, Vector2]
    residual: tuple[Vector2, Vector2, Vector2]
    l1_l1_minimum: Fraction
    l1_l2_minimum_squared: Fraction
    l1_l2_minimum_display: str


def _vector(value: Iterable[ExactScalar]) -> Vector2:
    coordinates = tuple(as_fraction(coordinate) for coordinate in value)
    if len(coordinates) != 2:
        raise ValueError("the replay admits exactly two coordinates per edge")
    return coordinates[0], coordinates[1]


def _add(left: Vector2, right: Vector2) -> Vector2:
    return left[0] + right[0], left[1] + right[1]


def _subtract(left: Vector2, right: Vector2) -> Vector2:
    return left[0] - right[0], left[1] - right[1]


def _sqrt_six_decimals(value: Fraction) -> str:
    """Format ``sqrt(value)`` to six places with exact half-even rounding."""

    if value < 0:
        raise ValueError("a squared norm cannot be negative")
    scale = 1_000_000
    scaled_numerator = value.numerator * scale * scale
    denominator = value.denominator
    floor_root = isqrt(scaled_numerator // denominator)
    midpoint_comparison = 4 * scaled_numerator - denominator * (2 * floor_root + 1) ** 2
    if midpoint_comparison > 0 or (midpoint_comparison == 0 and floor_root % 2 == 1):
        rounded = floor_root + 1
    else:
        rounded = floor_root
    whole, fractional = divmod(rounded, scale)
    return f"{whole}.{fractional:06d}"


def triangle_vector_obstruction(
    deltas: Iterable[Iterable[ExactScalar]],
) -> VectorObstruction:
    """Minimize the two source objectives exactly on one oriented 3-cycle.

    For residuals ``r = delta - d0(alpha)``, their vector sum is the cycle
    circulation ``c``. The triangle inequality bounds either sum of edge norms
    below by the corresponding norm of ``c``. The returned potential routes all
    residual to the final edge, attaining both bounds simultaneously.
    """

    edges = tuple(_vector(delta) for delta in deltas)
    if len(edges) != 3:
        raise ValueError("the replay requires the three oriented cycle edges")
    zero: Vector2 = Fraction(0), Fraction(0)
    circulation = _add(_add(edges[0], edges[1]), edges[2])
    potential = (zero, edges[0], _add(edges[0], edges[1]))
    gradient = (
        _subtract(potential[1], potential[0]),
        _subtract(potential[2], potential[1]),
        _subtract(potential[0], potential[2]),
    )
    residual: tuple[Vector2, Vector2, Vector2] = (
        _subtract(edges[0], gradient[0]),
        _subtract(edges[1], gradient[1]),
        _subtract(edges[2], gradient[2]),
    )
    if residual != (zero, zero, circulation):
        raise AssertionError("constructed repair did not route the residual to one edge")
    l1_l1 = representative_mass(circulation)
    l1_l2_squared = decode(evaluate({"operation": "squared_l2", "residual": [encode(v) for v in circulation]})["value"])
    return VectorObstruction(
        circulation,
        potential,
        residual,
        l1_l1,
        l1_l2_squared,
        _sqrt_six_decimals(l1_l2_squared),
    )


def source_three_node_example() -> VectorObstruction:
    """Replay ``[(1,0), (0,1), (0,0)]`` from the consolidated source corpus."""

    return triangle_vector_obstruction(((1, 0), (0, 1), (0, 0)))


# Executable finite evidence; AuthorityEffect: None.
