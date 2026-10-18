r"""
Unit Test Suite for Degree-Generic Window Lift in DDA Engine.

AuthorityEffect: None throughout.

Tests:
1. Degree 1 repair terminating with SOLVED and empty lift history.
2. Forced lift C^1 -> C^2 producing WindowLiftCert(lift_kind="tetrahedra").
3. Forced lift C^2 -> C^3 producing AUTHORIZATION_EXHAUSTED with lift_kind="unsupported" and zero cell invention.
"""

import sys
from pathlib import Path
import pytest

# Ensure coda is accessible
coda_dir = Path(__file__).resolve().parents[1] / "coda"
ooutwire_dir = Path(__file__).resolve().parents[2]

for p in [str(coda_dir), str(ooutwire_dir)]:
    if p not in sys.path:
        sys.path.insert(0, p)

from omega_engine.crates.discrete_deformation_algebra.dda_engine import (
    DDAEngine,
    TerminationStatus,
    WindowLiftCert,
)
from omega_engine.crates.residuals.network_residual import Network


def test_degree_1_ordinary_repair_solved():
    """Ordinary degree 1 repair terminates with SOLVED and empty lift history."""
    nodes = [0, 1, 2]
    edges = [(0, 1), (1, 2), (0, 2)]
    net = Network(nodes, edges)

    engine = DDAEngine(net)
    # Exact potential: v(0)=0, v(1)=1, v(2)=3 -> edge values (1, 2, 3)
    edge_vals = {(0, 1): 1.0, (1, 2): 2.0, (0, 2): 3.0}

    foundation = engine.run_foundation(edge_vals)
    assert foundation.is_valid()

    cert, residuals = engine.step_dda("exact_d0")
    term = engine.lift_or_terminate(residuals)

    assert term.status == TerminationStatus.SOLVED
    assert len(engine.lift_history) == 0
    assert term.algebraic_class_id == "exact"


def test_forced_lift_c1_to_c2():
    """Forced lift C^1 -> C^2 produces WindowLiftCert with lift_kind="tetrahedra"."""
    nodes = [0, 1, 2, 3]
    edges = [(0, 1), (1, 2), (2, 0), (0, 3), (1, 3), (2, 3)]
    faces = [(0, 1, 2), (0, 1, 3), (1, 2, 3), (0, 2, 3)]
    net = Network(nodes, edges, faces)

    engine = DDAEngine(net)
    # Non-zero curl on face (0,1,2): gamma2 > 0
    edge_vals = {(0, 1): 1.0, (1, 2): 1.0, (2, 0): 1.0, (0, 3): 0.0, (1, 3): 0.0, (2, 3): 0.0}

    foundation = engine.run_foundation(edge_vals)
    assert foundation.gamma2 > 1e-3

    term = engine.lift_or_terminate((foundation.phi1, foundation.gamma2, foundation.chi), max_lifts=1)

    assert len(engine.lift_history) == 1
    cert = engine.lift_history[0]
    assert cert.from_degree == 1
    assert cert.to_degree == 2
    assert cert.lift_kind == "tetrahedra"
    assert cert.num_higher_cells == 1
    assert cert.num_tetrahedra == 1  # backward compatibility alias
    assert cert.trigger_curvature_mass > 0
    assert cert.is_valid()


def test_forced_unsupported_lift_c2_to_c3():
    """Forced lift C^2 -> C^3 produces AUTHORIZATION_EXHAUSTED and lift_kind="unsupported"."""
    nodes = [0, 1, 2, 3]
    edges = [(0, 1), (1, 2), (2, 0), (0, 3), (1, 3), (2, 3)]
    faces = [(0, 1, 2), (0, 1, 3), (1, 2, 3), (0, 2, 3)]
    net = Network(nodes, edges, faces)

    engine = DDAEngine(net)
    engine.degree_window = 2

    # Force lift at degree 2 with non-zero curvature mass gamma3 = 1.0
    term = engine.lift_or_terminate((0.0, 1.0, 0.0), max_lifts=2)

    assert term.status == TerminationStatus.AUTHORIZATION_EXHAUSTED
    assert "unsupported-lift:C^2->C^3" in term.algebraic_class_id
    assert len(engine.lift_history) == 1

    c2_cert = engine.lift_history[0]
    assert c2_cert.from_degree == 2
    assert c2_cert.to_degree == 3
    assert c2_cert.lift_kind == "unsupported"
    assert c2_cert.num_higher_cells == 0  # Zero cell invention!
    assert c2_cert.is_valid()


