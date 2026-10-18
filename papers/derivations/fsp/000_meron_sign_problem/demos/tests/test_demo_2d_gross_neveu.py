"""test_demo_2d_gross_neveu.py: Test suite for 2D Staggered Gross-Neveu Meron Demo.

AuthorityEffect: None.

Verifies:
1. 2D Euclidean Staggered Lattice T^2 geometry and Dirac phase signs.
2. 2D Meron cluster topology, winding parity, and orientation involution tau.
3. Inverted posting index bipartite matching and exact zero-sum doublet cancellation.
4. Pure Gamma38 wire grammar parsing and semantic validation via validate_packet_semantics.
5. DDC DAG trace causality and master receipt cryptographic digest verification.
6. Hostile perturbation handling (asymmetric weights, corrupted signs).
7. Zero floating-point constants and calls (AST static audit).
8. Lexical and claim hygiene conformance.
"""

from __future__ import annotations

import ast
import hashlib
import json
import os
import sys
from fractions import Fraction
from pathlib import Path

import pytest

DEMOS_DIR = Path(__file__).resolve().parent.parent
CODE_DIR = DEMOS_DIR.parent / "code"
REPO_ROOT = DEMOS_DIR
for p in DEMOS_DIR.parents:
    if (p / "omega_engine_pfp").exists():
        REPO_ROOT = p
        break

if str(CODE_DIR) not in sys.path:
    sys.path.insert(0, str(CODE_DIR))
if str(DEMOS_DIR / "code") not in sys.path:
    sys.path.insert(0, str(DEMOS_DIR / "code"))
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from demo_2d_gross_neveu_meron import (
    WIRE_TURNS_2D_GN,
    MeronCluster2D,
    StaggeredLattice2D,
    build_canonical_2d_gn_ensemble,
    emit_2d_gn_ddc_dag,
    execute_2d_gn_cancellation,
    generate_2d_gn_receipt,
    run_demo,
    validate_wire_string,
)
from omega_engine_pfp.domain.tower.parser import (
    GAMMA_38,
    parse_packet,
    serialize_packet,
    validate_packet_semantics,
)

from blind_problem import assert_lexical_hygiene



class TestStaggeredLattice2DGeometry:
    """Verifies discrete 2D torus dimensions, links, and staggered phase signs."""

    def test_default_dimensions_and_volume(self) -> None:
        """Lattice initializes with 4x4 sites and 32 links."""
        lat = StaggeredLattice2D(4, 4)
        assert lat.lx == 4
        assert lat.lt == 4
        assert lat.num_sites == 16
        assert len(lat.sites) == 16
        assert len(lat.links_x) == 16
        assert len(lat.links_t) == 16
        assert len(lat.all_links) == 32

    def test_staggered_dirac_phase_signs(self) -> None:
        """Spatial links have phase +1; temporal links have phase (-1)^x."""
        lat = StaggeredLattice2D(4, 4)
        assert lat.staggered_phase((0, 0), (1, 0)) == 1
        assert lat.staggered_phase((1, 0), (2, 0)) == 1

        assert lat.staggered_phase((0, 0), (0, 1)) == 1
        assert lat.staggered_phase((1, 0), (1, 1)) == -1
        assert lat.staggered_phase((2, 0), (2, 1)) == 1
        assert lat.staggered_phase((3, 0), (3, 1)) == -1

    def test_rejects_non_integer_dimensions(self) -> None:
        """Constructor rejects float dimensions fail-closed."""
        with pytest.raises(TypeError):
            StaggeredLattice2D(4.0, 4)
        with pytest.raises(TypeError):
            StaggeredLattice2D(4, 4.5)




class TestMeronCluster2DTopology:
    """Verifies 2D cluster classification, meron identification, and involution properties."""

    def test_neutral_cluster_properties(self) -> None:
        """Zero winding cluster is non-meron with positive fermion sign."""
        c = MeronCluster2D("c_neut", [(0, 0)], [], winding=(0, 0), meron_count=0)
        assert c.is_meron is False
        assert c.fermion_sign == 1

    def test_bound_dipole_cluster_properties(self) -> None:
        """Even meron count (dipole) with zero winding has positive sign."""
        c = MeronCluster2D("c_dipole", [(0, 0)], [], winding=(0, 0), meron_count=2)
        assert c.is_meron is False
        assert c.fermion_sign == 1

    def test_odd_meron_cluster_properties(self) -> None:
        """Odd winding cluster is meron with negative sign when sign_factor=1."""
        c = MeronCluster2D("c_meron", [(0, 0)], [], winding=(1, 0), meron_count=1)
        assert c.is_meron is True
        assert c.fermion_sign == -1

    def test_orientation_flip_involution_idempotency_and_sign_reversal(self) -> None:
        """Involution tau flips sign, preserves weight, and satisfies tau^2 = id."""
        c = MeronCluster2D("c1", [(0, 0)], [], winding=(0, 1), meron_count=1, weight=Fraction(7, 3))
        tau_c = c.orientation_flip()

        assert tau_c.is_meron is True
        assert tau_c.fermion_sign == -c.fermion_sign
        assert tau_c.weight == c.weight
        assert tau_c.winding == (0, -1)

        tau2_c = tau_c.orientation_flip()
        assert tau2_c.fermion_sign == c.fermion_sign
        assert tau2_c.winding == c.winding

    def test_rejects_float_weights(self) -> None:
        """Constructor rejects float weights fail-closed."""
        with pytest.raises(TypeError, match="Weight must be an exact fractions.Fraction"):
            MeronCluster2D("c_float", [], [], weight=1.5)




class TestGrossNeveu2DSolverCancellation:
    """Verifies exact pairwise cancellation on 2D ensembles and zero duality gap."""

    def test_canonical_ensemble_exact_cancellation(self) -> None:
        """Canonical 2D Gross-Neveu ensemble cancels odd sectors with zero duality gap."""
        ensemble = build_canonical_2d_gn_ensemble(4, 4)
        res = execute_2d_gn_cancellation(ensemble)

        assert res["status"] == "EXACT_REPAIR"
        assert res["duality_gap"] == Fraction(0, 1)
        assert res["pairs_cancelled"] == 2
        assert res["zero_meron_sum"] == Fraction(150, 1)
        assert res["total_partition_sum"] == Fraction(150, 1)
        assert res["zero_sectors_positive"] is True

    def test_hostile_asymmetric_weights_fail_closed(self) -> None:
        """When an odd doublet has asymmetric weights, solver detects non-zero duality gap."""
        c = MeronCluster2D("c_odd", [(0, 0)], [], winding=(1, 0), meron_count=1, weight=Fraction(10, 1))
        tau_c = c.orientation_flip()
        tau_c.weight = Fraction(11, 1)

        res = execute_2d_gn_cancellation([(c, c.weight), (tau_c, tau_c.weight)])
        assert res["status"] == "UNREPAIRED_OBSTRUCTION"
        assert res["duality_gap"] > Fraction(0, 1)
        assert res["pairs_cancelled"] == 0

    def test_hostile_sign_perturbation_fail_closed(self) -> None:
        """When two identical odd clusters are provided without opposite signs, cancellation fails."""
        c1 = MeronCluster2D("c1", [(0, 0)], [], winding=(1, 0), meron_count=1, weight=Fraction(5, 1), sign_factor=1)
        c2 = MeronCluster2D("c2", [(0, 0)], [], winding=(-1, 0), meron_count=1, weight=Fraction(5, 1), sign_factor=1)

        res = execute_2d_gn_cancellation([(c1, c1.weight), (c2, c2.weight)])
        assert res["status"] == "UNREPAIRED_OBSTRUCTION"
        assert res["duality_gap"] == Fraction(10, 1)
        assert res["pairs_cancelled"] == 0




class TestSymbolGameWireGrammar2DGN:
    """Verifies Gamma38 wire compliance, parsing, and semantic validation across all turns."""

    def test_all_wire_turns_pass_grammar_and_semantics(self) -> None:
        """Every input and expected response wire validates under validate_packet_semantics."""
        for turn in WIRE_TURNS_2D_GN:
            in_wire = turn["input_wire"]
            out_wire = turn["expected_response_wire"]

            assert all(c in GAMMA_38 for c in in_wire)
            assert all(c in GAMMA_38 for c in out_wire)

            pkt_in = parse_packet(in_wire)
            validate_packet_semantics(pkt_in)
            assert serialize_packet(pkt_in) == in_wire

            pkt_out = parse_packet(out_wire)
            validate_packet_semantics(pkt_out)
            assert serialize_packet(pkt_out) == out_wire

    def test_wire_validation_helper_behavior(self) -> None:
        """validate_wire_string accepts valid wires and rejects corrupted ones."""
        valid = "op<<1100><liftreq>>"
        assert validate_wire_string(valid) is True

        corrupted_char = "op<<1100><liftreq>>_INVALID"
        assert validate_wire_string(corrupted_char) is False

        malformed_syntax = "op<<1100><liftreq>"
        assert validate_wire_string(malformed_syntax) is False




class TestArtifactEmissionAndIntegrity:
    """Verifies DDC DAG causal structure, node schema, and master receipt SHA-256 digest."""

    def test_dag_trace_structure_and_causality(self, tmp_path: Path) -> None:
        """DAG file emits 6 nodes across turns 0-4 with strict parent causality."""
        dag_file = str(tmp_path / "test_dag.jsonl")
        canc_res = {
            "status": "EXACT_REPAIR",
            "duality_gap": Fraction(0, 1),
            "pairs_cancelled": 2,
            "total_partition_sum": Fraction(150, 1),
            "zero_sectors_positive": True,
        }
        nodes = emit_2d_gn_ddc_dag(dag_file, canc_res)
        assert len(nodes) == 6

        seen = set()
        for n in nodes:
            for p in n["parent_ids"]:
                assert p in seen, f"Parent {p} does not precede child {n['node_id']}"
            seen.add(n["node_id"])

            wire = n["gamma38_wire"]
            assert all(c in GAMMA_38 for c in wire)
            pkt = parse_packet(wire)
            validate_packet_semantics(pkt)

        assert nodes[-1]["action"] == "CERTIFY_EXACT_REPAIR"
        assert nodes[-1]["payload"]["status"] == "EXACT_REPAIR"
        assert nodes[-1]["payload"]["duality_gap"] == "0"

    def test_master_receipt_digest_recomputation(self, tmp_path: Path) -> None:
        """Master receipt contains verified SHA-256 digest matching body recomputation."""
        receipt_file = str(tmp_path / "test_receipt.json")
        canc_res = {
            "status": "EXACT_REPAIR",
            "duality_gap": Fraction(0, 1),
            "pairs_cancelled": 2,
            "zero_meron_sum": Fraction(150, 1),
            "odd_meron_residual": Fraction(0, 1),
            "total_partition_sum": Fraction(150, 1),
            "zero_sectors_positive": True,
        }
        receipt = generate_2d_gn_receipt(receipt_file, canc_res)
        assert os.path.exists(receipt_file)
        assert "sha256_digest" in receipt

        with open(receipt_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        embedded = data.pop("sha256_digest")
        ser = json.dumps(data, indent=2, sort_keys=True)
        recomp = hashlib.sha256(ser.encode("utf-8")).hexdigest()
        assert embedded == recomp




class TestZeroFloatsAndLexicalHygiene:
    """Verifies complete absence of float types and adherence to claim hygiene."""

    def test_source_code_has_zero_float_constants_or_calls(self) -> None:
        """AST static analysis confirms 0 float literals and 0 calls to float()."""
        src_path = DEMOS_DIR / "code" / "demo_2d_gross_neveu_meron.py"
        assert src_path.exists()
        tree = ast.parse(src_path.read_text(encoding="utf-8"))

        for node in ast.walk(tree):
            if isinstance(node, ast.Constant):
                assert type(node.value) is not float, f"Float literal found: {node.value}"
            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    assert node.func.id != "float", "Call to built-in float() found"

    def test_prompts_pass_lexical_hygiene(self) -> None:
        """Blind wire prompts pass lexical hygiene without leaking domain hints."""
        for turn in WIRE_TURNS_2D_GN:
            assert_lexical_hygiene(turn["wire_prompt"])

    def test_run_demo_function_completes_successfully(self) -> None:
        """End-to-end execution of run_demo returns 0 (success)."""
        ret = run_demo(live=False)
        assert ret == 0
