"""
Adversarial & Falsification Tests: LLMs & Transformer Token Dynamics
Style: Lev Landau / Soviet Inspector
AuthorityEffect: None
"""

import sys
from pathlib import Path

_code_dir = Path(__file__).resolve().parent.parent / "code"
if str(_code_dir) not in sys.path:
    sys.path.insert(0, str(_code_dir))

from domain_llms_kernel import (
    DomainEngine,
)


def test_adversarial_anti_causal_leakage_rejection():
    """
    INVARIANT: Causal attention requires strict acyclicity: no future token
    may direct an attention edge to an earlier token in a causal decoder.
    """
    engine = DomainEngine()
    receipt = engine.evaluate_causal_attention(seq_len=5)
    for src, dst in receipt.causal_edges:
        src_idx = int(src.split("_")[1])
        dst_idx = int(dst.split("_")[1])
        assert src_idx < dst_idx, f"Anti-causal leakage detected: {src} -> {dst}"


def test_adversarial_boundary_nilpotency_token_n_grams():
    """
    INVARIANT: For any valid n-gram simplicial 2-complex, the matrix product
    B_1 * B_2 must evaluate to identically zero over Z.
    """
    engine = DomainEngine()
    vertices = ["tok_0", "tok_1", "tok_2", "tok_3"]
    edges = [
        ("tok_0", "tok_1"),
        ("tok_1", "tok_2"),
        ("tok_0", "tok_2"),
        ("tok_2", "tok_3"),
        ("tok_1", "tok_3"),
    ]
    faces = [
        ("tok_0", "tok_1", "tok_2"),
        ("tok_1", "tok_2", "tok_3"),
    ]
    receipt = engine.evaluate_simplicial_boundary_matrices(vertices, edges, faces)
    assert receipt.is_nilpotent
    for i, row in enumerate(receipt.product_matrix):
        for k, val in enumerate(row):
            assert val == 0, f"Boundary defect at ({i}, {k}): {val}"


def test_adversarial_gradient_obstruction_inviolability():
    """
    INVARIANT: ContinuousGradientObstruction is unbridged;
    smooth backpropagation in R^d cannot be derived from discrete tokens.
    """
    engine = DomainEngine()
    gap = engine.check_gap_obstruction()
    assert gap["status"] == "UNBRIDGED_OBSTRUCTION"
    assert "Continuous backpropagation gradients" in gap["reason"]
    assert gap["authority_effect"] == "None"
