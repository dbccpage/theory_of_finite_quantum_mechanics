"""
Unit tests for DDC Operation C (Context Exposure).
AuthorityEffect: None.
"""

from fractions import Fraction

from context_exposure import ContextWindowExtractor


def test_context_window_disjoint_partition():
    """Verify internal and boundary edges partition properly."""
    # Graph: A - B - C - D
    edges = [("A", "B"), ("B", "C"), ("C", "D")]
    extractor = ContextWindowExtractor(edges)

    # Window: {B, C}
    # Internal: (B, C)
    # Boundary: (A, B) and (C, D)
    window = {"B", "C"}
    ambient = {
        ("A", "B"): Fraction(10),
        ("B", "C"): Fraction(20),
        ("C", "D"): Fraction(30),
    }

    receipt = extractor.expose(window, ambient)
    assert receipt.status == "CONTEXT_EXPOSED"
    assert receipt.internal_edges == [("B", "C")]
    assert set(receipt.boundary_edges) == {("A", "B"), ("C", "D")}
    assert receipt.internal_cochain[("B", "C")] == Fraction(20)
    assert receipt.boundary_cochain[("A", "B")] == Fraction(10)
    assert receipt.boundary_cochain[("C", "D")] == Fraction(30)


def test_entire_graph_as_window():
    """If window is entire graph, boundary is empty."""
    edges = [("A", "B"), ("B", "C")]
    extractor = ContextWindowExtractor(edges)

    window = {"A", "B", "C"}
    ambient = {("A", "B"): Fraction(1), ("B", "C"): Fraction(2)}

    receipt = extractor.expose(window, ambient)
    assert len(receipt.internal_edges) == 2
    assert len(receipt.boundary_edges) == 0
