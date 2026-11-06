"""Deterministic finite-truncation obstruction solver, ported from Rust.

The represented operator is ``H_obstr = delta.T @ delta + V_defect``.  This
module mirrors ``omega_solvers/src/q_obstruction_solver.rs`` without depending
on NumPy, so its cyclic-Jacobi trace is deterministic in the minimum Python
runtime.

Scope fences:

* receipts concern finite-dimensional real-symmetric truncations only;
* the spectral ``l2`` Laplacian is not an ``l1`` compatibility norm or an
  ``H1`` cohomology class;
* orthogonal conjugation changes represented frame and does not repair a
  defect;
* every result is evidence-only and has ``AuthorityEffect::None``.
"""

from __future__ import annotations
from dataclasses import dataclass
from hashlib import sha256
import json
import math
import sys
from typing import Iterable, Sequence, TypeAlias

try:
    from .solver_evidence import (
        Certificate,
        CertificateKind,
        SolverDiagnostics,
        SolverError,
        SolverResult,
    )
except ImportError:
    from solver_evidence import (
        Certificate,
        CertificateKind,
        SolverDiagnostics,
        SolverError,
        SolverResult,
    )


Q_SPECTRAL_RECEIPT_SCHEMA = "omega.q-spectral-receipt.v1"
Q_GAUGE_MODEL = "O(n) real orthogonal conjugation on a finite truncation"
Q_TRUNCATION_NOTE = (
    "finite-dimensional real-symmetric truncation of a Q-level Hilbert "
    "cochain space; continuum-object claims remain Q-held; this receipt "
    "mints no authority"
)
Q_AUTHORITY_EFFECT = "None"

FloatVector: TypeAlias = tuple[float, ...]
FloatMatrix: TypeAlias = tuple[FloatVector, ...]
IntMatrix: TypeAlias = tuple[tuple[int, ...], ...]


def _rows(values: Iterable[Iterable[float]], label: str) -> FloatMatrix:
    def checked_float(value: float) -> float:
        if isinstance(value, bool):
            raise SolverError(
                SolverError.INFEASIBLE, f"{label} contains a Boolean scalar"
            )
        return float(value)

    try:
        matrix = tuple(tuple(checked_float(value) for value in row) for row in values)
    except (TypeError, ValueError, OverflowError) as error:
        raise SolverError.infeasible() from error
    if matrix and any(len(row) != len(matrix[0]) for row in matrix):
        raise SolverError(SolverError.INFEASIBLE, f"{label} is ragged")
    return matrix


def _shape(matrix: FloatMatrix) -> tuple[int, int]:
    return len(matrix), len(matrix[0]) if matrix else 0


def _finite(matrix: FloatMatrix) -> bool:
    return all(math.isfinite(value) for row in matrix for value in row)


def _identity(n: int) -> FloatMatrix:
    return tuple(
        tuple(1.0 if row == column else 0.0 for column in range(n)) for row in range(n)
    )


def _transpose(matrix: FloatMatrix, column_count: int | None = None) -> FloatMatrix:
    rows, columns = _shape(matrix)
    if rows == 0:
        return tuple(() for _ in range(column_count or 0))
    return tuple(
        tuple(matrix[row][column] for row in range(rows)) for column in range(columns)
    )


def _matmul(left: FloatMatrix, right: FloatMatrix) -> FloatMatrix:
    left_rows, inner = _shape(left)
    right_rows, right_columns = _shape(right)
    if inner != right_rows:
        raise SolverError.infeasible()
    return tuple(
        tuple(
            sum(left[row][k] * right[k][column] for k in range(inner))
            for column in range(right_columns)
        )
        for row in range(left_rows)
    )


def _add(left: FloatMatrix, right: FloatMatrix) -> FloatMatrix:
    if _shape(left) != _shape(right):
        raise SolverError.infeasible()
    return tuple(
        tuple(a + b for a, b in zip(left_row, right_row))
        for left_row, right_row in zip(left, right)
    )


def _scale(matrix: FloatMatrix, scalar: float) -> FloatMatrix:
    return tuple(tuple(scalar * value for value in row) for row in matrix)


def _matvec(matrix: FloatMatrix, vector: Sequence[float]) -> FloatVector:
    if matrix and len(matrix[0]) != len(vector):
        raise SolverError.infeasible()
    return tuple(sum(a * b for a, b in zip(row, vector)) for row in matrix)


def _dot(left: Sequence[float], right: Sequence[float]) -> float:
    return sum(a * b for a, b in zip(left, right))


def _amax(matrix: FloatMatrix) -> float:
    return max((abs(value) for row in matrix for value in row), default=0.0)


@dataclass(frozen=True)
class QObstructionInput:
    """A represented coboundary and symmetric defect potential on ``C0``."""

    coboundary: FloatMatrix
    defect_potential: FloatMatrix

    @classmethod
    def from_rows(
        cls,
        coboundary: Iterable[Iterable[float]],
        defect_potential: Iterable[Iterable[float]],
    ) -> "QObstructionInput":
        return cls(
            _rows(coboundary, "coboundary"), _rows(defect_potential, "defect_potential")
        )


@dataclass(frozen=True)
class QSpectralReceipt:
    """Replayable eigendata for one finite represented operator."""

    schema: str
    dim: int
    eigenvalues: FloatVector
    ground_energy: float
    spectral_gap: float | None
    ground_state: FloatVector
    eigenvectors: tuple[FloatVector, ...]
    residual_inf_norm: float
    jacobi_sweeps: int
    gauge_model: str
    truncation_note: str

    def canonical_payload(self) -> dict:
        return {
            "dim": self.dim,
            "eigenvalues": list(self.eigenvalues),
            "eigenvectors": [list(vector) for vector in self.eigenvectors],
            "gauge_model": self.gauge_model,
            "ground_energy": self.ground_energy,
            "ground_state": list(self.ground_state),
            "jacobi_sweeps": self.jacobi_sweeps,
            "residual_inf_norm": self.residual_inf_norm,
            "schema": self.schema,
            "spectral_gap": self.spectral_gap,
            "truncation_note": self.truncation_note,
        }

    @property
    def evidence_sha256(self) -> str:
        encoded = json.dumps(
            self.canonical_payload(),
            allow_nan=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
        return sha256(encoded).hexdigest()


def _validate_input(input_data: QObstructionInput) -> int:
    potential = _rows(input_data.defect_potential, "defect_potential")
    coboundary = _rows(input_data.coboundary, "coboundary")
    n, potential_columns = _shape(potential)
    if not _finite(coboundary) or not _finite(potential):
        raise SolverError.non_finite_input()
    if n == 0 or potential_columns != n:
        raise SolverError.infeasible()
    if coboundary and len(coboundary[0]) != n:
        raise SolverError.infeasible()
    for row in range(n):
        for column in range(row + 1, n):
            if potential[row][column] != potential[column][row]:
                raise SolverError.infeasible()
    return n


def obstruction_hamiltonian(input_data: QObstructionInput) -> FloatMatrix:
    """Assemble ``delta.T @ delta + V_defect`` after validation."""

    n = _validate_input(input_data)
    delta = _rows(input_data.coboundary, "coboundary")
    potential = _rows(input_data.defect_potential, "defect_potential")
    gram = tuple(
        tuple(sum(row[i] * row[j] for row in delta) for j in range(n)) for i in range(n)
    )
    return _add(gram, potential)


def symmetrize(matrix: Iterable[Iterable[float]]) -> tuple[FloatMatrix, float]:
    """Return ``((M + M.T)/2, max_abs((M - M.T)/2))``."""

    checked = _rows(matrix, "matrix")
    rows, columns = _shape(checked)
    if rows != columns:
        raise SolverError.infeasible()
    if not _finite(checked):
        raise SolverError.non_finite_input()
    symmetric = tuple(
        tuple((checked[i][j] + checked[j][i]) * 0.5 for j in range(rows))
        for i in range(rows)
    )
    residual = max(
        (
            abs((checked[i][j] - checked[j][i]) * 0.5)
            for i in range(rows)
            for j in range(rows)
        ),
        default=0.0,
    )
    return symmetric, residual


def _off_diagonal_frobenius(matrix: list[list[float]]) -> float:
    return math.sqrt(
        sum(
            value * value
            for i, row in enumerate(matrix)
            for j, value in enumerate(row)
            if i != j
        )
    )


def _jacobi_eigen(
    matrix: FloatMatrix, max_sweeps: int
) -> tuple[list[float], FloatMatrix, int]:
    n = len(matrix)
    a = [list(row) for row in matrix]
    q = [list(row) for row in _identity(n)]
    frobenius = math.sqrt(sum(value * value for row in matrix for value in row))
    stop = sys.float_info.epsilon * max(frobenius, sys.float_info.min) * float(n)
    sweeps = 0
    while sweeps < max_sweeps and _off_diagonal_frobenius(a) > stop:
        for p in range(max(n - 1, 0)):
            for r in range(p + 1, n):
                apr = a[p][r]
                if apr == 0.0:
                    continue
                tau = (a[r][r] - a[p][p]) / (2.0 * apr)
                if tau >= 0.0:
                    t = 1.0 / (tau + math.sqrt(1.0 + tau * tau))
                else:
                    t = -1.0 / (-tau + math.sqrt(1.0 + tau * tau))
                c = 1.0 / math.sqrt(1.0 + t * t)
                s = t * c
                for k in range(n):
                    akp, akr = a[k][p], a[k][r]
                    a[k][p] = c * akp - s * akr
                    a[k][r] = s * akp + c * akr
                for k in range(n):
                    apk, ark = a[p][k], a[r][k]
                    a[p][k] = c * apk - s * ark
                    a[r][k] = s * apk + c * ark
                for k in range(n):
                    qkp, qkr = q[k][p], q[k][r]
                    q[k][p] = c * qkp - s * qkr
                    q[k][r] = s * qkp + c * qkr
        sweeps += 1
    return [a[i][i] for i in range(n)], tuple(tuple(row) for row in q), sweeps


def _canonical_sign(vector: Iterable[float]) -> FloatVector:
    values = tuple(vector)
    first = next((value for value in values if abs(value) > 1e-12), None)
    return (
        tuple(-value for value in values)
        if first is not None and first < 0.0
        else values
    )


@dataclass(frozen=True)
class QObstructionSolver:
    """Fixed-order cyclic-Jacobi eigensolver matching the Rust production seam."""

    tolerance: float = 1e-10
    max_sweeps: int = 64

    def solve(self, input_data: QObstructionInput) -> SolverResult[QSpectralReceipt]:
        if (
            not math.isfinite(self.tolerance)
            or self.tolerance < 0.0
            or self.max_sweeps < 0
        ):
            raise SolverError.infeasible()
        hamiltonian = obstruction_hamiltonian(input_data)
        if not _finite(hamiltonian):
            raise SolverError.numerical_failure(
                "floating-point overflow assembling H_obstr = delta.T delta + V_defect"
            )
        n = len(hamiltonian)
        values, vectors_as_columns, sweeps = _jacobi_eigen(hamiltonian, self.max_sweeps)
        order = sorted(range(n), key=lambda index: (values[index], index))
        eigenvalues = tuple(values[index] for index in order)
        eigenvectors = tuple(
            _canonical_sign(vectors_as_columns[row][index] for row in range(n))
            for index in order
        )
        residual = 0.0
        for eigenvalue, vector in zip(eigenvalues, eigenvectors):
            hv = _matvec(hamiltonian, vector)
            residual = max(
                residual,
                max(
                    (
                        abs(value - eigenvalue * component)
                        for value, component in zip(hv, vector)
                    ),
                    default=0.0,
                ),
            )
        if not math.isfinite(residual):
            raise SolverError.numerical_failure("non-finite eigenpair residual")
        receipt = QSpectralReceipt(
            schema=Q_SPECTRAL_RECEIPT_SCHEMA,
            dim=n,
            eigenvalues=eigenvalues,
            ground_energy=eigenvalues[0],
            spectral_gap=eigenvalues[1] - eigenvalues[0] if n >= 2 else None,
            ground_state=eigenvectors[0],
            eigenvectors=eigenvectors,
            residual_inf_norm=residual,
            jacobi_sweeps=sweeps,
            gauge_model=Q_GAUGE_MODEL,
            truncation_note=Q_TRUNCATION_NOTE,
        )
        certificate_payload = json.dumps(
            {
                "eigenvalue": receipt.ground_energy,
                "eigenvector": list(receipt.ground_state),
            },
            allow_nan=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
        diagnostics = SolverDiagnostics(
            converged=residual <= self.tolerance,
            primal_residual=residual,
            dual_residual=None,
            primal_dual_gap=None,
            iteration_count=sweeps,
            tolerance=self.tolerance,
            certificates=[Certificate(CertificateKind.Eigenpair, certificate_payload)],
        )
        return SolverResult.new_with_diagnostics(receipt, diagnostics)


def orthogonal_gauge(generator: Iterable[Iterable[float]]) -> FloatMatrix:
    """Exponentiate an exactly skew-symmetric generator by scaling and squaring."""

    checked = _rows(generator, "generator")
    n, columns = _shape(checked)
    if columns != n:
        raise SolverError.infeasible()
    if not _finite(checked):
        raise SolverError.non_finite_input()
    if any(checked[i][j] + checked[j][i] != 0.0 for i in range(n) for j in range(n)):
        raise SolverError.infeasible()
    scaled = checked
    squarings = 0
    while _amax(scaled) > 0.5:
        scaled = _scale(scaled, 0.5)
        squarings += 1
    result = _identity(n)
    term = _identity(n)
    for k in range(1, 33):
        term = _scale(_matmul(term, scaled), 1.0 / float(k))
        result = _add(result, term)
        if _amax(term) < sys.float_info.epsilon:
            break
    for _ in range(squarings):
        result = _matmul(result, result)
    return result


def gauge_transform_input(
    input_data: QObstructionInput,
    gauge: Iterable[Iterable[float]],
) -> tuple[QObstructionInput, float]:
    """Apply ``delta -> delta G.T`` and ``V -> G V G.T``."""

    n = _validate_input(input_data)
    checked_gauge = _rows(gauge, "gauge")
    if _shape(checked_gauge) != (n, n) or not _finite(checked_gauge):
        raise SolverError.infeasible()
    transpose = _transpose(checked_gauge)
    delta = _rows(input_data.coboundary, "coboundary")
    transformed_delta = _matmul(delta, transpose) if delta else ()
    conjugated = _matmul(_matmul(checked_gauge, input_data.defect_potential), transpose)
    potential, residual = symmetrize(conjugated)
    return QObstructionInput(transformed_delta, potential), residual


def imaginary_time_excited_ratio(
    receipt: QSpectralReceipt,
    psi: Sequence[float],
    t: float,
) -> float:
    if not math.isfinite(t) or any(not math.isfinite(value) for value in psi):
        raise SolverError.non_finite_input()
    if t < 0.0 or len(psi) != receipt.dim:
        raise SolverError.infeasible()
    coefficients = tuple(_dot(vector, psi) for vector in receipt.eigenvectors)
    ground = abs(coefficients[0])
    if ground < 1e-300:
        raise SolverError.infeasible()
    excited_square = sum(
        (coefficient * math.exp(-(eigenvalue - receipt.ground_energy) * t)) ** 2
        for coefficient, eigenvalue in zip(coefficients[1:], receipt.eigenvalues[1:])
    )
    return math.sqrt(excited_square) / ground


def imaginary_time_evolve(
    receipt: QSpectralReceipt,
    psi: Sequence[float],
    t: float,
) -> FloatVector:
    if not math.isfinite(t) or any(not math.isfinite(value) for value in psi):
        raise SolverError.non_finite_input()
    if t < 0.0 or len(psi) != receipt.dim:
        raise SolverError.infeasible()
    output = [0.0] * receipt.dim
    for vector, eigenvalue in zip(receipt.eigenvectors, receipt.eigenvalues):
        coefficient = _dot(vector, psi) * math.exp(-eigenvalue * t)
        for index, component in enumerate(vector):
            output[index] += coefficient * component
    return tuple(output)


@dataclass(frozen=True)
class QObstructionInputDegree1:
    """Degree-1 Hodge input ``L1 = d0 d0.T + d1.T d1`` on ``C1``."""

    d0: FloatMatrix
    d1: FloatMatrix | None
    defect_potential: FloatMatrix

    @classmethod
    def from_rows(
        cls,
        d0: Iterable[Iterable[float]],
        d1: Iterable[Iterable[float]] | None,
        defect_potential: Iterable[Iterable[float]],
    ) -> "QObstructionInputDegree1":
        return cls(
            _rows(d0, "d0"),
            None if d1 is None else _rows(d1, "d1"),
            _rows(defect_potential, "defect_potential"),
        )


def degree1_hodge_laplacian(input_data: QObstructionInputDegree1) -> FloatMatrix:
    d0 = _rows(input_data.d0, "d0")
    m, _ = _shape(d0)
    down = tuple(
        tuple(
            sum(d0[i][k] * d0[j][k] for k in range(len(d0[0]) if d0 else 0))
            for j in range(m)
        )
        for i in range(m)
    )
    if input_data.d1 is None:
        return down
    d1 = _rows(input_data.d1, "d1")
    if d1 and len(d1[0]) != m:
        raise SolverError.infeasible()
    up = tuple(
        tuple(sum(row[i] * row[j] for row in d1) for j in range(m)) for i in range(m)
    )
    return _add(down, up)


def solve_degree1(
    solver: QObstructionSolver,
    input_data: QObstructionInputDegree1,
) -> SolverResult[QSpectralReceipt]:
    d0 = _rows(input_data.d0, "d0")
    potential = _rows(input_data.defect_potential, "defect_potential")
    m = len(d0)
    if _shape(potential) != (m, m) or m == 0:
        raise SolverError.infeasible()
    assembled = _add(degree1_hodge_laplacian(input_data), potential)
    operator, asymmetry = symmetrize(assembled)
    if not math.isfinite(asymmetry) or asymmetry > solver.tolerance:
        raise SolverError.numerical_failure(
            f"degree-1 operator asymmetry {asymmetry} exceeds tolerance {solver.tolerance}"
        )
    return solver.solve(QObstructionInput((), operator))


@dataclass(frozen=True)
class ParityShadowReceipt:
    delta1_delta0_zero: bool
    max_composite_entry: int
    shadow_orientation_free: bool

    def canonical_payload(self) -> dict:
        return {
            "delta1_delta0_zero": self.delta1_delta0_zero,
            "max_composite_entry": self.max_composite_entry,
            "shadow_orientation_free": self.shadow_orientation_free,
        }


def _integer_rows(values: Iterable[Iterable[int]], label: str) -> IntMatrix:
    matrix = tuple(tuple(value for value in row) for row in values)
    if matrix and any(len(row) != len(matrix[0]) for row in matrix):
        raise ValueError(f"{label} is ragged")
    if any(
        isinstance(value, bool) or not isinstance(value, int)
        for row in matrix
        for value in row
    ):
        raise TypeError(f"{label} must contain integers")
    return matrix


def parity_shadow_check(
    d0: Iterable[Iterable[int]],
    d1: Iterable[Iterable[int]],
    d0_reoriented: Iterable[Iterable[int]],
) -> ParityShadowReceipt:
    checked_d0 = _integer_rows(d0, "d0")
    checked_d1 = _integer_rows(d1, "d1")
    checked_reoriented = _integer_rows(d0_reoriented, "d0_reoriented")
    if checked_reoriented and _shape(checked_reoriented) != _shape(checked_d0):
        raise ValueError("reoriented d0 shape mismatch")
    if checked_d1 and len(checked_d1[0]) != len(checked_d0):
        raise ValueError("d1/d0 shape mismatch")
    columns = len(checked_d0[0]) if checked_d0 else 0
    composite = tuple(
        tuple(
            sum(row[k] * checked_d0[k][column] for k in range(len(checked_d0)))
            for column in range(columns)
        )
        for row in checked_d1
    )
    max_entry = max((abs(value) for row in composite for value in row), default=0)

    def shadow(matrix: IntMatrix) -> tuple[tuple[int, ...], ...]:
        return tuple(tuple(value % 2 for value in row) for row in matrix)

    return ParityShadowReceipt(
        delta1_delta0_zero=max_entry == 0,
        max_composite_entry=max_entry,
        shadow_orientation_free=shadow(checked_d0) == shadow(checked_reoriented),
    )


@dataclass(frozen=True)
class WeightedCarrier:
    d0: FloatMatrix
    w0: FloatVector
    w1: FloatVector
    defect_potential: FloatMatrix

    @classmethod
    def from_rows(
        cls,
        d0: Iterable[Iterable[float]],
        w0: Iterable[float],
        w1: Iterable[float],
        defect_potential: Iterable[Iterable[float]],
    ) -> "WeightedCarrier":
        return cls(
            _rows(d0, "d0"),
            tuple(float(value) for value in w0),
            tuple(float(value) for value in w1),
            _rows(defect_potential, "defect_potential"),
        )


def weighted_to_unit_input(carrier: WeightedCarrier) -> QObstructionInput:
    d0 = _rows(carrier.d0, "d0")
    m, n = _shape(d0)
    if len(carrier.w0) != n or len(carrier.w1) != m:
        raise SolverError.infeasible()
    if _shape(carrier.defect_potential) != (n, n):
        raise SolverError.infeasible()
    weights = carrier.w0 + carrier.w1
    if any(not math.isfinite(weight) or weight <= 0.0 for weight in weights):
        raise SolverError.infeasible()
    w0_inverse_sqrt = tuple(1.0 / math.sqrt(weight) for weight in carrier.w0)
    w1_sqrt = tuple(math.sqrt(weight) for weight in carrier.w1)
    coboundary = tuple(
        tuple(d0[i][j] * w1_sqrt[i] * w0_inverse_sqrt[j] for j in range(n))
        for i in range(m)
    )
    transformed_potential = tuple(
        tuple(
            carrier.defect_potential[i][j] * w0_inverse_sqrt[i] * w0_inverse_sqrt[j]
            for j in range(n)
        )
        for i in range(n)
    )
    potential, _ = symmetrize(transformed_potential)
    return QObstructionInput(coboundary, potential)


def s2_rayleigh_scan(
    input_data: QObstructionInput,
    receipt: QSpectralReceipt,
    test_vectors: Iterable[Sequence[float]],
) -> tuple[float, float]:
    hamiltonian = obstruction_hamiltonian(input_data)

    def rayleigh(vector: Sequence[float]) -> float:
        if len(vector) != receipt.dim:
            raise SolverError.infeasible()
        denominator = _dot(vector, vector)
        if denominator == 0.0:
            raise SolverError.infeasible()
        return _dot(vector, _matvec(hamiltonian, vector)) / denominator

    max_violation = max(
        (receipt.ground_energy - rayleigh(vector) for vector in test_vectors),
        default=0.0,
    )
    max_violation = max(0.0, max_violation)
    ground_error = abs(rayleigh(receipt.ground_state) - receipt.ground_energy)
    return max_violation, ground_error


def s3_excited_ground_ratio(
    receipt: QSpectralReceipt,
    psi0: Sequence[float],
    t: float,
) -> tuple[float, float] | None:
    if len(psi0) != receipt.dim or not math.isfinite(t) or t < 0.0:
        return None
    lambda0 = receipt.ground_energy
    lambda1 = next(
        (value for value in receipt.eigenvalues if value > lambda0 + 1e-12), None
    )
    if lambda1 is None:
        return None
    coefficients = tuple(_dot(vector, psi0) for vector in receipt.eigenvectors)

    def mass(ground: bool, time: float) -> float:
        return math.sqrt(
            sum(
                (coefficient * math.exp(-eigenvalue * time)) ** 2
                for coefficient, eigenvalue in zip(coefficients, receipt.eigenvalues)
                if ((abs(eigenvalue - lambda0) <= 1e-12) is ground)
            )
        )

    ground0 = mass(True, 0.0)
    if ground0 < 1e-9:
        return None
    excited0 = mass(False, 0.0)
    ground_t = mass(True, t)
    excited_t = mass(False, t)
    measured = excited_t / ground_t
    bound = math.exp(-(lambda1 - lambda0) * t) * (excited0 / ground0)
    return measured, bound


__all__ = [
    "FloatMatrix",
    "FloatVector",
    "ParityShadowReceipt",
    "Q_AUTHORITY_EFFECT",
    "Q_GAUGE_MODEL",
    "Q_SPECTRAL_RECEIPT_SCHEMA",
    "Q_TRUNCATION_NOTE",
    "QObstructionInput",
    "QObstructionInputDegree1",
    "QObstructionSolver",
    "QSpectralReceipt",
    "WeightedCarrier",
    "degree1_hodge_laplacian",
    "gauge_transform_input",
    "imaginary_time_evolve",
    "imaginary_time_excited_ratio",
    "obstruction_hamiltonian",
    "orthogonal_gauge",
    "parity_shadow_check",
    "s2_rayleigh_scan",
    "s3_excited_ground_ratio",
    "solve_degree1",
    "symmetrize",
    "weighted_to_unit_input",
]


