"""Tests for SP4: SM/SUSY Proximity Census and Linear Energy Obstruction.

AuthorityEffect: None.
"""

import sys
import os

import numpy as np
import pytest

from sm_susy_proximity import exhaustive_census, feature_vector, GROUP_MENU, SM_TARGET
from linear_energy_obstruction import (
    pure_l1_energy,
    coboundary_d0_c3,
    verify_linear_energy,
)


class TestSMProximity:
    def test_min_distance_is_3(self):
        result = exhaustive_census()
        assert result["min_distance"] == 3.0

    def test_minimizers_are_d4_and_q8(self):
        result = exhaustive_census()
        names = {tuple(t) for t in result["min_triples"]}
        assert ("D4", "Z3", "1") in names
        assert ("Q8", "Z3", "1") in names

    def test_shadow_distance_is_11(self):
        result = exhaustive_census()
        assert result["shadow_distance"] == 11.0

    def test_searched_all_1000(self):
        result = exhaustive_census()
        assert result["n_triples_searched"] == 1000

    def test_no_distance_below_3(self):
        result = exhaustive_census()
        assert result["min_distance"] >= 3.0

    def test_finite_groups_have_no_lie_algebra(self):
        """Feature coordinate 6 (compact-connected Lie extra) is 0 for all finite groups."""
        for i2 in range(10):
            for i1 in range(10):
                for i0 in range(10):
                    fv = feature_vector(GROUP_MENU[i2][0], GROUP_MENU[i1][0], GROUP_MENU[i0][0])
                    assert fv[6] == 0.0


class TestLinearEnergy:
    def test_degree_1_homogeneity(self):
        d0 = coboundary_d0_c3()
        omega_0 = np.array([1.0, 0.0, 0.0])
        for phi in [0.5, 1.0, 2.0, 3.7, 10.0]:
            E_phi = pure_l1_energy(phi, omega_0, d0)
            E_1 = pure_l1_energy(1.0, omega_0, d0)
            assert abs(E_phi - phi * E_1) < 1e-10

    def test_negative_phi_symmetry(self):
        d0 = coboundary_d0_c3()
        omega_0 = np.array([1.0, 0.0, 0.0])
        for phi in [1.0, 2.5, 7.3]:
            assert abs(pure_l1_energy(phi, omega_0, d0) - pure_l1_energy(-phi, omega_0, d0)) < 1e-10

    def test_r_squared_is_one(self):
        result = verify_linear_energy()
        assert result["r_squared"] > 1.0 - 1e-10

    def test_is_exactly_linear(self):
        result = verify_linear_energy()
        assert result["is_exactly_linear"]

    def test_declared_family_is_not_mexican_hat(self):
        result = verify_linear_energy()
        assert result["is_not_mexican_hat"]

    def test_rejects_unrelated_coboundary(self):
        omega_0 = np.array([1.0, 0.0, 0.0])
        with pytest.raises(ValueError, match="scoped to the directed C3"):
            pure_l1_energy(1.0, omega_0, np.eye(3))

    def test_zero_energy_at_origin(self):
        d0 = coboundary_d0_c3()
        omega_0 = np.array([1.0, 0.0, 0.0])
        assert abs(pure_l1_energy(0.0, omega_0, d0)) < 1e-15
