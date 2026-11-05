#!/usr/bin/env python3
"""Unit tests for `verify_continuum_derivation_spine.py`."""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import verify_continuum_derivation_spine as vcds


class TestContinuumDerivationSpine(unittest.TestCase):
    def test_stage_1_scalar_field(self) -> None:
        res = vcds.verify_stage_1_scalar_field()
        self.assertTrue(res["verified"])
        self.assertEqual(res["pairs_checked"], 2)

    def test_stage_2_inner_product_and_parallelogram(self) -> None:
        res = vcds.verify_stage_2_inner_product_and_parallelogram()
        self.assertTrue(res["verified"])
        self.assertEqual(res["parallelogram_lhs_rhs"], "54")

    def test_stage_3_state_effect_duality(self) -> None:
        res = vcds.verify_stage_3_state_effect_duality()
        self.assertTrue(res["verified"])
        self.assertEqual(res["frame_sum"], "1")
        for p_str in res["frame_probabilities"]:
            p = Fraction(p_str)
            self.assertGreaterEqual(p, Fraction(0, 1))
            self.assertLessEqual(p, Fraction(1, 1))

    def test_stage_4_composite_local_tomography(self) -> None:
        res = vcds.verify_stage_4_composite_local_tomography()
        self.assertTrue(res["verified"])
        self.assertEqual(res["two_qubit_complex_dim"], 16)
        self.assertEqual(res["two_rebit_symmetric_composite_dim"], 10)
        self.assertEqual(res["two_rebit_symmetric_product_dim"], 9)
        self.assertEqual(res["two_rebit_deficit"], 1)

    def test_stage_5_wigner_stone_dynamics(self) -> None:
        res = vcds.verify_stage_5_wigner_stone_dynamics()
        self.assertTrue(res["verified"])
        self.assertEqual(res["skew_hermitian_re_quad"], "0")

    def test_stage_6_kraus_and_luders(self) -> None:
        res = vcds.verify_stage_6_kraus_and_luders()
        self.assertTrue(res["verified"])
        self.assertEqual(res["kraus_branch_norm_sum"], res["input_norm_sq"])

    def test_stage_7_directed_continuum_limit(self) -> None:
        res = vcds.verify_stage_7_directed_continuum_limit()
        self.assertTrue(res["verified"])
        self.assertLessEqual(
            Fraction(res["abs_tail_expectation"]),
            Fraction(res["tightness_bound_C_eps"]),
        )

    def test_stage_8_discrete_lattice_hamiltonian(self) -> None:
        res = vcds.verify_stage_8_discrete_lattice_hamiltonian()
        self.assertTrue(res["verified"])
        self.assertEqual(res["quadratic_laplacian_exact"], "10/3")

    def test_build_receipt(self) -> None:
        receipt = vcds.build_receipt()
        self.assertEqual(receipt["schema_version"], "1.0.0")
        self.assertEqual(receipt["authority_effect"], "None")
        self.assertEqual(receipt["lean_module"]["path"], "lean4/ContinuumDerivationSpine.lean")
        self.assertEqual(len(receipt["lean_module"]["sha256"]), 64)
        self.assertEqual(len(receipt["stages"]), 8)
        for stage_data in receipt["stages"].values():
            self.assertTrue(stage_data["verified"])


if __name__ == "__main__":
    unittest.main()
