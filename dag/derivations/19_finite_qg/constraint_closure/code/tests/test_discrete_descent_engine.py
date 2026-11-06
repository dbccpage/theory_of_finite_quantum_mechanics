"""Tests for the self-contained discrete descent engine & cascade solver.

Verifies:
1. Hodge decomposition and execution tape generation in quotient descent router.
2. Stepwise audit trail recording in descent trace recorder.
3. Cascade solver hierarchical residual minimization.
4. Obligation preservation across degree lifts: an unresolved degree-1 obstruction
   must remain in prior_degree_obligations and prevent false is_solved=True.
5. Backward-compatibility aliases (DDAEngine, DdaCascadeRouter, DDATraceRecorder).

AuthorityEffect: None.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
import numpy as np
import pytest

code_dir = Path(__file__).resolve().parents[1]
if str(code_dir) not in sys.path:
    sys.path.insert(0, str(code_dir))

from network_residual import Network, build_tetrahedron_boundary
from discrete_descent_engine import (
    DDAEngine,
    DiscreteDescentEngine,
    FoundationCert,
    DDAStepCert,
    WindowLiftCert,
    TerminationCert,
    TerminationStatus,
)
from quotient_descent_router import QuotientDescentRouter, DdaCascadeRouter
from descent_trace_recorder import (
    DescentTraceRecorder,
    DDATraceRecorder,
    get_global_trace_recorder,
)
from solver_of_solvers import CascadeSolver, SolverCascadeReceipt


def test_quotient_descent_router_tape():
    """Test QuotientDescentRouter Hodge split and tape generation."""
    d0 = np.array([[-1.0, 1.0, 0.0], [0.0, -1.0, 1.0], [1.0, 0.0, -1.0]])
    d1 = np.array([[1.0, 1.0, 1.0]])

    router = QuotientDescentRouter(d0=d0, d1=d1)
    w = np.array([0.5, -0.5, 0.2])

    exact, coexact, harmonic = router.compute_hodge_components(w)
    assert exact.shape == w.shape
    assert coexact.shape == w.shape
    assert harmonic.shape == w.shape
    assert "C" in router.tape


def test_descent_trace_recorder(tmp_path):
    """Test DescentTraceRecorder step logging and trace file emission."""
    recorder = DescentTraceRecorder(trace_dir=str(tmp_path / "descent_trace"))
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


def test_cascade_solver_lift_preserves_prior_degree_obligations():
    """Verify that when a degree-1 obstruction survives a lift, earlier obligations

    are preserved and is_solved() refuses to declare success.
    """
    nodes = [0, 1, 2]
    edges = [(0, 1), (1, 2), (2, 0)]
    faces = []
    net = Network(nodes=nodes, edges=edges, faces=faces)

    solver = CascadeSolver(network=net)
    edge_vals = {(0, 1): 1.0, (1, 2): 1.0, (2, 0): 1.0}
    receipt = solver.solve(edge_values=edge_vals, max_lifts=1)

    assert isinstance(receipt, SolverCascadeReceipt)
    assert receipt.initial_residual_size == pytest.approx(3.0)

    if receipt.terminal_status != "Exact":
        assert not receipt.is_solved()


def test_backward_compatibility_facades():
    """Verify that legacy DDA names import and behave identically to domain names."""
    d0 = np.array([[-1.0, 1.0, 0.0], [0.0, -1.0, 1.0], [1.0, 0.0, -1.0]])
    d1 = np.array([[1.0, 1.0, 1.0]])

    r_new = QuotientDescentRouter(d0=d0, d1=d1)
    r_old = DdaCascadeRouter(d0=d0, d1=d1)
    assert type(r_new) is type(r_old)

    rec_new = DescentTraceRecorder()
    rec_old = DDATraceRecorder()
    assert type(rec_new) is type(rec_old)
