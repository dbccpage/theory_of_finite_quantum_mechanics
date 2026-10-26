# -*- coding: utf-8 -*-
"""
test_gtla_fault_examples.py: Anticipated fault catalog & decision invariants for CODA-GTLA.

This module catalogues anticipated defect mutants against production decision points:
1. Treating a non-zero quotient Phi_1 class as authorized standing (killed by firewall).
2. Skipping the FOC^sharp obstruction calculus and blindly authorizing (killed by complex checks).
3. Soft-converting IEEE 754 floats to rationals rather than raising TypeError (killed by zero-floats invariant).

AuthorityEffect: None.
"""

from __future__ import annotations

from typing import Any

import pytest
from coda_gtla_core import (
    DSharpOutput,
    FocSharpOutput,
    ProblemInstance,
    _validate_exact_rational,
    execute_master_normal_form,
    functor_d_sharp,
    functor_r_sharp,
    functor_rho_sharp,
    functor_tau_sharp,
)
from sympy import Float, Rational
from test_coda_gtla import (
    _anomalon_packet,
    _authorized_packet,
    _empty_sieve_packet,
    _nonclosed_packet,
)


def mutant_nonzero_quotient_as_standing(problem: ProblemInstance) -> bool:
    """Fault: Treat a nonzero Phi_1 class as authorized standing."""
    receipt = execute_master_normal_form(problem)
    foc = receipt.foc_stage
    if foc is not None and foc.is_coherent_residual and foc.phi1_distance > Rational(0, 1):
        return True
    return receipt.is_authorized()


def mutant_skip_pipeline_stage_still_accept(problem: ProblemInstance) -> bool:
    """Fault: Skip FOC^sharp and still accept as if the obstruction stage reported exact repair."""
    r_out = functor_r_sharp(problem)
    if r_out.is_refused:
        return False
    rho_out = functor_rho_sharp(problem, r_out)
    d_out = functor_d_sharp(problem, rho_out)
    skipped_foc = FocSharpOutput(
        phi1_distance=Rational(0, 1),
        gamma2_distance=Rational(0, 1),
        is_exact_repair=True,
        is_coherent_residual=False,
        is_nonclosed_defect=False,
    )
    term = functor_tau_sharp(problem, r_out, d_out, skipped_foc)
    return term.is_authorized


def mutant_validate_accept_float(val: Any, name: str) -> Rational:
    """Fault: Accept IEEE 754 floats by converting them instead of refusing."""
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


def test_mutant_nonzero_quotient_as_standing_killed() -> None:
    # Invariant: a positive Phi_1 class is T_res, not standing.
    real = execute_master_normal_form(_anomalon_packet())
    mutant = mutant_nonzero_quotient_as_standing(_anomalon_packet())
    assert real.is_authorized() is False
    assert real.is_anomalon() is True
    assert real.is_refused() is False
    assert real.terminal_outcome.phi1_distance == Rational(2, 1)
    assert mutant is True
    assert mutant is not real.is_authorized()

    real_auth = execute_master_normal_form(_authorized_packet())
    mutant_auth = mutant_nonzero_quotient_as_standing(_authorized_packet())
    assert real_auth.is_authorized() is True
    assert real_auth.terminal_outcome.phi1_distance == Rational(0, 1)
    assert mutant_auth is True

    real_empty = execute_master_normal_form(_empty_sieve_packet())
    mutant_empty = mutant_nonzero_quotient_as_standing(_empty_sieve_packet())
    assert real_empty.is_authorized() is False
    assert real_empty.is_refused() is True
    assert mutant_empty is False


def test_mutant_skip_pipeline_stage_still_accept_killed() -> None:
    # Invariant: skipping FOC^sharp must not authorize a nonclosed (Gamma_2 > 0) packet.
    real = execute_master_normal_form(_nonclosed_packet())
    mutant = mutant_skip_pipeline_stage_still_accept(_nonclosed_packet())
    assert real.is_authorized() is False
    assert real.is_refused() is True
    assert real.terminal_outcome.gamma2_distance > Rational(0, 1)
    assert mutant is False  # Forged FOC output is rejected by production tau.

    real_auth = execute_master_normal_form(_authorized_packet())
    mutant_auth = mutant_skip_pipeline_stage_still_accept(_authorized_packet())
    assert real_auth.is_authorized() is True
    assert mutant_auth is True

    real_empty = execute_master_normal_form(_empty_sieve_packet())
    mutant_empty = mutant_skip_pipeline_stage_still_accept(_empty_sieve_packet())
    assert real_empty.is_authorized() is False
    assert real_empty.is_refused() is True
    assert mutant_empty is False

    r_out = functor_r_sharp(_nonclosed_packet())
    rho_out = functor_rho_sharp(_nonclosed_packet(), r_out)
    d_out = functor_d_sharp(_nonclosed_packet(), rho_out)
    assert d_out.gluing_succeeded is True
    assert isinstance(d_out, DSharpOutput)


def test_mutant_accept_float_killed() -> None:
    # Invariant: floats are refused; a mutant that converts them disagrees.
    with pytest.raises(TypeError, match="floats strictly forbidden"):
        _validate_exact_rational(0.25, "x")

    real_quarter = _real_float_outcome(0.25)
    mutant_quarter = mutant_validate_accept_float(0.25, "x")
    assert real_quarter == "refused_float"
    assert mutant_quarter == Rational(1, 4)
    assert mutant_quarter != real_quarter

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

    with pytest.raises(TypeError, match="floats strictly forbidden"):
        _validate_exact_rational(0.0, "diff[0,0]")
