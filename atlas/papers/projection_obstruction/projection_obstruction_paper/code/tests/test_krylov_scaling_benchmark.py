"""Finite numerical examples for sparse evolution, envelopes and Taylor jets.

Comparisons at sampled times do not qualify an all-time numerical certificate
or a general theorem. Interaction-norm envelopes need not be sharp.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from krylov_scaling_benchmark import (
    SpinChainModel,
    build_2d_grid_model,
    build_sparse_hamiltonian,
    compute_higher_order_expansion_and_timescale,
    run_single_scaling_benchmark,
    solve_mean_field_trajectory,
)


def test_sparse_hamiltonian_hermiticity_and_dimension() -> None:
    """Ensure constructed sparse Hamiltonian is strictly Hermitian with dimension 2^N."""
    model = SpinChainModel(num_qubits=6, j_xx=0.5, j_yy=0.5, j_zz=1.2, hx=0.7, hz=0.3)
    ham = build_sparse_hamiltonian(model)
    assert ham.shape == (64, 64)
    # Check Hermiticity: H - H^dagger == 0
    diff = ham - ham.conjugate().transpose()
    assert diff.nnz == 0 or np.max(np.abs(diff.data)) < 1.0e-14


def test_mean_field_norm_preservation() -> None:
    """Ensure mean-field integration strictly preserves state normalization."""
    model = SpinChainModel(num_qubits=6, j_zz=1.0, hx=0.8)
    initial_sites = [
        np.array([np.cos(0.2 * i), np.sin(0.2 * i)], dtype=np.complex128) for i in range(6)
    ]
    times = np.linspace(0.0, 0.5, 11, dtype=np.float64)
    trajectory = solve_mean_field_trajectory(model, initial_sites, times)

    assert len(trajectory) == 11
    for step_sites in trajectory:
        assert len(step_sites) == 6
        for site in step_sites:
            norm_val = float(np.linalg.norm(site))
            assert math.isclose(norm_val, 1.0, abs_tol=1.0e-12)


def test_duhamel_envelope_comparison_12_qubits_tfim() -> None:
    """Test Duhamel error bound vs exact Krylov evolution for 12-qubit TFIM chain."""
    model = SpinChainModel(num_qubits=12, j_zz=1.0, hx=1.0)
    # Tilted product state
    initial_sites = [np.array([np.cos(0.4), np.sin(0.4)], dtype=np.complex128) for _ in range(12)]
    res = run_single_scaling_benchmark(
        model, initial_sites, model_name="TFIM-12Q", t_max=0.15, num_steps=5
    )

    assert res.is_duhamel_bound_valid, "interaction envelope comparison failed"
    assert res.is_observable_bound_valid, "observable envelope comparison failed"
    assert res.max_trace_distance > 0.05
    assert res.mean_sharpness_ratio >= 1.0
    assert res.numerical_error_certified is False
    assert res.execution_time_seconds < 5.0


def test_duhamel_envelope_comparison_14_qubits_tfim() -> None:
    """Test Duhamel error bound vs exact Krylov evolution for 14-qubit TFIM chain."""
    model = SpinChainModel(num_qubits=14, j_zz=1.0, hx=0.8)
    initial_sites = [np.array([np.cos(0.35), np.sin(0.35)], dtype=np.complex128) for _ in range(14)]
    res = run_single_scaling_benchmark(
        model, initial_sites, model_name="TFIM-14Q", t_max=0.12, num_steps=4
    )

    assert res.is_duhamel_bound_valid
    assert res.is_observable_bound_valid
    assert res.mean_sharpness_ratio >= 1.0
    assert res.numerical_error_certified is False
    assert res.execution_time_seconds < 8.0


def test_duhamel_envelope_comparison_16_qubits_tfim() -> None:
    """Test Duhamel error bound vs exact Krylov evolution for 16-qubit TFIM chain."""
    model = SpinChainModel(num_qubits=16, j_zz=1.0, hx=0.7)
    initial_sites = [np.array([np.cos(0.3), np.sin(0.3)], dtype=np.complex128) for _ in range(16)]
    res = run_single_scaling_benchmark(
        model, initial_sites, model_name="TFIM-16Q", t_max=0.10, num_steps=3
    )

    assert res.is_duhamel_bound_valid
    assert res.is_observable_bound_valid
    assert res.mean_sharpness_ratio >= 1.0
    assert res.numerical_error_certified is False
    assert res.execution_time_seconds < 15.0


def test_duhamel_bound_xxz_quench_12_qubits() -> None:
    """Test Duhamel error bound under Heisenberg XXZ quench dynamics for 12 qubits."""
    model = SpinChainModel(num_qubits=12, j_xx=0.6, j_yy=0.6, j_zz=1.0, hz=0.4)
    # Staggered Néel-like state
    initial_sites = [
        np.array([np.cos(0.25 * ((-1) ** i)), np.sin(0.25 * ((-1) ** i))], dtype=np.complex128)
        for i in range(12)
    ]
    res = run_single_scaling_benchmark(
        model, initial_sites, model_name="XXZ-12Q", t_max=0.15, num_steps=4
    )

    assert res.is_duhamel_bound_valid
    assert res.is_observable_bound_valid
    assert res.mean_sharpness_ratio >= 1.0
    assert res.numerical_error_certified is False


def test_higher_order_expansion_boundary_coefficient_and_quartic_diagnostic() -> None:
    """Compare c2 and the quartic diagnostic for three internal couplings."""
    # 6-qubit chain: cut between site 2 and site 3.
    # A = {0, 1, 2}, B = {3, 4, 5}. Boundary bond is (2, 3).
    # Vary internal bulk couplings in A (bonds 0, 1) and B (bonds 3, 4).
    theta_vals = [0.2, 0.4, 0.7, 1.1, 0.5, 0.3]
    initial_sites = [np.array([np.cos(th), np.sin(th)], dtype=np.complex128) for th in theta_vals]

    c2_list = []
    c4_list = []
    tau_list = []

    for internal_j in [0.0, 1.0, 2.5]:
        bonds = [internal_j, internal_j, 1.2, internal_j, internal_j]
        model = SpinChainModel(
            num_qubits=6,
            bond_jzz=bonds,
            hx=0.6,
        )
        c2, c3, c4, tau_e = compute_higher_order_expansion_and_timescale(
            model, initial_sites, cut_site=2
        )
        c2_list.append(c2)
        c4_list.append(c4)
        tau_list.append(tau_e)

        # Time-reversal symmetry: c_3 must be zero
        assert abs(c3) < 1.0e-4, f"c_3 should vanish under real dynamics, got {c3}"

    # Verify c_2 area-law invariance across all internal couplings
    assert math.isclose(c2_list[0], c2_list[1], rel_tol=1.0e-3), (
        f"c_2 changed with internal coupling! {c2_list}"
    )
    assert math.isclose(c2_list[0], c2_list[2], rel_tol=1.0e-3), (
        f"c_2 changed with internal coupling! {c2_list}"
    )

    # Verify c_4 varies substantially with internal coupling while c_2 is invariant
    assert abs(c4_list[2] - c4_list[0]) > 0.5, f"c_4 did not vary with internal coupling: {c4_list}"

    # The quartic diagnostic varies for these three inputs; no remainder bound.
    assert abs(tau_list[2] - tau_list[0]) > 0.05, (
        f"tau_E did not shift with internal coupling: {tau_list}"
    )


def test_time_reversal_breaking_yields_odd_growth_c3() -> None:
    """Verify that breaking time-reversal symmetry generates an O(t^3) term c_3."""
    # Complex phase in state breaks time-reversal symmetry
    initial_sites = [
        np.array([np.cos(0.5), np.sin(0.5) * np.exp(0.5j)], dtype=np.complex128),
        np.array([np.cos(0.8), np.sin(0.8)], dtype=np.complex128),
        np.array([np.cos(0.3), np.sin(0.3)], dtype=np.complex128),
        np.array([np.cos(0.6), np.sin(0.6)], dtype=np.complex128),
    ]
    model = SpinChainModel(num_qubits=4, j_zz=1.0, hx=0.8, hy=0.4)
    c2, c3, c4, tau_e = compute_higher_order_expansion_and_timescale(
        model, initial_sites, cut_site=1
    )

    # This chosen Hamiltonian and complex state have a nonzero cubic term.
    assert abs(c3) > 0.05, f"c_3 should be non-zero when TR is broken, got {c3}"


def test_2d_lattice_geometry_area_law_and_connectivity_scaling() -> None:
    """Compare boundary coefficients and quartic ratios for three fixed geometries."""
    # 12 qubits in 1D vs 2D square vs 2D triangular
    theta = 0.6
    u_site = np.array([np.cos(theta), np.sin(theta)], dtype=np.complex128)
    initial_sites = [u_site.copy() for _ in range(12)]

    # 1D Chain: cut_site = 5 (between 5 and 6), exactly 1 boundary bond
    model_1d = SpinChainModel(num_qubits=12, j_zz=1.0, hx=0.8)
    c2_1d, c3_1d, c4_1d, tau_1d = compute_higher_order_expansion_and_timescale(
        model_1d, initial_sites, cut_site=5
    )

    # 2D Square: 3x4 grid, exactly 3 boundary bonds
    model_sq, cut_sq = build_2d_grid_model(3, 4, j_zz=1.0, hx=0.8, lattice_type="square")
    c2_sq, c3_sq, c4_sq, tau_sq = compute_higher_order_expansion_and_timescale(
        model_sq, initial_sites, cut_site=cut_sq
    )

    # 2D Triangular: 3x4 grid, exactly 5 boundary bonds (3 horizontal + 2 diagonal)
    model_tri, cut_tri = build_2d_grid_model(3, 4, j_zz=1.0, hx=0.8, lattice_type="triangular")
    c2_tri, c3_tri, c4_tri, tau_tri = compute_higher_order_expansion_and_timescale(
        model_tri, initial_sites, cut_site=cut_tri
    )

    # 1. Area law rate scaling: c2(2D Square) / c2(1D) == 3.000000
    assert math.isclose(c2_sq / c2_1d, 3.0, rel_tol=1.0e-3), (
        f"2D Square area law did not scale by 3! Got {c2_sq / c2_1d}"
    )

    # 2. Triangular area law rate scaling: c2(Triangular) / c2(Square) == 5/3
    assert math.isclose(c2_tri / c2_sq, 5.0 / 3.0, rel_tol=1.0e-3), (
        f"Triangular area law did not scale by 5/3! Got {c2_tri / c2_sq}"
    )

    # 3. Ratios decrease for these inputs, without a general monotonicity claim.
    assert tau_sq < tau_1d, f"Square tau_E ({tau_sq}) not smaller than 1D ({tau_1d})"
    assert tau_tri < tau_sq, f"Triangular tau_E ({tau_tri}) not smaller than Square ({tau_sq})"

    # 4. Sampled errors lie below the conservative interaction envelope
    res_sq = run_single_scaling_benchmark(
        model_sq, initial_sites, model_name="Square-12Q", t_max=0.15, num_steps=4
    )
    assert res_sq.is_duhamel_bound_valid
    assert res_sq.is_observable_bound_valid
    assert res_sq.numerical_error_certified is False
