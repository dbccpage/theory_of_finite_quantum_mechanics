"""Bounds compared with actual trajectories and witness counterexamples."""

import numpy as np
import pytest
from coda_higher_cell.defect_bounds import (
    duhamel_observable_certificate,
    evaluate_k_party_trace_defect,
    operator_norm,
    schatten1_dual_witness,
    schatten_1_norm,
    short_time_k_party_defect_lower_bound,
)
from coda_higher_cell.k_cell_retraction import k_cell_normal_projector


@pytest.mark.parametrize("t", [0, 0.001, 0.005, 1 / 54, 0.05, 0.2])
def test_short_time_bound_against_analytic_ghz_state(t):
    psi = np.zeros(8, dtype=complex)
    psi[0], psi[7] = np.cos(t), -1j * np.sin(t)
    state = np.outer(psi, psi.conj())
    bound, threshold, in_window = short_time_k_party_defect_lower_bound(2, 3, 1, t)
    assert threshold == pytest.approx(1 / 54)
    assert in_window == (t <= threshold)
    assert evaluate_k_party_trace_defect(state, [2] * 3) + 1e-12 >= bound


def test_zero_initial_speed_does_not_imply_future_factorization():
    x, z = np.array([[0, 1], [1, 0]]), np.diag([1, -1])
    h = np.kron(x, np.eye(2)) + np.kron(z, x)
    rho0 = np.diag([1.0, 0.0])
    rho = np.kron(rho0, rho0)
    velocity = -1j * (h @ rho - rho @ h)
    assert np.allclose(k_cell_normal_projector(velocity, [rho0] * 2, [2] * 2), 0)
    t = 0.1
    psi = np.array(
        [
            np.cos(np.sqrt(2) * t),
            -1j * np.sin(np.sqrt(2) * t) / np.sqrt(2),
            -1j * np.sin(np.sqrt(2) * t) / np.sqrt(2),
            0,
        ]
    )
    assert evaluate_k_party_trace_defect(np.outer(psi, psi.conj()), [2, 2]) > 0.01


def test_classical_separable_state_has_defect_one():
    assert evaluate_k_party_trace_defect(np.diag([0.5, 0, 0, 0.5]), [2, 2]) == pytest.approx(1)


def test_polar_witness_does_not_annihilate_tangents():
    rhos = [np.diag([0.75, 0.25]), np.diag([1 / 3, 2 / 3])]
    n = np.diag([1, -1, -1, 1])
    assert np.allclose(k_cell_normal_projector(n, rhos, [2, 2]), n)
    w, norm, error = schatten1_dual_witness(n)
    assert norm == pytest.approx(1)
    assert error < 1e-12
    tangent = np.kron(np.diag([1, -1]), rhos[1])
    assert np.vdot(w, tangent) == pytest.approx(-2 / 3)


@pytest.mark.parametrize("shape", [(4, 4), (3, 2), (2, 3)])
def test_complex_polar_alignment(shape):
    rng = np.random.default_rng(21)
    n = rng.normal(size=shape) + 1j * rng.normal(size=shape)
    w, norm, err = schatten1_dual_witness(n)
    assert norm <= 1 + 1e-12
    assert err < 1e-12
    assert np.vdot(w, n) == pytest.approx(schatten_1_norm(n))


def test_zero_and_thresholded_witness():
    w, norm, error = schatten1_dual_witness(np.zeros((2, 2)))
    assert np.array_equal(w, np.zeros((2, 2))) and norm == 0 and error == 0
    _, _, error = schatten1_dual_witness(np.diag([1, 1e-8]), tol=1e-7)
    assert error == pytest.approx(1e-8)


def test_duhamel_calculation():
    assert duhamel_observable_certificate(np.diag([2, -2]), 0.05) == pytest.approx(0.1)


@pytest.mark.parametrize(
    "args",
    [
        (np.nan, 3, 1, 0),
        (2, 3, np.inf, 0),
        (2, 3, 1, -1),
        (-2, 3, 1, 0),
        (2, 1, 1, 0),
        (2, 2.5, 1, 0),
        (2, 3, 0, 0),
    ],
)
def test_invalid_bound_inputs(args):
    with pytest.raises(ValueError):
        short_time_k_party_defect_lower_bound(*args)


def test_degenerate_bound_inputs():
    assert short_time_k_party_defect_lower_bound(0, 3, 0, 1) == (0, 0, False)
    value, threshold, flag = short_time_k_party_defect_lower_bound(0, 3, 1, 0)
    assert value == 0 and threshold == 0 and not flag
    with pytest.raises(ValueError):
        duhamel_observable_certificate(np.eye(2), -0.1)


@pytest.mark.parametrize("operator", [np.full((2, 2), np.nan), np.array([]), np.ones(2)])
def test_invalid_norm_inputs(operator):
    with pytest.raises(ValueError):
        operator_norm(operator)


@pytest.mark.parametrize("g,t", [(1e300, 1), (1e-300, 1), (1, 1e300)])
def test_unrepresentable_bound_inputs(g, t):
    with pytest.raises(ValueError):
        short_time_k_party_defect_lower_bound(2, 3, g, t)
