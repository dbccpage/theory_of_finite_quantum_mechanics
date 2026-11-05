"""Exact finite binary-colouring obstruction on all rational and Gaussian rays.

AuthorityEffect: None. Fixed radius-two primitive real rays supply49 variables,
138 orthogonal-pair inequalities and26 internal normalized frame equations.
Pair inequalities use actual cross-product completions, possibly outside the
box. Shared bounded search is independent of production models and solvers.
This does not classify arbitrary signed or nonnegative frame functions.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations, product
import json
from math import gcd
from pathlib import Path
import sys
from typing import cast

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checker_support.binary_frame_system import BinaryFrameSystem
from checker_support.boundary import cli, evaluate, require
from checker_support.outcome import Outcome

Vector = tuple[int, int, int]


def _dot(u: Vector, v: Vector) -> int:
    return u[0]*v[0] + u[1]*v[1] + u[2]*v[2]


def _cross(u: Vector, v: Vector) -> Vector:
    return (u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0])


def _rays() -> tuple[Vector, ...]:
    return tuple(cast(Vector, v) for v in product(range(-2, 3), repeat=3)
                 if gcd(*v) == 1 and next(x for x in v if x) > 0)


def _constraints(rays: tuple[Vector, ...]) -> BinaryFrameSystem:
    pairs = tuple((i, j) for i, j in combinations(range(len(rays)), 2) if _dot(rays[i], rays[j]) == 0)
    edges = set(pairs)
    triples = tuple((i, j, k) for i, j, k in combinations(range(len(rays)), 3)
                    if {(i, j), (i, k), (j, k)} <= edges)
    return BinaryFrameSystem(len(rays), pairs, triples)


def _small_controls() -> None:
    for size in (3, 4):
        system = BinaryFrameSystem(size, tuple(combinations(range(size), 2)),
                                   tuple(combinations(range(size), 3)))
        # Direct enumeration is independent of propagation and branching.
        exact = any(system._check_assignment(v) for v in product((0, 1), repeat=size))
        require(exact == (size == 3), 'unexpected exhaustive control result')
        found, _ = system._search(16384)
        require((found is not None) == exact, 'exhaustive solver control failed')


@dataclass(frozen=True, slots=True, init=False)
class RationalColouringWitness:
    """Owns the fixed finite geometric witness and its binary constraint system."""
    rays: tuple[Vector, ...]
    system: BinaryFrameSystem

    def __init__(self) -> None:
        rays = _rays()
        object.__setattr__(self, 'rays', rays)
        object.__setattr__(self, 'system', _constraints(rays))

    def _completions(self) -> int:
        outside = 0
        for i, j in self.system.pairs:
            u, v = self.rays[i], self.rays[j]
            w = _cross(u, v)
            require(w != (0, 0, 0), 'degenerate completion')
            require(_dot(u, v) == _dot(u, w) == _dot(v, w) == 0, 'nonorthogonal completion')
            outside += int(max(map(abs, w)) > 2)
        return outside

    def _controls(self) -> None:
        systems = (BinaryFrameSystem(self.system.size, (), self.system.triples),
                   BinaryFrameSystem(self.system.size, self.system.pairs, ()))
        for system in systems:
            assignment, _ = system._search(16384)
            require(assignment is not None, 'constraint-deletion control must be SAT')
            require(system._check_assignment(assignment), 'invalid constraint-deletion model')
        _small_controls()

    def _verify(self) -> dict[str, object]:
        require((len(self.rays), len(self.system.pairs), len(self.system.triples)) == (49, 138, 26),
                'unexpected witness census')
        outside = self._completions()
        assignment, nodes = self.system._search(16384)
        require(assignment is None, 'obstruction unexpectedly has a binary colouring')
        self._controls()
        return {'status': 'PASS', 'authority_effect': 'None',
                'claim': 'No {0,1}-valued frame function on all Q^3 or Q(i)^3 rays',
                'rays': len(self.rays), 'orthogonal_pairs': len(self.system.pairs),
                'internal_frames': len(self.system.triples), 'completed_pairs': len(self.system.pairs),
                'raw_cross_products_outside_box': outside, 'binary_search_nodes': nodes,
                'controls': ['triples-only SAT', 'pairs-only SAT', 'exhaustive small instances'],
                'not_established': ['signed rigidity', 'nonnegative rigidity', 'exotic extension']}

    def verify(self) -> Outcome[dict[str, object]]:
        return evaluate(self._verify)


def verify() -> Outcome[dict[str, object]]:
    return evaluate(RationalColouringWitness).bind(lambda witness: witness.verify())


def _main() -> None:
    result = RationalColouringWitness()._verify()
    print(json.dumps(result, indent=2))


def main() -> int:
    return cli(_main)


if __name__ == '__main__':
    raise SystemExit(main())
