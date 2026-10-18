"""Unit tests for Step 3: Wilsonian Finite-Size Scaling Extrapolator."""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path
import sys
import unittest

CODE_DIR = str(Path(__file__).resolve().parents[1] / "code")
if CODE_DIR not in sys.path:
    sys.path.insert(0, CODE_DIR)

from interval_calculus import RationalInterval
from wilsonian_extrapolator import WilsonianExtrapolator


class TestWilsonianExtrapolator(unittest.TestCase):
    def test_insufficient_lengths_rejection(self) -> None:
        ext = WilsonianExtrapolator()
        ext.add_observation(4, Fraction(1))
        with self.assertRaises(ValueError):
            ext.extrapolate()

    def test_exact_polynomial_scaling_l4_6_8_12(self) -> None:
        """Test exact rational recovery of f_infty from L=4, 6, 8, 12 chains."""
        f_infty = Fraction(5, 11)
        c1 = Fraction(3, 2)
        c2 = Fraction(-7, 4)

        ext = WilsonianExtrapolator(scaling_variable_power=2)
        chain_lengths = [4, 6, 8, 12]
        for l in chain_lengths:
            g_l = f_infty + c1 / (l ** 2) + c2 / (l ** 4)
            ext.add_observation(l, g_l)

        receipt = ext.extrapolate()
        self.assertEqual(receipt.extrapolated_thermodynamic_limit.lo, f_infty)
        self.assertEqual(receipt.extrapolated_thermodynamic_limit.hi, f_infty)
        self.assertEqual(receipt.extrapolated_thermodynamic_limit.width, Fraction(0))
        self.assertEqual(len(receipt.input_chain_lengths), 4)
        self.assertEqual(receipt.scaling_variable_power, 2)

    def test_interval_uncertainty_propagation(self) -> None:
        """Uncertainty intervals on finite chains must propagate to a bounding interval on f_infty."""
        f_infty = Fraction(1, 2)
        ext = WilsonianExtrapolator(scaling_variable_power=2)
        chain_lengths = [4, 6, 8, 12]
        r = Fraction(1, 1000)
        for l in chain_lengths:
            g_l = f_infty + Fraction(1) / (l ** 2)
            ext.add_observation(l, g_l, radius=r)

        receipt = ext.extrapolate()
        self.assertTrue(receipt.extrapolated_thermodynamic_limit.contains(f_infty))
        self.assertTrue(receipt.extrapolated_thermodynamic_limit.width > 0)

    def test_extensive_partition_sum_scaling(self) -> None:
        """Test scaling when observations are extensive values Z(L) = L * f_infty + Delta(L)."""
        f_infty = Fraction(2, 3)
        ext = WilsonianExtrapolator(scaling_variable_power=2)
        chain_lengths = [4, 6, 8, 12]
        for l in chain_lengths:
            total_e0 = l * f_infty + Fraction(3) / l
            ext.add_observation(l, total_e0, is_density=False)

        receipt = ext.extrapolate()
        self.assertEqual(receipt.extrapolated_thermodynamic_limit.lo, f_infty)
        self.assertEqual(receipt.extrapolated_thermodynamic_limit.hi, f_infty)


if __name__ == "__main__":
    unittest.main()
