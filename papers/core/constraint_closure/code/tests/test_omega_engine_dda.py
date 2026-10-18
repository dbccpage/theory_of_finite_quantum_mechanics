"""Tests for universe_anomalonica.omega_engine.dda subsystem.

AuthorityEffect: None.
"""

import os
import sys
import numpy as np
import pytest

base_dir = os.environ.get("CODA_OOUTWIRE_DOCS")
if base_dir:
    math_dir = os.path.join(base_dir, "universe_anomalonica", "math")
    for p in [base_dir, math_dir]:
        if p not in sys.path:
            sys.path.insert(0, p)

try:
    from dda_engine import DDAEngine, TerminationStatus
    from dda_cascade_router import DdaCascadeRouter
    from solver_of_solvers import CascadeSolver, SolverCascadeReceipt
    from dda_trace_recorder import DDATraceRecorder, get_global_trace_recorder
    from network_residual import build_tetrahedron_boundary, Network
except ImportError:
    try:
        from ..dda_engine import DDAEngine, TerminationStatus
        from ..dda_cascade_router import DdaCascadeRouter
        from ..solver_of_solvers import CascadeSolver, SolverCascadeReceipt
        from ..dda_trace_recorder import DDATraceRecorder, get_global_trace_recorder
        from ..network_residual import build_tetrahedron_boundary, Network
    except ImportError:
        pytestmark = pytest.mark.skip(reason="local dda modules not present")


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


def test_dda_trace_recorder(tmp_path):
    """Test DDATraceRecorder step logging and trace file emission."""
    recorder = DDATraceRecorder(trace_dir=str(tmp_path / "dda_trace"))
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

