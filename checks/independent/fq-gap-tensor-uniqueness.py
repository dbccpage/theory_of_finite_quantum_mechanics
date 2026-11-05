"""Exact bounded integer outer-product controls. AuthorityEffect: None.

The integer identities correspond to TensorUniquenessOuterProducts.lean.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import product
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checker_support.boundary import cli, evaluate
from checker_support.cases import Cases
from checker_support.domains import integer, integer_matrix, rational, sequence
from checker_support.outcome import Outcome
from checker_support.rational_matrix import RationalMatrix


def _matrix(value: object) -> RationalMatrix:
    return RationalMatrix(integer_matrix(value, rows=2, cols=2))


def det(value: object) -> int:
    """Compatibility query. Invalid inputs raise the shared typed Violation."""
    return _matrix(value).det2().numerator


def rank(value: object) -> int:
    """Independent rational elimination, bounding each stored intermediate."""
    rows = [list(row) for row in _matrix(value).rows]
    pivot_row = 0
    for col in range(2):
        candidate = next((r for r in range(pivot_row, 2) if rows[r][col]), None)
        if candidate is None:
            continue
        rows[candidate], rows[pivot_row] = rows[pivot_row], rows[candidate]
        pivot = rows[pivot_row][col]
        rows[pivot_row] = [rational(x/pivot, "elimination quotient") for x in rows[pivot_row]]
        other = 1-pivot_row
        factor = rows[other][col]
        rows[other] = [rational(x-rational(factor*y, "elimination product"), "elimination difference")
                       for x, y in zip(rows[other], rows[pivot_row])]
        pivot_row += 1
    return pivot_row


@dataclass(frozen=True, slots=True, init=False)
class TensorOuterProductControls:
    """Owns a census radius in 0..5. Matrix arithmetic has 4096-bit bounds."""
    radius: int

    def __init__(self, radius: object = 3) -> None:
        object.__setattr__(self, "radius", integer(radius, "census radius", 0, 5))

    @staticmethod
    def determinant(value: object) -> Outcome[int]:
        return evaluate(det, value)

    @staticmethod
    def matrix_rank(value: object) -> Outcome[int]:
        return evaluate(rank, value)

    @staticmethod
    def _outer(value: object) -> RationalMatrix:
        a, b, c, d = (rational(integer(x), "vector coordinate")
                      for x in sequence(value, "two integer vectors", 4))
        return RationalMatrix(((rational(a*c), rational(a*d)), (rational(b*c), rational(b*d))))

    @staticmethod
    def outer_product(value: object) -> Outcome[RationalMatrix]:
        return evaluate(TensorOuterProductControls._outer, value)

    def _verify(self) -> dict[str, object]:
        cases = Cases()
        identity = ((1, 0), (0, 1))
        inputs = list(product(range(-self.radius, self.radius+1), repeat=4))
        inputs.extend([(10**50, -17, 10**40, 23), (0, 0, 0, 0)])
        for coordinates in inputs:
            matrix = self._outer(coordinates).integer_rows()
            cases.require(det(matrix) == 0, "outer determinant")
            cases.require(rank(matrix) <= 1, "independent elimination")
            cases.require(matrix != identity, "identity is not an outer product")
        cases.require(det(identity) == 1 and rank(identity) == 2, "identity negative control")
        changed = ((11, 14), (15, 21))
        cases.require(det(changed) != 0 and rank(changed) == 2, "altered outer-product entry")
        ones = ((1, 1), (1, 1))
        cases.require(2 != det(ones), "wrong determinant sign rejected")
        return {"checks": cases.checks, "failed": 0, "input_vectors": len(inputs),
                "negative_controls": 3, "identity_det": det(identity),
                "scope": "Exact finite census with independent elimination; the universal integer identity is separately Lean checked."}

    def verify(self) -> Outcome[dict[str, object]]:
        return evaluate(self._verify)


def _main() -> None:
    print(json.dumps(TensorOuterProductControls()._verify()))


def main() -> int:
    return cli(_main)


if __name__ == "__main__":
    raise SystemExit(main())
