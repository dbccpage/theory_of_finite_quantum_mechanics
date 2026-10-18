from __future__ import annotations
import math
import numpy as np
from omega_engine.crates.engine.base.engine_base import Engine
from omega_engine.crates.linear_algebra_theory.density import ComplexDensityMatrix

CONTRACT_ID = "urn:omega:engine:operator_algebra_engine:file:v1.0.0"
EPSILON_QUANTUM_EIGEN = 1e-9
DEFAULT_TOLERANCE = 1e-9


class OperatorAlgebraError(Exception):
    pass


class ZeroDimension(OperatorAlgebraError):
    pass


class EmptyGenerators(OperatorAlgebraError):
    pass


class NonSquareMatrix(OperatorAlgebraError):
    def __init__(self, rows, cols):
        super().__init__(f"matrix must be square, got {rows}x{cols}")


class DimensionMismatch(OperatorAlgebraError):
    def __init__(self, expected, got):
        super().__init__(f"dimension mismatch: expected {expected}, got {got}")


class NonUnitalState(OperatorAlgebraError):
    def __init__(self, trace):
        super().__init__(f"state must satisfy omega(I)=1, got {trace}")


class NonPositiveState(OperatorAlgebraError):
    def __init__(self, min_eigenvalue):
        super().__init__(
            f"state density is not positive, min eigenvalue {min_eigenvalue}"
        )


class NonFaithfulState(OperatorAlgebraError):
    def __init__(self, min_eigenvalue):
        super().__init__(
            f"modular flow requires a faithful state, min eigenvalue {min_eigenvalue}"
        )


class NonDiagonalState(OperatorAlgebraError):
    def __init__(self, max_off_diagonal):
        super().__init__(
            f"finite modular flow helper expects diagonal density, max off-diagonal {max_off_diagonal}"
        )


class InvalidObservable(OperatorAlgebraError):
    pass


def ensure_square(matrix: np.ndarray):
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
        rows = matrix.shape[0] if matrix.ndim > 0 else 0
        cols = matrix.shape[1] if matrix.ndim > 1 else 0
        raise NonSquareMatrix(rows, cols)


def identity(dim: int) -> np.ndarray:
    return np.eye(dim, dtype=complex)


def matrix_unit(dim: int, row: int, col: int) -> np.ndarray:
    out = np.zeros((dim, dim), dtype=complex)
    out[row, col] = 1.0 + 0.0j
    return out


def matrix_unit_basis(dim: int) -> list:
    basis = []
    for r in range(dim):
        for c in range(dim):
            basis.append(matrix_unit(dim, r, c))
    return basis


def operator_norm(a: np.ndarray) -> float:
    s = np.linalg.svd(a, compute_uv=False)
    return float(np.max(s)) if len(s) > 0 else 0.0


def min_max_hermitian_eigenvalue(a: np.ndarray) -> tuple:
    eigenvalues = np.linalg.eigh(a)[0]
    return float(np.min(eigenvalues)), float(np.max(eigenvalues))


def min_hermitian_eigenvalue(a: np.ndarray) -> float:
    return min_max_hermitian_eigenvalue(a)[0]


def hermitian_complex_rank(a: np.ndarray, tolerance: float) -> int:
    eigenvalues = np.linalg.eigh(a)[0]
    return int(np.sum(np.abs(eigenvalues) > tolerance))


def complex_to_real_block(a: np.ndarray) -> np.ndarray:
    n = a.shape[0]
    block = np.zeros((2 * n, 2 * n), dtype=float)
    block[0:n, 0:n] = a.real
    block[0:n, n : 2 * n] = -a.imag
    block[n : 2 * n, 0:n] = a.imag
    block[n : 2 * n, n : 2 * n] = a.real
    return block


def flatten_complex_matrix(a: np.ndarray) -> np.ndarray:
    n = a.shape[0]
    m = a.shape[1]
    flat = a.flatten(order="F")
    out = np.zeros(2 * n * m, dtype=float)
    out[0 : n * m] = flat.real
    out[n * m : 2 * n * m] = flat.imag
    return out


def multiply_flattened_by_i(v: np.ndarray) -> np.ndarray:
    half = len(v) // 2
    out = np.zeros(len(v), dtype=float)
    out[0:half] = -v[half : 2 * half]
    out[half : 2 * half] = v[0:half]
    return out


def complex_span_columns(mats: list) -> np.ndarray:
    if not mats:
        return np.zeros((0, 0), dtype=float)
    columns = []
    for mat in mats:
        v = flatten_complex_matrix(mat)
        iv = multiply_flattened_by_i(v)
        columns.append(v)
        columns.append(iv)
    return np.column_stack(columns)


def real_rank(matrix: np.ndarray, tolerance: float) -> int:
    if matrix.shape[0] == 0 or matrix.shape[1] == 0:
        return 0
    s = np.linalg.svd(matrix, compute_uv=False)
    return int(np.sum(s > tolerance))


def complex_span_rank(mats: list, tolerance: float) -> int:
    if not mats:
        return 0
    return real_rank(complex_span_columns(mats), tolerance) // 2


def add_to_complex_span(basis: list, candidate: np.ndarray, tolerance: float) -> bool:
    before = complex_span_rank(basis, tolerance)
    trial = list(basis)
    trial.append(candidate)
    after = complex_span_rank(trial, tolerance)
    if after > before:
        basis.append(candidate)
        return True
    return False


class CStarAlgebra(Engine):
    def dim(self) -> int:
        raise NotImplementedError()

    def unit(self) -> np.ndarray:
        raise NotImplementedError()

    def star(self, a: np.ndarray) -> np.ndarray:
        raise NotImplementedError()

    def multiply(self, a: np.ndarray, b: np.ndarray) -> np.ndarray:
        raise NotImplementedError()

    def norm(self, a: np.ndarray) -> float:
        raise NotImplementedError()

    def cstar_identity_defect(self, a: np.ndarray) -> float:
        a_star_a = self.multiply(self.star(a), a)
        lhs = self.norm(a_star_a)
        rhs = self.norm(a) ** 2
        return abs(lhs - rhs)


class MatrixCStarAlgebra(CStarAlgebra):
    def __init__(self, dim: int, tolerance: float = DEFAULT_TOLERANCE):
        if dim == 0:
            raise ZeroDimension()
        self._dim = dim
        self._tolerance = max(tolerance, EPSILON_QUANTUM_EIGEN)

    @classmethod
    def new(cls, dim: int):
        return cls(dim)

    @classmethod
    def with_tolerance(cls, dim: int, tolerance: float):
        return cls(dim, tolerance)

    def dim(self) -> int:
        return self._dim

    def tolerance(self) -> float:
        return self._tolerance

    def ensure_element(self, a: np.ndarray):
        ensure_square(a)
        if a.shape[0] != self.dim():
            raise DimensionMismatch(self.dim(), a.shape[0])

    def unit(self) -> np.ndarray:
        return identity(self.dim())

    def star(self, a: np.ndarray) -> np.ndarray:
        self.ensure_element(a)
        return a.conj().T

    def multiply(self, a: np.ndarray, b: np.ndarray) -> np.ndarray:
        self.ensure_element(a)
        self.ensure_element(b)
        return a @ b

    def norm(self, a: np.ndarray) -> float:
        self.ensure_element(a)
        return operator_norm(a)


class AlgebraicState:
    def __init__(
        self, density: ComplexDensityMatrix, tolerance: float = DEFAULT_TOLERANCE
    ):
        ensure_square(density.rho())
        self._density = density
        self._tolerance = max(tolerance, EPSILON_QUANTUM_EIGEN)

        trace = float(np.trace(density.rho()).real)
        if abs(trace - 1.0) > self._tolerance:
            raise NonUnitalState(trace)

        min_ev = min_hermitian_eigenvalue(density.rho())
        if min_ev < -self._tolerance:
            raise NonPositiveState(min_ev)

    @classmethod
    def from_density(cls, density: ComplexDensityMatrix):
        return cls(density)

    @classmethod
    def with_tolerance(cls, density: ComplexDensityMatrix, tolerance: float):
        return cls(density, tolerance)

    @classmethod
    def vector_state(cls, psi: np.ndarray):
        norm = float(np.linalg.norm(psi))
        if norm <= EPSILON_QUANTUM_EIGEN or not math.isfinite(norm):
            raise InvalidObservable("cyclic vector has zero or non-finite norm")
        normalized = psi / norm
        dm = ComplexDensityMatrix.from_cvector(normalized)
        return cls(dm, EPSILON_QUANTUM_EIGEN)

    def density(self) -> ComplexDensityMatrix:
        return self._density

    def dim(self) -> int:
        return self._density.dim()

    def expectation(self, observable: np.ndarray) -> complex:
        ensure_square(observable)
        if observable.shape[0] != self.dim():
            raise DimensionMismatch(self.dim(), observable.shape[0])
        return complex(np.trace(self._density.rho() @ observable))

    def is_positive_on_square(self, a: np.ndarray) -> bool:
        val = self.expectation(a.conj().T @ a)
        return val.real >= -self._tolerance and abs(val.imag) <= self._tolerance


class GnsConstruction:
    def __init__(self, state: AlgebraicState):
        self._state = state
        self._matrix_units = matrix_unit_basis(state.dim())

        n = len(self._matrix_units)
        gram = np.zeros((n, n), dtype=complex)
        for i, a in enumerate(self._matrix_units):
            for j, b in enumerate(self._matrix_units):
                gram[i, j] = state.expectation(a.conj().T @ b)
        self._gram = gram
        self._quotient_dimension = hermitian_complex_rank(gram, state._tolerance)

    @classmethod
    def from_state(cls, state: AlgebraicState):
        return cls(state)

    def gram(self) -> np.ndarray:
        return self._gram

    def quotient_dimension(self) -> int:
        return self._quotient_dimension

    def cyclic_expectation(self, observable: np.ndarray) -> complex:
        return self._state.expectation(observable)

    def inner_product(self, a: np.ndarray, b: np.ndarray) -> complex:
        return self._state.expectation(a.conj().T @ b)

    def left_action_matrix(self, a: np.ndarray) -> np.ndarray:
        ensure_square(a)
        if a.shape[0] != self._state.dim():
            raise DimensionMismatch(self._state.dim(), a.shape[0])

        dim = self._state.dim()
        n2 = dim * dim
        action = np.zeros((n2, n2), dtype=complex)
        for col, basis_element in enumerate(self._matrix_units):
            image = a @ basis_element
            for row in range(dim):
                for col_basis in range(dim):
                    row_index = row * dim + col_basis
                    action[row_index, col] = image[row, col_basis]
        return action


class DoubleCommutantDiagnostic:
    def __init__(
        self, gen_dim: int, comm_dim: int, double_comm_dim: int, is_closed: bool
    ):
        self.generated_dimension = gen_dim
        self.commutant_dimension = comm_dim
        self.double_commutant_dimension = double_comm_dim
        self.is_double_commutant_closed = is_closed


class FiniteVonNeumannAlgebra:
    def __init__(self, dim: int, basis: list, tolerance: float = DEFAULT_TOLERANCE):
        self._dim = dim
        self._basis = basis
        self._tolerance = tolerance

    @classmethod
    def generated_by(cls, dim: int, generators: list):
        return cls.generated_by_with_tolerance(dim, generators, DEFAULT_TOLERANCE)

    @classmethod
    def generated_by_with_tolerance(cls, dim: int, generators: list, tolerance: float):
        if dim == 0:
            raise ZeroDimension()
        if not generators:
            raise EmptyGenerators()
        tolerance = max(tolerance, EPSILON_QUANTUM_EIGEN)

        for gen in generators:
            ensure_square(gen)
            if gen.shape[0] != dim:
                raise DimensionMismatch(dim, gen.shape[0])

        basis: list[np.ndarray] = []
        add_to_complex_span(basis, identity(dim), tolerance)
        for gen in generators:
            add_to_complex_span(basis, gen, tolerance)
            add_to_complex_span(basis, gen.conj().T, tolerance)

        max_dim = dim * dim
        changed = True
        while changed and complex_span_rank(basis, tolerance) < max_dim:
            changed = False
            snapshot = list(basis)
            for a in snapshot:
                for b in snapshot:
                    product = a @ b
                    if add_to_complex_span(basis, product, tolerance):
                        changed = True

        return cls(dim, basis, tolerance)

    def dim(self) -> int:
        return self._dim

    def algebra_dimension(self) -> int:
        return complex_span_rank(self._basis, self._tolerance)

    def basis(self) -> list:
        return self._basis

    def commutant_basis(self) -> list:
        return commutant_basis(self.dim(), self._basis, self._tolerance)

    def commutant_dimension(self) -> int:
        return complex_span_rank(self.commutant_basis(), self._tolerance)

    def double_commutant_diagnostic(self) -> DoubleCommutantDiagnostic:
        comm = self.commutant_basis()
        double_comm = commutant_basis(self.dim(), comm, self._tolerance)
        gen_dim = self.algebra_dimension()
        comm_dim = complex_span_rank(comm, self._tolerance)
        double_comm_dim = complex_span_rank(double_comm, self._tolerance)

        return DoubleCommutantDiagnostic(
            gen_dim, comm_dim, double_comm_dim, gen_dim == double_comm_dim
        )

    def is_factor(self) -> bool:
        return self.commutant_dimension() == 1


class ModularFlow:
    @staticmethod
    def diagonal_state_flow(
        state: AlgebraicState, observable: np.ndarray, t: float
    ) -> np.ndarray:
        ensure_square(observable)
        dim = state.dim()
        if observable.shape[0] != dim:
            raise DimensionMismatch(dim, observable.shape[0])

        density = state.density().rho()
        max_off_diagonal = max_off_diagonal_norm(density)
        if max_off_diagonal > state._tolerance:
            raise NonDiagonalState(max_off_diagonal)

        min_probability = min(density[i, i].real for i in range(dim))
        if min_probability <= state._tolerance:
            raise NonFaithfulState(min_probability)

        flowed = np.zeros((dim, dim), dtype=complex)
        for i in range(dim):
            for j in range(dim):
                ratio_log = math.log(density[i, i].real / density[j, j].real)
                phase = np.exp(1j * t * ratio_log)
                flowed[i, j] = phase * observable[i, j]
        return flowed


def commutant_basis(dim: int, generators: list, tolerance: float) -> list:
    constraints = commutant_constraint_matrix(dim, generators)
    nullspace = real_nullspace(constraints, tolerance)
    return [real_vector_to_complex_matrix(dim, v) for v in nullspace]


def commutant_constraint_matrix(dim: int, generators: list) -> np.ndarray:
    n2 = dim * dim
    rows = 2 * len(generators) * n2
    cols = 2 * n2
    matrix = np.zeros((rows, cols), dtype=float)
    row = 0

    for gen in generators:
        for i in range(dim):
            for j in range(dim):
                for k in range(dim):
                    add_complex_coeff(matrix, row, dim, i, k, gen[k, j])
                    add_complex_coeff(matrix, row, dim, k, j, -gen[i, k])
                row += 2
    return matrix


def add_complex_coeff(
    matrix: np.ndarray, row: int, dim: int, var_row: int, var_col: int, coeff: complex
):
    n2 = dim * dim
    index = var_row + var_col * dim
    re_col = index
    im_col = index + n2

    matrix[row, re_col] += coeff.real
    matrix[row, im_col] -= coeff.imag
    matrix[row + 1, re_col] += coeff.imag
    matrix[row + 1, im_col] += coeff.real


def real_nullspace(matrix: np.ndarray, tolerance: float) -> list:
    if matrix.shape[1] == 0:
        return []
    u, s, vh = np.linalg.svd(matrix)
    rank = int(np.sum(s > tolerance))

    nullspace_basis = []
    for row in range(rank, matrix.shape[1]):
        nullspace_basis.append(vh[row, :])
    return nullspace_basis


def real_vector_to_complex_matrix(dim: int, vector: np.ndarray) -> np.ndarray:
    n2 = dim * dim
    out = np.zeros((dim, dim), dtype=complex)
    for col in range(dim):
        for row in range(dim):
            index = row + col * dim
            out[row, col] = complex(vector[index], vector[index + n2])
    return out


def max_off_diagonal_norm(matrix: np.ndarray) -> float:
    max_val = 0.0
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            if i != j:
                max_val = max(max_val, abs(matrix[i, j]))
    return max_val



