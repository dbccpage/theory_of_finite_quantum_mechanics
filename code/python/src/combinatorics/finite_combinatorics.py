"""Exact binomial coefficients, integer partitions, and counting formulas.

Origin: code/rust/src/combinatorics/enumeration.rs function binomial.
The phase-space count d*d is the number of labels, not the trace obstruction
in lean4/FiniteQM.lean theorem weyl_heisenberg_finite_trace_obstruction.
Claim: urn:omega:fqm:combinatorics:exact-binomial-and-counts:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/src/combinatorics/test_finite_combinatorics.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 6; AST Sonar cognitive complexity max 4; AST nesting depth max 1; lizard 1.24.1 cyclomatic complexity max 6.
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


@dataclass(frozen=True)
class FiniteProjectivePlaneParams:
    """Counting parameters named for PG(2, q) and AG(2, q). Existence is not claimed."""

    order_q: int
    pg_points: int
    pg_lines: int
    points_per_line: int
    ag_points: int
    ag_lines: int
    parallel_classes: int


def _fail(kind: type[CombinatoricsError], invariant: str, **parameters: object) -> CombinatoricsError:
    return kind(invariant, parameters)


def _exact_int(value: object, role: str) -> int:
    if isinstance(value, float):
        raise _fail(CombinatoricsError, "float refused at the public boundary", role=role, received="float")
    if type(value) is bool:
        raise _fail(CombinatoricsError, "boolean refused where an integer was required", role=role)
    if type(value) is not int:
        raise _fail(CombinatoricsError, "value is not an exact integer", role=role, received=type(value).__name__)
    return value


def _choose(n: int, k: int) -> int:
    if k > n - k:
        return _product(n, n - k)
    return _product(n, k)


def _product(n: int, k: int) -> int:
    result = 1
    for index in range(1, k + 1):
        result = result * (n - k + index) // index
    return result


def binomial_exact(n: object, k: object) -> int:
    """Exact C(n, k). Negative arguments and k > n return 0."""
    left = _exact_int(n, "n")
    right = _exact_int(k, "k")
    if left < 0 or right < 0 or right > left:
        return 0
    return _choose(left, right)


def _word_count(alphabet_size: int, length: int) -> int:
    if length == 0:
        return 1
    total = 1
    step = 0
    while step < length:
        total *= alphabet_size
        step += 1
    return total


def enumerate_cartesian_words(alphabet_size: object, length: object, budget: object) -> List[Tuple[int, ...]]:
    """Words in {0, ..., alphabet_size-1}^length when the count does not exceed budget."""
    size = _exact_int(alphabet_size, "alphabet_size")
    width = _exact_int(length, "length")
    limit = _exact_int(budget, "budget")
    if size < 0 or width < 0 or limit < 0:
        raise _fail(CombinatoricsError, "alphabet_size, length, and budget must be non-negative")
    total = _word_count(size, width)
    if total > limit:
        raise _fail(CombinatoricsBudgetError, "Cartesian word count exceeds budget", total=total, budget=limit)
    return [tuple(word) for word in product(range(size), repeat=width)]


def _record_partition(rem: int, max_part: int, prefix: List[int], result: List[Tuple[int, ...]]) -> None:
    if rem == 0:
        result.append(tuple(prefix))
        return
    _descend_parts(rem, max_part, prefix, result)


def _descend_parts(rem: int, max_part: int, prefix: List[int], result: List[Tuple[int, ...]]) -> None:
    for part in range(min(rem, max_part), 0, -1):
        prefix.append(part)
        _record_partition(rem - part, part, prefix, result)
        prefix.pop()


def integer_partitions(n: object) -> List[Tuple[int, ...]]:
    """Non-increasing positive partitions of n, lexicographic by the generator order."""
    size = _exact_int(n, "n")
    if size < 0:
        raise _fail(CombinatoricsError, "n must be non-negative", received=size)
    if size == 0:
        return [()]
    result: List[Tuple[int, ...]] = []
    _record_partition(size, size, [], result)
    return result


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
