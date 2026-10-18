"""Operational quantum-information tools above density matrices.

Faithful port of ``crates/omega_engine.crates.engine/src/quantum/quantum_information_engine.rs``.

POVMs (measurement effects + Born probabilities) and the truncated-Fock Wigner
function. Computational infrastructure only -- no accept/reject authority.
"""

from __future__ import annotations
import math
from typing import List

import numpy as np

CONTRACT_ID = "urn:omega:qm:quantum_information_engine:file:v1.0.0"
AUTHORITY_EFFECT = "None"

DEFAULT_TOLERANCE = 1e-9
EPSILON_QUANTUM_EIGEN = 1e-9


class QuantumInfoError(Exception):
    pass


class QuantumBackendUnrequestedRefused(QuantumInfoError):
    def __init__(self, msg="QUANTUM_BACKEND_UNREQUESTED_REFUSED"):
        super().__init__(msg)
        self.refusal_route = "QUANTUM_BACKEND_UNREQUESTED_REFUSED"


def assert_quantum_carrier_admitted(quantum_carrier_admitted: bool = False):
    if not quantum_carrier_admitted:
        raise QuantumBackendUnrequestedRefused()


class EmptyPovm(QuantumInfoError):
    pass


class EmptyGrid(QuantumInfoError):
    pass


class NonSquareMatrix(QuantumInfoError):
    pass


class DimensionMismatch(QuantumInfoError):
    pass


class PovmDoesNotSumToIdentity(QuantumInfoError):
    pass


class PovmElementNotPositive(QuantumInfoError):
    pass


class NonHermitianEffect(QuantumInfoError):
    pass


def _ensure_square(m: np.ndarray) -> None:
    if m.ndim != 2 or m.shape[0] != m.shape[1]:
        raise NonSquareMatrix(f"matrix must be square, got {m.shape}")


def _identity(dim: int) -> np.ndarray:
    return np.eye(dim, dtype=complex)


def _max_entry_norm(m: np.ndarray) -> float:
    if m.size == 0:
        return 0.0
    return float(np.max(np.abs(m)))


def _max_hermitian_error(m: np.ndarray) -> float:
    return _max_entry_norm(m - m.conj().T)


def _min_hermitian_eigenvalue(m: np.ndarray) -> float:
    herm = 0.5 * (m + m.conj().T)
    return float(np.min(np.linalg.eigvalsh(herm)))


class Povm:
    def __init__(
        self, elements: List[np.ndarray], tolerance: float = DEFAULT_TOLERANCE
    ):
        if not elements:
            raise EmptyPovm("POVM must contain at least one effect")
        self._elements = [np.asarray(e, dtype=complex) for e in elements]
        _ensure_square(self._elements[0])
        self._dim = self._elements[0].shape[0]
        self._tolerance = max(tolerance, EPSILON_QUANTUM_EIGEN)
        self._validate()

    @classmethod
    def new(cls, elements: List[np.ndarray]) -> "Povm":
        return cls(elements)

    @classmethod
    def with_tolerance(cls, elements: List[np.ndarray], tolerance: float) -> "Povm":
        return cls(elements, tolerance)

    @classmethod
    def computational_basis(cls, dim: int) -> "Povm":
        if dim == 0:
            raise DimensionMismatch("dimension mismatch: expected 1, got 0")
        elements = []
        for i in range(dim):
            e = np.zeros((dim, dim), dtype=complex)
            e[i, i] = 1.0
            elements.append(e)
        return cls(elements)

    @classmethod
    def qubit_unsharp_z(cls, sharpness: float) -> "Povm":
        eta = min(max(sharpness, 0.0), 1.0)
        e0 = np.zeros((2, 2), dtype=complex)
        e1 = np.zeros((2, 2), dtype=complex)
        e0[0, 0] = (1.0 + eta) * 0.5
        e0[1, 1] = (1.0 - eta) * 0.5
        e1[0, 0] = (1.0 - eta) * 0.5
        e1[1, 1] = (1.0 + eta) * 0.5
        return cls([e0, e1])

    def dim(self) -> int:
        return self._dim

    def len(self) -> int:
        return len(self._elements)

    def __len__(self) -> int:
        return len(self._elements)

    def is_empty(self) -> bool:
        return len(self._elements) == 0

    def elements(self) -> List[np.ndarray]:
        return self._elements

    def apply_matrix(self, rho: np.ndarray) -> List[float]:
        rho = np.asarray(rho, dtype=complex)
        _ensure_square(rho)
        if rho.shape[0] != self._dim:
            raise DimensionMismatch(
                f"dimension mismatch: expected {self._dim}, got {rho.shape[0]}"
            )
        probabilities = []
        for effect in self._elements:
            trace = np.trace(effect @ rho)
            cleaned = 0.0 if abs(trace.real) < self._tolerance else trace.real
            probabilities.append(max(cleaned, 0.0))
        return probabilities

    def apply(self, rho) -> List[float]:
        if hasattr(rho, "rho"):
            return self.apply_matrix(rho.rho())
        return self.apply_matrix(rho)

    def _validate(self) -> None:
        total = np.zeros((self._dim, self._dim), dtype=complex)
        for index, effect in enumerate(self._elements):
            _ensure_square(effect)
            if effect.shape[0] != self._dim:
                raise DimensionMismatch(
                    f"dimension mismatch: expected {self._dim}, got {effect.shape[0]}"
                )
            herm_error = _max_hermitian_error(effect)
            if herm_error > self._tolerance:
                raise NonHermitianEffect(
                    f"POVM effect {index} is not Hermitian, max error {herm_error}"
                )
            min_ev = _min_hermitian_eigenvalue(effect)
            if min_ev < -self._tolerance:
                raise PovmElementNotPositive(
                    f"POVM effect {index} is not positive semidefinite, min eigenvalue {min_ev}"
                )
            total += effect
        max_error = _max_entry_norm(total - _identity(self._dim))
        if max_error > self._tolerance:
            raise PovmDoesNotSumToIdentity(
                f"POVM effects do not sum to identity, max error {max_error}"
            )


class WignerGrid:
    def __init__(
        self, q_points: List[float], p_points: List[float], values: np.ndarray
    ):
        self.q_points = list(q_points)
        self.p_points = list(p_points)
        self.values = values  

    def negativity_volume(self) -> float:
        if len(self.q_points) < 2 or len(self.p_points) < 2:
            return 0.0
        dq = _average_spacing(self.q_points)
        dp = _average_spacing(self.p_points)
        neg = self.values[self.values < 0.0]
        return float(np.sum(-neg * dq * dp))


def _average_spacing(points: List[float]) -> float:
    if len(points) < 2:
        return 0.0
    total = sum(abs(points[i + 1] - points[i]) for i in range(len(points) - 1))
    return total / (len(points) - 1)


def _associated_laguerre(n: int, k: int, x: float) -> float:
    if n == 0:
        return 1.0
    if n == 1:
        return 1.0 + k - x
    l_nm2 = 1.0
    l_nm1 = 1.0 + k - x
    for current in range(2, n + 1):
        c = float(current)
        nxt = ((2.0 * c - 1.0 + k - x) * l_nm1 - (c - 1.0 + k) * l_nm2) / c
        l_nm2 = l_nm1
        l_nm1 = nxt
    return l_nm1


def _sqrt_factorial_ratio(n: int, m: int) -> float:
    if n == m:
        return 1.0
    acc = 1.0
    for value in range(n + 1, m + 1):
        acc /= value
    return math.sqrt(acc)


def _wigner_fock_kernel(m: int, n: int, alpha: complex) -> complex:
    if m < n:
        return _wigner_fock_kernel(n, m, alpha).conjugate()
    k = m - n
    radius = abs(alpha) ** 2
    laguerre = _associated_laguerre(n, k, 4.0 * radius)
    parity = 1.0 if n % 2 == 0 else -1.0
    coeff = (
        parity
        * _sqrt_factorial_ratio(n, m)
        * math.exp(-2.0 * radius)
        * laguerre
        * 2.0
        / math.pi
    )
    return coeff * ((2.0 * alpha) ** k)


def wigner_qp_point(rho: np.ndarray, q: float, p: float, cutoff: int) -> float:
    rho = np.asarray(rho, dtype=complex)
    _ensure_square(rho)
    if cutoff == 0 or cutoff > rho.shape[0]:
        raise DimensionMismatch(
            f"dimension mismatch: expected {rho.shape[0]}, got {cutoff}"
        )
    alpha = complex(q, p) / math.sqrt(2.0)
    w_alpha = 0.0 + 0.0j
    for m in range(cutoff):
        for n in range(cutoff):
            w_alpha += rho[m, n] * _wigner_fock_kernel(m, n, alpha)
    val = 0.5 * w_alpha.real
    return float(min(max(val, -1.0 / math.pi), 1.0 / math.pi))


def wigner_matrix(
    rho: np.ndarray, q_points: List[float], p_points: List[float]
) -> WignerGrid:
    rho = np.asarray(rho, dtype=complex)
    _ensure_square(rho)
    if not q_points or not p_points:
        raise EmptyGrid("phase-space grids must be non-empty")
    cutoff = rho.shape[0]
    values = np.zeros((len(q_points), len(p_points)), dtype=float)
    for qi, q in enumerate(q_points):
        for pi, p in enumerate(p_points):
            values[qi, pi] = wigner_qp_point(rho, q, p, cutoff)
    return WignerGrid(q_points, p_points, values)


from omega_engine.crates.engine.base.eng_base import Engine


class QuantumInformationEngine(Engine):
    authority_effect = "None"
    implements = (CONTRACT_ID,)




