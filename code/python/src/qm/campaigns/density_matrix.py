from __future__ import annotations

from fractions import Fraction
from typing import Any, Sequence, Tuple
import numpy as np

from ..domain.gaussian_rational import Gaussian
from ..domain.primitives import (
    exact_dagger,
    exact_is_psd,
    exact_purity,
    exact_trace,
    is_exact_rational_density_matrix,
    to_exact_matrix,
)


class ExactDensityMatrix:
    """Exact rational density operator on C^d over Q(i).

    AuthorityEffect: None.

    Immutable state object accepted only when exactly square, Hermitian,
    positive semidefinite, and having trace exactly 1.
    """

    def __init__(self, matrix: Sequence[Sequence[Any]]) -> None:
        mat = to_exact_matrix(matrix)
        if not is_exact_rational_density_matrix(mat):
            raise ValueError(
                "Matrix is not an exact rational density operator "
                "(must be square, Hermitian, PSD, and have exact trace 1)"
            )
        self._dim = len(mat)
        self._entries = tuple(tuple(row) for row in mat)

    @property
    def dim(self) -> int:
        return self._dim

    @property
    def entries(self) -> tuple[tuple[Gaussian, ...], ...]:
        return self._entries

    def to_list(self) -> list[list[Gaussian]]:
        return [list(row) for row in self._entries]

    def to_fraction_list(self) -> list[list[Fraction]]:
        """Return real entries as Fractions, raising ValueError if any entry has non-zero imaginary component."""
        res = []
        for row in self._entries:
            row_fracs = []
            for g in row:
                if g.imag != 0:
                    raise ValueError(f"Entry {g} has nonzero imaginary component")
                row_fracs.append(g.real)
            res.append(row_fracs)
        return res

    def trace(self) -> Fraction:
        return Fraction(1, 1)

    def purity(self) -> Fraction:
        return exact_purity(self._entries)

    def is_pure(self) -> bool:
        return self.purity() == Fraction(1, 1)

    def expectation(self, operator: Sequence[Sequence[Any]]) -> Gaussian:
        """Exact expectation Tr(O rho) for an operator O."""
        op = to_exact_matrix(operator)
        if len(op) != self._dim:
            raise ValueError(f"Operator dimension mismatch: expected {self._dim}, got {len(op)}")
        tr = Gaussian.of(0)
        for i in range(self._dim):
            for j in range(self._dim):
                tr = tr + op[i][j] * self._entries[j][i]
        return tr

    @classmethod
    def pure(cls, state_vector: Sequence[Any]) -> ExactDensityMatrix:
        """Construct pure state Gram projector |psi><psi| / <psi|psi>."""
        vec = [Gaussian.of(v) for v in state_vector]
        norm_sq = sum((v * v.conjugate() for v in vec), Gaussian.of(0))
        if norm_sq.imag != 0 or norm_sq.real <= 0:
            raise ValueError("Zero amplitude vector has no ray")
        norm = norm_sq.real
        d = len(vec)
        entries = [
            [(vec[i] * vec[j].conjugate()) / norm for j in range(d)]
            for i in range(d)
        ]
        return cls(entries)

    @classmethod
    def maximally_mixed(cls, dim: int) -> ExactDensityMatrix:
        """Construct maximally mixed state I_d / d."""
        if dim < 1:
            raise ValueError("Dimension must be positive")
        inv_d = Fraction(1, dim)
        entries = [
            [Gaussian.of(inv_d) if i == j else Gaussian.of(0) for j in range(dim)]
            for i in range(dim)
        ]
        return cls(entries)

    @classmethod
    def mixture(
        cls, components: Sequence[tuple[Fraction | int, ExactDensityMatrix]]
    ) -> ExactDensityMatrix:
        """Construct convex mixture sum_i p_i rho_i."""
        if not components:
            raise ValueError("Mixture requires at least one component")
        d = components[0][1].dim
        weight_sum = Fraction(0)
        accum = [[Gaussian.of(0) for _ in range(d)] for _ in range(d)]
        for w, state in components:
            if state.dim != d:
                raise ValueError("All mixture components must share dimension")
            fw = Fraction(w)
            if fw < 0:
                raise ValueError(f"Negative mixture weight: {w}")
            weight_sum += fw
            gw = Gaussian.of(fw)
            for i in range(d):
                for j in range(d):
                    accum[i][j] = accum[i][j] + gw * state.entries[i][j]
        if weight_sum != Fraction(1, 1):
            raise ValueError(f"Mixture weights sum to {weight_sum}, not 1")
        return cls(accum)

    @classmethod
    def from_unnormalized(
        cls, matrix: Sequence[Sequence[Any]]
    ) -> tuple[ExactDensityMatrix, Fraction]:
        """Normalize an unnormalized PSD operator M: returns (M / Tr(M), Tr(M))."""
        mat = to_exact_matrix(matrix)
        if not exact_is_psd(mat):
            raise ValueError("Matrix is not positive semidefinite")
        tr = exact_trace(mat)
        if tr.imag != 0 or tr.real <= 0:
            raise ValueError("Non-positive trace has no normalisation")
        t_val = tr.real
        d = len(mat)
        norm_entries = [[mat[i][j] / t_val for j in range(d)] for i in range(d)]
        return cls(norm_entries), t_val

    def partial_trace_b(self, da: int = 2, db: int = 2) -> ExactDensityMatrix:
        """Partial trace over subsystem B: Tr_b(rho)."""
        if da * db != self._dim:
            raise ValueError(f"Dimension mismatch: {da}*{db} != {self._dim}")
        res = [[Gaussian.of(0) for _ in range(da)] for _ in range(da)]
        for i in range(da):
            for j in range(da):
                for k in range(db):
                    res[i][j] = res[i][j] + self._entries[i * db + k][j * db + k]
        return ExactDensityMatrix(res)

    def partial_trace_a(self, da: int = 2, db: int = 2) -> ExactDensityMatrix:
        """Partial trace over subsystem A: Tr_a(rho)."""
        if da * db != self._dim:
            raise ValueError(f"Dimension mismatch: {da}*{db} != {self._dim}")
        res = [[Gaussian.of(0) for _ in range(db)] for _ in range(db)]
        for i in range(db):
            for j in range(db):
                for k in range(da):
                    res[i][j] = res[i][j] + self._entries[k * db + i][k * db + j]
        return ExactDensityMatrix(res)

    def tensor(self, other: ExactDensityMatrix) -> ExactDensityMatrix:
        """Kronecker tensor product rho_A (x) rho_B."""
        da, db = self._dim, other.dim
        d = da * db
        res = [[Gaussian.of(0) for _ in range(d)] for _ in range(d)]
        for ia in range(da):
            for ja in range(da):
                ea = self._entries[ia][ja]
                for ib in range(db):
                    for jb in range(db):
                        eb = other.entries[ib][jb]
                        res[ia * db + ib][ja * db + jb] = ea * eb
        return ExactDensityMatrix(res)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ExactDensityMatrix):
            return False
        return self._entries == other.entries

    def __repr__(self) -> str:
        return f"ExactDensityMatrix(dim={self._dim}, entries={self._entries})"


def exact_born_probability(
    rho: ExactDensityMatrix | Sequence[Sequence[Any]],
    projection: Sequence[Sequence[Any]],
) -> Fraction:
    """Exact Born probability Tr(P rho) over Q."""
    rho_mat = rho.entries if isinstance(rho, ExactDensityMatrix) else to_exact_matrix(rho)
    p_mat = to_exact_matrix(projection)
    d = len(rho_mat)
    if len(p_mat) != d:
        raise ValueError(f"Dimension mismatch: state {d}x{d}, projector {len(p_mat)}x{len(p_mat)}")
    tr = Gaussian.of(0)
    for i in range(d):
        for j in range(d):
            tr = tr + p_mat[i][j] * rho_mat[j][i]
    if tr.imag != 0:
        raise ValueError("Born probability has nonzero imaginary component")
    return tr.real


def exact_measure_and_update(
    rho: ExactDensityMatrix | Sequence[Sequence[Any]],
    projection: Sequence[Sequence[Any]],
) -> tuple[Fraction, ExactDensityMatrix | None]:
    """Exact projective measurement and Lüders update.

    Returns (p, rho_post):
      - If p > 0: p in Q and rho_post is ExactDensityMatrix representing P rho P / p
      - If p == 0: Fraction(0) and None
    """
    p = exact_born_probability(rho, projection)
    if p <= Fraction(0):
        return Fraction(0), None

    rho_mat = rho.entries if isinstance(rho, ExactDensityMatrix) else to_exact_matrix(rho)
    p_mat = to_exact_matrix(projection)
    d = len(rho_mat)

    temp = [
        [sum((rho_mat[i][k] * p_mat[k][j] for k in range(d)), Gaussian.of(0)) for j in range(d)]
        for i in range(d)
    ]
    p_rho_p = [
        [sum((p_mat[i][k] * temp[k][j] for k in range(d)), Gaussian.of(0)) for j in range(d)]
        for i in range(d)
    ]
    p_gauss = Gaussian.of(p)
    post_entries = [[p_rho_p[i][j] / p_gauss for j in range(d)] for i in range(d)]
    return p, ExactDensityMatrix(post_entries)


def is_valid_density_matrix(rho: Any, tol: float | None = 1e-9) -> bool:
    """Validate whether rho is a density operator (backward compatible)."""
    if isinstance(rho, ExactDensityMatrix):
        return True
    if tol is None or tol == 0.0:
        return is_exact_rational_density_matrix(rho)
    if isinstance(rho, np.ndarray) and np.issubdtype(rho.dtype, np.inexact):
        if rho.ndim != 2 or rho.shape[0] != rho.shape[1]:
            return False
        if not bool(np.allclose(rho, rho.conj().T, rtol=0.0, atol=tol)):
            return False
        if not bool(np.isclose(np.trace(rho), 1.0, rtol=0.0, atol=tol)):
            return False
        evals = np.linalg.eigvalsh(rho)
        return bool(np.all(evals >= -tol))
    return is_exact_rational_density_matrix(rho)


def born_probability(rho: np.ndarray, projection: np.ndarray) -> float:
    return float(np.real(np.trace(projection @ rho)))


def measure_and_update(rho: np.ndarray, projection: np.ndarray) -> tuple[float, np.ndarray]:
    p = born_probability(rho, projection)
    if p <= 0.0:
        return 0.0, np.zeros_like(rho)
    rho_post = (projection @ rho @ projection) / p
    return float(p), rho_post


__all__ = [
    "ExactDensityMatrix",
    "born_probability",
    "exact_born_probability",
    "exact_measure_and_update",
    "is_exact_rational_density_matrix",
    "is_valid_density_matrix",
    "measure_and_update",
]
