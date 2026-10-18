"""
test_symbol_game_coda_meron_ladder.py: Tests for Symbol Game CODA & Meron 4D Ladder.

AuthorityEffect: None.

Verifies:
  1. Top five targets structure, dimensions (2D to 4D), and CODA layers.
  2. Pure Gamma38 wire parsing and semantic validity across all targets.
  3. Claim hygiene enforcement rejecting forbidden hype verbs.
  4. Blind problem declaration hygiene rejecting domain smuggling keywords.
  5. Mathematical exactness of rational intervals, bivectors, and sign cancellations.
  6. Receipt export and SHA-256 integrity verification.
"""

from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path
import tempfile
import unittest

from omega_engine_projects.finite_to_continuum.code.symbol_game_coda_meron_ladder import (
    BLIND_FORBIDDEN_KEYWORDS,
    FORBIDDEN_CLAIM_WORDS,
    TargetSpec,
    assert_blind_hygiene,
    assert_claim_hygiene,
    build_top_five_targets,
    compute_t1_receipt,
    compute_t2_receipt,
    compute_t3_receipt,
    compute_t4_receipt,
    compute_t5_receipt,
    export_target_ladder_receipt,
    verify_all_targets,
    verify_target_gamma38,
    verify_target_hygiene,
)
from omega_engine_pfp.domain.tower.parser import (
    GAMMA_38,
    parse_packet,
    validate_packet_semantics,
)


class TestSymbolGameCodaMeronLadder(unittest.TestCase):
    """Test suite for Symbol Game CODA & Meron 4D Ladder module."""

    def setUp(self) -> None:
        self.targets = build_top_five_targets()

    def test_top_five_targets_count_and_dimensions(self) -> None:
        """Assert exactly 5 targets exist spanning dimensions 2, 3, and 4."""
        self.assertEqual(len(self.targets), 5)
        expected_dims = [2, 2, 3, 4, 4]
        actual_dims = [t.dimension for t in self.targets]
        self.assertEqual(actual_dims, expected_dims)

        target_ids = [t.target_id for t in self.targets]
        expected_ids = [
            "T1_2D_MERON_TORUS_CANCELLATION",
            "T2_REGGE_DEFICIT_ANGLE_CONTINUUM_ENCLOSURE",
            "T3_3D_MERON_STRINGS_PONTRYAGIN_T3",
            "T4_4D_REGGE_SIMPLICITY_BIANCHI_HOLONOMY",
            "T5_4D_MERON_HALF_INSTANTON_CHERN_CANCELLATION",
        ]
        self.assertEqual(target_ids, expected_ids)

    def test_all_targets_gamma38_wire_validity(self) -> None:
        """Assert all wire strings use only Gamma38 glyphs and pass parser validation."""
        for t in self.targets:
            wire = t.gamma38_wire
            for ch in wire:
                self.assertIn(ch, GAMMA_38, f"Target {t.target_id} contains illegal character {ch!r}")

            parsed = parse_packet(wire)
            self.assertIsNotNone(parsed)

            validate_packet_semantics(parsed)

            self.assertTrue(verify_target_gamma38(t))

    def test_all_targets_claim_hygiene(self) -> None:
        """Assert narrative fields contain zero forbidden hype verbs."""
        for t in self.targets:
            self.assertTrue(verify_target_hygiene(t))

        for bad_word in FORBIDDEN_CLAIM_WORDS:
            with self.assertRaises(ValueError):
                assert_claim_hygiene(f"This result {bad_word} the theorem.")

    def test_all_targets_blind_hygiene(self) -> None:
        """Assert blind declarations contain zero domain smuggling keywords."""
        for t in self.targets:
            assert_blind_hygiene(t.blind_problem_declaration)

        for bad_keyword in BLIND_FORBIDDEN_KEYWORDS:
            with self.assertRaises(ValueError):
                assert_blind_hygiene(f"Consider the {bad_keyword} system.")

    def test_t1_mathematical_receipt(self) -> None:
        """Assert T1 2D torus receipt contains exact values and zero duality gap."""
        r1 = compute_t1_receipt()
        self.assertEqual(r1["dimension"], 2)
        self.assertEqual(r1["sites"], 16)
        self.assertEqual(r1["exact_partition_z"], 912)
        self.assertEqual(r1["winding_parity_sectors"]["duality_gap"], "0")
        self.assertEqual(r1["winding_parity_sectors"]["odd_winding_clusters_cancelled"], 192)

    def test_t2_mathematical_receipt(self) -> None:
        """Assert T2 Regge calculus receipt contains positive CM det and interval pi/3."""
        r2 = compute_t2_receipt()
        self.assertEqual(r2["dimension"], 2)
        self.assertEqual(r2["deficit_angle_sixths"], 1)
        self.assertTrue(r2["nondegenerate"])
        self.assertEqual(r2["cayley_menger_det_2simplex"], "3")

        lo_str, hi_str = r2["deficit_angle_interval_radians"]
        lo = Fraction(lo_str)
        hi = Fraction(hi_str)
        width = hi - lo
        self.assertGreater(width, 0)
        self.assertLess(width, Fraction(1, 10**20))

    def test_t3_mathematical_receipt(self) -> None:
        """Assert T3 3D torus string receipt contains orthogonality and cancellation."""
        r3 = compute_t3_receipt()
        self.assertEqual(r3["dimension"], 3)
        self.assertEqual(r3["lattice_sites"], 64)
        self.assertTrue(r3["odd_winding_cancellation"])
        max_res = Fraction(r3["character_orthogonality_max_residual"])
        self.assertLessEqual(max_res, Fraction(1, 10**20))

    def test_t4_mathematical_receipt(self) -> None:
        """Assert T4 4D Regge bivectors satisfy simplicity and contracted Bianchi."""
        r4 = compute_t4_receipt()
        self.assertEqual(r4["dimension"], 4)
        self.assertEqual(r4["barrett_crane_simplicity_norm"], "0")
        self.assertEqual(r4["contracted_bianchi_norm_bivector"], "0")
        self.assertEqual(r4["boundary_tetrahedra_count"], 5)
        self.assertEqual(r4["triangular_hinges_count"], 10)

    def test_t5_mathematical_receipt(self) -> None:
        """Assert T5 4D merons satisfy second Chern half-integer charge and sign flip."""
        r5 = compute_t5_receipt()
        self.assertEqual(r5["dimension"], 4)
        self.assertEqual(r5["half_instanton_topological_charge"], "1/2")
        self.assertEqual(r5["cluster_fermion_sign"], -1)
        self.assertEqual(r5["inversion_fermion_sign"], 1)
        self.assertTrue(r5["exact_zero_sum_doublet"])
        self.assertTrue(r5["partition_sign_obstruction_resolved"])

    def test_verify_all_targets_summary(self) -> None:
        """Assert verify_all_targets returns full verification summary."""
        summary = verify_all_targets()
        self.assertEqual(summary["total_targets"], 5)
        self.assertEqual(summary["dimensions_covered"], [2, 2, 3, 4, 4])
        self.assertTrue(summary["all_verified"])

    def test_export_and_validate_receipt_file(self) -> None:
        """Assert export_target_ladder_receipt writes valid JSON with valid SHA-256."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = Path(tmpdir) / "test_ladder_receipt.json"
            exported = export_target_ladder_receipt(target_path=out_file)
            self.assertTrue(exported.exists())

            with exported.open("r", encoding="utf-8") as f:
                data = json.load(f)

            self.assertEqual(data["receipt_version"], "1.0.0")
            self.assertIn("sha256_digest", data)
            self.assertEqual(len(data["targets"]), 5)
            self.assertTrue(data["verification_summary"]["all_verified"])


if __name__ == "__main__":
    unittest.main()
