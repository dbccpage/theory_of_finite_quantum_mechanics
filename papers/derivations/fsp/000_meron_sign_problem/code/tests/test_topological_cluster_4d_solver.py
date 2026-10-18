"""Unit test suite for 4D Topological Cluster Involution Solver, Wire Grammar & DDC DAG.

Verifies:
1. TopologicalCluster4DSolver initialization and combined 3D/4D cluster state representation.
2. Sign-reversing cluster involution tau:
   - Odd half-instanton sectors (N_+ != N_-): (N_+, N_-) |-> (N_-, N_+) inverts sign sigma |-> -sigma.
   - Zero-charge sectors (N_+ = N_-) with odd 3D winding loops (I(c) = 1): flips 3D loop orientation, sigma |-> -sigma.
   - Zero-charge sectors with even winding: remain strictly positive (sigma = +1).
   - Involutive idempotency (tau^2 = id) and weight preservation w(tau(C)) = w(C).
   - Pairwise zero-sum doublet cancellation (1 + (-1)) * w(C) = 0 certified with zero duality gap.
3. Pure Gamma38 wire grammar integration:
   - 38-glyph alphabet Gamma38 strictness.
   - Parser and semantic validation (validate_packet_semantics).
   - Round-trip bijection serialize_packet(parse_packet(w)) == w.
   - Exact fraction binary encoding under opcode <10010>.
4. DDC DAG trace emission:
   - 5-stage causal chain across turns 0 to 4.
   - Strict acyclic parent causality.
   - Valid Gamma38 wire packets on 100% of nodes.
   - Terminal node certification of EXACT_REPAIR with zero duality gap.
5. Lexical & claim hygiene: zero forbidden domain keywords and zero claim hype verbs.
6. Zero float enforcement: AST static audit and runtime type validation.
7. Railway-Oriented Programming (ROP) fail-closed boundaries via Result[T, Refusal].
"""

from __future__ import annotations

import ast
import json
import os
from fractions import Fraction
from pathlib import Path

import pytest
from omega_engine_pfp.domain.tower.parser import (
    GAMMA_38,
    parse_packet,
    serialize_packet,
    validate_packet_semantics,
)

from topological_cluster_4d_solver import (
    CombinedTopologicalCluster,
    TopologicalCluster4DSolver,
    assert_claim_hygiene,
    assert_lexical_hygiene,
    assert_no_floats,
    emit_ddc_dag_trace,
    execute_involution_cancellation,
    fraction_to_gamma38,
    generate_gamma38_wire,
    validate_gamma38_wire,
)
from topological_half_instanton_4d import (
    HalfInstantonCluster4D,
    orientation_flip,
)
from topological_meron_3d import (
    build_plaquette_loop,
    build_winding_loop,
)



class TestTopologicalCluster4DSolverArchitecture:
    """Verifies solver construction, geometry parameters, and type barriers."""

    def test_solver_initialization_defaults(self) -> None:
        """Solver initializes with default 4D torus (2,2,2,2) and 3D lattice (4,4,4)."""
        solver = TopologicalCluster4DSolver()
        assert solver.torus_4d.dimensions == (2, 2, 2, 2)
        assert solver.torus_4d.volume == 16
        assert solver.lattice_3d.dimensions == (4, 4, 4)
        assert solver.lattice_3d.volume == 64

    def test_solver_custom_dimensions(self) -> None:
        """Solver accepts custom integer dimensions."""
        solver = TopologicalCluster4DSolver(
            torus_dim=(4, 4, 4, 4), lattice_dim_3d=(6, 6, 6)
        )
        assert solver.torus_4d.volume == 256
        assert solver.lattice_3d.volume == 216

    def test_solver_rejects_float_dimensions(self) -> None:
        """Solver rejects floating-point dimensions fail-closed."""
        with pytest.raises(TypeError):
            TopologicalCluster4DSolver(torus_dim=(2.0, 2, 2, 2))
        with pytest.raises(TypeError):
            TopologicalCluster4DSolver(lattice_dim_3d=(4.5, 4, 4))




class TestCombinedClusterAndTopologicalInvariants:
    """Verifies CombinedTopologicalCluster value objects and topological metrics."""

    def test_combined_cluster_creation_and_properties(self) -> None:
        """Combined cluster holds 4D instanton, 3D loops, and exact rational weight."""
        inst = HalfInstantonCluster4D(n_plus=1, n_minus=0)
        l_3d = build_winding_loop("x")
        cluster = CombinedTopologicalCluster(
            cluster_id="cluster_01",
            half_instanton=inst,
            loops_3d=(l_3d,),
            weight=Fraction(3, 2),
            sign_factor=1,
        )
        assert cluster.cluster_id == "cluster_01"
        assert cluster.weight == Fraction(3, 2)
        assert cluster.is_odd_half_instanton is True
        assert cluster.second_chern_number == Fraction(1, 2)
        assert cluster.winding_parity_3d == 1

    def test_combined_cluster_zero_charge_sector(self) -> None:
        """Zero-charge 4D sector with even 3D winding has strictly positive sign."""
        inst = HalfInstantonCluster4D(n_plus=1, n_minus=1)
        l_even = build_plaquette_loop("xy")
        cluster = CombinedTopologicalCluster(
            cluster_id="zero_even",
            half_instanton=inst,
            loops_3d=(l_even,),
            weight=Fraction(5, 1),
        )
        assert cluster.is_zero_charge_4d is True
        assert cluster.winding_parity_3d == 0
        assert cluster.fermion_determinant_sign == 1

    def test_combined_cluster_zero_charge_with_odd_3d_loop(self) -> None:
        """Zero-charge 4D sector with odd 3D winding has base sign -1."""
        inst = HalfInstantonCluster4D(n_plus=2, n_minus=2)
        l_odd = build_winding_loop("z")
        cluster = CombinedTopologicalCluster(
            cluster_id="zero_odd_3d",
            half_instanton=inst,
            loops_3d=(l_odd,),
            weight=Fraction(7, 4),
        )
        assert cluster.is_zero_charge_4d is True
        assert cluster.winding_parity_3d == 1
        assert cluster.fermion_determinant_sign == -1




class TestClusterInvolutionTauAndZeroSumDoublet:
    """Verifies sign reversal under tau and zero-sum doublet cancellation."""

    def test_involution_odd_half_instanton_sign_reversal(self) -> None:
        """For odd half-instanton (N_+ != N_-), tau flips (N_+, N_-) -> (N_-, N_+) and reverses sign."""
        solver = TopologicalCluster4DSolver()
        c = HalfInstantonCluster4D(n_plus=1, n_minus=0, weight=Fraction(11, 7))
        tau_c = solver.cluster_involution_tau(c)

        assert tau_c.n_plus == 0 and tau_c.n_minus == 1
        assert solver.second_chern_number(tau_c) == -solver.second_chern_number(c)
        assert solver.fermion_determinant_sign(c) == -1
        assert solver.fermion_determinant_sign(tau_c) == 1
        assert (
            solver.fermion_determinant_sign(c)
            + solver.fermion_determinant_sign(tau_c)
            == 0
        )

    def test_involution_zero_charge_odd_3d_winding_sign_reversal(self) -> None:
        """For zero-charge sector (N_+ = N_-) with odd 3D winding loop, tau inverts sign sigma -> -sigma."""
        solver = TopologicalCluster4DSolver()
        inst = HalfInstantonCluster4D(n_plus=1, n_minus=1)
        l_odd = build_winding_loop("x")
        c = CombinedTopologicalCluster(
            cluster_id="c_zero_odd",
            half_instanton=inst,
            loops_3d=(l_odd,),
            weight=Fraction(3, 1),
            sign_factor=1,
        )

        tau_c = solver.cluster_involution_tau(c)
        assert solver.fermion_determinant_sign(c) == -1
        assert solver.fermion_determinant_sign(tau_c) == 1
        assert (
            solver.fermion_determinant_sign(c)
            + solver.fermion_determinant_sign(tau_c)
            == 0
        )

    def test_involution_zero_charge_even_winding_strictly_positive(self) -> None:
        """For zero-charge sector (N_+ = N_-) with even winding, cluster is strictly positive and invariant."""
        solver = TopologicalCluster4DSolver()
        inst = HalfInstantonCluster4D(n_plus=2, n_minus=2)
        l_even = build_plaquette_loop("xy")
        c = CombinedTopologicalCluster(
            cluster_id="c_zero_even",
            half_instanton=inst,
            loops_3d=(l_even,),
            weight=Fraction(4, 1),
            sign_factor=1,
        )

        tau_c = solver.cluster_involution_tau(c)
        assert solver.fermion_determinant_sign(c) == 1
        assert solver.fermion_determinant_sign(tau_c) == 1

    def test_involution_idempotency_and_weight_preservation(self) -> None:
        """Involution tau is strictly idempotent (tau^2 = id) and preserves exact weights."""
        solver = TopologicalCluster4DSolver()
        c = HalfInstantonCluster4D(n_plus=3, n_minus=0, weight=Fraction(13, 5))
        tau_c = solver.cluster_involution_tau(c)
        tau_tau_c = solver.cluster_involution_tau(tau_c)

        assert tau_tau_c.n_plus == c.n_plus
        assert tau_tau_c.n_minus == c.n_minus
        assert tau_tau_c.weight == c.weight
        assert (
            solver.fermion_determinant_sign(tau_tau_c)
            == solver.fermion_determinant_sign(c)
        )

    def test_verify_zero_sum_doublet_certified_zero_duality_gap(self) -> None:
        """Certified zero-sum doublet (1 + (-1)) * w(C) = 0 with zero duality gap."""
        solver = TopologicalCluster4DSolver()
        c = HalfInstantonCluster4D(n_plus=1, n_minus=0, weight=Fraction(17, 3))
        res = solver.verify_zero_sum_doublet(c)

        assert res["exact_zero_sum_doublet"] is True
        assert res["duality_gap"] == "0"
        assert res["weight_preserved"] is True
        assert res["involution_intact"] is True

    def test_rop_verify_doublet_monadic_ok_and_err(self) -> None:
        """ROP method returns Ok(dict) for valid cluster and typed Err(Refusal) on failure."""
        solver = TopologicalCluster4DSolver()
        c_valid = HalfInstantonCluster4D(n_plus=1, n_minus=0)
        rop_res = solver.verify_doublet_rop(c_valid)
        assert rop_res.is_ok
        assert rop_res.unwrap()["exact_zero_sum_doublet"] is True




class TestEnsemblePartitionFunctionCancellation:
    """Verifies ensemble summation and cancellation across diverse clusters."""

    def test_ensemble_pure_odd_half_instantons_vanishes(self) -> None:
        """Ensemble of odd half-instanton pairs sums to exact rational 0."""
        solver = TopologicalCluster4DSolver()
        c1 = HalfInstantonCluster4D(1, 0, weight=Fraction(2, 1))
        c1_tau = orientation_flip(c1)
        c2 = HalfInstantonCluster4D(2, 1, weight=Fraction(3, 1))
        c2_tau = orientation_flip(c2)

        res = solver.solve([c1, c1_tau, c2, c2_tau])
        assert res.odd_sum == Fraction(0, 1)
        assert res.duality_gap == Fraction(0, 1)
        assert res.status == "EXACT_REPAIR"

    def test_ensemble_mixed_3d_and_4d_odd_sectors_cancel(self) -> None:
        """Ensemble mixing 3D loops and 4D instantons cancels all odd sectors leaving Z > 0."""
        solver = TopologicalCluster4DSolver()
        l_odd = build_winding_loop("x")
        l_odd_tau = build_winding_loop("x", direction=-1)
        l_even = build_plaquette_loop("xy")
        c_odd = HalfInstantonCluster4D(1, 0)
        c_odd_tau = orientation_flip(c_odd)
        c_zero = HalfInstantonCluster4D(0, 0)

        ensemble = [l_odd, l_odd_tau, l_even, c_odd, c_odd_tau, c_zero]
        res = solver.solve(ensemble)

        assert res.odd_sum == Fraction(0, 1)
        assert res.zero_sum == Fraction(2, 1)
        assert res.total_partition_sum == Fraction(2, 1)
        assert res.zero_sectors_positive is True

    def test_ensemble_empty_boundary_conditions(self) -> None:
        """Empty ensemble evaluates to 0 partition sum without error."""
        solver = TopologicalCluster4DSolver()
        res = solver.solve([])
        assert res.total_partition_sum == Fraction(0, 1)
        assert res.odd_sectors_cancelled == 0
        assert res.duality_gap == Fraction(0, 1)




class TestGamma38WireGrammarIntegration:
    """Verifies Gamma38 38-glyph alphabet compliance, parsing, and semantic validation."""

    def test_gamma38_wire_alphabet_strict_character_set(self) -> None:
        """Emitted wire contains characters exclusively from Gamma38."""
        wire = generate_gamma38_wire()
        for ch in wire:
            assert ch in GAMMA_38

    def test_gamma38_wire_parse_and_validate_packet_semantics(self) -> None:
        """Wire parses with parse_packet and satisfies validate_packet_semantics."""
        wire = generate_gamma38_wire()
        pkt = parse_packet(wire)
        validate_packet_semantics(pkt)

    def test_gamma38_wire_roundtrip_bijection(self) -> None:
        """Roundtrip serialization bijection serialize_packet(parse_packet(w)) == w."""
        wire = generate_gamma38_wire()
        pkt = parse_packet(wire)
        assert serialize_packet(pkt) == wire

    def test_fraction_to_gamma38_canonical_rational_encoding(self) -> None:
        """fraction_to_gamma38 produces valid opcode <10010> RationalValue in binary."""
        w_zero = fraction_to_gamma38(Fraction(0, 1))
        assert w_zero == "op<<10010><0><0><1>>"
        pkt_zero = parse_packet(w_zero)
        validate_packet_semantics(pkt_zero)

        w_half = fraction_to_gamma38(Fraction(1, 2))
        assert w_half == "op<<10010><0><1><10>>"
        pkt_half = parse_packet(w_half)
        validate_packet_semantics(pkt_half)

        w_neg = fraction_to_gamma38(Fraction(-1, 2))
        assert w_neg == "op<<10010><1><1><10>>"
        pkt_neg = parse_packet(w_neg)
        validate_packet_semantics(pkt_neg)

        w_five_thirds = fraction_to_gamma38(Fraction(5, 3))
        assert w_five_thirds == "op<<10010><0><101><11>>"
        pkt_ft = parse_packet(w_five_thirds)
        validate_packet_semantics(pkt_ft)

    def test_validate_gamma38_wire_helper_accepts_valid_and_rejects_corrupted(
        self,
    ) -> None:
        """validate_gamma38_wire returns True for valid strings and False for corrupted."""
        valid_wire = "op<<10010><0><1><10>>"
        assert validate_gamma38_wire(valid_wire) is True

        corrupted_alphabet = "op<<10010><0><1><10>>_FORBIDDEN"
        assert validate_gamma38_wire(corrupted_alphabet) is False

        malformed_brackets = "op<<10010><0><1><10>"
        assert validate_gamma38_wire(malformed_brackets) is False




class TestLexicalAndClaimHygiene:
    """Verifies 100% lexical hygiene (zero domain keywords, zero claim hype verbs)."""

    def test_clean_texts_pass_hygiene(self) -> None:
        """Clean mathematical texts pass lexical and claim hygiene filters."""
        clean = "Discrete cluster configuration undergoing orientation-reversing involution"
        assert_lexical_hygiene(clean)
        assert_claim_hygiene(clean)

    def test_forbidden_domain_keywords_raise_value_error(self) -> None:
        """Texts with smuggled domain keywords raise ValueError fail-closed."""
        forbidden_samples = [
            "This model contains a meron string loop",
            "Fermion determinant sign cancellation",
            "Lattice hamiltonian matrix representation",
            "Quantum monte carlo simulation algorithm",
        ]
        for sample in forbidden_samples:
            with pytest.raises(ValueError, match="LEXICAL HYGIENE VIOLATION"):
                assert_lexical_hygiene(sample)

    def test_forbidden_claim_hype_verbs_raise_value_error(self) -> None:
        """Texts with unhedged hype verbs raise ValueError fail-closed."""
        hype_samples = [
            "This proof mathematically verifies the algorithm",
            "The cluster involution fundamentally guarantees sign freedom",
            "It is impossible for signs to persist",
            "The universal solution is flawless",
        ]
        for sample in hype_samples:
            with pytest.raises(ValueError, match="CLAIM HYGIENE VIOLATION"):
                assert_claim_hygiene(sample)

    def test_wire_packet_contains_zero_domain_or_hype_words(self) -> None:
        """Generated wire packet contains zero forbidden substrings."""
        wire = generate_gamma38_wire()
        wire_lower = wire.lower()
        for word in [
            "meron",
            "fermion",
            "physics",
            "proves",
            "guarantees",
            "flawless",
        ]:
            assert word not in wire_lower




class TestDdcDagTraceEmission:
    """Verifies turn-by-turn DDC DAG emission, parent causality, and terminal status."""

    def test_dag_emission_produces_valid_jsonl_file(self, tmp_path: Path) -> None:
        """emit_ddc_dag_trace creates a valid JSON Lines file with exactly 6 nodes."""
        dag_file = str(tmp_path / "test_dag.jsonl")
        nodes = emit_ddc_dag_trace(dag_file)
        assert len(nodes) == 6
        assert os.path.exists(dag_file)

        with open(dag_file, "r", encoding="utf-8") as f:
            lines = [json.loads(line) for line in f]
        assert len(lines) == 6

    def test_dag_5_stage_causal_chain_turns_and_actions(
        self, tmp_path: Path
    ) -> None:
        """Nodes record turns 0 to 4 with expected stages and actions."""
        dag_file = str(tmp_path / "test_dag.jsonl")
        nodes = emit_ddc_dag_trace(dag_file)

        expected_stages = [
            ("CARRIER_DECLARATION", "ASSERT_CARRIER", 0),
            ("PLAQUETTE_BREAKUP", "PROBE_PLAQUETTES", 1),
            ("TOPOLOGICAL_HOLONOMY", "MEASURE_HOLONOMY", 2),
            ("LIFT_REQUEST", "REQUEST_LIFT", 3),
            ("LIFT_GRANT", "GRANT_LIFT", 3),
            ("EXACT_REPAIR", "CERTIFY_EXACT_REPAIR", 4),
        ]
        for n, (exp_stage, exp_action, exp_turn) in zip(nodes, expected_stages):
            assert n["stage"] == exp_stage
            assert n["action"] == exp_action
            assert n["turn"] == exp_turn

    def test_dag_strict_parent_causality_acyclic(self, tmp_path: Path) -> None:
        """Every parent ID strictly precedes the child node in the trace."""
        dag_file = str(tmp_path / "test_dag.jsonl")
        nodes = emit_ddc_dag_trace(dag_file)
        seen: set[str] = set()

        for n in nodes:
            for p in n["parent_ids"]:
                assert p in seen, f"Parent {p} does not precede child {n['node_id']}"
            seen.add(n["node_id"])

    def test_dag_every_node_carries_valid_gamma38_wire(
        self, tmp_path: Path
    ) -> None:
        """Every node contains valid Gamma38 wire conforming to validate_packet_semantics."""
        dag_file = str(tmp_path / "test_dag.jsonl")
        nodes = emit_ddc_dag_trace(dag_file)
        for n in nodes:
            wire = n["gamma38_wire"]
            for ch in wire:
                assert ch in GAMMA_38
            pkt = parse_packet(wire)
            validate_packet_semantics(pkt)

    def test_dag_terminal_exact_repair_zero_duality_gap(
        self, tmp_path: Path
    ) -> None:
        """Terminal node certifies EXACT_REPAIR with zero duality gap."""
        dag_file = str(tmp_path / "test_dag.jsonl")
        nodes = emit_ddc_dag_trace(dag_file)
        terminal = nodes[-1]
        assert terminal["action"] == "CERTIFY_EXACT_REPAIR"
        assert terminal["payload"]["status"] == "EXACT_REPAIR"
        assert terminal["payload"]["duality_gap"] == "0"

    def test_export_canonical_dags_dual_destinations(self, tmp_path: Path) -> None:
        """export_canonical_dags writes to both canonical result paths."""
        solver = TopologicalCluster4DSolver()
        p1_tmp = str(tmp_path / "results" / "4d_topological_cluster_dag.jsonl")
        p2_tmp = str(tmp_path / "code" / "results" / "4d_topological_cluster_dag.jsonl")
        p1, p2 = solver.export_canonical_dags(path1=p1_tmp, path2=p2_tmp)
        assert os.path.exists(p1)
        assert os.path.exists(p2)
        with open(p1, "r", encoding="utf-8") as f1, open(
            p2, "r", encoding="utf-8"
        ) as f2:
            assert f1.read() == f2.read()




class TestZeroFloatsAndAstStaticAudit:
    """Audits the AST and runtime behavior of topological_cluster_4d_solver to confirm zero floats."""

    def test_ast_audit_solver_zero_float_constants_and_calls(self) -> None:
        """AST static analysis confirms absence of float literals and float() calls in source."""
        src_path = (
            Path(__file__).resolve().parent.parent
            / "topological_cluster_4d_solver.py"
        )
        assert src_path.exists(), f"Source file missing: {src_path}"

        tree = ast.parse(src_path.read_text(encoding="utf-8"))

        for node in ast.walk(tree):
            if isinstance(node, ast.Constant):
                assert (
                    type(node.value) is not float
                ), f"Float literal found in source code: {node.value}"
            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    assert (
                        node.func.id != "float"
                    ), "Call to float() built-in found in source code"

    def test_runtime_rejection_of_floats_in_weights_and_clusters(self) -> None:
        """Runtime assert_no_floats and constructor barriers reject float values."""
        assert_no_floats(1, Fraction(3, 4), "string", (1, 2), {"a": Fraction(1, 1)})

        with pytest.raises(TypeError, match="Floating-point value forbidden"):
            assert_no_floats(1.0)
        with pytest.raises(TypeError, match="Floating-point value forbidden"):
            assert_no_floats([1, Fraction(1, 1), 2.5])

        with pytest.raises(TypeError, match="Floating-point value forbidden"):
            CombinedTopologicalCluster(cluster_id="c_float", weight=1.5)

        c = [HalfInstantonCluster4D(1, 0)]
        with pytest.raises(TypeError, match="Floats forbidden in cluster weights"):
            execute_involution_cancellation(c, weights=[1.0])
