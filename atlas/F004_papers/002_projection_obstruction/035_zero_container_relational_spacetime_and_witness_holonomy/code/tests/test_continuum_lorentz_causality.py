"""Standalone test suite for emergent continuum Lorentz causality and relational observer packet.

Covers all 8 standalone tests specified for Milestone M1 (Requirement X7):
1. test_relational_continuum_observer_packet_initialization
2. test_gauge_repair_quotient_admissibility
3. test_causal_light_cone_emergence_and_timelike_saturation
4. test_spacelike_exponential_tail_suppression
5. test_continuum_refinement_scaling_limit
6. test_discrete_4current_relativistic_conservation_o_a2
7. test_lorentz_boost_invariance_of_causal_boundary
8. test_continuum_lorentz_fail_closed_validation

AuthorityEffect: None.
"""

from __future__ import annotations

import dataclasses
import math

import numpy as np
import pytest
from continuum_lorentz_causality import (
    CarrierNetwork,
    ContinuumCausalityError,
    analyze_continuum_scaling_limit,
    apply_lorentz_boost,
    build_relational_continuum_packet,
    classify_causal_sector,
    compute_lorentz_causal_envelope,
    compute_quotient_residual_lp,
    setup_scaling_grid,
    simulate_defect_wave_packet,
    verify_conservation_convergence_order,
    verify_lorentz_boost_invariance,
)


def test_relational_continuum_observer_packet_initialization() -> None:
    """Verify initialization, 9-tuple elements, Bianchi identity d1 @ d0 == 0, and immutability."""
    packet = build_relational_continuum_packet(
        num_sites=5,
        defect_values=[0.1, 0.2, 0.15, 0.05],
    )
    assert len(packet.carrier_nodes_k) == 5
    assert len(packet.adjacency_r) == 4
    assert packet.defect_operator_delta.shape == (4,)

    # Verify Bianchi identity d1 @ d0 == 0
    d0 = packet.gauge_shifts_d0
    d1 = packet.cycle_check_d1
    bianchi_product = np.matmul(d1, d0)
    assert np.allclose(bianchi_product, 0.0, atol=1.0e-14)

    # Verify trace norm J
    expected_j = sum([0.1, 0.2, 0.15, 0.05])  # 0.50
    assert math.isclose(packet.gauge_norm_j, expected_j, abs_tol=1.0e-14)

    # Verify immutability
    with pytest.raises(dataclasses.FrozenInstanceError):
        packet.gauge_norm_j = 1.0  # type: ignore[misc]

    # Verify CarrierNetwork chain complex on a 2-simplicial triangle complex
    tri_carrier = CarrierNetwork(
        nodes=(0, 1, 2),
        edges=((0, 1), (1, 2), (0, 2)),
        faces=((0, 1, 2),),
    )
    assert tri_carrier.num_nodes == 3
    assert tri_carrier.num_edges == 3
    assert tri_carrier.num_faces == 1
    assert tri_carrier.hop_distance(0, 2) == 1
    assert tri_carrier.verify_coboundary_complex() is True


def test_gauge_repair_quotient_admissibility() -> None:
    """Verify quotient repair admissibility via dynamic LP solving on open chains, rings, and simplicial carriers."""
    # Case 1: Pure gauge induced by 0-cochain alpha on open chain -> AUTHORIZED
    packet_pure = build_relational_continuum_packet(
        num_sites=4,
        gauge_alpha=[1.5, 0.5, -0.5, -1.0],
    )
    assert packet_pure.causal_terminalizer_tau == "AUTHORIZED"
    assert packet_pure.terminalize() == "AUTHORIZED"
    assert packet_pure.is_pure_gauge is True
    assert packet_pure.quotient_residual == 0.0
    assert packet_pure.operational_stickiness == 0.0

    # Case 2: Tree topology (1D open chain) has H^1 = 0 -> any defect is pure gauge modulo im(d^0)
    packet_tree = build_relational_continuum_packet(
        num_sites=4,
        defect_values=[1.0, 0.0, 0.0],
    )
    assert packet_tree.causal_terminalizer_tau == "AUTHORIZED"
    assert packet_tree.terminalize() == "AUTHORIZED"
    assert packet_tree.is_pure_gauge is True
    assert math.isclose(packet_tree.quotient_residual, 0.0, abs_tol=1.0e-10)
    assert math.isclose(packet_tree.operational_stickiness, 0.0, abs_tol=1.0e-10)

    # Case 3: Periodic closed ring C_4 has H^1 != 0 -> non-zero circulation is OBSTRUCTED
    packet_obs_periodic = build_relational_continuum_packet(
        num_sites=4,
        defect_values=[1.0, 0.0, 0.0, 0.0],
        periodic=True,
    )
    assert packet_obs_periodic.causal_terminalizer_tau == "OBSTRUCTED"
    assert packet_obs_periodic.terminalize() == "OBSTRUCTED"
    assert packet_obs_periodic.is_pure_gauge is False
    assert packet_obs_periodic.quotient_residual > 0.0
    assert packet_obs_periodic.operational_stickiness > 0.0

    # Case 4: Simplicial CarrierNetwork 1-cycle has H^1 != 0 -> uniform circulation is OBSTRUCTED
    carrier_tri = CarrierNetwork(
        nodes=(0, 1, 2),
        edges=((0, 1), (1, 2), (2, 0)),
    )
    packet_tri = build_relational_continuum_packet(
        carrier=carrier_tri,
        defect_values=[1.0, 1.0, 1.0],
    )
    assert packet_tri.causal_terminalizer_tau == "OBSTRUCTED"
    assert packet_tri.terminalize() == "OBSTRUCTED"
    assert packet_tri.is_pure_gauge is False
    assert math.isclose(packet_tri.quotient_residual, 3.0, abs_tol=1.0e-8)
    assert math.isclose(packet_tri.operational_stickiness, 3.0, abs_tol=1.0e-8)

    # Case 5: 2-simplicial complex with 2-face: non-zero curvature residual triggers REFUSAL
    carrier_face = CarrierNetwork(
        nodes=(0, 1, 2),
        edges=((0, 1), (1, 2), (0, 2)),
        faces=((0, 1, 2),),
    )
    # Boundary defect: d1 delta = 1.0 + 1.0 - 0.0 = 2.0 != 0
    packet_refusal = build_relational_continuum_packet(
        carrier=carrier_face,
        defect_values=[1.0, 1.0, 0.0],
    )
    assert packet_refusal.causal_terminalizer_tau == "REFUSAL"
    assert packet_refusal.terminalize() == "REFUSAL"
    assert packet_refusal.is_pure_gauge is False
    assert packet_refusal.quotient_residual > 0.0

    # Case 6: Direct LP calculation verification on closed loop
    d0_cycle = np.array([
        [-1.0,  1.0,  0.0],
        [ 0.0, -1.0,  1.0],
        [ 1.0,  0.0, -1.0],
    ], dtype=np.float64)
    circulation_delta = np.array([1.0, 1.0, 1.0], dtype=np.float64)
    lp_result = compute_quotient_residual_lp(d0_cycle, circulation_delta)
    assert lp_result.is_pure_gauge is False
    assert lp_result.quotient_residual > 0.5
    assert lp_result.operational_stickiness > 0.5

    pure_delta = d0_cycle @ np.array([2.0, 1.0, 0.0])
    lp_pure_res = compute_quotient_residual_lp(d0_cycle, pure_delta)
    assert lp_pure_res.is_pure_gauge is True
    assert math.isclose(lp_pure_res.quotient_residual, 0.0, abs_tol=1.0e-10)


def test_causal_light_cone_emergence_and_timelike_saturation() -> None:
    """Verify timelike saturation at operator-norm envelope and null cone boundary classification."""
    grid = setup_scaling_grid(
        lattice_spacing_a=0.05,
        system_length=1.0,
        v_lr=2.0,
        spatial_decay_mu=1.0,
    )

    # Timelike evaluation: d = 0.2, tau = 0.5, c_eff = 2.0 -> s^2 = (2*0.5)^2 - 0.2^2 = 0.96
    res_timelike = compute_lorentz_causal_envelope(
        grid=grid,
        distance=0.2,
        elapsed_time=0.5,
        observable_norm=1.5,
        edge_norm=1.0,
    )
    assert res_timelike.classification == "TIMELIKE"
    assert res_timelike.minkowski_interval_s2 > 0.0
    assert math.isclose(res_timelike.minkowski_interval_s2, 0.96, abs_tol=1.0e-12)
    assert math.isclose(res_timelike.influence_weight, 3.0, abs_tol=1.0e-12)
    assert res_timelike.acausal_leakage == 0.0
    assert res_timelike.is_within_light_cone is True

    # Null cone boundary: d = 1.0, tau = 0.5, c_eff = 2.0 -> s^2 = 1.0 - 1.0 = 0.0
    res_null = compute_lorentz_causal_envelope(
        grid=grid,
        distance=1.0,
        elapsed_time=0.5,
        observable_norm=1.5,
        edge_norm=1.0,
    )
    assert res_null.classification == "NULL"
    assert math.isclose(res_null.minkowski_interval_s2, 0.0, abs_tol=1.0e-12)
    assert math.isclose(res_null.influence_weight, 3.0, abs_tol=1.0e-12)
    assert res_null.is_within_light_cone is True


def test_spacelike_exponential_tail_suppression() -> None:
    """Verify that influence weights outside the light cone decay strictly exponentially."""
    grid = setup_scaling_grid(
        lattice_spacing_a=0.05,
        system_length=2.0,
        v_lr=1.0,
        spatial_decay_mu=2.0,
    )

    res1 = compute_lorentz_causal_envelope(grid=grid, distance=0.6, elapsed_time=0.4)
    res2 = compute_lorentz_causal_envelope(grid=grid, distance=0.8, elapsed_time=0.4)

    assert res1.classification == "SPACELIKE"
    assert res2.classification == "SPACELIKE"
    assert res1.minkowski_interval_s2 < 0.0
    assert res2.minkowski_interval_s2 < 0.0
    assert res1.is_within_light_cone is False
    assert res2.is_within_light_cone is False

    # Theoretical values: w = 2.0 * exp(exponent)
    # exponent_1 = -(2.0 / 0.05) * (0.6 - 1.0 * 0.4) = -40 * 0.2 = -8.0
    # exponent_2 = -(2.0 / 0.05) * (0.8 - 1.0 * 0.4) = -40 * 0.4 = -16.0
    expected_w1 = 2.0 * math.exp(-8.0)
    expected_w2 = 2.0 * math.exp(-16.0)
    assert math.isclose(res1.influence_weight, expected_w1, rel_tol=1.0e-7)
    assert math.isclose(res2.influence_weight, expected_w2, rel_tol=1.0e-7)

    # Ratio verification: exp(-mu/a * (0.8 - 0.6)) = exp(-8.0)
    ratio = res2.influence_weight / res1.influence_weight
    assert math.isclose(ratio, math.exp(-8.0), rel_tol=1.0e-7)
    assert res2.influence_weight < 1.0e-6


def test_continuum_refinement_scaling_limit() -> None:
    """Verify monotonic exponential collapse of spacelike leakage as lattice pitch a -> 0."""
    spacings = [0.10, 0.05, 0.025, 0.0125]
    weights = []
    for a in spacings:
        g = setup_scaling_grid(
            lattice_spacing_a=a,
            system_length=1.0,
            v_lr=1.0,
            spatial_decay_mu=2.0,
        )
        res = compute_lorentz_causal_envelope(g, distance=0.6, elapsed_time=0.3)
        weights.append(res.influence_weight)

    # Monotonic decrease outside the cone
    assert weights[0] > weights[1] > weights[2] > weights[3]
    # a = 0.10   -> exp(-2.0 * 0.3 / 0.10)   = exp(-6.0)
    # a = 0.05   -> exp(-2.0 * 0.3 / 0.05)   = exp(-12.0)
    # a = 0.025  -> exp(-2.0 * 0.3 / 0.025)  = exp(-24.0)
    # a = 0.0125 -> exp(-2.0 * 0.3 / 0.0125) = exp(-48.0)
    assert math.isclose(weights[0], 2.0 * math.exp(-6.0), rel_tol=1.0e-6)
    assert math.isclose(weights[1], 2.0 * math.exp(-12.0), rel_tol=1.0e-6)
    assert math.isclose(weights[2], 2.0 * math.exp(-24.0), rel_tol=1.0e-6)
    assert weights[3] < 1.0e-18

    # Convergence diagnostics over spatial domain
    analysis = analyze_continuum_scaling_limit(
        spacings=spacings[:3],
        elapsed_time_tau=0.3,
        v_lr=1.0,
        spatial_decay_mu=2.0,
    )
    assert analysis.is_converging is True
    assert analysis.spacelike_leakages[2] < analysis.spacelike_leakages[0]


def test_discrete_4current_relativistic_conservation_o_a2() -> None:
    """Verify second-order O(a^2) convergence of discrete defect 4-current continuity equation."""
    spacings = (0.10, 0.05, 0.025)
    report = verify_conservation_convergence_order(
        spacings=spacings,
        t_eval=0.1,
        c_eff=1.0,
    )

    assert report.is_second_order is True
    assert len(report.convergence_orders) == 2
    # Order 1 (between 0.10 and 0.05)
    assert 1.90 <= report.convergence_orders[0] <= 2.10
    # Order 2 (between 0.05 and 0.025)
    assert 1.90 <= report.convergence_orders[1] <= 2.10
    assert 1.95 <= report.mean_order <= 2.05

    # Ratio check: R(a) / R(a/2) approx 4.0
    ratio_1 = report.residuals[0] / report.residuals[1]
    ratio_2 = report.residuals[1] / report.residuals[2]
    assert math.isclose(ratio_1, 4.0, rel_tol=0.05)
    assert math.isclose(ratio_2, 4.0, rel_tol=0.05)


def test_lorentz_boost_invariance_of_causal_boundary() -> None:
    """Verify exact invariance of Minkowski interval s^2 under relational Lorentz boosts."""
    c = 2.0
    beta = 0.6

    # Test null separation: dt = 1.0, dx = 2.0 -> s^2 = 4(1)^2 - 2^2 = 0.0
    dt_null, dx_null = 1.0, 2.0
    dt_p, dx_p = apply_lorentz_boost(dt_null, dx_null, c_eff=c, beta=beta)
    s2_orig = c ** 2 * dt_null ** 2 - dx_null ** 2
    s2_boosted = c ** 2 * dt_p ** 2 - dx_p ** 2
    assert math.isclose(s2_orig, 0.0, abs_tol=1.0e-14)
    assert math.isclose(s2_boosted, 0.0, abs_tol=1.0e-14)

    # Test timelike separation: dt = 2.0, dx = 1.0 -> s^2 = 4(4) - 1 = 15.0
    dt_time, dx_time = 2.0, 1.0
    dt_tp, dx_tp = apply_lorentz_boost(dt_time, dx_time, c_eff=c, beta=beta)
    s2_t_orig = c ** 2 * dt_time ** 2 - dx_time ** 2
    s2_t_boosted = c ** 2 * dt_tp ** 2 - dx_tp ** 2
    assert math.isclose(s2_t_orig, 15.0, abs_tol=1.0e-14)
    assert math.isclose(s2_t_boosted, 15.0, abs_tol=1.0e-14)

    # Spacelike separation invariance via verify_lorentz_boost_invariance helper
    s2_s, s2_sp, is_inv = verify_lorentz_boost_invariance(
        separation_d=3.0,
        elapsed_time_tau=0.5,
        boost_velocity=1.2,
        c_eff=c,
    )
    assert is_inv is True
    assert math.isclose(s2_s, s2_sp, abs_tol=1.0e-14)

    # Superluminal boost (|beta| >= 1) must fail closed with ContinuumCausalityError
    with pytest.raises(ContinuumCausalityError, match="subluminal"):
        apply_lorentz_boost(1.0, 1.0, c_eff=c, beta=1.0)


def test_continuum_lorentz_fail_closed_validation() -> None:
    """Verify that non-physical, degenerate, or invalid inputs fail closed immediately."""
    # Non-positive lattice spacing
    with pytest.raises(ContinuumCausalityError, match="lattice_spacing_a must be positive"):
        setup_scaling_grid(lattice_spacing_a=0.0)
    with pytest.raises(ContinuumCausalityError, match="lattice_spacing_a must be positive"):
        setup_scaling_grid(lattice_spacing_a=-0.05)

    # Boolean subclass guard
    with pytest.raises(ContinuumCausalityError, match="lattice_spacing_a must be positive"):
        setup_scaling_grid(lattice_spacing_a=True)  # type: ignore[arg-type]

    # Negative elapsed time
    grid = setup_scaling_grid(lattice_spacing_a=0.1)
    with pytest.raises(ContinuumCausalityError, match="elapsed_time must be non-negative"):
        compute_lorentz_causal_envelope(grid, distance=0.5, elapsed_time=-0.1)

    # Negative distance
    with pytest.raises(ContinuumCausalityError, match="distance must be non-negative"):
        compute_lorentz_causal_envelope(grid, distance=-0.5, elapsed_time=0.1)

    # Non-positive Lieb-Robinson velocity
    with pytest.raises(ContinuumCausalityError, match="v_lr must be positive"):
        setup_scaling_grid(lattice_spacing_a=0.1, v_lr=0.0)

    # Disconnected nodes in carrier hop distance
    disc_carrier = CarrierNetwork(nodes=(0, 1), edges=())
    with pytest.raises(ContinuumCausalityError, match="No path between"):
        disc_carrier.hop_distance(0, 1)

    # CarrierNetwork hop_distance unknown node rejection and boolean rejection
    c_net = CarrierNetwork(nodes=(0, 1), edges=((0, 1),))
    with pytest.raises(ContinuumCausalityError, match="Source node 999 not in carrier nodes"):
        c_net.hop_distance(999, 0)
    with pytest.raises(ContinuumCausalityError, match="Target node 999 not in carrier nodes"):
        c_net.hop_distance(0, 999)
    with pytest.raises(ContinuumCausalityError, match="Source node 999 not in carrier nodes"):
        c_net.hop_distance(999, 999)
    with pytest.raises(ContinuumCausalityError, match="must be int or str, not bool"):
        c_net.hop_distance(True, 0)  # type: ignore[arg-type]
    with pytest.raises(ContinuumCausalityError, match="must be int or str, not bool"):
        c_net.hop_distance(0, False)  # type: ignore[arg-type]

    # CarrierNetwork topology validation
    with pytest.raises(ContinuumCausalityError, match="CarrierNetwork must have at least one node"):
        CarrierNetwork(nodes=(), edges=())
    with pytest.raises(ContinuumCausalityError, match="Carrier node True must be int or str, not bool"):
        CarrierNetwork(nodes=(True, 0), edges=())  # type: ignore[arg-type]
    with pytest.raises(ContinuumCausalityError, match="Duplicate edge"):
        CarrierNetwork(nodes=(0, 1), edges=((0, 1), (0, 1)))
    with pytest.raises(ContinuumCausalityError, match="Duplicate or anti-parallel edge"):
        CarrierNetwork(nodes=(0, 1), edges=((0, 1), (1, 0)))
    with pytest.raises(ContinuumCausalityError, match="Self-loop edge"):
        CarrierNetwork(nodes=(0,), edges=((0, 0),))
    with pytest.raises(ContinuumCausalityError, match="references non-existent node"):
        CarrierNetwork(nodes=(0,), edges=((0, 1),))
    with pytest.raises(ContinuumCausalityError, match="Face.*vertices must be distinct"):
        CarrierNetwork(nodes=(0, 1), edges=((0, 1),), faces=((0, 0, 1),))
    with pytest.raises(ContinuumCausalityError, match="Face boundary edge.*not in edges"):
        CarrierNetwork(nodes=(0, 1, 2), edges=((0, 1), (1, 2)), faces=((0, 1, 2),))

    # Fewer than 2 sites in packet construction
    with pytest.raises(ContinuumCausalityError, match="num_sites must be at least 2"):
        build_relational_continuum_packet(num_sites=1)


def test_simulate_defect_wave_packet_minimum_grid_points() -> None:
    """Verify that coarse grids (a >= L/2) and invalid stencil parameters fail closed."""
    # Coarse lattice with a = 100.0, L = 1.0 (yielding len(xs) = 1)
    grid_coarse = setup_scaling_grid(lattice_spacing_a=100.0, system_length=1.0)
    with pytest.raises(ContinuumCausalityError, match="at least 3 sites"):
        simulate_defect_wave_packet(grid_coarse, t_max=0.1)

    # Coarse lattice with a = 0.7, L = 1.0 (yielding len(xs) = 2)
    grid_two = setup_scaling_grid(lattice_spacing_a=0.7, system_length=1.0)
    with pytest.raises(ContinuumCausalityError, match="at least 3 sites"):
        simulate_defect_wave_packet(grid_two, t_max=0.1)

    # Valid grid with at least 3 sites succeeds
    grid_valid = setup_scaling_grid(lattice_spacing_a=0.1, system_length=1.0)
    field = simulate_defect_wave_packet(grid_valid, t_max=0.1, n_times=5)
    assert field.max_residual >= 0.0

    # Guard checks for n_times, t_max, sigma
    with pytest.raises(ContinuumCausalityError, match="n_times must be an integer >= 3"):
        simulate_defect_wave_packet(grid_valid, t_max=0.1, n_times=2)
    with pytest.raises(ContinuumCausalityError, match="n_times must be an integer >= 3"):
        simulate_defect_wave_packet(grid_valid, t_max=0.1, n_times=True)  # type: ignore[arg-type]
    with pytest.raises(ContinuumCausalityError, match="t_max must be positive"):
        simulate_defect_wave_packet(grid_valid, t_max=0.0)
    with pytest.raises(ContinuumCausalityError, match="sigma must be positive"):
        simulate_defect_wave_packet(grid_valid, t_max=0.1, sigma=0.0)


def test_verify_conservation_convergence_order_high_velocity_and_guards() -> None:
    """Verify that dynamic domain centering preserves second-order convergence for c_eff >= 60.0."""
    spacings = (0.10, 0.05, 0.025)
    # High-velocity test: c_eff = 60.0
    report_fast = verify_conservation_convergence_order(
        spacings=spacings,
        t_eval=0.1,
        c_eff=60.0,
    )
    assert report_fast.is_second_order is True
    assert 1.90 <= report_fast.mean_order <= 2.10

    # Guard checks for non-positive / boolean parameters
    with pytest.raises(ContinuumCausalityError, match="c_eff must be positive"):
        verify_conservation_convergence_order(spacings, c_eff=0.0)
    with pytest.raises(ContinuumCausalityError, match="c_eff must be positive"):
        verify_conservation_convergence_order(spacings, c_eff=-1.0)
    with pytest.raises(ContinuumCausalityError, match="sigma must be positive"):
        verify_conservation_convergence_order(spacings, sigma=-0.25)
    with pytest.raises(ContinuumCausalityError, match="t_eval must be positive"):
        verify_conservation_convergence_order(spacings, t_eval=-0.1)
    with pytest.raises(ContinuumCausalityError, match="spacings\\[1\\] must be positive"):
        verify_conservation_convergence_order((0.1, True))  # type: ignore[arg-type]
    with pytest.raises(ContinuumCausalityError, match="at least two spacings"):
        verify_conservation_convergence_order((0.1,))


def test_verify_lorentz_boost_invariance_ultra_relativistic() -> None:
    """Verify that ultra-relativistic boosts (1 - beta = 1e-6) remain invariant under scaled tolerance."""
    c = 1.0
    beta = 1.0 - 1.0e-6
    s2_o, s2_p, is_inv = verify_lorentz_boost_invariance(
        separation_d=0.5,
        elapsed_time_tau=1.0,
        boost_velocity=beta * c,
        c_eff=c,
    )
    assert is_inv is True
    assert math.isclose(s2_o, 0.75, abs_tol=1.0e-12)

    # Subluminal bounds
    with pytest.raises(ContinuumCausalityError, match="subluminal"):
        verify_lorentz_boost_invariance(
            separation_d=0.5,
            elapsed_time_tau=1.0,
            boost_velocity=1.0,
            c_eff=1.0,
        )


def test_input_guards_and_fail_closed_adversarial_vectors() -> None:
    """Verify fail-closed rejection of booleans, NaNs, and negative inputs across public API."""
    # 1. build_relational_continuum_packet guards
    with pytest.raises(ContinuumCausalityError, match="num_sites must be integer"):
        build_relational_continuum_packet(num_sites=2.5)  # type: ignore[arg-type]
    with pytest.raises(ContinuumCausalityError, match="num_sites must be integer"):
        build_relational_continuum_packet(num_sites=True)  # type: ignore[arg-type]
    with pytest.raises(ContinuumCausalityError, match="c_eff must be positive"):
        build_relational_continuum_packet(num_sites=3, c_eff=-1.0)
    with pytest.raises(ContinuumCausalityError, match="c_eff must be positive"):
        build_relational_continuum_packet(num_sites=3, c_eff=True)  # type: ignore[arg-type]
    with pytest.raises(ContinuumCausalityError, match="elapsed_time must be non-negative"):
        build_relational_continuum_packet(num_sites=3, elapsed_time=-1.0)
    with pytest.raises(ContinuumCausalityError, match="elapsed_time must be non-negative"):
        build_relational_continuum_packet(num_sites=3, elapsed_time=True)  # type: ignore[arg-type]
    with pytest.raises(ContinuumCausalityError, match="distance must be non-negative"):
        build_relational_continuum_packet(num_sites=3, distance=-1.0)
    with pytest.raises(ContinuumCausalityError, match="distance must be non-negative"):
        build_relational_continuum_packet(num_sites=3, distance=True)  # type: ignore[arg-type]

    # 2. classify_causal_sector guards
    with pytest.raises(ContinuumCausalityError, match="minkowski_interval_s2 must be a finite number"):
        classify_causal_sector(True)  # type: ignore[arg-type]
    with pytest.raises(ContinuumCausalityError, match="tolerance must be non-negative"):
        classify_causal_sector(10.0, tolerance=float("nan"))
    with pytest.raises(ContinuumCausalityError, match="tolerance must be non-negative"):
        classify_causal_sector(10.0, tolerance=-1.0e-5)

    # 3. apply_lorentz_boost & verify_lorentz_boost_invariance guards
    with pytest.raises(ContinuumCausalityError, match="dt must be a finite number"):
        apply_lorentz_boost(dt=True, dx=0.0, c_eff=1.0, beta=0.5)  # type: ignore[arg-type]
    with pytest.raises(ContinuumCausalityError, match="dx must be a finite number"):
        apply_lorentz_boost(dt=1.0, dx=False, c_eff=1.0, beta=0.5)  # type: ignore[arg-type]
    with pytest.raises(ContinuumCausalityError, match="separation_d must be non-negative"):
        verify_lorentz_boost_invariance(separation_d=True, elapsed_time_tau=1.0, boost_velocity=0.5, c_eff=1.0)  # type: ignore[arg-type]
    with pytest.raises(ContinuumCausalityError, match="separation_d must be non-negative"):
        verify_lorentz_boost_invariance(separation_d=-1.0, elapsed_time_tau=1.0, boost_velocity=0.5, c_eff=1.0)
    with pytest.raises(ContinuumCausalityError, match="separation_d must be non-negative"):
        verify_lorentz_boost_invariance(separation_d=float("nan"), elapsed_time_tau=1.0, boost_velocity=0.5, c_eff=1.0)
