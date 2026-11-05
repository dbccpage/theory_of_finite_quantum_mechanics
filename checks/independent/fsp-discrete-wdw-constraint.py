"""Declared diagonal constraint and kernel-projector audit. AuthorityEffect: None."""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import sys
import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from checker_support.boundary import Violation, cli, evaluate
from checker_support.cases import Cases
from checker_support.diagonal_constraint import DiagonalConstraint
from checker_support.domains import integer
from checker_support.outcome import Outcome


@dataclass(frozen=True, slots=True, init=False)
class ConstraintKernelControls:
    """Owns the candidate diagonal operator and a census radius in 0..4."""
    constraint: DiagonalConstraint
    radius: int

    def __init__(self, constraint: object = None, radius: object = 2) -> None:
        admitted_radius = integer(radius, "constraint census radius", 0, 4)
        candidate = DiagonalConstraint((0, 2, -1)) if constraint is None else constraint
        if type(candidate) is not DiagonalConstraint:
            raise Violation("input", "candidate requires an admitted diagonal constraint")
        object.__setattr__(self, "constraint", candidate)
        object.__setattr__(self, "radius", admitted_radius)

    def _verify(self) -> dict[str, object]:
        cases = Cases()
        constraint = sp.ImmutableMatrix(self.constraint.matrix.rows)
        projector = sp.ImmutableMatrix(self.constraint.kernel_projector.rows)
        basis = [sp.eye(3)[:, i] for i in range(3)]
        cases.require(constraint.T == constraint, "constraint symmetry")
        cases.require(constraint.nullspace() == [basis[0]], "declared kernel")
        cases.require(constraint.eigenvals() == {0: 1, 2: 1, -1: 1}, "exact spectrum")
        cases.require(dict(self.constraint.spectrum) == {Q(0): 1, Q(2): 1, Q(-1): 1}, "API spectrum")
        cases.require(projector*projector == projector, "projector idempotence")
        cases.require(constraint*projector == sp.zeros(3), "projector image lies in kernel")
        cases.require(constraint*constraint != constraint, "constraint is not idempotent")
        cases.require(not self.constraint.is_projector, "API nonprojector")
        cases.require(self.constraint.kernel_basis == ((Q(1), Q(0), Q(0)),), "API kernel basis")
        cases.require(self.constraint.rank == 2 and self.constraint.kernel_dimension == 1, "API rank and nullity")
        x, y, z, t = sp.symbols("x y z t")
        vector = sp.Matrix((x, y, z))
        kernel_vector = sp.Matrix((t, 0, 0))
        cases.require(((vector-projector*vector).T*kernel_vector)[0] == 0, "symbolic residual orthogonality")
        vectors = 0
        for values in product(range(-self.radius, self.radius+1), repeat=3):
            vector = sp.Matrix(values)
            weighted = constraint*vector
            projected = projector*vector
            in_kernel = weighted == sp.zeros(3, 1)
            cases.require(in_kernel == (values[1] == 0 and values[2] == 0), "kernel coordinates")
            cases.require((projected == vector) == in_kernel, "projector fixed points")
            cases.require(self.constraint._contains(values) == in_kernel, "API kernel membership")
            cases.require(self.constraint._apply(values) == tuple(weighted), "API operator application")
            cases.require(self.constraint._project(values) == tuple(projected), "API projection")
            vectors += 1
        positive = self.constraint._quadratic((0, 1, 0))
        negative = self.constraint._quadratic((0, 0, 1))
        cases.require(positive == 2 and negative == -1, "indefinite quadratic witnesses")
        cases.require(self.constraint.is_indefinite and not self.constraint.is_positive_semidefinite, "API indefinite classification")
        return {"vectors": vectors, "rank": self.constraint.rank,
                "kernel_dimension": self.constraint.kernel_dimension, "positive": positive, "negative": negative,
                "nonprojector": not self.constraint.is_projector, "failures": 0, "checks": cases.checks}

    def verify(self) -> Outcome[dict[str, object]]:
        return evaluate(self._verify)


def _main() -> None:
    result = ConstraintKernelControls()._verify()
    print(f"vectors={result['vectors']} rank={result['rank']} kernel_dimension={result['kernel_dimension']} "
          f"quadratic_values=({result['positive']},{result['negative']}) "
          f"nonprojector={result['nonprojector']} failures={result['failures']}")


def main() -> int:
    return cli(_main)


if __name__ == "__main__":
    raise SystemExit(main())
