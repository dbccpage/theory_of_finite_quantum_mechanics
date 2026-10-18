from __future__ import annotations
"""Exact tests for the consolidated finite cochain obstruction kernel."""


from fractions import Fraction

import pytest

from omega_engine.crates.discrete_deformation_algebra import FiniteCochainComplex
from omega_engine.crates.solver.solv_finite_cochain_obstruction import (
    Verdict,
    analyze_finite_cochain,
)


def _filled_triangle() -> FiniteCochainComplex:
    return FiniteCochainComplex.from_rows(
        dimensions=(3, 3, 1),
        d0=((-1, 1, 0), (0, -1, 1), (-1, 0, 1)),
        d1=((1, 1, -1),),
    )


def test_exact_repair_returns_primitive_witness() -> None:
    complex_ = _filled_triangle()
    result = analyze_finite_cochain(complex_, (1, 2, 3))

    assert result.verdict is Verdict.EXACT_REPAIR
    assert result.primitive_witness is not None
    assert complex_.primitive_difference(result.primitive_witness) == result.beta
    assert result.authority_effect == "None"


def test_curvature_is_computed_not_asserted() -> None:
    result = analyze_finite_cochain(_filled_triangle(), (1, 2, 4))

    assert result.verdict is Verdict.CURVATURE
    assert result.closure_defect == (Fraction(-1),)


def test_closed_nonexact_circle_is_a_residual() -> None:
    circle = FiniteCochainComplex.from_rows(
        dimensions=(3, 3, 0),
        d0=((-1, 1, 0), (0, -1, 1), (1, 0, -1)),
        d1=(),
    )
    result = analyze_finite_cochain(circle, (1, 1, 1))

    assert result.verdict is Verdict.CLOSED_RESIDUAL
    assert result.residual_representative == result.beta
    assert result.primitive_witness is None
    assert result.coefficient_domain == "Q"
    assert result.period_witness is not None
    assert result.period_boundary_defect == (Fraction(0),) * 3
    assert result.period_pairing == Fraction(1)
    assert result.period_is_boundary is False
    assert (
        sum(
            (
                coefficient * value
                for coefficient, value in zip(result.beta, result.period_witness)
            ),
            Fraction(0),
        )
        == result.period_pairing
    )


def test_invalid_complex_is_detected_before_classification() -> None:
    invalid = FiniteCochainComplex.from_rows(
        dimensions=(2, 2, 1),
        d0=((-1, 1), (-1, 1)),
        d1=((1, 1),),
    )

    result = analyze_finite_cochain(invalid, (0, 0))
    assert result.verdict is Verdict.INVALID_COMPLEX
    assert result.primitive_witness == (Fraction(0), Fraction(0))
    assert result.closure_defect == (Fraction(0),)


def test_invalid_complex_retains_nonexact_face_diagnostics() -> None:
    invalid = FiniteCochainComplex.from_rows(
        dimensions=(2, 2, 1),
        d0=((-1, 1), (-1, 1)),
        d1=((1, 1),),
    )

    result = analyze_finite_cochain(invalid, (1, 0))

    assert result.verdict is Verdict.INVALID_COMPLEX
    assert result.primitive_witness is None
    assert result.closure_defect == (Fraction(1),)


def test_closed_residual_period_witness_supports_multiple_c2_rows() -> None:
    complex_ = FiniteCochainComplex.from_rows(
        dimensions=(1, 2, 2),
        d0=((0,), (0,)),
        d1=((0, 1), (0, 0)),
    )

    result = analyze_finite_cochain(complex_, (1, 0))

    assert result.verdict is Verdict.CLOSED_RESIDUAL
    assert result.period_witness == (Fraction(1), Fraction(0))
    assert result.period_boundary_defect == (Fraction(0),)
    assert result.period_pairing == Fraction(1)
    assert result.period_is_boundary is False


def test_exact_arithmetic_rejects_float_inputs() -> None:
    with pytest.raises(TypeError, match="floating point is forbidden"):
        FiniteCochainComplex.from_rows((1, 1, 0), ((0.5,),), ())


def test_receipt_hash_is_deterministic() -> None:
    first = analyze_finite_cochain(_filled_triangle(), (1, 2, 3))
    second = analyze_finite_cochain(_filled_triangle(), (1, 2, 3))

    assert first.evidence_sha256 == second.evidence_sha256
    assert len(first.evidence_sha256) == 64


def test_zero_middle_dimension_has_correct_complex_defect_shape() -> None:
    complex_ = FiniteCochainComplex.from_rows((2, 0, 1), (), ((),))

    assert complex_.complex_defect() == ((Fraction(0), Fraction(0)),)
    assert analyze_finite_cochain(complex_, ()).verdict is Verdict.EXACT_REPAIR


