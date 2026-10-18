"""Exact affine-scalar minimax solver for the PO-014 fixed-witness rail.

The canonical problem is one shared optimization

    inf_z max_w |weight_w * (offset_w + coefficients_w . z)|.

All canonical arithmetic is rational.  The optional NumPy least-squares
routine is returned in a distinct ``SURROGATE_ONLY`` type and cannot mint a
canonical or certified status.

AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations, product
from typing import ClassVar

import numpy as np
from sympy import Abs, Matrix, Rational, simplify

from omega_engine.crates.linear_algebra_theory.exact import (
    ExactInput,
    as_rational,
)


class PO014MinimaxRefused(ValueError):
    """The fixed-witness exact minimax contract was not supplied."""


@dataclass(frozen=True, order=True)
class PO014WitnessIndex:
    """The sole witness-index schema used by inputs and exact receipts."""

    value: str

    def __post_init__(self) -> None:
        if not isinstance(self.value, str) or not self.value.strip():
            raise PO014MinimaxRefused("witness indices must be non-empty strings")


@dataclass(frozen=True)
class PO014AffineWitness:
    """One weighted affine scalar residual, indexed before optimization."""

    index: PO014WitnessIndex | str
    coefficients: tuple[ExactInput, ...]
    offset: ExactInput
    weight: ExactInput = 1

    def __post_init__(self) -> None:
        index = self.index if isinstance(self.index, PO014WitnessIndex) else PO014WitnessIndex(self.index)
        coefficients = tuple(as_rational(value) for value in self.coefficients)
        offset = as_rational(self.offset)
        weight = as_rational(self.weight)
        if weight <= 0:
            raise PO014MinimaxRefused("PO-014 witness weights must be strictly positive")
        object.__setattr__(self, "index", index)
        object.__setattr__(self, "coefficients", coefficients)
        object.__setattr__(self, "offset", offset)
        object.__setattr__(self, "weight", weight)

    def weighted_residual(self, z: tuple[Rational, ...]) -> Rational:
        if len(z) != len(self.coefficients):
            raise ValueError("optimizer dimension does not match affine witness")
        return simplify(
            self.weight
            * (self.offset + sum(a * value for a, value in zip(self.coefficients, z, strict=True)))
        )


@dataclass(frozen=True)
class PO014IndexedScalar:
    """An exact scalar keyed by the common PO-014 witness-index schema."""

    index: PO014WitnessIndex
    value: Rational


@dataclass(frozen=True)
class PO014MinimaxReceipt:
    """Replayable exact finite receipt for one fixed witness family."""

    z_star: tuple[Rational, ...]
    residuals: tuple[PO014IndexedScalar, ...]
    active_witnesses: tuple[PO014WitnessIndex, ...]
    t_star: Rational
    dual_lower_bound_witness: tuple[PO014IndexedScalar, ...]
    dual_lower_bound: Rational
    exact_gap: Rational
    witness_indices: tuple[PO014WitnessIndex, ...]
    status: ClassVar[str] = "CANONICAL_EXACT_COMPUTATIONAL_RECEIPT"
    authority_effect: str = "None"

    @property
    def optimizer(self) -> tuple[Rational, ...]:
        return self.z_star

    @property
    def residual_by_index(self) -> dict[PO014WitnessIndex, Rational]:
        return {entry.index: entry.value for entry in self.residuals}

    @property
    def dual_by_index(self) -> dict[PO014WitnessIndex, Rational]:
        return {entry.index: entry.value for entry in self.dual_lower_bound_witness}

    @property
    def is_certified(self) -> bool:
        """This flag means only that the finite rational receipt replayed."""

        return self.exact_gap == 0 and self.t_star == self.dual_lower_bound

    def verify(self, problem: "PO014MinimaxProblem") -> bool:
        return verify_po014_minimax_receipt(problem, self)


@dataclass(frozen=True)
class PO014LeastSquaresSurrogateResult:
    """Numerical least-squares diagnostic; never a canonical PO-014 result."""

    optimizer: tuple[float, ...]
    residuals: tuple[tuple[PO014WitnessIndex, float], ...]
    max_abs_residual: float
    authority_effect: str = "None"

    _STATUS: ClassVar[str] = "SURROGATE_ONLY"

    @property
    def status(self) -> str:
        return self._STATUS

    @property
    def is_canonical(self) -> bool:
        return False

    @property
    def is_certified(self) -> bool:
        return False


def _lexicographically_less(left: Matrix, right: Matrix) -> bool:
    for a, b in zip(left, right, strict=True):
        difference = simplify(a - b)
        if difference == 0:
            continue
        return bool(difference < 0)
    return False


def _zero_affine_solution(a_matrix: Matrix, b_vector: Matrix) -> Matrix | None:
    if a_matrix.rank() != a_matrix.row_join(-b_vector).rank():
        return None
    solution, _parameters = a_matrix.gauss_jordan_solve(-b_vector)
    substitutions = {symbol: Rational(0) for symbol in solution.free_symbols}
    return Matrix(solution.subs(substitutions))


def _independent_columns(matrix: Matrix, rank: int) -> tuple[int, ...]:
    for indices in combinations(range(matrix.cols), rank):
        if matrix[:, indices].rank() == rank:
            return indices
    raise ArithmeticError("no independent column basis for PO-014 affine family")


def _solve_primal_vertices(a_matrix: Matrix, b_vector: Matrix) -> tuple[Matrix, Matrix, Rational]:
    """Solve the rational Chebyshev regression LP by active-vertex enumeration."""

    zero_solution = _zero_affine_solution(a_matrix, b_vector)
    if zero_solution is not None:
        return zero_solution, Matrix.zeros(a_matrix.rows, 1), Rational(0)

    rank = a_matrix.rank()
    if rank == 0:
        z = Matrix.zeros(a_matrix.cols, 1)
        residual = b_vector
        return z, residual, simplify(max(Abs(value) for value in residual))

    basis_columns = _independent_columns(a_matrix, rank)
    reduced = a_matrix[:, basis_columns]
    best_z: Matrix | None = None
    best_residual: Matrix | None = None
    best_t: Rational | None = None

    for row_indices in combinations(range(a_matrix.rows), rank + 1):
        for signs in product((Rational(-1), Rational(1)), repeat=rank + 1):
            active = Matrix(
                [
                    [sign * reduced[row, column] for column in range(rank)] + [Rational(-1)]
                    for row, sign in zip(row_indices, signs, strict=True)
                ]
            )
            if active.rank() != rank + 1:
                continue
            rhs = Matrix(
                [-sign * b_vector[row, 0] for row, sign in zip(row_indices, signs, strict=True)]
            )
            candidate = active.inv() * rhs
            t_value = simplify(candidate[rank, 0])
            if t_value < 0:
                continue
            z = Matrix.zeros(a_matrix.cols, 1)
            for local, column in enumerate(basis_columns):
                z[column, 0] = simplify(candidate[local, 0])
            residual = a_matrix * z + b_vector
            if any(bool(Abs(value) > t_value) for value in residual):
                continue
            if (
                best_t is None
                or bool(t_value < best_t)
                or (t_value == best_t and best_z is not None and _lexicographically_less(z, best_z))
            ):
                best_z, best_residual, best_t = z, residual, t_value

    if best_z is None or best_residual is None or best_t is None:
        raise ArithmeticError("no feasible PO-014 minimax vertex found")
    return best_z, best_residual, simplify(best_t)


def _solve_dual_lower_bound(
    a_matrix: Matrix,
    b_vector: Matrix,
    residual: Matrix,
    t_star: Rational,
) -> tuple[Matrix, Rational]:
    """Construct ``A^T y=0, ||y||_1<=1`` from active subgradients."""

    if t_star == 0:
        return Matrix.zeros(a_matrix.rows, 1), Rational(0)
    active_rows = tuple(
        row for row in range(a_matrix.rows) if simplify(Abs(residual[row, 0]) - t_star) == 0
    )
    signs = {
        row: Rational(1) if residual[row, 0] > 0 else Rational(-1)
        for row in active_rows
    }
    rank = a_matrix.rank()
    for subset_size in range(1, min(rank + 1, len(active_rows)) + 1):
        for row_indices in combinations(active_rows, subset_size):
            gradients = Matrix(
                [
                    [signs[row] * a_matrix[row, column] for row in row_indices]
                    for column in range(a_matrix.cols)
                ]
                + [[Rational(1) for _row in row_indices]]
            )
            rhs = Matrix.zeros(a_matrix.cols + 1, 1)
            rhs[a_matrix.cols, 0] = 1
            try:
                lambdas, parameters = gradients.gauss_jordan_solve(rhs)
            except ValueError:
                continue
            if parameters.rows != 0 or any(bool(value < 0) for value in lambdas):
                continue
            dual = Matrix.zeros(a_matrix.rows, 1)
            for row, value in zip(row_indices, lambdas, strict=True):
                dual[row, 0] = simplify(value * signs[row])
            if a_matrix.T * dual != Matrix.zeros(a_matrix.cols, 1):
                continue
            if simplify(sum(Abs(value) for value in dual) - 1) != 0:
                continue
            lower_bound = simplify((b_vector.T * dual)[0])
            if simplify(lower_bound - t_star) == 0:
                return dual, lower_bound
    raise ArithmeticError("no exact PO-014 dual lower-bound witness found")


@dataclass(frozen=True)
class PO014MinimaxProblem:
    """A fixed, nonempty family of affine scalar witnesses."""

    witnesses: tuple[PO014AffineWitness, ...]
    authority_effect: str = "None"

    def __post_init__(self) -> None:
        witnesses = tuple(self.witnesses)
        if not witnesses:
            raise PO014MinimaxRefused("PO-014 requires a nonempty witness family")
        if not all(isinstance(witness, PO014AffineWitness) for witness in witnesses):
            raise PO014MinimaxRefused("all PO-014 witnesses must be PO014AffineWitness values")
        if self.authority_effect != "None":
            raise PO014MinimaxRefused("AuthorityEffect must be None")
        dimension = len(witnesses[0].coefficients)
        if dimension == 0:
            raise PO014MinimaxRefused("PO-014 requires a nondegenerate optimizer dimension")
        if any(len(witness.coefficients) != dimension for witness in witnesses):
            raise PO014MinimaxRefused("all affine witnesses must share one optimizer dimension")
        indices = [witness.index for witness in witnesses]
        if len(indices) != len(set(indices)):
            raise PO014MinimaxRefused("PO-014 witness indices must be unique")
        object.__setattr__(self, "witnesses", tuple(sorted(witnesses, key=lambda item: item.index)))

    @property
    def dimension(self) -> int:
        return len(self.witnesses[0].coefficients)

    def solve_exact(self) -> PO014MinimaxReceipt:
        return solve_po014_minimax_exact(self)


def _problem_matrices(problem: PO014MinimaxProblem) -> tuple[Matrix, Matrix]:
    a_matrix = Matrix(
        [
            [witness.weight * coefficient for coefficient in witness.coefficients]
            for witness in problem.witnesses
        ]
    )
    b_vector = Matrix([witness.weight * witness.offset for witness in problem.witnesses])
    return a_matrix, b_vector


def solve_po014_minimax_exact(problem: PO014MinimaxProblem) -> PO014MinimaxReceipt:
    """Solve and replay the canonical shared-optimizer PO-014 problem exactly."""

    if not isinstance(problem, PO014MinimaxProblem):
        raise PO014MinimaxRefused("canonical solve requires PO014MinimaxProblem")
    a_matrix, b_vector = _problem_matrices(problem)
    z, residual, t_star = _solve_primal_vertices(a_matrix, b_vector)
    dual, lower_bound = _solve_dual_lower_bound(a_matrix, b_vector, residual, t_star)
    z_star = tuple(simplify(z[index, 0]) for index in range(z.rows))
    residual_entries = tuple(
        PO014IndexedScalar(witness.index, simplify(residual[row, 0]))
        for row, witness in enumerate(problem.witnesses)
    )
    active = tuple(
        entry.index for entry in residual_entries if simplify(Abs(entry.value) - t_star) == 0
    )
    dual_entries = tuple(
        PO014IndexedScalar(witness.index, simplify(dual[row, 0]))
        for row, witness in enumerate(problem.witnesses)
    )
    receipt = PO014MinimaxReceipt(
        z_star=z_star,
        residuals=residual_entries,
        active_witnesses=active,
        t_star=simplify(t_star),
        dual_lower_bound_witness=dual_entries,
        dual_lower_bound=simplify(lower_bound),
        exact_gap=simplify(t_star - lower_bound),
        witness_indices=tuple(witness.index for witness in problem.witnesses),
        authority_effect="None",
    )
    if not verify_po014_minimax_receipt(problem, receipt):
        raise ArithmeticError("internal exact PO-014 receipt failed replay")
    return receipt


def verify_po014_minimax_receipt(
    problem: PO014MinimaxProblem,
    receipt: PO014MinimaxReceipt,
) -> bool:
    """Replay primal feasibility and the exact dual lower bound."""

    if receipt.authority_effect != "None" or receipt.witness_indices != tuple(
        witness.index for witness in problem.witnesses
    ):
        return False
    if len(receipt.z_star) != problem.dimension:
        return False
    residual_by_index = receipt.residual_by_index
    dual_by_index = receipt.dual_by_index
    if set(residual_by_index) != set(receipt.witness_indices):
        return False
    if set(dual_by_index) != set(receipt.witness_indices):
        return False
    for witness in problem.witnesses:
        if simplify(
            residual_by_index[witness.index] - witness.weighted_residual(receipt.z_star)
        ) != 0:
            return False
    if simplify(max(Abs(value) for value in residual_by_index.values()) - receipt.t_star) != 0:
        return False
    expected_active = tuple(
        index
        for index in receipt.witness_indices
        if simplify(Abs(residual_by_index[index]) - receipt.t_star) == 0
    )
    if receipt.active_witnesses != expected_active:
        return False
    for column in range(problem.dimension):
        if simplify(
            sum(
                dual_by_index[witness.index] * witness.weight * witness.coefficients[column]
                for witness in problem.witnesses
            )
        ) != 0:
            return False
    if bool(sum(Abs(value) for value in dual_by_index.values()) > 1):
        return False
    lower_bound = simplify(
        sum(
            dual_by_index[witness.index] * witness.weight * witness.offset
            for witness in problem.witnesses
        )
    )
    return (
        simplify(lower_bound - receipt.dual_lower_bound) == 0
        and simplify(receipt.t_star - receipt.dual_lower_bound) == 0
        and simplify(receipt.exact_gap) == 0
    )


def solve_po014_least_squares_surrogate(
    problem: PO014MinimaxProblem,
) -> PO014LeastSquaresSurrogateResult:
    """Run weighted least squares for comparison, explicitly outside the canonical rail."""

    if not isinstance(problem, PO014MinimaxProblem):
        raise PO014MinimaxRefused("surrogate solve requires PO014MinimaxProblem")
    a_matrix, b_vector = _problem_matrices(problem)
    a_float = np.asarray(a_matrix.tolist(), dtype=float)
    b_float = np.asarray(list(b_vector), dtype=float)
    optimizer, *_ = np.linalg.lstsq(a_float, -b_float, rcond=None)
    residual = a_float @ optimizer + b_float
    return PO014LeastSquaresSurrogateResult(
        optimizer=tuple(float(value) for value in optimizer),
        residuals=tuple(
            (witness.index, float(residual[row]))
            for row, witness in enumerate(problem.witnesses)
        ),
        max_abs_residual=float(np.max(np.abs(residual))),
        authority_effect="None",
    )


__all__ = [
    "PO014MinimaxRefused",
    "PO014WitnessIndex",
    "PO014AffineWitness",
    "PO014IndexedScalar",
    "PO014MinimaxReceipt",
    "PO014LeastSquaresSurrogateResult",
    "PO014MinimaxProblem",
    "solve_po014_minimax_exact",
    "verify_po014_minimax_receipt",
    "solve_po014_least_squares_surrogate",
]


