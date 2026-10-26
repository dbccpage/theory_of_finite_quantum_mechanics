# -*- coding: utf-8 -*-
"""
test_coda_a.py: Unit, theorem alignment, invariant, and contract tests for CODA-A.

Verifies:
1. Definition A-D1 & Decomposition: x = C x + residual(C, x).
2. Theorem A-T1: residual(C, x) == 0 <=> C x == x (bidirectional over multiple vectors).
3. Theorem A-T2: C(residual(C, x)) == 0 for projections.
4. Theorem A-T3: residual(C, residual(C, x)) == residual(C, x).
5. Theorem A-T4: Range equals fixed set: x in im(C) <=> C x == x.
6. Theorem A-T5: Commuting transport: T(residual(C, x)) == residual(D, T x).
7. Theorem A-T6: Cokernel residual equivalence: x - y in im(C) <=> residual(C, x) == residual(C, y).
8. Theorem A-T7: Unique induced map on quotient V / R.
9. Induced quotient section: s([x]) in ker(C).
10. Scope fence A-S1: Terminal disjointness, replayable auth evidence invariant.
11. 5-case finite cochain classifier with d1 * d0 = 0 validation.
12. Strict zero floats invariant (floats and booleans in scalar position raise TypeError).
13. Release contract tests (unified title, version 0.1.0, clean inventory).

AuthorityEffect: None.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from coda_a_core import (
    AuthEvidence,
    ResidualOutcome,
    ResidualTerminalClass,
    Terminal,
    _validate_exact_int,
    _validate_exact_rational,
    classify_closure_attempt,
    difference_in_image,
    induced_quotient_section,
    is_anomalon,
    maps_commute,
    quotient_universal_factor,
    reproduce_worked_example,
    residual,
    residual_in_kernel,
    residual_not_auth,
    residual_transport,
)
from sympy import Matrix, Rational


def _axis_projection() -> Matrix:
    return Matrix([[1, 0], [0, 0]])


def _oblique_projection() -> Matrix:
    # C = [[1, 1], [0, 0]] -> C^2 = [[1, 1], [0, 0]] = C
    return Matrix([[1, 1], [0, 0]])


def _3d_projection() -> Matrix:
    # Projects onto first two coordinates
    return Matrix([[1, 0, 0], [0, 1, 0], [0, 0, 0]])


# ---------------------------------------------------------------------------
# Elementary Theorems A-T1 through A-T7 & Section 4
# ---------------------------------------------------------------------------

def test_decomposition_identity() -> None:
    """Definition A-D1: x = C x + residual(C, x) holds universally."""
    # Projection case
    C_proj = _axis_projection()
    for v in [Matrix([[3], [4]]), Matrix([[0], [0]]), Matrix([[-5], [7]])]:
        assert v == C_proj * v + residual(C_proj, v)

    # Non-projection case
    N = Matrix([[0, 1], [0, 0]])
    v = Matrix([[2], [5]])
    assert v == N * v + residual(N, v)

    # 3D case
    C3 = _3d_projection()
    v3 = Matrix([[1], [2], [3]])
    assert v3 == C3 * v3 + residual(C3, v3)


def test_at1_bidirectional_exact_examples() -> None:
    """Theorem A-T1: residual(C, x) == 0 <=> C x == x in both directions."""
    C = _axis_projection()

    # Direction 1: C x == x => residual == 0
    fixed_vectors = [Matrix([[3], [0]]), Matrix([[0], [0]]), Matrix([[-7], [0]])]
    for x in fixed_vectors:
        assert C * x == x
        assert residual(C, x).is_zero_matrix is True

    # Direction 2: C x != x => residual != 0
    unfixed_vectors = [Matrix([[3], [4]]), Matrix([[0], [1]]), Matrix([[1], [-2]])]
    for x in unfixed_vectors:
        assert C * x != x
        assert residual(C, x).is_zero_matrix is False

    # Oblique projection
    C_obl = _oblique_projection()
    fixed_obl = Matrix([[2], [0]])  # C * [2, 0]^T = [2, 0]^T
    assert C_obl * fixed_obl == fixed_obl
    assert residual(C_obl, fixed_obl).is_zero_matrix is True


def test_at2_projection_eats_leftover() -> None:
    """Theorem A-T2: C(residual(C, x)) == 0 for any projection."""
    C = _axis_projection()
    for x in [Matrix([[3], [4]]), Matrix([[-1], [2]]), Matrix([[0], [5]])]:
        r = residual(C, x)
        assert (C * r).is_zero_matrix is True
        assert residual_in_kernel(C, x).is_zero_matrix is True

    # Oblique projection
    C_obl = _oblique_projection()
    x_obl = Matrix([[3], [4]])
    assert (C_obl * residual(C_obl, x_obl)).is_zero_matrix is True


def test_at3_leftover_of_leftover() -> None:
    """Theorem A-T3: residual(C, residual(C, x)) == residual(C, x)."""
    C = _axis_projection()
    x = Matrix([[3], [4]])
    r = residual(C, x)
    assert residual(C, r) == r

    C_obl = _oblique_projection()
    x_obl = Matrix([[1], [2]])
    r_obl = residual(C_obl, x_obl)
    assert residual(C_obl, r_obl) == r_obl


def test_at4_range_equals_fixed_set() -> None:
    """Theorem A-T4: x in im(C) <=> C x == x for projection C."""
    C = _axis_projection()

    # In image:
    y = Matrix([[5], [9]])
    x_in_im = C * y  # [5, 0]^T
    assert C * x_in_im == x_in_im
    assert difference_in_image(C, x_in_im, Matrix([[0], [0]])) is True

    # Not in image:
    x_not_in_im = Matrix([[5], [1]])
    assert C * x_not_in_im != x_not_in_im
    assert difference_in_image(C, x_not_in_im, Matrix([[0], [0]])) is False


def test_at5_commuting_transport() -> None:
    """Theorem A-T5: T(residual(C, x)) == residual(D, T x) under T C = D T."""
    C = _axis_projection()
    x = Matrix([[3], [4]])
    T_scale = Matrix([[2, 0], [0, 2]])
    assert maps_commute(T_scale, C, C) is True
    assert T_scale * residual(C, x) == residual(C, T_scale * x)
    assert residual_transport(C, C, T_scale, x) == T_scale * residual(C, x)

    # Non-commuting map
    S_swap = Matrix([[0, 1], [1, 0]])
    assert maps_commute(S_swap, C, C) is False
    with pytest.raises(ValueError, match="commuting transport hypothesis"):
        residual_transport(C, C, S_swap, x)


def test_at6_leftover_classes_match_cokernel() -> None:
    """Theorem A-T6: x - y in im(C) <=> residual(C, x) == residual(C, y)."""
    C = _axis_projection()

    # Same class: difference is in im(C)
    x = Matrix([[3], [4]])
    y_same = Matrix([[5], [4]])  # diff = [-2, 0]^T in im(C)
    assert difference_in_image(C, x, y_same) is True
    assert residual(C, x) == residual(C, y_same)

    # Different class: difference is not in im(C)
    y_diff = Matrix([[3], [5]])  # diff = [0, -1]^T not in im(C)
    assert difference_in_image(C, x, y_diff) is False
    assert residual(C, x) != residual(C, y_diff)

    # Oblique projection tests
    C_obl = _oblique_projection()
    v1 = Matrix([[2], [1]])
    # C_obl * [1, 0]^T = [1, 0]^T
    v2 = v1 + Matrix([[1], [0]])  # differs by [1, 0]^T in im(C)
    assert difference_in_image(C_obl, v1, v2) is True
    assert residual(C_obl, v1) == residual(C_obl, v2)


def test_at7_quotient_universal_factorization() -> None:
    """Theorem A-T7: linear f vanishing on R factors uniquely as g * pi = f."""
    # Let V = Q^2, R = span([1, 0]^T) = im(C).
    # pi : Q^2 -> Q^1 projects to second coordinate: pi = [[0, 1]]
    pi = Matrix([[0, 1]])
    # f : Q^2 -> Q^1 vanishes on R: f = [[0, 3]]
    f = Matrix([[0, 3]])
    g = quotient_universal_factor(f, pi)
    assert g == Matrix([[3]])
    assert g * pi == f


def test_induced_quotient_section() -> None:
    """Section 4: induced section s([x]) = x - C x lands in ker(C)."""
    C = _axis_projection()
    x = Matrix([[3], [4]])
    s_x = induced_quotient_section(C, x)
    assert s_x == Matrix([[0], [4]])
    assert (C * s_x).is_zero_matrix is True


# ---------------------------------------------------------------------------
# Scope Fence A-S1 & Classifier Invariants
# ---------------------------------------------------------------------------

def test_scope_fence_as1_terminal_disjointness() -> None:
    """A-S1: Terminal coproduct disjointness and replayable requirement."""
    # Replayable auth evidence
    auth_valid = AuthEvidence(packet_id="p1", terminalizer_id="tau1", replayable=True)
    term_auth = Terminal(auth_evidence=auth_valid)
    assert term_auth.is_auth() is True
    assert term_auth.is_residual() is False

    # Non-replayable auth evidence MUST NOT be recognized as valid authority
    auth_unreplayable = AuthEvidence(packet_id="p2", terminalizer_id="tau2", replayable=False)
    term_unrep = Terminal(auth_evidence=auth_unreplayable)
    assert term_unrep.is_auth() is False

    # Residual outcome
    res_out = ResidualOutcome(
        classification=ResidualTerminalClass.CLOSED_RESIDUAL,
        residual_class_id="res1",
        defect_vector=Matrix([[1], [0]]),
        quotient_distance=Rational(1, 1),
        is_closed=True,
    )
    term_res = Terminal(residual_outcome=res_out)
    assert term_res.is_auth() is False
    assert term_res.is_residual() is True
    assert residual_not_auth(res_out) is True

    # Disjointness errors
    with pytest.raises(ValueError, match="cannot co-inhabit"):
        Terminal(auth_evidence=auth_valid, residual_outcome=res_out)

    with pytest.raises(ValueError, match="must carry either"):
        Terminal(auth_evidence=None, residual_outcome=None)


def test_residual_outcome_classification_invariants() -> None:
    """ResidualOutcome strictly rejects invalid combinations."""
    # Negative distance rejected
    with pytest.raises(ValueError, match="must be non-negative"):
        ResidualOutcome(
            classification=ResidualTerminalClass.CLOSED_RESIDUAL,
            residual_class_id="neg",
            defect_vector=Matrix([[1], [0]]),
            quotient_distance=Rational(-1, 1),
            is_closed=True,
        )

    # None distance rejected
    with pytest.raises(ValueError, match="cannot be None"):
        ResidualOutcome(
            classification=ResidualTerminalClass.CLOSED_RESIDUAL,
            residual_class_id="none",
            defect_vector=Matrix([[1], [0]]),
            quotient_distance=None,  # type: ignore
            is_closed=True,
        )

    # ClosedResidual must have is_closed=True
    with pytest.raises(ValueError, match="ClosedResidual must satisfy is_closed=True"):
        ResidualOutcome(
            classification=ResidualTerminalClass.CLOSED_RESIDUAL,
            residual_class_id="inconsistent_closed",
            defect_vector=Matrix([[1], [0]]),
            quotient_distance=Rational(1, 1),
            is_closed=False,
        )

    # OpenResidual must have is_closed=False
    with pytest.raises(ValueError, match="OpenResidual must satisfy is_closed=False"):
        ResidualOutcome(
            classification=ResidualTerminalClass.OPEN_RESIDUAL,
            residual_class_id="inconsistent_open",
            defect_vector=Matrix([[1], [0]]),
            quotient_distance=Rational(1, 1),
            is_closed=True,
        )

    # ClosureAbsorbed must have distance=0
    with pytest.raises(ValueError, match="ClosureAbsorbed must have quotient_distance=0"):
        ResidualOutcome(
            classification=ResidualTerminalClass.CLOSURE_ABSORBED,
            residual_class_id="inconsistent_absorbed",
            defect_vector=Matrix([[1], [0]]),
            quotient_distance=Rational(1, 1),
            is_closed=True,
        )


def test_cochain_complex_condition_enforced() -> None:
    """Classifier requires and verifies d1 * d0 = 0 before cohomology processing."""
    d0 = Matrix([[1], [2]])
    # Broken complex: d1 * d0 = [[1, 1]] * [[1], [2]] = 3 != 0
    d1_broken = Matrix([[1, 1]])
    defect = Matrix([[1], [0]])

    with pytest.raises(ValueError, match="d1 \\* d0 != 0: declared matrices do not form a valid cochain complex"):
        classify_closure_attempt(d0=d0, d1=d1_broken, defect_cochain=defect)


def test_5_case_classification_suite() -> None:
    """Verify all 5 cases of the discrete residual taxonomy."""
    d0 = Matrix([[1], [2]])
    d1 = Matrix([[2, -1]])  # d1 * d0 = 0, valid!

    # 1. ClosureAbsorbed: [2, 4]^T in im(d0)
    defect_abs = Matrix([[2], [4]])
    res_abs = classify_closure_attempt(d0, d1, defect_abs)
    assert res_abs.classification == ResidualTerminalClass.CLOSURE_ABSORBED
    assert res_abs.quotient_distance == Rational(0)
    assert res_abs.is_closed is True
    assert is_anomalon(res_abs.classification) is False

    # 2. OpenResidual: d1 * defect != 0
    defect_open = Matrix([[1], [0]])  # d1 * [1, 0]^T = 2 != 0
    res_open = classify_closure_attempt(d0, d1, defect_open)
    assert res_open.classification == ResidualTerminalClass.OPEN_RESIDUAL
    assert res_open.is_closed is False
    assert is_anomalon(res_open.classification) is False

    # 3. ClosedResidual (Anomalon in 3D valid complex)
    d0_3d = Matrix([[1], [0], [0]])
    d1_3d = Matrix([[0, 0, 1]])  # d1 * d0 = 0
    defect_closed = Matrix([[0], [1], [0]])  # d1 * defect = 0, not in im(d0)
    res_anom = classify_closure_attempt(d0_3d, d1_3d, defect_closed)
    assert res_anom.classification == ResidualTerminalClass.CLOSED_RESIDUAL
    assert is_anomalon(res_anom.classification) is True
    assert res_anom.quotient_distance == Rational(1)
    assert res_anom.is_closed is True

    # 4. LiftRequired
    res_lift = classify_closure_attempt(d0, d1, defect_abs, pending_lift=True)
    assert res_lift.classification == ResidualTerminalClass.LIFT_REQUIRED
    assert is_anomalon(res_lift.classification) is False

    # 5. RefusedClosure
    res_ref = classify_closure_attempt(d0, d1, defect_abs, refusal_reason="Invalid signature")
    assert res_ref.classification == ResidualTerminalClass.REFUSED_CLOSURE
    assert is_anomalon(res_ref.classification) is False


def test_zero_floats_and_scalar_validation() -> None:
    """Strict zero floats invariant on scalar operations."""
    with pytest.raises(TypeError, match="got float"):
        _validate_exact_rational(1.25, "val")

    with pytest.raises(TypeError, match="got bool"):
        _validate_exact_rational(True, "val")

    with pytest.raises(TypeError, match="got float"):
        _validate_exact_int(3.0, "val")

    with pytest.raises(TypeError, match="got bool"):
        _validate_exact_int(False, "val")


def test_malformed_inputs_public_api() -> None:
    """Public functions reject malformed dimensions and non-square matrices."""
    C = _axis_projection()
    x = Matrix([[1], [2]])

    # Non-square matrix
    with pytest.raises(ValueError, match="must be square"):
        residual(Matrix([[1, 0, 0], [0, 1, 0]]), x)

    # Dimension mismatch
    with pytest.raises(ValueError, match="dimension.*must match"):
        residual(C, Matrix([[1], [2], [3]]))

    # Difference in image dimension mismatch
    with pytest.raises(ValueError, match="same dimension"):
        difference_in_image(C, x, Matrix([[1], [2], [3]]))


def test_reproduce_worked_example() -> None:
    """Replay worked example test."""
    res = reproduce_worked_example()
    assert res["specimen1_class"] == "OpenResidual"
    assert res["specimen1_distance"] == Rational(1, 1)
    assert res["specimen2_class"] == "ClosedResidual"
    assert res["specimen2_is_anomalon"] is True
    assert res["specimen2_distance"] == Rational(1, 1)
    assert res["specimen3_class"] == "LiftRequired"
    assert res["specimen3_distance"] is None
    assert res["firewall_audit"]["firewall_intact"] is True
    assert res["firewall_audit"]["authority_effect"] == "None"


# ---------------------------------------------------------------------------
# Blocking Findings B1, B2, B3 Regression Tests
# ---------------------------------------------------------------------------

def test_b1_quotient_universal_factor_uniqueness_and_surjectivity() -> None:
    """
    B1: quotient_universal_factor requires rank(pi) == pi.rows to guarantee factor uniqueness.
    Zero-map counterexample f = [[0, 0]], pi = [[0, 0]] has infinite factors g = [[tau0]],
    and must be rejected.
    """
    # Reproduced review counterexample:
    f_zero = Matrix([[0, 0]])
    pi_zero = Matrix([[0, 0]])
    with pytest.raises(ValueError, match="surjective onto the quotient space"):
        quotient_universal_factor(f_zero, pi_zero)

    # Non-surjective rank-deficient pi:
    pi_deficient = Matrix([[1, 0], [0, 0]])
    f_valid = Matrix([[2, 0]])
    with pytest.raises(ValueError, match="surjective onto the quotient space"):
        quotient_universal_factor(f_valid, pi_deficient)

    # Valid surjective pi with unique exact rational factor:
    # pi : Q^2 -> Q^1, pi = [[1, 2]]
    # f : Q^2 -> Q^1, f = [[3, 6]] = 3 * pi
    pi_surj = Matrix([[1, 2]])
    f_surj = Matrix([[3, 6]])
    g = quotient_universal_factor(f_surj, pi_surj)
    assert g == Matrix([[3]])
    assert (g * pi_surj - f_surj).is_zero_matrix

    # Incompatible f (does not factor through pi):
    f_incompat = Matrix([[1, 0]])
    with pytest.raises(ArithmeticError, match="quotient factorization failed"):
        quotient_universal_factor(f_incompat, pi_surj)


def test_b2_honest_quotient_distances_no_sentinels() -> None:
    """
    B2: classify_closure_attempt computes exact L1 distance for mathematical states,
    and leaves quotient_distance as None for administrative states (no fake 1 or 3/4).
    """
    from coda_a_core import LinearRepairProblem

    # Reproduced review counterexample for OpenResidual:
    d0 = Matrix([[1], [0]])
    d1 = Matrix([[0, 1]])
    x = Matrix([[0], [5]])
    # Valid complex: d1 * d0 = [[0]]
    assert (d1 * d0).is_zero_matrix

    res_open = classify_closure_attempt(d0, d1, x)
    assert res_open.classification == ResidualTerminalClass.OPEN_RESIDUAL
    # Must report exact distance 5, NOT sentinel 1
    assert res_open.quotient_distance == Rational(5, 1)

    # Verify against direct solver call
    solver_cert = LinearRepairProblem(repair_map_d0=d0).quotient_l1_distance(cochain=x)
    assert res_open.quotient_distance == Rational(solver_cert.distance)

    # Administrative states must have quotient_distance is None (never 1 or 3/4)
    res_lift = classify_closure_attempt(d0, d1, x, pending_lift=True)
    assert res_lift.classification == ResidualTerminalClass.LIFT_REQUIRED
    assert res_lift.quotient_distance is None

    res_refused = classify_closure_attempt(d0, d1, x, refusal_reason="Administrative hold")
    assert res_refused.classification == ResidualTerminalClass.REFUSED_CLOSURE
    assert res_refused.quotient_distance is None


def test_b3_classifier_and_residual_outcome_validation_invariants() -> None:
    """
    B3: Strict validation of pending_lift, d1 dimensions, zero-distance invariants,
    identifiers, and refusal text.
    """
    d0 = Matrix([[1], [2]])
    d1 = Matrix([[2, -1]])
    defect = Matrix([[2], [4]])

    # 1. pending_lift="False" (truthy string) must raise TypeError, not become LiftRequired
    with pytest.raises(TypeError, match="pending_lift must be an exact bool"):
        classify_closure_attempt(d0, d1, defect, pending_lift="False")  # type: ignore

    # 2. Zero-row d1 with mismatched column count must fail column dimension check
    d1_zero_row_bad_cols = Matrix.zeros(0, 99)
    with pytest.raises(ValueError, match="d1 cols \\(99\\) must match defect dimension"):
        classify_closure_attempt(d0, d1_zero_row_bad_cols, defect)

    # 3. ClosedResidual with quotient_distance=0 must be rejected
    with pytest.raises(ValueError, match="ClosedResidual must have positive quotient_distance"):
        ResidualOutcome(
            classification=ResidualTerminalClass.CLOSED_RESIDUAL,
            residual_class_id="invalid_zero_closed",
            defect_vector=defect,
            quotient_distance=Rational(0, 1),
            is_closed=True,
        )

    # 4. OpenResidual with quotient_distance=0 must be rejected
    with pytest.raises(ValueError, match="OpenResidual cannot have quotient_distance=0"):
        ResidualOutcome(
            classification=ResidualTerminalClass.OPEN_RESIDUAL,
            residual_class_id="invalid_zero_open",
            defect_vector=defect,
            quotient_distance=Rational(0, 1),
            is_closed=False,
        )

    # 5. Invalid identifiers or refusal reasons must be rejected
    with pytest.raises(TypeError, match="residual_class_id must be a non-empty string"):
        ResidualOutcome(
            classification=ResidualTerminalClass.CLOSED_RESIDUAL,
            residual_class_id="   ",
            defect_vector=defect,
            quotient_distance=Rational(1, 1),
            is_closed=True,
        )

    with pytest.raises(TypeError, match="refusal_reason must be a non-empty string"):
        ResidualOutcome(
            classification=ResidualTerminalClass.REFUSED_CLOSURE,
            residual_class_id="valid_id",
            defect_vector=defect,
            quotient_distance=None,
            is_closed=False,
            refusal_reason="",
        )

    with pytest.raises(TypeError, match="closure_id must be a non-empty string"):
        classify_closure_attempt(d0, d1, defect, closure_id="")

    with pytest.raises(TypeError, match="refusal_reason must be a non-empty string"):
        classify_closure_attempt(d0, d1, defect, refusal_reason="   ")



def test_release_contract_and_forbidden_stale_tokens() -> None:
    """Verify release contract hygiene: canonical title present and forbidden tokens absent."""
    pkg_dir = Path(__file__).resolve().parents[2]

    # Assert obsolete declared axiom file is gone
    old_axiom_file = pkg_dir / "lean4" / "coda_a_t03_declared_anomalon_axiom.lean"
    assert not old_axiom_file.exists(), "coda_a_t03_declared_anomalon_axiom.lean must not exist"

    # Assert new toy witness file is present
    toy_witness_file = pkg_dir / "lean4" / "T03ToyAnomalonWitness.lean"
    assert toy_witness_file.is_file()

    # Check ledger content
    ledger_path = pkg_dir / "coda_a_claim_ledger.md"
    assert ledger_path.is_file()
    ledger_text = ledger_path.read_text(encoding="utf-8")
    assert "CODA-A: Residuals of Projections, Kernels, and Cokernels" in ledger_text
    assert "A-T1" in ledger_text
    assert "A-T7" in ledger_text
    assert "A-S1" in ledger_text
    assert "CA-SPEC-01" not in ledger_text
    assert "ABSORB-008" not in ledger_text

