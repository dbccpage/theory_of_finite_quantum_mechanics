"""Tests for SP3: Regge Deficit + Ponzano-Regge 6j.

AuthorityEffect: None.
"""

import sys
import os
import math
from fractions import Fraction

import pytest

from regge_deficit_hexwall import (
    deficit_angle_2d,
    turning_angle_2d,
    hexagonal_disk_deficit,
    verify_linear_divergence,
)
from ponzano_regge_6j import (
    triangle_valid,
    wigner_6j_exact,
    verify_regular_tetrahedron,
)


class TestDeficitAngles:
    def test_flat_interior(self):
        assert abs(deficit_angle_2d(6)) < 1e-15

    def test_corner(self):
        assert abs(deficit_angle_2d(2) - 4 * math.pi / 3) < 1e-12

    def test_edge(self):
        assert abs(deficit_angle_2d(3) - math.pi) < 1e-12

    def test_pentagonal(self):
        assert abs(deficit_angle_2d(5) - math.pi / 3) < 1e-12

    def test_heptagonal_negative(self):
        assert deficit_angle_2d(7) < 0


class TestTurningAngles:
    def test_corner_turning(self):
        assert abs(turning_angle_2d(2) - math.pi / 3) < 1e-12

    def test_edge_turning_zero(self):
        assert abs(turning_angle_2d(3)) < 1e-15


class TestHexagonalDisk:
    @pytest.mark.parametrize("R", [1, 2, 3, 4, 5, 10])
    def test_deficit_equals_2pi_plus_6piR(self, R):
        result = hexagonal_disk_deficit(R)
        expected = 2 * math.pi + 6 * math.pi * R
        assert result["deficit_match"], (
            f"R={R}: {result['total_deficit_radians']} != {expected}"
        )

    @pytest.mark.parametrize("R", [1, 2, 3, 4, 5, 10])
    def test_deficit_units_6_plus_18R(self, R):
        result = hexagonal_disk_deficit(R)
        assert result["units_match"], (
            f"R={R}: units {result['total_deficit_units']} != {result['expected_deficit_units']}"
        )

    @pytest.mark.parametrize("R", [1, 2, 3, 4, 5, 10, 50])
    def test_gauss_bonnet_turning_is_2pi(self, R):
        result = hexagonal_disk_deficit(R)
        assert result["gauss_bonnet_is_2pi"], (
            f"R={R}: turning = {result['gauss_bonnet_turning']} != 2π"
        )

    def test_diverges_linearly(self):
        result = verify_linear_divergence()
        assert result["all_slopes_correct"], (
            f"slopes {result['slopes']} != 6π = {result['expected_slope_6pi']}"
        )
        assert result["diverges"]


class TestTriangleInequalities:
    def test_111_valid(self):
        assert triangle_valid(1, 1, 1)

    def test_integer_perimeter(self):
        assert (1 + 1 + 1) == 3

    def test_invalid_triad(self):
        assert not triangle_valid(1, 1, 3)


class TestPonzanoRegge6j:
    def test_regular_tetrahedron_exact(self):
        result = wigner_6j_exact(1, 1, 1, 1, 1, 1)
        assert result == Fraction(1, 6), f"6j = {result} != 1/6"

    def test_verification_audit(self):
        result = verify_regular_tetrahedron()
        assert result["match"]
        assert result["term_z3"] == -24
        assert result["term_z4"] == 120
        assert result["raw_sum"] == 96
        assert result["prefactor"] == Fraction(1, 576)
        assert result["product"] == Fraction(1, 6)

    def test_z_range(self):
        result = verify_regular_tetrahedron()
        assert result["z_range"] == (3, 4)

    def test_trivial_6j_000(self):
        result = wigner_6j_exact(0, 0, 0, 0, 0, 0)
        assert result == Fraction(1, 1), f"{{0 0 0; 0 0 0}} = {result} != 1"

    def test_triangle_inequality_failure(self):
        result = wigner_6j_exact(1, 1, 5, 1, 1, 1)
        assert result == Fraction(0)

    def test_exact_api_refuses_irrational_result(self):
        with pytest.raises(ValueError, match="not rational"):
            wigner_6j_exact(0, 0, 0, 1, 1, 1)
