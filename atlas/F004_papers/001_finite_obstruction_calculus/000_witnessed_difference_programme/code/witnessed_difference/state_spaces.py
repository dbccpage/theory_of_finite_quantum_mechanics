"""Finite convex state spaces: exact decompositions into extreme points.

The square with extreme points v1 = (1, 0), v2 = (0, 1), v3 = (-1, 0),
v4 = (0, -1) is not a simplex: its centre is both v1/2 + v3/2 and v2/2 + v4/2.
Decompositions are enumerated exactly as the basic feasible solutions of
{lambda >= 0, sum lambda = 1, sum lambda_j v_j = x}; the decomposition polytope
is a single point exactly when there is one such solution.  Nonsimpliciality is
a finite geometric fact here, not a quantum discriminator.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations

from .exact_linear import ExactField, Vector, coerce_matrix, coerce_vector, rank, solve
from .outcomes import Accepted, Outcome, RefusalCode, Refused

FIELD = ExactField.RATIONAL
POINT_BUDGET = 10
Point = tuple[Fraction, ...]


@dataclass(frozen=True)
class StateSpace:
    extreme_points: tuple[Point, ...]

    @property
    def dimension(self) -> int:
        return len(self.extreme_points[0])


@dataclass(frozen=True)
class ConvexDecomposition:
    weights: tuple[Fraction, ...]

    @property
    def support(self) -> tuple[int, ...]:
        return tuple(index for index, weight in enumerate(self.weights) if weight != 0)


def _basic_decompositions(points: tuple[Point, ...], target: Point) -> tuple[ConvexDecomposition, ...]:
    """Every vertex of the decomposition polytope, each an exact nonnegative solution."""

    found: dict[tuple[Fraction, ...], None] = {}
    for size in range(1, len(points) + 1):
        for support in combinations(range(len(points)), size):
            columns = tuple(points[j] + (Fraction(1),) for j in support)
            if rank(columns, len(target) + 1, FIELD) != size:
                continue
            system = tuple(tuple(column[row] for column in columns) for row in range(len(target) + 1))
            solution = solve(system, target + (Fraction(1),), size, FIELD)
            if solution is None or any(value < 0 for value in solution):
                continue
            weights = [Fraction(0)] * len(points)
            for index, value in zip(support, solution):
                weights[index] = value
            found[tuple(weights)] = None
    return tuple(ConvexDecomposition(weights) for weights in found)


def make_state_space(points: object) -> Outcome[StateSpace]:
    """Admit distinct exact points of one dimension, each extreme (not a mixture of the others)."""

    admitted = coerce_matrix(points, (None, None), FIELD)
    if isinstance(admitted, Refused):
        return admitted
    listed = admitted.value
    if not listed or not listed[0] or len(set(listed)) != len(listed):
        return Refused(RefusalCode.INVALID_INPUT, "declare distinct points of positive dimension")
    if len(listed) > POINT_BUDGET:
        return Refused(RefusalCode.BUDGET_EXHAUSTED, f"the decomposition census is budgeted to {POINT_BUDGET} points")
    for index, point in enumerate(listed):
        others = listed[:index] + listed[index + 1 :]
        if others and _basic_decompositions(others, point):  # type: ignore[arg-type]
            return Refused(RefusalCode.INVALID_INPUT, f"point {index} is a mixture of the others, not extreme")
    return Accepted(StateSpace(listed))  # type: ignore[arg-type]


def square_state_space() -> StateSpace:
    """The gbit square: v1 = (1, 0), v2 = (0, 1), v3 = (-1, 0), v4 = (0, -1)."""

    one, zero = Fraction(1), Fraction(0)
    return StateSpace(((one, zero), (zero, one), (-one, zero), (zero, -one)))


def triangle_state_space() -> StateSpace:
    """The 2-simplex with extreme points (0, 0), (1, 0), (0, 1)."""

    one, zero = Fraction(1), Fraction(0)
    return StateSpace(((zero, zero), (one, zero), (zero, one)))


@dataclass(frozen=True)
class DecompositionFamily:
    point: Vector
    decompositions: tuple[ConvexDecomposition, ...]

    @property
    def unique(self) -> bool:
        return len(self.decompositions) == 1


def _readmit(space: object) -> Outcome[StateSpace]:
    if not isinstance(space, StateSpace):
        return Refused(RefusalCode.INVALID_INPUT, "a state space is required")
    return make_state_space(space.extreme_points)


def decompositions_of(space: StateSpace, point: object) -> Outcome[DecompositionFamily]:
    """The exact vertices of {lambda >= 0 : sum lambda = 1, sum lambda_j v_j = point}."""

    admitted = _readmit(space)
    if isinstance(admitted, Refused):
        return admitted
    target = coerce_vector(point, admitted.value.dimension, FIELD)
    if isinstance(target, Refused):
        return target
    found = _basic_decompositions(admitted.value.extreme_points, target.value)  # type: ignore[arg-type]
    if not found:
        return Refused(RefusalCode.OUTSIDE_CARRIER, "the point is not in the convex hull of the extreme points")
    return Accepted(DecompositionFamily(target.value, found))


def is_simplex(space: StateSpace) -> Outcome[bool]:
    """A simplex has affinely independent extreme points."""

    admitted = _readmit(space)
    if isinstance(admitted, Refused):
        return admitted
    points = admitted.value.extreme_points
    lifted = tuple(point + (Fraction(1),) for point in points)
    return Accepted(rank(lifted, admitted.value.dimension + 1, FIELD) == len(points))


@dataclass(frozen=True)
class DecompositionUniqueness:
    simplex: bool
    unique: bool
    decompositions: int


def is_simplex_decomposition_unique(space: StateSpace, point: object) -> Outcome[DecompositionUniqueness]:
    """Report simpliciality together with whether this point decomposes uniquely."""

    family = decompositions_of(space, point)
    if isinstance(family, Refused):
        return family
    simplex = is_simplex(space).value  # type: ignore[union-attr]
    return Accepted(DecompositionUniqueness(simplex, family.value.unique, len(family.value.decompositions)))


# Executable finite evidence; AuthorityEffect: None.
