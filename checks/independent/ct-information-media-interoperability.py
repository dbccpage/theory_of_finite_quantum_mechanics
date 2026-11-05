"""Bounded finite information-task algebra and interoperability controls.

AuthorityEffect: None. A task is a supplied total function on a finite product
of label sets. Cloning here is a predicate on its blank-input slice, not a
physical implementation or a claim that every functional task is possible.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import permutations, product
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checker_support.boundary import cli, evaluate, require as ensure, Violation
from checker_support.cases import Cases
from checker_support.domains import integer, sequence
from checker_support.outcome import Outcome

Point = tuple[int, int]
Factors = tuple[tuple[int, ...], tuple[int, ...]]


@dataclass(frozen=True, slots=True, init=False)
class FiniteProductTask:
    """Owned endofunction on [0,left_size) x [0,right_size), each size1..64.

    The row-major table is total and has <=4096 entries. Images stay in the
    same carrier; a task need not be injective or factor into local functions.
    """

    left_size: int
    right_size: int
    outputs: tuple[Point, ...]

    def __init__(self, left_size: object, right_size: object, outputs: object) -> None:
        left = integer(left_size, "left carrier size", 1, 64)
        right = integer(right_size, "right carrier size", 1, 64)
        table = []
        for value in sequence(outputs, "total task table", left*right):
            a, b = sequence(value, "task output", 2)
            table.append((integer(a, "left output", 0, left-1), integer(b, "right output", 0, right-1)))
        object.__setattr__(self, "left_size", left)
        object.__setattr__(self, "right_size", right)
        object.__setattr__(self, "outputs", tuple(table))

    def _at(self, point: Point) -> Point:
        """Internal lookup for already admitted carrier points."""
        return self.outputs[point[0]*self.right_size+point[1]]

    def _apply(self, point: object) -> Point:
        a, b = sequence(point, "task input", 2)
        return self._at((integer(a, "left input", 0, self.left_size-1),
                         integer(b, "right input", 0, self.right_size-1)))

    def apply(self, point: object) -> Outcome[Point]:
        return evaluate(self._apply, point)

    def is_reversible(self) -> bool:
        return len(set(self.outputs)) == len(self.outputs)

    def local_factors(self) -> Factors | None:
        """Return the two component functions exactly when the table is local."""
        left = tuple(self._at((a, 0))[0] for a in range(self.left_size))
        right = tuple(self._at((0, b))[1] for b in range(self.right_size))
        if any(self._at((a, b)) != (left[a], right[b])
               for a, b in product(range(self.left_size), range(self.right_size))):
            return None
        return left, right

    @staticmethod
    def _other(value: object) -> FiniteProductTask:
        if type(value) is not FiniteProductTask:
            raise Violation("input", "task operation requires a FiniteProductTask")
        return value

    def _compose(self, other: object) -> FiniteProductTask:
        prior = self._other(other)
        if (self.left_size, self.right_size) != (prior.left_size, prior.right_size):
            raise Violation("input", "task composition carriers differ")
        return FiniteProductTask(self.left_size, self.right_size, tuple(self._at(point) for point in prior.outputs))

    def compose(self, other: object) -> Outcome[FiniteProductTask]:
        """self after other: returned task applies other first, then self."""
        return evaluate(self._compose, other)

    def _inverse(self) -> FiniteProductTask:
        if not self.is_reversible():
            raise Violation("check", "nonbijective task has no inverse")
        inverse = [(0, 0)]*len(self.outputs)
        for index, (a, b) in enumerate(self.outputs):
            inverse[a*self.right_size+b] = divmod(index, self.right_size)
        return FiniteProductTask(self.left_size, self.right_size, inverse)

    def inverse(self) -> Outcome[FiniteProductTask]:
        return evaluate(self._inverse)

    def _parallel(self, other: object) -> FiniteProductTask:
        rhs = self._other(other)
        left = integer(self.left_size*rhs.left_size, "product left size", 1, 64)
        right = integer(self.right_size*rhs.right_size, "product right size", 1, 64)
        table = []
        for a, b in product(range(left), range(right)):
            own = self._at((a//rhs.left_size, b//rhs.right_size))
            theirs = rhs._at((a % rhs.left_size, b % rhs.right_size))
            table.append((own[0]*rhs.left_size+theirs[0], own[1]*rhs.right_size+theirs[1]))
        return FiniteProductTask(left, right, table)

    def parallel(self, other: object) -> Outcome[FiniteProductTask]:
        """Regroup paired inputs as (A x B) x (A' x B') using row-major labels."""
        return evaluate(self._parallel, other)

    def _clones(self, blank: object) -> bool:
        if self.left_size != self.right_size:
            raise Violation("input", "cloning predicate requires equal carrier sizes")
        admitted = integer(blank, "blank label", 0, self.right_size-1)
        return all(self._at((label, admitted)) == (label, label) for label in range(self.left_size))

    def clones(self, blank: object) -> Outcome[bool]:
        return evaluate(self._clones, blank)


def controlled(point: object) -> Point:
    a, b = sequence(point, "binary pair", 2)
    left, right = integer(a, "left bit", 0, 1), integer(b, "right bit", 0, 1)
    return left ^ right, right


def check_controlled_permutation(cases: Cases) -> None:
    states = tuple(product(range(2), repeat=2))
    task = FiniteProductTask(2, 2, tuple(controlled(point) for point in states))
    doubled, inverse = task.compose(task), task.inverse()
    cases.append(("controlled.involution", all(controlled(controlled(point)) == point for point in states)
                  and doubled.ok and doubled.value == FiniteProductTask(2, 2, states)
                  and inverse.ok and inverse.value == task))
    cases.append(("controlled.permutation", task.is_reversible()))
    local = {tuple((f[a], g[b]) for a, b in states) for f, g in product(permutations(range(2)), repeat=2)}
    cases.append(("controlled.local_products", len(local) == 4
                  and all(FiniteProductTask(2, 2, table).local_factors() is not None for table in local)))
    cases.append(("controlled.nonlocal", task.outputs not in local and task.local_factors() is None))
    cases.append(("controlled.composite_permutations", len(tuple(permutations(states))) == 24))


def check_product_cloning(cases: Cases) -> None:
    first = FiniteProductTask(4, 4, tuple((a, a) for a, _ in product(range(4), repeat=2)))
    second = FiniteProductTask(3, 3, tuple((b, b) for b, _ in product(range(3), repeat=2)))
    combined = first.parallel(second)
    if combined.error is not None:
        raise Violation(combined.error.kind, combined.error.message)
    task = combined.value
    if task is None:
        raise Violation("check", "parallel construction returned no task")
    predicates = first.clones(0), second.clones(0), task.clones(0)
    cases.append(("cloning.blank_slices", all(result.ok and result.value is True for result in predicates)))
    for a, b in product(range(4), range(3)):
        label = a*3+b
        result = task.apply((label, 0))
        cases.append((f"cloning.{a}.{b}", result.ok and result.value == (label, label)))


def run_checks() -> dict[str, object]:
    cases = Cases()
    check_controlled_permutation(cases)
    check_product_cloning(cases)
    failures = [name for name, passed in cases if not passed]
    return {"scope": "finite functional information tasks", "authority_effect": "None",
            "total_checks": len(cases), "failures": failures, "failed_checks": len(failures), "all_passed": not failures}


def main() -> int:
    result = run_checks()
    ensure(result["all_passed"] is True, "finite information-task controls failed: "+str(result["failures"]))
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(cli(main))
