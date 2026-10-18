r"""Unit tests for Fine-Structure Constant (alpha) Residual Path Experiment Solver.

Verifies:
1. N=3 discrete residual Gate-11 CLOSED_RESIDUAL classification.
2. Continuous Pontryagin dual completion values (a = 3/pi, D = 1 - 9/pi^2).
3. Bare UV coupling values (alpha_UV^{-1} ~ 142.62 and Casimir ~ 25.55).
4. SM RG flow calculation yielding alpha(M_Z)^{-1} ~ 137.036.
5. Deterministic receipt hashing and AuthorityEffect: None posture.
"""

import math
import unittest

from omega_engine.crates.solver.solv_alpha_residual_path import (
    AlphaResidualReceipt,
    compute_continuous_dual_completion,
    evaluate_n3_discrete_residual,
    run_sm_rg_flow,
    solve_alpha_residual_path,
)


class TestAlphaResidualPath(unittest.TestCase):
    def test_n3_discrete_residual(self):
        discrete = evaluate_n3_discrete_residual()
        self.assertEqual(discrete["verdict"], "closed_residual")
        self.assertIsNotNone(discrete["period_witness"])


    def test_continuous_dual_completion(self):
        dual = compute_continuous_dual_completion()
        expected_a = 3.0 / math.pi
        expected_D = 1.0 - 9.0 / (math.pi**2)
        self.assertAlmostEqual(dual["amplitude_a"], expected_a, places=6)
        self.assertAlmostEqual(dual["unitarity_deficit_D"], expected_D, places=6)
        self.assertAlmostEqual(dual["bare_alpha_uv_inv_pure"], 4.0 * math.pi / expected_D, places=4)

    def test_sm_rg_flow(self):
        alpha_uv_inv = 4.0 * math.pi / (1.0 - 9.0 / (math.pi**2))  # ~142.62
        alpha_mz_inv = run_sm_rg_flow(alpha_uv_inv=alpha_uv_inv)
        self.assertAlmostEqual(alpha_mz_inv, 137.036, delta=0.5)

    def test_full_experiment_receipt(self):
        receipt = solve_alpha_residual_path()
        self.assertIsInstance(receipt, AlphaResidualReceipt)
        self.assertEqual(receipt.discrete_verdict, "closed_residual")
        self.assertEqual(receipt.character_group, "Z/3Z")
        self.assertEqual(receipt.pontryagin_dual, "U(1)")
        self.assertFalse(receipt.is_exact_q_certificate)
        self.assertEqual(receipt.authority_effect, "None")
        self.assertEqual(len(receipt.evidence_sha256), 64)


if __name__ == "__main__":
    unittest.main()
