"""Unit tests for the Meron-Cluster to Continuum Wilsonian Bridge."""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path
import sys
import unittest

CODE_DIR = str(Path(__file__).resolve().parents[1] / "code")
if CODE_DIR not in sys.path:
    sys.path.insert(0, CODE_DIR)

from meron_wilsonian_bridge import MeronWilsonianBridge


class TestMeronWilsonianBridge(unittest.TestCase):
    def test_canonical_traces_retrieval(self) -> None:
        bridge = MeronWilsonianBridge()
        self.assertEqual(bridge.get_or_compute_trace(4), 912)
        self.assertEqual(bridge.get_or_compute_trace(6), 33012)
        self.assertEqual(bridge.get_or_compute_trace(8), 973824)

    def test_log_density_interval(self) -> None:
        bridge = MeronWilsonianBridge()
        g4 = bridge.compute_log_density(4)
        self.assertTrue(Fraction(17039, 10000) <= g4.lo <= g4.hi <= Fraction(17040, 10000))
        self.assertTrue(g4.width < Fraction(1, 10**18))

    def test_thermodynamic_limit_extrapolation(self) -> None:
        bridge = MeronWilsonianBridge()
        meron_rec, scaling_rec = bridge.extrapolate_meron_continuum(chain_lengths=(4, 6, 8))
        self.assertEqual(meron_rec.authority_effect, "None")
        self.assertEqual(len(meron_rec.chain_lengths), 3)

        f_mid = float(meron_rec.thermodynamic_limit["float_midpoint"])
        self.assertAlmostEqual(f_mid, 1.69411, places=4)

        res = meron_rec.finite_size_residuals
        self.assertTrue(4 in res and 6 in res and 8 in res)


if __name__ == "__main__":
    unittest.main()
