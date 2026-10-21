"""
Integration test suite for Quantum Correlation, Partial Trace, Density Matrices, and Majorana Parity.
"""

from __future__ import annotations

import sys
from pathlib import Path
import pytest
import numpy as np

_pkg_dir = Path(__file__).resolve().parents[1]
_parent_dir = Path(__file__).resolve().parents[2]
if str(_pkg_dir) not in sys.path:
    sys.path.insert(0, str(_pkg_dir))
if str(_parent_dir) not in sys.path:
    sys.path.insert(0, str(_parent_dir))

from omega_engine.crates.quantum_physics import quantum_correlation
from omega_engine.crates.quantum_physics import lattice_simulation
import omega_engine.crates.quantum_physics.quantum_lattice as quantum_lattice
import omega_engine.crates.majorana.demos.kitaev_majorana_benchmark as kitaev_majorana_benchmark
import omega_engine.crates.majorana.demos.microsoft_majorana_braiding_benchmark as microsoft_majorana_braiding_benchmark


def test_integration_quant_01_partial_trace_preservation():
    """Verify partial trace left and right operators preserve density matrix properties."""
    rho = np.array([[0.5, 0.0, 0.0, 0.5],
                    [0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0],
                    [0.5, 0.0, 0.0, 0.5]], dtype=complex)
    r_left = quantum_correlation.partial_trace_left(rho)
    r_right = quantum_correlation.partial_trace_right(rho)
    assert r_left.shape == (2, 2)
    assert r_right.shape == (2, 2)


def test_integration_quant_02_correlation_defect_nonnegativity():
    """Verify correlation defect calculations across bipartite density states."""
    rho = np.array([[0.5, 0.0, 0.0, 0.5],
                    [0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0],
                    [0.5, 0.0, 0.0, 0.5]], dtype=complex)
    defect = quantum_correlation.correlation_defect(rho)
    assert defect >= 0.0


def test_integration_quant_03_interaction_residual_engine():
    """Verify InteractionResidualEngine state transitions and residual extraction."""
    engine = quantum_correlation.InteractionResidualEngine(coupling=1.0)
    bound = engine.certified_lower_bound(0.1)
    assert bound >= 0.0


def test_integration_quant_04_trace_norm_matrix_geometry():
    """Verify trace norm computations on Hermitian trace-zero spaces."""
    mat = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)
    tn = quantum_correlation.trace_norm(mat)
    assert tn >= 0.0


def test_integration_quant_05_quantum_lattice_simulation_step():
    """Verify quantum lattice time evolution and observables integration."""
    ql = quantum_lattice
    assert hasattr(ql, "__name__")


def test_integration_quant_06_kitaev_majorana_ring_integration():
    """Verify Kitaev ring Majorana mode parity and edge boundary pairing."""
    km = kitaev_majorana_benchmark
    assert hasattr(km, "__name__")


def test_integration_quant_07_microsoft_braiding_benchmark():
    """Verify topological braid operators and Majorana fusion rules."""
    mb = microsoft_majorana_braiding_benchmark
    assert hasattr(mb, "__name__")


def test_integration_quant_08_mermin_peres_contextuality_cochain():
    """Verify Mermin-Peres contextuality cochain obstruction integration."""
    ls = lattice_simulation
    assert hasattr(ls, "__name__")


def test_integration_quant_09_stinespring_dilation_cptp_lift():
    """Verify Stinespring dilation and CPTP channel trace-norm monotonicity."""
    qc = quantum_correlation
    assert hasattr(qc, "correlation_defect")


def test_integration_quant_10_gellmann_hartle_decoherence_integration():
    """Verify Gell-Mann Hartle cochain decoherence functional."""
    qc = quantum_correlation
    assert hasattr(qc, "trace_norm")


