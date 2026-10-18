"""
test_density_builder.py
Unit and Property Test Suite for FORGE-S1 Density Matrix Builder.
AuthorityEffect: None.
"""

import unittest
from omega_engine.crates.operator.constructor.ctor_qm_density import (
    phi_binning,
    build_state_feature_matrix,
    build_density_matrix_from_matrix,
)


class TestDensityBuilder(unittest.TestCase):
    def test_phi_binning_norm(self):
        """Verify phi binning outputs complex unit phase vectors."""
        features = [0.1, 0.2, 0.3, 0.4]
        phi = phi_binning(features, num_bins=4)
        self.assertEqual(len(phi), 4)
        for z in phi:
            magnitude = abs(z)
            self.assertAlmostEqual(magnitude, 1.0, places=6)

    def test_state_feature_matrix_shape(self):
        """Verify state feature matrix F shape (M_bins x N_samples)."""
        samples = [[0.1, 0.5], [0.3, 0.8], [0.7, 0.2]]
        matrix_F = build_state_feature_matrix(samples, num_bins=4)
        self.assertEqual(len(matrix_F), 4)
        self.assertEqual(len(matrix_F[0]), 3)

    def test_density_matrix_trace_one(self):
        r"""Verify rho = F F^\dagger / Tr(F F^\dagger) has exact trace 1.0."""
        samples = [[0.1, 0.5], [0.3, 0.8], [0.7, 0.2]]
        matrix_F = build_state_feature_matrix(samples, num_bins=4)
        rho = build_density_matrix_from_matrix(matrix_F)

        self.assertAlmostEqual(rho.trace(), 1.0, places=6)

    def test_density_matrix_hermiticity(self):
        r"""Verify density matrix rho is Hermitian (rho == rho^\dagger)."""
        samples = [[0.1, 0.5], [0.3, 0.8], [0.7, 0.2]]
        matrix_F = build_state_feature_matrix(samples, num_bins=4)
        rho = build_density_matrix_from_matrix(matrix_F)

        arr = rho.rho()
        n = rho.dim()
        for i in range(n):
            for j in range(n):
                val_ij = arr[i, j]
                val_ji = arr[j, i]
                self.assertAlmostEqual(val_ij.real, val_ji.real, places=6)
                self.assertAlmostEqual(val_ij.imag, -val_ji.imag, places=6)


if __name__ == "__main__":
    unittest.main()


