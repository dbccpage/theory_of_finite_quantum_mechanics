"""Spin chain models, Pauli operators, and Hilbert space metrics for CAQD.

Provides constructors for 1D Transverse-Field Ising Models (TFIM) and
XXZ Heisenberg chains, along with exact partial traces, Schatten-1 norms,
and physical observables.

AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Sequence, Tuple
import numpy as np
import scipy.linalg


# Single-qubit Pauli matrices (2x2 complex numpy arrays)
I2 = np.array([[1.0, 0.0], [0.0, 1.0]], dtype=complex)
SIGMA_X = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
SIGMA_Y = np.array([[0.0, -1.0j], [1.0j, 0.0]], dtype=complex)
SIGMA_Z = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)


def validate_times(times: Sequence[float]) -> np.ndarray:
    """Require a finite, nonempty, nondecreasing sampling grid."""
    result = np.asarray(times, dtype=float)
    if result.ndim != 1 or not len(result) or not np.all(np.isfinite(result)) or np.any(np.diff(result) < 0):
        raise ValueError("t_span must be a nonempty finite nondecreasing sequence")
    return result


def validate_density_matrix(rho: np.ndarray, dim: int, tol: float = 1e-10) -> np.ndarray:
    """Validate the finite density-matrix domain; allow roundoff at tolerance."""
    result = np.array(rho, dtype=complex, copy=True)
    if result.shape != (dim, dim) or not np.all(np.isfinite(result)):
        raise ValueError(f"density matrix must be finite with shape ({dim}, {dim})")
    if not np.allclose(result, result.conj().T, atol=tol, rtol=0):
        raise ValueError("density matrix must be Hermitian")
    if not np.isclose(np.trace(result), 1, atol=tol, rtol=0):
        raise ValueError("density matrix must have unit trace")
    if scipy.linalg.eigvalsh(result).min() < -tol:
        raise ValueError("density matrix must be positive semidefinite")
    return result


def pauli_matrices() -> dict[str, np.ndarray]:
    """Return dictionary of single-qubit Pauli matrices."""
    return {"I": I2.copy(), "X": SIGMA_X.copy(), "Y": SIGMA_Y.copy(), "Z": SIGMA_Z.copy()}


def operator_norm(O: np.ndarray) -> float:
    """Compute operator norm (spectral norm, ||O||_inf = largest singular value)."""
    s = scipy.linalg.svdvals(O)
    return float(np.max(s)) if len(s) > 0 else 0.0


def trace_norm(X: np.ndarray) -> float:
    """Compute Schatten-1 trace norm (||X||_1 = sum of singular values)."""
    s = scipy.linalg.svdvals(X)
    return float(np.sum(s))


def hilbert_schmidt_norm(X: np.ndarray) -> float:
    """Compute Hilbert-Schmidt (Frobenius) norm ||X||_HS = sqrt(Tr(X^dagger X))."""
    return float(np.sqrt(np.real(np.trace(X.conj().T @ X))))


def pauli_on_site(op: np.ndarray, site: int, num_sites: int) -> np.ndarray:
    """Embed single-site operator `op` at `site` in a chain of `num_sites` qubits."""
    if not (0 <= site < num_sites):
        raise ValueError(f"Site {site} out of range for {num_sites} sites.")
    res = np.array([[1.0]], dtype=complex)
    for i in range(num_sites):
        curr = op if i == site else I2
        res = np.kron(res, curr)
    return res


def two_body_op(op1: np.ndarray, op2: np.ndarray, site1: int, site2: int, num_sites: int) -> np.ndarray:
    """Embed two single-site operators on site1 and site2 in a chain of `num_sites` qubits."""
    if site1 == site2:
        raise ValueError(f"Sites must be distinct, got site1={site1}, site2={site2}.")
    if not (0 <= site1 < num_sites and 0 <= site2 < num_sites):
        raise ValueError(f"Sites ({site1}, {site2}) out of range for {num_sites} sites.")
    res = np.array([[1.0]], dtype=complex)
    for i in range(num_sites):
        if i == site1:
            curr = op1
        elif i == site2:
            curr = op2
        else:
            curr = I2
        res = np.kron(res, curr)
    return res


def partial_trace(rho: np.ndarray, keep_sites: Sequence[int], num_sites: int, d: int = 2) -> np.ndarray:
    """Compute reduced density matrix by tracing out sites not in `keep_sites`.
    
    Args:
        rho: Density matrix of dimension (d^num_sites, d^num_sites).
        keep_sites: Sequence of site indices to keep.
        num_sites: Total number of sites in the chain.
        d: Local site Hilbert space dimension (default 2 for qubits).
        
    Returns:
        Reduced density matrix of shape (d^k, d^k) where k = len(keep_sites).
    """
    keep = sorted(list(keep_sites))
    if len(set(keep)) != len(keep) or any(not isinstance(i, (int, np.integer)) or isinstance(i, bool)
                                       or not 0 <= i < num_sites for i in keep):
        raise ValueError("keep_sites must contain distinct valid site indices")
    if np.shape(rho) != (d**num_sites, d**num_sites):
        raise ValueError("rho shape does not match the declared subsystem dimensions")
    k = len(keep)
    if k == num_sites:
        return rho.copy()
    if k == 0:
        return np.array([[np.trace(rho)]], dtype=complex)
    
    trace_out = [i for i in range(num_sites) if i not in keep]
    
    # Reshape into tensor with indices (row_0, ..., row_{N-1}, col_0, ..., col_{N-1})
    shape = [d] * (2 * num_sites)
    tensor = rho.reshape(shape)
    
    # Trace out indices in trace_out from highest to lowest to avoid index shifting
    for site in sorted(trace_out, reverse=True):
        tensor = np.trace(tensor, axis1=site, axis2=site + num_sites)
        num_sites -= 1
        
    dim_keep = d ** k
    return tensor.reshape((dim_keep, dim_keep))


@dataclass(frozen=True)
class LocalTerm:
    """Represents a local term in a Hamiltonian."""
    term_type: str        # e.g. "1-local" or "2-local"
    sites: Tuple[int, ...] # tuple of site indices
    matrix: np.ndarray    # matrix on the local subsystem
    full_matrix: np.ndarray # matrix embedded into full Hilbert space


class SpinChainModel:
    """Base class for 1D spin chain models."""
    def __init__(self, num_sites: int, periodic: bool = False):
        if num_sites < 2:
            raise ValueError(f"Number of sites N must be >= 2, got {num_sites}.")
        self.num_sites = num_sites
        self.dim = 2 ** num_sites
        self.periodic = periodic
        self.terms: List[LocalTerm] = []
        self._H: np.ndarray | None = None

    @property
    def H(self) -> np.ndarray:
        """Full system Hamiltonian matrix."""
        if self._H is None:
            self._H = sum((term.full_matrix for term in self.terms), np.zeros((self.dim, self.dim), dtype=complex))
        return self._H

    @property
    def edges(self) -> List[Tuple[int, int]]:
        """List of interacting edges (a, b) in the lattice."""
        edg = [(i, i + 1) for i in range(self.num_sites - 1)]
        if self.periodic:
            edg.append((self.num_sites - 1, 0))
        return edg

    def get_terms_for_edge(self, edge: Tuple[int, int]) -> List[LocalTerm]:
        """Return Hamiltonian terms acting across `edge`."""
        a, b = edge
        # Ordered bonds distinguish the two declared periodic N=2 terms.
        # Matching both orientations here counted each term twice per site.
        return [t for t in self.terms if t.term_type == "2-local" and t.sites == (a, b)]

    def get_terms_for_site(self, site: int) -> List[LocalTerm]:
        """Return 1-local Hamiltonian terms acting strictly at `site`."""
        return [t for t in self.terms if t.term_type == "1-local" and t.sites == (site,)]


class TFIMChain(SpinChainModel):
    """1D Transverse-Field Ising Model:
    
    H = -J sum_{i=0}^{N-2} sigma_i^z sigma_{i+1}^z - h sum_{i=0}^{N-1} sigma_i^x
    """
    def __init__(self, num_sites: int, J: float = 1.0, h: float = 1.0, periodic: bool = False):
        super().__init__(num_sites, periodic)
        self.J = float(J)
        self.h = float(h)
        self._build_terms()

    def _build_terms(self) -> None:
        N = self.num_sites
        # 1-local transverse field terms: -h sigma_x
        for i in range(N):
            m_loc = -self.h * SIGMA_X
            m_full = pauli_on_site(m_loc, i, N)
            self.terms.append(LocalTerm(term_type="1-local", sites=(i,), matrix=m_loc, full_matrix=m_full))

        # 2-local Ising interaction terms: -J sigma_z sigma_z
        num_bonds = N if self.periodic else N - 1
        for i in range(num_bonds):
            j = (i + 1) % N
            m_loc = -self.J * np.kron(SIGMA_Z, SIGMA_Z)
            m_full = two_body_op(-self.J * SIGMA_Z, SIGMA_Z, i, j, N)
            self.terms.append(LocalTerm(term_type="2-local", sites=(i, j), matrix=m_loc, full_matrix=m_full))


class XXZChain(SpinChainModel):
    """1D XXZ Heisenberg Spin Chain:
    
    H = -J sum_{i=0}^{N-2} (sigma_i^x sigma_{i+1}^x + sigma_i^y sigma_{i+1}^y + delta sigma_i^z sigma_{i+1}^z)
        - h sum_{i=0}^{N-1} sigma_i^z
    """
    def __init__(self, num_sites: int, J: float = 1.0, delta: float = 1.0, h: float = 0.2, periodic: bool = False):
        super().__init__(num_sites, periodic)
        self.J = float(J)
        self.delta = float(delta)
        self.h = float(h)
        self._build_terms()

    def _build_terms(self) -> None:
        N = self.num_sites
        # 1-local longitudinal magnetic field: -h sigma_z
        if abs(self.h) > 1e-14:
            for i in range(N):
                m_loc = -self.h * SIGMA_Z
                m_full = pauli_on_site(m_loc, i, N)
                self.terms.append(LocalTerm(term_type="1-local", sites=(i,), matrix=m_loc, full_matrix=m_full))

        # 2-local XXZ exchange terms: -J (XX + YY + delta ZZ)
        num_bonds = N if self.periodic else N - 1
        for i in range(num_bonds):
            j = (i + 1) % N
            m_loc = -self.J * (
                np.kron(SIGMA_X, SIGMA_X) +
                np.kron(SIGMA_Y, SIGMA_Y) +
                self.delta * np.kron(SIGMA_Z, SIGMA_Z)
            )
            m_full = (
                two_body_op(-self.J * SIGMA_X, SIGMA_X, i, j, N) +
                two_body_op(-self.J * SIGMA_Y, SIGMA_Y, i, j, N) +
                two_body_op(-self.J * self.delta * SIGMA_Z, SIGMA_Z, i, j, N)
            )
            self.terms.append(LocalTerm(term_type="2-local", sites=(i, j), matrix=m_loc, full_matrix=m_full))


# Standard Observables
def staggered_magnetization(num_sites: int) -> np.ndarray:
    """Return staggered magnetization operator M_stag = (1/N) sum_i (-1)^i sigma_i^z."""
    res = np.zeros((2**num_sites, 2**num_sites), dtype=complex)
    for i in range(num_sites):
        sign = (-1.0) ** i
        res += (sign / num_sites) * pauli_on_site(SIGMA_Z, i, num_sites)
    return res


def center_correlation(num_sites: int) -> np.ndarray:
    """Return nearest-neighbor sigma^z correlation across center bond."""
    mid = num_sites // 2
    return two_body_op(SIGMA_Z, SIGMA_Z, mid - 1, mid, num_sites)


def transverse_magnetization(num_sites: int) -> np.ndarray:
    """Return total transverse magnetization operator M_x = (1/N) sum_i sigma_i^x."""
    res = np.zeros((2**num_sites, 2**num_sites), dtype=complex)
    for i in range(num_sites):
        res += (1.0 / num_sites) * pauli_on_site(SIGMA_X, i, num_sites)
    return res


# Standard Initial States
def neel_state(num_sites: int) -> np.ndarray:
    """Return pure Néel density matrix |1010...> <1010...|."""
    # Basis: |0> = [1, 0]^T, |1> = [0, 1]^T
    ket0 = np.array([1.0, 0.0], dtype=complex)
    ket1 = np.array([0.0, 1.0], dtype=complex)
    psi = np.array([1.0], dtype=complex)
    for i in range(num_sites):
        curr = ket1 if i % 2 == 0 else ket0
        psi = np.kron(psi, curr)
    return np.outer(psi, psi.conj())


def polarized_x_state(num_sites: int) -> np.ndarray:
    """Return pure +X polarized state |+...+> <+...+|."""
    plus = np.array([1.0, 1.0], dtype=complex) / np.sqrt(2.0)
    psi = np.array([1.0], dtype=complex)
    for _ in range(num_sites):
        psi = np.kron(psi, plus)
    return np.outer(psi, psi.conj())


def all_up_state(num_sites: int) -> np.ndarray:
    """Return pure ferromagnetic ground state |0...0> <0...0|."""
    ket0 = np.array([1.0, 0.0], dtype=complex)
    psi = np.array([1.0], dtype=complex)
    for _ in range(num_sites):
        psi = np.kron(psi, ket0)
    return np.outer(psi, psi.conj())
