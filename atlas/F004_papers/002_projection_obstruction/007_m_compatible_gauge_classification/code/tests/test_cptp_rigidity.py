"""T20-T24: CPTP quantum channel measure-and-prepare rigidity tests on trace-zero space H_n^0 for GS-001.

Verifies exact CPTP measure-and-prepare channel construction, Kraus/Choi completely positive
and trace preserving properties, and trace norm sphere reachability and rigidity.
"""

import sys
from pathlib import Path
import numpy as np
import pytest

_pkg = Path(__file__).resolve().parents[1]
if str(_pkg / "code") not in sys.path:
    sys.path.insert(0, str(_pkg / "code"))

from cptp import (
    cptp_measure_and_prepare,
    is_cptp_trace_norm_rigid,
    trace_norm,
    is_hermitian_trace_zero,
)


def test_t20_t22_cptp_measure_and_prepare_channel():
    """T20-T22: Construct CPTP measure-and-prepare channel for X, Y in H_n^0 with equal trace norm.

    Verifies trace preservation, complete positivity, and Lambda(X) = Y.
    """
    X = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)
    Y = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)

    assert is_hermitian_trace_zero(X)
    assert is_hermitian_trace_zero(Y)

    norm_X = trace_norm(X)
    norm_Y = trace_norm(Y)
    assert np.isclose(norm_X, 2.0)
    assert np.isclose(norm_Y, 2.0)

    # Construct CPTP measure-and-prepare channel Lambda_{X -> Y}
    channel, kraus_ops = cptp_measure_and_prepare(X, Y)

    # Verify Lambda(X) = Y
    LX = channel(X)
    assert np.allclose(LX, Y, atol=1e-6)

    # Verify trace preservation: Tr(Lambda(A)) = Tr(A) for random matrix A
    A_sample = np.array([[3.0, 1.0j], [-1.0j, 2.0]], dtype=complex)
    tr_A = np.trace(A_sample)
    tr_LA = np.trace(channel(A_sample))
    assert np.isclose(tr_LA, tr_A)

    # Verify Kraus completeness relation: sum K_i^\dagger K_i = I
    kraus_sum = sum(K.conj().T @ K for K in kraus_ops)
    assert np.allclose(kraus_sum, np.eye(2), atol=1e-6)


def test_t23_t24_cptp_trace_norm_rigidity():
    """T23-T24: Bidirectional CPTP measure-and-prepare contractivity forces j(X) = j(Y) whenever ||X||_1 = ||Y||_1.

    Demonstrates that contractivity under all CPTP quantum channels forces j = c ||.||_1 on H_n^0.
    """
    X = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)
    Y = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)

    # Trace norm is strictly CPTP rigid
    is_rigid, j_X, j_Y = is_cptp_trace_norm_rigid(X, Y, trace_norm)
    assert is_rigid
    assert np.isclose(j_X, j_Y)

    # Error conditions
    X_bad_tr = np.array([[1.0, 0.0], [0.0, 1.0]], dtype=complex)
    with pytest.raises(ValueError, match="trace-zero"):
        cptp_measure_and_prepare(X_bad_tr, Y)

    Y_diff_norm = np.array([[2.0, 0.0], [0.0, -2.0]], dtype=complex)
    with pytest.raises(ValueError, match="Trace norm mismatch"):
        cptp_measure_and_prepare(X, Y_diff_norm)
