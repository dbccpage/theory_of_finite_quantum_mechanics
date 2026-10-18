"""Smoke test for decomposed quantum_physics/quantum_correlation.py."""
import numpy as np
import pytest
from omega_engine.crates.quantum_physics.quantum_correlation import (
    InteractionResidualEngine,
    correlation_defect,
    partial_trace_left,
    partial_trace_right,
    trace_norm,
    EscapeRateCertificate,
)


def test_quantum_correlation_smoke():
    engine = InteractionResidualEngine(coupling=1.0)
    cert = engine.verify_bound()
    assert isinstance(cert, EscapeRateCertificate)
    assert cert.bound_verified


def test_old_coda_quantum_import_deleted():
    with pytest.raises(ImportError):
        import omega_engine.crates.coda.quantum_correlation  # type: ignore


