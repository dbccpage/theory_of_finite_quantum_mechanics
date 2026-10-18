r"""
Unit tests for Chern-Simons character-variety structures (codaq/chern_simons.py).
"""

import cmath
import math
import pytest
from omega_engine.crates.quantum_physics.chern_simons import (
    FIGURE_EIGHT_VOLUME,
    ChernSimonsKnotAction,
    FigureEightCharacterVariety,
    TrefoilCharacterVariety,
)


def test_figure_eight_volume_constant():
    assert abs(FIGURE_EIGHT_VOLUME - 2.029883212819) < 1e-10


def test_figure_eight_cs_values():
    cs_ab = FigureEightCharacterVariety.cs_value("abelian")
    assert cs_ab == 0.0

    cs_plus = FigureEightCharacterVariety.cs_value("non_abelian_plus")
    expected_plus = 1j * (FIGURE_EIGHT_VOLUME / (2.0 * math.pi))
    assert abs(cs_plus - expected_plus) < 1e-12

    cs_minus = FigureEightCharacterVariety.cs_value("non_abelian_minus")
    assert abs(cs_minus + expected_plus) < 1e-12


def test_figure_eight_flat_connections():
    flat_pairs = FigureEightCharacterVariety.non_abelian_flat_connections()
    assert len(flat_pairs) == 2

    for m, l in flat_pairs:
        val_a = FigureEightCharacterVariety.eval_A(m, l)
        assert abs(val_a) < 1e-10


def test_trefoil_cs_values():
    cs1 = TrefoilCharacterVariety.cs_value(1)
    assert abs(cs1 - 1.0 / 6.0) < 1e-12

    cs5 = TrefoilCharacterVariety.cs_value(5)
    assert abs(cs5 - 25.0 / 6.0) < 1e-12


def test_cs_knot_action_gradient_at_flat_connection():
    action = ChernSimonsKnotAction("figure_eight")
    flat_pairs = FigureEightCharacterVariety.non_abelian_flat_connections()
    m0, l0 = flat_pairs[0]

    val = action.eval([m0, l0])
    assert abs(val) < 1e-12

    grad = action.gradient([m0, l0])
    assert abs(grad[0]) < 1e-4 and abs(grad[1]) < 1e-4



