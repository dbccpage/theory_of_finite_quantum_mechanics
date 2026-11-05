"""Bounded equality LP aggregate with independent certificate replay.

Minimize c*x subject to A*x=b, x>=0 and b>=0. At most32 equations and64
variables; every exact component and arithmetic intermediate has4096 bits.
AuthorityEffect: None. Search exhaustion is a resource refusal, not infeasibility.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as Q

from .boundary import Violation, evaluate, require
from .domains import integer, rational, sequence
from .linear_program_certificate import LinearProgramCertificate, Vector
from .outcome import Outcome

Rows = tuple[Vector, ...]


def dot(left: Vector, right: Vector) -> Q:
    """Internal admitted vectors of equal length; every term and prefix bounded."""
    total = Q(0)
    for a, b in zip(left, right):
        total = rational(total+rational(a*b, "LP product"), "LP sum")
    return total


def vector(value: object, size: int, maximum: int) -> Vector:
    return tuple(rational(item, "LP entry") for item in sequence(value, "LP vector", size, maximum))


@dataclass(frozen=True, slots=True, init=False)
class ExactLinearProgram:
    """Owns a nonempty equality system; all solve outcomes carry replayable witnesses."""
    objective: Vector
    coefficients: Rows
    target: Vector

    def __init__(self, objective: object, coefficients: object, target: object) -> None:
        cost = sequence(objective, "LP objective", maximum=64)
        rows = sequence(coefficients, "LP rows", maximum=32)
        if not cost or not rows:
            raise Violation("input", "LP objective and rows must be nonempty")
        owned_cost = vector(cost, len(cost), 64)
        owned_rows = tuple(vector(row, len(cost), 64) for row in rows)
        owned_target = vector(target, len(rows), 32)
        if any(value < 0 for value in owned_target):
            raise Violation("input", "LP right-hand side must be nonnegative")
        object.__setattr__(self, "objective", owned_cost)
        object.__setattr__(self, "coefficients", owned_rows)
        object.__setattr__(self, "target", owned_target)

    @property
    def dimensions(self) -> tuple[int, int]:
        return len(self.target), len(self.objective)

    def _primal(self, value: Vector) -> None:
        if len(value) != len(self.objective):
            raise Violation("input", "primal dimension does not match LP")
        require(all(entry >= 0 for entry in value), "LP primal must be nonnegative")
        require(all(dot(row, value) == rhs for row, rhs in zip(self.coefficients, self.target)), "LP primal equalities fail")

    def _dual_columns(self, value: Vector) -> Vector:
        if len(value) != len(self.target):
            raise Violation("input", "dual dimension does not match LP")
        return tuple(dot(value, column) for column in zip(*self.coefficients))

    def _verify_optimal(self, certificate: LinearProgramCertificate) -> Q:
        self._primal(certificate.primal)
        columns = self._dual_columns(certificate.dual)
        require(all(value <= cost for value, cost in zip(columns, self.objective)), "LP dual inequalities fail")
        value = dot(self.objective, certificate.primal)
        require(value == dot(self.target, certificate.dual), "LP objectives have a nonzero gap")
        return value

    def _verify_infeasible(self, certificate: LinearProgramCertificate) -> None:
        require(all(value <= 0 for value in self._dual_columns(certificate.dual)), "Farkas dual inequalities fail")
        require(dot(self.target, certificate.dual) > 0, "Farkas separating objective must be positive")

    def _verify_unbounded(self, certificate: LinearProgramCertificate) -> None:
        self._primal(certificate.primal)
        if len(certificate.ray) != len(self.objective):
            raise Violation("input", "ray dimension does not match LP")
        require(all(value >= 0 for value in certificate.ray), "unbounded ray must be nonnegative")
        require(all(dot(row, certificate.ray) == 0 for row in self.coefficients), "unbounded ray leaves equality kernel")
        require(dot(self.objective, certificate.ray) < 0, "unbounded ray must strictly reduce objective")

    def _verify(self, certificate: object) -> Q | None:
        if type(certificate) is not LinearProgramCertificate:
            raise Violation("input", "LP certificate required")
        if certificate.status == "optimal":
            return self._verify_optimal(certificate)
        if certificate.status == "infeasible":
            self._verify_infeasible(certificate)
        else:
            self._verify_unbounded(certificate)
        return None

    def verify(self, certificate: object) -> Outcome[Q | None]:
        return evaluate(self._verify, certificate)

    def _solve(self, pivot_limit: object) -> LinearProgramCertificate:
        from .simplex_tableau import SimplexTableau
        limit = integer(pivot_limit, "LP pivot budget", 0, 4096)
        certificate = SimplexTableau(self, limit).solve()
        self._verify(certificate)
        return certificate

    def solve(self, pivot_limit: object = 4096) -> Outcome[LinearProgramCertificate]:
        return evaluate(self._solve, pivot_limit)
