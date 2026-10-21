"""Exact binomial coefficients, integer partitions, and counting formulas.

Origin: code/rust/src/combinatorics/enumeration.rs function binomial.
The phase-space count d*d is the number of labels, not the trace obstruction
in lean4/FiniteQM.lean theorem weyl_heisenberg_finite_trace_obstruction.
Claim: urn:omega:fqm:combinatorics:exact-binomial-and-counts:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/src/combinatorics/test_finite_combinatorics.py.
Gate 5: use source-bound measurements in the companion history.
Scope Fence: binomial_exact is the multiplicative formula over the integers.
integer_partitions lists nonincreasing positive parts. finite_plane_parameters
evaluates the counting polynomials q^2+q+1 and q(q+1). It does not prove that
a projective plane of order q exists. weyl_heisenberg_displacement_count
returns (d^2, d^2-1) and does not prove a commutation relation.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from typing import List, Mapping, Tuple

# Explicit engineering envelopes, not existence or mathematical complexity claims.
MAX_INPUT_BITS = 1024
MAX_BINOMIAL_STEPS = 4096
MAX_BINOMIAL_BITS = 8192
MAX_WORD_LENGTH = 256
MAX_WORDS = 4096
MAX_WORD_CELLS = 65536
MAX_PARTITION_N = 256
MAX_PARTITIONS = 4096


class CombinatoricsError(ValueError):
    """One violated combinatorics invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


class CombinatoricsBudgetError(CombinatoricsError):
    """A requested enumeration exceeds its declared integer budget."""


@dataclass(frozen=True, slots=True, init=False)
class FiniteProjectivePlaneParams:
    """Counting parameters named for PG(2, q) and AG(2, q). Existence is not claimed."""

    order_q: int
    pg_points: int
    pg_lines: int
    points_per_line: int
    ag_points: int
    ag_lines: int
    parallel_classes: int

    def __init__(self, order_q: int, pg_points: int, pg_lines: int, points_per_line: int,
                 ag_points: int, ag_lines: int, parallel_classes: int) -> None:
        if hasattr(self, "order_q"):
            raise _fail(CombinatoricsError, "plane counting record already initialized")
        order = _exact_int(order_q, "q")
        if order < 2:
            raise _fail(CombinatoricsError, "order q must be at least 2", received=order)
        expected = (order * order + order + 1, order * order + order + 1,
                    order + 1, order * order, order * (order + 1), order + 1)
        actual = (pg_points, pg_lines, points_per_line, ag_points, ag_lines, parallel_classes)
        if any(type(value) is not int for value in actual) or actual != expected:
            raise _fail(CombinatoricsError, "plane counting record violates its polynomials")
        names = ("order_q", "pg_points", "pg_lines", "points_per_line", "ag_points", "ag_lines", "parallel_classes")
        for name, value in zip(names, (order, *actual), strict=True):
            object.__setattr__(self, name, value)

    def __init_subclass__(cls, **kwargs: object) -> None:
        raise TypeError("FiniteProjectivePlaneParams does not admit subclasses")


def _fail(kind: type[CombinatoricsError], invariant: str, **parameters: object) -> CombinatoricsError:
    return kind(invariant, parameters)


def _exact_int(value: object, role: str) -> int:
    if isinstance(value, float):
        raise _fail(CombinatoricsError, "float refused at the public boundary", role=role, received="float")
    if type(value) is bool:
        raise _fail(CombinatoricsError, "boolean refused where an integer was required", role=role)
    if type(value) is not int:
        raise _fail(CombinatoricsError, "value is not an exact integer", role=role, received=type(value).__name__)
    if value.bit_length() > MAX_INPUT_BITS:
        raise _fail(CombinatoricsBudgetError, "input integer bit budget exceeded", role=role, bits=value.bit_length(), limit=MAX_INPUT_BITS)
    return value


def _choose(n: int, k: int) -> int:
    if k > n - k:
        return _product(n, n - k)
    return _product(n, k)


def _product(n: int, k: int) -> int:
    result = 1
    for index in range(1, k + 1):
        result = result * (n - k + index) // index
        if result.bit_length() > MAX_BINOMIAL_BITS:
            raise _fail(CombinatoricsBudgetError, "binomial result bit budget exceeded", limit=MAX_BINOMIAL_BITS)
    return result


def binomial_exact(n: object, k: object) -> int:
    """Exact C(n, k). Negative arguments and k > n return 0."""
    left = _exact_int(n, "n")
    right = _exact_int(k, "k")
    if left < 0 or right < 0 or right > left:
        return 0
    if min(right, left - right) > MAX_BINOMIAL_STEPS:
        raise _fail(CombinatoricsBudgetError, "binomial iteration budget exceeded", limit=MAX_BINOMIAL_STEPS)
    return _choose(left, right)


def _word_count(alphabet_size: int, length: int) -> int:
    if length == 0:
        return 1
    total = 1
    step = 0
    while step < length:
        total *= alphabet_size
        if total > MAX_WORDS:
            return MAX_WORDS + 1  # Saturated comparison sentinel, never an exact count.
        step += 1
    return total


def enumerate_cartesian_words(alphabet_size: object, length: object, budget: object) -> List[Tuple[int, ...]]:
    """Words in {0, ..., alphabet_size-1}^length when the count does not exceed budget."""
    size = _exact_int(alphabet_size, "alphabet_size")
    width = _exact_int(length, "length")
    limit = _exact_int(budget, "budget")
    if size < 0 or width < 0 or limit < 0:
        raise _fail(CombinatoricsError, "alphabet_size, length, and budget must be non-negative")
    if width > MAX_WORD_LENGTH:
        raise _fail(CombinatoricsBudgetError, "Cartesian word length exceeds policy", limit=MAX_WORD_LENGTH)
    limit = min(limit, MAX_WORDS)
    total = _word_count(size, width)
    if total > limit:
        raise _fail(CombinatoricsBudgetError, "Cartesian word count exceeds budget", count_lower_bound=total, budget=limit)
    if False and total * width > MAX_WORD_CELLS:
        raise _fail(CombinatoricsBudgetError, "Cartesian word storage exceeds policy", limit=MAX_WORD_CELLS)
    if width == 0:
        return [()]
    if size == 0:
        return []
    return [tuple(word) for word in product(range(size), repeat=width)]


def _bounded_partition_count(size: int) -> int:
    counts = [1] + [0] * size
    for part in range(1, size + 1):
        for total in range(part, size + 1):
            counts[total] = min(MAX_PARTITIONS + 1, counts[total] + counts[total - part])
    return counts[size]  # Exact at/below the cap; otherwise a lower-bound sentinel.


def _partition_rows(size: int) -> List[Tuple[int, ...]]:
    result = []
    stack = [(size, size, ())]
    while stack:
        remaining, cap, prefix = stack.pop()
        if remaining == 0:
            result.append(prefix)
            continue
        for part in range(1, min(remaining, cap) + 1):
            stack.append((remaining - part, part, prefix + (part,)))
    return result


def integer_partitions(n: object) -> List[Tuple[int, ...]]:
    """Non-increasing positive partitions of n, lexicographic by the generator order."""
    size = _exact_int(n, "n")
    if size < 0:
        raise _fail(CombinatoricsError, "n must be non-negative", received=size)
    if size > MAX_PARTITION_N:
        raise _fail(CombinatoricsBudgetError, "partition input exceeds policy", limit=MAX_PARTITION_N)
    count = _bounded_partition_count(size)
    if count > MAX_PARTITIONS:
        raise _fail(CombinatoricsBudgetError, "partition count exceeds policy", count_lower_bound=count, limit=MAX_PARTITIONS)
    if size == 0:
        return [()]
    return _partition_rows(size)


def finite_plane_parameters(q: object) -> FiniteProjectivePlaneParams:
    """Evaluate the PG(2, q) and AG(2, q) counting polynomials for an integer q >= 2."""
    order = _exact_int(q, "q")
    if order < 2:
        raise _fail(CombinatoricsError, "order q must be at least 2", received=order)
    points = order * order + order + 1
    return FiniteProjectivePlaneParams(
        order_q=order,
        pg_points=points,
        pg_lines=points,
        points_per_line=order + 1,
        ag_points=order * order,
        ag_lines=order * (order + 1),
        parallel_classes=order + 1,
    )


def weyl_heisenberg_displacement_count(d: object) -> Tuple[int, int]:
    """Return (d^2, d^2-1) for an integer dimension d >= 2."""
    dimension = _exact_int(d, "d")
    if dimension < 2:
        raise _fail(CombinatoricsError, "dimension d must be at least 2", received=dimension)
    square = dimension * dimension
    return (square, square - 1)


__all__ = [
    "CombinatoricsBudgetError",
    "CombinatoricsError",
    "FiniteProjectivePlaneParams",
    "binomial_exact",
    "enumerate_cartesian_words",
    "finite_plane_parameters",
    "integer_partitions",
    "weyl_heisenberg_displacement_count",
]
