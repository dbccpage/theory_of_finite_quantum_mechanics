# -*- coding: utf-8 -*-
"""
test_coda_or.py: Unit, regression, and mutation test suite for CODA-OR.

Verifies:
1. Section 6A Worked Example exact reproduction (Table 6A 4 squares).
2. Exact cochain quotient solving (LinearRepairProblem) over exact rationals.
3. Complex condition enforcement (d1 * d0 == 0) and exact rational matrix entries.
4. Strict Zero Floats Invariant (floats, booleans, and symbols rejected with TypeError).
5. OR-D3 / OR-T5–T6 Support Sieve Necessity & Non-Creation Firewall.
6. Target binding invariants: arrows, sieves, and objects must strictly agree on target id.
7. Schema validation for declared strings, booleans, and IDs.
8. Defensive immutability: environments and results store immutable matrix snapshots.
9. Protected skeleton mutation discipline and non-empty loss ledger requirements.

Run: python -m pytest -n 8 coda_atlas/F005_coda/or/code/tests -v
"""

from __future__ import annotations

import pytest
from coda_or_core import (
    R_EMPTY_SUPPORT,
    R_NO_TERMINALIZER,
    R_UNSUPPORTED_COMPONENT,
    ComparisonObject,
    EnrichedEnvironment,
    ProtectedSkeleton,
    SilentMutationRefusal,
    SquareStatus,
    SupportArrow,
    SupportSieve,
    _validate_exact_int,
    _validate_exact_rational,
    classify_diagram_square,
    evaluate_comparison_authority,
    reproduce_section_6a_worked_example,
)
from sympy import Matrix, Rational, Symbol


def test_section_6a_worked_example_reproduction() -> None:
    """OR-D2 / Section 6A: exact table reproduction."""
    results = reproduce_section_6a_worked_example()
    assert len(results) == 4

    # Square 1: StrictCommute
    assert results[0].status == SquareStatus.STRICT_COMMUTE
    assert results[0].quotient_distance == Rational(0, 1)
    assert results[0].is_closed is True
    assert results[0].is_exact is True

    # Square 2: WeakCommuteCertified (exact repair)
    assert results[1].status == SquareStatus.WEAK_COMMUTE_CERTIFIED
    assert results[1].quotient_distance == Rational(0, 1)
    assert results[1].repair_2cell == Matrix([[3]])
    assert results[1].is_closed is True
    assert results[1].is_exact is True

    # Square 3: H^1DiagramTear (closed residual)
    assert results[2].status == SquareStatus.H1_DIAGRAM_TEAR
    assert results[2].quotient_distance == Rational(3, 1)
    assert results[2].is_closed is True
    assert results[2].is_exact is False

    # Square 4: OpenDiagramObstruction (unstabilized defect)
    assert results[3].status == SquareStatus.OPEN_DIAGRAM_OBSTRUCTION
    assert results[3].quotient_distance == Rational(3, 1)
    assert results[3].is_closed is False
    assert results[3].boundary_image == Matrix([[3]])
    assert results[3].is_exact is False


def test_multidimensional_cochain_quotient_repair() -> None:
    """Verify cochain quotient repair on higher-dimensional complexes."""
    d0 = Matrix([
        [1, 0],
        [1, 1],
        [0, 1],
    ])
    d1 = Matrix([[1, -1, 1]])

    env = EnrichedEnvironment(
        dim_c0=2,
        dim_c1=3,
        dim_c2=1,
        d0=d0,
        d1=d1,
        name="2D_CochainComplex",
    )

    # 1. Exact defect in im(d0): delta = d0 * [2, 3] = [2, 5, 3]
    exact_defect = Matrix([[2], [5], [3]])
    res_exact = classify_diagram_square(exact_defect, env)
    assert res_exact.status == SquareStatus.WEAK_COMMUTE_CERTIFIED
    assert res_exact.quotient_distance == Rational(0, 1)
    assert res_exact.is_closed is True
    assert res_exact.is_exact is True

    # 2. Closed defect in ker(d1)
    cochain_ker = Matrix([[1], [2], [1]])
    res_ker = classify_diagram_square(cochain_ker, env)
    assert res_ker.status == SquareStatus.WEAK_COMMUTE_CERTIFIED

    # 3. Non-closed defect: [1, 0, 0] -> d1 * [1, 0, 0] = [1] != 0
    res_open = classify_diagram_square(Matrix([[1], [0], [0]]), env)
    assert res_open.status == SquareStatus.OPEN_DIAGRAM_OBSTRUCTION
    assert res_open.quotient_distance > Rational(0, 1)
    assert res_open.is_closed is False
    assert res_open.boundary_image == Matrix([[1]])


def test_complex_property_enforcement() -> None:
    """Verify that d1 * d0 != 0 raises ValueError."""
    d0 = Matrix([[1, 0], [0, 1]])
    d1_bad = Matrix([[1, 1]])  # d1 * d0 = [1, 1] != [0, 0]

    with pytest.raises(ValueError, match="Complex condition violated"):
        EnrichedEnvironment(
            dim_c0=2,
            dim_c1=2,
            dim_c2=1,
            d0=d0,
            d1=d1_bad,
        )


def test_zero_floats_invariant() -> None:
    """Strictly reject IEEE 754 floating point and booleans in scalar position."""
    assert _validate_exact_rational(Rational(3, 4), "x") == Rational(3, 4)
    assert _validate_exact_rational(5, "x") == Rational(5, 1)
    assert _validate_exact_rational("7/3", "x") == Rational(7, 3)

    with pytest.raises(TypeError, match="got float"):
        _validate_exact_rational(0.75, "x")

    with pytest.raises(TypeError, match="got bool"):
        _validate_exact_rational(True, "x")

    with pytest.raises(TypeError, match="symbolic expression"):
        _validate_exact_rational(Symbol("s"), "x")

    # Integer validation
    assert _validate_exact_int(2, "dim") == 2
    with pytest.raises(TypeError, match="got bool"):
        _validate_exact_int(True, "dim")
    with pytest.raises(TypeError):
        _validate_exact_int(2.0, "dim")
    with pytest.raises(ValueError, match="non-negative"):
        _validate_exact_int(-1, "dim")

    # Diagram defect float rejection
    env = EnrichedEnvironment(
        dim_c0=1,
        dim_c1=1,
        dim_c2=1,
        d0=Matrix([[1]]),
        d1=Matrix([[0]]),
    )
    with pytest.raises(TypeError, match="floats strictly forbidden"):
        classify_diagram_square([1.5], env)

    with pytest.raises(TypeError, match="got bool"):
        classify_diagram_square([False], env)


def test_target_binding_arrow_sieve_mismatch() -> None:
    """Finding 2: Arrow targeting Y must not be admitted to a sieve targeting X."""
    arrow_y = SupportArrow(
        source_regime_id="Reg_A",
        target_object_id="Y",
        source_has_authority=True,
        certificate_id="chi_A",
    )
    with pytest.raises(ValueError, match="Arrow target 'Y' does not match sieve target 'X'"):
        SupportSieve(
            target_object_id="X",
            arrows=(arrow_y,),
        )


def test_target_binding_sieve_object_mismatch() -> None:
    """Finding 2: Sieve targeting Y must not be admitted to ComparisonObject X."""
    arrow_y = SupportArrow(
        source_regime_id="Reg_A",
        target_object_id="Y",
        source_has_authority=True,
        certificate_id="chi_A",
    )
    sieve_y = SupportSieve(
        target_object_id="Y",
        arrows=(arrow_y,),
    )
    with pytest.raises(ValueError, match="support_sieve target 'Y' does not match object_id 'X'"):
        ComparisonObject(
            object_id="X",
            weight_class="finite",
            support_sieve=sieve_y,
            descent_d="D",
            verifier_v="V",
            terminalizer_tau="tau",
        )


def test_malformed_support_fields_rejected() -> None:
    """Finding 2: Schema validation must reject malformed truthy strings, booleans, and empty strings."""
    # 1. source_has_authority="false" is a string, must raise TypeError
    with pytest.raises(TypeError, match="source_has_authority must be an exact bool"):
        SupportArrow(
            source_regime_id="Reg_A",
            target_object_id="X",
            source_has_authority="false",  # type: ignore
            certificate_id="chi_A",
        )

    # 2. certificate_id=False is a bool, must raise TypeError
    with pytest.raises(TypeError, match="certificate_id must be a declared non-empty string, got bool"):
        SupportArrow(
            source_regime_id="Reg_A",
            target_object_id="X",
            source_has_authority=True,
            certificate_id=False,  # type: ignore
        )

    # 3. certificate_id="" is an empty string, must raise ValueError
    with pytest.raises(ValueError, match="certificate_id must be a non-empty string"):
        SupportArrow(
            source_regime_id="Reg_A",
            target_object_id="X",
            source_has_authority=True,
            certificate_id="",
        )

    # 4. Empty declared names in ComparisonObject
    sieve_x = SupportSieve(target_object_id="X", arrows=())
    with pytest.raises(ValueError, match="terminalizer_tau must be a non-empty string"):
        ComparisonObject(
            object_id="X",
            weight_class="finite",
            support_sieve=sieve_x,
            terminalizer_tau="",
        )


def test_differential_matrix_entry_scalar_validation() -> None:
    """Finding 3: EnrichedEnvironment must validate every entry of d0 and d1 as exact rationals."""
    # Floating-point entry in d1
    with pytest.raises(TypeError, match="floats strictly forbidden"):
        EnrichedEnvironment(
            dim_c0=0,
            dim_c1=1,
            dim_c2=1,
            d0=Matrix.zeros(1, 0),
            d1=Matrix([[0.5]]),
        )

    # Floating-point entry in d0
    with pytest.raises(TypeError, match="floats strictly forbidden"):
        EnrichedEnvironment(
            dim_c0=1,
            dim_c1=1,
            dim_c2=0,
            d0=Matrix([[0.5]]),
            d1=Matrix.zeros(0, 1),
        )

    # Symbolic entry in d1
    s = Symbol("s")
    with pytest.raises(TypeError, match="symbolic expression"):
        EnrichedEnvironment(
            dim_c0=0,
            dim_c1=1,
            dim_c2=1,
            d0=Matrix.zeros(1, 0),
            d1=Matrix([[s]]),
        )

    # Boolean entry in d1
    with pytest.raises(TypeError, match="got bool"):
        EnrichedEnvironment(
            dim_c0=0,
            dim_c1=1,
            dim_c2=1,
            d0=Matrix.zeros(1, 0),
            d1=Matrix([[True]]),
        )


def test_immutable_environment_snapshot_prevents_alias_mutation() -> None:
    """Finding 4: Caller mutating d1 after construction must not alter EnrichedEnvironment."""
    d0 = Matrix([[1]])
    d1 = Matrix([[0]])
    env = EnrichedEnvironment(
        dim_c0=1,
        dim_c1=1,
        dim_c2=1,
        d0=d0,
        d1=d1,
    )

    # Caller mutates external matrix
    d1[0, 0] = 1
    # env.d1 remains unchanged at 0
    assert env.d1[0, 0] == 0
    assert (env.d1 * env.d0).is_zero_matrix is True

    # Attempting to directly mutate env.d1 raises TypeError
    with pytest.raises(TypeError):
        env.d1[0, 0] = 1


def test_immutable_result_snapshot_prevents_evidence_mutation() -> None:
    """Finding 4: Caller mutating raw defect after classification must not alter result."""
    env = EnrichedEnvironment(
        dim_c0=1,
        dim_c1=1,
        dim_c2=1,
        d0=Matrix([[1]]),
        d1=Matrix([[0]]),
    )
    raw = Matrix([[0]])
    result = classify_diagram_square(raw, env)
    assert result.status == SquareStatus.STRICT_COMMUTE
    assert result.raw_defect[0, 0] == 0

    # Caller mutates original vector
    raw[0, 0] = 3
    # Result retains its original classified value
    assert result.raw_defect[0, 0] == 0
    assert result.status == SquareStatus.STRICT_COMMUTE

    # Attempting to mutate result.raw_defect raises TypeError
    with pytest.raises(TypeError):
        result.raw_defect[0, 0] = 5


def test_gtor_02_non_creation_firewall() -> None:
    """OR-T6: Object in comparison envelope does not create authority."""
    sieve_ok = SupportSieve(
        target_object_id="X_cand",
        arrows=(
            SupportArrow(
                source_regime_id="A1",
                target_object_id="X_cand",
                source_has_authority=True,
                certificate_id="chi_1",
            ),
        ),
    )
    obj_no_term = ComparisonObject(
        object_id="X_cand",
        weight_class="finite_colimit",
        support_sieve=sieve_ok,
        terminalizer_tau=None,
    )
    res = evaluate_comparison_authority(obj_no_term)
    assert res.inhabited is False
    assert res.refusal_code == R_NO_TERMINALIZER
    assert res.residual_mass > Rational(0, 1)
    assert res.authority_effect == "None"


def test_gtor_04_support_sieve_necessity() -> None:
    """OR-T5: Empty support sieve forces hard refusal R_empty_support."""
    sieve_empty = SupportSieve(target_object_id="X_lim", arrows=())
    assert sieve_empty.is_empty() is True

    obj_empty = ComparisonObject(
        object_id="X_lim",
        weight_class="finite_limit",
        support_sieve=sieve_empty,
        descent_d="D_lim",
        verifier_v="V_lim",
        terminalizer_tau="tau_lim",
    )
    res = evaluate_comparison_authority(obj_empty)
    assert res.inhabited is False
    assert res.refusal_code == R_EMPTY_SUPPORT
    assert res.residual_mass == Rational(1, 1)
    assert res.authority_effect == "None"

    # Arrow with no source authority or missing certificate
    sieve_uncert = SupportSieve(
        target_object_id="X_lim",
        arrows=(
            SupportArrow(
                source_regime_id="A_unauth",
                target_object_id="X_lim",
                source_has_authority=False,
                certificate_id="chi_fake",
            ),
            SupportArrow(
                source_regime_id="A_nocert",
                target_object_id="X_lim",
                source_has_authority=True,
                certificate_id=None,
            ),
        ),
    )
    assert sieve_uncert.is_empty() is True
    obj_uncert = ComparisonObject(
        object_id="X_lim",
        weight_class="finite_limit",
        support_sieve=sieve_uncert,
        descent_d="D_lim",
        verifier_v="V_lim",
        terminalizer_tau="tau_lim",
    )
    res_uncert = evaluate_comparison_authority(obj_uncert)
    assert res_uncert.inhabited is False
    assert res_uncert.refusal_code == R_EMPTY_SUPPORT


def test_certified_comparison_authority() -> None:
    """When support sieve is certified and local terminalizer is declared."""
    sieve_cert = SupportSieve(
        target_object_id="X_good",
        arrows=(
            SupportArrow(
                source_regime_id="A1",
                target_object_id="X_good",
                source_has_authority=True,
                certificate_id="chi_A1",
            ),
            SupportArrow(
                source_regime_id="A2",
                target_object_id="X_good",
                source_has_authority=True,
                certificate_id="chi_A2",
            ),
        ),
    )
    obj_cert = ComparisonObject(
        object_id="X_good",
        weight_class="finite_limit",
        support_sieve=sieve_cert,
        descent_d="D_good",
        verifier_v="V_good",
        terminalizer_tau="tau_good",
    )
    res = evaluate_comparison_authority(obj_cert)
    assert res.inhabited is True
    assert res.refusal_code is None
    assert res.residual_mass == Rational(0, 1)
    assert "term_certified_comparison_X_good" in str(res.terminal_state)
    assert res.authority_effect == "None"


def test_protected_skeleton_mutation_refusal() -> None:
    """Protected skeleton Skel_A requires declared LossLedger for mutations."""
    skel = ProtectedSkeleton(
        skeleton_id="Skel_A",
        elements=("node1", "node2", "edge12"),
    )

    # Unmodified skeleton passes without ledger
    skel_same, ledger = skel.mutate(("node1", "node2", "edge12"), loss_ledger=None)
    assert skel_same.elements == skel.elements
    assert ledger is None

    # Modified skeleton without loss ledger raises SilentMutationRefusal
    with pytest.raises(SilentMutationRefusal, match="mutated without declared non-empty LossLedger"):
        skel.mutate(("node1", "node2", "edge12", "extra_node"), loss_ledger=None)

    # Modified skeleton with empty loss ledger raises SilentMutationRefusal
    with pytest.raises(SilentMutationRefusal, match="mutated without declared non-empty LossLedger"):
        skel.mutate(("node1", "node2", "edge12", "extra_node"), loss_ledger="")

    # Modified skeleton with declared loss ledger succeeds
    skel_mutated, recorded_ledger = skel.mutate(
        ("node1", "node2", "edge12", "extra_node"),
        loss_ledger="LossLedger_Adjoin_extra_node",
    )
    assert len(skel_mutated.elements) == 4
    assert recorded_ledger == "LossLedger_Adjoin_extra_node"


def test_or_edge_cases_and_uncovered_branches():
    # String conversion error and invalid type error
    with pytest.raises(TypeError, match="string could not be converted"):
        _validate_exact_rational("invalid_rational", "val")
    with pytest.raises(TypeError, match="must be an exact rational"):
        _validate_exact_rational([1, 2], "val")

    # EnrichedEnvironment type & dimension checks
    with pytest.raises(TypeError, match="must be sympy.Matrix"):
        EnrichedEnvironment(1, 1, 1, "not_a_matrix", Matrix([0]))
    with pytest.raises(ValueError, match="d0 dimensions"):
        EnrichedEnvironment(2, 2, 1, Matrix([0]), Matrix([[0, 0]]))
    with pytest.raises(ValueError, match="d1 dimensions"):
        EnrichedEnvironment(1, 2, 2, Matrix([[0], [0]]), Matrix([0]))

    # classify_diagram_square with row vector (gets transposed)
    env = EnrichedEnvironment(
        dim_c0=1,
        dim_c1=2,
        dim_c2=1,
        d0=Matrix([[1], [0]]),
        d1=Matrix([[0, 1]]),
    )
    res_row = classify_diagram_square(Matrix([[0, 0]]), env)
    assert res_row.status.value == "StrictCommute"

    # Non-vector matrix (e.g. 2x2)
    with pytest.raises(ValueError, match="must be a column vector"):
        classify_diagram_square(Matrix.eye(2), env)

    # Dimension mismatch
    with pytest.raises(ValueError, match="must match C\\^1 dimension"):
        classify_diagram_square([1, 2, 3], env)

    # dim_c0 == 0 branch
    env_c0_zero = EnrichedEnvironment(
        dim_c0=0,
        dim_c1=2,
        dim_c2=1,
        d0=Matrix.zeros(2, 0),
        d1=Matrix.zeros(1, 2),
    )
    res_c0_zero = classify_diagram_square([1, 2], env_c0_zero)
    assert res_c0_zero.quotient_distance == Rational(3, 1)

    # Component descent require_all_sources
    sieve_mixed = SupportSieve(
        target_object_id="X_part",
        arrows=(
            SupportArrow("A1", "X_part", True, "chi_1"),
            SupportArrow("A2", "X_part", False, "chi_2"),
        ),
    )
    obj_mixed = ComparisonObject("X_part", "finite", sieve_mixed, "D", "V", "tau")
    res_part = evaluate_comparison_authority(obj_mixed, require_all_sources=True)
    assert res_part.inhabited is False
    assert res_part.refusal_code == R_UNSUPPORTED_COMPONENT
