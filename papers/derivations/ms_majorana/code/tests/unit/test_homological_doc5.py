"""Narrow tests for py_updates_5.md defect fixes in omega_homology.

Defect 1 (replay gating): ``create_cochain_complex`` must return a typed
``Refusal`` (not raise) at the replay boundary when d1.d0 != 0 or dimensions
mismatch, and must return a ``CochainComplex`` on valid input. The raising
``CochainComplex.new`` is preserved for utility-level use (covered by the
existing golden gate test).
"""

from omega_engine.crates.homology_theory import (
    CochainComplex,
    CoboundaryLawViolation,
    QMatrix,
    TheoremProvenance,
    create_cochain_complex,
    q,
)
from omega_engine.crates.type.refusal import Refusal


def prov():
    return TheoremProvenance.new("test")


def test_create_cochain_complex_refuses_on_coboundary_violation():
    d0 = QMatrix.from_row_major(2, 2, [q(1), q(0), q(0), q(1)])
    d1 = QMatrix.from_row_major(1, 2, [q(1), q(1)])

    raised = False
    try:
        CochainComplex.new(2, 2, 1, d0, d1, prov())
    except CoboundaryLawViolation:
        raised = True
    assert raised, "CochainComplex.new must still raise (utility level)"

    result = create_cochain_complex(2, 2, 1, d0, d1, prov())
    assert isinstance(result, Refusal)
    assert "CoboundaryLawViolation" in result.reason


def test_create_cochain_complex_refuses_on_dimension_mismatch():
    d0 = QMatrix.zero(1, 1)
    d1 = QMatrix.zero(1, 2)
    result = create_cochain_complex(2, 2, 1, d0, d1, prov())
    assert isinstance(result, Refusal)
    assert "DimensionMismatch" in result.reason


def test_create_cochain_complex_returns_complex_on_valid_input():
    d0 = QMatrix.from_row_major(2, 2, [q(1), q(0), q(0), q(1)])
    d1 = QMatrix.zero(0, 2)
    result = create_cochain_complex(2, 2, 0, d0, d1, prov())
    assert isinstance(result, CochainComplex)
    assert (result.c0_dim, result.c1_dim, result.c2_dim) == (2, 2, 0)


