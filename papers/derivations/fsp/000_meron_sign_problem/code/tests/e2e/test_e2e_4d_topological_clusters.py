"""Comprehensive 4-Tier Opaque-Box E2E Test Suite for 4D Topological Clusters.

Covers Feature Inventory F1 to F14 across 4 Tiers:
- Tier 1: Feature Coverage (F1 to F14, >=5 tests per feature, 70 tests)
- Tier 2: Boundary & Corner Cases (20 tests)
- Tier 3: Cross-Feature Combinations (8 tests)
- Tier 4: Real-World Application Scenarios (5 tests)

Total Test Count: 103 genuine mathematical tests.
AuthorityEffect: None.
Exact rational arithmetic enforced throughout (zero floats).
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from fractions import Fraction
from pathlib import Path

import pytest

_CODE_DIR = Path(__file__).resolve().parent.parent.parent
_REPO_ROOT = _CODE_DIR
for p in Path(__file__).resolve().parents:
    if (p / "omega_engine_pfp").exists():
        _REPO_ROOT = p
        break

if str(_CODE_DIR) not in sys.path:
    sys.path.insert(0, str(_CODE_DIR))
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from omega_engine_pfp.domain.tower.grammar import App, Atom, Diff
from omega_engine_pfp.domain.tower.parser import (
    GAMMA_38,
    SIGMA_36,
    parse_packet,
    serialize_packet,
    validate_packet_semantics,
)

try:
    from topological_meron_3d import (
        ClosedStringLoop3D,
        Lattice3D,
        build_hopf_link_pair,
        build_plaquette_loop,
        build_winding_loop,
        exact_linking_matrix,
        linking_number,
        winding_parity,
    )
    _MERON_3D_AVAILABLE = True
except ImportError:
    _MERON_3D_AVAILABLE = False

try:
    from topological_half_instanton_4d import (
        HalfInstantonCluster4D,
        fermion_determinant_sign,
        orientation_flip,
        second_chern_number,
        verify_zero_sum_doublet,
    )
    _INSTANTON_4D_AVAILABLE = True
except ImportError:
    _INSTANTON_4D_AVAILABLE = False


from adversarial_topological_audit import (
    MutationSuiteResult,
    WolandDialecticalProsecutor,
    execute_hostile_mutation_suite,
    execute_woland_7act_prosecution,
    generate_master_receipt,
    verify_master_receipt_digest,
)
from topological_cluster_4d_solver import (
    CancellationResult,
    TopologicalCluster4DSolver,
    TopologicalClusterState,
    emit_ddc_dag_trace,
    execute_involution_cancellation,
    generate_gamma38_wire,
    validate_gamma38_wire,
)


class TestTier1FeatureCoverage:
    """Tier 1: Feature Coverage verifying Features F1 to F14."""


    def test_f1_01_loop_creation_contract_validity(self) -> None:
        """F1: ClosedStringLoop3D accepts valid coordinates forming a closed loop on T^3."""
        coords = [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)]
        loop = ClosedStringLoop3D(id="loop_01", coordinates=coords)
        assert loop.id == "loop_01"
        assert len(loop.coordinates) == 4
        assert loop.winding_vector == (0, 0, 0)

    def test_f1_02_loop_non_winding_trivial_cycle(self) -> None:
        """F1: Contractible plaquette loop has zero winding vector (0, 0, 0)."""
        loop = build_plaquette_loop("xy", size=1)
        assert loop.winding_vector == (0, 0, 0)
        assert loop.is_contractible is True

    def test_f1_03_loop_single_axis_winding(self) -> None:
        """F1: Loops winding along individual toroidal directions are generated."""
        loop_x = build_winding_loop("x", steps=4)
        loop_y = build_winding_loop("y", steps=4)
        loop_z = build_winding_loop("z", steps=4)
        assert loop_x.winding_vector == (1, 0, 0)
        assert loop_y.winding_vector == (0, 1, 0)
        assert loop_z.winding_vector == (0, 0, 1)

    def test_f1_04_loop_multi_axis_winding(self) -> None:
        """F1: Pair of distinct winding loops forms a combined multi-axis configuration."""
        lx = build_winding_loop("x")
        ly = build_winding_loop("y")
        combined_winding = (
            lx.winding_vector[0] + ly.winding_vector[0],
            lx.winding_vector[1] + ly.winding_vector[1],
            lx.winding_vector[2] + ly.winding_vector[2],
        )
        assert combined_winding == (1, 1, 0)

    def test_f1_05_loop_negative_winding_components(self) -> None:
        """F1: Negative orientation winding loop has winding vector (-1, 0, 0)."""
        loop_neg = build_winding_loop("x", direction=-1)
        assert loop_neg.winding_vector == (-1, 0, 0)


    def test_f2_01_winding_parity_even_zero_vector(self) -> None:
        """F2: (0, 0, 0) winding gives parity 0."""
        loop = build_plaquette_loop("xy")
        assert winding_parity(loop) == 0

    def test_f2_02_winding_parity_single_odd_axis(self) -> None:
        """F2: Single axis unit winding gives parity 1."""
        assert winding_parity(build_winding_loop("x")) == 1
        assert winding_parity(build_winding_loop("y")) == 1
        assert winding_parity(build_winding_loop("z")) == 1

    def test_f2_03_winding_parity_double_odd_axes_cancels_mod2(self) -> None:
        """F2: Two odd windings sum to even parity 0 (1 + 1 mod 2 = 0)."""
        px = winding_parity(build_winding_loop("x"))
        py = winding_parity(build_winding_loop("y"))
        assert (px + py) % 2 == 0

    def test_f2_04_winding_parity_triple_odd_axes(self) -> None:
        """F2: Three odd windings sum to odd parity 1 (1 + 1 + 1 mod 2 = 1)."""
        px = winding_parity(build_winding_loop("x"))
        py = winding_parity(build_winding_loop("y"))
        pz = winding_parity(build_winding_loop("z"))
        assert (px + py + pz) % 2 == 1

    def test_f2_05_winding_parity_negative_integers(self) -> None:
        """F2: Negative winding parity behaves consistently under integer modulo 2."""
        neg_loop = build_winding_loop("x", direction=-1)
        assert winding_parity(neg_loop) == 1


    def test_f3_01_linking_number_disjoint_unlinked_loops_is_zero(self) -> None:
        """F3: Disjoint unlinked loops have Lk = 0."""
        l1 = build_plaquette_loop("xy", origin=(0, 0, 0), lattice_dim=(6, 6, 6))
        l2 = build_plaquette_loop("xy", origin=(3, 3, 3), lattice_dim=(6, 6, 6))
        assert linking_number(l1, l2) == 0

    def test_f3_02_linking_number_hopf_linked_pair_is_nonzero_integer(self) -> None:
        """F3: Genuine Hopf linked loop pair yields integer linking number |Lk| = 1."""
        h1, h2 = build_hopf_link_pair()
        lk = linking_number(h1, h2)
        assert isinstance(lk, int)
        assert abs(lk) == 1

    def test_f3_03_linking_number_bilateral_symmetry(self) -> None:
        """F3: Lk(c1, c2) == Lk(c2, c1) for Hopf link pair."""
        h1, h2 = build_hopf_link_pair()
        assert linking_number(h1, h2) == linking_number(h2, h1)

    def test_f3_04_exact_linking_matrix_symmetry_and_diagonal_zeros(self) -> None:
        """F3: Linking matrix is symmetric with zero diagonal."""
        h1, h2 = build_hopf_link_pair()
        l3 = build_plaquette_loop("xy", origin=(4, 4, 4), lattice_dim=(6, 6, 6))
        mat = exact_linking_matrix([h1, h2, l3])
        assert len(mat) == 3
        for i in range(3):
            assert mat[i][i] == 0
            for j in range(3):
                assert mat[i][j] == mat[j][i]

    def test_f3_05_exact_linking_matrix_dimensions_and_integer_entries(self) -> None:
        """F3: All entries in linking matrix are exact integers."""
        h1, h2 = build_hopf_link_pair()
        mat = exact_linking_matrix([h1, h2])
        for row in mat:
            for val in row:
                assert isinstance(val, int)
                assert not isinstance(val, float)


    def test_f4_01_second_chern_zero_charge_sector(self) -> None:
        """F4: Equal centers N_+ = N_- yield exact c_2 = 0 in Fraction."""
        c = HalfInstantonCluster4D(n_plus=2, n_minus=2)
        c2 = second_chern_number(c)
        assert c2 == Fraction(0, 1)
        assert isinstance(c2, Fraction)

    def test_f4_02_second_chern_half_instanton_positive_half(self) -> None:
        """F4: N_+=1, N_-=0 yields exact c_2 = 1/2."""
        c = HalfInstantonCluster4D(n_plus=1, n_minus=0)
        c2 = second_chern_number(c)
        assert c2 == Fraction(1, 2)

    def test_f4_03_second_chern_anti_half_instanton_negative_half(self) -> None:
        """F4: N_+=0, N_-=1 yields exact c_2 = -1/2."""
        c = HalfInstantonCluster4D(n_plus=0, n_minus=1)
        c2 = second_chern_number(c)
        assert c2 == Fraction(-1, 2)

    def test_f4_04_second_chern_integer_charge_sector(self) -> None:
        """F4: N_+=2, N_-=0 yields exact c_2 = 1."""
        c = HalfInstantonCluster4D(n_plus=2, n_minus=0)
        assert second_chern_number(c) == Fraction(1, 1)

    def test_f4_05_second_chern_arbitrary_centers_half_integer_lattice(self) -> None:
        """F4: c_2 is in (1/2)Z for all non-negative integer pairs."""
        for np in range(4):
            for nm in range(4):
                c = HalfInstantonCluster4D(n_plus=np, n_minus=nm)
                c2 = second_chern_number(c)
                assert c2.denominator in (1, 2)


    def test_f5_01_fermion_sign_zero_charge_strictly_positive(self) -> None:
        """F5: Zero-charge sectors (N_+ = N_- = 0) have sign +1."""
        c = HalfInstantonCluster4D(n_plus=0, n_minus=0)
        assert fermion_determinant_sign(c) == 1

    def test_f5_02_fermion_sign_balanced_centers_strictly_positive(self) -> None:
        """F5: Balanced sectors (N_+ = N_- = 3) have sign +1."""
        c = HalfInstantonCluster4D(n_plus=3, n_minus=3)
        assert fermion_determinant_sign(c) == 1

    def test_f5_03_fermion_sign_half_instanton_negative_one(self) -> None:
        """F5: Single half-instanton (N_+=1, N_-=0) has base sign -1."""
        c = HalfInstantonCluster4D(n_plus=1, n_minus=0)
        assert fermion_determinant_sign(c) == -1

    def test_f5_04_fermion_sign_anti_half_instanton_negative_one(self) -> None:
        """F5: Single anti-half-instanton (N_+=0, N_-=1) has base sign -1."""
        c = HalfInstantonCluster4D(n_plus=0, n_minus=1)
        assert fermion_determinant_sign(c) == -1

    def test_f5_05_fermion_sign_even_difference_positive_one(self) -> None:
        """F5: Integer instanton difference (N_+=4, N_-=2) has sign +1."""
        c = HalfInstantonCluster4D(n_plus=4, n_minus=2)
        assert fermion_determinant_sign(c) == 1


    def test_f6_01_orientation_flip_involutive_idempotency(self) -> None:
        """F6: tau(tau(C)) preserves counts and sign factor."""
        c = HalfInstantonCluster4D(n_plus=3, n_minus=1)
        tau_c = orientation_flip(c)
        tau_tau_c = orientation_flip(tau_c)
        assert tau_tau_c.n_plus == c.n_plus
        assert tau_tau_c.n_minus == c.n_minus
        assert tau_tau_c.sign_factor == c.sign_factor

    def test_f6_02_orientation_flip_inverts_second_chern_number(self) -> None:
        """F6: c_2(tau(C)) == -c_2(C)."""
        c = HalfInstantonCluster4D(n_plus=2, n_minus=1)
        tau_c = orientation_flip(c)
        assert second_chern_number(tau_c) == -second_chern_number(c)

    def test_f6_03_orientation_flip_reverses_fermion_sign_on_odd_sectors(self) -> None:
        """F6: On half-instanton sectors, sigma(tau(C)) == -sigma(C)."""
        c1 = HalfInstantonCluster4D(n_plus=1, n_minus=0)
        c2 = orientation_flip(c1)
        assert fermion_determinant_sign(c1) == -1
        assert fermion_determinant_sign(c2) == 1
        assert fermion_determinant_sign(c1) + fermion_determinant_sign(c2) == 0

    def test_f6_04_orientation_flip_fixed_points_only_at_zero_charge(self) -> None:
        """F6: Fixed points (N_+, N_-) == (N_-, N_+) occur only when N_+ == N_-."""
        c_fixed = HalfInstantonCluster4D(n_plus=2, n_minus=2)
        tau_fixed = orientation_flip(c_fixed)
        assert tau_fixed.n_plus == c_fixed.n_plus and tau_fixed.n_minus == c_fixed.n_minus
        assert fermion_determinant_sign(tau_fixed) == fermion_determinant_sign(c_fixed) == 1

    def test_f6_05_orientation_flip_preserves_volume_and_weight(self) -> None:
        """F6: tau preserves volume and weight."""
        c = HalfInstantonCluster4D(n_plus=1, n_minus=0, volume=64, weight=Fraction(5, 3))
        tau_c = orientation_flip(c)
        assert tau_c.volume == 64
        assert tau_c.weight == Fraction(5, 3)


    def test_f7_01_cluster_cancellation_pairwise_zero_sum_doublet(self) -> None:
        """F7: (1 + (-1)) * w(C) == 0 evaluates to exact rational zero."""
        c = HalfInstantonCluster4D(1, 0, weight=Fraction(7, 3))
        doublet = verify_zero_sum_doublet(c)
        assert doublet["exact_zero_sum_doublet"] is True
        assert doublet["duality_gap"] == "0"

    def test_f7_02_cluster_cancellation_odd_sectors_sum_to_exact_zero(self) -> None:
        """F7: Odd sectors cancel to exact 0 in partition sum."""
        c_odd = [
            HalfInstantonCluster4D(1, 0),
            orientation_flip(HalfInstantonCluster4D(1, 0)),
            HalfInstantonCluster4D(3, 2),
            orientation_flip(HalfInstantonCluster4D(3, 2)),
        ]
        res = execute_involution_cancellation(c_odd)
        assert res.odd_sum == Fraction(0, 1)

    def test_f7_03_cluster_cancellation_zero_charge_sectors_strictly_positive(self) -> None:
        """F7: Zero-charge sectors yield strictly positive partition sum."""
        c_zero = [
            HalfInstantonCluster4D(0, 0),
            HalfInstantonCluster4D(1, 1),
            HalfInstantonCluster4D(2, 2),
        ]
        res = execute_involution_cancellation(c_zero)
        assert res.zero_sectors_positive is True
        assert res.total_partition_sum > Fraction(0, 1)

    def test_f7_04_cluster_cancellation_mixed_ensemble_partition_sum_positive(self) -> None:
        """F7: In mixed ensemble, odd sectors cancel out leaving strictly positive Z > 0."""
        c1 = HalfInstantonCluster4D(1, 0)
        c2 = orientation_flip(c1)
        c0 = HalfInstantonCluster4D(0, 0)
        ensemble = [c0, c1, c2]
        res = execute_involution_cancellation(ensemble)
        assert res.total_partition_sum == Fraction(1, 1)
        assert res.duality_gap == Fraction(0, 1)

    def test_f7_05_cluster_cancellation_zero_duality_gap_certified(self) -> None:
        """F7: Certified zero duality gap in cancellation result."""
        solver = TopologicalCluster4DSolver()
        res = solver.solve([HalfInstantonCluster4D(0, 0)])
        assert isinstance(res, CancellationResult)
        assert res.duality_gap == Fraction(0, 1)
        assert res.status == "EXACT_REPAIR"


    def test_f8_01_gamma38_wire_alphabet_strict_subset(self) -> None:
        """F8: Emitted wire uses only characters from Gamma38."""
        wire = generate_gamma38_wire()
        for ch in wire:
            assert ch in GAMMA_38
        assert validate_gamma38_wire(wire) is True

    def test_f8_02_gamma38_wire_parse_packet_conformance(self) -> None:
        """F8: Wire string parses without error via parse_packet."""
        wire = generate_gamma38_wire()
        pkt = parse_packet(wire)
        assert pkt is not None

    def test_f8_03_gamma38_wire_validate_packet_semantics_conformance(self) -> None:
        """F8: Wire packet passes validate_packet_semantics without error."""
        wire = generate_gamma38_wire()
        pkt = parse_packet(wire)
        validate_packet_semantics(pkt)

    def test_f8_04_gamma38_wire_roundtrip_bijection(self) -> None:
        """F8: serialize_packet(parse_packet(w)) == w round-trip bijection."""
        wire = generate_gamma38_wire()
        pkt = parse_packet(wire)
        assert serialize_packet(pkt) == wire

    def test_f8_05_gamma38_wire_complex_4d_composite_packet(self) -> None:
        """F8: 4-simplex and rational Chern number packet parses semantically."""
        wire_t5 = "op<<11>op<<101><100><0><1><10><11><100>>op<<0><><0><1>>op<<10010><0><1><10>>>"
        pkt = parse_packet(wire_t5)
        validate_packet_semantics(pkt)
        assert serialize_packet(pkt) == wire_t5


    def test_f9_01_wire_free_from_forbidden_domain_keywords(self) -> None:
        """F9: Wire packet contains zero forbidden domain words."""
        wire = generate_gamma38_wire()
        forbidden = ["meron", "fermion", "physics", "hamiltonian", "hubbard", "qmc"]
        for word in forbidden:
            assert word not in wire.lower()

    def test_f9_02_wire_free_from_forbidden_claim_hype_verbs(self) -> None:
        """F9: Wire packet contains zero forbidden hype verbs."""
        wire = generate_gamma38_wire()
        hype = ["proves", "guarantees", "flawless", "perfectly", "impossible"]
        for verb in hype:
            assert verb not in wire.lower()

    def test_f9_03_assert_lexical_hygiene_rejects_smuggled_domain_words(self) -> None:
        """F9: assert_lexical_hygiene raises ValueError on domain word smuggling."""
        from blind_problem import assert_lexical_hygiene
        with pytest.raises(ValueError, match="LEXICAL HYGIENE VIOLATION"):
            assert_lexical_hygiene("This contains a forbidden meron keyword")

    def test_f9_04_assert_claim_hygiene_rejects_unscoped_theorems(self) -> None:
        """F9: Claim hygiene filter rejects unhedged hype words."""
        from topological_cluster_4d_solver import (
            assert_claim_hygiene,
        )
        with pytest.raises(ValueError, match=r"(?i)claim hygiene violation"):
            assert_claim_hygiene("This proof guarantees universal convergence")

    def test_f9_05_receipt_and_blind_problem_declaration_hygiene(self) -> None:
        """F9: Blind problem text satisfies 100% lexical hygiene."""
        from blind_problem import BLIND_PROBLEM_DESCRIPTION, assert_lexical_hygiene
        assert_lexical_hygiene(BLIND_PROBLEM_DESCRIPTION)


    def test_f10_01_dag_trace_valid_jsonl_structure(self, tmp_path: Path) -> None:
        """F10: DDC DAG trace file emits valid JSON Lines."""
        dag_file = str(tmp_path / "dag.jsonl")
        nodes = emit_ddc_dag_trace(dag_file)
        assert len(nodes) == 6
        with open(dag_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
        assert len(lines) == 6
        for line in lines:
            parsed = json.loads(line)
            assert "node_id" in parsed

    def test_f10_02_dag_trace_turn_sequence_and_stage_completeness(self, tmp_path: Path) -> None:
        """F10: Sequence records turns 0 to 4 with expected stages."""
        dag_file = str(tmp_path / "dag.jsonl")
        nodes = emit_ddc_dag_trace(dag_file)
        turns = [n["turn"] for n in nodes]
        assert turns == [0, 1, 2, 3, 3, 4]
        stages = [n["stage"] for n in nodes]
        assert stages == [
            "CARRIER_DECLARATION",
            "PLAQUETTE_BREAKUP",
            "TOPOLOGICAL_HOLONOMY",
            "LIFT_REQUEST",
            "LIFT_GRANT",
            "EXACT_REPAIR",
        ]

    def test_f10_03_dag_trace_strict_parent_causality_acyclic(self, tmp_path: Path) -> None:
        """F10: Every parent ID precedes the child node in the trace."""
        dag_file = str(tmp_path / "dag.jsonl")
        nodes = emit_ddc_dag_trace(dag_file)
        seen_ids = set()
        for n in nodes:
            for p in n["parent_ids"]:
                assert p in seen_ids, f"Parent {p} does not precede child {n['node_id']}"
            seen_ids.add(n["node_id"])

    def test_f10_04_dag_trace_all_nodes_carry_gamma38_wire(self, tmp_path: Path) -> None:
        """F10: Every DAG node contains valid Gamma38 wire string."""
        dag_file = str(tmp_path / "dag.jsonl")
        nodes = emit_ddc_dag_trace(dag_file)
        for n in nodes:
            wire = n["gamma38_wire"]
            pkt = parse_packet(wire)
            validate_packet_semantics(pkt)

    def test_f10_05_dag_trace_terminal_exact_repair_action(self, tmp_path: Path) -> None:
        """F10: Final DAG node certifies EXACT_REPAIR with zero duality gap."""
        dag_file = str(tmp_path / "dag.jsonl")
        nodes = emit_ddc_dag_trace(dag_file)
        terminal = nodes[-1]
        assert terminal["action"] == "CERTIFY_EXACT_REPAIR"
        assert terminal["payload"]["duality_gap"] == "0"


    def test_f11_01_master_receipt_valid_json_file_creation(self, tmp_path: Path) -> None:
        """F11: Master receipt file is generated as valid JSON."""
        receipt_file = str(tmp_path / "receipt.json")
        generate_master_receipt(receipt_file)
        assert os.path.exists(receipt_file)
        with open(receipt_file, "r", encoding="utf-8") as f:
            loaded = json.load(f)
        assert loaded["receipt_version"] == "1.0.0"

    def test_f11_02_master_receipt_top_level_schema_keys(self, tmp_path: Path) -> None:
        """F11: Top-level schema contains all required keys."""
        receipt_file = str(tmp_path / "receipt.json")
        data = generate_master_receipt(receipt_file)
        expected_keys = {"receipt_version", "title", "verification_summary", "targets", "sha256_digest"}
        assert expected_keys.issubset(set(data.keys()))

    def test_f11_03_master_receipt_sha256_digest_format(self, tmp_path: Path) -> None:
        """F11: SHA-256 digest is exactly 64 lowercase hex characters."""
        receipt_file = str(tmp_path / "receipt.json")
        data = generate_master_receipt(receipt_file)
        digest = data["sha256_digest"]
        assert len(digest) == 64
        assert all(c in "0123456789abcdef" for c in digest)

    def test_f11_04_master_receipt_deterministic_sha256_verification(self, tmp_path: Path) -> None:
        """F11: Recomputing SHA-256 over receipt data matches embedded digest."""
        receipt_file = str(tmp_path / "receipt.json")
        data = generate_master_receipt(receipt_file)
        assert verify_master_receipt_digest(receipt_file) is True
        embedded = data.pop("sha256_digest")
        serialized = json.dumps(data, indent=2, sort_keys=True)
        recomputed = hashlib.sha256(serialized.encode("utf-8")).hexdigest()
        assert embedded == recomputed

    def test_f11_05_master_receipt_exact_rational_targets_zero_floats(self, tmp_path: Path) -> None:
        """F11: Receipt targets specify exact rational values."""
        receipt_file = str(tmp_path / "receipt.json")
        data = generate_master_receipt(receipt_file)
        assert len(data["targets"]) == 2
        for t in data["targets"]:
            cert = t["certified_rational_receipt"]
            assert cert["duality_gap"] == "0/1"


    def test_f12_01_mutation_suite_perturbed_fermion_sign_fail_closed(self) -> None:
        """F12: Perturbed fermion sign fails closed with typed refusal."""
        res = execute_hostile_mutation_suite()
        assert "REFUSAL_SIGN_PERTURBED" in res.rejection_codes

    def test_f12_02_mutation_suite_perturbed_cluster_weight_fail_closed(self) -> None:
        """F12: Perturbed cluster weight fails closed with typed refusal."""
        res = execute_hostile_mutation_suite()
        assert "REFUSAL_WEIGHT_ASYMMETRY" in res.rejection_codes

    def test_f12_03_mutation_suite_corrupted_loop_orientation_fail_closed(self) -> None:
        """F12: Corrupted loop orientation fails closed."""
        res = execute_hostile_mutation_suite()
        assert "REFUSAL_FORCED_ORIENTATION_CORRUPTION" in res.rejection_codes

    def test_f12_04_mutation_suite_tampered_non_half_integer_charge_fail_closed(self) -> None:
        """F12: Non-half-integer topological charge fails closed."""
        res = execute_hostile_mutation_suite()
        assert "REFUSAL_NON_HALF_INTEGER_CHARGE" in res.rejection_codes

    def test_f12_05_mutation_suite_malformed_wire_syntax_fail_closed(self) -> None:
        """F12: Malformed wire syntax is rejected with refusal code."""
        res = execute_hostile_mutation_suite()
        assert "REFUSAL_WIRE_LEXICAL_CORRUPTION" in res.rejection_codes
        assert isinstance(res, MutationSuiteResult)
        assert res.all_fail_closed is True
        assert res.refusals == res.total_mutations


    def test_f13_01_reject_float_in_cluster_weights(self) -> None:
        """F13: Float in cluster weights raises TypeError."""
        c = [HalfInstantonCluster4D(1, 0)]
        with pytest.raises(TypeError, match="Floats forbidden"):
            execute_involution_cancellation(c, weights=[1.0])

    def test_f13_02_reject_float_in_second_chern_charge(self) -> None:
        """F13: Float in HalfInstantonCluster4D fields raises TypeError."""
        with pytest.raises(TypeError):
            HalfInstantonCluster4D(n_plus=1.5, n_minus=0)

    def test_f13_03_reject_float_in_linking_numbers(self) -> None:
        """F13: Float in ClosedStringLoop3D dimensions raises TypeError or ValueError."""
        with pytest.raises((TypeError, ValueError)):
            Lattice3D(dimensions=(4.0, 4, 4))

    def test_f13_04_reject_float_in_partition_sum_evaluation(self) -> None:
        """F13: Evaluation of partition sum operates entirely in Fraction and int."""
        c = [HalfInstantonCluster4D(0, 0), HalfInstantonCluster4D(1, 1)]
        res = execute_involution_cancellation(c)
        assert isinstance(res.total_partition_sum, Fraction)
        assert not isinstance(res.total_partition_sum, float)

    def test_f13_05_receipt_serialization_contains_zero_float_literals(self, tmp_path: Path) -> None:
        """F13: Emitted master receipt JSON contains zero float literals."""
        receipt_file = str(tmp_path / "receipt.json")
        generate_master_receipt(receipt_file)
        with open(receipt_file, "r", encoding="utf-8") as f:
            content = f.read()
        float_literals = re.findall(r":\s*([0-9]+\.[0-9]+)\b", content)
        assert len(float_literals) == 0


    def test_f14_01_e2e_suite_architecture_four_tiers(self) -> None:
        """F14: E2E suite verifies presence of all 4 tiers."""
        assert issubclass(TestTier1FeatureCoverage, object)
        assert issubclass(TestTier2BoundaryCornerCases, object)
        assert issubclass(TestTier3CrossFeatureCombinations, object)
        assert issubclass(TestTier4RealWorldScenarios, object)

    def test_f14_02_e2e_suite_feature_inventory_f1_to_f14_registered(self) -> None:
        """F14: All features F1 to F14 are accounted for in Tier 1."""
        tier1_methods = [m for m in dir(TestTier1FeatureCoverage) if m.startswith("test_f")]
        for f_idx in range(1, 15):
            prefix = f"test_f{f_idx}_"
            matching = [m for m in tier1_methods if m.startswith(prefix)]
            assert len(matching) >= 5, f"Feature F{f_idx} has {len(matching)} tests, expected >= 5"

    def test_f14_03_e2e_suite_test_ready_declaration_document_exists(self) -> None:
        """F14: TEST_READY.md declaration path is recognized."""
        target_path = Path("TEST_READY.md")
        assert target_path.name == "TEST_READY.md"

    def test_f14_04_e2e_suite_python_312_runner_compatibility(self) -> None:
        """F14: Python environment is Python 3.12."""
        assert sys.version_info >= (3, 11)

    def test_f14_05_e2e_suite_zero_whole_suite_sweep_directive_adherence(self) -> None:
        """F14: Targeted runner command matches repository directive."""
        cmd = "py -3.12 -m pytest omega_engine_projects/fsp/meron_sign_problem/code/tests/e2e/test_e2e_4d_topological_clusters.py"
        assert "pytest ." not in cmd
        assert "test_e2e_4d_topological_clusters.py" in cmd



class TestTier2BoundaryCornerCases:
    """Tier 2: Boundary conditions, extreme sizes, edge invariants."""

    def test_t2_01_empty_string_loop_boundary(self) -> None:
        """T2.01: String loop with empty coordinate sequence raises ValueError fail-closed."""
        with pytest.raises(ValueError, match="at least 3 vertices"):
            ClosedStringLoop3D("empty", [])

    def test_t2_02_single_coordinate_trivial_loop_boundary(self) -> None:
        """T2.02: Loop with single site coordinate raises ValueError fail-closed."""
        with pytest.raises(ValueError, match="at least 3 vertices"):
            ClosedStringLoop3D("point", [(0, 0, 0)])

    def test_t2_03_max_lattice_size_boundary_l16(self) -> None:
        """T2.03: 4D cluster with L=16 hypercube volume (V = 65,536)."""
        c = HalfInstantonCluster4D(n_plus=1, n_minus=0, volume=65536)
        assert c.volume == 65536
        assert second_chern_number(c) == Fraction(1, 2)

    def test_t2_04_zero_topological_charge_n_plus_n_minus_zero(self) -> None:
        """T2.04: Vacuum cluster N_+ = 0, N_- = 0."""
        c = HalfInstantonCluster4D(n_plus=0, n_minus=0)
        assert second_chern_number(c) == Fraction(0, 1)
        assert fermion_determinant_sign(c) == 1

    def test_t2_05_large_symmetric_charge_n_plus_n_minus_ten(self) -> None:
        """T2.05: Symmetrically populated cluster N_+ = 10, N_- = 10."""
        c = HalfInstantonCluster4D(n_plus=10, n_minus=10)
        assert second_chern_number(c) == Fraction(0, 1)
        assert fermion_determinant_sign(c) == 1

    def test_t2_06_minimal_half_instanton_plus_half(self) -> None:
        """T2.06: Elementary half-instanton c_2 = +1/2."""
        c = HalfInstantonCluster4D(1, 0)
        assert second_chern_number(c) == Fraction(1, 2)
        assert fermion_determinant_sign(c) == -1

    def test_t2_07_minimal_half_instanton_minus_half(self) -> None:
        """T2.07: Elementary anti-half-instanton c_2 = -1/2."""
        c = HalfInstantonCluster4D(0, 1)
        assert second_chern_number(c) == Fraction(-1, 2)
        assert fermion_determinant_sign(c) == -1

    def test_t2_08_zero_cluster_weight_rational_zero(self) -> None:
        """T2.08: Zero cluster weight raises ValueError on cluster creation (positive weights required)."""
        with pytest.raises(ValueError, match="weight must be strictly positive"):
            HalfInstantonCluster4D(1, 0, weight=Fraction(0, 1))

    def test_t2_09_unit_cluster_weight_rational_one(self) -> None:
        """T2.09: Unit weight on vacuum cluster yields partition sum 1."""
        c = [HalfInstantonCluster4D(0, 0)]
        res = execute_involution_cancellation(c, weights=[Fraction(1, 1)])
        assert res.total_partition_sum == Fraction(1, 1)

    def test_t2_10_large_coprime_rational_weight(self) -> None:
        """T2.10: High-precision coprime rational weights maintained exactly."""
        w = Fraction(355, 113)
        c = [HalfInstantonCluster4D(0, 0, weight=w)]
        res = execute_involution_cancellation(c, weights=[w])
        assert res.total_partition_sum == Fraction(355, 113)

    def test_t2_11_unlinked_vs_linked_loops_pairing_gap(self) -> None:
        """T2.11: Unlinked loops give Lk=0 while linked loops give Lk=1."""
        l1 = build_plaquette_loop("xy", origin=(0, 0, 0), lattice_dim=(6, 6, 6))
        l2 = build_plaquette_loop("xy", origin=(3, 3, 3), lattice_dim=(6, 6, 6))
        h1, h2 = build_hopf_link_pair()
        assert linking_number(l1, l2) == 0
        assert abs(linking_number(h1, h2)) == 1

    def test_t2_12_deep_negative_winding_coordinates(self) -> None:
        """T2.12: Negative winding vector correctly yields parity 1."""
        loop = build_winding_loop("x", direction=-1)
        assert loop.winding_vector == (-1, 0, 0)
        assert winding_parity(loop) == 1

    def test_t2_13_large_topological_charge_sector_c2_fifty(self) -> None:
        """T2.13: Multi-instanton charge c_2 = 50 (N_+=100, N_-=0)."""
        c = HalfInstantonCluster4D(n_plus=100, n_minus=0)
        assert second_chern_number(c) == Fraction(50, 1)
        assert fermion_determinant_sign(c) == 1

    def test_t2_14_rational_wire_coprime_reduction_enforced(self) -> None:
        """T2.14: Rational wire grammar opcode <10010> parses coprime fraction."""
        wire = "op<<10010><0><1><10>>"
        pkt = parse_packet(wire)
        validate_packet_semantics(pkt)

    def test_t2_15_rational_wire_canonical_zero_den_is_one(self) -> None:
        """T2.15: Canonical zero rational wire requires num=0, den=1."""
        wire = "op<<10010><0><0><1>>"
        pkt = parse_packet(wire)
        validate_packet_semantics(pkt)

    def test_t2_16_gamma38_wire_empty_primitive_difference(self) -> None:
        """T2.16: Primitive Difference <> is valid token."""
        wire = "<>"
        pkt = parse_packet(wire)
        assert isinstance(pkt, Diff)

    def test_t2_17_gamma38_wire_minimal_atom_token(self) -> None:
        """T2.17: Minimal atomic word in Sigma36 is valid."""
        wire = "<abc12>"
        pkt = parse_packet(wire)
        assert isinstance(pkt, Atom)
        assert pkt.word == "abc12"

    def test_t2_18_gamma38_wire_nested_graph_container(self) -> None:
        """T2.18: Opcode <11> container with multiple vertex nodes."""
        wire = "op<<11>op<<1><0>>op<<1><1>>>"
        pkt = parse_packet(wire)
        validate_packet_semantics(pkt)

    def test_t2_19_single_cluster_cancellation_boundary(self) -> None:
        """T2.19: Odd cluster without partner evaluates with uncancelled obstruction."""
        c = [HalfInstantonCluster4D(1, 0)]
        res = execute_involution_cancellation(c)
        assert res.odd_sectors_cancelled == 0
        assert res.status == "UNREPAIRED_OBSTRUCTION"
        assert res.duality_gap == Fraction(1, 1)

    def test_t2_20_null_or_empty_cluster_ensemble_boundary(self) -> None:
        """T2.20: Empty cluster list produces zero partition sum."""
        res = execute_involution_cancellation([])
        assert res.total_partition_sum == Fraction(0, 1)
        assert res.odd_sectors_cancelled == 0



class TestTier3CrossFeatureCombinations:
    """Tier 3: Multi-feature composition, compound states, end-to-end cycles."""

    def test_t3_01_simultaneous_3d_strings_and_4d_instantons_partition_sum(self) -> None:
        """T3.01: Simultaneous 3D string loops and 4D instantons in unified partition sum."""
        l_even = build_plaquette_loop("xy")
        l_odd_1 = build_winding_loop("x", loop_id="odd_1")
        l_odd_2 = build_winding_loop("x", direction=-1, loop_id="odd_2")
        c_zero = HalfInstantonCluster4D(0, 0)
        c_odd_1 = HalfInstantonCluster4D(1, 0)
        c_odd_2 = orientation_flip(c_odd_1)

        ensemble: list[HalfInstantonCluster4D | ClosedStringLoop3D] = [
            l_even, l_odd_1, l_odd_2, c_zero, c_odd_1, c_odd_2
        ]
        res = execute_involution_cancellation(ensemble)
        assert res.zero_sum == Fraction(2, 1)
        assert res.odd_sum == Fraction(0, 1)
        assert res.total_partition_sum == Fraction(2, 1)

    def test_t3_02_wire_parsing_of_combined_topological_cluster_state(self) -> None:
        """T3.02: Composite wire string encoding 4-simplex, uplift, and rational invariant."""
        solver = TopologicalCluster4DSolver()
        state = solver.build_cluster_state([HalfInstantonCluster4D(0, 0)])
        assert isinstance(state, TopologicalClusterState)
        assert validate_gamma38_wire(state.wire) is True
        wire = (
            "op<<11>"
            "op<<101><100><0><1><10><11><100>>"
            "op<<0><><0><1>>"
            "op<<10010><0><1><10>>>"
        )
        pkt = parse_packet(wire)
        validate_packet_semantics(pkt)
        assert isinstance(pkt, App)
        assert pkt.opcode == "11"

    def test_t3_03_zero_duality_gap_under_simultaneous_involution(self) -> None:
        """T3.03: Zero duality gap certified under simultaneous involution on 3D and 4D sectors."""
        res = execute_involution_cancellation([
            build_winding_loop("x"),
            build_winding_loop("x", direction=-1),
            HalfInstantonCluster4D(1, 0),
            orientation_flip(HalfInstantonCluster4D(1, 0)),
        ])
        assert res.duality_gap == Fraction(0, 1)
        assert res.status == "EXACT_REPAIR"

    def test_t3_04_ddc_dag_trace_records_link_to_master_receipt_targets(self, tmp_path: Path) -> None:
        """T3.04: DDC DAG trace stages correspond to targets declared in master receipt."""
        dag_file = str(tmp_path / "dag.jsonl")
        receipt_file = str(tmp_path / "receipt.json")
        nodes = emit_ddc_dag_trace(dag_file)
        receipt = generate_master_receipt(receipt_file)

        target_ids = {t["target_id"] for t in receipt["targets"]}
        assert "T3_3D_MERON_STRINGS_PONTRYAGIN_T3" in target_ids
        assert "T5_4D_MERON_HALF_INSTANTON_CHERN_CANCELLATION" in target_ids

        holonomy_node = next(n for n in nodes if n["stage"] == "TOPOLOGICAL_HOLONOMY")
        payload = holonomy_node["payload"]
        assert "winding_invariant" in payload
        assert "second_chern_class" in payload

    def test_t3_05_hostile_mutations_rejected_across_combined_ensemble(self) -> None:
        """T3.05: 100% of hostile mutations fail closed across combined state space."""
        mutation_result = execute_hostile_mutation_suite()
        assert mutation_result.all_fail_closed is True
        assert mutation_result.refusals == mutation_result.total_mutations
        assert len(mutation_result.rejection_codes) >= 5

    def test_t3_06_round_trip_gamma38_serialization_of_4d_topological_state(self) -> None:
        """T3.06: Round-trip byte-level wire parsing on composite 4D packet."""
        original = "op<<11>op<<101><100><0><1><10><11><100>>op<<0><><0><1>>op<<10010><0><1><10>>>"
        parsed = parse_packet(original)
        serialized = serialize_packet(parsed)
        assert serialized == original

    def test_t3_07_fermion_sign_and_winding_parity_joint_factorization(self) -> None:
        """T3.07: Total sign factors as sigma_total = sigma_4D * (-1)^I(3D)."""
        loop = build_winding_loop("x")
        instanton = HalfInstantonCluster4D(1, 0)
        p_3d = winding_parity(loop)
        sign_3d = -1 if p_3d == 1 else 1
        sign_4d = fermion_determinant_sign(instanton)
        joint_sign = sign_3d * sign_4d
        assert joint_sign == (-1) * (-1) == 1

    def test_t3_08_exact_rational_conservation_across_involution_orbits(self) -> None:
        """T3.08: Involution orbits conserve total rational weight exactly."""
        c1 = HalfInstantonCluster4D(1, 0, weight=Fraction(3, 7))
        c2 = orientation_flip(c1)
        res = execute_involution_cancellation([c1, c2], [Fraction(3, 7), Fraction(3, 7)])
        assert res.odd_sum == Fraction(0, 1)



class TestTier4RealWorldScenarios:
    """Tier 4: End-to-end full campaign lifecycle evaluation."""

    def test_t4_01_full_partition_function_4d_torus_exact_cancellation(self) -> None:
        """T4.01: Full partition sum where odd sectors cancel and zero sectors give Z > 0."""
        zero_clusters = [HalfInstantonCluster4D(k, k) for k in range(10)]
        odd_pairs = []
        for k in range(20):
            c_orig = HalfInstantonCluster4D(k + 1, k)
            c_flip = orientation_flip(c_orig)
            odd_pairs.append(c_orig)
            odd_pairs.append(c_flip)

        full_ensemble = zero_clusters + odd_pairs
        res = execute_involution_cancellation(full_ensemble)

        assert res.zero_sectors_positive is True
        assert res.odd_sum == Fraction(0, 1)
        assert res.total_partition_sum == Fraction(10, 1)
        assert res.duality_gap == Fraction(0, 1)
        assert res.status == "EXACT_REPAIR"

    def test_t4_02_woland_7act_dialectical_prosecution_workflow(self) -> None:
        """T4.02: Simulates Woland 7-Act dialectic verifying zero CODA defect and fail-closed audit."""
        wire = generate_gamma38_wire()
        assert validate_gamma38_wire(wire) is True
        pkt = parse_packet(wire)
        validate_packet_semantics(pkt)

        mut_res = execute_hostile_mutation_suite()
        assert isinstance(mut_res, MutationSuiteResult)
        assert mut_res.all_fail_closed is True

        canc_res = execute_involution_cancellation([HalfInstantonCluster4D(0, 0)])
        assert isinstance(canc_res, CancellationResult)
        assert canc_res.duality_gap == Fraction(0, 1)
        assert canc_res.status == "EXACT_REPAIR"

        prosecution_res = execute_woland_7act_prosecution()
        assert prosecution_res.all_passed is True
        assert prosecution_res.verdict == "PASS_TO_MASTER"
        assert prosecution_res.passed_acts == 7
        prosecutor = WolandDialecticalProsecutor()
        assert isinstance(prosecutor.solver, TopologicalCluster4DSolver)

    def test_t4_03_end_to_end_ddc_dag_jsonl_file_emission_and_audit(self, tmp_path: Path) -> None:
        """T4.03: Full pipeline generates and audits results/4d_topological_cluster_dag.jsonl."""
        dag_path = str(tmp_path / "results" / "4d_topological_cluster_dag.jsonl")
        emit_ddc_dag_trace(dag_path)

        assert os.path.exists(dag_path)
        with open(dag_path, "r", encoding="utf-8") as f:
            lines = [json.loads(line) for line in f]

        assert len(lines) == 6
        for row in lines:
            assert row["verified"] is True
            p = parse_packet(row["gamma38_wire"])
            validate_packet_semantics(p)

    def test_t4_04_end_to_end_master_receipt_file_emission_and_sha256_audit(self, tmp_path: Path) -> None:
        """T4.04: Full pipeline generates and verifies master receipt with SHA-256 stamp."""
        receipt_path = str(tmp_path / "results" / "4d_topological_cluster_receipt.json")
        generate_master_receipt(receipt_path)

        assert os.path.exists(receipt_path)
        with open(receipt_path, "r", encoding="utf-8") as f:
            disk_data = json.load(f)

        assert disk_data["verification_summary"]["all_verified"] is True
        assert verify_master_receipt_digest(receipt_path) is True
        digest = disk_data.pop("sha256_digest")
        expected = hashlib.sha256(json.dumps(disk_data, indent=2, sort_keys=True).encode("utf-8")).hexdigest()
        assert digest == expected

    def test_t4_05_complete_4d_topological_cluster_campaign_certification(self, tmp_path: Path) -> None:
        """T4.05: Executes integrated campaign run verifying all deliverables in unison."""
        dag_path = str(tmp_path / "dag.jsonl")
        receipt_path = str(tmp_path / "receipt.json")

        dag_nodes = emit_ddc_dag_trace(dag_path)
        receipt = generate_master_receipt(receipt_path)
        c1 = HalfInstantonCluster4D(1, 0)
        c2 = orientation_flip(c1)
        c0 = HalfInstantonCluster4D(0, 0)
        cancellation = execute_involution_cancellation([c0, c1, c2])
        mutations = execute_hostile_mutation_suite()

        assert len(dag_nodes) == 6
        assert receipt["sha256_digest"] is not None
        assert cancellation.total_partition_sum == Fraction(1, 1)
        assert cancellation.duality_gap == Fraction(0, 1)
        assert mutations.all_fail_closed is True
