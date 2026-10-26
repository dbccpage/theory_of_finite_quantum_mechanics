"""Injected-fault mutants for CODA-A decision procedures.

Each mutant locally redefines one production decision. Tests assert that the
mutant disagrees with the real oracle on a known packet from test_coda_a.py,
so the suite kills the fault if it is ever injected into production.

Reconstruction A: residual C x = x - C x is zero iff C x = x; C(residual)=0
needs C C = C; T transports residuals only when T C = D T.
"""

from __future__ import annotations

from typing import Any

import pytest
from coda_a_core import (
    AuthEvidence,
    Terminal,
    _validate_exact_rational,
    classify_closure_attempt,
    is_projection,
    maps_commute,
    residual,
    residual_in_kernel,
    residual_transport,
)
from sympy import Float, Matrix, Rational


def _axis_projection() -> Matrix:
    return Matrix([[1, 0], [0, 0]])


def _unfixed() -> Matrix:
    return Matrix([[3], [4]])


def _fixed() -> Matrix:
    return Matrix([[3], [0]])


def _nilpotent_not_projection() -> Matrix:
    return Matrix([[0, 1], [0, 0]])


def _commuting_transport() -> Matrix:
    return Matrix([[2, 0], [0, 2]])


def _swap() -> Matrix:
    return Matrix([[0, 1], [1, 0]])


def _d0() -> Matrix:
    return Matrix([[1], [2]])


def _absorbed_defect() -> Matrix:
    return Matrix([[2], [4]])


def _anomalon_defect() -> Matrix:
    return Matrix([[1], [-1]])


def mutant_residual_as_zero(C: Matrix, x: Matrix) -> Matrix:
    """Treat residual as zero even when C x != x."""
    del C
    col = Matrix(x)
    if col.rows == 1:
        col = col.T
    return Matrix.zeros(col.rows, 1)


def mutant_residual_wrong_sign(C: Matrix, x: Matrix) -> Matrix:
    """Compute x + C x instead of x - C x."""
    col = Matrix(x)
    return col + C * col


def mutant_skip_idempotence_claim_kernel(C: Matrix, x: Matrix) -> Matrix:
    """Skip C C = C and still claim C(residual) = 0."""
    del C
    col = Matrix(x)
    if col.rows == 1:
        col = col.T
    return Matrix.zeros(col.rows, 1)


def mutant_treat_commute_optional(T: Matrix, C: Matrix, D: Matrix, x: Matrix) -> Matrix:
    """Return T(residual C x) even when T C != D T."""
    del D
    return Matrix(T) * residual(C, x)


def mutant_validate_accept_float(val: Any, name: str) -> Rational:
    """Accept IEEE 754 floats by converting them instead of refusing."""
    if isinstance(val, bool):
        raise TypeError(f"{name} must be an exact rational or integer, got bool")
    if isinstance(val, (float, Float)):
        return Rational(val)
    val_dtype = getattr(val, "dtype", None)
    if val_dtype is not None and "float" in str(val_dtype).lower():
        return Rational(val)
    return _validate_exact_rational(val, name)


def _real_float_outcome(val: Any) -> Any:
    try:
        return _validate_exact_rational(val, "x")
    except TypeError as exc:
        if "float" in str(exc):
            return "refused_float"
        raise


def _real_kernel_outcome(C: Matrix, x: Matrix) -> Any:
    try:
        return residual_in_kernel(C, x)
    except ValueError as exc:
        if "idempotence" in str(exc):
            return "refused_not_idempotent"
        raise


def _real_transport_outcome(C: Matrix, D: Matrix, T: Matrix, x: Matrix) -> Any:
    try:
        return residual_transport(C, D, T, x)
    except ValueError as exc:
        if "commuting" in str(exc):
            return "refused_noncommuting"
        raise


def test_mutant_residual_as_zero_killed_when_not_fixed() -> None:
    # Invariant: residual C x = 0 iff C x = x; a nonzero leftover is not absorbed.
    C = _axis_projection()
    x = _unfixed()
    fixed = _fixed()

    assert (C * fixed).equals(fixed)
    assert residual(C, fixed).is_zero_matrix
    assert mutant_residual_as_zero(C, fixed).equals(residual(C, fixed))

    assert not (C * x).equals(x)
    real_leftover = residual(C, x)
    mutant_leftover = mutant_residual_as_zero(C, x)
    assert real_leftover == Matrix([[0], [4]])
    assert not real_leftover.is_zero_matrix
    assert mutant_leftover.is_zero_matrix
    assert mutant_leftover != real_leftover


def test_mutant_residual_wrong_sign_killed() -> None:
    # Invariant: residual C x = x - C x, NOT x + C x.
    C = _axis_projection()
    x = Matrix([[3], [4]])
    real_leftover = residual(C, x)
    mutant_leftover = mutant_residual_wrong_sign(C, x)
    assert real_leftover == Matrix([[0], [4]])
    assert mutant_leftover == Matrix([[6], [4]])
    assert real_leftover != mutant_leftover


def test_mutant_skip_idempotence_killed_on_non_projection() -> None:
    # Invariant: C(residual)=0 is claimed only under C C = C.
    C = _axis_projection()
    N = _nilpotent_not_projection()
    x = _unfixed()
    nvec = Matrix([[0], [1]])

    assert is_projection(C)
    real_ok = residual_in_kernel(C, x)
    mutant_ok = mutant_skip_idempotence_claim_kernel(C, x)
    assert real_ok.is_zero_matrix
    assert mutant_ok.equals(real_ok)

    leftover_N = residual(N, nvec)
    assert not is_projection(N)
    assert leftover_N == Matrix([[-1], [1]])
    assert not (N * leftover_N).is_zero_matrix
    real_bad = _real_kernel_outcome(N, nvec)
    mutant_bad = mutant_skip_idempotence_claim_kernel(N, nvec)
    assert real_bad == "refused_not_idempotent"
    assert mutant_bad.is_zero_matrix
    assert mutant_bad != real_bad


def test_mutant_commute_optional_killed_when_T_does_not_intertwine() -> None:
    # Invariant: T(residual C x) = residual D (T x) only when T C = D T.
    C = _axis_projection()
    x = _unfixed()
    T = _commuting_transport()
    S = _swap()

    assert maps_commute(T, C, C)
    real_ok = residual_transport(C, C, T, x)
    mutant_ok = mutant_treat_commute_optional(T, C, C, x)
    assert (T * residual(C, x)).equals(real_ok)
    assert real_ok.equals(residual(C, T * x))
    assert mutant_ok.equals(real_ok)

    assert not maps_commute(S, C, C)
    real_bad = _real_transport_outcome(C, C, S, x)
    mutant_claimed = mutant_treat_commute_optional(S, C, C, x)
    assert mutant_claimed.equals(S * residual(C, x))
    assert not mutant_claimed.equals(residual(C, S * x))
    assert real_bad == "refused_noncommuting"
    assert mutant_claimed != real_bad


def test_mutant_accept_float_killed() -> None:
    # Invariant: floats are refused; a mutant that converts them disagrees.
    with pytest.raises(TypeError, match="got float"):
        _validate_exact_rational(0.25, "x")

    real_half = _real_float_outcome(0.25)
    mutant_half = mutant_validate_accept_float(0.25, "x")
    assert real_half == "refused_float"
    assert mutant_half == Rational(1, 4)
    assert mutant_half != real_half

    real_sympy = _real_float_outcome(Float(0.5))
    mutant_sympy = mutant_validate_accept_float(Float(0.5), "x")
    assert real_sympy == "refused_float"
    assert mutant_sympy == Rational(1, 2)
    assert mutant_sympy != real_sympy

    with pytest.raises(TypeError, match="got bool"):
        _validate_exact_rational(False, "x")
    with pytest.raises(TypeError, match="got bool"):
        mutant_validate_accept_float(False, "x")

    real_int = _validate_exact_rational(2, "x")
    mutant_int = mutant_validate_accept_float(2, "x")
    assert real_int == Rational(2, 1)
    assert mutant_int == real_int


def test_mutant_broken_cochain_condition_killed() -> None:
    # Invariant: d1 * d0 = 0 is mandatory for cochain complex classification.
    d0 = Matrix([[1], [2]])
    d1_broken = Matrix([[1, 1]])  # d1 * d0 = 3 != 0
    defect = Matrix([[1], [0]])

    with pytest.raises(ValueError, match="d1 \\* d0 != 0"):
        classify_closure_attempt(d0=d0, d1=d1_broken, defect_cochain=defect)


def test_mutant_unreplayable_authority_killed() -> None:
    # Invariant: AuthEvidence with replayable=False must not be recognized as is_auth().
    ev_unreplayable = AuthEvidence(packet_id="p1", terminalizer_id="t1", replayable=False)
    term = Terminal(auth_evidence=ev_unreplayable)
    assert term.is_auth() is False

    # Valid replayable evidence
    ev_replayable = AuthEvidence(packet_id="p1", terminalizer_id="t1", replayable=True)
    term_valid = Terminal(auth_evidence=ev_replayable)
    assert term_valid.is_auth() is True


def test_mutant_pi_non_surjective_bypass_killed() -> None:
    # Invariant: quotient_universal_factor requires rank(pi) == pi.rows (B1).
    from coda_a_core import quotient_universal_factor

    f_zero = Matrix([[0, 0]])
    pi_zero = Matrix([[0, 0]])

    with pytest.raises(ValueError, match="surjective"):
        quotient_universal_factor(f_zero, pi_zero)


def test_mutant_sentinel_distance_killed() -> None:
    # Invariant: classify_closure_attempt computes exact L1 distance, never sentinels (B2).
    d0 = Matrix([[1], [0]])
    d1 = Matrix([[0, 1]])
    x = Matrix([[0], [5]])

    res = classify_closure_attempt(d0, d1, x)
    assert res.quotient_distance == Rational(5, 1)
    # A mutant returning sentinel 1 is killed:
    assert res.quotient_distance != Rational(1, 1)

    # Administrative lift must be None, never sentinel 3/4:
    res_lift = classify_closure_attempt(d0, d1, x, pending_lift=True)
    assert res_lift.quotient_distance is None
    assert res_lift.quotient_distance != Rational(3, 4)

