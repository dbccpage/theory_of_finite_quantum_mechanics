"""CPTP quantum channel measure-and-prepare rigidity on trace-zero Hermitian space H_n^0 for GS-001.

AuthorityEffect: None.
"""

from __future__ import annotations

from typing import Callable, Sequence
import numpy as np

Gauge = Callable[[np.ndarray], float]


def is_hermitian_trace_zero(X: np.ndarray, atol: float = 1e-9) -> bool:
    """Check whether matrix X is a Hermitian trace-zero matrix X in H_n^0."""
    arr = np.asarray(X, dtype=complex)
    if arr.ndim != 2 or arr.shape[0] != arr.shape[1]:
        return False
    is_herm = bool(np.allclose(arr, arr.conj().T, atol=atol))
    is_tr_zero = bool(abs(np.trace(arr)) < atol)
    return is_herm and is_tr_zero


def trace_norm(X: np.ndarray) -> float:
    """Trace norm ||X||_1 = Tr(|X|) = sum singular values on H_n^0."""
    arr = np.asarray(X, dtype=complex)
    s = np.linalg.svd(arr, compute_uv=False)
    return float(np.sum(s))


def cptp_measure_and_prepare(
    X: np.ndarray, Y: np.ndarray
) -> tuple[Callable[[np.ndarray], np.ndarray], Sequence[np.ndarray]]:
    """Construct exact CPTP measure-and-prepare quantum channel Lambda_{X -> Y} on H_n^0.

    For X, Y in H_n^0 with equal trace norm ||X||_1 = ||Y||_1 = 2t:
    1. Spectral decompose X = X_+ - X_- with Tr(X_+) = Tr(X_-) = t.
    2. Measure projection P_+ onto supp(X_+) vs P_- = I - P_+.
    3. Prepare Y_+ / t when P_+ triggers, and Y_- / t when P_- triggers.

    Returns (channel_fn, kraus_operators).
    """
    X_arr = np.asarray(X, dtype=complex)
    Y_arr = np.asarray(Y, dtype=complex)

    if not is_hermitian_trace_zero(X_arr):
        raise ValueError("X must be a Hermitian trace-zero matrix in H_n^0")
    if not is_hermitian_trace_zero(Y_arr):
        raise ValueError("Y must be a Hermitian trace-zero matrix in H_n^0")

    norm_X = trace_norm(X_arr)
    norm_Y = trace_norm(Y_arr)

    if abs(norm_X - norm_Y) > 1e-7:
        raise ValueError(
            f"Trace norm mismatch: ||X||_1={norm_X:.4f} != ||Y||_1={norm_Y:.4f}"
        )
    if norm_X <= 1e-12:
        raise ValueError("Matrix X must be non-zero")

    t = norm_X / 2.0

    # Spectral decomposition of X = sum lambda_i |v_i><v_i|
    evals_x, evecs_x = np.linalg.eigh(X_arr)
    pos_mask_x = evals_x > 1e-12

    # Projections P_+ and P_-
    n = X_arr.shape[0]
    P_pos = np.zeros((n, n), dtype=complex)
    for i in np.where(pos_mask_x)[0]:
        v = evecs_x[:, i : i + 1]
        P_pos += v @ v.conj().T

    P_neg = np.eye(n, dtype=complex) - P_pos

    # Spectral decomposition of Y = Y_+ - Y_-
    evals_y, evecs_y = np.linalg.eigh(Y_arr)
    Y_pos = np.zeros((n, n), dtype=complex)
    Y_neg = np.zeros((n, n), dtype=complex)

    for i, lam in enumerate(evals_y):
        v = evecs_y[:, i : i + 1]
        if lam > 1e-12:
            Y_pos += lam * (v @ v.conj().T)
        elif lam < -1e-12:
            Y_neg += (-lam) * (v @ v.conj().T)

    rho_pos = Y_pos / t
    rho_neg = Y_neg / t

    # Kraus operators for measure-and-prepare channel
    # Lambda(A) = Tr(P_+ A) rho_pos + Tr(P_- A) rho_neg
    kraus_ops = []

    # Eigenspaces of rho_pos and rho_neg
    evals_rpos, evecs_rpos = np.linalg.eigh(rho_pos)
    evals_rneg, evecs_rneg = np.linalg.eigh(rho_neg)

    # For P_+ measurement -> prepare rho_pos = sum p_i |r_i><r_i|
    for i, p_i in enumerate(evals_rpos):
        if p_i > 1e-12:
            r_i = evecs_rpos[:, i : i + 1]
            # Kraus K_{pos,i} = sqrt(p_i) r_i v_pos^T
            # For each basis vector in P_+ support
            for j in np.where(pos_mask_x)[0]:
                v_j = evecs_x[:, j : j + 1]
                K = np.sqrt(p_i) * (r_i @ v_j.conj().T)
                kraus_ops.append(K)

    # For P_- measurement -> prepare rho_neg
    for i, q_i in enumerate(evals_rneg):
        if q_i > 1e-12:
            s_i = evecs_rneg[:, i : i + 1]
            for j in range(n):
                if not pos_mask_x[j]:
                    v_j = evecs_x[:, j : j + 1]
                    K = np.sqrt(q_i) * (s_i @ v_j.conj().T)
                    kraus_ops.append(K)

    def channel(A: np.ndarray) -> np.ndarray:
        arr_A = np.asarray(A, dtype=complex)
        tr_pos = np.trace(P_pos @ arr_A)
        tr_neg = np.trace(P_neg @ arr_A)
        return tr_pos * rho_pos + tr_neg * rho_neg

    return channel, kraus_ops


def is_cptp_trace_norm_rigid(
    X: np.ndarray, Y: np.ndarray, gauge: Gauge
) -> tuple[bool, float, float]:
    """Verify bidirectional CPTP contractivity j(Lambda(X)) <= j(X) and j(Lambda_inv(Y)) <= j(Y).

    Shows j(X) = j(Y) whenever ||X||_1 = ||Y||_1, forcing j = c ||.||_1 on H_n^0.
    Returns (is_equal, j_X, j_Y).
    """
    ch_xy, _ = cptp_measure_and_prepare(X, Y)
    ch_yx, _ = cptp_measure_and_prepare(Y, X)

    LX = ch_xy(X)
    LY = ch_yx(Y)

    j_X = gauge(X)
    j_LX = gauge(LX)
    j_Y = gauge(Y)
    j_LY = gauge(LY)

    # Bidirectional contractivity forces j(X) = j(Y)
    is_rigid = bool(
        np.isclose(j_X, j_Y, atol=1e-6) and j_LX <= j_X + 1e-6 and j_LY <= j_Y + 1e-6
    )
    return is_rigid, j_X, j_Y
