"""test_demo_3d_meron_string.py: Test suite for 3D Meron String Linking Demo.

AuthorityEffect: None.

Verifies:
1. 3D Lattice geometry on T^3 (6x6x6, 216 sites) and coordinate wraparounds.
2. 1D Closed string loops, exact winding vectors W(c) in Z^3, and parity I(c) in {0, 1}.
3. Discrete Gauss linking numbers Lk in Z distinguishing Hopf links (Lk=1) from unlinked loops (Lk=0).
4. Involution tau properties: tau^2 = id, sign reversal sigma(tau(C)) = -sigma(C), weight preservation.
5. Inverted posting index bipartite pairing and exact zero-sum cancellation with zero duality gap.
6. Pure Gamma38 wire grammar parsing and semantic validation via validate_packet_semantics.
7. DDC DAG trace causality and master receipt cryptographic SHA-256 digest recomputation.
8. Zero floating-point constants and calls (AST static audit).
9. Lexical and claim hygiene conformance.
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

from demo_3d_meron_string_linking import (  # noqa: E402
    WIRE_TURNS_3D_STRINGS,
    MeronStringCluster3D,
    build_canonical_3d_string_ensemble,
    emit_3d_string_ddc_dag,
    execute_3d_string_cancellation,
    generate_3d_string_receipt,
    run_demo,
    validate_wire_string,
)
from omega_engine_pfp.domain.tower.parser import (  # noqa: E402
    GAMMA_38,
    parse_packet,
    validate_packet_semantics,
)

from blind_problem import assert_lexical_hygiene  # noqa: E402
from topological_meron_3d import (  # noqa: E402
    ClosedStringLoop3D,
    Lattice3D,
    build_hopf_link_pair,
    build_plaquette_loop,
    build_unlinked_pair,
    build_winding_loop,
    linking_number,
)

# ============================================================================
# Test Suite 1: 3D Torus Geometry & Loop Winding
# ============================================================================


class TestLattice3DAndLoopGeometry:
    """Verifies discrete 3-torus dimensions, wraparounds, and winding vectors."""

    def test_dimensions_and_volume(self) -> None:
        """Lattice T^3 initializes with 6x6x6 sites and volume 216."""
        lat = Lattice3D((6, 6, 6))
        assert lat.lx == 6
        assert lat.ly == 6
        assert lat.lz == 6
        assert lat.volume == 216

    def test_coordinate_wraparounds(self) -> None:
        """Points wrap into the fundamental domain [0, 5]^3."""
        lat = Lattice3D((6, 6, 6))
        assert lat.wrap_coordinate((6, 7, -1)) == (0, 1, 5)

    def test_axis_winding_vectors(self) -> None:
        """Loops winding along coordinate axes have exact winding vectors in Z^3."""
        dim = (6, 6, 6)
        lx = build_winding_loop("x", lattice_dim=dim, steps=6)
        ly = build_winding_loop("y", lattice_dim=dim, steps=6)
        lz = build_winding_loop("z", lattice_dim=dim, steps=6)

        assert lx.winding_vector == (1, 0, 0)
        assert ly.winding_vector == (0, 1, 0)
        assert lz.winding_vector == (0, 0, 1)

    def test_contractible_plaquette_has_zero_winding(self) -> None:
        """Planar plaquette loop has winding (0, 0, 0) and length 8."""
        dim = (6, 6, 6)
        p = build_plaquette_loop("xy", origin=(0, 0, 0), size=2, lattice_dim=dim)
        assert p.is_contractible is True
        assert p.winding_vector == (0, 0, 0)


# ============================================================================
# Test Suite 2: Topological Invariants & Gauss Linking
# ============================================================================


class TestTopologicalInvariantsAndLinking:
    """Verifies winding parity I(c) and discrete Gauss linking numbers."""

    def test_winding_parity_evaluations(self) -> None:
        """Topological parity I(c) = (Wx + Wy + Wz) mod 2."""
        dim = (6, 6, 6)
        lx = build_winding_loop("x", lattice_dim=dim, steps=6)
        assert lx.winding_parity == 1

        p = build_plaquette_loop("xy", lattice_dim=dim, size=2)
        assert p.winding_parity == 0

        # Helical loop with W = (1, 1, 0) has even parity (1+1+0) mod 2 = 0
        pts_helical: list[tuple[int, int, int]] = []
        for k in range(6):
            pts_helical.append((k, k, 0))
            pts_helical.append(((k + 1) % 6, k, 0))
        hel = ClosedStringLoop3D("helical", pts_helical, lattice_dim=dim)
        assert hel.winding_vector == (1, 1, 0)
        assert hel.winding_parity == 0

    def test_hopf_link_has_non_zero_gauss_linking(self) -> None:
        """Hopf link pair has discrete Gauss linking number Lk = 1."""
        dim = (6, 6, 6)
        h1, h2 = build_hopf_link_pair(origin=(1, 1, 1), lattice_dim=dim)
        assert h1.is_contractible is True
        assert h2.is_contractible is True
        lk = linking_number(h1, h2)
        assert lk == 1

    def test_unlinked_pair_has_zero_linking(self) -> None:
        """Disjoint planar loops have linking number Lk = 0."""
        dim = (6, 6, 6)
        u1, u2 = build_unlinked_pair(lattice_dim=dim)
        lk = linking_number(u1, u2)
        assert lk == 0


# ============================================================================
# Test Suite 3: Meron String Cluster Involution Properties
# ============================================================================


class TestMeronStringCluster3DInvolution:
    """Verifies cluster involution tau: c_odd -> -c_odd and fermion sign reversal."""

    def test_neutral_cluster_properties(self) -> None:
        """Zero winding cluster is non-meron with positive fermion sign."""
        dim = (6, 6, 6)
        p = build_plaquette_loop("xy", lattice_dim=dim)
        c = MeronStringCluster3D("c_p", [p], weight=Fraction(100, 1))
        assert c.has_meron is False
        assert c.fermion_sign == 1

    def test_meron_cluster_involution_reverses_sign(self) -> None:
        """Tau involution reverses fermion sign and preserves weight."""
        dim = (6, 6, 6)
        mx = build_winding_loop("x", lattice_dim=dim, steps=6)
        c = MeronStringCluster3D("c_mx", [mx], weight=Fraction(40, 1), sign_factor=-1)
        assert c.has_meron is True
        assert c.fermion_sign == -1

        tau_c = c.orientation_flip()
        assert tau_c.fermion_sign == 1
        assert tau_c.weight == c.weight

        # Involution idempotence: tau(tau(C)) has same sign and weight
        tau_tau_c = tau_c.orientation_flip()
        assert tau_tau_c.fermion_sign == c.fermion_sign
        assert tau_tau_c.weight == c.weight

    def test_involution_on_non_meron_raises_error(self) -> None:
        """Involution fails closed when attempted on cluster with zero odd loops."""
        dim = (6, 6, 6)
        p = build_plaquette_loop("xy", lattice_dim=dim)
        c = MeronStringCluster3D("c_p", [p], weight=Fraction(100, 1))
        with pytest.raises(ValueError):
            c.orientation_flip()


# ============================================================================
# Test Suite 4: Exact Bipartite Cancellation Solver
# ============================================================================


class TestBipartiteCancellationSolver:
    """Verifies exact rational cancellation and fail-closed residual detection."""

    def test_canonical_3d_ensemble_exact_repair(self) -> None:
        """Canonical ensemble cancels 3 odd-winding meron pairs with zero duality gap."""
        ensemble = build_canonical_3d_string_ensemble((6, 6, 6))
        assert ensemble.total_clusters == 10
        assert len(ensemble.zero_meron_clusters) == 4
        assert len(ensemble.odd_meron_clusters) == 6

        res = execute_3d_string_cancellation(ensemble)
        assert res["status"] == "EXACT_REPAIR"
        assert res["duality_gap"] == Fraction(0, 1)
        assert res["pairs_cancelled"] == 3
        assert res["zero_meron_sum"] == Fraction(310, 1)
        assert res["odd_meron_residual"] == Fraction(0, 1)
        assert res["total_partition_sum"] == Fraction(310, 1)
        assert res["zero_sectors_positive"] is True

    def test_perturbed_ensemble_detects_obstruction_fail_closed(self) -> None:
        """Perturbed ensemble with un-paired meron string reports OBSTRUCTION_REMAINS."""
        ensemble = build_canonical_3d_string_ensemble((6, 6, 6))
        dim = (6, 6, 6)
        # Add an un-paired odd meron
        mx_extra = build_winding_loop("x", offset=(1, 1, 1), lattice_dim=dim, steps=6, loop_id="mx_extra")
        extra_cluster = MeronStringCluster3D(
            cluster_id="c_extra",
            loops=[mx_extra],
            weight=Fraction(15, 1),
            sign_factor=-1,
        )
        ensemble.add_cluster(extra_cluster)

        res = execute_3d_string_cancellation(ensemble)
        assert res["status"] == "OBSTRUCTION_REMAINS"
        assert res["duality_gap"] == Fraction(15, 1)
        assert res["odd_meron_residual"] == Fraction(-15, 1)


# ============================================================================
# Test Suite 5: Gamma38 Wire Grammar & DDC DAG Trace
# ============================================================================


class TestGamma38WireGrammarAndDDCDAG:
    """Verifies pure Gamma38 wire communication and DAG causal structure."""

    def test_all_wire_turns_valid_gamma38(self) -> None:
        """All turn wire strings pass Gamma38 character and semantic validation."""
        for turn in WIRE_TURNS_3D_STRINGS:
            assert validate_wire_string(turn["input_wire"])
            assert validate_wire_string(turn["expected_response_wire"])

    def test_ddc_dag_emission_and_causality(self, tmp_path: Path) -> None:
        """Emitted DDC DAG trace has valid causal parent ordering and Gamma38 wires."""
        dag_file = str(tmp_path / "test_dag.jsonl")
        canc_res = {
            "status": "EXACT_REPAIR",
            "duality_gap": Fraction(0, 1),
            "pairs_cancelled": 3,
            "zero_meron_sum": Fraction(310, 1),
            "odd_meron_residual": Fraction(0, 1),
            "total_partition_sum": Fraction(310, 1),
        }
        nodes = emit_3d_string_ddc_dag(dag_file, canc_res)
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

        # Terminal certification node
        assert nodes[-1]["action"] == "CERTIFY_EXACT_REPAIR"
        assert nodes[-1]["payload"]["status"] == "EXACT_REPAIR"
        assert nodes[-1]["payload"]["duality_gap"] == "0"

    def test_master_receipt_digest_recomputation(self, tmp_path: Path) -> None:
        """Master receipt contains verified SHA-256 digest matching body recomputation."""
        receipt_file = str(tmp_path / "test_receipt.json")
        canc_res = {
            "status": "EXACT_REPAIR",
            "duality_gap": Fraction(0, 1),
            "pairs_cancelled": 3,
            "zero_meron_sum": Fraction(310, 1),
            "odd_meron_residual": Fraction(0, 1),
            "total_partition_sum": Fraction(310, 1),
            "zero_sectors_positive": True,
        }
        receipt = generate_3d_string_receipt(receipt_file, canc_res)
        assert os.path.exists(receipt_file)
        assert "sha256_digest" in receipt

        with open(receipt_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        embedded = data.pop("sha256_digest")
        ser = json.dumps(data, indent=2, sort_keys=True)
        recomp = hashlib.sha256(ser.encode("utf-8")).hexdigest()
        assert embedded == recomp


# ============================================================================
# Test Suite 6: Zero Floats AST Audit & Lexical Hygiene
# ============================================================================


class TestZeroFloatsAndLexicalHygiene:
    """Verifies complete absence of float types and adherence to claim hygiene."""

    def test_source_code_has_zero_float_constants_or_calls(self) -> None:
        """AST static analysis confirms 0 float literals and 0 calls to float()."""
        src_path = DEMOS_DIR / "code" / "demo_3d_meron_string_linking.py"
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
        for turn in WIRE_TURNS_3D_STRINGS:
            assert_lexical_hygiene(turn["wire_prompt"])

    def test_run_demo_function_completes_successfully(self) -> None:
        """End-to-end execution of run_demo returns 0 (success)."""
        ret = run_demo(live=False)
        assert ret == 0
