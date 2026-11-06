"""
Tests for Machine Learning, LLMs & Transformer Token Dynamics Domain Kernel
AuthorityEffect: None
"""

import sys
from pathlib import Path

# Add domain code directory to sys.path
_code_dir = Path(__file__).resolve().parent.parent / "code"
if str(_code_dir) not in sys.path:
    sys.path.insert(0, str(_code_dir))

from domain_llms_kernel import (
    CausalAttentionDAGReceipt,
    DomainEngine,
    PrimitiveDifferenceSetting,
    SimplicialBoundaryReceipt,
)


def test_initial_void_to_root():
    engine = DomainEngine()
    assert engine.state.step == 0
    assert engine.step_01_admit_root("<>")
    assert engine.state.step == 1
    assert "<>" in engine.state.carrier
    assert "branch_root_single" in engine.state.branches_retained


def test_germ_creation_and_witness():
    engine = DomainEngine()
    engine.step_01_admit_root("<>")
    assert engine.step_02_admit_germ("tok_alpha", "tok_beta")
    assert engine.state.step == 2
    assert ("tok_alpha", "tok_beta") in engine.state.relations


def test_irreflexive_enforcement_and_distinctness():
    engine = DomainEngine()
    engine.step_01_admit_root("<>")
    engine.step_02_admit_germ("tok_alpha", "tok_beta")
    # inject reflexive defect
    engine.state.relations.add(("tok_alpha", "tok_alpha"))
    assert not engine.setting.is_irrefl()

    # Discharge obstruction
    assert engine.step_03_enforce_irrefl()
    assert engine.setting.is_irrefl()
    assert engine.setting.is_distinct()


def test_full_16_stage_presentation_sequence():
    """Validates full 16-stage evolutionary sequence for Domain 10."""
    engine = DomainEngine()
    assert engine.step_01_admit_root("<>")
    assert engine.step_02_admit_germ("t0", "t1")
    assert engine.step_03_enforce_irrefl()
    assert engine.step_04_admit_orientation()
    assert engine.step_05_isolate_queue()
    assert engine.step_06_instantiate_alphabet(["t0", "t1", "t2", "t3"])
    receipt_b = engine.step_07_evaluate_boundary_closure()
    assert receipt_b.is_nilpotent
    dag = engine.step_08_synthesize_causal_poset()
    assert isinstance(dag, CausalAttentionDAGReceipt)
    assert dag.is_strictly_causal
    assert engine.step_09_resolve_parity()
    assert engine.step_10_admit_higher_complexes()
    assert engine.step_11_enforce_conservation()
    assert engine.step_12_quotient_observer_interface()
    assert engine.step_13_prune_fuel_bounded_branches()
    assert engine.step_14_establish_frontier()
    gap = engine.step_15_isolate_gap_obstruction()
    assert gap["gap_id"] == "ContinuousGradientObstruction"
    cert = engine.step_16_terminal_certification()
    assert cert["status"] == "CERTIFIED"
    assert cert["steps_completed"] == 16
    assert cert["authority_effect"] == "None"


def test_boundary_closure_invariant():
    """Verifies that evaluate_boundary_closure returns genuine SimplicialBoundaryReceipt with B_1*B_2 = 0."""
    engine = DomainEngine()
    engine.step_01_admit_root("<>")
    engine.step_02_admit_germ("t0", "t1")
    engine.step_03_enforce_irrefl()
    receipt = engine.evaluate_boundary_closure()
    assert isinstance(receipt, SimplicialBoundaryReceipt)
    assert receipt.is_nilpotent
    assert bool(receipt) is True
    for row in receipt.product_matrix:
        for val in row:
            assert val == 0


def test_causal_attention_dag_strictly_lower_triangular():
    """Verifies causal attention DAG enforces acyclic temporal precedence (i > j)."""
    engine = DomainEngine()
    receipt = engine.evaluate_causal_attention(seq_len=4)
    assert receipt.is_strictly_causal
    assert receipt.max_context_length == 4
    # For seq_len=4, num edges = 4*3/2 = 6
    assert len(receipt.causal_edges) == 6
    # Verify no anti-causal edge (tok_j, tok_i) with j >= i
    for src, dst in receipt.causal_edges:
        src_idx = int(src.split("_")[1])
        dst_idx = int(dst.split("_")[1])
        assert src_idx < dst_idx


def test_transposition_sign_inversion():
    """Verifies 1-chain transposition sign inversion: partial_1(sigma(e)) == -partial_1(e)."""
    setting = PrimitiveDifferenceSetting(
        carrier={"t0", "t1"}, relation={("t0", "t1")}, a="t0", b="t1"
    )
    assert setting.verify_transposition_sign_inversion(("t0", "t1"))


def test_explicit_recovery_gap_detection():
    """Verifies isolation of ContinuousGradientObstruction."""
    engine = DomainEngine()
    gap_info = engine.check_gap_obstruction()
    assert gap_info["gap_id"] == "ContinuousGradientObstruction"
    assert gap_info["status"] == "UNBRIDGED_OBSTRUCTION"
    assert engine.gap_detected
