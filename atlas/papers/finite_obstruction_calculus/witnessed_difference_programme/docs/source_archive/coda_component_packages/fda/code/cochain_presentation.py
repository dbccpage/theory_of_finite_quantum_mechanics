# -*- coding: utf-8 -*-
"""
cochain_presentation.py: Standalone Exact Rational Cochain & L1 Quotient Solver.

Provides LinearRepairProblem and QuotientDistanceCertificate with exact rational
arithmetic (SymPy Rational / Matrix) without external monorepo dependencies.

AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations
from typing import Any, Optional, Tuple

from sympy import Abs, Basic, ImmutableMatrix, Matrix, Rational, simplify
from sympy.matrices.matrixbase import MatrixBase


def _as_exact_rational(value: Any) -> Rational:
    """Convert an exact scalar to SymPy Rational, rejecting floats and booleans."""
    if isinstance(value, bool):
        raise TypeError(f"exact arithmetic rejects bool; got {value!r}")
    if isinstance(value, float):
        raise TypeError(f"exact arithmetic rejects float; got {value!r}")
    if isinstance(value, int):
        return Rational(value, 1)
    if isinstance(value, Fraction):
        return Rational(value.numerator, value.denominator)
    if isinstance(value, Rational):
        return value
    if isinstance(value, str):
        return Rational(value)
    if hasattr(value, "is_Float") and value.is_Float:
        raise TypeError(f"exact arithmetic rejects SymPy Float; got {value!r}")
    if isinstance(value, Basic) and value.is_rational:
        return Rational(value)
    raise TypeError(f"exact arithmetic rejects {type(value).__name__}; use an exact scalar")


def exact_matrix_from_matrix(value: MatrixBase) -> Matrix:
    """Copy a matrix through the exact rational scalar gate."""
    return Matrix(
        value.rows,
        value.cols,
        [_as_exact_rational(value[row, col]) for row in range(value.rows) for col in range(value.cols)],
    )


def exact_equal(left: MatrixBase, right: MatrixBase) -> bool:
    """Check exact mathematical equality between two matrices."""
    if left.shape != right.shape:
        return False
    diff = left - right
    return all(simplify(diff[r, c]) == 0 for r in range(diff.rows) for c in range(diff.cols))


def _is_exact_rational_scalar(val: Any) -> bool:
    """Return True if scalar is an exact rational or integer, False for floats, symbols, etc."""
    if isinstance(val, bool) or isinstance(val, float):
        return False
    if hasattr(val, "is_Float") and val.is_Float:
        return False
    if isinstance(val, (int, Fraction, Rational)):
        return True
    if isinstance(val, Basic):
        return bool(val.is_rational)
    return False


@dataclass(frozen=True)
class ExactnessCertificate:
    """Exact membership or non-membership witness for omega in im(d0)."""

    is_exact_coboundary: bool
    cochain: Matrix
    repair_map: Matrix
    witness: Optional[Matrix]
    separating_left_kernel_vector: Optional[Matrix]
    separating_pairing: Optional[Rational]

    def __post_init__(self) -> None:
        for name in ("cochain", "repair_map", "witness", "separating_left_kernel_vector"):
            value = getattr(self, name)
            if isinstance(value, MatrixBase):
                object.__setattr__(self, name, ImmutableMatrix(value))

    def snapshot(self) -> ExactnessCertificate:
        """Return an independent record whose matrix entries cannot be mutated."""
        return ExactnessCertificate(
            self.is_exact_coboundary,
            self.cochain,
            self.repair_map,
            self.witness,
            self.separating_left_kernel_vector,
            self.separating_pairing,
        )

    def verify(self) -> bool:
        # 1. Structural / shape validation
        if not isinstance(self.repair_map, MatrixBase) or not isinstance(self.cochain, MatrixBase):
            return False

        m = self.repair_map.rows
        n = self.repair_map.cols
        if self.cochain.shape != (m, 1):
            return False

        # 2. Scalar domain validation on base matrices
        for mat in (self.repair_map, self.cochain):
            for r in range(mat.rows):
                for c in range(mat.cols):
                    if not _is_exact_rational_scalar(mat[r, c]):
                        return False

        if self.is_exact_coboundary:
            if self.witness is None or not isinstance(self.witness, MatrixBase):
                return False
            if self.witness.shape != (n, 1):
                return False
            for r in range(self.witness.rows):
                for c in range(self.witness.cols):
                    if not _is_exact_rational_scalar(self.witness[r, c]):
                        return False
            return exact_equal(self.repair_map * self.witness, self.cochain)

        # Non-membership branch: separating hyperplane witness
        if self.separating_left_kernel_vector is None or self.separating_pairing is None:
            return False
        if not isinstance(self.separating_left_kernel_vector, MatrixBase):
            return False
        if not _is_exact_rational_scalar(self.separating_pairing):
            return False

        separator = self.separating_left_kernel_vector
        if separator.shape != (m, 1):
            return False
        for r in range(separator.rows):
            for c in range(separator.cols):
                if not _is_exact_rational_scalar(separator[r, c]):
                    return False

        if not exact_equal(separator.T * self.repair_map, Matrix.zeros(1, n)):
            return False

        pairing_diff = simplify((separator.T * self.cochain)[0] - self.separating_pairing)
        return pairing_diff == 0 and self.separating_pairing != 0


@dataclass(frozen=True)
class QuotientDistanceCertificate:
    """Exact rational L1 distance from omega to im(d0)."""

    distance: Rational
    repair_witness: Matrix
    residual: Matrix
    cochain: Matrix
    dual_witness: Matrix
    dual_pairing: Rational
    repair_map: Matrix

    def __post_init__(self) -> None:
        for name in ("repair_witness", "residual", "cochain", "dual_witness", "repair_map"):
            value = getattr(self, name)
            if isinstance(value, MatrixBase):
                object.__setattr__(self, name, ImmutableMatrix(value))

    def snapshot(self) -> QuotientDistanceCertificate:
        """Return an independent record whose matrix entries cannot be mutated."""
        return QuotientDistanceCertificate(
            self.distance, self.repair_witness, self.residual, self.cochain,
            self.dual_witness, self.dual_pairing, self.repair_map,
        )

    def verify(self) -> bool:
        # 1. Structural / shape validation
        matrices = [self.repair_map, self.cochain, self.repair_witness, self.residual, self.dual_witness]
        if not all(isinstance(m, MatrixBase) for m in matrices):
            return False

        m = self.repair_map.rows
        n = self.repair_map.cols
        if self.cochain.shape != (m, 1):
            return False
        if self.repair_witness.shape != (n, 1):
            return False
        if self.residual.shape != (m, 1):
            return False
        if self.dual_witness.shape != (m, 1):
            return False

        # 2. Scalar domain validation (exact rationals only, zero floats/symbols)
        if not _is_exact_rational_scalar(self.distance) or not _is_exact_rational_scalar(self.dual_pairing):
            return False
        for mat in matrices:
            for r in range(mat.rows):
                for c in range(mat.cols):
                    if not _is_exact_rational_scalar(mat[r, c]):
                        return False

        # 3. Primal-dual equations and bounds
        try:
            return (
                exact_equal(self.residual, self.cochain - self.repair_map * self.repair_witness)
                and simplify(sum(Abs(value) for value in self.residual) - self.distance) == 0
                and exact_equal(
                    self.repair_map.T * self.dual_witness,
                    Matrix.zeros(self.repair_map.cols, 1),
                )
                and all(bool(Abs(value) <= 1) for value in self.dual_witness)
                and (
                    simplify((self.dual_witness.T * self.cochain)[0] - self.dual_pairing) == 0
                    if self.repair_map.rows > 0
                    else self.dual_pairing == 0
                )
                and simplify(self.dual_pairing - self.distance) == 0
                and bool(self.distance >= 0)
                and bool(self.dual_pairing >= 0)
            )
        except Exception:
            return False



def _independent_column_indices(matrix: Matrix, rank: int) -> Tuple[int, ...]:
    for indices in combinations(range(matrix.cols), rank):
        if matrix[:, indices].rank() == rank:
            return indices
    raise ArithmeticError("matrix rank has no matching independent-column witness")


def _exact_l1_primal_vertex(repair_map: Matrix, cochain: Matrix) -> Tuple[Matrix, Matrix, Rational]:
    """Enumerate vertices of the rational residual hyperplane arrangement."""
    rank = repair_map.rank()
    witness = Matrix.zeros(repair_map.cols, 1)
    if rank == 0:
        residual = cochain
        return witness, residual, simplify(sum(Abs(value) for value in residual))

    basis_columns = _independent_column_indices(repair_map, rank)
    reduced = repair_map[:, basis_columns]
    best: Optional[Tuple[Rational, Matrix, Matrix]] = None
    for row_indices in combinations(range(repair_map.rows), rank):
        square = reduced.extract(row_indices, range(rank))
        if square.rank() != rank:
            continue
        target = cochain.extract(row_indices, (0,))
        solution = square.gauss_jordan_solve(target)[0]
        candidate_witness = Matrix.zeros(repair_map.cols, 1)
        for col_idx, basis_idx in enumerate(basis_columns):
            candidate_witness[basis_idx, 0] = solution[col_idx, 0]
        residual = cochain - repair_map * candidate_witness
        cost = simplify(sum(Abs(value) for value in residual))
        if best is None or cost < best[0]:
            best = (cost, candidate_witness, residual)

    if best is None:
        raise ArithmeticError("hyperplane vertex enumeration yielded no candidates")
    return best[1], best[2], best[0]


def _exact_l1_dual_vertex(repair_map: Matrix, cochain: Matrix) -> Tuple[Matrix, Rational]:
    """Enumerate vertices of ker(d0^T) intersected with the unit cube."""
    row_count = repair_map.rows
    rank = repair_map.rank()
    if rank == 0:
        if row_count == 0:
            return Matrix.zeros(0, 1), Rational(0)
        witness = Matrix(
            [
                Rational(1) if value > 0 else Rational(-1) if value < 0 else Rational(0)
                for value in cochain
            ]
        )
        return witness, simplify((witness.T * cochain)[0])

    if rank == row_count:
        witness = Matrix.zeros(row_count, 1)
        return witness, Rational(0)

    from itertools import product as cartesian_product

    best: Optional[Tuple[Rational, Matrix]] = None
    transpose = repair_map.T
    for free_indices in combinations(range(row_count), rank):
        free_matrix = transpose[:, free_indices]
        if free_matrix.rank() != rank:
            continue
        fixed_indices = tuple(index for index in range(row_count) if index not in free_indices)
        for fixed_signs in cartesian_product((Rational(-1), Rational(1)), repeat=len(fixed_indices)):
            fixed_vector = Matrix(fixed_signs)
            fixed_matrix = transpose[:, fixed_indices]
            right_hand_side = -(fixed_matrix * fixed_vector)
            try:
                free_vector, parameters = free_matrix.gauss_jordan_solve(right_hand_side)
            except ValueError:
                continue
            if parameters.rows != 0 or any(Abs(value) > 1 for value in free_vector):
                continue
            candidate = Matrix.zeros(row_count, 1)
            for index, value in zip(free_indices, free_vector):
                candidate[index, 0] = value
            for index, value in zip(fixed_indices, fixed_signs):
                candidate[index, 0] = value
            pairing = simplify((candidate.T * cochain)[0])
            if best is None or bool(pairing > best[0]):
                best = (pairing, candidate)
    if best is None:
        raise ArithmeticError("no dual l1 vertex found")
    return best[1], best[0]


class LinearRepairProblem:
    """Exact finite linear repair problem d0 : V0 -> V1."""

    def __init__(self, repair_map_d0: MatrixBase):
        self.d0 = exact_matrix_from_matrix(repair_map_d0)

    def exactness_certificate(self, cochain: MatrixBase) -> ExactnessCertificate:
        """Return and recheck either a repair witness or a separating witness."""
        omega = exact_matrix_from_matrix(cochain)
        if omega.shape != (self.d0.rows, 1):
            raise ValueError(f"cochain has shape {omega.shape}, expected {(self.d0.rows, 1)}")

        if self.d0.rank() == self.d0.row_join(omega).rank():
            solution, _parameters = self.d0.gauss_jordan_solve(omega)
            substitutions = {symbol: Rational(0) for symbol in solution.free_symbols}
            witness = solution.subs(substitutions)
            certificate = ExactnessCertificate(
                is_exact_coboundary=True,
                cochain=omega,
                repair_map=self.d0,
                witness=witness,
                separating_left_kernel_vector=None,
                separating_pairing=None,
            )
        else:
            separator = next(
                vector for vector in self.d0.T.nullspace() if simplify((vector.T * omega)[0]) != 0
            )
            certificate = ExactnessCertificate(
                is_exact_coboundary=False,
                cochain=omega,
                repair_map=self.d0,
                witness=None,
                separating_left_kernel_vector=separator,
                separating_pairing=simplify((separator.T * omega)[0]),
            )

        if not certificate.verify():
            raise ArithmeticError("internal exactness certificate failed self-recheck")
        return certificate

    def quotient_l1_distance(self, cochain: MatrixBase) -> QuotientDistanceCertificate:
        """Solve and certify the rational L1 distance by vertex enumeration."""
        omega = exact_matrix_from_matrix(cochain)
        if omega.shape != (self.d0.rows, 1):
            raise ValueError(f"cochain has shape {omega.shape}, expected {(self.d0.rows, 1)}")

        repair_vector, residual, optimum = _exact_l1_primal_vertex(self.d0, omega)
        dual_witness, dual_pairing = _exact_l1_dual_vertex(self.d0, omega)
        if simplify(dual_pairing - optimum) != 0:
            raise ArithmeticError("primal and dual quotient optima disagree")

        certificate = QuotientDistanceCertificate(
            distance=simplify(optimum),
            repair_witness=repair_vector,
            residual=residual,
            cochain=omega,
            dual_witness=dual_witness,
            dual_pairing=dual_pairing,
            repair_map=self.d0,
        )
        if not certificate.verify():
            raise ArithmeticError("internal quotient certificate failed self-recheck")
        return certificate
