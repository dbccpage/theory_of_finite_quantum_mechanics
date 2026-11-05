"""Exact diagonal vertex-sign switching audit. AuthorityEffect: None."""
from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checker_support.boundary import cli, evaluate
from checker_support.cases import Cases
from checker_support.domains import sequence
from checker_support.outcome import Outcome
from checker_support.rational_matrix import RationalMatrix
from checker_support.signed_triangle import SignedTriangle

Rows = tuple[tuple[int, ...], ...]


def _matrix(value: object) -> RationalMatrix:
    rows = sequence(value, "3x3 matrix", 3, 3)
    snapshot = tuple(sequence(row, "matrix row", 3, 3) for row in rows)
    return RationalMatrix.from_integers(snapshot)


def multiply(first: object, second: object) -> Rows:
    """Compatibility entry point for bounded native integer 3x3 matrices."""
    left, right = _matrix(first), _matrix(second)
    return left.mul(right).integer_rows()


@dataclass(frozen=True, slots=True, init=False)
class TriangleSwitchingControls:
    """Owns the complete eight-triangle family for the finite audit."""
    triangles: tuple[SignedTriangle, ...]

    def __init__(self) -> None:
        triangles = tuple(SignedTriangle(edges) for edges in product((-1, 1), repeat=3))
        object.__setattr__(self, "triangles", triangles)

    @staticmethod
    def matrix_product(first: object, second: object) -> Outcome[Rows]:
        return evaluate(multiply, first, second)

    def _verify(self) -> dict[str, int]:
        cases = Cases()
        balanced = 0
        switching_cases = 0
        for triangle in self.triangles:
            adjacency = triangle.adjacency.integer_rows()
            cycle = triangle.cycle_product
            can_be_positive = False
            for gauge in product((-1, 1), repeat=3):
                diagonal = tuple(tuple(gauge[i] if i == j else 0 for j in range(3)) for i in range(3))
                transformed = multiply(multiply(diagonal, adjacency), diagonal)
                switched = triangle._switch(gauge)
                cases.require(transformed == switched.adjacency.integer_rows(), "matrix and edge switching agree")
                edges = transformed[0][1], transformed[1][2], transformed[2][0]
                cases.require(edges[0]*edges[1]*edges[2] == cycle, "cycle invariant")
                can_be_positive |= edges == (1, 1, 1)
                if gauge == triangle.normalizing_gauge:
                    cases.require(edges == (1, 1, cycle), "constructive normal form")
                switching_cases += 1
            cases.require(can_be_positive == (cycle == 1), "switching classification")
            balanced += can_be_positive
        cases.require(balanced == 4 and switching_cases == 64, "finite family population")
        return {"triangles": len(self.triangles), "switching_cases": switching_cases,
                "balanced": balanced, "obstructed": len(self.triangles)-balanced,
                "failures": 0, "checks": cases.checks}

    def verify(self) -> Outcome[dict[str, int]]:
        return evaluate(self._verify)


def _main() -> None:
    result = TriangleSwitchingControls()._verify()
    print(f"triangles={result['triangles']} switching_cases={result['switching_cases']} "
          f"balanced={result['balanced']} obstructed={result['obstructed']} failures={result['failures']}")


def main() -> int:
    return cli(_main)


if __name__ == "__main__":
    raise SystemExit(main())
