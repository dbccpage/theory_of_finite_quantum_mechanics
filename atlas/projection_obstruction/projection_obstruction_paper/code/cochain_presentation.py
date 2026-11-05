"""Exact induced-cochain, quotient, and coboundary certificates for PO-000 §7.2."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from itertools import combinations, product

from exactsym import Abs, Matrix, MatrixBase, Rational, simplify

from exact import ExactInput, exact_column, exact_equal, exact_matrix, exact_matrix_from_matrix


class MissingObservationMapError(KeyError):
    """A residual has no declared observation map."""


class HigherDifferentialUnavailable(RuntimeError):
    """The native covering-edge carrier does not supply ``C2`` or ``d1``."""


@dataclass(frozen=True)
class ObservationMap:
    """One exact linear map ``q_e : R_e -> V_e``."""

    edge_id: str
    matrix: Matrix

    def __post_init__(self) -> None:
        object.__setattr__(self, "matrix", exact_matrix_from_matrix(self.matrix))

    def observe(self, residual: MatrixBase) -> Matrix:
        vector = exact_matrix_from_matrix(residual)
        if vector.shape != (self.matrix.cols, 1):
            raise ValueError(
                f"residual for {self.edge_id!r} has shape {vector.shape}, "
                f"expected {(self.matrix.cols, 1)}"
            )
        return self.matrix * vector


@dataclass(frozen=True)
class InducedCochain:
    """Ordered exact edge blocks produced by a total observation presentation."""

    edge_order: tuple[str, ...]
    blocks: tuple[Matrix, ...]

    def as_vector(self) -> Matrix:
        if not self.blocks:
            return Matrix.zeros(0, 1)
        return Matrix.vstack(*self.blocks)


@dataclass(frozen=True)
class ExactnessCertificate:
    """Exact membership or non-membership witness for ``omega in im(d0)``."""

    is_exact_coboundary: bool
    cochain: Matrix
    repair_map: Matrix
    witness: Matrix | None
    separating_left_kernel_vector: Matrix | None
    separating_pairing: Rational | None

    def verify(self) -> bool:
        if self.is_exact_coboundary:
            return self.witness is not None and exact_equal(
                self.repair_map * self.witness, self.cochain
            )
        if self.separating_left_kernel_vector is None or self.separating_pairing is None:
            return False
        separator = self.separating_left_kernel_vector
        return exact_equal(
            separator.T * self.repair_map, Matrix.zeros(1, self.repair_map.cols)
        ) and (
            simplify((separator.T * self.cochain)[0] - self.separating_pairing) == 0
            and self.separating_pairing != 0
        )


@dataclass(frozen=True)
class QuotientDistanceCertificate:
    """Exact rational ``l1`` distance from ``omega`` to ``im(d0)``."""

    distance: Rational
    repair_witness: Matrix
    residual: Matrix
    cochain: Matrix
    dual_witness: Matrix
    dual_pairing: Rational
    repair_map: Matrix

    def verify(self) -> bool:
        return (
            exact_equal(self.residual, self.cochain - self.repair_map * self.repair_witness)
            and simplify(sum(Abs(value) for value in self.residual) - self.distance) == 0
            and self.dual_witness.shape == (self.repair_map.rows, 1)
            and exact_equal(
                self.repair_map.T * self.dual_witness,
                Matrix.zeros(self.repair_map.cols, 1),
            )
            and all(bool(Abs(value) <= 1) for value in self.dual_witness)
            and simplify((self.dual_witness.T * self.cochain)[0] - self.dual_pairing) == 0
            and simplify(self.dual_pairing - self.distance) == 0
            and bool(self.distance >= 0)
            and bool(self.dual_pairing >= 0)
        )


def _independent_column_indices(matrix: Matrix, rank: int) -> tuple[int, ...]:
    for indices in combinations(range(matrix.cols), rank):
        if matrix[:, indices].rank() == rank:
            return indices
    raise ArithmeticError("matrix rank has no matching independent-column witness")


def _exact_l1_primal_vertex(repair_map: Matrix, cochain: Matrix) -> tuple[Matrix, Matrix, Rational]:
    """Enumerate vertices of the rational residual hyperplane arrangement."""

    rank = repair_map.rank()
    witness = Matrix.zeros(repair_map.cols, 1)
    if rank == 0:
        residual = cochain
        return witness, residual, simplify(sum(Abs(value) for value in residual))

    basis_columns = _independent_column_indices(repair_map, rank)
    reduced = repair_map[:, basis_columns]
    best: tuple[Rational, Matrix, Matrix] | None = None
    for row_indices in combinations(range(repair_map.rows), rank):
        square = reduced.extract(row_indices, range(rank))
        if square.rank() != rank:
            continue
        target = cochain.extract(row_indices, (0,))
        reduced_witness = square.inv() * target
        candidate = Matrix.zeros(repair_map.cols, 1)
        for local_index, column_index in enumerate(basis_columns):
            candidate[column_index, 0] = reduced_witness[local_index, 0]
        residual = cochain - repair_map * candidate
        distance = simplify(sum(Abs(value) for value in residual))
        if best is None or bool(distance < best[0]):
            best = (distance, candidate, residual)
    if best is None:
        raise ArithmeticError("no primal l1 vertex found despite positive matrix rank")
    return best[1], best[2], best[0]


def _exact_l1_dual_vertex(repair_map: Matrix, cochain: Matrix) -> tuple[Matrix, Rational]:
    """Enumerate vertices of ``ker(d0^T)`` intersected with the unit cube."""

    row_count = repair_map.rows
    rank = repair_map.rank()
    transpose = repair_map.T
    if rank == 0:
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

    best: tuple[Rational, Matrix] | None = None
    for free_indices in combinations(range(row_count), rank):
        free_matrix = transpose[:, free_indices]
        if free_matrix.rank() != rank:
            continue
        fixed_indices = tuple(index for index in range(row_count) if index not in free_indices)
        for fixed_signs in product((Rational(-1), Rational(1)), repeat=len(fixed_indices)):
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
            for index, value in zip(free_indices, free_vector, strict=True):
                candidate[index, 0] = value
            for index, value in zip(fixed_indices, fixed_signs, strict=True):
                candidate[index, 0] = value
            pairing = simplify((candidate.T * cochain)[0])
            if best is None or bool(pairing > best[0]):
                best = (pairing, candidate)
    if best is None:
        raise ArithmeticError("no dual l1 vertex found")
    return best[1], best[0]


@dataclass(frozen=True)
class AdmittedComplexV1:
    """Capability witness for a verified cochain complex (C0 -> d0 -> C1 -> d1 -> C2)."""

    d0: Matrix
    d1: Matrix

    def __post_init__(self) -> None:
        d0_mat = exact_matrix_from_matrix(self.d0)
        d1_mat = exact_matrix_from_matrix(self.d1)
        if hasattr(d0_mat, "as_immutable"):
            d0_mat = d0_mat.as_immutable()
        if hasattr(d1_mat, "as_immutable"):
            d1_mat = d1_mat.as_immutable()
        object.__setattr__(self, "d0", d0_mat)
        object.__setattr__(self, "d1", d1_mat)
        self.validate()

    def validate(self) -> None:
        if self.d1.cols != self.d0.rows:
            raise ValueError("d1 and d0 dimensions do not compose")
        if not exact_equal(self.d1 * self.d0, Matrix.zeros(self.d1.rows, self.d0.cols)):
            raise ValueError("d1 * d0 != 0; complex composition failed")


# Canonical induced cochain class and backward-compatible alias
ObservedEdgeField = InducedCochain


@dataclass(frozen=True)
class AdmittedCochain:
    """Authenticated cochain produced by an ObservationPresentation with complex capability."""

    field: InducedCochain
    complex_capability: AdmittedComplexV1

    def __post_init__(self) -> None:
        if not isinstance(self.complex_capability, AdmittedComplexV1):
            raise TypeError(
                f"complex_capability must be an AdmittedComplexV1 instance, got {type(self.complex_capability).__name__}"
            )
        self.complex_capability.validate()

    def as_vector(self) -> Matrix:
        return self.field.as_vector()


class ObservationPresentation:
    """A total, ordered family of exact observation maps."""

    def __init__(self, edge_order: Sequence[str], maps: Mapping[str, ObservationMap]):
        if not edge_order:
            raise ValueError("an observation presentation needs at least one edge")
        if len(set(edge_order)) != len(edge_order):
            raise ValueError("edge_order contains duplicates")
        missing = set(edge_order) - set(maps)
        extra = set(maps) - set(edge_order)
        if missing or extra:
            raise ValueError(
                f"observation-map domain mismatch; missing={sorted(missing)}, extra={sorted(extra)}"
            )
        if any(edge_id != maps[edge_id].edge_id for edge_id in edge_order):
            raise ValueError("observation-map keys must match their edge_id fields")
        self.edge_order = tuple(edge_order)
        self.maps = dict(maps)

    def induce_field(self, residuals: Mapping[str, MatrixBase]) -> InducedCochain:
        """Produce an unadmitted edge field using standard linear algebra terminology."""

        missing = set(self.edge_order) - set(residuals)
        extra = set(residuals) - set(self.edge_order)
        if missing:
            raise MissingObservationMapError(
                f"normal residuals missing declared edges: {sorted(missing)}"
            )
        if extra:
            raise MissingObservationMapError(
                f"normal residuals contain edges without declared maps: {sorted(extra)}"
            )
        return InducedCochain(
            edge_order=self.edge_order,
            blocks=tuple(
                self.maps[edge_id].observe(residuals[edge_id]) for edge_id in self.edge_order
            ),
        )

    def induce(
        self,
        residuals: Mapping[str, MatrixBase],
        capability: AdmittedComplexV1 | None = None,
    ) -> InducedCochain | AdmittedCochain:
        """Build an induced edge field or admitted cochain if capability is supplied."""

        field = self.induce_field(residuals)
        if capability is not None:
            if not isinstance(capability, AdmittedComplexV1):
                raise TypeError(
                    f"capability must be an AdmittedComplexV1 instance, got {type(capability).__name__}"
                )
            capability.validate()
            if capability.d0.rows != field.as_vector().rows:
                raise ValueError(
                    f"stacked observed field dimension {field.as_vector().rows} "
                    f"does not match d0.rows={capability.d0.rows}"
                )
            return AdmittedCochain(field=field, complex_capability=capability)
        return field


class LinearRepairProblem:
    """Exact finite linear repair problem ``d0 : V0 -> V1`` (linear algebra level)."""

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
        """Solve and certify the rational ``l1`` distance by vertex enumeration."""

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


class CoboundaryProblem(LinearRepairProblem):
    """Exact finite coboundary/image-membership problem using only ``d0``."""


class AdmittedComplexCoboundaryProblem(LinearRepairProblem):
    """Coboundary problem with an explicit ``AdmittedComplexV1`` higher-cell witness."""

    def __init__(self, capability: AdmittedComplexV1):
        if not isinstance(capability, AdmittedComplexV1):
            raise HigherDifferentialUnavailable(
                "Refusing 'AdmittedComplexCoboundaryProblem': missing AdmittedComplexV1 "
                "capability witness (C2, d1)"
            )
        capability.validate()
        super().__init__(capability.d0)
        self.capability = capability


def verify_cochain_complex(d0: MatrixBase, d1: MatrixBase | None) -> AdmittedComplexV1:
    """Check ``d1*d0=0`` exactly, or refuse absent higher-cell data."""

    if d1 is None:
        raise HigherDifferentialUnavailable("PO-000 native covering-edge data supplies no C2 or d1")
    left = exact_matrix_from_matrix(d1)
    right = exact_matrix_from_matrix(d0)
    if left.cols != right.rows:
        raise ValueError("d1 and d0 dimensions do not compose")
    if not exact_equal(left * right, Matrix.zeros(left.rows, right.cols)):
        raise ArithmeticError("d1*d0=0 complex condition failed")
    return AdmittedComplexV1(d0=right, d1=left)


def observation_map(edge_id: str, rows: Sequence[Sequence[ExactInput]]) -> ObservationMap:
    """Convenience constructor that rejects floating-point coefficients."""

    return ObservationMap(edge_id=edge_id, matrix=exact_matrix(rows))


def exact_cochain(values: Sequence[ExactInput]) -> Matrix:
    """Convenience constructor for tests and replay fixtures."""

    return exact_column(values)

