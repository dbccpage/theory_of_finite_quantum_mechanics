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

    def test_tfq_0307_operational_noncontextuality_bridge(self) -> None:
        res = vcds.verify_tfq_0307_operational_noncontextuality_bridge()
        self.assertTrue(res["verified"])
        ks = res["ks_no_colouring_certificate"]
        self.assertEqual(ks["box_rays_count"], 49)
        self.assertEqual(ks["pair_completion_frames_count"], 82)
        self.assertEqual(ks["internal_triple_frames_count"], 26)
        self.assertEqual(ks["total_frame_declarations"], 108)
        self.assertEqual(ks["distinct_ordered_frames"], 103)
        self.assertEqual(ks["distinct_canonical_w_ordered_frames"], 96)
        self.assertEqual(ks["distinct_sign_normalized_unordered_frames"], 86)
        self.assertEqual(ks["active_unsat_core"]["active_total_frame_declarations"], 62)
        self.assertEqual(ks["active_unsat_core"]["branches_verified"], 6)
        self.assertEqual(ks["active_unsat_core"]["zero_one_valuations_count"], 0)
        self.assertEqual(ks["full_ks_scenario"]["zero_one_valuations_count"], 0)
        self.assertTrue(ks["full_ks_scenario"]["admits_exotic_qi3_nonneg_valuation"])
        self.assertFalse(ks["full_ks_scenario"]["latitude_symmetry_assumed"])

        tfq = res["tfq_0307_four_tier_classification"]
        self.assertEqual(
            tfq["tier1_zero_one_kochen_specker"]["nine_anchor_single_frame_zero_one_valuations"],
            192,
        )
        self.assertEqual(
            tfq["tier1_zero_one_kochen_specker"]["fifteen_anchor_bisector_zero_one_valuations"],
            48,
        )
        self.assertEqual(
            tfq["tier1_zero_one_kochen_specker"]["ks_full_scenario_zero_one_valuations"],
            0,
        )
        self.assertTrue(
            tfq["tier2_rational_nonquadratic_frame_functions"]["ks_scenario_inhabited_by_exotic_qi3"]
        )
        self.assertEqual(
            tfq["tier2_rational_nonquadratic_frame_functions"]["exotic_qi3_witness_111"],
            "2/3",
        )
        self.assertTrue(
            tfq["tier3_operator_effect_valuation_algebraic_born"]["excludes_exotic_qi3_without_topology"]
        )
        self.assertEqual(
            tfq["tier3_operator_effect_valuation_algebraic_born"]["algebraic_residual_discrepancy_at_witness_111"],
            "1/3",
        )
        self.assertTrue(
            tfq["tier4_topological_and_continuum_gleason_closure"]["bounded_anchor_amplification_closes_born_uniquely"]
        )

    def test_build_receipt(self) -> None:
        receipt = vcds.build_receipt()
        self.assertEqual(receipt["schema_version"], "1.0.0")
        self.assertEqual(receipt["authority_effect"], "None")
        self.assertEqual(receipt["lean_module"]["path"], "lean4/ContinuumDerivationSpine.lean")
        self.assertEqual(len(receipt["lean_module"]["sha256"]), 64)
        self.assertEqual(len(receipt["stages"]), 8)
        for stage_data in receipt["stages"].values():
            self.assertTrue(stage_data["verified"])
        self.assertIn("tfq_0307_operational_noncontextuality_bridge", receipt)
        self.assertTrue(receipt["tfq_0307_operational_noncontextuality_bridge"]["verified"])
        self.assertIn("five_node_gleason_and_born_spine_synthesis", receipt)
        self.assertTrue(receipt["five_node_gleason_and_born_spine_synthesis"]["verified"])

    def test_five_node_gleason_and_born_spine_synthesis(self) -> None:
        res = vcds.verify_five_node_gleason_and_born_spine_synthesis()
        self.assertTrue(res["verified"])
        self.assertEqual(
            res["stage_10_lean_declarations"],
            [
                "tfq1057_collar_chain_and_drift_synthesis",
                "tfq1059_real_and_complex_sphere_spectral_synthesis",
                "five_node_gleason_and_born_spine_synthesis",
            ],
        )
        sec10 = res["tfq_1057_collar_step_scaling_and_drift"]
        self.assertTrue(sec10["uniform_step_bound_k0_excluded_as_delta_to_zero"])
        self.assertEqual(sec10["witness_111_min_ray_sin_sq_t9"], "1/3")
        self.assertEqual(sec10["witness_111_min_ray_sin_sq_t15"], "1/3")
        self.assertEqual(sec10["witness_123_min_ray_sin_sq_t15"], "3/28")
        self.assertTrue(sec10["sublinear_drift_forces_zero_verified"])
        self.assertTrue(sec10["inv_k_step_error_preserves_constant_gap_verified"])

        part_f = res["tfq_1059_sphere3_and_sphereC_spectral_synthesis"]
        self.assertEqual(part_f["tfq1059_declarations_count"], 36)
        self.assertTrue(part_f["sphere3_sInf_sSup_sandwich_verified"])
        self.assertTrue(part_f["sphereC_sInf_sSup_sandwich_verified"])
        self.assertTrue(part_f["real_triaxial_spectral_ordering_verified"])
        self.assertTrue(part_f["complex_triaxial_spectral_ordering_verified"])
        self.assertEqual(part_f["spectral_families_tested"], 5)


if __name__ == "__main__":
    unittest.main()

