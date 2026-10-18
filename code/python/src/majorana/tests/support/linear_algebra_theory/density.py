import math
import numpy as np

DEFAULT_TOL = 1e-8
ZERO_NORM_TOL = 1e-12


class DensityMatrixError(Exception):
    pass


class ZeroDimension(DensityMatrixError):
    pass


class ShapeMismatch(DensityMatrixError):
    pass


class NonFiniteEntry(DensityMatrixError):
    pass


class ZeroVector(DensityMatrixError):
    pass


class NegativeProbability(DensityMatrixError):
    pass


class DimensionMismatch(DensityMatrixError):
    pass


class NonUnitary(DensityMatrixError):
    pass


class NonTracePreservingChannel(DensityMatrixError):
    pass


class NonPhysical(DensityMatrixError):
    pass


class InvalidTolerance(DensityMatrixError):
    pass


class UnsupportedOperation(DensityMatrixError):
    pass


class InvalidTopK(DensityMatrixError):
    pass


class NegativeWeight(DensityMatrixError):
    pass


class WeightSumNotOne(DensityMatrixError):
    pass


class TraceNotOne(DensityMatrixError):
    pass


class NoValidStates(DensityMatrixError):
    pass


class GraphDimensionMismatch(DensityMatrixError):
    pass


class InvalidKrausShape(DensityMatrixError):
    pass


class NonHermitian(DensityMatrixError):
    pass


class NotPositiveSemidefinite(DensityMatrixError):
    pass


class NonFiniteTolerance(DensityMatrixError):
    pass


class InvalidWindow(DensityMatrixError):
    pass


class NormalizationDrift(DensityMatrixError):
    pass


class H1NormalizationError(DensityMatrixError):
    pass


class InvalidProbabilityMass(DensityMatrixError):
    pass


class DensityMatrixConfig:
    def __init__(
        self,
        trace_tol=DEFAULT_TOL,
        hermitian_tol=DEFAULT_TOL,
        psd_tol=DEFAULT_TOL,
        unitary_tol=DEFAULT_TOL,
        weight_sum_tol=DEFAULT_TOL,
        zero_norm_tol=ZERO_NORM_TOL,
        channel_tol=DEFAULT_TOL,
    ):
        self._trace_tol = trace_tol
        self._hermitian_tol = hermitian_tol
        self._psd_tol = psd_tol
        self._unitary_tol = unitary_tol
        self._weight_sum_tol = weight_sum_tol
        self._zero_norm_tol = zero_norm_tol
        self._channel_tol = channel_tol
        self.validate()

    @classmethod
    def default(cls):
        return cls()

    @classmethod
    def try_new(
        cls,
        trace_tol,
        hermitian_tol,
        psd_tol,
        unitary_tol,
        weight_sum_tol,
        zero_norm_tol,
        channel_tol,
    ):
        cfg = cls(
            trace_tol=trace_tol,
            hermitian_tol=hermitian_tol,
            psd_tol=psd_tol,
            unitary_tol=unitary_tol,
            weight_sum_tol=weight_sum_tol,
            zero_norm_tol=zero_norm_tol,
            channel_tol=channel_tol,
        )
        return cfg

    def trace_tol(self):
        return self._trace_tol

    def hermitian_tol(self):
        return self._hermitian_tol

    def psd_tol(self):
        return self._psd_tol

    def unitary_tol(self):
        return self._unitary_tol

    def weight_sum_tol(self):
        return self._weight_sum_tol

    def zero_norm_tol(self):
        return self._zero_norm_tol

    def channel_tol(self):
        return self._channel_tol

    def validate(self):
        tolerances = [
            ("trace_tol", self._trace_tol),
            ("hermitian_tol", self._hermitian_tol),
            ("psd_tol", self._psd_tol),
            ("unitary_tol", self._unitary_tol),
            ("weight_sum_tol", self._weight_sum_tol),
            ("zero_norm_tol", self._zero_norm_tol),
            ("channel_tol", self._channel_tol),
        ]
        for name, tol in tolerances:
            if not math.isfinite(tol):
                raise NonFiniteTolerance(f"non-finite tolerance for {name}: {tol}")
            if tol <= 0.0:
                raise InvalidTolerance(f"invalid tolerance for {name}: {tol}")
        if self._psd_tol < self._hermitian_tol:
            raise InvalidTolerance(
                f"psd_tol {self._psd_tol} cannot be less than hermitian_tol {self._hermitian_tol}"
            )


class DensityMatrixValidationReport:
    def __init__(self, trace, hermitian_defect, min_eigenvalue, config):
        self._trace = trace
        self._hermitian_defect = hermitian_defect
        self._min_eigenvalue = min_eigenvalue
        self._config = config

    def trace(self):
        return self._trace

    def hermitian_defect(self):
        return self._hermitian_defect

    def min_eigenvalue(self):
        return self._min_eigenvalue

    def config(self):
        return self._config


class DensityMatrixCandidate:
    def __init__(self, dim: int, rho: np.ndarray):
        self._dim = dim
        self._rho = rho

    @classmethod
    def from_raw(cls, dim: int, data_vec: list):
        if dim == 0:
            raise ZeroDimension("density matrix dimension must be positive")
        expected = dim * dim
        if len(data_vec) != expected:
            raise ShapeMismatch(
                f"density matrix data length mismatch: expected {expected}, actual {len(data_vec)}"
            )

        for index, value in enumerate(data_vec):
            z = complex(value)
            if not (math.isfinite(z.real) and math.isfinite(z.imag)):
                raise NonFiniteEntry(
                    f"density matrix contains non-finite entry at index {index}"
                )

        arr = np.array(data_vec, dtype=complex).reshape((dim, dim))
        return cls(dim, arr)

    @classmethod
    def from_rho(cls, rho: np.ndarray):
        dim = rho.shape[0]
        if dim == 0:
            raise ZeroDimension("density matrix dimension must be positive")
        if rho.shape[1] != dim:
            raise ShapeMismatch("rho is not square")
        return cls(dim, rho)

    def validate(self, config: DensityMatrixConfig):
        config.validate()
        trace = np.trace(self._rho).real
        if abs(trace - 1.0) > config.trace_tol():
            raise TraceNotOne(f"trace not one: trace={trace}, tol={config.trace_tol()}")

        diff = self._rho - self._rho.conj().T
        defect = np.linalg.norm(diff)
        if defect > config.hermitian_tol():
            raise NonHermitian(f"non-hermitian matrix; defect={defect}")

        eigenvalues = np.linalg.eigh(self._rho)[0]
        min_eigenvalue = np.min(eigenvalues)
        if min_eigenvalue < -config.psd_tol():
            raise NotPositiveSemidefinite(
                f"not positive semidefinite; min_eigenvalue={min_eigenvalue}, tol={config.psd_tol()}"
            )

        report = DensityMatrixValidationReport(trace, defect, min_eigenvalue, config)
        return NumericalDensityMatrix(self._dim, self._rho, report)

    def diagnostic_hermitian_project(self):
        self._rho = (self._rho + self._rho.conj().T) / 2.0
        return self

    def dim(self):
        return self._dim

    def rho(self):
        return self._rho

    def into_rho(self):
        return self._rho


class NumericalDensityMatrix:
    def __init__(
        self, dim: int, rho: np.ndarray, validation: DensityMatrixValidationReport
    ):
        self._dim = dim
        self._rho = rho
        self._validation = validation

    @classmethod
    def from_validated(cls, dim: int, data_vec: list, config: DensityMatrixConfig):
        candidate = DensityMatrixCandidate.from_raw(dim, data_vec)
        return candidate.validate(config)

    def dim(self) -> int:
        return self._dim

    def dimension(self) -> int:
        return self._dim

    def rho(self) -> np.ndarray:
        return self._rho

    def validation_report(self) -> DensityMatrixValidationReport:
        return self._validation

    def into_rho(self) -> np.ndarray:
        return self._rho

    @classmethod
    def maximally_mixed(cls, dim: int):
        return cls.try_maximally_mixed(dim)

    @classmethod
    def try_maximally_mixed(cls, dim: int):
        if dim == 0:
            raise ZeroDimension("density matrix dimension must be positive")
        rho = np.eye(dim, dtype=complex) / dim
        candidate = DensityMatrixCandidate.from_rho(rho)
        return candidate.validate(DensityMatrixConfig.default())

    @classmethod
    def from_amplitudes(cls, psi: list, config: DensityMatrixConfig):
        config.validate()
        dim = len(psi)
        if dim == 0:
            raise ZeroDimension("density matrix dimension must be positive")

        psi_arr = np.array(psi, dtype=complex)
        norm2 = np.sum(np.abs(psi_arr) ** 2)
        if abs(norm2 - 1.0) > config.trace_tol():
            raise TraceNotOne(f"trace not one: trace={norm2}, tol={config.trace_tol()}")

        rho = np.outer(psi_arr, psi_arr.conj())
        candidate = DensityMatrixCandidate.from_rho(rho)
        return candidate.validate(config)

    @classmethod
    def from_cvector_checked(cls, psi: np.ndarray, config: DensityMatrixConfig):
        config.validate()
        dim = len(psi)
        if dim == 0:
            raise ZeroDimension()
        norm2 = np.sum(np.abs(psi) ** 2)
        if abs(norm2 - 1.0) > config.trace_tol():
            raise TraceNotOne(f"trace not one: trace={norm2}, tol={config.trace_tol()}")

        rho = np.outer(psi, psi.conj())
        candidate = DensityMatrixCandidate.from_rho(rho)
        return candidate.validate(config)

    @classmethod
    def from_cvector(cls, psi: np.ndarray):
        return cls.from_cvector_checked(psi, DensityMatrixConfig.default())

    @classmethod
    def from_diagonal_probs(cls, probs: list, config: DensityMatrixConfig):
        config.validate()
        dim = len(probs)
        if dim == 0:
            raise ZeroDimension()

        for index, value in enumerate(probs):
            if not math.isfinite(value):
                raise NonFiniteEntry(f"non-finite entry at index {index}")
            if value < 0.0:
                raise NegativeProbability(
                    f"negative probability at index {index}: {value}"
                )

        sum_p = sum(probs)
        if abs(sum_p - 1.0) > config.trace_tol():
            raise TraceNotOne(f"trace not one: trace={sum_p}, tol={config.trace_tol()}")

        rho = np.diag(probs).astype(complex)
        candidate = DensityMatrixCandidate.from_rho(rho)
        return candidate.validate(config)

    def trace(self) -> float:
        return self._validation.trace()

    def purity(self) -> float:
        return np.trace(self._rho @ self._rho).real

    def l1_coherence(self) -> float:
        total = 0.0
        for i in range(self._dim):
            for j in range(self._dim):
                if i != j:
                    total += abs(self._rho[i, j])
        return total

    def approximate_eigenvalues(self) -> list:
        eigenvalues = np.linalg.eigh(self._rho)[0]
        return sorted(eigenvalues.tolist(), reverse=True)

    def von_neumann_entropy(self) -> float:
        config = self._validation.config()
        entropy = 0.0
        for val in self.approximate_eigenvalues():
            if val < -config.psd_tol():
                raise NotPositiveSemidefinite(
                    f"not positive semidefinite; min_eigenvalue={val}, tol={config.psd_tol()}"
                )
            if val > 0.0:
                entropy += -val * math.log(val)
        return entropy

    def entropy_bits(self) -> float:
        return self.von_neumann_entropy() / math.log(2.0)

    def partial_trace_b(self, dim_a: int, dim_b: int):
        if self._dim != dim_a * dim_b:
            raise DimensionMismatch()

        reshaped = self._rho.reshape((dim_a, dim_b, dim_a, dim_b))
        reduced = np.trace(reshaped, axis1=1, axis2=3)
        candidate = DensityMatrixCandidate.from_rho(reduced)
        return candidate.validate(self._validation.config())

    def partial_trace_a(self, dim_a: int, dim_b: int):
        if self._dim != dim_a * dim_b:
            raise DimensionMismatch()

        reshaped = self._rho.reshape((dim_a, dim_b, dim_a, dim_b))
        reduced = np.trace(reshaped, axis1=0, axis2=2)
        candidate = DensityMatrixCandidate.from_rho(reduced)
        return candidate.validate(self._validation.config())

    def trace_distance(self, other: "NumericalDensityMatrix") -> float:
        diff = self._rho - other._rho
        eigenvalues = np.linalg.eigh(diff)[0]
        return 0.5 * np.sum(np.abs(eigenvalues))

    def projection_distortion(self, other: "NumericalDensityMatrix") -> float:
        return float(np.linalg.norm(self._rho - other._rho))

    @classmethod
    def try_mixture(cls, components: list, config: DensityMatrixConfig):
        config.validate()
        if not components:
            raise NoValidStates()

        sum_w = sum(w for _, w in components)
        if not math.isfinite(sum_w):
            raise NonPhysical()
        if abs(sum_w - 1.0) > config.weight_sum_tol():
            raise WeightSumNotOne(f"weight sum not one: sum={sum_w}")

        dim = components[0][0].dim()
        rho = np.zeros((dim, dim), dtype=complex)
        for index, (comp, weight) in enumerate(components):
            if not math.isfinite(weight):
                raise NonPhysical()
            if weight < 0.0:
                raise NegativeWeight(f"negative weight: index {index}, value {weight}")
            if comp.dim() != dim:
                raise DimensionMismatch()
            rho += comp.rho() * weight

        candidate = DensityMatrixCandidate.from_rho(rho)
        return candidate.validate(config)

    def get(self, i: int, j: int) -> complex:
        if i >= self._dim or j >= self._dim:
            raise DimensionMismatch()
        return self._rho[i, j]

    def to_complex(self) -> list:
        return self._rho.flatten().tolist()

    def pure(self) -> bool:
        return bool(abs(self.purity() - 1.0) < self._validation.config().trace_tol())

    @classmethod
    def from_embedding(cls, embedding: list, phase_fn, config: DensityMatrixConfig):
        config.validate()
        if not embedding:
            raise ZeroDimension()

        psi = np.zeros(len(embedding), dtype=complex)
        for index, x in enumerate(embedding):
            if not math.isfinite(x):
                raise NonFiniteEntry(f"non-finite entry at index {index}")
            phase = phase_fn(index, x) if phase_fn else 0.0
            if not math.isfinite(phase):
                raise NonPhysical()
            psi[index] = x * math.cos(phase) + 1j * x * math.sin(phase)

        norm = np.linalg.norm(psi)
        if norm <= config.zero_norm_tol():
            raise ZeroVector()
        psi /= norm
        return cls.from_cvector_checked(psi, config)

    @classmethod
    def diagnostic_from_graph_laplacian(cls, laplacian: list, dim: int):
        if dim == 0:
            raise ZeroDimension()
        if len(laplacian) != dim * dim:
            raise ShapeMismatch()
        if any(not math.isfinite(x) for x in laplacian):
            raise NonPhysical()

        rho = np.array(laplacian, dtype=complex).reshape((dim, dim))
        trace = np.trace(rho).real
        if trace <= 1e-12:
            raise TraceNotOne(f"trace not one: trace={trace}, tol=1e-12")
        rho /= trace
        return DensityMatrixCandidate.from_rho(rho)

    @classmethod
    def try_from_bloch(cls, vector: list):
        x, y, z = vector
        if not (math.isfinite(x) and math.isfinite(y) and math.isfinite(z)):
            raise NonPhysical()

        config = DensityMatrixConfig.default()
        radius = math.sqrt(x * x + y * y + z * z)
        if radius > 1.0 + config.psd_tol():
            raise NotPositiveSemidefinite(
                f"not positive semidefinite; min_eigenvalue={(1.0 - radius) / 2.0}, tol={config.psd_tol()}"
            )

        rho = np.zeros((2, 2), dtype=complex)
        rho[0, 0] = 1.0 + z
        rho[0, 1] = x - 1j * y
        rho[1, 0] = x + 1j * y
        rho[1, 1] = 1.0 - z
        rho /= 2.0
        candidate = DensityMatrixCandidate.from_rho(rho)
        return candidate.validate(config)

    def apply_kraus(self, operators: list, config: DensityMatrixConfig):
        config.validate()
        if not operators:
            raise NoValidStates()

        completeness = np.zeros((self._dim, self._dim), dtype=complex)
        for op in operators:
            if op.shape != (self._dim, self._dim):
                raise InvalidKrausShape(
                    f"invalid kraus shape: expected {self._dim}, actual {op.shape[0]}"
                )
            completeness += op.conj().T @ op

        defect = np.linalg.norm(completeness - np.eye(self._dim))
        if defect > config.channel_tol():
            raise NonTracePreservingChannel(
                f"Kraus operators are not trace preserving; defect={defect}"
            )

        rho = np.zeros((self._dim, self._dim), dtype=complex)
        for op in operators:
            rho += op @ self._rho @ op.conj().T

        candidate = DensityMatrixCandidate.from_rho(rho)
        return candidate.validate(config)

    def to_real_block(self) -> np.ndarray:
        block = np.zeros((2 * self._dim, 2 * self._dim), dtype=float)
        for i in range(self._dim):
            for j in range(self._dim):
                z = self._rho[i, j]
                block[i, j] = z.real
                block[i, j + self._dim] = -z.imag
                block[i + self._dim, j] = z.imag
                block[i + self._dim, j + self._dim] = z.real
        return block


def try_normalize_density(dim: int, data: list, config: DensityMatrixConfig):
    config.validate()
    candidate = DensityMatrixCandidate.from_raw(dim, data)
    trace = np.trace(candidate.rho()).real
    if trace > 1e-30:
        candidate = DensityMatrixCandidate.from_rho(candidate.into_rho() / trace)
    return candidate.validate(config)


ComplexDensityMatrix = NumericalDensityMatrix
DensityMatrix = NumericalDensityMatrix

