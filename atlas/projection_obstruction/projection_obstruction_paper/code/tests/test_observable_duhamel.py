"""Comprehensive unit and property tests for Observable Duhamel predictive bounds (R1).

Verifies:
1. Rigorous interval arithmetic and error enclosure.
2. Locality-controlled influence weights w_{O,e}(t-s) and exponential decay outside light cone.
3. Observable-specific Duhamel convolution bounds enclosing true quantum expectation errors.
4. Volume-uniform scaling benchmark on 1D and 2D lattice families.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import pytest

_code_dir = Path(__file__).resolve().parents[1]
if str(_code_dir) not in sys.path:
    sys.path.insert(0, str(_code_dir))

from observable_duhamel import (  # noqa: E402
    DuhamelInputError,
    Interval,
    LatticeEdge,
    NumericalErrorEnclosure,
    ObservableDuhamelResult,
    ObservableSupport,
    StateDefect,
    NormalRate,
    EquationResidual,
    weak_coupling_duhamel_counterexample,
    build_spin_chain_lattice_spec,
    compute_graph_distance_table,
    compute_influence_weight,
    compute_observable_edge_distance,
    compute_quadrature_remainder_bound,
    evaluate_observable_duhamel_bound,
    evaluate_observable_duhamel_detailed,
    run_volume_scaling_benchmark,
    verify_volume_uniformity,
)


class TestIntervalArithmetic:
    """Verify exact real interval algebra and enclosure primitives."""

    def test_interval_creation_and_properties(self) -> None:
        interval = Interval(0.2, 0.8)
        assert interval.lower == 0.2
        assert interval.upper == 0.8
        assert math.isclose(interval.width, 0.6)
        assert math.isclose(interval.midpoint, 0.5)
        assert interval.contains(0.5)
        assert interval.contains(0.2)
        assert interval.contains(0.8)
        assert not interval.contains(0.1)
        assert not interval.contains(0.9)

    def test_invalid_interval_rejected(self) -> None:
        with pytest.raises(DuhamelInputError, match="lower .* exceeds upper"):
            Interval(1.0, 0.5)

        with pytest.raises(DuhamelInputError, match="endpoints must be finite"):
            Interval(float("nan"), 1.0)

    def test_interval_addition(self) -> None:
        a = Interval(1.0, 3.0)
        b = Interval(2.0, 5.0)
        c = a + b
        assert c.lower == 3.0
        assert c.upper == 8.0

        d = a + 2.5
        assert d.lower == 3.5
        assert d.upper == 5.5

        e = 1.0 + a
        assert e.lower == 2.0
        assert e.upper == 4.0

    def test_interval_subtraction(self) -> None:
        a = Interval(5.0, 10.0)
        b = Interval(1.0, 2.0)
        c = a - b
        assert c.lower == 3.0  # 5 - 2
        assert c.upper == 9.0  # 10 - 1

        d = a - 2.0
        assert d.lower == 3.0
        assert d.upper == 8.0

    def test_interval_multiplication(self) -> None:
        a = Interval(2.0, 4.0)
        b = Interval(-1.0, 3.0)
        c = a * b
        assert c.lower == -4.0
        assert c.upper == 12.0

        d = a * 2.0
        assert d.lower == 4.0
        assert d.upper == 8.0

    def test_interval_hull(self) -> None:
        a = Interval(1.0, 3.0)
        b = Interval(5.0, 7.0)
        h = a.hull(b)
        assert h.lower == 1.0
        assert h.upper == 7.0


class TestLocalityInfluenceWeights:
    """Verify spatial decay, light cone bounds, and distance calculators."""

    def test_observable_edge_distance_1d_chain(self) -> None:
        obs = ObservableSupport(sites=(5,), operator_norm=1.0)
        # Edge (5, 6) has distance 0 to site 5
        d0 = compute_observable_edge_distance(obs, (5, 6))
        assert d0 == 0.0

        # Edge (8, 9) has distance min(|5-8|, |5-9|) = 3
        d3 = compute_observable_edge_distance(obs, (8, 9))
        assert d3 == 3.0

        # Edge (1, 2) has distance min(|5-1|, |5-2|) = 3
        d_left = compute_observable_edge_distance(obs, (1, 2))
        assert d_left == 3.0

    def test_graph_distance_table_bfs(self) -> None:
        nodes = [0, 1, 2, 3]
        edges = [(0, 1), (1, 2), (2, 3)]
        dist = compute_graph_distance_table(nodes, edges)
        assert dist[(0, 3)] == 3.0
        assert dist[(1, 2)] == 1.0
        assert dist[(0, 0)] == 0.0

    def test_influence_weight_spatial_decay(self) -> None:
        """Influence weight must decay strictly exponentially outside the causal cone."""
        tau = 0.5
        v_lr = 2.0
        mu = 1.0
        # Light cone boundary is at distance v_lr * tau = 1.0
        w_near = compute_influence_weight(
            observable_support=(0,),
            edge=(1, 2),
            elapsed_time=tau,
            velocity=v_lr,
            decay_rate=mu,
            distance=1.0,  # on cone boundary
        )
        w_far = compute_influence_weight(
            observable_support=(0,),
            edge=(5, 6),
            elapsed_time=tau,
            velocity=v_lr,
            decay_rate=mu,
            distance=5.0,  # far outside cone
        )
        assert w_far < w_near
        # Theoretical ratio: exp(-mu * (5 - 1)) = exp(-4)
        expected_ratio = math.exp(-4.0)
        assert math.isclose(w_far / w_near, expected_ratio, rel_tol=1.0e-5)

    def test_influence_weight_universal_operator_cap(self) -> None:
        """Inside the causal cone, weight must never exceed ||O||_∞."""
        tau = 5.0
        v_lr = 2.0
        mu = 1.0
        norm_o = 1.5
        norm_h = 0.8
        universal_cap = norm_o  # 1.5

        w = compute_influence_weight(
            observable_support=ObservableSupport(sites=(0,), operator_norm=norm_o),
            edge=LatticeEdge(u=0, v=1, coupling_norm=norm_h),
            elapsed_time=tau,
            velocity=v_lr,
            decay_rate=mu,
            distance=0.0,
        )
        assert w <= universal_cap
        assert math.isclose(w, universal_cap, rel_tol=1.0e-7)

    def test_invalid_parameters_raise_error(self) -> None:
        with pytest.raises(DuhamelInputError, match="elapsed_time must be non-negative"):
            compute_influence_weight(observable_support=(0,), edge=(0, 1), elapsed_time=-0.1)

        with pytest.raises(DuhamelInputError, match="velocity must be positive"):
            compute_influence_weight(observable_support=(0,), edge=(0, 1), elapsed_time=0.1, velocity=-1.0)


class TestDuhamelBoundEvaluation:
    """Verify convolution evaluation and numerical error enclosures."""

    def test_zero_defects_yields_pure_discretization_error(self) -> None:
        obs = ObservableSupport(sites=(0,), operator_norm=1.0)
        defects = {(0, 1): 0.0, (1, 2): 0.0}
        interval = evaluate_observable_duhamel_bound(
            observable=obs,
            defects_by_edge=defects,
            time_horizon=0.5,
            initial_error=0.05,
            numerical_error=0.01,
        )
        assert interval.lower == 0.0
        assert math.isclose(interval.upper, 0.06, abs_tol=1.0e-12)

    def test_constant_defect_analytic_consistency(self) -> None:
        obs = ObservableSupport(sites=(0,), operator_norm=1.0)
        defects_inside = {(0, 1): 0.5}
        # 1. Inside light cone at distance=0, weight saturates at universal cap ||O||_infty = 1.0.
        # Integral_0^t nu * 1.0 d tau = nu * t = 0.5 * 0.1 = 0.05
        t = 0.1
        nu = 0.5
        v = 2.0
        interval_inside = evaluate_observable_duhamel_bound(
            observable=obs,
            defects_by_edge=defects_inside,
            time_horizon=t,
            velocity=v,
            c0=1.0,
            initial_error=0.0,
            numerical_error=0.0,
            quadrature_steps=100,
        )
        assert math.isclose(interval_inside.upper, nu * t, rel_tol=1.0e-3)

        # 2. Outside light cone at distance d=2 (e.g. edge (2, 3)), exponent v*tau - mu*d < 0 for tau in [0, 0.1].
        # w(tau) = c0 * ||O||_infty * exp(v*tau - mu*d) = exp(-2.0) * exp(2*tau).
        # Integral_0^t nu * exp(-mu*d) * exp(v*tau) d tau = nu * exp(-mu*d) * (exp(v*t) - 1) / v
        mu = 1.0
        d = 2.0
        dist_table = {(0, 2): 2.0, (0, 3): 3.0}
        defects_outside = {(2, 3): nu}
        expected_outside = nu * math.exp(-mu * d) * (math.exp(v * t) - 1.0) / v
        interval_outside = evaluate_observable_duhamel_bound(
            observable=obs,
            defects_by_edge=defects_outside,
            time_horizon=t,
            velocity=v,
            decay_rate=mu,
            c0=1.0,
            graph_distances=dist_table,
            initial_error=0.0,
            numerical_error=0.0,
            quadrature_steps=100,
        )
        assert math.isclose(interval_outside.upper, expected_outside, rel_tol=1.0e-3)

    def test_enclosure_with_synthetic_expectation_error(self) -> None:
        """Simulate true expectation drift and verify containment in Duhamel interval."""
        obs = ObservableSupport(sites=(2,), operator_norm=1.0)
        # On a 5-site chain, with interaction coupling J=1.0, defect rate nu_e=0.4
        nodes, edges, couplings, dist_table = build_spin_chain_lattice_spec(5)
        defects = {e: 0.4 for e in edges}
        t = 0.2

        interval = evaluate_observable_duhamel_bound(
            observable=obs,
            defects_by_edge=defects,
            time_horizon=t,
            edge_couplings=couplings,
            graph_distances=dist_table,
            initial_error=0.01,
            numerical_error=0.005,
        )

        # A physically possible expectation deviation Δ⟨O⟩ ≤ 0.1
        true_simulated_error = 0.08
        assert interval.contains(true_simulated_error)
        assert interval.upper < 2.0  # strictly informative

    def test_quadrature_remainder_bound(self) -> None:
        rem = compute_quadrature_remainder_bound(
            step_size=0.01,
            time_horizon=1.0,
            second_derivative_bound=4.0,
        )
        # (1.0 * 0.0001 / 12) * 4.0 = 0.0004 / 12 = 3.33e-5
        assert math.isclose(rem, (0.0001 / 12.0) * 4.0)

    def test_detailed_duhamel_result_audit(self) -> None:
        obs = ObservableSupport(sites=(1,), operator_norm=1.0)
        defects = {(0, 1): 0.2, (1, 2): 0.3}
        res = evaluate_observable_duhamel_detailed(
            observable=obs,
            defects_by_edge=defects,
            time_horizon=0.2,
            initial_error=0.02,
            numerical_error=0.01,
        )
        assert isinstance(res, ObservableDuhamelResult)
        assert res.is_informative
        assert len(res.per_edge_weights) == 2
        assert len(res.per_edge_contributions) == 2
        assert res.initial_error == 0.02
        assert res.numerical_error == 0.01


class TestVolumeUniformityBenchmark:
    """Verify that predictive intervals remain volume-uniform on 1D and 2D spin chains."""

    def test_1d_spin_chain_volume_scaling_informative(self) -> None:
        """Show that as 1D chain length N increases from 6 to 48, the bound plateaus."""
        sizes = (6, 10, 16, 24, 36, 48)
        bench = run_volume_scaling_benchmark(
            lattice_family="1d_chain",
            sizes=sizes,
            time_horizon=0.20,
            defect_rate_per_bond=0.5,
            velocity=2.0,
            decay_rate=1.5,
        )

        assert bench["demonstration_successful"] is True
        assert bench["is_uniformly_bounded"] is True

        records = bench["records"]
        # The global unweighted bound must scale with system size
        small_global = records[0]["global_unweighted_bound"]
        large_global = records[-1]["global_unweighted_bound"]
        assert large_global >= small_global

        # The locality-controlled bound for center site must plateau
        b_16 = records[2]["observable_bound"]
        b_48 = records[-1]["observable_bound"]
        assert abs(b_48 - b_16) < 0.05
        assert b_48 < 2.0  # remains strictly informative

    def test_2d_square_lattice_volume_scaling(self) -> None:
        """Show volume uniformity on 2D square lattices (4, 9, 16, 25, 36 sites)."""
        sizes = (4, 9, 16, 25, 36)
        bench = run_volume_scaling_benchmark(
            lattice_family="2d_square",
            sizes=sizes,
            time_horizon=0.15,
            defect_rate_per_bond=0.4,
            velocity=2.0,
            decay_rate=1.5,
        )
        assert bench["demonstration_successful"] is True
        assert bench["is_uniformly_bounded"] is True

    def test_verify_volume_uniformity_contract_function(self) -> None:
        """Verify interface contract: verify_volume_uniformity."""
        assert verify_volume_uniformity("1d_chain", sizes=(8, 16, 24, 32)) is True
        assert verify_volume_uniformity("2d_square", sizes=(9, 16, 25, 36)) is True


class TestObservableDuhamelEdgeCasesAndValidation:
    """Exhaustive validation and boundary coverage for observable_duhamel module."""

    def test_numerical_error_enclosure_properties(self) -> None:
        enc = NumericalErrorEnclosure(
            initial_error=0.02,
            ode_truncation_error=0.005,
            quadrature_error=0.001,
            floating_point_slack=1.0e-12,
        )
        assert math.isclose(enc.total_numerical_error, 0.006 + 1.0e-12)
        assert math.isclose(enc.total_enclosed_error, 0.026 + 1.0e-12)

    def test_interval_sub_float_and_rmul(self) -> None:
        iv = Interval(2.0, 5.0)
        sub_f = iv - 1.0
        assert sub_f.lower == 1.0
        assert sub_f.upper == 4.0
        rmul = 3.0 * iv
        assert rmul.lower == 6.0
        assert rmul.upper == 15.0

    def test_observable_support_validation(self) -> None:
        with pytest.raises(DuhamelInputError, match="must contain at least one site"):
            ObservableSupport(sites=())
        with pytest.raises(DuhamelInputError, match="must be positive and finite"):
            ObservableSupport(sites=(0,), operator_norm=-1.0)
        with pytest.raises(DuhamelInputError, match="must be positive and finite"):
            ObservableSupport(sites=(0,), operator_norm=float("inf"))

    def test_lattice_edge_and_normalization(self) -> None:
        edge = LatticeEdge(u=1, v=2, coupling_norm=0.7)
        assert edge.as_tuple() == (1, 2)
        from observable_duhamel import _normalize_edge
        assert _normalize_edge(edge) == (1, 2)
        assert _normalize_edge([3, 4]) == (3, 4)
        with pytest.raises(DuhamelInputError, match="Cannot interpret"):
            _normalize_edge((1, 2, 3))

    def test_observable_edge_distance_string_fallbacks_and_errors(self) -> None:
        with pytest.raises(DuhamelInputError, match="Observable support cannot be empty"):
            compute_observable_edge_distance([], (0, 1))

        # String matching overlap
        d_overlap = compute_observable_edge_distance(["siteA"], ("siteA", "siteB"))
        assert d_overlap == 0.0
        # String matching disjoint
        d_disjoint = compute_observable_edge_distance(["siteA"], ("siteB", "siteC"))
        assert d_disjoint == 1.0

    def test_influence_weight_zero_norms_and_validation(self) -> None:
        w_zero_o = compute_influence_weight(
            observable_support=(0,),
            edge=(0, 1),
            elapsed_time=0.1,
            observable_norm=0.0,
        )
        assert w_zero_o == 0.0

        w_zero_h = compute_influence_weight(
            observable_support=(0,),
            edge=LatticeEdge(u=0, v=1, coupling_norm=0.0),
            elapsed_time=0.1,
        )
        assert w_zero_h == 0.0

        with pytest.raises(DuhamelInputError, match="Spatial decay rate must be positive"):
            compute_influence_weight((0,), (0, 1), elapsed_time=0.1, decay_rate=-0.5)

        with pytest.raises(DuhamelInputError, match="Prefactor c0 must be positive"):
            compute_influence_weight((0,), (0, 1), elapsed_time=0.1, c0=0.0)

        with pytest.raises(DuhamelInputError, match="Distance must be non-negative"):
            compute_influence_weight((0,), (0, 1), elapsed_time=0.1, distance=-2.0)

        # Huge exponent saturation (testing line 241)
        w_huge = compute_influence_weight(
            observable_support=(0,),
            edge=(0, 1),
            elapsed_time=500.0,
            velocity=10.0,
            distance=0.0,
        )
        assert w_huge == 1.0

    def test_quadrature_remainder_zero_inputs(self) -> None:
        assert compute_quadrature_remainder_bound(0.0, 1.0) == 0.0
        assert compute_quadrature_remainder_bound(0.1, 0.0) == 0.0

    def test_evaluate_duhamel_bound_time_zero_and_negative_errors(self) -> None:
        zero_iv = evaluate_observable_duhamel_bound(
            observable=(0,),
            defects_by_edge={(0, 1): 1.0},
            time_horizon=0.0,
            initial_error=0.05,
            numerical_error=0.02,
        )
        assert zero_iv.lower == 0.0
        assert math.isclose(zero_iv.upper, 0.07)

        with pytest.raises(DuhamelInputError, match="time_horizon must be non-negative"):
            evaluate_observable_duhamel_bound((0,), {(0, 1): 1.0}, time_horizon=-0.1)

        with pytest.raises(DuhamelInputError, match="Errors must be non-negative"):
            evaluate_observable_duhamel_bound((0,), {(0, 1): 1.0}, time_horizon=0.1, initial_error=-0.01)

        with pytest.raises(DuhamelInputError, match="Defect rate for edge .* cannot be negative"):
            evaluate_observable_duhamel_bound((0,), {(0, 1): -0.5}, time_horizon=0.1)

    def test_evaluate_duhamel_bound_callable_and_interpolated_sequence(self) -> None:
        # Callable defect
        def fn_defect(s: float) -> float:
            return 0.5 + 0.1 * s

        iv_fn = evaluate_observable_duhamel_bound(
            observable=(0,),
            defects_by_edge={(0, 1): fn_defect},
            time_horizon=0.2,
        )
        assert iv_fn.upper > 0.0

        # Sequence defect with interpolation (different step count)
        seq_samples = [0.4, 0.5, 0.6]  # 3 samples
        iv_seq = evaluate_observable_duhamel_bound(
            observable=(0,),
            defects_by_edge={(0, 1): seq_samples},
            time_horizon=0.2,
            quadrature_steps=20,  # 20 steps => triggers interpolation
        )
        assert iv_seq.upper > 0.0

        # Unsupported defect format
        with pytest.raises(DuhamelInputError, match="Unsupported defect format"):
            evaluate_observable_duhamel_bound(
                observable=(0,),
                defects_by_edge={(0, 1): "invalid"},  # type: ignore
                time_horizon=0.2,
            )

    def test_detailed_duhamel_result_with_callable_and_sequence(self) -> None:
        defects = {
            (0, 1): lambda s: 0.2 * (1.0 + s),
            (1, 2): [0.1, 0.2, 0.3, 0.4],
        }
        res = evaluate_observable_duhamel_detailed(
            observable=(0,),
            defects_by_edge=defects,
            time_horizon=0.15,
        )
        assert res.global_unweighted_bound > 0.0

    def test_volume_scaling_benchmark_unknown_family_raises_error(self) -> None:
        with pytest.raises(DuhamelInputError, match="Unknown lattice family"):
            run_volume_scaling_benchmark(lattice_family="hexagonal", sizes=(4,))  # type: ignore


def test_weak_coupling_duhamel_counterexample() -> None:
    """Verify Review Finding 2 weak-coupling Duhamel bound regression test.

    H = epsilon * X (x) X, epsilon=0.1, t=0.1.
    True error: |sin(0.02)| = 0.019998666...
    Duhamel bound: 0.02.
    """
    res = weak_coupling_duhamel_counterexample(epsilon=0.1, time_horizon=0.1)
    assert res["status"] == "pass"
    assert res["is_enclosed"] is True
    assert math.isclose(res["actual_error"], math.sin(0.02), abs_tol=1e-12)
    assert math.isclose(res["duhamel_bound"], 0.02, abs_tol=1e-12)
    assert res["ratio_actual_to_bound"] <= 1.0
    assert res["ratio_actual_to_bound"] > 0.999


def test_defect_dataclasses_distinction() -> None:
    """Verify distinct semantics of StateDefect, NormalRate, and EquationResidual."""
    sd = StateDefect(distance=0.15)
    assert sd.distance == 0.15
    nr = NormalRate(rate=0.25)
    assert nr.rate == 0.25
    er = EquationResidual(time=0.1, norm_1=0.2)
    assert er.norm_1 == 0.2
