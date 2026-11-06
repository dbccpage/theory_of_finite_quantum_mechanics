"""Tests of retained finite calculations and declared fixtures.
Physical recovery and removed certificate wrappers are outside this test scope.
"""

import subprocess
from pathlib import Path

import numpy as np
import yaml
from cdt_zolotarev_evaluator import (
    LanczosSignApproximation,
    MultiShiftCGSolver,
    ZolotarevRationalApproximation,
)






def test_rational_sign_error_on_independent_grid():
    """Checks rational-sign error on a second finite sample grid; no supremum bound."""
    eps = 0.05
    degree_m = 10
    zolo = ZolotarevRationalApproximation.compute(eps, degree_m)

    assert len(zolo.poles) == degree_m
    assert len(zolo.zeros) == degree_m
    assert len(zolo.residues) == degree_m

    # Error on sample grid in [eps, 1]
    x_test = np.linspace(eps, 1.0, 200)
    errors = [abs(1.0 - ZolotarevRationalApproximation.evaluate_scalar(x, zolo)) for x in x_test]
    max_err = max(errors)

    assert 0 <= zolo.sampled_max_error <= 1e-9
    assert max_err <= 1e-9

    # Pointwise error expression on this sample only; not a global GW bound.
    gw_bound = 2.0 * max_err + max_err**2
    assert gw_bound <= 1e-8




def test_multishift_cg_simultaneous_convergence():
    """Validates that multi-shift CG solves all shifted systems simultaneously."""
    np.random.seed(42)
    n = 24
    m_shifts = 6
    # Create Hermitian positive definite matrix A = H^2
    M = np.random.randn(n, n) + 1j * np.random.randn(n, n)
    A = M.conj().T @ M + 0.1 * np.eye(n)
    shifts = list(np.linspace(0.01, 2.0, m_shifts))
    b = np.random.randn(n) + 1j * np.random.randn(n)

    sols, iters, max_res = MultiShiftCGSolver.solve(A, shifts, b, tol=1e-10)

    assert iters <= 50
    assert max_res <= 1e-8

    # Compare with exact np.linalg.solve for each shift
    I = np.eye(n, dtype=complex)
    for l, s in enumerate(shifts):
        exact_x = np.linalg.solve(A + s * I, b)
        rel_diff = np.linalg.norm(sols[l] - exact_x) / np.linalg.norm(exact_x)
        assert rel_diff <= 1e-8


def test_lanczos_sign_approximation_convergence():
    """Validates Lanczos sign projection approximation against exact matrix sign function."""
    np.random.seed(42)
    n = 20
    M = np.random.randn(n, n) + 1j * np.random.randn(n, n)
    H = 0.5 * (M + M.conj().T) + 0.5 * np.eye(n)
    v = np.random.randn(n) + 1j * np.random.randn(n)

    # Exact sign
    evals, evecs = np.linalg.eigh(H)
    sgn_exact = evecs @ np.diag(np.sign(evals)) @ evecs.conj().T
    target = sgn_exact @ v

    # Lanczos approximation
    approx = LanczosSignApproximation.apply(H, v, k_steps=20)
    err = np.linalg.norm(approx - target) / np.linalg.norm(target)
    assert err <= 0.20  # Krylov subspace bounds direction
