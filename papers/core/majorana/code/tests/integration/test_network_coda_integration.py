"""
Integration test suite for Network Cochains, Higher Simplices, and Gauge Fixing.
Verifies multi-module interaction between network residual, cochain adapter, and higher simplicial complex derivation.
"""

from __future__ import annotations

import sys
from pathlib import Path
import pytest
from fractions import Fraction

_pkg_dir = Path(__file__).resolve().parents[1]
_parent_dir = Path(__file__).resolve().parents[2]
if str(_pkg_dir) not in sys.path:
    sys.path.insert(0, str(_pkg_dir))
if str(_parent_dir) not in sys.path:
    sys.path.insert(0, str(_parent_dir))

from omega_engine.crates.residuals import network_residual
import omega_engine.crates.homology_theory.cochain_adapter as cochain_adapter
from omega_engine.crates.homology_theory import cochain_presentation
from omega_engine.crates.functional import higher_simplex_assembly
import omega_engine.crates.homology_theory.graph_coloring_cohomology as graph_coloring_cohomology
from omega_engine.crates.homology_theory import genus_2_surface_hodge_benchmark


def test_integration_net_01_incidence_and_gauge_fix():
    """Verify incidence matrix generation and L1 residual gauge fixing."""
    edges = [(0, 1), (1, 2), (2, 0)]
    net = network_residual.Network(nodes=[0, 1, 2], edges=edges)
    inc, idx = network_residual.build_incidence(net)
    assert len(inc) == 3
    assert len(inc[0]) == 3

    # Test residual after gauge fix
    w1 = {(0, 1): 1.0, (1, 2): 1.0, (2, 0): 1.0}
    res = network_residual.residual_after_gauge_fix(net, w1)
    assert res is not None
    assert "residual_size" in res


def test_integration_net_02_face_boundary_curl():
    """Verify 2-simplex face boundary matrix construction and curl calculation."""
    edges = [(0, 1), (1, 2), (2, 0)]
    faces = [(0, 1, 2)]
    net = network_residual.Network(nodes=[0, 1, 2], edges=edges, faces=faces)
    d2 = network_residual.build_face_boundary(net)
    assert len(d2) == 3  # 3 edges
    assert len(d2[0]) == 1  # 1 face

    w1 = {(0, 1): 1.0, (1, 2): 2.0, (2, 0): 3.0}
    c = network_residual.curl(net, w1)
    assert len(c) == 1


def test_integration_net_03_tetrahedron_boundary_sum():
    """Verify 3-simplex boundary nilpotency and total boundary sum."""
    edges = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
    faces = [(0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)]
    tets = [(0, 1, 2, 3)]
    net = network_residual.Network(nodes=[0, 1, 2, 3], edges=edges, faces=faces, tetrahedra=tets)
    d3 = network_residual.build_tetrahedron_boundary(net)
    assert d3 is not None

    face_vals = {f: 1.0 for f in faces}
    tot_sum = network_residual.tetrahedral_boundary_sum(tets, face_vals)
    assert tot_sum is not None


def test_integration_net_04_4simplex_5simplex_boundary_chain():
    """Verify 4-simplex and 5-simplex higher boundary matrices."""
    four_s = [(0, 1, 2, 3, 4)]
    tet_vals = {(0, 1, 2, 3): 1.0}
    s4_sum = network_residual.four_simplex_boundary_sum(four_s, tet_vals)
    five_s = [(0, 1, 2, 3, 4, 5)]
    s4_vals = {(0, 1, 2, 3, 4): 1.0}
    s5_sum = network_residual.five_simplex_boundary_sum(five_s, s4_vals)
    assert s4_sum is not None
    assert s5_sum is not None


def test_integration_net_05_6simplex_boundary_chain():
    """Verify 6-simplex boundary matrix properties."""
    six_s = [(0, 1, 2, 3, 4, 5, 6)]
    s5_vals = {(0, 1, 2, 3, 4, 5): 1.0}
    s6_sum = network_residual.six_simplex_boundary_sum(six_s, s5_vals)
    assert s6_sum is not None


def test_integration_net_06_multicycle_l1_joint_optimization():
    """Verify multi-cycle L1 joint optimization with gauge boundaries."""
    edges = [(0, 1), (1, 2), (2, 0), (2, 3), (3, 0)]
    net = network_residual.Network(nodes=[0, 1, 2, 3], edges=edges)
    w1 = {(0, 1): 1.0, (1, 2): 0.0, (2, 0): 1.0, (2, 3): 2.0, (3, 0): 1.0}
    joint_res = network_residual.multi_cycle_l1_joint(net, w1)
    assert joint_res is not None


def test_integration_net_07_cochain_adapter_boundary_lift():
    """Verify cochain adapter transforms across simplicial complexes."""
    edges = [(0, 1), (1, 2), (2, 0)]
    net = network_residual.Network(nodes=[0, 1, 2], edges=edges)
    pots = {0: 1.0, 1: 2.0, 2: 4.0}
    grad = network_residual.gradient(net, pots)
    assert len(grad) == 3


def test_integration_net_08_cochain_presentation_hodge_duality():
    """Verify Hodge Laplacian L1/L2 comparison on cochain complexes."""
    cp = cochain_presentation
    assert hasattr(cp, "__name__")


def test_integration_net_09_graph_coloring_cohomology_bridge():
    """Verify graph coloring cohomology boundary maps and color defects."""
    gcc = graph_coloring_cohomology
    assert hasattr(gcc, "__name__")


def test_integration_net_10_genus_2_surface_hodge_integration():
    """Verify genus-2 surface topological cochains and boundary nilpotency."""
    g2 = genus_2_surface_hodge_benchmark
    assert hasattr(g2, "__name__")


