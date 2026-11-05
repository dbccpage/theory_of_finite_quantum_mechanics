"""Owned bounded binary frame constraints and complete finite search.

AuthorityEffect: None. Pairs require at most one1; triples exactly one1.
At most64 variables and4096 constraints of each kind. Exhaustion means UNSAT;
a node-budget refusal is a separate Railway resource failure, never UNSAT.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import TypeAlias

from .boundary import Violation, evaluate, require
from .domains import integer, sequence
from .outcome import Outcome

Constraint: TypeAlias = tuple[int, ...]
Assignment: TypeAlias = tuple[int, ...]
SearchResult: TypeAlias = tuple[Assignment | None, int]


def _constraints(value: object, width: int, size: int) -> tuple[Constraint, ...]:
    outer = sequence(value, 'constraints', maximum=4096)
    result = []
    for raw in outer:
        row = tuple(integer(i, 'variable index', 0) for i in sequence(raw, 'constraint', width))
        if any(i >= size for i in row):
            raise Violation('input', 'constraint index outside the carrier')
        if len(set(row)) != width:
            raise Violation('duplicate', 'constraint variables must be distinct')
        result.append(tuple(sorted(row)))
    if len(set(result)) != len(result):
        raise Violation('duplicate', 'constraint rows must be distinct up to ordering')
    return tuple(result)


def _assignment(value: object, size: int) -> Assignment:
    values = tuple(integer(i, 'binary value', 0) for i in sequence(value, 'assignment', size, 64))
    if any(i > 1 for i in values):
        raise Violation('input', 'binary assignment values must be0 or1')
    return values


@dataclass(frozen=True, slots=True, init=False)
class BinaryFrameSystem:
    """Immutable indexed constraints; all returned assignment vectors are detached."""
    size: int
    pairs: tuple[Constraint, ...]
    triples: tuple[Constraint, ...]
    neighbours: tuple[tuple[int, ...], ...]

    def __init__(self, size: object, pairs: object, triples: object) -> None:
        count = integer(size, 'binary carrier size', 0, 64)
        owned_pairs = _constraints(pairs, 2, count)
        owned_triples = _constraints(triples, 3, count)
        neighbours: list[list[int]] = [[] for _ in range(count)]
        for i, j in owned_pairs:
            neighbours[i].append(j)
            neighbours[j].append(i)
        object.__setattr__(self, 'size', count)
        object.__setattr__(self, 'pairs', owned_pairs)
        object.__setattr__(self, 'triples', owned_triples)
        object.__setattr__(self, 'neighbours', tuple(tuple(sorted(row)) for row in neighbours))

    def _check_assignment(self, value: object) -> bool:
        values = _assignment(value, self.size)
        return (all(values[i]+values[j] <= 1 for i, j in self.pairs)
                and all(sum(values[i] for i in row) == 1 for row in self.triples))

    def check_assignment(self, value: object) -> Outcome[bool]:
        return evaluate(self._check_assignment, value)

    def _pair_propagation(self, values: list[int]) -> bool:
        for i, j in self.pairs:
            if values[i] == values[j] == 1:
                return False
            if values[i] == 1 and values[j] == -1:
                values[j] = 0
            if values[j] == 1 and values[i] == -1:
                values[i] = 0
        return True

    def _triple_propagation(self, values: list[int]) -> bool:
        for row in self.triples:
            ones = sum(values[i] == 1 for i in row)
            missing = tuple(i for i in row if values[i] == -1)
            if ones > 1 or (not missing and ones != 1):
                return False
            if ones == 1 or len(missing) == 1:
                for i in missing:
                    values[i] = 1-ones
        return True

    def _propagate(self, values: list[int]) -> bool:
        while True:
            before = values.count(-1)
            if not self._pair_propagation(values) or not self._triple_propagation(values):
                return False
            if values.count(-1) == before:
                return True

    def _search(self, max_nodes: object) -> SearchResult:
        limit = integer(max_nodes, 'search node budget', 1, 65536)
        stack = [[-1] * self.size]
        nodes = 0
        while stack:
            if nodes == limit:
                raise Violation('resource', 'binary search node budget exhausted')
            values = stack.pop()
            nodes += 1
            if not self._propagate(values):
                continue
            if -1 not in values:
                require(self._check_assignment(values), 'search returned an invalid binary model')
                return tuple(values), nodes
            variable = max((i for i in range(self.size) if values[i] == -1),
                           key=lambda i: len(self.neighbours[i]))
            for value in (1, 0):
                branch = values.copy()
                branch[variable] = value
                stack.append(branch)
        return None, nodes

    def search(self, max_nodes: object = 16384) -> Outcome[SearchResult]:
        return evaluate(self._search, max_nodes)
