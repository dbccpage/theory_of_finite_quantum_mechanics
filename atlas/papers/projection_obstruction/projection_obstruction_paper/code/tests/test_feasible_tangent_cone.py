"""Unit, property, and regression test suite for feasible tangent cone boundary geometry.

Tests Requirement R4 for Paper PO-000 Extension:
- Exact distance to feasible tangent cone dist_1(L, T_M^{feas}(m)) = 2 ||(P_0 L P_0)^-||_1
- Conical Hahn-Banach duality and zero duality gap certification
- Cluster product state manifolds and tangent cone projections
- Refinement Monotonicity Theorem: dist_1(L, T_{AB}^{feas}) <= dist_1(L, T_{A (x) B}^{feas})
- Strict improvement vs failure to improve characterizations
- Fail-closed input validation and edge cases
"""

from __future__ import annotations

import numpy as np
import pytest
from feasible_tangent_cone import (
    BoundaryGeometryError,
    ClusterPartition,
    ClusterProductManifold,
    FeasibleTangentCone,
    RefinementMonotonicityResult,
    TangentDistanceResult,
    characterize_refinement_transition,
    compute_feasible_tangent_cone_distance,
    evaluate_cluster_refinement,
    gell_mann_basis,
    operator_norm,
    trace_norm,
    verify_cluster_refinement_monotonicity,
    two_qubit_entangling_counterexample,
)

# ==============================================================================
# 1. State Space & Feasible Tangent Cone Tests (Single Factor)
# ==============================================================================


def test_full_rank_interior_state_has_zero_cone_distance():
    """Interior (full-rank) mixed states have empty kernel, so distance is always zero."""
    d = 3
    # Thermal-like full rank state
    evals = np.array([0.5, 0.3, 0.2])
    rho = np.diag(evals).astype(complex)
    cone = FeasibleTangentCone(rho)

    assert cone.is_full_rank
    assert not cone.is_pure
    assert cone.kernel_dimension == 0
    assert cone.rank == 3

    # Random traceless Hermitian direction
    np.random.seed(42)
    mat = np.random.randn(d, d) + 1j * np.random.randn(d, d)
    l_dir = (mat + mat.conj().T) / 2.0
    l_dir -= np.trace(l_dir) / d * np.eye(d)

    dist = cone.distance(l_dir)
    assert dist == 0.0
    assert cone.is_feasible(l_dir)

    cert = cone.solve_distance_certified(l_dir)
    assert cert.distance == 0.0
    assert cert.is_feasible
    assert cert.duality_gap == 0.0


def test_pure_boundary_state_feasible_direction():
    """Directions with P_0 L P_0 >= 0 are feasible and have zero distance."""
    # Pure qubit state |0><0|
    rho = np.array([[1.0, 0.0], [0.0, 0.0]], dtype=complex)
    cone = FeasibleTangentCone(rho)

    assert cone.is_pure
    assert not cone.is_full_rank
    assert cone.kernel_dimension == 1

    # Direction with positive kernel entry: L = -|0><0| + |1><1|
    # P_0 = |1><1|, so P_0 L P_0 = +1 >= 0
    l_inward = np.array([[-1.0, 0.0], [0.0, 1.0]], dtype=complex)
    assert cone.is_feasible(l_inward)
    assert cone.distance(l_inward) == 0.0

    # Off-diagonal coherent direction X: L = [[0, 1], [1, 0]]
    # P_0 L P_0 = 0 >= 0
    l_coherence = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
    assert cone.is_feasible(l_coherence)
    assert cone.distance(l_coherence) == 0.0


def test_pure_boundary_state_infeasible_direction_exact_hahn_banach():
    """Directions with negative kernel block exit the positive cone at first order.

    Distance is exactly 2 ||(P_0 L P_0)^-||_1 via Hahn-Banach duality.
    """
    # Pure qubit state |0><0|
    rho = np.array([[1.0, 0.0], [0.0, 0.0]], dtype=complex)
    cone = FeasibleTangentCone(rho)

    # Direction pointing out: L = |0><0| - |1><1|
    # Kernel block P_0 L P_0 = -1 < 0
    l_outward = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)

    assert not cone.is_feasible(l_outward)
    dist = cone.distance(l_outward)
    # Expected: 2 * |-1| = 2.0
    assert np.isclose(dist, 2.0, atol=1e-12)

    cert = cone.solve_distance_certified(l_outward)
    assert np.isclose(cert.distance, 2.0, atol=1e-12)
    assert not cert.is_feasible
    assert cert.duality_gap < 1e-14
    assert np.isclose(cert.kernel_block_trace_norm, 1.0, atol=1e-12)

    # Verify primal witness achieves dist
    x_star = cert.primal_witness
    assert cone.is_feasible(x_star)
    assert np.isclose(trace_norm(l_outward - x_star), 2.0, atol=1e-12)

    # Verify dual witness satisfies norm <= 1 and achieves dist
    w_star = cert.dual_witness
    assert operator_norm(w_star) <= 1.0 + 1e-12
    dual_val = float(np.real(np.trace(w_star @ l_outward)))
    assert np.isclose(dual_val, 2.0, atol=1e-12)


@pytest.mark.parametrize("dim, rank", [(3, 1), (3, 2), (4, 1), (4, 2), (4, 3), (5, 2)])
def test_arbitrary_mixed_rank_deficient_states_duality(dim: int, rank: int):
    """Verify conical Hahn-Banach duality and zero duality gap for various dims and ranks."""
    np.random.seed(dim * 10 + rank)

    # Random mixed state of specified rank
    pos_evals = np.random.uniform(0.1, 1.0, size=rank)
    pos_evals /= pos_evals.sum()
    all_evals = np.zeros(dim)
    all_evals[:rank] = pos_evals

    # Random unitary rotation
    u_mat = np.random.randn(dim, dim) + 1j * np.random.randn(dim, dim)
    q_mat, _ = np.linalg.qr(u_mat)
    rho = q_mat @ np.diag(all_evals) @ q_mat.conj().T
    rho = (rho + rho.conj().T) / 2.0
    rho /= np.trace(rho).real

    cone = FeasibleTangentCone(rho)
    assert cone.rank == rank
    assert cone.dimension == dim
    assert cone.kernel_dimension == dim - rank

    # Random traceless generator
    g_mat = np.random.randn(dim, dim) + 1j * np.random.randn(dim, dim)
    l_gen = (g_mat + g_mat.conj().T) / 2.0
    l_gen -= np.trace(l_gen) / dim * np.eye(dim)

    cert = cone.solve_distance_certified(l_gen)
    assert isinstance(cert, TangentDistanceResult)
    assert cert.duality_gap < 1e-12
    assert cert.distance >= 0.0

    # Check primal witness properties
    x_star = cert.primal_witness
    assert cone.is_feasible(x_star, atol=1e-9)
    assert np.isclose(trace_norm(l_gen - x_star), cert.distance, atol=1e-9)

    # Check dual witness properties
    w_star = cert.dual_witness
    assert operator_norm(w_star) <= 1.0 + 1e-9
    dual_val = float(np.real(np.trace(w_star @ l_gen)))
    assert np.isclose(dual_val, cert.distance, atol=1e-9)


def test_zero_velocity_is_zero_distance():
    """A zero velocity direction L=0 is trivially in the cone with distance 0."""
    rho = np.array([[1.0, 0.0], [0.0, 0.0]], dtype=complex)
    l_zero = np.zeros((2, 2), dtype=complex)
    assert compute_feasible_tangent_cone_distance(l_zero, rho) == 0.0


# ==============================================================================
# 2. Cluster Product Manifold & Projection Tests
# ==============================================================================


def test_gell_mann_basis_orthonormality():
    """Verify Gell-Mann basis is orthonormal and traceless for d=2, 3, 4."""
    for d in (2, 3, 4):
        basis = gell_mann_basis(d)
        assert len(basis) == d * d - 1
        for i, b1 in enumerate(basis):
            assert np.isclose(np.trace(b1), 0.0, atol=1e-12)
            assert np.allclose(b1, b1.conj().T, atol=1e-12)
            for j, b2 in enumerate(basis):
                inner = np.trace(b1 @ b2).real
                expected = 1.0 if i == j else 0.0
                assert np.isclose(inner, expected, atol=1e-12)


def test_cluster_projections_idempotent_and_orthogonal():
    """P_m and Q_m are idempotent and project onto orthogonal subspaces."""
    rho_a = np.array([[0.8, 0.0], [0.0, 0.2]], dtype=complex)
    rho_b = np.array([[0.5, 0.0], [0.0, 0.5]], dtype=complex)
    manifold = ClusterProductManifold([rho_a, rho_b])

    assert manifold.num_clusters == 2
    assert manifold.cluster_dimensions == (2, 2)
    assert manifold.total_dimension == 4

    np.random.seed(101)
    mat = np.random.randn(4, 4) + 1j * np.random.randn(4, 4)
    l_dir = (mat + mat.conj().T) / 2.0
    l_dir -= np.trace(l_dir) / 4.0 * np.eye(4)

    p_l = manifold.linear_tangent_projection(l_dir)
    q_l = manifold.normal_projection(l_dir)

    # Idempotence: P(P(L)) = P(L), Q(Q(L)) = Q(L)
    assert np.allclose(manifold.linear_tangent_projection(p_l), p_l, atol=1e-12)
    assert np.allclose(manifold.normal_projection(q_l), q_l, atol=1e-12)

    # Orthogonal split: P(L) + Q(L) = L
    assert np.allclose(p_l + q_l, l_dir, atol=1e-12)

    # Q(L) has zero marginals on all clusters
    assert np.allclose(manifold.cluster_marginal(q_l, 0), np.zeros((2, 2)), atol=1e-12)
    assert np.allclose(manifold.cluster_marginal(q_l, 1), np.zeros((2, 2)), atol=1e-12)


def test_cluster_tangent_feasibility_check():
    """Verify is_feasible_tangent rejects normal components and infeasible marginals."""
    # Pure state on A (|0><0|), mixed on B
    rho_a = np.array([[1.0, 0.0], [0.0, 0.0]], dtype=complex)
    rho_b = np.array([[0.5, 0.0], [0.0, 0.5]], dtype=complex)
    manifold = ClusterProductManifold([rho_a, rho_b])

    # Case 1: Purely tangent and inward on A: X_A = -|0><0| + |1><1|, X_B = 0
    xa_inward = np.array([[-1.0, 0.0], [0.0, 1.0]], dtype=complex)
    x_tangent_feasible = manifold.embed_cluster_operator(xa_inward, 0)
    assert manifold.is_feasible_tangent(x_tangent_feasible)

    # Case 2: Tangent but outward on A: X_A = |0><0| - |1><1|, X_B = 0
    xa_outward = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)
    x_tangent_infeasible = manifold.embed_cluster_operator(xa_outward, 0)
    assert not manifold.is_feasible_tangent(x_tangent_infeasible)

    # Case 3: Entangling normal component (e.g. Z_A (x) Z_B)
    z_mat = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)
    x_entangling = np.kron(z_mat, z_mat) - np.kron(rho_a, z_mat) - np.kron(z_mat, rho_b)
    x_entangling -= np.trace(x_entangling) / 4.0 * np.eye(4)
    assert not manifold.is_feasible_tangent(x_entangling)


# ==============================================================================
# 3. Refinement Monotonicity Tests
# ==============================================================================


def test_refinement_monotonicity_strict_improvement():
    """Inter-cluster entangling interaction yields strict improvement upon merging."""
    # Two pure qubits: |00><00|
    rho_a = np.array([[1.0, 0.0], [0.0, 0.0]], dtype=complex)
    rho_b = np.array([[1.0, 0.0], [0.0, 0.0]], dtype=complex)
    m = np.kron(rho_a, rho_b)

    # Interaction: H_int = X_A (x) X_B (genuinely entangling at |00>)
    x = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
    h_int = np.kron(x, x)

    # Generator L = -i [H_int, m]
    l_gen = -1.0j * (h_int @ m - m @ h_int)
    l_gen = (l_gen + l_gen.conj().T) / 2.0
    l_gen -= np.trace(l_gen) / 4.0 * np.eye(4)

    # Verify monotonicity
    is_monotone = verify_cluster_refinement_monotonicity(rho_a, rho_b, l_gen)
    assert is_monotone

    # Evaluate details
    res = evaluate_cluster_refinement(rho_a, rho_b, l_gen)
    assert isinstance(res, RefinementMonotonicityResult)
    assert res.is_monotone
    assert res.is_strictly_improving
    assert res.dist_merged < res.dist_unmerged
    # Because L is a unitary commutator, on the merged space M_{AB}, L has P_0 L P_0 = 0
    assert np.isclose(res.dist_merged, 0.0, atol=1e-7)
    assert res.dist_unmerged > 0.5
    assert "Strict refinement improvement" in res.reason


def test_refinement_monotonicity_zero_improvement_local_generator():
    """If generator is already purely local, cluster merging gives zero improvement."""
    rho_a = np.array([[0.7, 0.0], [0.0, 0.3]], dtype=complex)
    rho_b = np.array([[0.6, 0.0], [0.0, 0.4]], dtype=complex)
    m = np.kron(rho_a, rho_b)

    # Local Hamiltonians only: H = X_A (x) I + I (x) Y_B
    x = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
    y = np.array([[0.0, -1j], [1j, 0.0]], dtype=complex)
    h_local = np.kron(x, np.eye(2)) + np.kron(np.eye(2), y)

    l_gen = -1.0j * (h_local @ m - m @ h_local)
    l_gen = (l_gen + l_gen.conj().T) / 2.0
    l_gen -= np.trace(l_gen) / 4.0 * np.eye(4)

    res = evaluate_cluster_refinement(rho_a, rho_b, l_gen)
    assert res.is_monotone
    assert not res.is_strictly_improving
    assert np.isclose(res.dist_unmerged, 0.0, atol=1e-7)
    assert np.isclose(res.dist_merged, 0.0, atol=1e-7)
    assert np.isclose(res.improvement, 0.0, atol=1e-7)


def test_refinement_monotonicity_boundary_dissipation():
    """Open-system dissipation that pushes out of boundary retains boundary obstruction."""
    # Pure state on A, full rank on B
    rho_a = np.array([[1.0, 0.0], [0.0, 0.0]], dtype=complex)
    rho_b = np.array([[0.5, 0.0], [0.0, 0.5]], dtype=complex)

    # Interaction + Dissipator pushing population out of support on A
    p0_a = np.array([[0.0, 0.0], [0.0, 1.0]], dtype=complex)
    p1_a = np.array([[1.0, 0.0], [0.0, 0.0]], dtype=complex)

    # Dissipation rate gamma = 1.0
    l_diss = 0.5 * (np.kron(p1_a, rho_b) - np.kron(p0_a, rho_b))
    l_diss_dir = (l_diss + l_diss.conj().T) / 2.0
    l_diss_dir -= np.trace(l_diss_dir) / 4.0 * np.eye(4)

    is_monotone = verify_cluster_refinement_monotonicity(rho_a, rho_b, l_diss_dir)
    assert is_monotone

    res = evaluate_cluster_refinement(rho_a, rho_b, l_diss_dir)
    assert res.is_monotone
    # Monotonicity inequality: dist_merged <= dist_unmerged
    assert res.dist_merged <= res.dist_unmerged + 1e-7


def test_characterize_refinement_transition_scaling():
    """Verify refinement improvement scales smoothly with inter-cluster coupling."""
    rho_a = np.array([[1.0, 0.0], [0.0, 0.0]], dtype=complex)
    rho_b = np.array([[1.0, 0.0], [0.0, 0.0]], dtype=complex)

    x = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
    h_int = np.kron(x, x)

    couplings = [0.0, 0.2, 0.5, 1.0]
    records = characterize_refinement_transition(rho_a, rho_b, h_int, couplings)

    assert len(records) == 4
    improvements = [r.improvement for r in records]

    # At g=0, improvement is 0
    assert np.isclose(improvements[0], 0.0, atol=1e-7)

    # Improvement increases monotonically with coupling
    for i in range(len(improvements) - 1):
        assert improvements[i] <= improvements[i + 1] + 1e-7


def test_multipartite_cluster_merging():
    """Verify cluster partition merging on a 3-cluster system."""
    partition = ClusterPartition([[0], [1], [2]], [2, 2, 2])
    assert partition.num_clusters == 3
    assert partition.cluster_dimensions == (2, 2, 2)
    assert partition.total_dimension == 8

    # Merge clusters 0 and 1
    merged = partition.merge_clusters(0, 1)
    assert merged.num_clusters == 2
    assert merged.cluster_dimensions == (4, 2)
    assert merged.total_dimension == 8
    assert merged.clusters == ((0, 1), (2,))


# ==============================================================================
# 4. Fail-Closed Input Validation & Edge Case Tests
# ==============================================================================


def test_rejects_non_hermitian_state():
    non_herm = np.array([[1.0, 1.0], [0.0, 1.0]], dtype=complex)
    with pytest.raises(BoundaryGeometryError, match="not Hermitian"):
        FeasibleTangentCone(non_herm)


def test_rejects_non_unit_trace_state():
    bad_tr = np.array([[0.5, 0.0], [0.0, 0.2]], dtype=complex)
    with pytest.raises(BoundaryGeometryError, match="unit trace"):
        FeasibleTangentCone(bad_tr)


def test_rejects_non_psd_state():
    neg_eval = np.array([[1.2, 0.0], [0.0, -0.2]], dtype=complex)
    with pytest.raises(BoundaryGeometryError, match="positive semidefinite"):
        FeasibleTangentCone(neg_eval)


def test_rejects_non_hermitian_generator():
    rho = np.array([[1.0, 0.0], [0.0, 0.0]], dtype=complex)
    cone = FeasibleTangentCone(rho)
    non_herm_l = np.array([[0.0, 1.0], [0.0, 0.0]], dtype=complex)
    with pytest.raises(BoundaryGeometryError, match="not Hermitian"):
        cone.distance(non_herm_l)


def test_rejects_non_traceless_generator():
    rho = np.array([[1.0, 0.0], [0.0, 0.0]], dtype=complex)
    cone = FeasibleTangentCone(rho)
    bad_tr_l = np.array([[1.0, 0.0], [0.0, 1.0]], dtype=complex)
    with pytest.raises(BoundaryGeometryError, match="traceless"):
        cone.distance(bad_tr_l)


def test_rejects_mismatched_dimensions():
    rho_2 = np.array([[1.0, 0.0], [0.0, 0.0]], dtype=complex)
    cone = FeasibleTangentCone(rho_2)
    l_3 = np.zeros((3, 3), dtype=complex)
    with pytest.raises(BoundaryGeometryError, match="dimension"):
        cone.distance(l_3)


def test_rejects_nan_and_inf():
    nan_mat = np.array([[np.nan, 0.0], [0.0, 1.0]], dtype=complex)
    with pytest.raises(BoundaryGeometryError, match="NaN or infinite"):
        FeasibleTangentCone(nan_mat)


def test_cluster_partition_overlapping_sites_rejected():
    with pytest.raises(BoundaryGeometryError, match="overlapping sites"):
        ClusterPartition([[0, 1], [1, 2]], [2, 2, 2])


# ==============================================================================
# 5. Interface Contract Compliance Tests
# ==============================================================================


def test_project_interface_contracts():
    """Verify exact function signatures and return types match PROJECT.md § Interface Contracts."""
    rho_a = np.array([[1.0, 0.0], [0.0, 0.0]], dtype=complex)
    rho_b = np.array([[0.5, 0.0], [0.0, 0.5]], dtype=complex)
    m = np.kron(rho_a, rho_b)

    l_zero = np.zeros((4, 4), dtype=complex)

    # 1. compute_feasible_tangent_cone_distance(lindbladian_action, density_matrix_m) -> float
    val = compute_feasible_tangent_cone_distance(l_zero, m)
    assert isinstance(val, float)
    assert val == 0.0

    # 2. verify_cluster_refinement_monotonicity(state_A, state_B, lindbladian) -> bool
    mono = verify_cluster_refinement_monotonicity(rho_a, rho_b, l_zero)
    assert isinstance(mono, bool)
    assert mono is True


# ==============================================================================
# 6. Mathematical Invariants & Property Tests
# ==============================================================================


def test_unitary_covariance_of_cone_distance():
    """Cone distance is unitarily gauge-covariant: dist(U L U^dag, T^{feas}(U rho U^dag)) == dist(L, T^{feas}(rho))."""
    dim = 3
    # Rank 1 state
    rho = np.diag([1.0, 0.0, 0.0]).astype(complex)

    # Random direction
    np.random.seed(777)
    mat = np.random.randn(dim, dim) + 1j * np.random.randn(dim, dim)
    l_dir = (mat + mat.conj().T) / 2.0
    l_dir -= np.trace(l_dir) / dim * np.eye(dim)

    cone_base = FeasibleTangentCone(rho)
    dist_base = cone_base.distance(l_dir)

    # Random unitary U
    u_mat, _ = np.linalg.qr(np.random.randn(dim, dim) + 1j * np.random.randn(dim, dim))
    rho_rotated = u_mat @ rho @ u_mat.conj().T
    l_rotated = u_mat @ l_dir @ u_mat.conj().T

    cone_rotated = FeasibleTangentCone(rho_rotated)
    dist_rotated = cone_rotated.distance(l_rotated)

    assert np.isclose(dist_base, dist_rotated, atol=1e-11)


def test_tangent_cone_convexity_and_conical_scaling():
    """Feasible tangent cone is convex and closed under non-negative scaling."""
    rho = np.diag([1.0, 0.0, 0.0]).astype(complex)
    cone = FeasibleTangentCone(rho)

    # Two feasible directions (e.g. population leaving |0> into |1> and |2>)
    x1 = np.diag([-1.0, 1.0, 0.0]).astype(complex)
    x2 = np.diag([-1.0, 0.0, 1.0]).astype(complex)

    assert cone.is_feasible(x1)
    assert cone.is_feasible(x2)

    # Convex combination
    for alpha in [0.0, 0.25, 0.5, 0.75, 1.0]:
        x_combo = alpha * x1 + (1.0 - alpha) * x2
        assert cone.is_feasible(x_combo)

    # Non-negative scaling
    for c in [0.0, 0.5, 2.0, 10.0]:
        assert cone.is_feasible(c * x1)


def test_subadditivity_and_positive_homogeneity():
    """Cone distance satisfies subadditivity dist(L1 + L2) <= dist(L1) + dist(L2) and homogeneity."""
    dim = 3
    rho = np.diag([1.0, 0.0, 0.0]).astype(complex)
    cone = FeasibleTangentCone(rho)

    np.random.seed(888)
    m1 = np.random.randn(dim, dim) + 1j * np.random.randn(dim, dim)
    l1 = (m1 + m1.conj().T) / 2.0 - np.trace(m1 + m1.conj().T).real / (2 * dim) * np.eye(dim)

    m2 = np.random.randn(dim, dim) + 1j * np.random.randn(dim, dim)
    l2 = (m2 + m2.conj().T) / 2.0 - np.trace(m2 + m2.conj().T).real / (2 * dim) * np.eye(dim)

    d1 = cone.distance(l1)
    d2 = cone.distance(l2)
    d12 = cone.distance(l1 + l2)

    # Subadditivity (triangle inequality)
    assert d12 <= d1 + d2 + 1e-12

    # Positive homogeneity: dist(c * L) = c * dist(L)
    for c in [0.1, 0.5, 2.0, 5.0]:
        dc = cone.distance(c * l1)
        assert np.isclose(dc, c * d1, atol=1e-11)


def test_three_cluster_refinement_hierarchy():
    """Verify refinement hierarchy across 3-cluster partition: dist_{012} <= dist_{01, 2} <= dist_{0, 1, 2}."""
    rho_0 = np.array([[1.0, 0.0], [0.0, 0.0]], dtype=complex)
    rho_1 = np.array([[1.0, 0.0], [0.0, 0.0]], dtype=complex)
    rho_2 = np.array([[1.0, 0.0], [0.0, 0.0]], dtype=complex)

    m_3 = np.kron(np.kron(rho_0, rho_1), rho_2)

    # Entangling Hamiltonian across sites 0 and 1: X_0 (x) X_1 (x) I_2
    x = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
    h_01 = np.kron(np.kron(x, x), np.eye(2))

    l_3cluster = -1.0j * (h_01 @ m_3 - m_3 @ h_01)
    l_3cluster = (l_3cluster + l_3cluster.conj().T) / 2.0
    l_3cluster -= np.trace(l_3cluster) / 8.0 * np.eye(8)

    # 1. Fully unmerged partition {0}, {1}, {2}
    manifold_unmerged = ClusterProductManifold([rho_0, rho_1, rho_2])
    dist_0_1_2 = manifold_unmerged.feasible_tangent_distance(l_3cluster)

    # 2. Partially merged partition {0, 1}, {2}
    rho_01 = np.kron(rho_0, rho_1)
    manifold_partially_merged = ClusterProductManifold([rho_01, rho_2])
    dist_01_2 = manifold_partially_merged.feasible_tangent_distance(l_3cluster)

    # 3. Fully merged partition {0, 1, 2}
    cone_full = FeasibleTangentCone(m_3)
    dist_012 = cone_full.distance(l_3cluster)

    # Hierarchy: dist_012 <= dist_01_2 <= dist_0_1_2
    assert dist_012 <= dist_01_2 + 1e-7
    assert dist_01_2 <= dist_0_1_2 + 1e-7

    # Since H_01 is an internal interaction for {0, 1}, merging 0 and 1 strictly absorbs it:
    assert dist_01_2 < dist_0_1_2
    assert np.isclose(dist_012, 0.0, atol=1e-7)
    assert np.isclose(dist_01_2, 0.0, atol=1e-7)
    assert dist_0_1_2 > 1.5




def test_deterministic_property_bounds():
    """Deterministic property test: cone distance is non-negative, bounded by 2||L||_1, and achieves 0 duality gap."""
    pauli_x = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
    pauli_y = np.array([[0.0, -1j], [1j, 0.0]], dtype=complex)
    pauli_z = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)

    thetas = [0.0, np.pi / 4, np.pi / 2, 3 * np.pi / 4, np.pi]
    phis = [0.0, np.pi / 3, 2 * np.pi / 3, np.pi, 5 * np.pi / 3]
    vectors = [
        (1.0, 0.0, 0.0),
        (0.0, 1.0, 0.0),
        (0.0, 0.0, 1.0),
        (-0.5, 0.7, -0.2),
        (1.2, -0.8, 0.4),
    ]

    for theta in thetas:
        for phi in phis:
            psi = np.array(
                [np.cos(theta / 2.0), np.exp(1j * phi) * np.sin(theta / 2.0)],
                dtype=complex,
            )
            rho = np.outer(psi, psi.conj())
            cone = FeasibleTangentCone(rho)

            for l_x, l_y, l_z in vectors:
                l_pauli = l_x * pauli_x + l_y * pauli_y + l_z * pauli_z
                cert = cone.solve_distance_certified(l_pauli)

                # 1. Non-negativity
                assert cert.distance >= -1e-12

                # 2. Bounded by 2 ||L||_1
                norm_l = trace_norm(l_pauli)
                assert cert.distance <= 2.0 * norm_l + 1e-11

                # 3. Duality gap is zero within tolerance
                assert cert.duality_gap < 1e-11


def test_two_qubit_entangling_counterexample():
    """Verify Review Finding 1 two-qubit entangling counterexample.

    m = |00><00|, H = X (x) X => L = -i [H, m].
    Ambient distance is 0, both partial traces vanish, but product distance is 2.0
    certified with dual witness W = L and zero duality gap.
    """
    res = two_qubit_entangling_counterexample()
    assert res["status"] == "pass"
    assert res["ambient_cone_distance"] < 1e-10
    assert res["is_ambient_feasible"] is True
    assert res["partial_trace_a_norm"] < 1e-10
    assert res["partial_trace_b_norm"] < 1e-10
    assert np.isclose(res["product_cone_distance"], 2.0, atol=1e-5)
    assert np.isclose(res["dual_lower_bound"], 2.0, atol=1e-5)
    assert np.isclose(res["dual_witness_operator_norm"], 1.0, atol=1e-5)
    assert res["duality_gap"] < 1e-5

