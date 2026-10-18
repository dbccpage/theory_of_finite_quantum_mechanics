"""Exact finite causal sets, interval counts, and the 2D interval action.

Origin: lean4/CausalOrder.lean theorem spacelike_symm, theorem spacelike_irrefl,
theorem c1_spacelike_1_2, theorem c1_not_spacelike_0_1, and theorem c1_not_spacelike_0_2.
Claim: urn:omega:fqm:causal:c1-spacelike-witness:v1
AuthorityEffect: None
Mutation-Kills: 8 non-equivalent source mutants, executed by code/python/src/general_relativity/test_causal_control.py.
Gate 5 measurement: radon 6.0.1 cyclomatic complexity max 6; AST Sonar cognitive complexity max 5; AST nesting depth max 2; lizard 1.24.1 cyclomatic complexity max 6.
Scope Fence: c1_spacelike_witness checks the three-element C1 poset. The
two-dimensional interval action is the finite count N - 2 N_0 + 4 N_1 - 2 N_2.
This file does not identify a continuum spacetime and does not prove the
Benincasa-Dowker continuum limit.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Mapping, Sequence


AUTHORITY_FENCE = (
    "AuthorityEffect None; not PROVED; finite causal set; no continuum admission."
)


class PosetError(ValueError):
    """One violated causal-set invariant, with the measured parameters."""

    def __init__(self, invariant: str, parameters: Mapping[str, object] | None = None) -> None:
        self.invariant = invariant
        self.parameters = {} if parameters is None else dict(parameters)
        rendered = ", ".join(f"{key}={value}" for key, value in self.parameters.items())
        message = invariant if rendered == "" else f"{invariant} ({rendered})"
        super().__init__(message)


def _fail(invariant: str, **parameters: object) -> PosetError:
    return PosetError(invariant, parameters)


def _require_int(value: object, role: str) -> int:
    if isinstance(value, float):
        raise _fail("float refused at the causal boundary", role=role, received="float")
    if isinstance(value, bool):
        raise _fail("boolean refused where an integer was required", role=role)
    if isinstance(value, int):
        return value
    raise _fail("value is not an integer", role=role, received=type(value).__name__)


def _require_index(value: object, size: int, role: str) -> int:
    index = _require_int(value, role)
    if index < 0 or index >= size:
        raise _fail("element index is out of bounds", role=role, index=index, size=size)
    return index


@dataclass(frozen=True)
class FinitePoset:
    """Finite strict partial order stored as its transitive closure."""

    size: int
    strict_relations: frozenset[tuple[int, int]]

    @classmethod
    def from_relations(cls, size: object, relations: Sequence[object]) -> FinitePoset:
        width = _require_size(size)
        edges = _parse_relations(relations, width)
        closure = _transitive_closure(width, edges)
        _refuse_cycle(width, closure)
        strict = _strict_pairs(width, closure)
        return cls(size=width, strict_relations=strict)

    def less(self, left: object, right: object) -> bool:
        source = _require_index(left, self.size, "left")
        target = _require_index(right, self.size, "right")
        return (source, target) in self.strict_relations

    def interval(self, left: object, right: object) -> list[int]:
        source = _require_index(left, self.size, "left")
        target = _require_index(right, self.size, "right")
        if source == target:
            return [source]
        if (source, target) not in self.strict_relations:
            return []
        return _closed_interval(self, source, target)

    def predecessors(self, element: object) -> list[int]:
        index = _require_index(element, self.size, "element")
        return sorted(source for source in range(self.size) if (source, index) in self.strict_relations)

    def successors(self, element: object) -> list[int]:
        index = _require_index(element, self.size, "element")
        return sorted(target for target in range(self.size) if (index, target) in self.strict_relations)

    def relation_count(self) -> int:
        return len(self.strict_relations)


def _require_size(size: object) -> int:
    width = _require_int(size, "size")
    if width < 0:
        raise _fail("causal set size is negative", size=width)
    return width


def _parse_relations(relations: Sequence[object], size: int) -> dict[int, set[int]]:
    if isinstance(relations, (str, bytes)) or not isinstance(relations, (list, tuple)):
        raise _fail("relations are not a sequence", received=type(relations).__name__)
    adjacency = {index: set() for index in range(size)}
    for index, item in enumerate(relations):
        _add_relation(adjacency, item, size, index)
    return adjacency


def _add_relation(adjacency: dict[int, set[int]], item: object, size: int, index: int) -> None:
    if isinstance(item, (str, bytes)) or not isinstance(item, (list, tuple)) or len(item) != 2:
        raise _fail("relation is not a pair", index=index, received=type(item).__name__)
    source = _require_index(item[0], size, f"relation[{index}].source")
    target = _require_index(item[1], size, f"relation[{index}].target")
    if source == target:
        return
    adjacency[source].add(target)


def _transitive_closure(size: int, adjacency: dict[int, set[int]]) -> dict[int, set[int]]:
    for middle in range(size):
        _close_through(adjacency, middle, size)
    return adjacency


def _close_through(adjacency: dict[int, set[int]], middle: int, size: int) -> None:
    for source in range(size):
        if middle in adjacency[source]:
            adjacency[source].update(adjacency[middle])


def _refuse_cycle(size: int, adjacency: dict[int, set[int]]) -> None:
    for element in range(size):
        if element in adjacency[element]:
            raise _fail("causal relation contains a cycle", element=element)


def _strict_pairs(size: int, adjacency: dict[int, set[int]]) -> frozenset[tuple[int, int]]:
    pairs: list[tuple[int, int]] = []
    for source in range(size):
        pairs.extend((source, target) for target in adjacency[source])
    return frozenset(pairs)


def _closed_interval(poset: FinitePoset, source: int, target: int) -> list[int]:
    middle: list[int] = []
    for element in range(poset.size):
        if _strictly_between(poset, source, element, target):
            middle.append(element)
    middle.sort()
    return [source, *middle, target]


def _strictly_between(poset: FinitePoset, source: int, element: int, target: int) -> bool:
    if element == source or element == target:
        return False
    if (source, element) not in poset.strict_relations:
        return False
    return (element, target) in poset.strict_relations


@dataclass(frozen=True)
class CausalSet:
    """Discrete causal set carrying exact finite observables."""

    degree: int
    label: str
    order: FinitePoset

    @classmethod
    def discrete(cls, degree: object, label: object = "") -> CausalSet:
        width = _require_size(degree)
        name = _require_label(label)
        return cls(degree=width, label=name, order=FinitePoset(width, frozenset()))

    @classmethod
    def from_relations(cls, degree: object, relations: Sequence[object], label: object = "") -> CausalSet:
        width = _require_size(degree)
        name = _require_label(label)
        return cls(degree=width, label=name, order=FinitePoset.from_relations(width, relations))

    @staticmethod
    def authority_fence() -> str:
        return AUTHORITY_FENCE

    def spacelike(self, left: object, right: object) -> bool:
        source = _require_index(left, self.degree, "left")
        target = _require_index(right, self.degree, "right")
        if source == target:
            return False
        if self.order.less(source, target):
            return False
        return not self.order.less(target, source)

    def alexandrov_interval(self, left: object, right: object) -> list[int]:
        return self.order.interval(left, right)

    def past(self, element: object) -> list[int]:
        return self.order.predecessors(element)

    def future(self, element: object) -> list[int]:
        return self.order.successors(element)

    def ordering_fraction(self) -> Fraction:
        if self.degree < 2:
            return Fraction(0)
        numerator = 2 * self.order.relation_count()
        denominator = self.degree * (self.degree - 1)
        return Fraction(numerator, denominator)

    def interval_abundances(self) -> list[int]:
        max_open = max(0, self.degree - 2)
        counts = [0] * (max_open + 1)
        for source, target in self.order.strict_relations:
            _record_abundance(self, counts, source, target)
        return counts

    def two_dimensional_interval_action(self) -> int:
        counts = self.interval_abundances()
        n0 = _count_at(counts, 0)
        n1 = _count_at(counts, 1)
        n2 = _count_at(counts, 2)
        return self.degree - 2 * n0 + 4 * n1 - 2 * n2


def _require_label(label: object) -> str:
    if not isinstance(label, str):
        raise _fail("causal label is not a string", received=type(label).__name__)
    return label


def _record_abundance(causal: CausalSet, counts: list[int], source: int, target: int) -> None:
    open_count = len(causal.order.interval(source, target)) - 2
    if open_count < len(counts):
        counts[open_count] += 1


def _count_at(counts: list[int], index: int) -> int:
    if index < len(counts):
        return counts[index]
    return 0


def c1_spacelike_witness() -> int:
    """Return 1 when the Lean C1 poset has the stated spacelike pattern."""
    poset = CausalSet.from_relations(3, ((0, 1), (0, 2)), label="C1")
    if poset.spacelike(1, 2) is not True:
        raise _fail("C1 elements 1 and 2 are not spacelike")
    if poset.spacelike(2, 1) is not True:
        raise _fail("C1 spacelike relation is not symmetric", left=2, right=1)
    if poset.spacelike(0, 1) is not False:
        raise _fail("C1 elements 0 and 1 are spacelike")
    if poset.spacelike(0, 2) is not False:
        raise _fail("C1 elements 0 and 2 are spacelike")
    if poset.spacelike(0, 0) is not False:
        raise _fail("C1 spacelike relation is reflexive")
    return 1


def main() -> int:
    """Print the C1 spacelike certificate."""
    try:
        print(c1_spacelike_witness())
    except PosetError as error:
        print(error.invariant)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
