"""Tests for omega_engine.crates.discrete_deformation_algebra subsystem.

AuthorityEffect: None.
"""

import os
import sys
import numpy as np
import pytest

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

from omega_engine.crates.discrete_deformation_algebra import (
    DDAEngine,
    DdaCascadeRouter,
    CascadeSolver,
    SolverCascadeReceipt,
    DDATraceRecorder,
    TerminationStatus,
    get_global_trace_recorder,
)
from omega_engine.crates.residuals.network_residual import build_tetrahedron_boundary, Network


def test_dda_cascade_router_tape():
    """Test DdaCascadeRouter Hodge split and tape generation."""
    d0 = np.array([[-1.0, 1.0, 0.0], [0.0, -1.0, 1.0], [1.0, 0.0, -1.0]])
    d1 = np.array([[1.0, 1.0, 1.0]])

    router = DdaCascadeRouter(d0=d0, d1=d1)
    w = np.array([0.5, -0.5, 0.2])

    exact, coexact, harmonic = router.compute_hodge_components(w)
    assert exact.shape == w.shape
    assert coexact.shape == w.shape
    assert harmonic.shape == w.shape
    assert "C" in router.tape


def test_dda_trace_recorder():
    """Test DDATraceRecorder step logging and trace file emission."""
    recorder = DDATraceRecorder()
    rec = recorder.record_step(
        op_type="FOUNDATION",
        tape_token="E",
        res_before=1.5,
        res_after=1.0,
        metadata={"cycle": "c1"},
    )
    assert rec.operation_type == "FOUNDATION"
    assert rec.tape_token == "E"
    assert rec.delta_residual == 0.5
    assert len(recorder.tape) >= 1
    assert os.path.exists(recorder.trace_dir / "latest_dda_trace.json")


def test_cascade_solver_execution():
    """Test CascadeSolver hierarchical residual removal loop."""
    nodes = [0, 1, 2, 3]
    edges = [(0, 1), (1, 2), (2, 0), (0, 3), (1, 3), (2, 3)]
    faces = [(0, 1, 2), (0, 1, 3), (1, 2, 3), (2, 0, 3)]
    net = Network(nodes=nodes, edges=edges, faces=faces)
    edge_vals = {(0, 1): 0.4, (1, 2): -0.3, (2, 0): 0.1, (0, 3): 0.0, (1, 3): 0.2, (2, 3): -0.1}

    solver = CascadeSolver(network=net)
    receipt = solver.solve(edge_values=edge_vals, max_lifts=1)

    assert isinstance(receipt, SolverCascadeReceipt)
    assert receipt.initial_residual_size >= 0.0
    assert receipt.authority_effect == "None"





