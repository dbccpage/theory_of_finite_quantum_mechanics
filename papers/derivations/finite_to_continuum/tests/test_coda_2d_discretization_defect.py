# -*- coding: utf-8 -*-
"""Unit tests for 2D CS-Q Discretization Defect Operators and 2D Cubature."""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path
import sys
import unittest

CODE_DIR = str(Path(__file__).resolve().parents[1] / "code")
if CODE_DIR not in sys.path:
    sys.path.insert(0, CODE_DIR)

from coda_2d_discretization_defect import (
    DiscretizationDefect2DCarrier,
    Discrete2DCubatureSolver,
    verify_2d_mesh_refinement,
)
from interval_calculus import RationalInterval


class TestCoda2DDiscretizationDefect(unittest.TestCase):
    def test_carrier_validation_2d(self) -> None:
        val = RationalInterval(Fraction(1), Fraction(1))
        # Negative grid spacing fails
        with self.assertRaises(ValueError):
            DiscretizationDefect2DCarrier("bad_ax", Fraction(-1), Fraction(1), val, 2, 2, Fraction(1), Fraction(1))
        # Zero order fails
        with self.assertRaises(ValueError):
            DiscretizationDefect2DCarrier("bad_px", Fraction(1), Fraction(1), val, 0, 2, Fraction(1), Fraction(1))
        # Negative prefactor fails
        with self.assertRaises(ValueError):
            DiscretizationDefect2DCarrier("bad_cx", Fraction(1), Fraction(1), val, 2, 2, Fraction(-1), Fraction(1))

    def test_2d_cubature_mesh_refinement(self) -> None:
        # Integrate f(x, y) = x^2 * y^2 on [0, 1]^2
        # Exact continuous integral = (1/3) * (1/3) = 1/9
        # d^2 f / dx^2 = 2 y^2 <= 2, so M_xx = 2, prefactor Cx = 2/12 = 1/6
        # d^2 f / dy^2 = 2 x^2 <= 2, so M_yy = 2, prefactor Cy = 2/12 = 1/6
        solver = Discrete2DCubatureSolver(
            lambda x, y: (x * x) * (y * y),
            m_xx_bound=Fraction(2),
            m_yy_bound=Fraction(2),
        )
        coarse = solver.solve(4, 4)
        fine = solver.solve(8, 8)

        receipt = verify_2d_mesh_refinement(coarse, fine)
        self.assertTrue(receipt.is_contractive)
        self.assertTrue(receipt.is_overlapping)
        self.assertTrue(receipt.fine_defect < receipt.coarse_defect)
        # Check enclosure of true 1/9
        self.assertTrue(receipt.refined_enclosure.contains(Fraction(1, 9)))

    def test_2d_mesh_refinement_inconsistency_rejection(self) -> None:
        c1 = DiscretizationDefect2DCarrier(
            "coarse_disjoint", Fraction(1, 2), Fraction(1, 2), RationalInterval(Fraction(10)), 2, 2, Fraction(1, 100), Fraction(1, 100)
        )
        c2 = DiscretizationDefect2DCarrier(
            "fine_disjoint", Fraction(1, 4), Fraction(1, 4), RationalInterval(Fraction(0)), 2, 2, Fraction(1, 100), Fraction(1, 100)
        )
        with self.assertRaises(ValueError):
            verify_2d_mesh_refinement(c1, c2)


if __name__ == "__main__":
    unittest.main()
