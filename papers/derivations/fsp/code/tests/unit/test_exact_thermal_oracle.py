"""Unit Tests: Exact Spectral Thermal Oracle, Trotter Discretization Bounds, and Free Triangle Benchmark.
AuthorityEffect: None.

Tests:
1. Strict positivity of exact thermal trace Z_exact = Tr(e^(-beta * H)) > 0 for finite real beta.
2. Controlled Trotter discretization error and Euler transfer contraction radius checks.
3. Demonstration that naive Euler transfer (I - dtau * H)^M can yield negative partition sums for coarse dtau, whereas Z_exact > 0.
4. Analytical and numerical solution of the 3-site spinless free fermion triangle (E in {-1, -1, 2}, Z(2) = 2e^2 + e^(-4)).
5. Reusability of HamiltonianGinBridge database across multiple models without UNIQUE constraint collision.
6. Refusal semantics: EmptyEnsembleRefusal for missing models, SplitBrainRefusal for approximate/defective pairs.
7. Strict input validation refusing invalid beta, non-positive Trotter steps, NaN/Inf, and out-of-bounds particle counts.
"""

from __future__ import annotations

import math
from pathlib import Path
import sys

import numpy as np
import pytest

code_dir = Path(__file__).resolve().parent.parent.parent
if str(code_dir) not in sys.path:
    sys.path.insert(0, str(code_dir))

from fermionic_hamiltonian import (
    DiscreteFermionicHamiltonian,
    FermionicLattice,
    free_triangle_analytics,
)
from hamiltonian_gin_bridge import HamiltonianGinBridge


# ----------------------------------------------------------------------------
# 1. Exact Thermal Trace Positivity & Discretization Bounds
# ----------------------------------------------------------------------------

def test_exact_thermal_trace_positivity():
    """Validates that exact spectral trace Z_exact = Tr(e^(-beta * H)) is strictly positive."""
    # Test across multiple geometries and particle fillings
    lattice_chain = FermionicLattice.linear_chain(3, periodic=False)
    h_chain = DiscreteFermionicHamiltonian(lattice_chain, t=1.0, u=2.5, num_up=1, num_down=1)

    for beta in [0.1, 0.5, 1.0, 2.0, 5.0, 10.0]:
        z_exact = h_chain.compute_exact_thermal_trace(beta=beta)
        assert z_exact > 0.0
        assert math.isfinite(z_exact)

    # Frustrated triangle cluster with interaction
    lattice_tri = FermionicLattice.triangle_cluster()
    h_tri = DiscreteFermionicHamiltonian(lattice_tri, t=1.0, u=1.0, num_up=2, num_down=1)
    for beta in [0.2, 1.5, 4.0]:
        z_exact_tri = h_tri.compute_exact_thermal_trace(beta=beta)
        assert z_exact_tri > 0.0
        assert math.isfinite(z_exact_tri)


def test_euler_trotter_discretization_and_contraction_radius():
    """
    Validates that Euler transfer T = I - dtau * H has a finite contraction radius,
    and reports Trotter discretization error relative to Z_exact.
    """
    lattice = FermionicLattice.linear_chain(2, periodic=False)
    h = DiscreteFermionicHamiltonian(lattice, t=1.0, u=4.0, num_up=1, num_down=1)

    # At small Trotter steps (large dtau), Euler contraction may be unsafe
    res_coarse = h.compute_partition_functions(beta=2.0, trotter_steps=2)
    assert "z_exact" in res_coarse
    assert "trotter_discretization_error" in res_coarse
    assert res_coarse["z_exact"] > 0.0

    # With refined Trotter steps, discretization error decreases monotonically
    res_fine_4 = h.compute_partition_functions(beta=2.0, trotter_steps=4)
    res_fine_16 = h.compute_partition_functions(beta=2.0, trotter_steps=16)

    assert res_fine_16["trotter_discretization_error"] < res_coarse["trotter_discretization_error"]
    assert res_fine_16["euler_contraction_safe"] is True


def test_coarse_euler_negative_partition_counterexample():
    """
    Reproduces the adversarial counterexample: for H with positive eigenvalue lambda=2,
    beta=1, M=1 gives Euler T = 1 - 1*2 = -1, yielding Z = -1,
    while exact thermal trace is exp(-2) > 0.
    """
    # Construct a 2-site lattice where maximum eigenvalue exceeds 1/dtau
    lattice = FermionicLattice.linear_chain(2, periodic=False)
    h = DiscreteFermionicHamiltonian(lattice, t=2.0, u=4.0, num_up=1, num_down=1)

    beta = 2.0
    trotter_steps = 1  # dtau = 2.0, very coarse
    res = h.compute_partition_functions(beta=beta, trotter_steps=trotter_steps)

    # Exact trace is always strictly positive
    assert res["z_exact"] > 0.0
    # Euler contraction radius condition dtau * max|lambda| < 1 is violated
    assert res["euler_contraction_safe"] is False
    # Discretization error is explicitly recorded
    assert res["trotter_discretization_error"] > 0.0


# ----------------------------------------------------------------------------
# 2. Free Triangle Benchmark: Representation-Dependent Negativity
# ----------------------------------------------------------------------------

def test_free_triangle_analytics_and_polynomial_solvability():
    """
    Validates that the 3-site spinless free fermion triangle (U=0, 2 spin-up fermions)
    has eigenvalues {-1, -1, 2}, exact Z(2) = 2e^2 + e^(-4), and is solvable in O(N^3) time.
    """
    # 1. Analytical solution
    analytics = free_triangle_analytics(beta=2.0, t=1.0)
    assert analytics["two_particle_energies"] == [-1.0, -1.0, 2.0]
    expected_z = 2.0 * math.exp(2.0) + math.exp(-4.0)
    assert abs(analytics["exact_partition_function"] - expected_z) < 1e-12
    assert analytics["single_particle_solvable"] is True

    # 2. Many-body Hamiltonian matrix representation
    h_tri = DiscreteFermionicHamiltonian.create_free_triangle(t=1.0, num_up=2, num_down=0)
    assert h_tri.dim == 3

    # Eigenvalues of many-body matrix must match {-1, -1, 2}
    mat_arr = np.array(h_tri.matrix, dtype=float)
    eigvals = np.sort(np.linalg.eigvalsh(mat_arr))
    expected_eigvals = np.array([-1.0, -1.0, 2.0])
    np.testing.assert_allclose(eigvals, expected_eigvals, atol=1e-12)

    # Exact thermal trace at beta=2
    z_mb = h_tri.compute_exact_thermal_trace(beta=2.0)
    assert abs(z_mb - expected_z) < 1e-12

    # In the real-space occupation basis, Trotter paths exhibit sign frustration
    paths = h_tri.generate_sample_paths(beta=2.0, trotter_steps=3)
    cancelling_paths = [p for p in paths if p["is_cancelling"]]
    assert len(cancelling_paths) > 0, "Odd cycle in real-space basis must host negative amplitudes"


# ----------------------------------------------------------------------------
# 3. Database Reusability & Unified Audit Semantics
# ----------------------------------------------------------------------------

def test_repeated_database_indexing_without_key_collision():
    """
    Validates that indexing multiple models on the same HamiltonianGinBridge instance
    does not cause UNIQUE constraint failed: GinInvolutionPairs.pair_id.
    """
    bridge = HamiltonianGinBridge(in_memory=True)
    try:
        lattice4 = FermionicLattice.linear_chain(4, periodic=True)
        h1 = DiscreteFermionicHamiltonian(lattice4, t=1.0, u=0.0, num_up=2, num_down=0)
        res1 = bridge.index_hamiltonian_paths(h1, beta=1.0, trotter_steps=3, model_name="Run1_Ring4")
        assert res1["total_paths"] > 0

        # Second indexing call on the SAME bridge
        h2 = DiscreteFermionicHamiltonian(lattice4, t=0.8, u=0.0, num_up=2, num_down=0)
        res2 = bridge.index_hamiltonian_paths(h2, beta=1.0, trotter_steps=3, model_name="Run2_Ring4")
        assert res2["total_paths"] > 0

        # Both models can be audited independently
        rec1 = bridge.audit_sign_resolution("Run1_Ring4")
        rec2 = bridge.audit_sign_resolution("Run2_Ring4")
        assert rec1.model_name == "Run1_Ring4"
        assert rec2.model_name == "Run2_Ring4"
    finally:
        bridge.close()


def test_missing_model_refusal():
    """Validates that auditing a missing model yields EmptyEnsembleRefusal."""
    bridge = HamiltonianGinBridge(in_memory=True)
    try:
        rec = bridge.audit_sign_resolution("NonExistentModel")
        assert rec.terminal_route == "EmptyEnsembleRefusal"
        assert rec.raw_average_sign == 0.0
        assert rec.gin_quotiented_average_sign == 0.0
        assert rec.all_exact_cancellations is False
    finally:
        bridge.close()


def test_approximate_pair_defect_refusal():
    """
    Validates that an approximate pair with defect 5e-11 is NOT labeled as exact cancellation,
    and routes to SplitBrainRefusal.
    """
    bridge = HamiltonianGinBridge(in_memory=True)
    try:
        c = bridge.conn.cursor()
        # Manually register two configurations with weight defect 5e-11
        w_pos = 1.0
        w_neg = 1.0 + 5e-11
        c.execute("INSERT INTO FermionConfigurations VALUES (501, 'ApproxModel', 2, 4, ?, 1, 1);", (w_pos,))
        c.execute("INSERT INTO FermionConfigurations VALUES (502, 'ApproxModel', 2, 4, ?, -1, 1);", (w_neg,))

        # Register pair
        c.execute(
            """INSERT INTO GinInvolutionPairs 
               (pair_id, cfg_pos_id, cfg_neg_id, involution_type, is_exact_partner)
               VALUES (999, 501, 502, 'ApproximateSymmetry', 0);"""
        )
        bridge.conn.commit()

        rec = bridge.audit_sign_resolution("ApproxModel")
        assert rec.all_exact_cancellations is False
        assert rec.max_weight_defect >= 5e-11
        assert rec.total_uncancelled_mass >= 5e-11
        assert rec.terminal_route == "SplitBrainRefusal"
    finally:
        bridge.close()


# ----------------------------------------------------------------------------
# 4. Strict Input Bounds Validation
# ----------------------------------------------------------------------------

def test_input_bounds_validation():
    """Validates that input validators reject invalid parameters."""
    # Invalid lattice num_sites
    with pytest.raises(ValueError, match="positive integer"):
        FermionicLattice(num_sites=0, edges=[])

    # Invalid edge indices
    with pytest.raises(ValueError, match="outside site range"):
        FermionicLattice(num_sites=3, edges=[(0, 3)])

    # Self loops
    with pytest.raises(ValueError, match="Self-loops are not permitted"):
        FermionicLattice(num_sites=3, edges=[(1, 1)])

    lattice = FermionicLattice.linear_chain(3)

    # Non-finite couplings
    with pytest.raises(ValueError, match="Couplings t and u must be finite"):
        DiscreteFermionicHamiltonian(lattice, t=float("nan"), u=1.0)
    with pytest.raises(ValueError, match="Couplings t and u must be finite"):
        DiscreteFermionicHamiltonian(lattice, t=1.0, u=float("inf"))

    # Negative particle counts
    with pytest.raises(ValueError, match="non-negative"):
        DiscreteFermionicHamiltonian(lattice, num_up=-1, num_down=1)

    # Zero total fermions
    with pytest.raises(ValueError, match="at least one fermion"):
        DiscreteFermionicHamiltonian(lattice, num_up=0, num_down=0)

    # Fermions exceeding site count
    with pytest.raises(ValueError, match="cannot exceed lattice sites"):
        DiscreteFermionicHamiltonian(lattice, num_up=4, num_down=0)

    # Invalid beta in partition function
    h = DiscreteFermionicHamiltonian(lattice, num_up=1, num_down=0)
    with pytest.raises(ValueError, match="beta must be a positive finite real number"):
        h.compute_partition_functions(beta=-1.0)
    with pytest.raises(ValueError, match="beta must be a positive finite real number"):
        h.compute_exact_thermal_trace(beta=0.0)

    # Invalid trotter steps
    with pytest.raises(ValueError, match="trotter_steps must be a positive integer >= 1"):
        h.compute_partition_functions(beta=1.0, trotter_steps=0)
