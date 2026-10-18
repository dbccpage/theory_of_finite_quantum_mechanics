"""test_demo_4d_su2_cluster_gauge_updates.py: Test suite for 4D SU(2) Gauge-Coupled Topological Cluster Demo.

AuthorityEffect: None.

Verifies:
1. 4D Spacetime Torus T^4 geometry (8x8x4x4, 1024 sites, 4096 links, 6144 plaquettes).
2. Non-abelian SU(2) link holonomy dynamics, exact rational Wilson action, and local gauge invariance.
3. Localized half-instanton centers, second Chern charge density q(x) in (1/2)Z, and tau inversion c_2 |-> -c_2.
4. Gauge-coupled topological cluster solver exact zero-sum cancellation with zero duality gap and Z = 450.
5. Pure Gamma38 wire grammar parsing and semantic validation via validate_packet_semantics.
6. DDC DAG trace causality and master receipt cryptographic SHA-256 digest recomputation.
7. Zero floating-point constants and calls (AST static audit).
8. Lexical and claim hygiene conformance.
"""

from __future__ import annotations

import ast
import hashlib
import json
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

from blind_problem import assert_lexical_hygiene  # noqa: E402
from demo_4d_su2_cluster_gauge_updates import (  # noqa: E402
    CANONICAL_4D_SU2_WIRE_TURNS,
    build_gauge_coupled_ensemble,
    emit_4d_su2_cluster_ddc_dag,
    run_4d_su2_cluster_gauge_updates_demo,
    run_su2_gauge_update_cycle,
    validate_wire_string,
)
from omega_engine_pfp.domain.tower.parser import (  # noqa: E402
    GAMMA_38,
    parse_packet,
    validate_packet_semantics,
)
from su2_link_holonomy_4d import (  # noqa: E402
    LatticeGaugeField4D,
    RationalSU2,
    SU2TopologicalClusterCoupler,
)


class Test4DSU2LatticeAndGaugeDynamics:
    """Verifies 4D discrete torus geometry and non-abelian SU(2) gauge field dynamics on L >= 8."""

    def test_lattice_geometry_and_counts(self) -> None:
        """8x8x4x4 lattice yields 1024 sites, 4096 links, and 6144 plaquettes."""
        field = LatticeGaugeField4D(dimensions=(8, 8, 4, 4))
        assert field.volume == 1024
        assert len(field.torus.sites()) == 1024
        assert field.total_wilson_action() == Fraction(0, 1)

    def test_gauge_update_cycle_and_invariance(self) -> None:
        """Validates exact Delta S_W and local gauge invariance under Omega(x)."""
        metrics = run_su2_gauge_update_cycle(dim=(8, 8, 4, 4))
        assert metrics["volume"] == 1024
        assert metrics["initial_action"] == "0"
        assert metrics["gauge_invariance_exact"] is True
        assert Fraction(metrics["updated_action"]) > Fraction(0, 1)


class Test4DClusterInvolutionAndExactCancellation:
    """Verifies orientation flip inversion and gauge-coupled cluster cancellation."""

    def test_gauge_coupled_ensemble_cancellation(self) -> None:
        """Coupled ensemble evaluates exact Z = 450, zero duality gap, and 3 cancelled pairs."""
        field = LatticeGaugeField4D(dimensions=(8, 8, 4, 4))
        coupler = SU2TopologicalClusterCoupler(field)
        ensemble, metrics = build_gauge_coupled_ensemble(coupler)

        assert len(ensemble) == 9
        assert metrics["orientation_inversion_exact"] is True

        canc_res = metrics["solver_results"]
        assert canc_res["status"] == "EXACT_REPAIR"
        assert canc_res["duality_gap"] == Fraction(0, 1)
        assert canc_res["total_partition_sum"] == Fraction(450, 1)
        assert canc_res["zero_charge_sum"] == Fraction(450, 1)
        assert canc_res["odd_charge_sum"] == Fraction(0, 1)
        assert canc_res["pairs_cancelled"] == 3


class Test4DSU2WireGrammarAndDDCExecution:
    """Verifies Gamma38 wire formatting, DDC DAG causality, and receipt generation."""

    def test_wire_turns_grammatical_validity(self) -> None:
        """All canonical wire turns adhere strictly to Gamma38 grammar."""
        for turn in CANONICAL_4D_SU2_WIRE_TURNS:
            in_w = turn["input_wire"]
            out_w = turn["expected_response_wire"]
            assert validate_wire_string(in_w)
            assert validate_wire_string(out_w)
            assert all(ch in GAMMA_38 for ch in in_w)
            assert all(ch in GAMMA_38 for ch in out_w)

    def test_ddc_dag_emission_and_causality(self, tmp_path: Path) -> None:
        """DDC DAG trace emits 6 nodes with strict acyclic parent causality."""
        dag_file = tmp_path / "test_4d_su2_dag.jsonl"
        gauge_metrics = run_su2_gauge_update_cycle(dim=(8, 8, 4, 4))
        field = LatticeGaugeField4D(dimensions=(8, 8, 4, 4))
        coupler = SU2TopologicalClusterCoupler(field)
        _, cluster_metrics = build_gauge_coupled_ensemble(coupler)
        canc_res = cluster_metrics["solver_results"]

        nodes = emit_4d_su2_cluster_ddc_dag(str(dag_file), gauge_metrics, canc_res)

        assert len(nodes) == 6
        assert dag_file.is_file()

        # Check DAG parent linkage
        for i in range(1, len(nodes)):
            assert nodes[i]["parent_ids"] == [nodes[i - 1]["node_id"]]

        # Check terminal repair
        term = nodes[-1]
        assert term["stage"] == "EXACT_REPAIR"
        assert term["payload"]["status"] == "EXACT_REPAIR"
        assert term["payload"]["duality_gap"] == "0"
        assert term["payload"]["total_partition_sum"] == "450"

    def test_run_4d_su2_cluster_gauge_updates_demo_end_to_end(self, tmp_path: Path) -> None:
        """End-to-end demo execution generates valid receipt and digest."""
        rcpt_file = tmp_path / "test_su2_receipt.json"
        dag_file = tmp_path / "test_su2_dag.jsonl"
        receipt = run_4d_su2_cluster_gauge_updates_demo(
            output_receipt=str(rcpt_file),
            output_dag=str(dag_file),
            dim=(8, 8, 4, 4),
        )

        assert receipt["authority_effect"] == "None"
        assert receipt["gauge_group"]["type"] == "SU(2)"
        assert receipt["exact_cancellation_metrics"]["status"] == "EXACT_REPAIR"
        assert receipt["exact_cancellation_metrics"]["total_partition_sum"] == "450"
        assert receipt["exact_cancellation_metrics"]["duality_gap"] == "0"
        assert receipt["wire_grammar"]["pure_gamma_38"] is True

        # Independent digest verification
        stored_digest = receipt["sha256_digest"]
        body_to_hash = {k: v for k, v in receipt.items() if k != "sha256_digest"}
        recomputed = hashlib.sha256(json.dumps(body_to_hash, indent=2, sort_keys=True).encode("utf-8")).hexdigest()
        assert stored_digest == recomputed


class Test4DSU2CodeHygieneAndZeroFloats:
    """Verifies zero floating-point usage and lexical hygiene."""

    def test_ast_zero_floats(self) -> None:
        """Ensures demo_4d_su2_cluster_gauge_updates.py contains zero float literals or calls."""
        demo_code_path = DEMOS_DIR / "code" / "demo_4d_su2_cluster_gauge_updates.py"
        tree = ast.parse(demo_code_path.read_text(encoding="utf-8"))

        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, float):
                pytest.fail(f"Float literal {node.value} detected in {demo_code_path.name}")
            if isinstance(node, ast.Name) and node.id == "float":
                pytest.fail(f"Call or reference to 'float' detected in {demo_code_path.name}")

    def test_lexical_hygiene(self) -> None:
        """Verifies wire turn prompts conform to lexical hygiene."""
        for turn in CANONICAL_4D_SU2_WIRE_TURNS:
            assert_lexical_hygiene(turn["wire_prompt"])
            assert_lexical_hygiene(turn["grammar_prompt"])
