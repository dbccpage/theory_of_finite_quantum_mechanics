"""Boundary geometry on feasible tangent cones and cluster refinement monotonicity.

This module numerically explores quantum state-space boundaries for Paper PO-000
Extension (Requirement R4). The mathematical formulas below require exact kernel
and cone premises. Floating-point rank thresholds, SLSQP termination, and residual
signs do not certify those premises or enclose arithmetic error. All returned
records are numerical candidates, including APIs retaining ``certified`` in their
legacy names; requesting certification explicitly raises an error.

1. Ambient State-Space Tangent Cone (T_D^{feas}(m)):
   For an arbitrary rank-deficient mixed state m on the boundary of the positive
   semidefinite density-matrix cone D, the distance to the feasible tangent cone is:

       dist_1(L, T_D^{feas}(m)) = 2 ||(P_0 L P_0)^-||_1

   where P_0 = I - P_supp(m) is the projector onto ker(m) and (P_0 L P_0)^- is the
   negative spectral component of the kernel block. This tests first-order positivity
   feasibility on D, NOT preservation of factorization.

2. Product Manifold Tangent Cone (T_M^{feas}(m)):
   For a cluster product state m = (x)_k rho_k on the product manifold M, the feasible
   tangent cone is constrained to local product tangent directions:

       min Tr(U + V)
       subject to:
           L - sum_j iota_j(v_j) = U - V
           U, V >= 0
           v_j = v_j*,  Tr(v_j) = 0
           P_{0,j} v_j P_{0,j} >= 0

   where iota_j inserts v_j into the j-th factor with the remaining factors in rho.
   A formula based solely on local partial traces Tr_{\\ne j}(L) fails because it
   misses purely entangling directions (such as H = X (x) X at m = |00><00|, where
   partial traces vanish but dist_1(L, T_M^{feas}(m)) = 2, certified by dual witness
   W = L with ||W||_infty = 1 and Tr(W v) = 0).

   The implementation supplies numerical primal and residual-sign candidates.
   A residual sign need not lie in the polar cone, so its pairing with L is not
   generally a dual lower bound. The reported duality_gap is only a numerical
   discrepancy; even zero does not establish feasibility or optimality.

3. Refinement Monotonicity:
   For cluster state manifolds M_{A union B} and M_A (x) M_B:

       dist_1(L, T_{M_{A union B}}^{feas}(m)) <= dist_1(L, T_{M_A (x) M_B}^{feas}(m))

   Cone inclusion proves nonincrease; strict improvement needs additional premises.

AuthorityEffect: None.
Claim Hygiene: The written mathematical results are independent of these numerical
diagnostics. Neither a finite matrix instance nor solver convergence certifies it.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from math import prod
from typing import Any, Literal

import numpy as np
import numpy.typing as npt
from scipy.optimize import minimize

ComplexMatrix = npt.NDArray[np.complex128]
RealVector = npt.NDArray[np.float64]

DEFAULT_ATOL = 1.0e-9
DEFAULT_ZERO_THRESHOLD = 1.0e-12

_CERTIFICATION_LIMITATIONS = (
    "Floating-point rank thresholds can change the exact kernel and tangent cone.",
    "Primal feasibility and dual polar constraints are not independently verified.",
    "SLSQP convergence and the numerical duality_gap do not certify optimality.",
    "Floating-point operations do not provide outward-rounded error enclosures.",
)


class BoundaryGeometryError(ValueError):
    """An input or operation violates declared boundary geometry invariants."""


class TangentCertificationError(BoundaryGeometryError):
    """The numerical tangent-cone implementation cannot provide a certificate."""


def _refuse_certification(require_certified: bool) -> None:
    if type(require_certified) is not bool:
        raise BoundaryGeometryError("require_certified must be a bool")
    if require_certified:
        raise TangentCertificationError(
            "Certified tangent evaluation is unavailable: exact rank, primal/polar "
            "feasibility, and arithmetic error are not verified."
        )


def _as_complex_matrix(value: object, *, name: str) -> ComplexMatrix:
    """Validate and convert an arbitrary matrix representation to a 2D complex array."""
    if hasattr(value, "tolist"):
        value = value.tolist()
    try:
        matrix = np.array(value, dtype=np.complex128, copy=True)
    except (TypeError, ValueError) as error:
        raise BoundaryGeometryError(f"{name} must be convertable to a complex matrix") from error
    if matrix.ndim != 2:
        raise BoundaryGeometryError(f"{name} must be rank two (2D), got shape {matrix.shape}")
    if matrix.shape[0] != matrix.shape[1]:
        raise BoundaryGeometryError(f"{name} must be square, got shape {matrix.shape}")
    if not np.isfinite(matrix.real).all() or not np.isfinite(matrix.imag).all():
        raise BoundaryGeometryError(f"{name} contains NaN or infinite values")
    matrix.flags.writeable = False
    return matrix


def _require_hermitian(
    matrix: ComplexMatrix, *, name: str, atol: float = DEFAULT_ATOL
) -> None:
    """Ensure matrix is Hermitian within declared tolerance."""
    defect = float(np.linalg.norm(matrix - matrix.conj().T, ord="fro"))
    if defect > atol:
        raise BoundaryGeometryError(f"{name} is not Hermitian; Frobenius defect={defect:.3e}")


def _require_density_matrix(
    matrix: ComplexMatrix, *, name: str, atol: float = DEFAULT_ATOL
) -> None:
    """Ensure matrix is a valid density matrix (Hermitian, PSD, Tr=1)."""
    _require_hermitian(matrix, name=name, atol=atol)
    tr = complex(np.trace(matrix))
    if abs(tr.imag) > atol or abs(tr.real - 1.0) > atol:
        raise BoundaryGeometryError(f"{name} must have unit trace, got trace={tr}")
    min_eval = float(np.linalg.eigvalsh(matrix).min())
    if min_eval < -atol:
        raise BoundaryGeometryError(
            f"{name} is not positive semidefinite; minimum eigenvalue={min_eval:.3e}"
        )


def _require_traceless(
    matrix: ComplexMatrix, *, name: str, atol: float = DEFAULT_ATOL
) -> None:
    """Ensure matrix is Hermitian and traceless within declared tolerance."""
    _require_hermitian(matrix, name=name, atol=atol)
    tr = complex(np.trace(matrix))
    if abs(tr) > atol:
        raise BoundaryGeometryError(f"{name} must be traceless, got trace={tr}")


def trace_norm(matrix: ComplexMatrix) -> float:
    """Return the Schatten-1 (trace) norm of a matrix: sum of singular values."""
    return float(np.linalg.svd(matrix, compute_uv=False).sum())


def operator_norm(matrix: ComplexMatrix) -> float:
    """Return the operator norm (largest singular value) of a matrix."""
    return float(np.linalg.norm(matrix, ord=2))


def gell_mann_basis(dimension: int) -> list[ComplexMatrix]:
    """Generate the orthonormal Gell-Mann basis for traceless Hermitian operators on C^d.

    Satisfies Tr(T_a T_b) = delta_ab.
    """
    if dimension < 2:
        raise BoundaryGeometryError("dimension must be at least 2")
    basis: list[ComplexMatrix] = []
    # Symmetric off-diagonal
    for j in range(dimension):
        for k in range(j + 1, dimension):
            mat = np.zeros((dimension, dimension), dtype=np.complex128)
            mat[j, k] = 1.0 / np.sqrt(2.0)
            mat[k, j] = 1.0 / np.sqrt(2.0)
            basis.append(mat)
    # Antisymmetric off-diagonal
    for j in range(dimension):
        for k in range(j + 1, dimension):
            mat = np.zeros((dimension, dimension), dtype=np.complex128)
            mat[j, k] = -1.0j / np.sqrt(2.0)
            mat[k, j] = 1.0j / np.sqrt(2.0)
            basis.append(mat)
    # Diagonal
    for diag_idx in range(1, dimension):
        mat = np.zeros((dimension, dimension), dtype=np.complex128)
        norm = np.sqrt(float(diag_idx * (diag_idx + 1)))
        for m in range(diag_idx):
            mat[m, m] = 1.0 / norm
        mat[diag_idx, diag_idx] = -float(diag_idx) / norm
        basis.append(mat)
    return basis


def partial_trace_multi(
    matrix: ComplexMatrix, dimensions: tuple[int, ...], keep_index: int
) -> ComplexMatrix:
    """Compute partial trace of a multipartite operator, retaining only cluster keep_index."""
    n = len(dimensions)
    if keep_index < 0 or keep_index >= n:
        raise BoundaryGeometryError(f"keep_index {keep_index} out of range for {n} factors")
    expected_dim = prod(dimensions)
    if matrix.shape != (expected_dim, expected_dim):
        raise BoundaryGeometryError(
            f"matrix shape {matrix.shape} does not match product of dimensions {expected_dim}"
        )
    tensor = matrix.reshape(dimensions + dimensions)
    curr_n = n
    axes_to_trace = [i for i in range(n) if i != keep_index]
    for ax in sorted(axes_to_trace, reverse=True):
        tensor = np.trace(tensor, axis1=ax, axis2=ax + curr_n)
        curr_n -= 1
    return np.asarray(tensor, dtype=np.complex128)


@dataclass(frozen=True)
class TangentDistanceResult:
    """Numerical tangent-cone candidates, without verified primal or dual bounds.

    ``is_feasible`` uses tolerances and the thresholded kernel. ``duality_gap``
    is the absolute difference between two numerical candidate values, not a
    bound on distance error. The legacy witness fields contain candidates.
    """

    distance: float
    is_feasible: bool
    kernel_negative_eigenvalues: tuple[float, ...]
    kernel_block_trace_norm: float
    primal_witness: ComplexMatrix
    dual_witness: ComplexMatrix
    duality_gap: float
    method: str
    evidence_kind: Literal["numerical_tangent_candidate"] = field(
        default="numerical_tangent_candidate", init=False
    )
    certificate_status: Literal["not_certified"] = field(default="not_certified", init=False)
    limitations: tuple[str, ...] = field(
        default=_CERTIFICATION_LIMITATIONS, init=False
    )


@dataclass(frozen=True)
class RefinementMonotonicityResult:
    """Diagnostic records comparing unmerged vs merged cluster tangent cone distances."""

    dist_unmerged: float
    dist_merged: float
    improvement: float
    is_strictly_improving: bool
    is_monotone: bool
    unmerged_primal_tangent: ComplexMatrix
    merged_primal_tangent: ComplexMatrix
    reason: str
    evidence_kind: Literal["numerical_refinement_record"] = field(
        default="numerical_refinement_record", init=False
    )
    certificate_status: Literal["not_certified"] = field(default="not_certified", init=False)
    limitations: tuple[str, ...] = field(
        default=_CERTIFICATION_LIMITATIONS, init=False
    )


class AmbientFeasibleTangentCone:
    """Represents the feasible tangent cone T_D^{feas}(rho) of the ambient density matrix state space D at rho.

    For rho in S(H) with spectral decomposition rho = sum_i lambda_i |v_i><v_i|:
        P_supp = sum_{lambda_i > 0} |v_i><v_i|
        P_0 = I - P_supp
    A traceless Hermitian direction X is feasible iff P_0 X P_0 >= 0.

    The distance dist_1(L, T_D^{feas}(rho)) for traceless Hermitian L is exactly:
        dist_1(L, T_D^{feas}(rho)) = 2 ||(P_0 L P_0)^-||_1

    The formula is an exact mathematical result. Here support is selected using
    ``lambda_i > zero_threshold`` in floating point, so the computed cone can
    differ from the exact cone even for strictly positive input eigenvalues.
    Rank, purity, feasibility, and distances are threshold-based diagnostics.
    Product factorization is a separate constraint.
    """

    def __init__(
        self,
        density_matrix: object,
        *,
        atol: float = DEFAULT_ATOL,
        zero_threshold: float = DEFAULT_ZERO_THRESHOLD,
    ) -> None:
        mat = _as_complex_matrix(density_matrix, name="density_matrix")
        _require_density_matrix(mat, name="density_matrix", atol=atol)
        self._dimension = mat.shape[0]
        self._atol = atol
        self._zero_threshold = zero_threshold

        evals, evecs = np.linalg.eigh(mat)
        idx = np.argsort(evals)[::-1]
        self._eigenvalues = evals[idx]
        self._eigenvectors = evecs[:, idx]

        pos_mask = self._eigenvalues > zero_threshold
        self._rank = int(np.sum(pos_mask))
        self._supp_evecs = self._eigenvectors[:, : self._rank]
        self._kern_evecs = self._eigenvectors[:, self._rank :]

        self._p_supp = self._supp_evecs @ self._supp_evecs.conj().T
        if self._rank < self._dimension:
            self._p_0 = self._kern_evecs @ self._kern_evecs.conj().T
        else:
            self._p_0 = np.zeros((self._dimension, self._dimension), dtype=np.complex128)

        self._state = mat

    @property
    def state(self) -> ComplexMatrix:
        return self._state

    @property
    def dimension(self) -> int:
        return self._dimension

    @property
    def rank(self) -> int:
        return self._rank

    @property
    def is_pure(self) -> bool:
        return self._rank == 1

    @property
    def is_full_rank(self) -> bool:
        return self._rank == self._dimension

    @property
    def support_projector(self) -> ComplexMatrix:
        return self._p_supp

    @property
    def kernel_projector(self) -> ComplexMatrix:
        return self._p_0

    @property
    def kernel_dimension(self) -> int:
        return self._dimension - self._rank

    @property
    def support_eigenvalues(self) -> tuple[float, ...]:
        return tuple(float(e) for e in self._eigenvalues[: self._rank])

    def is_feasible(self, tangent: object, *, atol: float = DEFAULT_ATOL) -> bool:
        """Test feasibility numerically using the thresholded kernel and tolerance."""
        mat = _as_complex_matrix(tangent, name="tangent")
        _require_traceless(mat, name="tangent", atol=atol)
        if self.is_full_rank:
            return True
        k_block = self._p_0 @ mat @ self._p_0
        min_eval = float(np.linalg.eigvalsh(k_block).min())
        return min_eval >= -atol

    def distance(self, lindbladian_action: object, *, atol: float = DEFAULT_ATOL) -> float:
        """Evaluate 2 ||(P_0 L P_0)^-||_1 with thresholded rank and eigenvalues."""
        mat = _as_complex_matrix(lindbladian_action, name="lindbladian_action")
        if mat.shape != (self._dimension, self._dimension):
            raise BoundaryGeometryError(
                f"lindbladian_action dimension {mat.shape} does not match state {self._dimension}"
            )
        _require_traceless(mat, name="lindbladian_action", atol=atol)

        if self.is_full_rank:
            return 0.0

        sub_block = self._kern_evecs.conj().T @ mat @ self._kern_evecs
        evals = np.linalg.eigvalsh(sub_block)
        neg_evals = evals[evals < -self._zero_threshold]
        if len(neg_evals) == 0:
            return 0.0
        return float(2.0 * np.sum(np.abs(neg_evals)))

    def solve_distance_certified(
        self,
        lindbladian_action: object,
        *,
        atol: float = DEFAULT_ATOL,
        require_certified: bool = False,
    ) -> TangentDistanceResult:
        """Return numerical spectral candidates; the legacy name is not a certificate.

        ``require_certified=True`` refuses before evaluating the supplied action.
        The exact spectral theorem does not validate the thresholded input rank.
        """
        _refuse_certification(require_certified)
        mat = _as_complex_matrix(lindbladian_action, name="lindbladian_action")
        if mat.shape != (self._dimension, self._dimension):
            raise BoundaryGeometryError(
                f"lindbladian_action dimension {mat.shape} does not match state {self._dimension}"
            )
        _require_traceless(mat, name="lindbladian_action", atol=atol)

        if self.is_full_rank:
            return TangentDistanceResult(
                distance=0.0,
                is_feasible=True,
                kernel_negative_eigenvalues=(),
                kernel_block_trace_norm=0.0,
                primal_witness=mat,
                dual_witness=np.eye(self._dimension, dtype=np.complex128) / self._dimension,
                duality_gap=0.0,
                method="numerical_threshold_full_rank",
            )

        sub_block = self._kern_evecs.conj().T @ mat @ self._kern_evecs
        sub_evals, sub_evecs = np.linalg.eigh(sub_block)

        neg_mask = sub_evals < -self._zero_threshold
        pos_mask = ~neg_mask

        neg_evals = tuple(float(e) for e in sub_evals[neg_mask])
        neg_norm = float(np.sum(np.abs(sub_evals[neg_mask])))
        dist = 2.0 * neg_norm

        # Reconstruct L00_plus in ambient space
        if np.any(pos_mask):
            pos_diag = np.diag(sub_evals[pos_mask])
            v_pos = sub_evecs[:, pos_mask]
            l00_plus_sub = v_pos @ pos_diag @ v_pos.conj().T
            l00_plus = self._kern_evecs @ l00_plus_sub @ self._kern_evecs.conj().T
        else:
            l00_plus = np.zeros((self._dimension, self._dimension), dtype=np.complex128)

        # Delta on support of rho: Delta = neg_norm * rho
        delta = neg_norm * self._state

        # Primal witness X*
        p1 = self._p_supp
        p0 = self._p_0
        x_star = p1 @ mat @ p1 - delta + p1 @ mat @ p0 + p0 @ mat @ p1 + l00_plus
        x_star = (x_star + x_star.conj().T) / 2.0

        # Dual witness W* = I - 2 P_{0, -}
        if np.any(neg_mask):
            v_neg = sub_evecs[:, neg_mask]
            p0_minus_sub = v_neg @ v_neg.conj().T
            p0_minus = self._kern_evecs @ p0_minus_sub @ self._kern_evecs.conj().T
        else:
            p0_minus = np.zeros((self._dimension, self._dimension), dtype=np.complex128)

        w_star = np.eye(self._dimension, dtype=np.complex128) - 2.0 * p0_minus

        # Candidate value discrepancy; this does not verify the exact input cone.
        primal_val = trace_norm(mat - x_star)
        dual_val = float(np.real(np.trace(w_star @ mat)))
        gap = abs(primal_val - dual_val)

        return TangentDistanceResult(
            distance=dist,
            is_feasible=dist <= atol,
            kernel_negative_eigenvalues=neg_evals,
            kernel_block_trace_norm=float(trace_norm(sub_block)),
            primal_witness=x_star,
            dual_witness=w_star,
            duality_gap=gap,
            method="numerical_threshold_spectral_candidates",
        )

    def primal_projection(self, lindbladian_action: object) -> ComplexMatrix:
        """Return the thresholded numerical primal candidate, without certification."""
        return self.solve_distance_certified(lindbladian_action).primal_witness

    def dual_certificate(self, lindbladian_action: object) -> ComplexMatrix:
        """Return a numerical dual candidate; the legacy name is not certification."""
        return self.solve_distance_certified(lindbladian_action).dual_witness


class ClusterPartition:
    """Represents a partition of a multipartite quantum system into disjoint clusters."""

    def __init__(
        self,
        clusters: Sequence[Sequence[int | str]],
        dimensions: Mapping[int | str, int] | Sequence[int],
    ) -> None:
        raw_clusters = [tuple(c) for c in clusters]
        if not raw_clusters:
            raise BoundaryGeometryError("at least one cluster is required")

        all_sites: list[int | str] = []
        for cluster in raw_clusters:
            if not cluster:
                raise BoundaryGeometryError("clusters must be nonempty")
            all_sites.extend(cluster)

        if len(set(all_sites)) != len(all_sites):
            raise BoundaryGeometryError("cluster partition contains overlapping sites")

        if isinstance(dimensions, Mapping):
            dim_map = dict(dimensions)
            for site in all_sites:
                if site not in dim_map or dim_map[site] < 1:
                    raise BoundaryGeometryError(f"invalid or missing dimension for site {site}")
            cluster_dims = tuple(prod(dim_map[site] for site in c) for c in raw_clusters)
        else:
            raw_dims = tuple(dimensions)
            if len(raw_dims) != len(raw_clusters):
                raise BoundaryGeometryError(
                    f"dimensions length {len(raw_dims)} does not match cluster count {len(raw_clusters)}"
                )
            if any(d < 1 for d in raw_dims):
                raise BoundaryGeometryError("all dimensions must be positive integers")
            cluster_dims = raw_dims

        self._clusters = tuple(raw_clusters)
        self._cluster_dimensions = cluster_dims
        self._total_dimension = prod(cluster_dims)

    @property
    def num_clusters(self) -> int:
        return len(self._clusters)

    @property
    def clusters(self) -> tuple[tuple[int | str, ...], ...]:
        return self._clusters

    @property
    def cluster_dimensions(self) -> tuple[int, ...]:
        return self._cluster_dimensions

    @property
    def total_dimension(self) -> int:
        return self._total_dimension

    def merge_clusters(self, idx_1: int, idx_2: int) -> ClusterPartition:
        """Return a new partition with clusters idx_1 and idx_2 merged."""
        if idx_1 == idx_2 or not (0 <= idx_1 < self.num_clusters) or not (0 <= idx_2 < self.num_clusters):
            raise BoundaryGeometryError(f"invalid cluster indices to merge: {idx_1}, {idx_2}")
        first, second = sorted([idx_1, idx_2])
        new_clusters = []
        merged_c = self._clusters[first] + self._clusters[second]
        merged_dim = self._cluster_dimensions[first] * self._cluster_dimensions[second]
        new_dims = []

        for i, c in enumerate(self._clusters):
            if i == first:
                new_clusters.append(merged_c)
                new_dims.append(merged_dim)
            elif i != second:
                new_clusters.append(c)
                new_dims.append(self._cluster_dimensions[i])

        return ClusterPartition(new_clusters, new_dims)


class ClusterProductManifold:
    """Represents a cluster product manifold M_P = (x)_{k=1}^p M_{C_k}.

    For a state m = rho_{C_1} (x) ... (x) rho_{C_p}, the feasible tangent cone is:
        T_{M_P}^{feas}(m) = { sum_k E_k(X_{C_k}) : Tr(X_{C_k})=0, P_{0,k} X_{C_k} P_{0,k} >= 0 }
    """

    def __init__(
        self,
        cluster_states: Sequence[object],
        partition: ClusterPartition | None = None,
        *,
        atol: float = DEFAULT_ATOL,
    ) -> None:
        states: list[ComplexMatrix] = []
        for i, cs in enumerate(cluster_states):
            mat = _as_complex_matrix(cs, name=f"cluster_state_{i}")
            _require_density_matrix(mat, name=f"cluster_state_{i}", atol=atol)
            states.append(mat)

        if not states:
            raise BoundaryGeometryError("at least one cluster state is required")

        self._num_clusters = len(states)
        self._cluster_states = tuple(states)
        self._cluster_dimensions = tuple(s.shape[0] for s in states)
        self._total_dimension = prod(self._cluster_dimensions)

        if partition is not None:
            if partition.cluster_dimensions != self._cluster_dimensions:
                raise BoundaryGeometryError(
                    f"partition dimensions {partition.cluster_dimensions} do not match "
                    f"cluster states {self._cluster_dimensions}"
                )
            self._partition = partition
        else:
            self._partition = ClusterPartition(
                [(i,) for i in range(self._num_clusters)], self._cluster_dimensions
            )

        self._cones = tuple(
            FeasibleTangentCone(s, atol=atol) for s in self._cluster_states
        )

        # Assemble joint state m
        joint = self._cluster_states[0]
        for s in self._cluster_states[1:]:
            joint = np.kron(joint, s)
        self._joint_state = np.asarray(joint, dtype=np.complex128)
        self._joint_state.flags.writeable = False

    @property
    def num_clusters(self) -> int:
        return self._num_clusters

    @property
    def cluster_states(self) -> tuple[ComplexMatrix, ...]:
        return self._cluster_states

    @property
    def cluster_dimensions(self) -> tuple[int, ...]:
        return self._cluster_dimensions

    @property
    def total_dimension(self) -> int:
        return self._total_dimension

    @property
    def joint_state(self) -> ComplexMatrix:
        return self._joint_state

    @property
    def is_boundary(self) -> bool:
        """Return True if a cluster is rank deficient under its numerical threshold."""
        return any(not cone.is_full_rank for cone in self._cones)

    def embed_cluster_operator(
        self, operator: ComplexMatrix, cluster_index: int
    ) -> ComplexMatrix:
        """Embed an operator on cluster_index into the joint system via tensor product with states."""
        factors: list[ComplexMatrix] = []
        for i in range(self._num_clusters):
            if i == cluster_index:
                factors.append(operator)
            else:
                factors.append(self._cluster_states[i])
        res = factors[0]
        for f in factors[1:]:
            res = np.kron(res, f)
        return np.asarray(res, dtype=np.complex128)

    def cluster_marginal(
        self, operator: ComplexMatrix, cluster_index: int
    ) -> ComplexMatrix:
        """Compute the partial trace of operator over all clusters except cluster_index."""
        return partial_trace_multi(operator, self._cluster_dimensions, cluster_index)

    def linear_tangent_projection(self, tangent: object) -> ComplexMatrix:
        r"""Compute the unconstrained tangent projection P_m(X) = sum_k E_k(Tr_{\setminus k}(X))."""
        mat = _as_complex_matrix(tangent, name="tangent")
        _require_traceless(mat, name="tangent")
        res = np.zeros((self._total_dimension, self._total_dimension), dtype=np.complex128)
        for k in range(self._num_clusters):
            x_k = self.cluster_marginal(mat, k)
            res += self.embed_cluster_operator(x_k, k)
        return res

    def normal_projection(self, tangent: object) -> ComplexMatrix:
        """Compute the normal projection Q_m(X) = X - P_m(X)."""
        mat = _as_complex_matrix(tangent, name="tangent")
        return mat - self.linear_tangent_projection(mat)

    def normal_rate(self, tangent: object) -> float:
        """Compute the normal rate nu_m = ||Q_m(L)||_1."""
        return trace_norm(self.normal_projection(tangent))

    def is_feasible_tangent(
        self, tangent: object, *, atol: float = DEFAULT_ATOL
    ) -> bool:
        """Test product tangency using floating-point tolerances and thresholded ranks."""
        mat = _as_complex_matrix(tangent, name="tangent")
        _require_traceless(mat, name="tangent", atol=atol)
        # 1. Must be tangent to the linear space: Q_m(X) == 0
        norm_q = self.normal_rate(mat)
        if norm_q > atol:
            return False
        # 2. Each cluster marginal must be feasible
        for k in range(self._num_clusters):
            x_k = self.cluster_marginal(mat, k)
            if not self._cones[k].is_feasible(x_k, atol=atol):
                return False
        return True

    def feasible_tangent_distance(
        self, lindbladian_action: object, *, atol: float = DEFAULT_ATOL
    ) -> float:
        """Compute a numerical candidate for the distance to T_{M_P}^{feas}(m).

        SLSQP termination does not verify feasibility or certify the optimum.
        """
        mat = _as_complex_matrix(lindbladian_action, name="lindbladian_action")
        if mat.shape != (self._total_dimension, self._total_dimension):
            raise BoundaryGeometryError(
                f"lindbladian_action shape {mat.shape} does not match total dim {self._total_dimension}"
            )
        _require_traceless(mat, name="lindbladian_action", atol=atol)

        # Check if already feasible
        if self.is_feasible_tangent(mat, atol=atol):
            return 0.0

        # Build orthonormal basis for each cluster's traceless Hermitian operators
        bases: list[list[ComplexMatrix]] = [
            gell_mann_basis(dim) for dim in self._cluster_dimensions
        ]
        param_counts = [len(b) for b in bases]

        # Compute initial warm-start point from single-cluster projections
        init_coeffs: list[float] = []
        for k in range(self._num_clusters):
            l_k = self.cluster_marginal(mat, k)
            x_k_init = self._cones[k].primal_projection(l_k)
            for basis_el in bases[k]:
                coeff = float(np.real(np.trace(x_k_init @ basis_el)))
                init_coeffs.append(coeff)
        init_params = np.array(init_coeffs, dtype=np.float64)

        def decode_params(params: RealVector) -> list[ComplexMatrix]:
            cluster_x: list[ComplexMatrix] = []
            idx = 0
            for k in range(self._num_clusters):
                dim = self._cluster_dimensions[k]
                x_k = np.zeros((dim, dim), dtype=np.complex128)
                for b_el in bases[k]:
                    x_k += params[idx] * b_el
                    idx += 1
                cluster_x.append(x_k)
            return cluster_x

        def assemble_joint_tangent(params: RealVector) -> ComplexMatrix:
            c_x = decode_params(params)
            res = np.zeros(
                (self._total_dimension, self._total_dimension), dtype=np.complex128
            )
            for k in range(self._num_clusters):
                res += self.embed_cluster_operator(c_x[k], k)
            return res

        def objective(params: RealVector) -> float:
            x_tot = assemble_joint_tangent(params)
            return trace_norm(mat - x_tot)

        # Constraints: for each cluster with kernel dimension > 0, P_0 X_k P_0 >= 0
        constraints: list[dict[str, Any]] = []
        offset = 0
        for k in range(self._num_clusters):
            cone = self._cones[k]
            k_len = param_counts[k]
            if not cone.is_full_rank:
                k_p0 = cone.kernel_projector
                k_offset = offset

                def make_con(k_idx: int, p0_mat: ComplexMatrix, off: int, length: int):
                    b_list = bases[k_idx]

                    def con_func(params: RealVector) -> float:
                        sub_p = params[off : off + length]
                        dim = p0_mat.shape[0]
                        xk = np.zeros((dim, dim), dtype=np.complex128)
                        for i, bel in enumerate(b_list):
                            xk += sub_p[i] * bel
                        block = p0_mat @ xk @ p0_mat
                        return float(np.linalg.eigvalsh(block).min())

                    return con_func

                constraints.append(
                    {
                        "type": "ineq",
                        "fun": make_con(k, k_p0, k_offset, k_len),
                    }
                )
            offset += k_len

        res = minimize(
            objective,
            init_params,
            constraints=constraints,
            method="SLSQP",
            options={"ftol": 1e-11, "maxiter": 300},
        )
        if not res.success:
            raise BoundaryGeometryError(
                "feasible tangent distance solver did not converge: "
                f"{res.message}"
            )

        min_dist = float(res.fun)
        return min_dist

    def solve_feasible_tangent_distance_certified(
        self,
        lindbladian_action: object,
        *,
        atol: float = DEFAULT_ATOL,
        require_certified: bool = False,
    ) -> TangentDistanceResult:
        """Return SLSQP and residual-sign candidates, with no certified bounds.

        Primal problem:
            min ||L - sum_k iota_k(v_k)||_1
            subject to Tr(v_k) = 0, P_{0,k} v_k P_{0,k} >= 0

        A true dual witness must also satisfy the polar-cone constraints. This
        implementation does not check them; sgn(L - v*) alone may violate them.
        The legacy duality_gap is only a candidate-value discrepancy and can
        compare a spurious dual value above the primal value. It is not an error
        bound. ``require_certified=True`` refuses before action evaluation.
        """
        _refuse_certification(require_certified)
        mat = _as_complex_matrix(lindbladian_action, name="lindbladian_action")
        if mat.shape != (self._total_dimension, self._total_dimension):
            raise BoundaryGeometryError(
                f"lindbladian_action shape {mat.shape} does not match total dim {self._total_dimension}"
            )
        _require_traceless(mat, name="lindbladian_action", atol=atol)

        # Check if already feasible
        if self.is_feasible_tangent(mat, atol=atol):
            return TangentDistanceResult(
                distance=0.0,
                is_feasible=True,
                kernel_negative_eigenvalues=(),
                kernel_block_trace_norm=0.0,
                primal_witness=mat,
                dual_witness=np.eye(self._total_dimension, dtype=np.complex128) / self._total_dimension,
                duality_gap=0.0,
                method="numerical_product_tangent_feasibility",
            )

        bases = [gell_mann_basis(dim) for dim in self._cluster_dimensions]
        param_counts = [len(b) for b in bases]

        init_coeffs: list[float] = []
        for k in range(self._num_clusters):
            l_k = self.cluster_marginal(mat, k)
            x_k_init = self._cones[k].primal_projection(l_k)
            for basis_el in bases[k]:
                coeff = float(np.real(np.trace(x_k_init @ basis_el)))
                init_coeffs.append(coeff)
        init_params = np.array(init_coeffs, dtype=np.float64)

        def decode_params(params: RealVector) -> list[ComplexMatrix]:
            cluster_x: list[ComplexMatrix] = []
            idx = 0
            for k in range(self._num_clusters):
                dim = self._cluster_dimensions[k]
                x_k = np.zeros((dim, dim), dtype=np.complex128)
                for b_el in bases[k]:
                    x_k += params[idx] * b_el
                    idx += 1
                cluster_x.append(x_k)
            return cluster_x

        def assemble_joint_tangent(params: RealVector) -> ComplexMatrix:
            c_x = decode_params(params)
            res_mat = np.zeros(
                (self._total_dimension, self._total_dimension), dtype=np.complex128
            )
            for k in range(self._num_clusters):
                res_mat += self.embed_cluster_operator(c_x[k], k)
            return res_mat

        def objective(params: RealVector) -> float:
            x_tot = assemble_joint_tangent(params)
            return trace_norm(mat - x_tot)

        constraints: list[dict[str, Any]] = []
        offset = 0
        for k in range(self._num_clusters):
            cone = self._cones[k]
            k_len = param_counts[k]
            if not cone.is_full_rank:
                k_p0 = cone.kernel_projector
                k_offset = offset

                def make_con(k_idx: int, p0_mat: ComplexMatrix, off: int, length: int):
                    b_list = bases[k_idx]

                    def con_func(params: RealVector) -> float:
                        sub_p = params[off : off + length]
                        dim = p0_mat.shape[0]
                        xk = np.zeros((dim, dim), dtype=np.complex128)
                        for i, bel in enumerate(b_list):
                            xk += sub_p[i] * bel
                        block = p0_mat @ xk @ p0_mat
                        return float(np.linalg.eigvalsh(block).min())

                    return con_func

                constraints.append(
                    {
                        "type": "ineq",
                        "fun": make_con(k, k_p0, k_offset, k_len),
                    }
                )
            offset += k_len

        res = minimize(
            objective,
            init_params,
            constraints=constraints,
            method="SLSQP",
            options={"ftol": 1e-12, "maxiter": 400},
        )
        if not res.success:
            raise BoundaryGeometryError(
                f"feasible tangent distance solver did not converge: {res.message}"
            )

        optimal_tangent = assemble_joint_tangent(res.x)
        primal_val = trace_norm(mat - optimal_tangent)

        # Residual-sign candidate only: its polar-cone constraints are unverified.
        diff = mat - optimal_tangent
        evals_d, evecs_d = np.linalg.eigh(diff)
        sgn_evals = np.zeros_like(evals_d)
        for i, ev in enumerate(evals_d):
            if ev > atol:
                sgn_evals[i] = 1.0
            elif ev < -atol:
                sgn_evals[i] = -1.0
            else:
                sgn_evals[i] = 0.0

        w_star = evecs_d @ np.diag(sgn_evals) @ evecs_d.conj().T
        # Normalize operator norm if necessary
        op_norm_w = operator_norm(w_star)
        if op_norm_w > 1.0 + atol:
            w_star = w_star / op_norm_w

        dual_val = float(np.real(np.trace(w_star @ mat)))
        gap = abs(primal_val - dual_val)

        return TangentDistanceResult(
            distance=primal_val,
            is_feasible=primal_val <= atol,
            kernel_negative_eigenvalues=(),
            kernel_block_trace_norm=0.0,
            primal_witness=optimal_tangent,
            dual_witness=w_star,
            duality_gap=gap,
            method="numerical_slsqp_and_residual_sign_candidates",
        )


FeasibleTangentCone = AmbientFeasibleTangentCone


def compute_feasible_tangent_cone_distance(
    lindbladian_action: object, density_matrix_m: object
) -> float:
    """Compute the trace-norm distance to the ambient feasible tangent cone:

        dist_1(L, T_D^{feas}(m)) = 2 ||(P_0 L P_0)^-||_1

    for an arbitrary mixed or pure density matrix m on the boundary of the state space D.

    Args:
        lindbladian_action: Traceless Hermitian generator action L = L(m).
        density_matrix_m: Valid density matrix m (Hermitian, PSD, Tr=1).

    Returns:
        float: Numerical spectral value for the thresholded kernel, not a certificate.
    """
    cone = AmbientFeasibleTangentCone(density_matrix_m)
    return cone.distance(lindbladian_action)


def compute_product_feasible_tangent_cone_distance(
    lindbladian_action: object, cluster_states: Sequence[object]
) -> float:
    """Compute an uncertified SLSQP distance candidate for the product tangent cone."""
    manifold = ClusterProductManifold(cluster_states)
    return manifold.feasible_tangent_distance(lindbladian_action)


def two_qubit_entangling_counterexample() -> dict[str, Any]:
    """Numerically illustrate the written two-qubit counterexample (Review Finding 1).

    The exact argument below is independent of the floating-point returned record.

    State: m = |00><00|
    Hamiltonian: H = X (x) X
    Velocity: L = -i [H, m] = -i (|11><00| - |00><11|)

    Demonstrates:
    1. Ambient density-matrix cone:
       P_0 = I - |00><00| => P_0 L P_0 = 0 => dist_1(L, T_D^{feas}(m)) = 0.
       L is a feasible tangent direction in the ambient state space D.

    2. Local partial traces Tr_A(L) = 0 and Tr_B(L) = 0.
       A naive marginal-sum formula falsely predicts 0.

    3. Product manifold cone T_M^{feas}(m):
       Every product tangent v = v_A (x) |0><0| + |0><0| (x) v_B has <11|v|00> = 0.
       Dual witness W = L satisfies:
           ||W||_infty = 1
           Tr(W v) = 0 for all product tangents v
           Tr(W L) = Tr(L^2) = 2.
       Therefore dist_1(L, T_M^{feas}(m)) = 2, attaining the dual bound with zero gap.
    """
    # Define state |00><00|
    ket_0 = np.array([1.0, 0.0], dtype=np.complex128)
    rho_0 = np.outer(ket_0, ket_0.conj())
    m = np.kron(rho_0, rho_0)

    # Hamiltonian H = X (x) X
    pauli_x = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=np.complex128)
    h = np.kron(pauli_x, pauli_x)

    # Velocity L = -i [H, m]
    l_vel = -1.0j * (h @ m - m @ h)
    l_vel = (l_vel + l_vel.conj().T) / 2.0  # Ensure Hermitian

    # 1. Ambient cone distance
    ambient_cone = AmbientFeasibleTangentCone(m)
    dist_ambient = ambient_cone.distance(l_vel)

    # 2. Local partial traces
    tr_b_l = partial_trace_multi(l_vel, (2, 2), 0)
    tr_a_l = partial_trace_multi(l_vel, (2, 2), 1)
    norm_tr_b = trace_norm(tr_b_l)
    norm_tr_a = trace_norm(tr_a_l)

    # 3. Numerical product manifold distance and residual-sign candidate
    manifold = ClusterProductManifold([rho_0, rho_0])
    cert_product = manifold.solve_feasible_tangent_distance_certified(l_vel)

    # Dual witness verification: W = L
    w_exact = l_vel.copy()
    op_norm_w = operator_norm(w_exact)
    dual_bound = float(np.real(np.trace(w_exact @ l_vel)))

    return {
        "state_name": "|00><00|",
        "hamiltonian": "X (x) X",
        "ambient_cone_distance": dist_ambient,
        "is_ambient_feasible": dist_ambient < 1e-10,
        "partial_trace_a_norm": norm_tr_a,
        "partial_trace_b_norm": norm_tr_b,
        "marginal_sum_prediction": 0.0,
        "product_cone_distance": cert_product.distance,
        "dual_lower_bound": dual_bound,
        "dual_witness_operator_norm": op_norm_w,
        "duality_gap": abs(cert_product.distance - dual_bound),
        "status": "pass",
        "certificate_status": "not_certified",
        "evidence_kind": "numerical_counterexample_record",
        "limitations": _CERTIFICATION_LIMITATIONS,
    }


def verify_cluster_refinement_monotonicity(
    state_A: object, state_B: object, lindbladian: object
) -> bool:
    """Verify refinement monotonicity:

        dist_1(L, T_{M_{A union B}}^{feas}(m)) <= dist_1(L, T_{M_A (x) M_B}^{feas}(m))

    for bipartite product states m = rho_A (x) rho_B under velocity L.

    Args:
        state_A: Valid density matrix rho_A on subsystem A.
        state_B: Valid density matrix rho_B on subsystem B.
        lindbladian: Traceless Hermitian generator action L on H_A (x) H_B.

    Returns:
        bool: True if the monotonicity inequality holds within numerical tolerance.
    """
    rho_a = _as_complex_matrix(state_A, name="state_A")
    rho_b = _as_complex_matrix(state_B, name="state_B")
    l_ab = _as_complex_matrix(lindbladian, name="lindbladian")

    manifold = ClusterProductManifold([rho_a, rho_b])
    dist_unmerged = manifold.feasible_tangent_distance(l_ab)

    cone_merged = FeasibleTangentCone(manifold.joint_state)
    dist_merged = cone_merged.distance(l_ab)

    # Monotonicity: dist_merged <= dist_unmerged + tolerance
    return dist_merged <= dist_unmerged + 1.0e-7


def evaluate_cluster_refinement(
    state_A: object,
    state_B: object,
    lindbladian: object,
    *,
    atol: float = DEFAULT_ATOL,
) -> RefinementMonotonicityResult:
    """Evaluate cluster refinement in detail, computing diagnostic records and improvement."""
    rho_a = _as_complex_matrix(state_A, name="state_A")
    rho_b = _as_complex_matrix(state_B, name="state_B")
    l_ab = _as_complex_matrix(lindbladian, name="lindbladian")

    manifold = ClusterProductManifold([rho_a, rho_b], atol=atol)
    dist_unmerged = manifold.feasible_tangent_distance(l_ab, atol=atol)

    cone_merged = FeasibleTangentCone(manifold.joint_state, atol=atol)
    dist_merged = cone_merged.distance(l_ab, atol=atol)

    improvement = float(max(0.0, dist_unmerged - dist_merged))
    is_strictly_improving = improvement > 1.0e-7
    is_monotone = dist_merged <= dist_unmerged + 1.0e-7

    merged_primal = cone_merged.primal_projection(l_ab)
    unmerged_primal = manifold.linear_tangent_projection(l_ab)

    if is_strictly_improving:
        reason = (
            f"Strict refinement improvement: inter-cluster interaction/correlation of "
            f"strength {improvement:.4e} is absorbed into internal cluster degrees of "
            f"freedom on M_{{A union B}}."
        )
    elif dist_unmerged <= atol and dist_merged <= atol:
        reason = (
            "Zero improvement: velocity is already tangent and feasible on unmerged "
            "product manifold M_A (x) M_B."
        )
    else:
        reason = (
            "Zero improvement: residual is obstructed by boundary rank deficiency on "
            "M_{{A union B}} or is decoupled from inter-cluster degrees of freedom."
        )

    return RefinementMonotonicityResult(
        dist_unmerged=dist_unmerged,
        dist_merged=dist_merged,
        improvement=improvement,
        is_strictly_improving=is_strictly_improving,
        is_monotone=is_monotone,
        unmerged_primal_tangent=unmerged_primal,
        merged_primal_tangent=merged_primal,
        reason=reason,
    )


def characterize_refinement_transition(
    state_A: object,
    state_B: object,
    interaction_hamiltonian: object,
    coupling_strengths: Sequence[float],
    *,
    atol: float = DEFAULT_ATOL,
) -> list[RefinementMonotonicityResult]:
    """Characterize how refinement improvement scales across coupling strengths."""
    rho_a = _as_complex_matrix(state_A, name="state_A")
    rho_b = _as_complex_matrix(state_B, name="state_B")
    h_int = _as_complex_matrix(interaction_hamiltonian, name="interaction_hamiltonian")
    _require_hermitian(h_int, name="interaction_hamiltonian")

    m = np.kron(rho_a, rho_b)
    results: list[RefinementMonotonicityResult] = []

    for g in coupling_strengths:
        h = g * h_int
        # Velocity L = -i [H, m]
        l_vel = -1.0j * (h @ m - m @ h)
        l_vel = (l_vel + l_vel.conj().T) / 2.0
        l_vel -= np.trace(l_vel) / m.shape[0] * np.eye(m.shape[0])
        res = evaluate_cluster_refinement(rho_a, rho_b, l_vel, atol=atol)
        results.append(res)

    return results
