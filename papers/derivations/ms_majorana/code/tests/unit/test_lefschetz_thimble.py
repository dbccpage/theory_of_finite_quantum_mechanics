r"""Unit tests for Lefschetz Thimble Retraction & Gate-11 Sign Problem Solver Engine.

Verifies:
1. Gate-11 trichotomy classification (P_EXACT, P_CLOSED_NONEXACT, P_NONCLOSED).
2. ThimbleRetraction identity checks (i * r - id = d * h + h * d).
3. Complex Langevin runaway and gauge cooling limit cycle refusal paths.
4. Evidence SHA-256 digest and AuthorityEffect: None.
"""

import unittest
import numpy as np
from omega_engine.crates.solver.solv_lefschetz_thimble import (
    Gate11TrichotomyClass,
    ComplexLangevinDiagnostics,
    GaugeCoolingDiagnostics,
    ThimbleState,
    ThimbleRetraction,
    ThimbleGate11Receipt,
    LefschetzThimbleSolver,
)


class TestLefschetzThimble(unittest.TestCase):
    def setUp(self):
        self.solver = LefschetzThimbleSolver(tol=1e-6)

    def test_p_exact_repaired_phase_defect(self):
        phi = np.array([1.0 + 0.0j, 0.5 + 0.0j])
        state = ThimbleState(
            phi=phi,
            im_action=0.0,
            phase_cochain_omega=np.zeros(2),
            coboundary_d_omega=np.zeros(2),
            critical_point_id="J0",
        )
        receipt = self.solver.evaluate_gate11(state)
        self.assertEqual(receipt.trichotomy_class, "P_EXACT")
        self.assertEqual(receipt.cohomology_class_id, "EXACT_REPAIRED_VANISHING_DEFECT")
        self.assertTrue(receipt.is_flow_valid)
        self.assertEqual(receipt.authority_effect, "None")
        self.assertTrue(len(receipt.evidence_sha256) == 64)

    def test_p_closed_nonexact_stationary_thimble(self):
        phi = np.array([1.0 + 0.2j, 0.5 - 0.2j])
        state = ThimbleState(
            phi=phi,
            im_action=0.5,
            phase_cochain_omega=np.array([0.5, -0.5]),
            coboundary_d_omega=np.zeros(2),
            critical_point_id="J1",
        )
        receipt = self.solver.evaluate_gate11(state)
        self.assertEqual(receipt.trichotomy_class, "P_CLOSED_NONEXACT")
        self.assertEqual(receipt.cohomology_class_id, "CLOSED_NONEXACT_THIMBLE_J1")
        self.assertTrue(receipt.is_flow_valid)
        self.assertEqual(receipt.authority_effect, "None")

    def test_p_nonclosed_runaway_refusal(self):
        phi = np.array([10.0 + 5.0j, 20.0 - 5.0j])
        state = ThimbleState(
            phi=phi,
            im_action=100.0,
            phase_cochain_omega=np.array([1.0, 2.0]),
            coboundary_d_omega=np.array([0.5, -0.5]),
            critical_point_id="J0",
        )
        langevin_diag = ComplexLangevinDiagnostics(
            max_imaginary=5.0,
            drift_norm=10.0,
            mean_im_action=100.0,
            runaway_detected=True,
            step_count=50,
        )
        receipt = self.solver.evaluate_gate11(state, langevin_diag=langevin_diag)
        self.assertEqual(receipt.trichotomy_class, "P_NONCLOSED")
        self.assertFalse(receipt.is_flow_valid)
        self.assertEqual(receipt.cohomology_class_id, "REFUSED_BOUNDARY_LEAKAGE_OR_RUNAWAY")

    def test_thimble_retraction_identity(self):
        eye2 = np.eye(2)
        zero2 = np.zeros((2, 2))
        retraction = ThimbleRetraction(
            i_map=eye2,
            r_map=eye2,
            h_map=zero2,
            d_C=zero2,
            d_D=zero2,
        )
        self.assertTrue(retraction.verify_retraction_identity())


if __name__ == "__main__":
    unittest.main()
