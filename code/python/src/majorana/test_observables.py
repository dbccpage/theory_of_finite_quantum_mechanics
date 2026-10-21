"""
test_observables.py
Unit Test Suite for FORGE-S2 Density Matrix Observables API & Receipt Emitter.
AuthorityEffect: None.
"""

import unittest
from omega_engine.crates.operator.constructor.ctor_qm_density import (
    build_state_feature_matrix,
    build_density_matrix_from_matrix,
)
from omega_engine.crates.observable.obsv_qm_density import (
    compute_purity,
    compute_von_neumann_entropy,
    compute_l1_coherence,
    emit_observables_receipt,
)


class TestObservables(unittest.TestCase):
    def setUp(self):
        samples = [[0.1, 0.5], [0.3, 0.8], [0.7, 0.2]]
        matrix_F = build_state_feature_matrix(samples, num_bins=4)
        self.rho = build_density_matrix_from_matrix(matrix_F)

    def test_purity_range(self):
        r"""Verify purity gamma in [1/N, 1.0]."""
        purity = compute_purity(self.rho)
        dim = self.rho.dim()
        self.assertGreaterEqual(purity, 1.0 / dim - 1e-6)
        self.assertLessEqual(purity, 1.0 + 1e-6)

    def test_entropy_non_negative(self):
        r"""Verify von Neumann entropy S(rho) >= 0.0."""
        entropy = compute_von_neumann_entropy(self.rho)
        self.assertGreaterEqual(entropy, 0.0)

    def test_l1_coherence_non_negative(self):
        r"""Verify L1 coherence C_L1 >= 0.0."""
        l1_coh = compute_l1_coherence(self.rho)
        self.assertGreaterEqual(l1_coh, 0.0)

    def test_observables_receipt_schema(self):
        """Verify JSON receipt schema fields."""
        receipt = emit_observables_receipt(self.rho)
        self.assertEqual(receipt["dimension"], 4)
        self.assertAlmostEqual(receipt["trace"], 1.0, places=6)
        self.assertIn("purity", receipt)
        self.assertIn("von_neumann_entropy", receipt)
        self.assertIn("l1_coherence", receipt)
        self.assertEqual(receipt["authority_effect"], "None")


if __name__ == "__main__":
    unittest.main()


