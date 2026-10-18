"""Tests for Planar coloured operad, trees, grafting, and term hashing."""

import pytest
from src.operad_theory.planar_operad import (
    OperadColour,
    Operation,
    OpenLeaf,
    PlanarTree,
    OperadError,
)


def test_corolla_and_arity():
    c_in = OperadColour("V")
    c_out = OperadColour("W")
    op = Operation(name="mu", inputs=(c_in, c_in), output=c_out)

    tree = PlanarTree.corolla(op)
    assert tree.arity == 2
    assert tree.output_colour() == c_out
    assert len(tree.children) == 2


def test_grafting_and_term_hash():
    cV = OperadColour("V")
    cW = OperadColour("W")

    op_mu = Operation(name="mu", inputs=(cV, cV), output=cW)
    op_eta = Operation(name="eta", inputs=(cV,), output=cV)

    tree_mu = PlanarTree.corolla(op_mu)
    tree_eta = PlanarTree.corolla(op_eta)

    # Graft eta into slot 0 of mu
    grafted = tree_mu.graft(0, tree_eta)
    assert grafted.arity == 2  # eta has 1 leaf + slot 1 has 1 leaf = 2
    assert grafted.output_colour() == cW
    assert grafted.term_repr() == "mu(eta(leaf:V),leaf:V)"

    # SHA256 deterministic hash
    h1 = grafted.term_hash()
    h2 = grafted.term_hash()
    assert h1 == h2
    assert len(h1) == 64


def test_grafting_colour_mismatch_raises():
    cV = OperadColour("V")
    cW = OperadColour("W")
    cX = OperadColour("X")

    op1 = Operation(name="op1", inputs=(cV,), output=cW)
    op2 = Operation(name="op2", inputs=(cV,), output=cX)

    tree1 = PlanarTree.corolla(op1)
    tree2 = PlanarTree.corolla(op2)

    # Slot requires V, tree2 outputs X -> mismatch
    with pytest.raises(OperadError):
        tree1.graft(0, tree2)
