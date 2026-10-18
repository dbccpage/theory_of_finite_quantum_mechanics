from __future__ import annotations
"""FORGE-S1/S2 density_builder + observables tests (parity-facing).

AuthorityEffect: None.
"""


import unittest

from omega_engine.crates.operator.constructor.ctor_qm_density import (
    build_density_matrix_from_matrix,
    build_state_feature_matrix,
    phi_binning,
)
from omega_engine.crates.observable.obsv_qm_density import emit_observables_receipt


class TestPhiBinning(unittest.TestCase):
    def test_unit_modulus_known_phases(self):
        phi = phi_binning([0.0, 0.25, 0.5, 0.75], num_bins=4)
        self.assertEqual(len(phi), 4)
        for z in phi:
            self.assertAlmostEqual(abs(z), 1.0, places=12)
        self.assertAlmostEqual(phi[0].real, 1.0, places=12)
        self.assertAlmostEqual(phi[1].imag, 1.0, places=12)
        self.assertAlmostEqual(phi[2].real, -1.0, places=12)
        self.assertAlmostEqual(phi[3].imag, -1.0, places=12)

    def test_empty_pads_to_num_bins(self):
        phi = phi_binning([], num_bins=8)
        self.assertEqual(len(phi), 8)
        self.assertTrue(all(z == 1 + 0j for z in phi))

    def test_negative_feature_euclidean(self):
        phi = phi_binning([-0.25], num_bins=1)
        self.assertAlmostEqual(phi[0].real, 0.0, places=12)
        self.assertAlmostEqual(phi[0].imag, -1.0, places=12)


class TestDensityMatrix(unittest.TestCase):
    def test_trace_one_and_receipt(self):
        samples = [
            [0.12, 0.45, 0.88, 0.34],
            [0.25, 0.60, 0.70, 0.15],
            [0.80, 0.10, 0.40, 0.95],
        ]
        f = build_state_feature_matrix(samples, num_bins=4)
        self.assertEqual(len(f), 4)
        self.assertEqual(len(f[0]), 3)
        rho = build_density_matrix_from_matrix(f)
        self.assertEqual(rho.dim(), 4)
        self.assertAlmostEqual(rho.trace(), 1.0, places=10)
        receipt = emit_observables_receipt(rho)
        self.assertEqual(receipt["authority_effect"], "None")
        self.assertEqual(receipt["dimension"], 4)
        self.assertAlmostEqual(receipt["trace"], 1.0, places=8)
        self.assertGreaterEqual(receipt["purity"], 0.25 - 1e-8)
        self.assertLessEqual(receipt["purity"], 1.0 + 1e-8)
        self.assertGreaterEqual(receipt["von_neumann_entropy"], -1e-8)
        self.assertGreaterEqual(receipt["l1_coherence"], -1e-12)

    def test_single_sample_near_pure(self):
        f = build_state_feature_matrix([[0.0, 0.25, 0.5, 0.75]], num_bins=4)
        rho = build_density_matrix_from_matrix(f)
        self.assertAlmostEqual(rho.purity(), 1.0, places=8)


if __name__ == "__main__":
    unittest.main()


