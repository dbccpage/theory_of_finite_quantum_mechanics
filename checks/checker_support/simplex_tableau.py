"""Private bounded two-phase simplex workspace; answers require independent replay.

AuthorityEffect: None. Bland entering/leaving choices, at most4096 pivots and
32x97 tableau entries. No mutable state escapes through the certificate.
"""
from __future__ import annotations

from fractions import Fraction as Q

from .boundary import Violation
from .domains import integer, rational
from .exact_linear_program import ExactLinearProgram, dot
from .linear_program_certificate import LinearProgramCertificate, Vector


class SimplexTableau:
    """Per-solve workspace owned by ExactLinearProgram; not a mutable domain model."""

    def __init__(self, program: object, pivot_limit: object) -> None:
        if type(program) is not ExactLinearProgram:
            raise Violation("input", "exact LP required")
        self.limit = integer(pivot_limit, "LP pivot budget", 0, 4096)
        self.program = program
        self.m, self.n = program.dimensions
        self.width = self.n+self.m
        self.table = [list(row)+[Q(int(i == j)) for j in range(self.m)]+[rhs]
                      for i, (row, rhs) in enumerate(zip(program.coefficients, program.target))]
        self.basis = [self.n+i for i in range(self.m)]
        self.pivots = 0

    def _pivot(self, row: int, column: int) -> None:
        if self.pivots >= self.limit:
            raise Violation("resource", "LP pivot budget exhausted")
        pivot = self.table[row][column]
        if pivot == 0:
            raise Violation("check", "zero simplex pivot")
        normalized = [rational(value/pivot, "pivot quotient") for value in self.table[row]]
        updated = [self._eliminate(values, normalized, column) if i != row else normalized
                   for i, values in enumerate(self.table)]
        self.table = updated
        self.basis[row] = column
        self.pivots += 1

    @staticmethod
    def _eliminate(values: list[Q], normalized: list[Q], column: int) -> list[Q]:
        factor = values[column]
        return [rational(value-rational(factor*entry, "pivot product"), "pivot subtraction")
                for value, entry in zip(values, normalized)]

    def _reduced(self, costs: Vector) -> Vector:
        basic_costs = tuple(costs[index] for index in self.basis)
        columns = tuple(zip(*self.table))
        return tuple(rational(costs[j]-dot(basic_costs, columns[j]), "reduced cost") for j in range(self.width))

    def _run(self, costs: Vector, allowed: int) -> int | None:
        while True:
            reduced = self._reduced(costs)
            enter = next((j for j in range(allowed) if reduced[j] < 0), None)
            if enter is None:
                return None
            rows = [(rational(values[-1]/values[enter], "pivot ratio"), self.basis[i], i)
                    for i, values in enumerate(self.table) if values[enter] > 0]
            if not rows:
                return enter
            self._pivot(min(rows)[2], enter)

    def _dual(self, costs: Vector) -> Vector:
        return tuple(-value for value in self._reduced(costs)[self.n:])

    def _primal(self) -> Vector:
        values = [Q(0)]*self.n
        for index, row in zip(self.basis, self.table):
            if index < self.n:
                values[index] = row[-1]
        return tuple(values)

    def _ray(self, enter: int) -> Vector:
        values = [Q(0)]*self.n
        values[enter] = Q(1)
        for index, row in zip(self.basis, self.table):
            if index < self.n:
                values[index] = -row[enter]
        return tuple(values)

    def _remove_artificial_basis(self) -> None:
        for row, index in enumerate(self.basis):
            if index >= self.n:
                column = next((j for j in range(self.n) if self.table[row][j] != 0), None)
                if column is not None:
                    self._pivot(row, column)

    def solve(self) -> LinearProgramCertificate:
        phase_one = (Q(0),)*self.n+(Q(1),)*self.m
        if self._run(phase_one, self.width) is not None:
            raise Violation("check", "nonnegative auxiliary objective cannot be unbounded")
        residual = dot(tuple(phase_one[j] for j in self.basis), tuple(row[-1] for row in self.table))
        if residual > 0:
            # Auxiliary dual has y*A<=0, b*y>0: its original-variable costs are zero.
            dual = tuple(Q(1)-value for value in self._reduced(phase_one)[self.n:])
            return LinearProgramCertificate("infeasible", dual=dual)
        if residual < 0:
            raise Violation("check", "negative auxiliary objective violates feasibility")
        self._remove_artificial_basis()
        costs = self.program.objective+(Q(0),)*self.m
        enter = self._run(costs, self.n)
        if enter is not None:
            return LinearProgramCertificate("unbounded", primal=self._primal(), ray=self._ray(enter))
        return LinearProgramCertificate("optimal", primal=self._primal(), dual=self._dual(costs))
