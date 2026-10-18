r"""Unit tests for Discrete Yang-Mills Mass Gap & Topological Obstruction Engine.

Verifies:
1. Holonomy conservation check (d * omega = 0).
2. Zero-mode condensation refusal when topological obstruction class is missing.
3. Strictly positive mass gap Delta > 0 when topological obstruction class is present.
4. Cryptographic SHA-256 evidence digest under AuthorityEffect: None.
"""

import unittest
import numpy as np
from omega_engine.crates.solver.solv_yang_mills import (
    ObstructionSource,
    YangMillsLatticeData,
    YangMillsMassGapReceipt,
    YangMillsMassGapSolver,
)


class TestYangMillsMassGap(unittest.TestCase):
    def setUp(self):
        self.solver = YangMillsMassGapSolver(c_lattice_const=1.0)

    def test_certified_mass_gap_p_exact(self):
        data = YangMillsLatticeData(
            n_vertices=10,
            n_2simplices=20,
            curvature_omega=np.zeros(20),
            boundary_d_omega=np.zeros(20),
            immirzi_gamma=0.274,
            instanton_number=1,
            topological_invariant_phi=1.0,
        )

        receipt = self.solver.evaluate_mass_gap(data)
        self.assertTrue(receipt.holonomy_conserved)
        self.assertEqual(receipt.trichotomy_class, "P_EXACT")
        self.assertFalse(receipt.zero_mode_condensation_risk)
        self.assertGreater(receipt.mass_gap_delta, 0.0)
        self.assertEqual(receipt.authority_effect, "None")
        self.assertTrue(len(receipt.evidence_sha256) == 64)

    def test_refused_missing_topological_obstruction(self):
        data = YangMillsLatticeData(
            n_vertices=10,
            n_2simplices=20,
            curvature_omega=np.zeros(20),
            boundary_d_omega=np.zeros(20),
            immirzi_gamma=0.274,
            instanton_number=0,
            topological_invariant_phi=0.0,
        )

        receipt = self.solver.evaluate_mass_gap(data)
        self.assertTrue(receipt.holonomy_conserved)
        self.assertEqual(receipt.trichotomy_class, "P_CLOSED_NONEXACT")
        self.assertTrue(receipt.zero_mode_condensation_risk)
        self.assertEqual(receipt.mass_gap_delta, 0.0)
        self.assertTrue(any("REFUSED" in item for item in receipt.nonclaim_ledger))


if __name__ == "__main__":
    unittest.main()
