r"""Unit tests for Seiberg-Witten Resurgence & Instanton Trans-Series Unification Engine.

Verifies:
1. Exact rational duality-gap bounds over Fraction.
2. Heyting 3-valued logic (TRUE, UNKNOWN, FALSE) and refusal of UNKNOWN hole bindings.
3. Trans-series sector admission and Gate-11 classification.
4. Cryptographic evidence SHA-256 digest under AuthorityEffect: None.
"""

import unittest
from fractions import Fraction
from omega_engine.crates.solver.solv_seiberg_witten_resurgence import (
    OmegaTruthValue,
    StokesCoeffHole,
    UnificationContext,
    TransSeriesSector,
    ResurgenceGate11Receipt,
    SeibergWittenResurgenceSolver,
)


class TestSeibergWittenResurgence(unittest.TestCase):
    def setUp(self):
        self.solver = SeibergWittenResurgenceSolver()
        self.ctx = UnificationContext()

    def test_exact_certified_trans_series(self):
        hole0 = StokesCoeffHole(
            sector_k=1, order_n=0, hole_id="b_1_0", duality_predicate="electric_magnetic_duality"
        )
        sector1 = TransSeriesSector(
            sector_k=1,
            instanton_action_S=Fraction(1, 2),
            stokes_residual_omega=Fraction(0, 1),
            coboundary_d_omega=Fraction(0, 1),
            coeff_holes=[hole0],
        )
        duality_bindings = {
            "b_1_0": (Fraction(3, 4), Fraction(3, 4))
        }

        receipt = self.solver.solve_trans_series([sector1], duality_bindings, self.ctx)
        self.assertEqual(receipt.trichotomy_class, "P_EXACT")
        self.assertTrue(receipt.is_certified)
        self.assertEqual(receipt.admitted_sectors, [1])
        self.assertEqual(receipt.duality_gap_rational, Fraction(0, 1))
        self.assertEqual(receipt.authority_effect, "None")
        self.assertEqual(len(receipt.unbound_holes), 0)
        self.assertTrue(len(receipt.evidence_sha256) == 64)

    def test_refused_unknown_judgment(self):
        hole0 = StokesCoeffHole(
            sector_k=1, order_n=0, hole_id="b_1_0", duality_predicate="modular_duality"
        )
        sector1 = TransSeriesSector(
            sector_k=1,
            instanton_action_S=Fraction(1, 2),
            stokes_residual_omega=Fraction(0, 1),
            coboundary_d_omega=Fraction(0, 1),
            coeff_holes=[hole0],
        )
        duality_bindings = {
            "b_1_0": (Fraction(3, 4), Fraction(3, 4) + Fraction(1, 2000))
        }

        receipt = self.solver.solve_trans_series([sector1], duality_bindings, self.ctx)
        self.assertFalse(receipt.is_certified)
        self.assertEqual(receipt.unbound_holes, ["b_1_0"])
        self.assertTrue(any("REFUSED_BINDING" in entry for entry in receipt.nonclaim_ledger))

    def test_refused_nonclosed_stokes_residual(self):
        hole0 = StokesCoeffHole(
            sector_k=2, order_n=0, hole_id="b_2_0", duality_predicate="monodromy"
        )
        sector2 = TransSeriesSector(
            sector_k=2,
            instanton_action_S=Fraction(1, 1),
            stokes_residual_omega=Fraction(1, 10),
            coboundary_d_omega=Fraction(1, 100),
            coeff_holes=[hole0],
        )
        duality_bindings = {"b_2_0": (Fraction(1, 1), Fraction(1, 1))}

        receipt = self.solver.solve_trans_series([sector2], duality_bindings, self.ctx)
        self.assertEqual(receipt.trichotomy_class, "P_NONCLOSED")
        self.assertFalse(receipt.is_certified)
        self.assertEqual(len(receipt.admitted_sectors), 0)


if __name__ == "__main__":
    unittest.main()
