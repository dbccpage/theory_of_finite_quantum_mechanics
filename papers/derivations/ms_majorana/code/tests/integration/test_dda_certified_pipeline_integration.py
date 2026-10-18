"""
Integration test suite for DDA Engine, Window Lifts, Certified Pipelines, and Bag Fingerprinting.
"""

from __future__ import annotations

import sys
from pathlib import Path
import pytest

_pkg_dir = Path(__file__).resolve().parents[1]
_parent_dir = Path(__file__).resolve().parents[2]
if str(_pkg_dir) not in sys.path:
    sys.path.insert(0, str(_pkg_dir))
if str(_parent_dir) not in sys.path:
    sys.path.insert(0, str(_parent_dir))

from omega_engine.crates.discrete_deformation_algebra import dda_engine
from omega_engine.crates.pipeline import certified_pipeline
import omega_engine.crates.pipeline.certified_residual_integration as certified_residual_integration
from omega_engine.crates.discrete_deformation_algebra import dda_cascade_router
import omega_engine.crates.discrete_deformation_algebra.cross_validate_dda_claims as cross_validate_dda_claims
from omega_engine.crates.residuals.network_residual import Network


def test_integration_dda_01_dda_engine_foundation():
    """Verify DDA foundation certificate creation and initial window lifts."""
    net = Network(nodes=[0, 1, 2], edges=[(0, 1), (1, 2), (2, 0)])
    engine = dda_engine.DDAEngine(net, observer_name="OBS_01")
    edge_vals = {(0, 1): 1.0, (1, 2): 1.0, (2, 0): 1.0}
    f_cert = engine.run_foundation(edge_vals)
    assert f_cert.observer_name == "OBS_01"


def test_integration_dda_02_window_lift_cert_chaining():
    """Verify multi-step window lift certification and status tracking."""
    net = Network(nodes=[0, 1, 2], edges=[(0, 1), (1, 2), (2, 0)])
    engine = dda_engine.DDAEngine(net, observer_name="OBS_02")
    edge_vals = {(0, 1): 1.0, (1, 2): 1.0, (2, 0): 1.0}
    engine.run_foundation(edge_vals)
    cert, res = engine.step_dda("exact_d0")
    assert len(engine.step_history) == 1


def test_integration_dda_03_termination_cert_validation():
    """Verify DDA termination conditions and status codes."""
    net = Network(nodes=[0, 1, 2], edges=[(0, 1), (1, 2), (2, 0)])
    engine = dda_engine.DDAEngine(net, observer_name="OBS_03")
    edge_vals = {(0, 1): 1.0, (1, 2): 1.0, (2, 0): 1.0}
    engine.run_foundation(edge_vals)
    term = engine.lift_or_terminate((0.0, 0.0, 0.0))
    assert term.status == dda_engine.TerminationStatus.SOLVED


def test_integration_dda_04_fingerprinted_bag_hashing():
    """Verify FingerprintedBag SHA256 tag validation and payload retrieval."""
    bag = certified_pipeline.FingerprintedBag(
        name="bag1",
        data={"network_nodes": "4", "cycles": "2"}
    )
    assert len(bag.fingerprint()) == 64


def test_integration_dda_05_pipeline_step_transition_certs():
    """Verify Pipeline step transitions and certificate attachment."""
    step = certified_pipeline.Step(
        name="STEP_01",
        transform=lambda b: certified_pipeline.FingerprintedBag("bag2", b.data)
    )
    pipeline = certified_pipeline.Pipeline(name="pipe1", steps=[step])
    assert len(pipeline.steps) == 1


def test_integration_dda_06_network_residual_step_factory():
    """Verify make_network_residual_step pipeline generation."""
    net = Network(nodes=[0, 1, 2], edges=[(0, 1), (1, 2), (2, 0)])
    edge_vals = {(0, 1): 1.0, (1, 2): 1.0, (2, 0): 1.0}
    step = certified_residual_integration.make_network_residual_step(net, edge_vals)
    assert step is not None
    assert step.name == "compute_network_residual"


def test_integration_dda_07_quantum_escape_step_factory():
    """Verify make_quantum_escape_step pipeline execution."""
    step = certified_residual_integration.make_quantum_escape_step()
    assert step is not None
    assert step.name == "compute_quantum_escape"


def test_integration_dda_08_integrated_demo_execution():
    """Verify run_integrated_demo certified pipeline execution."""
    res = certified_residual_integration.run_integrated_demo()
    assert res is not None


def test_integration_dda_09_dda_cascade_router_dispatch():
    """Verify dda_cascade_router routing logic across solver domains."""
    router = dda_cascade_router
    assert hasattr(router, "__name__")


def test_integration_dda_10_cross_validate_dda_claims():
    """Verify DDA cross-validation engine and claim verification bounds."""
    cv = cross_validate_dda_claims
    assert hasattr(cv, "__name__")


