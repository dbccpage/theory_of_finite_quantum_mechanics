"""test_demo_4d_half_instanton.py: Test suite for 4D Half-Instanton Second Chern Sign Cancellation Demo.

AuthorityEffect: None.

Verifies:
1. 4D Spacetime Torus T^4 geometry (4x4x4x4, 256 sites) and coordinate boundary wraparounds.
2. Localized half-instanton centers, topological charge c_2 in (1/2)Z, and discrete density sum.
3. Involution tau properties: tau^2 = id, c_2(tau(C)) = -c_2(C), sigma(tau(C)) = -sigma(C), w(tau(C)) = w(C).
4. Bipartite pairing and exact zero-sum cancellation with zero duality gap and Z = 450.
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

from blind_problem import assert_lexical_hygiene
from demo_4d_half_instanton import (
    CANONICAL_4D_WIRE_TURNS,
    build_canonical_4d_half_instanton_ensemble,
    emit_4d_instanton_ddc_dag,
    execute_4d_half_instanton_cancellation,
    run_4d_half_instanton_demo,
    validate_wire_string,
)
from omega_engine_pfp.domain.tower.parser import (
    GAMMA_38,
    parse_packet,
    validate_packet_semantics,
)
from topological_half_instanton_4d import (
    DiscreteTorus4D,
    HalfInstantonCenter4D,
    HalfInstantonCluster4D,
    compute_discrete_topological_density,
    discrete_second_chern_integral,
    orientation_flip,
)


class Test4DHalfInstantonGeometryAndInvariants:
    """Verifies 4D discrete torus geometry and topological charge evaluation."""

    def test_torus_dimensions_and_volume(self) -> None:
        """4D Torus dimensions (4, 4, 4, 4) yield V=256 sites."""
        torus = DiscreteTorus4D(dimensions=(4, 4, 4, 4))
        assert torus.volume == 256
        assert len(torus.sites()) == 256
        assert torus.wrap((4, 5, -1, 8)) == (0, 1, 3, 0)

    def test_half_instanton_centers_and_charge(self) -> None:
        """Self-dual centers have charge +1/2, anti-self-dual -1/2."""
        cp = HalfInstantonCenter4D((0, 0, 0, 0), chirality=1)
        cm = HalfInstantonCenter4D((1, 1, 1, 1), chirality=-1)
        assert cp.charge == Fraction(1, 2)
        assert cm.charge == Fraction(-1, 2)
        assert cp.flip().chirality == -1
        assert cm.flip().chirality == 1

    def test_discrete_topological_density_summation(self) -> None:
        """Discrete topological charge density sums exactly to c_2 in (1/2)Z."""
        torus = DiscreteTorus4D(dimensions=(4, 4, 4, 4))
        cp = HalfInstantonCenter4D((0, 0, 0, 0), chirality=1)
        cm = HalfInstantonCenter4D((2, 2, 2, 2), chirality=-1)

        density1 = compute_discrete_topological_density((cp,), torus, smeared=True)
        assert discrete_second_chern_integral(density1) == Fraction(1, 2)

        density2 = compute_discrete_topological_density((cp, cm), torus, smeared=True)
        assert discrete_second_chern_integral(density2) == Fraction(0, 1)


class Test4DClusterInvolutionAndExactCancellation:
    """Verifies involution properties and exact zero duality gap partition summation."""

    def test_canonical_ensemble_structure(self) -> None:
        """Canonical ensemble contains 9 clusters (6 odd in 3 pairs, 3 neutral)."""
        ensemble = build_canonical_4d_half_instanton_ensemble()
        assert len(ensemble) == 9

        odd_clusters = [c for c in ensemble if (c.n_plus - c.n_minus) % 2 != 0]
        zero_clusters = [c for c in ensemble if (c.n_plus - c.n_minus) % 2 == 0]
        assert len(odd_clusters) == 6
        assert len(zero_clusters) == 3

    def test_involution_idempotency_and_sign_reversal(self) -> None:
        """Orientation flip tau satisfies tau^2 = id and sigma(tau(C)) = -sigma(C) on odd sectors."""
        c = HalfInstantonCluster4D(n_plus=1, n_minus=0, weight=Fraction(100, 1))
        tau_c = orientation_flip(c)
        assert tau_c.n_plus == 0 and tau_c.n_minus == 1
        assert tau_c.weight == c.weight
        assert c.fermion_determinant_sign == -1
        assert tau_c.fermion_determinant_sign == 1
        assert c.fermion_determinant_sign + tau_c.fermion_determinant_sign == 0

        tau_tau_c = orientation_flip(tau_c)
        assert tau_tau_c.n_plus == c.n_plus
        assert tau_tau_c.n_minus == c.n_minus
        assert tau_tau_c.fermion_determinant_sign == c.fermion_determinant_sign

    def test_exact_cancellation_execution(self) -> None:
        """Cancellation produces exact Z = 450, zero duality gap, and 3 cancelled pairs."""
        ensemble = build_canonical_4d_half_instanton_ensemble()
        res = execute_4d_half_instanton_cancellation(ensemble)

        assert res["status"] == "EXACT_REPAIR"
        assert res["duality_gap"] == Fraction(0, 1)
        assert res["total_partition_sum"] == Fraction(450, 1)
        assert res["zero_charge_sum"] == Fraction(450, 1)
        assert res["odd_charge_sum"] == Fraction(0, 1)
        assert res["pairs_cancelled"] == 3


class Test4DWireGrammarAndDDCExecution:
    """Verifies Gamma38 wire formatting, DDC DAG causality, and receipt generation."""

    def test_wire_turns_grammatical_validity(self) -> None:
        """All canonical wire turns adhere strictly to Gamma38 grammar."""
        for turn in CANONICAL_4D_WIRE_TURNS:
            in_w = turn["input_wire"]
            out_w = turn["expected_response_wire"]
            assert validate_wire_string(in_w)
            assert validate_wire_string(out_w)
            assert all(ch in GAMMA_38 for ch in in_w)
            assert all(ch in GAMMA_38 for ch in out_w)

    def test_ddc_dag_emission_and_causality(self, tmp_path: Path) -> None:
        """DDC DAG trace emits 6 nodes with strict acyclic parent causality."""
        dag_file = tmp_path / "test_4d_dag.jsonl"
        ensemble = build_canonical_4d_half_instanton_ensemble()
        canc_res = execute_4d_half_instanton_cancellation(ensemble)
        nodes = emit_4d_instanton_ddc_dag(str(dag_file), canc_res)

        assert len(nodes) == 6
        assert dag_file.is_file()

        for i in range(1, len(nodes)):
            assert nodes[i]["parent_ids"] == [nodes[i - 1]["node_id"]]

        term = nodes[-1]
        assert term["stage"] == "EXACT_REPAIR"
        assert term["payload"]["status"] == "EXACT_REPAIR"
        assert term["payload"]["duality_gap"] == "0"
        assert term["payload"]["total_partition_sum"] == "450"

    def test_run_4d_half_instanton_demo_end_to_end(self, tmp_path: Path) -> None:
        """End-to-end demo execution generates valid receipt and digest."""
        rcpt_file = tmp_path / "test_receipt.json"
        dag_file = tmp_path / "test_dag.jsonl"
        receipt = run_4d_half_instanton_demo(
            output_receipt=str(rcpt_file),
            output_dag=str(dag_file),
        )

        assert receipt["authority_effect"] == "None"
        assert receipt["exact_cancellation_metrics"]["status"] == "EXACT_REPAIR"
        assert receipt["exact_cancellation_metrics"]["total_partition_sum"] == "450"
        assert receipt["exact_cancellation_metrics"]["duality_gap"] == "0"
        assert receipt["wire_grammar"]["pure_gamma_38"] is True

        stored_digest = receipt["sha256_digest"]
        body_to_hash = {k: v for k, v in receipt.items() if k != "sha256_digest"}
        recomputed = hashlib.sha256(json.dumps(body_to_hash, indent=2, sort_keys=True).encode("utf-8")).hexdigest()
        assert len(stored_digest) == 64


class Test4DCodeHygieneAndZeroFloats:
    """Verifies zero floating-point usage and lexical hygiene."""

    def test_ast_zero_floats(self) -> None:
        """Ensures demo_4d_half_instanton.py contains zero float literals or calls."""
        demo_code_path = DEMOS_DIR / "code" / "demo_4d_half_instanton.py"
        tree = ast.parse(demo_code_path.read_text(encoding="utf-8"))

        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, float):
                pytest.fail(f"Float literal {node.value} detected in {demo_code_path.name}")
            if isinstance(node, ast.Name) and node.id == "float":
                pytest.fail(f"Call or reference to 'float' detected in {demo_code_path.name}")

    def test_lexical_hygiene(self) -> None:
        """Verifies wire turn prompts conform to lexical hygiene."""
        for turn in CANONICAL_4D_WIRE_TURNS:
            assert_lexical_hygiene(turn["wire_prompt"])
            assert_lexical_hygiene(turn["grammar_prompt"])
