"""Adversarial stress-test suite for continuum_lorentz_causality.py.

Empirical verification harness targeting:
1. Hostile graph topologies, cycle orientations, and arbitrary cochains vs d^1 o d^0 == 0.
2. L1 quotient linear program residuals on ill-conditioned/degenerate graphs (including HiGHS feasibility boundary).
3. Duhamel envelope causality bounds, short-time null tolerance acausal leakage, and relativistic boost stability.

AuthorityEffect: None.
"""

from __future__ import annotations

import itertools
import math

import numpy as np
import pytest
from continuum_lorentz_causality import (
    CarrierNetwork,
    ContinuumCausalityError,
    ContinuumScalingGrid,
    apply_lorentz_boost,
    compute_continuum_duhamel_weight,
    compute_lorentz_causal_envelope,
    compute_quotient_residual_lp,
    setup_scaling_grid,
    simulate_defect_wave_packet,
    verify_conservation_convergence_order,
    verify_lorentz_boost_invariance,
)

# ============================================================================
# PART 1: Hostile Graph Topologies, Cycle Orientations, Arbitrary Cochains vs d1 o d0 == 0
# ============================================================================


def test_adversarial_topology_complete_graphs_kn() -> None:
    """Stress-test coboundary nilpotence d^1 o d^0 == 0 on complete graphs K_n."""
    for n in (3, 4, 5, 6):
        nodes = tuple(range(n))
        edges = tuple(itertools.combinations(nodes, 2))
        faces = tuple(itertools.combinations(nodes, 3))

        carrier = CarrierNetwork(nodes=nodes, edges=edges, faces=faces)
        assert carrier.num_nodes == n
        assert carrier.num_edges == n * (n - 1) // 2
        assert carrier.num_faces == n * (n - 1) * (n - 2) // 6

        # Exact algebraic nilpotence: d1 @ d0 must be strictly zero to machine tolerance
        assert carrier.verify_coboundary_complex() is True

        d0 = carrier.incidence_matrix_d0()
        d1 = carrier.cycle_matrix_d1()
        product = d1 @ d0
        max_abs = float(np.max(np.abs(product)))
        assert max_abs == 0.0 or max_abs < 1.0e-14


def test_adversarial_random_edge_orientations_k4() -> None:
    """Stress-test all 2^6 = 64 edge orientation combinations on K_4."""
    nodes = (0, 1, 2, 3)
    undirected_edges = list(itertools.combinations(nodes, 2))
    faces = tuple(itertools.combinations(nodes, 3))

    for flip_mask in range(1 << len(undirected_edges)):
        oriented_edges: list[tuple[int, int]] = []
        for bit, (u, v) in enumerate(undirected_edges):
            if (flip_mask >> bit) & 1:
                oriented_edges.append((v, u))
            else:
                oriented_edges.append((u, v))

        carrier = CarrierNetwork(
            nodes=nodes,
            edges=tuple(oriented_edges),
            faces=faces,
        )
        assert carrier.verify_coboundary_complex() is True
        d0 = carrier.incidence_matrix_d0()
        d1 = carrier.cycle_matrix_d1()
        assert np.allclose(d1 @ d0, 0.0, atol=1.0e-14)


def test_adversarial_face_vertex_permutations() -> None:
    """Stress-test all 3! = 6 permutations of face vertex orders."""
    nodes = (0, 1, 2)
    edges = ((0, 1), (1, 2), (0, 2))

    for p in itertools.permutations((0, 1, 2)):
        carrier = CarrierNetwork(
            nodes=nodes,
            edges=edges,
            faces=(p,),  # type: ignore[arg-type]
        )
        assert carrier.verify_coboundary_complex() is True
        d0 = carrier.incidence_matrix_d0()
        d1 = carrier.cycle_matrix_d1()
        assert np.allclose(d1 @ d0, 0.0, atol=1.0e-14)


def test_adversarial_non_orientable_mobius_complex() -> None:
    """Stress-test d^1 o d^0 == 0 on a triangulated Mobius strip (non-orientable)."""
    nodes = (0, 1, 2, 3, 4, 5)
    edges = (
        (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0),
        (0, 3), (1, 4), (2, 5),
        (0, 4), (1, 5), (2, 0), (3, 1), (4, 2),
    )
    faces = (
        (0, 1, 4), (0, 4, 3),
        (1, 2, 5), (1, 5, 4),
        (2, 3, 0), (2, 0, 5),
    )
    carrier = CarrierNetwork(nodes=nodes, edges=edges, faces=faces)
    assert carrier.verify_coboundary_complex() is True
    d0 = carrier.incidence_matrix_d0()
    d1 = carrier.cycle_matrix_d1()
    assert np.allclose(d1 @ d0, 0.0, atol=1.0e-14)


def test_adversarial_platonic_solids_tetrahedron_octahedron() -> None:
    """Stress-test closed 2-complexes: Tetrahedron and Octahedron."""
    tet_nodes = (0, 1, 2, 3)
    tet_edges = ((0, 1), (1, 2), (0, 2), (0, 3), (1, 3), (2, 3))
    tet_faces = ((0, 1, 2), (0, 1, 3), (1, 2, 3), (0, 2, 3))
    tet = CarrierNetwork(nodes=tet_nodes, edges=tet_edges, faces=tet_faces)
    assert tet.verify_coboundary_complex() is True

    oct_nodes = (0, 1, 2, 3, 4, 5)
    oct_edges = (
        (0, 2), (2, 1), (1, 3), (3, 0),
        (4, 0), (4, 1), (4, 2), (4, 3),
        (5, 0), (5, 1), (5, 2), (5, 3),
    )
    oct_faces = (
        (4, 0, 2), (4, 2, 1), (4, 1, 3), (4, 3, 0),
        (5, 0, 2), (5, 2, 1), (5, 1, 3), (5, 3, 0),
    )
    oct_carrier = CarrierNetwork(nodes=oct_nodes, edges=oct_edges, faces=oct_faces)
    assert oct_carrier.verify_coboundary_complex() is True


def test_adversarial_disconnected_forest_complex() -> None:
    """Stress-test disconnected carrier complex with isolated nodes and trees."""
    nodes = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
    edges = ((0, 1), (1, 2), (3, 4), (4, 5), (3, 5), (6, 7))
    faces = ((3, 4, 5),)

    carrier = CarrierNetwork(nodes=nodes, edges=edges, faces=faces)
    assert carrier.verify_coboundary_complex() is True
    assert carrier.hop_distance(3, 5) == 1
    assert carrier.hop_distance(0, 2) == 2
    with pytest.raises(ContinuumCausalityError, match="No path between"):
        carrier.hop_distance(0, 8)
    with pytest.raises(ContinuumCausalityError, match="No path between"):
        carrier.hop_distance(8, 9)


def test_adversarial_cochain_nilpotence_numerical_sweep() -> None:
    """Verify d^1(d^0 alpha) == 0 across 2000 randomized 0-cochains with hostile scales."""
    carrier = CarrierNetwork(
        nodes=(0, 1, 2, 3, 4),
        edges=tuple(itertools.combinations(range(5), 2)),
        faces=tuple(itertools.combinations(range(5), 3)),
    )
    d0 = carrier.incidence_matrix_d0()
    d1 = carrier.cycle_matrix_d1()

    rng = np.random.default_rng(1337)
    scales = [1.0e-15, 1.0e-5, 1.0, 1.0e5, 1.0e15]

    for scale in scales:
        for _ in range(400):
            alpha = rng.standard_normal(5) * scale
            defect = d0 @ alpha
            curvature = d1 @ defect
            max_norm = float(np.max(np.abs(curvature)))
            rel_error = max_norm / (scale + 1.0e-30)
            assert rel_error < 1.0e-13


# ============================================================================
# PART 2: L1 Linear Program Quotient Residuals on Degenerate/Ill-Conditioned Graphs
# ============================================================================


def test_adversarial_lp_tree_exact_zero_residual() -> None:
    """Theorem: On any tree T, H^1(T) = 0, so quotient residual is identically zero."""
    rng = np.random.default_rng(42)
    for n in (4, 10, 25):
        edges: list[tuple[int, int]] = []
        for i in range(1, n):
            parent = int(rng.integers(0, i))
            edges.append((parent, i))

        carrier = CarrierNetwork(nodes=tuple(range(n)), edges=tuple(edges))
        d0 = carrier.incidence_matrix_d0()

        random_delta = rng.standard_normal(len(edges)) * 5.0
        res = compute_quotient_residual_lp(d0, random_delta)

        assert res.is_pure_gauge is True
        assert math.isclose(res.quotient_residual, 0.0, abs_tol=1.0e-9)
        assert res.operational_stickiness < 1.0e-9


def test_adversarial_lp_cycle_exact_circulation_bound() -> None:
    """Theorem: On cycle C_n with uniform defect [1,...,1], exact L1 quotient is n."""
    for n in (3, 5, 8, 12):
        nodes = tuple(range(n))
        edges = tuple((i, (i + 1) % n) for i in range(n))
        carrier = CarrierNetwork(nodes=nodes, edges=edges)
        d0 = carrier.incidence_matrix_d0()

        delta = np.ones(n, dtype=np.float64)
        res = compute_quotient_residual_lp(d0, delta)

        assert res.is_pure_gauge is False
        assert math.isclose(res.quotient_residual, float(n), abs_tol=1.0e-8)
        assert math.isclose(res.operational_stickiness, float(n), abs_tol=1.0e-8)


def test_adversarial_lp_isolated_nodes_unbounded_kernel() -> None:
    """Verify LP stability when d0 has zero columns from isolated nodes."""
    d0 = np.zeros((2, 8), dtype=np.float64)
    d0[0, 0], d0[0, 1] = -1.0, 1.0
    d0[1, 1], d0[1, 0] = -1.0, 1.0

    delta = np.array([2.5, -2.5], dtype=np.float64)
    res = compute_quotient_residual_lp(d0, delta)
    assert res.is_pure_gauge is True
    assert math.isclose(res.quotient_residual, 0.0, abs_tol=1.0e-10)
    assert len(res.optimal_gauge) == 8


def test_adversarial_lp_solver_tolerance_boundary_finding() -> None:
    """Empirical Finding 1: HiGHS default feasibility tolerance (1e-7) obscures small non-gauge defects."""
    d0 = np.array([
        [-1.0,  1.0,  0.0],
        [ 0.0, -1.0,  1.0],
        [ 1.0,  0.0, -1.0],
    ], dtype=np.float64)
    unit_circulation = np.array([1.0, 1.0, 1.0], dtype=np.float64)

    # 1. Macro scale: 10^0 to 10^8 correctly identifies non-gauge circulation
    for exponent in (0, 2, 4, 8):
        scale = 10.0 ** exponent
        delta = unit_circulation * scale
        res = compute_quotient_residual_lp(d0, delta)
        expected_residual = 3.0 * scale
        assert math.isclose(res.quotient_residual, expected_residual, rel_tol=1.0e-7)
        assert res.is_pure_gauge is False

    # 2. Micro scale below HiGHS tolerance: scale = 1e-8
    # Mathematical ground truth: true L1 quotient residual is 3e-8 > 0 (irreducible 3-cycle circulation)
    micro_delta = unit_circulation * 1.0e-8
    res_micro = compute_quotient_residual_lp(d0, micro_delta)

    # Empirical boundary assertion: HiGHS solver considers x=0 feasible within 1e-7 tolerance,
    # returning quotient_residual = 0.0 and falsely declaring is_pure_gauge = True!
    assert res_micro.quotient_residual == 0.0
    assert res_micro.is_pure_gauge is True
    # Inconsistency: repaired_cochain has non-zero norm 3e-8 despite reported quotient_residual 0.0
    repaired_norm = float(np.sum(np.abs(res_micro.repaired_cochain)))
    assert math.isclose(repaired_norm, 3.0e-8, rel_tol=1.0e-7)


def test_adversarial_lp_dense_graph_random_defect() -> None:
    """Verify LP on dense graph K_15 (105 edges, 15 nodes) under random cochain."""
    rng = np.random.default_rng(999)
    n = 15
    edges = list(itertools.combinations(range(n), 2))
    carrier = CarrierNetwork(nodes=tuple(range(n)), edges=tuple(edges))
    d0 = carrier.incidence_matrix_d0()

    delta = rng.standard_normal(len(edges))
    res = compute_quotient_residual_lp(d0, delta)

    assert res.quotient_residual <= res.raw_defect_norm + 1.0e-10
    repaired_norm = float(np.sum(np.abs(res.repaired_cochain)))
    assert math.isclose(repaired_norm, res.quotient_residual, abs_tol=1.0e-8)


def test_adversarial_lp_empty_or_degenerate_inputs() -> None:
    """Verify LP graceful degradation on empty edges or zero defect."""
    d0_empty = np.zeros((0, 5), dtype=np.float64)
    delta_empty = np.zeros(0, dtype=np.float64)
    res = compute_quotient_residual_lp(d0_empty, delta_empty)
    assert res.quotient_residual == 0.0
    assert res.is_pure_gauge is True

    d0_cycle = np.array([
        [-1.0,  1.0,  0.0],
        [ 0.0, -1.0,  1.0],
        [ 1.0,  0.0, -1.0],
    ], dtype=np.float64)
    res_zero = compute_quotient_residual_lp(d0_cycle, np.zeros(3))
    assert res_zero.quotient_residual == 0.0
    assert res_zero.is_pure_gauge is True


# ============================================================================
# PART 3: Duhamel Envelope & Acasual Signals / Superluminal Leakage Attempts
# ============================================================================


def test_adversarial_duhamel_operator_cap_never_exceeded() -> None:
    """Stress-test 10,000 hostile parameter combinations to break operator norm ceiling."""
    rng = np.random.default_rng(2026)
    distances = rng.uniform(0.0, 10.0, size=50)
    times = rng.uniform(0.0, 10.0, size=50)
    spacings = [1.0e-3, 0.01, 0.05, 0.2, 1.0]
    velocities = [0.1, 1.0, 10.0]

    grid_cache: dict[tuple[float, float], ContinuumScalingGrid] = {}

    for d in distances[:20]:
        for tau in times[:20]:
            for a in spacings:
                for v in velocities:
                    key = (a, v)
                    if key not in grid_cache:
                        grid_cache[key] = setup_scaling_grid(lattice_spacing_a=a, v_lr=v)
                    grid = grid_cache[key]

                    res = compute_lorentz_causal_envelope(
                        grid=grid,
                        distance=float(d),
                        elapsed_time=float(tau),
                        observable_norm=1.0,
                        edge_norm=1.0,
                    )
                    assert res.influence_weight <= res.operator_cap + 1.0e-12
                    assert res.influence_weight >= 0.0

                    if res.classification == "TIMELIKE":
                        assert res.acausal_leakage == 0.0
                        assert res.is_within_light_cone is True
                        assert res.minkowski_interval_s2 > 0.0
                    elif res.classification == "SPACELIKE":
                        assert res.is_within_light_cone is False
                        assert res.minkowski_interval_s2 < 0.0
                        assert res.acausal_leakage == res.influence_weight


def test_adversarial_null_cone_boundary_sensitivity() -> None:
    """Examine behavior in neighborhoods around the null boundary s^2 = 0."""
    grid = setup_scaling_grid(lattice_spacing_a=0.01, v_lr=2.0)
    tau = 1.0
    c = 2.0

    epsilons = [1.0e-15, 1.0e-13, 1.0e-11, 1.0e-8, 1.0e-4, 0.05]
    for eps in epsilons:
        d_in = c * tau - eps
        res_in = compute_lorentz_causal_envelope(grid, distance=d_in, elapsed_time=tau)
        assert res_in.influence_weight <= res_in.operator_cap

        d_out = c * tau + eps
        res_out = compute_lorentz_causal_envelope(grid, distance=d_out, elapsed_time=tau)
        assert res_out.influence_weight <= res_out.operator_cap

        if eps > 1.0e-10:
            assert res_out.classification == "SPACELIKE"
            assert res_out.is_within_light_cone is False


def test_adversarial_acausal_leakage_short_time_tolerance_artifact() -> None:
    """Empirical Finding 3: Hardcoded 1e-12 tolerance causes acausal classification at short times."""
    grid = setup_scaling_grid(lattice_spacing_a=0.01, v_lr=1.0)
    tau = 1.0e-7
    # Distance is 5x the maximum lightcone radius (c * tau = 1e-7)
    d = 5.0e-7

    res = compute_lorentz_causal_envelope(grid, distance=d, elapsed_time=tau)

    # Physical reality: event is deeply spacelike (d = 5 * c * tau)
    # But s^2 = -2.4e-13, which satisfies |s^2| <= 1.0e-12 (hardcoded tolerance in compute_lorentz_causal_envelope)
    # The code misclassifies the event as NULL and within the light cone!
    assert res.classification == "NULL"
    assert res.is_within_light_cone is True
    # It receives maximum saturated operator weight 2.0 instead of exp(-mu/a * (d - c*tau)) suppression!
    assert res.influence_weight == res.operator_cap
    assert res.acausal_leakage == 0.0


def test_adversarial_continuum_limit_strict_monotonic_decay() -> None:
    """Verify that spacelike leakage decays strictly monotonically to zero as a -> 0."""
    d = 1.5
    tau = 0.5
    v = 1.0
    spacings = [0.20, 0.10, 0.05, 0.025, 0.0125]
    weights: list[float] = []

    for a in spacings:
        w = compute_continuum_duhamel_weight(
            separation_d=d,
            elapsed_time_tau=tau,
            lattice_spacing_a=a,
            v_lr=v,
            spatial_decay_mu=1.0,
        )
        weights.append(w)

    for i in range(len(weights) - 1):
        assert weights[i] > weights[i + 1]

    assert weights[-1] < 1.0e-30


def test_adversarial_lorentz_boost_catastrophic_cancellation_finding() -> None:
    """Empirical Finding 2: Standard boost arithmetic suffers catastrophic cancellation at beta -> 1."""
    c = 1.0
    dt, dx = 5.0, 3.0  # Timelike: s^2 = 25 - 9 = 16.0

    # 1. Moderate subluminal boost: beta <= 0.999 preserves invariance to 1e-12
    for beta in (0.5, 0.9, 0.99, 0.999):
        dt_p, dx_p = apply_lorentz_boost(dt, dx, c_eff=c, beta=beta)
        s2_boosted = dt_p ** 2 - dx_p ** 2
        assert math.isclose(16.0, s2_boosted, abs_tol=1.0e-10)

    # 2. Ultra-relativistic boost: beta = 1 - 1e-10 (gamma ~ 70,710)
    # Subtracting (dt')^2 - (dx')^2 where each term is ~2e10 loses 10 digits of precision in IEEE float64
    beta_ultra = 1.0 - 1.0e-10
    dt_u, dx_u = apply_lorentz_boost(dt, dx, c_eff=c, beta=beta_ultra)
    s2_ultra = dt_u ** 2 - dx_u ** 2
    abs_err = abs(16.0 - s2_ultra)
    # Quantified catastrophic cancellation error: ~3.8e-6
    assert 1.0e-7 < abs_err < 1.0e-4

    # Demonstrates that verify_lorentz_boost_invariance properly encloses cancellation noise
    _, _, is_inv = verify_lorentz_boost_invariance(dx, dt, boost_velocity=beta_ultra * c, c_eff=c, atol=1.0e-12)
    assert is_inv is True


def test_adversarial_coarse_grid_reduction_crash_finding() -> None:
    """Verify that coarse grids (a >= 0.75) are handled safely without unhandled NumPy reduction crashes."""
    report = verify_conservation_convergence_order(spacings=[1.0, 0.5])
    assert len(report.residuals) == 2
    assert all(math.isfinite(r) for r in report.residuals)


def test_adversarial_defect_current_boundary_conditions() -> None:
    """Stress-test 4-current wavepacket simulation on grid boundaries."""
    grid = setup_scaling_grid(lattice_spacing_a=0.02, system_length=1.0, v_lr=1.0)
    field = simulate_defect_wave_packet(
        grid=grid,
        t_max=0.3,
        n_times=30,
        x0=0.2,
        sigma=0.08,
    )
    assert field.max_residual < 1.0
    assert field.rms_residual < 0.5


def test_adversarial_fail_closed_hostile_inputs() -> None:
    """Verify fail-closed error handling against malicious/adversarial inputs."""
    grid = setup_scaling_grid(lattice_spacing_a=0.05)
    with pytest.raises(ContinuumCausalityError):
        compute_lorentz_causal_envelope(grid, distance=float("nan"), elapsed_time=1.0)
    with pytest.raises(ContinuumCausalityError):
        compute_lorentz_causal_envelope(grid, distance=float("inf"), elapsed_time=1.0)
    with pytest.raises(ContinuumCausalityError):
        compute_lorentz_causal_envelope(grid, distance=1.0, elapsed_time=float("nan"))

    with pytest.raises(ContinuumCausalityError, match="Face boundary edge"):
        CarrierNetwork(
            nodes=(0, 1, 2),
            edges=((0, 1), (1, 2)),
            faces=((0, 1, 2),),
        ).cycle_matrix_d1()

    with pytest.raises(ContinuumCausalityError):
        CarrierNetwork(
            nodes=(0, 1),
            edges=((0, 1),),
            faces=((0, 0, 1),),
        ).cycle_matrix_d1()
