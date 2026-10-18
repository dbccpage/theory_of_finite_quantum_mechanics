"""Tests for SP1: L1 Hodge Split Inflation Ceiling on C3.

Verifies:
  1. R_split(e_i) == 7/3 for all 3 basis indicators
  2. No counterexample occurs in a declared random sample
  3. R_rep(omega) == 1 for non-coboundaries
  4. Phi_1/Phi_2 == sqrt(3) for non-trivial cohomology classes
  5. R_split(e_0) on C_n equals 3 - 2/n
  6. Selected interior fixtures have R_split < 7/3

AuthorityEffect: None.
"""

import sys
import os
import math

import numpy as np
import pytest

from hodge_split_c3 import (
    compute_split_inflation,
    compute_split_inflation_cn,
    sample_split_bound_c3,
)


SEVEN_THIRDS = 7.0 / 3.0
SQRT3 = math.sqrt(3.0)


class TestBasisIndicators:
    """R_split must equal exactly 7/3 at single-edge indicators."""

    @pytest.mark.parametrize("idx", [0, 1, 2])
    def test_positive_basis(self, idx):
        e = np.zeros(3)
        e[idx] = 1.0
        result = compute_split_inflation(e)
        assert abs(result["R_split"] - SEVEN_THIRDS) < 1e-12

    @pytest.mark.parametrize("idx", [0, 1, 2])
    def test_negative_basis(self, idx):
        e = np.zeros(3)
        e[idx] = -1.0
        result = compute_split_inflation(e)
        assert abs(result["R_split"] - SEVEN_THIRDS) < 1e-12


class TestProposedCeilingFalsification:
    """Finite probes of the proposed global 7/3 ceiling."""

    def test_random_cochains_satisfy_bound(self):
        result = sample_split_bound_c3(n_samples=10_000, seed=123)
        assert result["scope"] == "random_sample_only"
        assert result["satisfies_bound"], (
            f"max R_split = {result['max_R_split']} > 7/3 = {SEVEN_THIRDS}"
        )
        assert result["max_R_split"] < SEVEN_THIRDS + 1e-10

    def test_interior_points_strictly_below(self):
        """The selected non-vertex fixtures are strictly below 7/3."""
        interior_points = [
            np.array([0.5, 0.3, 0.2]),
            np.array([0.4, 0.4, 0.2]),
            np.array([1.0 / 3, 1.0 / 3, 1.0 / 3]),
            np.array([0.6, 0.2, 0.2]),
            np.array([0.5, 0.5, 0.0]),
        ]
        for omega in interior_points:
            result = compute_split_inflation(omega)
            assert result["R_split"] < SEVEN_THIRDS - 1e-6, (
                f"omega={omega}: R_split={result['R_split']} not strictly < 7/3"
            )


class TestRepresentativeOptimality:
    """R_rep == 1 identically for all non-coboundaries on C3."""

    @pytest.mark.parametrize(
        "omega",
        [
            np.array([1.0, 0.0, 0.0]),
            np.array([1.0, 2.0, 3.0]),
            np.array([0.1, 0.2, 0.7]),
            np.array([-1.0, 2.0, -0.5]),
            np.array([100.0, 200.0, 300.0]),
        ],
    )
    def test_R_rep_equals_one(self, omega):
        result = compute_split_inflation(omega)
        if abs(np.sum(omega)) > 1e-12:  # non-coboundary
            assert abs(result["R_rep"] - 1.0) < 1e-12

    def test_coboundary_is_indeterminate(self):
        """For exact coboundaries (s=0), R_rep is 0/0."""
        omega = np.array([1.0, -1.0, 0.0])  # sum = 0, in im(d0)
        result = compute_split_inflation(omega)
        assert math.isnan(result["R_rep"])


class TestQuotientNormRatio:
    """Phi_1/Phi_2 == sqrt(3) on all non-trivial cohomology classes of C3."""

    @pytest.mark.parametrize(
        "omega",
        [
            np.array([1.0, 0.0, 0.0]),
            np.array([1.0, 1.0, 1.0]),
            np.array([3.0, 7.0, 11.0]),
            np.array([-2.0, 5.0, -1.0]),
        ],
    )
    def test_ratio_equals_sqrt3(self, omega):
        result = compute_split_inflation(omega)
        if abs(np.sum(omega)) > 1e-12:
            assert abs(result["ratio"] - SQRT3) < 1e-12, (
                f"ratio={result['ratio']} != sqrt(3)={SQRT3}"
            )


class TestCycleScaling:
    """On C_n, R_split(e_0) = 3 - 2/n."""

    @pytest.mark.parametrize("n", [3, 4, 5, 6, 10, 20, 100])
    def test_single_edge_scaling(self, n):
        e0 = np.zeros(n)
        e0[0] = 1.0
        result = compute_split_inflation_cn(e0, n)
        expected = 3.0 - 2.0 / n
        assert abs(result["R_split"] - expected) < 1e-12, (
            f"C_{n}: R_split={result['R_split']} != {expected}"
        )

    def test_c3_matches_seven_thirds(self):
        e0 = np.zeros(3)
        e0[0] = 1.0
        result = compute_split_inflation_cn(e0, 3)
        assert abs(result["R_split"] - SEVEN_THIRDS) < 1e-12

    def test_approaches_3_as_n_grows(self):
        e0 = np.zeros(1000)
        e0[0] = 1.0
        result = compute_split_inflation_cn(e0, 1000)
        assert abs(result["R_split"] - 2.998) < 0.01
