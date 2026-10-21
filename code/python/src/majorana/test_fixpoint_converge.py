r"""Unit tests for Presheaf Colimit Convergence & DDA Tape Fixed-Point Solver Engine.

Verifies:
1. Presheaf axiom restriction compatibility.
2. DDA-tape monotonicity & uncompensated I step detection.
3. Terminal T-absorption synchronization.
4. Colimit residual inequality and Gate-11 classification under AuthorityEffect: None.
"""

import unittest
import numpy as np
from omega_engine.crates.solver.solv_fixpoint_converge import (
    DdaTapeLetter,
    DdaStepRecord,
    AgentTapeHistory,
    PresheafColimitReceipt,
    PresheafColimitVerifier,
)


class TestPresheafFixpointConverge(unittest.TestCase):
    def setUp(self):
        self.verifier = PresheafColimitVerifier(tol=1e-6)

    def test_exact_converged_colimit(self):
        agent1 = AgentTapeHistory(
            agent_id="agent_1",
            steps=[
                DdaStepRecord(DdaTapeLetter.C, residual_phi1=1.0, foc_class="P_CLOSED_NONEXACT"),
                DdaStepRecord(DdaTapeLetter.E, residual_phi1=0.0, foc_class="P_EXACT"),
                DdaStepRecord(DdaTapeLetter.T, residual_phi1=0.0, foc_class="P_EXACT"),
            ],
        )
        agent2 = AgentTapeHistory(
            agent_id="agent_2",
            steps=[
                DdaStepRecord(DdaTapeLetter.R, residual_phi1=0.5, foc_class="P_CLOSED_NONEXACT"),
                DdaStepRecord(DdaTapeLetter.E, residual_phi1=0.0, foc_class="P_EXACT"),
                DdaStepRecord(DdaTapeLetter.T, residual_phi1=0.0, foc_class="P_EXACT"),
            ],
        )

        local_residuals = {
            "U": np.array([0.0, 0.0]),
            "V": np.array([0.0, 0.0]),
        }
        restriction_maps = {
            ("V", "U"): np.eye(2),
        }

        receipt = self.verifier.evaluate_colimit_convergence(
            histories=[agent1, agent2],
            local_residuals=local_residuals,
            restriction_maps=restriction_maps,
            gluing_residual_delta=0.0,
        )

        self.assertTrue(receipt.is_presheaf_axiom_valid)
        self.assertTrue(receipt.is_dda_monotonicity_valid)
        self.assertTrue(receipt.is_t_absorption_valid)
        self.assertTrue(receipt.is_colimit_inequality_valid)
        self.assertEqual(receipt.trichotomy_class, "P_EXACT")
        self.assertEqual(receipt.authority_effect, "None")
        self.assertTrue(len(receipt.evidence_sha256) == 64)

    def test_uncompensated_inclusion_refusal(self):
        agent1 = AgentTapeHistory(
            agent_id="agent_bad",
            steps=[
                DdaStepRecord(DdaTapeLetter.I, residual_phi1=2.0, foc_class="P_NONCLOSED"),
                DdaStepRecord(DdaTapeLetter.T, residual_phi1=2.0, foc_class="P_NONCLOSED"),
            ],
        )

        receipt = self.verifier.evaluate_colimit_convergence(
            histories=[agent1],
            local_residuals={"U": np.array([2.0])},
            restriction_maps={},
            gluing_residual_delta=0.0,
        )

        self.assertFalse(receipt.is_dda_monotonicity_valid)
        self.assertEqual(receipt.trichotomy_class, "P_NONCLOSED")
        self.assertTrue(any("REFUSED" in item for item in receipt.nonclaim_ledger))


if __name__ == "__main__":
    unittest.main()
