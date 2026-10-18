r"""Unit tests for CascadeSolver HPL Deformation Transfer and Finite Hilbert Obstruction Layer.

Verifies:
1. NormalizedContraction side conditions (hi=0, rh=0, h^2=0).
2. Homological Perturbation Lemma (HPL) transfer delta_D = r (1 + delta h)^-1 delta i.
3. Neumann series uninvertible perturbation loss ledger handling.
4. Gate-11 projector preservation (P_exact, P_closed_nonexact, P_nonclosed).
5. Subspace truncation leakage check L_P = P A^\dagger (1 - P) A P.
6. Refusal of Born-uniqueness or continuum claims via OracleNeeded path.
7. AuthorityEffect: None on all emitted receipts.
"""

import sys
import unittest
from pathlib import Path

import numpy as np

coda_dir = Path(__file__).resolve().parents[1] / "coda"
if str(coda_dir) not in sys.path:
    sys.path.insert(0, str(coda_dir))

from omega_engine.crates.residuals.network_residual import Network
from omega_engine.crates.solver.solv_omega_engine_solver_of_solvers.solv_oesos import (
    CascadeSolver,
    NormalizedContraction,
)


class TestHPLHilbertCascade(unittest.TestCase):
    def setUp(self):
        self.net = Network(nodes=[0, 1, 2], edges=[(0, 1), (1, 2), (2, 0)])
        self.solver = CascadeSolver(self.net)

    def test_normalized_contraction_side_conditions(self):
        """Verify verification of normalized contraction side conditions (hi=0, rh=0, h^2=0)."""
        dim_C = 3
        dim_D = 1
        i_map = np.array([[1.0], [0.0], [0.0]])
        r_map = np.array([[1.0, 0.0, 0.0]])
        d_C = np.array([[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 1.0, 0.0]])
        h_map = np.array([[0.0, 0.0, 0.0], [0.0, 0.0, 1.0], [0.0, 0.0, 0.0]])
        d_D = np.array([[0.0]])

        contraction = NormalizedContraction(
            i_map=i_map, r_map=r_map, h_map=h_map, d_C=d_C, d_D=d_D
        )
        self.assertTrue(contraction.verify_side_conditions())
        self.assertEqual(self.solver.observer_name, "CascadeSolver")

    def test_hpl_deformation_transfer_invertible(self):
        """Verify HPL transfer delta_D = r (1 + delta h)^-1 delta i under AuthorityEffect: None."""
        dim_C = 3
        dim_D = 1
        i_map = np.array([[1.0], [0.0], [0.0]])
        r_map = np.array([[1.0, 0.0, 0.0]])
        d_C = np.array([[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 1.0, 0.0]])
        h_map = np.array([[0.0, 0.0, 0.0], [0.0, 0.0, 1.0], [0.0, 0.0, 0.0]])
        d_D = np.array([[0.0]])

        contraction = NormalizedContraction(
            i_map=i_map, r_map=r_map, h_map=h_map, d_C=d_C, d_D=d_D
        )

        # Small perturbation delta
        delta = np.array([[0.1, 0.2, 0.0], [0.3, 0.4, 0.1], [0.0, 0.1, 0.2]])

        delta_D, receipt = self.solver.stage_hpl_deformation(contraction, delta)

        self.assertIsNotNone(delta_D)
        self.assertEqual(delta_D.shape, (1, 1))
        self.assertTrue(receipt.contraction_side_conditions_valid)
        self.assertEqual(receipt.invertibility_status, "INVERTIBLE")
        self.assertEqual(receipt.authority_effect, "None")
        self.assertGreater(receipt.transferred_differential_norm, 0.0)

    def test_hpl_deformation_transfer_uninvertible(self):
        """Verify uninvertible perturbation handling emits loss ledger and AuthorityEffect: None."""
        dim_C = 3
        dim_D = 1
        i_map = np.array([[1.0], [0.0], [0.0]])
        r_map = np.array([[1.0, 0.0, 0.0]])
        d_C = np.array([[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 1.0, 0.0]])
        h_map = np.array([[0.0, 0.0, 0.0], [0.0, 0.0, 2.0], [0.0, 0.0, 0.0]])
        d_D = np.array([[0.0]])

        contraction = NormalizedContraction(
            i_map=i_map, r_map=r_map, h_map=h_map, d_C=d_C, d_D=d_D
        )

        # Large perturbation forcing spectral radius >= 1.0
        delta = np.array([[1.0, 1.0, 1.0], [1.0, 1.0, 1.0], [1.0, 1.0, 1.0]])

        delta_D, receipt = self.solver.stage_hpl_deformation(contraction, delta)

        self.assertIsNone(delta_D)
        self.assertEqual(receipt.invertibility_status, "UNINVERTIBLE_PERTURBATION")
        self.assertEqual(receipt.authority_effect, "None")
        self.assertIn("spectral_radius", receipt.loss_ledger)

    def test_finite_hilbert_gate11_projectors_and_leakage(self):
        """Verify Hilbert residual lift decomposes state into Gate-11 projectors and computes L_P leakage."""
        dim = 3
        # Nilpotent Q (Q^2 = 0)
        Q = np.array([[0.0, 1.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]])

        # Constraint operator A
        constraint_A = np.array([[0.5, 0.0, 0.0], [0.0, 0.2, 0.0], [0.0, 0.0, 0.8]])

        state_psi = np.array([1.0, 1.0, 1.0])

        lift_res, receipt = self.solver.stage_hilbert_residual_lift(
            Q, constraint_A, state_psi
        )

        self.assertEqual(receipt.hilbert_dim, dim)
        self.assertEqual(receipt.authority_effect, "None")
        self.assertGreaterEqual(receipt.truncation_leakage_L_P, 0.0)
        self.assertEqual(receipt.oracle_needed_status, "SATISFIED")
        self.assertFalse(lift_res["is_refused"])
        self.assertIn("L_P_operator", lift_res)

    def test_born_uniqueness_oracle_needed_refusal(self):
        """Verify explicit REFUSED_ORACLE_NEEDED when Born uniqueness is claimed without import witness."""
        dim = 2
        Q = np.zeros((dim, dim))
        constraint_A = np.eye(dim)
        state_psi = np.array([1.0, 0.0])

        oracle_packet = {
            "claims_born_uniqueness": True,
            "claims_continuum_limit": False,
            "import_witness_certified": False,  # Missing witness!
        }

        lift_res, receipt = self.solver.stage_hilbert_residual_lift(
            Q, constraint_A, state_psi, oracle_packet=oracle_packet
        )

        self.assertTrue(lift_res["is_refused"])
        self.assertEqual(receipt.oracle_needed_status, "REFUSED_ORACLE_NEEDED")
        self.assertEqual(receipt.authority_effect, "None")


if __name__ == "__main__":
    unittest.main()
