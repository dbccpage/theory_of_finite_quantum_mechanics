"""Tests for FiniteBicategory and Mac Lane pentagon/triangle coherence."""

import pytest
from src.higher_category_theory.bicategory import (
    Strict2Category,
    FiniteBicategory,
    check_pentagon_coherence,
    check_triangle_coherence,
)


def test_strict_2_category_composition():
    cat = Strict2Category()
    cat.add_object("A")
    cat.add_object("B")
    cat.add_object("C")
    cat.add_1cell("f", "A", "B")
    cat.add_1cell("g", "B", "C")

    gf = cat.compose_1("f", "g")
    assert gf == "g_circ_f"
    assert cat.one_cells[gf] == ("A", "C")


def test_pentagon_coherence_strict():
    cat = Strict2Category()
    for obj in ["A", "B", "C", "D", "E"]:
        cat.add_object(obj)

    cat.add_1cell("f", "A", "B")
    cat.add_1cell("g", "B", "C")
    cat.add_1cell("h", "C", "D")
    cat.add_1cell("k", "D", "E")

    bicat = FiniteBicategory(cat)
    # With identity associators, pentagon coherence holds strictly
    assert check_pentagon_coherence(bicat, "f", "g", "h", "k") is True


def test_triangle_coherence_strict():
    cat = Strict2Category()
    for obj in ["A", "B", "C"]:
        cat.add_object(obj)

    cat.add_1cell("f", "A", "B")
    cat.add_1cell("g", "B", "C")

    bicat = FiniteBicategory(cat)
    # With identity unitors and associator, triangle coherence holds
    assert check_triangle_coherence(bicat, "f", "g") is True
