# -*- coding: utf-8 -*-
"""Unit tests for Step 2: CS-Q Discretization Defect Operators."""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path
import sys
import unittest

CODE_DIR = str(Path(__file__).resolve().parents[1] / "code")
if CODE_DIR not in sys.path:
    sys.path.insert(0, CODE_DIR)

from discretization_defect import (
    DiscretizationDefectCarrier,
    Discrete1DHamiltonianSolver,
    DiscreteTrapezoidalQuadratureSolver,
    verify_mesh_refinement,
)
from interval_calculus import RationalInterval


class TestDiscretizationDefect(unittest.TestCase):
    def test_carrier_validation(self) -> None:
        val = RationalInterval(Fraction(1), Fraction(1))
        # Parameter a <= 0 fails
        with self.assertRaises(ValueError):
            DiscretizationDefectCarrier("bad_a", Fraction(0), val, 2, Fraction(1))
        # Order p < 1 fails
        with self.assertRaises(ValueError):
            DiscretizationDefectCarrier("bad_p", Fraction(1, 2), val, 0, Fraction(1))
        # Prefactor C < 0 fails
        with self.assertRaises(ValueError):
            DiscretizationDefectCarrier("bad_c", Fraction(1, 2), val, 2, Fraction(-1))

    def test_defect_bound_and_enclosure(self) -> None:
        # a = 1/4, p = 2, C = 2/3 ==> bound = (2/3) * (1/16) = 1/24
        val = RationalInterval(Fraction(1), Fraction(1))
        carrier = DiscretizationDefectCarrier("c1", Fraction(1, 4), val, 2, Fraction(2, 3))
        self.assertEqual(carrier.defect_bound, Fraction(1, 24))
        self.assertEqual(carrier.continuum_enclosure.lo, Fraction(23, 24))
        self.assertEqual(carrier.continuum_enclosure.hi, Fraction(25, 24))
        self.assertTrue(carrier.encloses(Fraction(1)))

    def test_trapezoidal_mesh_refinement(self) -> None:
        # Integrate f(x) = x^2 on [0, 1] -> true value = 1/3
        # f''(x) = 2, so M_2 = 2, prefactor C = 2/12 = 1/6
        solver = DiscreteTrapezoidalQuadratureSolver(lambda x: x * x, m2_bound=Fraction(2))
        coarse = solver.solve(4)
        fine = solver.solve(8)

        receipt = verify_mesh_refinement(coarse, fine)
        self.assertTrue(receipt.is_contractive)
        self.assertTrue(receipt.is_overlapping)
        self.assertTrue(receipt.refined_enclosure.contains(Fraction(1, 3)))
        self.assertTrue(receipt.fine_defect < receipt.coarse_defect)

    def test_mesh_refinement_inconsistency_rejection(self) -> None:
        # If coarse and fine have disjoint enclosures, verify_mesh_refinement must raise ValueError
        c_coarse = DiscretizationDefectCarrier(
            "c_disjoint", Fraction(1, 2), RationalInterval(Fraction(10)), 2, Fraction(1, 100)
        )
        c_fine = DiscretizationDefectCarrier(
            "f_disjoint", Fraction(1, 4), RationalInterval(Fraction(0)), 2, Fraction(1, 100)
        )
        with self.assertRaises(ValueError):
            verify_mesh_refinement(c_coarse, c_fine)

    def test_harmonic_lattice_solver(self) -> None:
        # Harmonic oscillator omega = 1, continuous E_0 = 1/2
        solver = Discrete1DHamiltonianSolver(omega=Fraction(1))
        c1 = solver.ground_state_energy_discrete(lattice_sites=16)
        c2 = solver.ground_state_energy_discrete(lattice_sites=32)

        self.assertTrue(c1.continuum_enclosure.contains(Fraction(1, 2)))
        self.assertTrue(c2.continuum_enclosure.contains(Fraction(1, 2)))
        self.assertTrue(c2.defect_bound < c1.defect_bound)


if __name__ == "__main__":
    unittest.main()
