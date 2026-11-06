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

    def test_part_e_dim_d_subspace_lift(self) -> None:
        res = vgcd.verify_part_e_dim_d_subspace_lift()
        self.assertTrue(res["verified"])
        self.assertTrue(res["c4_isometric_embed3D_verified"])
        self.assertTrue(res["c5_isometric_embed3D_verified"])
        self.assertTrue(res["replaceBasis3D_orthonormal_verified"])
        self.assertTrue(res["replaceBasis3D_noncontiguous_slots_verified"])
        self.assertEqual(res["subspace_3frame_trace_preserved"], "3/4")
        self.assertTrue(res["subspaceMatrix3D_rayleigh_match_verified"])
        self.assertTrue(res["coordinate_embed3D_matches_submatrix3D"])
        self.assertTrue(res["pure_state_subspace3D_born_rule_verified"])
        self.assertEqual(res["pure_state_subspace3D_partial_weight"], "3/5")

    def test_non_orthonormal_basis_rejected(self) -> None:
        e0 = [vgcd.GaussRat(1, 0), vgcd.GaussRat(0, 0)]
        e1_bad = [vgcd.GaussRat(1, 0), vgcd.GaussRat(1, 0)]
        self.assertFalse(vgcd.is_orthonormal_basis_d([e0, e1_bad]))

        # Negative control: replacing 3 slots of standard basis of C^4 with duplicate slot index i0 == i1
        # (dropping u1) or with a non-orthogonal triple is rejected by is_orthonormal_basis_d
        std4 = [
            [vgcd.GaussRat(1, 0) if j == i else vgcd.GaussRat(0, 0) for j in range(4)]
            for i in range(4)
        ]
        self.assertTrue(vgcd.is_orthonormal_basis_d(std4))
        rot_u0 = [vgcd.GaussRat(Fraction(3, 5), 0), vgcd.GaussRat(Fraction(4, 5), 0), vgcd.GaussRat(0, 0), vgcd.GaussRat(0, 0)]
        rot_u1 = [vgcd.GaussRat(Fraction(4, 5), 0), vgcd.GaussRat(Fraction(-3, 5), 0), vgcd.GaussRat(0, 0), vgcd.GaussRat(0, 0)]
        bad_dup_slots = vgcd.replace_basis_3d(std4, 0, 0, 2, rot_u0, rot_u1, std4[2])
        self.assertFalse(vgcd.is_orthonormal_basis_d(bad_dup_slots))
        bad_non_orth = vgcd.replace_basis_3d(std4, 0, 1, 2, std4[0], rot_u0, std4[2])
        self.assertFalse(vgcd.is_orthonormal_basis_d(bad_non_orth))

    def test_zero_matrix_rejected(self) -> None:
        z = vgcd.GaussRat(0, 0)
        zero_mat = ((z, z, z), (z, z, z), (z, z, z))
        with self.assertRaises(ValueError):
            vgcd.factorized_state_matrix(zero_mat)

    def test_part_f_tfq_1059_extrema_and_deflation(self) -> None:
        res = vgcd.verify_part_f_tfq_1059_extrema_and_deflation()
        self.assertTrue(res["verified"])
        self.assertEqual(res["tfq1059_declarations_count"], 22)
        self.assertTrue(res["sphere3_sInf_sSup_sandwich_verified"])
        self.assertEqual(res["sphere3_sandwich_values"], "0 <= 1/6 <= 1/3 <= 1/2 <= 1")
        self.assertTrue(res["common_normal_equator_min_verified"])
        self.assertEqual(res["deflateIso_real_weight"], "2/5")
        self.assertEqual(res["deflateIsoC_complex_weight"], "2/5")
        self.assertTrue(res["axisymmetric_mixed_state_real_verified"])
        self.assertTrue(res["axisymmetric_mixed_state_complex_verified"])
        self.assertTrue(res["triaxial_hResidual_six_circles_zero_verified"])
        self.assertEqual(res["six_normals_tight_diff_r_minus_a"], "-4")

    def test_tfq_1059_edge_cases_and_negative_controls(self) -> None:
        # Edge case 1: std_quad_real rejects the zero vector
        with self.assertRaises(ValueError):
            vgcd.std_quad_real(
                Fraction(1, 2),
                Fraction(1, 3),
                Fraction(1, 6),
                (Fraction(0, 1), Fraction(0, 1), Fraction(0, 1)),
            )

        # Edge case 2: equator_min_witness_real rejects a vector collinear with e1 (s1 = s2 = 0)
        with self.assertRaises(ValueError):
            vgcd.equator_min_witness_real((Fraction(3, 1), Fraction(0, 1), Fraction(0, 1)))

        # Edge case 3: perp_min_witness_real rejects a vector collinear with the rotated pole p_rot_r
        p_rot_r = (Fraction(3, 5), Fraction(4, 5), Fraction(0, 1))
        q_rot_r = (Fraction(-4, 5), Fraction(3, 5), Fraction(0, 1))
        r_rot_r = (Fraction(0, 1), Fraction(0, 1), Fraction(1, 1))
        with self.assertRaises(ValueError):
            vgcd.perp_min_witness_real(
                p_rot_r,
                q_rot_r,
                r_rot_r,
                (Fraction(6, 5), Fraction(8, 5), Fraction(0, 1)),
            )

        # Edge case 4: isotropic deflation by c > m_min breaks nonnegativity at the minimizer ray
        f_tri = lambda v: vgcd.std_quad_real(Fraction(1, 2), Fraction(1, 3), Fraction(1, 6), v)
        f_over_deflated = vgcd.deflate_iso_real(f_tri, Fraction(1, 4))
        e1_r = (Fraction(1, 1), Fraction(0, 1), Fraction(0, 1))
        e2_r = (Fraction(0, 1), Fraction(1, 1), Fraction(0, 1))
        e3_r = (Fraction(0, 1), Fraction(0, 1), Fraction(1, 1))
        self.assertLess(f_over_deflated(e3_r), Fraction(0, 1))

        # Edge case 5: non-axisymmetric triaxial state (f(p) + 2*m = 5/6 != W = 1) violates the
        # axisymmetric formula at the intermediate axis e2_r (giving 1/6 instead of alpha = 1/3)
        m_min = Fraction(1, 6)
        axisym_rhs_at_e2 = m_min + (f_tri(e1_r) - m_min) * (
            (vgcd.dot3_real(e2_r, e1_r) ** 2) / vgcd.dot3_real(e2_r, e2_r)
        )
        self.assertEqual(axisym_rhs_at_e2, Fraction(1, 6))
        self.assertNotEqual(f_tri(e2_r), axisym_rhs_at_e2)

        # Edge case 6: isotropic boundary state M = alpha = m = 1/3 collapses sInf = W/3 = sSup
        # and vanishes identically under deflate_iso_real(..., 1/3)
        f_iso = lambda v: vgcd.std_quad_real(Fraction(1, 3), Fraction(1, 3), Fraction(1, 3), v)
        f_iso_deflated = vgcd.deflate_iso_real(f_iso, Fraction(1, 3))
        for vec in (e1_r, e2_r, e3_r, (Fraction(2, 1), Fraction(-3, 1), Fraction(5, 1))):
            self.assertEqual(f_iso(vec), Fraction(1, 3))
            self.assertEqual(f_iso_deflated(vec), Fraction(0, 1))

        # Edge case 7: check_lean_declarations_and_hygiene rejects commented-out declarations,
        # forbidden `sorry` tokens, and unclosed block comments
        with self.assertRaises(ValueError):
            vgcd.check_lean_declarations_and_hygiene(
                "-- theorem nonempty_image_sphere3 : True := trivial\n",
                ("nonempty_image_sphere3",),
            )
        with self.assertRaises(ValueError):
            vgcd.check_lean_declarations_and_hygiene(
                "theorem nonempty_image_sphere3 : True := by sorry\n",
                ("nonempty_image_sphere3",),
            )
        with self.assertRaises(ValueError):
            vgcd.strip_lean_comments("/- unclosed block comment")

    def test_build_receipt(self) -> None:
        receipt = vgcd.build_receipt()
        self.assertEqual(receipt["schema_version"], "1.0.0")
        self.assertEqual(receipt["authority_effect"], "None")
        self.assertEqual(receipt["lean_module"]["path"], "lean4/GleasonContinuumDevelopment.lean")
        self.assertEqual(len(receipt["lean_module"]["sha256"]), 64)
        self.assertIn("part_e_dim_d_subspace_lift", receipt["parts"])
        self.assertIn("part_f_tfq_1059_extrema_and_deflation", receipt["parts"])
        for part_data in receipt["parts"].values():
            self.assertTrue(part_data["verified"])


if __name__ == "__main__":
    unittest.main()

