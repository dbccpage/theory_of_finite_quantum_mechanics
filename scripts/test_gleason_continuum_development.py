#!/usr/bin/env python3
"""Unit tests for `verify_gleason_continuum_development.py`."""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import verify_gleason_continuum_development as vgcd


class TestGleasonContinuumDevelopment(unittest.TestCase):
    def test_part_a_d3_density_and_rayleigh(self) -> None:
        res = vgcd.verify_part_a_d3_density_and_rayleigh()
        self.assertTrue(res["verified"])
        self.assertEqual(res["frob_norm_sq_pure"], "4")
        self.assertEqual(res["frob_norm_sq_mixed"], "8")
        self.assertEqual(res["trace_pure"], "1")
        self.assertEqual(res["trace_mixed"], "1")

    def test_part_b_all_finite_dimensions(self) -> None:
        res = vgcd.verify_part_b_all_finite_dimensions()
        self.assertTrue(res["verified"])
        self.assertTrue(res["d0_vacuously_unique"])
        self.assertTrue(res["d1_constant_one"])
        self.assertEqual(res["d2_forced_quadratic_value"], "4/5")
        self.assertEqual(res["d2_counterexample_value"], "1/2")
        self.assertEqual(res["d2_two_frame_forced_value"], "-1/5")
        self.assertTrue(res["d4_submatrix3D_overlap_verified"])
        self.assertTrue(res["d4_polarization_uniqueness_verified"])

    def test_part_c_continuum_regularity(self) -> None:
        res = vgcd.verify_part_c_continuum_regularity()
        self.assertTrue(res["verified"])
        self.assertEqual(res["pole_value_at_e0"], "1")
        self.assertEqual(res["orthogonal_value_at_e1"], "0")
        self.assertEqual(
            Fraction(res["piron_subadditivity_sum_uv"]) + Fraction(res["complement_ray_weight_w"]),
            Fraction(1, 1),
        )

    def test_part_d_infinite_dim_and_trace_escape(self) -> None:
        res = vgcd.verify_part_d_infinite_dim_and_trace_escape()
        self.assertTrue(res["verified"])
        self.assertEqual(res["tight_compression_N5"], "31/32")
        self.assertEqual(res["tight_compression_N10"], "1023/1024")
        self.assertEqual(res["escape_compression_for_k_ge_N"], "0")
        self.assertEqual(res["escape_full_stage_normalization"], "1")

    def test_zero_matrix_rejected(self) -> None:
        z = vgcd.GaussRat(0, 0)
        zero_mat = ((z, z, z), (z, z, z), (z, z, z))
        with self.assertRaises(ValueError):
            vgcd.factorized_state_matrix(zero_mat)

    def test_build_receipt(self) -> None:
        receipt = vgcd.build_receipt()
        self.assertEqual(receipt["schema_version"], "1.0.0")
        self.assertEqual(receipt["authority_effect"], "None")
        self.assertEqual(receipt["lean_module"]["path"], "lean4/GleasonContinuumDevelopment.lean")
        self.assertEqual(len(receipt["lean_module"]["sha256"]), 64)
        for part_data in receipt["parts"].values():
            self.assertTrue(part_data["verified"])


if __name__ == "__main__":
    unittest.main()
