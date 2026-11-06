"""Tests for SP5: Corrected Track B Physical Model Fences.

AuthorityEffect: None.
"""

import sys
import os
import math

import numpy as np
import pytest

from barbero_immirzi_fence import (
    action_density,
    deficit_4d,
    flat_packing_limit,
    escape_barrier,
    mcmc_valency_demo,
    THETA_4D,
)
from cosmological_ads_fence import (
    discrete_k6_sign_fixture,
    matter_deceleration,
    evaluate_declared_sign_cases,
)
from horizon_boundary_fence import (
    build_wheel_disk,
    absolute_h1_dimension,
    boundary_capacity_triangle,
    verify_horizon_fence,
)


class TestBarberoImmirzi:
    def test_theta_4d(self):
        assert abs(THETA_4D - math.acos(0.25)) < 1e-15

    def test_flat_packing_limit_is_4(self):
        assert flat_packing_limit() == 4

    def test_s6_approximate_value(self):
        s6 = action_density(6)
        assert abs(s6 - (-5.2688)) < 0.001

    def test_s6_is_minimum_on_3_to_8(self):
        s6 = action_density(6)
        for k in [3, 4, 5, 7, 8]:
            assert action_density(k) > s6 + 1e-6, (
                f"s({k}) = {action_density(k)} <= s(6) = {s6}"
            )

    def test_s10_below_s6_runaway(self):
        assert action_density(10) < action_density(6)

    def test_s15_below_s10(self):
        assert action_density(15) < action_density(10)

    def test_s25_below_s15(self):
        assert action_density(25) < action_density(15)

    def test_escape_barrier_corrected(self):
        result = escape_barrier()
        assert abs(result["barrier_to_k8_peak"] - 4.2916) < 0.001, (
            f"barrier = {result['barrier_to_k8_peak']} != 4.2916"
        )

    def test_escape_barrier_to_k7_is_1_6076(self):
        result = escape_barrier()
        assert abs(result["barrier_to_k7"] - 1.6076) < 0.001

    def test_runaway_at_k10_is_negative(self):
        result = escape_barrier()
        assert result["runaway_at_k10"] < 0, "s(10) should be < s(6)"

    def test_mcmc_constrained_concentrates_at_k6(self):
        result = mcmc_valency_demo(n_steps=50_000, k_range=(3, 8))
        assert result["fractions"][6] > 0.70, (
            f"constrained visits to k=6: {result['fractions'][6]:.2%} < 70%"
        )

    def test_mcmc_unconstrained_collapses_k6(self):
        result = mcmc_valency_demo(n_steps=50_000, k_range=(3, 15))
        assert result["fractions"][6] < 0.05, (
            f"unconstrained visits to k=6: {result['fractions'][6]:.2%} > 5%"
        )

    def test_linear_plunge_to_minus_infinity(self):
        """s(k) plunges to -infinity with average slope -THETA_4D for large k."""
        s_10 = action_density(10)
        s_25 = action_density(25)
        assert s_25 < s_10 - 15.0, f"s(25)={s_25} not significantly less than s(10)={s_10}"
        
        s_values = [action_density(k) for k in range(10, 100)]
        diffs = [s_values[i + 1] - s_values[i] for i in range(len(s_values) - 1)]
        avg_slope = np.mean(diffs)
        assert abs(avg_slope + THETA_4D) < 0.1, (
            f"avg slope {avg_slope} should be ≈ -{THETA_4D}"
        )


class TestSuppliedSignFixture:
    def test_epsilon_6_is_negative(self):
        result = discrete_k6_sign_fixture()
        assert result["epsilon_is_negative"]

    def test_s6_is_negative(self):
        result = discrete_k6_sign_fixture()
        assert result["action_is_negative"]

    def test_epsilon_6_value(self):
        result = discrete_k6_sign_fixture()
        assert abs(result["epsilon_6"] - (-1.6255)) < 0.001

    def test_deficit_is_negative(self):
        result = discrete_k6_sign_fixture()
        assert result["deficit_sign"] == "negative"

    @pytest.mark.parametrize(
        "rho,p",
        [(1.0, 0.0), (1.0, 0.333), (1.0, 1.0), (10.0, 0.0), (0.1, 0.01)],
    )
    def test_normal_matter_decelerates(self, rho, p):
        result = matter_deceleration(rho, p)
        assert result["decelerates"], (
            f"ρ={rho}, p={p}: ä/a = {result['a_ddot_over_a']} >= 0"
        )

    def test_declared_cases(self):
        result = evaluate_declared_sign_cases()
        assert result["all_normal_matter_decelerates"]
        assert result["k6_fixture"]["epsilon_is_negative"]
        assert result["k6_fixture"]["action_is_negative"]
        assert "no spacetime" in result["scope"]


class TestHorizonFence:
    def test_wheel_disk_nilpotency(self):
        d0, d1 = build_wheel_disk(6)
        assert np.allclose(d1 @ d0, 0)

    def test_absolute_h1_is_zero(self):
        d0, d1 = build_wheel_disk(6)
        result = absolute_h1_dimension(d0, d1)
        assert result["is_zero"], f"dim H^1 = {result['dim_H1']} != 0"

    def test_absolute_h1_zero_other_sizes(self):
        for n in [3, 4, 5, 8, 12]:
            d0, d1 = build_wheel_disk(n)
            result = absolute_h1_dimension(d0, d1)
            assert result["is_zero"], (
                f"n={n}: dim H^1 = {result['dim_H1']} != 0"
            )

    def test_boundary_capacity_is_4_not_6(self):
        result = boundary_capacity_triangle()
        assert result["capacity_is_4_not_6"], (
            f"capacity = {result['capacity']} != 4"
        )

    def test_comprehensive_fence(self):
        result = verify_horizon_fence()
        assert result["nilpotent"]
        assert result["absolute_h1"]["is_zero"]
        assert result["relative_h1_status"] == "requires_external_duality_transport"
        assert result["boundary_capacity"]["capacity_is_4_not_6"]
