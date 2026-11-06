# -*- coding: utf-8 -*-
"""
test_coda_cs.py: Unit and mutation test suite for CODA-CS.

Verifies:
1. Section 0 Worked Example reproduction (sampling, quadrature, fiber constancy).
2. 8-step BridgeAdmissible gate pipeline and refusal codes (BRIDGE-003 / CS-T5).
3. GTTC-02 / CS-T5 Continuum Non-Creation Firewall (coherence/limits do not mint authority).
4. Exact cochain quotient solving (LinearRepairProblem) over exact rationals without external dependencies.
5. Strict Zero Floats Invariant (floats and booleans rejected with TypeError at constructors and scalars).
6. Guard 4 non-empty profile enforcement & non-vacuous tower/domain checks.
7. Verified return value binding (re-evaluating stateful callables is prevented).
AuthorityEffect: None.

Run: python -m pytest -n 8 coda_atlas/F005_coda/cs/code/tests -v
"""

from __future__ import annotations

from collections.abc import MutableMapping
from typing import cast

import pytest
from coda_cs_core import (
    R_NO_COFINAL_SHADOW,
    R_NO_FINITE_SHADOW,
    R_NO_PROFILE,
    R_NO_TERMINAL,
    R_NOT_FACTORABLE,
    R_NOT_FIBER_CONSTANT,
    R_SHADOW_COHERENCE_FAILURE,
    R_UNBOUNDED_DEGREE,
    ContinuumQuery,
    ContinuumSignal,
    LinearRepairProblem,
    ProfileMap,
    ShadowSlice,
    ShadowTower,
    _validate_exact_int,
    _validate_exact_rational,
    compute_transition_quotient_obstruction,
    evaluate_query_authority,
    reproduce_worked_example,
    verify_bridge_admissibility,
)
from sympy import Matrix, Rational


def test_worked_example_reproduction() -> None:
    """CS-L1 / CS-T1: Worked Example reproduction."""
    val1, val2, is_admissible = reproduce_worked_example()
    # Quadrature sum for X(t) = 2t on grid:
    # t=0: 0, t=1/4: 1/2 (sq=1/4), t=2/4: 1 (sq=1), t=3/4: 3/2 (sq=9/4)
    # Sum of squares = 1/4 + 1 + 9/4 = 14/4 = 7/2. Times dt=1/4 = 7/8.
    assert val1 == Rational(7, 8)
    assert val2 == Rational(7, 8)
    assert is_admissible is True


def test_bridge_admissibility_gates() -> None:
    """8-Step BridgeAdmissible conditions and refusal branches."""
    pts = (Rational(0, 1), Rational(1, 2), Rational(1, 1))
    prof = ProfileMap(profile_id="Grid_3", sample_points=pts)
    samples = {p: Rational(p) for p in pts}
    sig = ContinuumSignal(signal_id="Sig1", samples=samples)

    # Base valid query
    q_valid = ContinuumQuery(query_id="Q1", degree_bound=2, evaluator=lambda s: Rational(1, 2))
    tower_valid = ShadowTower(
        tower_id="TowerValid",
        slices=(ShadowSlice("S1", 3, True),),
        is_cofinal=True,
    )

    # 1. Degree unbounded
    q_deg = ContinuumQuery(query_id="Q_High", degree_bound=6, evaluator=lambda s: Rational(1, 2))
    rep_deg = verify_bridge_admissibility(query=q_deg, tower=tower_valid, profile=prof, test_signals=[sig], max_degree=4)
    assert rep_deg.overall_admissible is False
    assert rep_deg.refusal_code == R_UNBOUNDED_DEGREE

    # 2. Non-cofinal
    tower_not_cofinal = ShadowTower(
        tower_id="TowerNotCofinal",
        slices=(ShadowSlice("S1", 3, True),),
        is_cofinal=False,
    )
    rep_cofinal = verify_bridge_admissibility(query=q_valid, tower=tower_not_cofinal, profile=prof, test_signals=[sig])
    assert rep_cofinal.overall_admissible is False
    assert rep_cofinal.refusal_code == R_NO_COFINAL_SHADOW

    # 3. Non-finite or unauthorized shadow
    tower_unauth = ShadowTower(
        tower_id="TowerUnauth",
        slices=(ShadowSlice("S1", 3, False),),
        is_cofinal=True,
    )
    rep_unauth = verify_bridge_admissibility(query=q_valid, tower=tower_unauth, profile=prof, test_signals=[sig])
    assert rep_unauth.overall_admissible is False
    assert rep_unauth.refusal_code == R_NO_FINITE_SHADOW

    # 4. Factorization mismatch
    rep_factor = verify_bridge_admissibility(
        query=q_valid,
        tower=tower_valid,
        profile=prof,
        test_signals=[sig],
        factored_evaluator=lambda v: Rational(99, 1),  # deliberately mismatching factored evaluator
    )
    assert rep_factor.overall_admissible is False
    assert rep_factor.refusal_code == R_NOT_FACTORABLE

    # 5. Fiber constancy violation: two signals with identical profile, but differing query values
    sig_alt = ContinuumSignal(signal_id="Sig2", samples=samples)
    q_fiber_bad = ContinuumQuery(
        query_id="Q_BadFiber",
        degree_bound=1,
        evaluator=lambda s: Rational(1, 1) if s.signal_id == "Sig1" else Rational(2, 1),
    )
    rep_fiber = verify_bridge_admissibility(
        query=q_fiber_bad,
        tower=tower_valid,
        profile=prof,
        test_signals=[sig, sig_alt],
        factored_evaluator=lambda v: Rational(1, 1),
    )
    assert rep_fiber.overall_admissible is False
    assert rep_fiber.refusal_code == R_NOT_FIBER_CONSTANT

    # 6. Local terminalizer missing
    rep_no_term = verify_bridge_admissibility(
        query=q_valid,
        tower=tower_valid,
        profile=prof,
        test_signals=[sig],
        factored_evaluator=lambda v: Rational(1, 2),
        has_terminalizer=False,
    )
    assert rep_no_term.overall_admissible is False
    assert rep_no_term.refusal_code == R_NO_TERMINAL

    # 7. Transition coherence failure (null transition)
    rep_no_trans = verify_bridge_admissibility(
        query=q_valid,
        tower=tower_valid,
        profile=prof,
        test_signals=[sig],
        factored_evaluator=lambda v: Rational(1, 2),
        has_terminalizer=True,
        d0_transition=None,
        defect_1cochain=None,
    )
    assert rep_no_trans.overall_admissible is False
    assert rep_no_trans.refusal_code == R_SHADOW_COHERENCE_FAILURE

    # 8. All gates pass
    rep_ok = verify_bridge_admissibility(
        query=q_valid,
        tower=tower_valid,
        profile=prof,
        test_signals=[sig],
        factored_evaluator=lambda v: Rational(1, 2),
        has_terminalizer=True,
        d0_transition=Matrix([[1]]),
        defect_1cochain=Matrix([[0]]),
    )
    assert rep_ok.overall_admissible is True
    assert rep_ok.refusal_code is None
    assert rep_ok.residual_mass == Rational(0, 1)
    assert rep_ok.is_profile_surjective is True


def test_guard_4_profile_nonempty_and_vacuous_checks() -> None:
    """Guard 4: Empty profile, empty tower, and empty test signals domain must refuse."""
    # 1. Empty profile
    empty_prof = ProfileMap(profile_id="EmptyGrid", sample_points=())
    pts = (Rational(0, 1), Rational(1, 1))
    sig = ContinuumSignal("Sig", {p: p for p in pts})
    q = ContinuumQuery("Q", 1, lambda s: Rational(0, 1))
    tower = ShadowTower("Tower", (ShadowSlice("S1", 1, True),), True)

    rep_empty_prof = verify_bridge_admissibility(
        query=q, tower=tower, profile=empty_prof, test_signals=[sig]
    )
    assert rep_empty_prof.is_profile_surjective is False
    assert rep_empty_prof.overall_admissible is False
    assert rep_empty_prof.refusal_code == R_NO_PROFILE

    # 2. Empty tower slices (must not pass vacuously)
    empty_tower = ShadowTower("EmptyTower", (), True)
    assert empty_tower.all_slices_authorized() is False
    rep_empty_tower = verify_bridge_admissibility(
        query=q, tower=empty_tower, profile=ProfileMap("P", pts), test_signals=[sig]
    )
    assert rep_empty_tower.is_shadow_finite is False
    assert rep_empty_tower.overall_admissible is False
    assert rep_empty_tower.refusal_code == R_NO_FINITE_SHADOW

    # 3. Empty test signals list (must not pass vacuously)
    rep_empty_signals = verify_bridge_admissibility(
        query=q, tower=tower, profile=ProfileMap("P", pts), test_signals=[]
    )
    assert rep_empty_signals.overall_admissible is False
    assert rep_empty_signals.refusal_code == R_NOT_FACTORABLE


def test_continuum_non_creation_firewall() -> None:
    """CS-T5: Continuum Non-Creation Firewall."""
    pts = (Rational(0, 1), Rational(1, 1))
    prof = ProfileMap(profile_id="Grid_2", sample_points=pts)
    samples = {p: Rational(p) for p in pts}
    sig = ContinuumSignal(signal_id="Sig1", samples=samples)
    q = ContinuumQuery(query_id="Q1", degree_bound=1, evaluator=lambda s: Rational(1, 1))
    tower = ShadowTower("Tower", (ShadowSlice("S1", 2, True),), is_cofinal=True)

    # Missing terminalizer blocks query authority
    res_no_term = evaluate_query_authority(
        signal=sig,
        query=q,
        tower=tower,
        profile=prof,
        factored_evaluator=lambda v: Rational(1, 1),
        has_terminalizer=False,
    )
    assert res_no_term.inhabited is False
    assert res_no_term.evaluated_value is None
    assert res_no_term.refusal_code == R_NO_TERMINAL
    assert res_no_term.authority_effect == "None"

    # Authorized query
    res_ok = evaluate_query_authority(
        signal=sig,
        query=q,
        tower=tower,
        profile=prof,
        factored_evaluator=lambda v: Rational(1, 1),
        has_terminalizer=True,
        d0_transition=Matrix([[1]]),
        defect_1cochain=Matrix([[0]]),
    )
    assert res_ok.inhabited is True
    assert res_ok.evaluated_value == Rational(1, 1)
    assert res_ok.authority_effect == "None"


def test_stateful_callable_binds_verified_value() -> None:
    """evaluate_query_authority returns the verified value, not an unchecked re-evaluation."""
    pts = (Rational(0, 1), Rational(1, 1))
    prof = ProfileMap(profile_id="Grid_2", sample_points=pts)
    samples = {p: Rational(p) for p in pts}
    sig = ContinuumSignal(signal_id="Sig1", samples=samples)

    # Stateful query returns Rational(1, 1) first, then Rational(99, 1)
    call_count = 0

    def stateful_eval(s: ContinuumSignal) -> Rational:
        nonlocal call_count
        call_count += 1
        return Rational(1, 1) if call_count <= 1 else Rational(99, 1)

    q = ContinuumQuery(query_id="Q_Stateful", degree_bound=1, evaluator=stateful_eval)
    tower = ShadowTower("Tower", (ShadowSlice("S1", 2, True),), is_cofinal=True)

    res = evaluate_query_authority(
        signal=sig,
        query=q,
        tower=tower,
        profile=prof,
        factored_evaluator=lambda v: Rational(1, 1),
        has_terminalizer=True,
        d0_transition=Matrix([[1]]),
        defect_1cochain=Matrix([[0]]),
    )
    assert res.inhabited is True
    # The verified value was Rational(1, 1); second call would be 99. The verified value must be returned.
    assert res.evaluated_value == Rational(1, 1)


def test_transition_cochain_quotient_solver() -> None:
    """Verify exact cochain quotient solver on shadow transitions."""
    # Basis map d0: 2 x 1
    d0 = Matrix([[1], [2]])

    # Exact defect in im(d0): [3, 6] = 3 * [1, 2]
    defect_exact = Matrix([[3], [6]])
    dist_exact, witness_exact, is_exact = compute_transition_quotient_obstruction(d0, defect_exact)
    assert dist_exact == Rational(0, 1)
    assert witness_exact == Matrix([[3]])
    assert is_exact is True

    # Non-exact defect: [1, 0]
    defect_non_exact = Matrix([[1], [0]])
    dist_ne, _witness_ne, is_ne = compute_transition_quotient_obstruction(d0, defect_non_exact)
    assert dist_ne > Rational(0, 1)
    assert is_ne is False


def test_standalone_cochain_presentation() -> None:
    """Direct verification of LinearRepairProblem and QuotientDistanceCertificate."""
    d0 = Matrix([[1], [1]])
    problem = LinearRepairProblem(repair_map_d0=d0)

    # Exact case
    cert_exact = problem.exactness_certificate(Matrix([[2], [2]]))
    assert cert_exact.is_exact_coboundary is True
    assert cert_exact.verify() is True

    # Separating witness case
    cert_sep = problem.exactness_certificate(Matrix([[1], [0]]))
    assert cert_sep.is_exact_coboundary is False
    assert cert_sep.verify() is True

    # Quotient distance certificate
    quotient_cert = problem.quotient_l1_distance(Matrix([[1], [0]]))
    assert quotient_cert.verify() is True
    assert quotient_cert.distance == Rational(1, 1)


def test_zero_floats_invariant() -> None:
    """Strictly reject IEEE 754 floating point and booleans."""
    # Scalar rational validation
    assert _validate_exact_rational(Rational(2, 5), "x") == Rational(2, 5)
    assert _validate_exact_rational(10, "x") == Rational(10, 1)
    assert _validate_exact_rational("3/7", "x") == Rational(3, 7)

    with pytest.raises(TypeError, match="got float"):
        _validate_exact_rational(0.5, "x")

    with pytest.raises(TypeError, match="got bool"):
        _validate_exact_rational(False, "x")

    # Integer validation
    assert _validate_exact_int(4, "dim") == 4
    with pytest.raises(TypeError, match="got bool"):
        _validate_exact_int(True, "dim")
    with pytest.raises(TypeError):
        _validate_exact_int(4.0, "dim")
    with pytest.raises(ValueError, match="non-negative"):
        _validate_exact_int(-3, "dim")

    # Float in signal sample evaluation
    sig = ContinuumSignal("S", {Rational(0, 1): Rational(1, 1)})
    with pytest.raises(TypeError, match="got float"):
        sig.evaluate_at(0.0)

    # Float in defect vector
    d0 = Matrix([[1], [1]])
    with pytest.raises(TypeError, match="floats strictly forbidden"):
        compute_transition_quotient_obstruction(d0, Matrix([[1.5], [2.0]]))


def test_exact_rational_constructors_and_immutability() -> None:
    """Constructors of ContinuumSignal and ProfileMap reject floats, booleans, and enforce immutability."""
    # ContinuumSignal rejects float keys
    with pytest.raises(TypeError, match="got float"):
        ContinuumSignal("FloatKey", {0.5: Rational(1, 1)})

    # ContinuumSignal rejects float values
    with pytest.raises(TypeError, match="got float"):
        ContinuumSignal("FloatVal", {Rational(0, 1): 0.5})

    # ContinuumSignal rejects bool keys
    with pytest.raises(TypeError, match="got bool"):
        ContinuumSignal("BoolKey", {True: Rational(1, 1)})

    # ContinuumSignal rejects bool values
    with pytest.raises(TypeError, match="got bool"):
        ContinuumSignal("BoolVal", {Rational(0, 1): False})

    # ProfileMap rejects float points
    with pytest.raises(TypeError, match="got float"):
        ProfileMap("FloatPt", (0.5,))

    # ProfileMap rejects bool points
    with pytest.raises(TypeError, match="got bool"):
        ProfileMap("BoolPt", (True,))

    # Immutability snapshot: mutating original dictionary does not change signal samples
    input_dict = {Rational(0, 1): Rational(0, 1)}
    sig = ContinuumSignal("Sig", input_dict)
    input_dict[Rational(0, 1)] = Rational(9, 1)
    assert sig.evaluate_at(Rational(0, 1)) == Rational(0, 1)


def test_cs_edge_cases_and_uncovered_branches() -> None:
    with pytest.raises(TypeError, match="string could not be converted"):
        _validate_exact_rational("abc", "x")
    with pytest.raises(TypeError, match="got list"):
        _validate_exact_rational([1, 2], "x")

    slice_s1 = ShadowSlice("S1", 2, True)
    slice_s2 = ShadowSlice("S2", 3, True)
    tower = ShadowTower("T", (slice_s1, slice_s2), True)
    assert tower.get_slice("S1") == slice_s1
    assert tower.get_slice("S2") == slice_s2
    assert tower.get_slice("missing") is None
    assert ShadowTower("empty", (), True).get_slice("S1") is None

    sig = ContinuumSignal("S", {Rational(0, 1): Rational(1, 1)})
    with pytest.raises(KeyError, match="has no sample"):
        sig.evaluate_at(Rational(1, 1))


def test_cs03_factors_fst_snd_is_false_on_bool_pair() -> None:
    """Reconstruction CS-03: Factors(fst, snd) is false on Bool×Bool."""
    signals = tuple(
        ContinuumSignal(
            signal_id=f"({a},{b})",
            samples={Rational(0, 1): Rational(a), Rational(1, 1): Rational(b)},
        )
        for a, b in ((0, 0), (0, 1), (1, 0), (1, 1))
    )
    q_snd = ContinuumQuery(
        query_id="snd",
        degree_bound=1,
        evaluator=lambda s: s.evaluate_at(Rational(1, 1)),
    )
    q_fst = ContinuumQuery(
        query_id="fst",
        degree_bound=1,
        evaluator=lambda s: s.evaluate_at(Rational(0, 1)),
    )
    profile_fst = ProfileMap(profile_id="fst", sample_points=(Rational(0, 1),))
    profile_full = ProfileMap(
        profile_id="id",
        sample_points=(Rational(0, 1), Rational(1, 1)),
    )
    tower = ShadowTower(
        tower_id="BoolxBool",
        slices=(ShadowSlice("pair", 2, True),),
        is_cofinal=True,
    )

    assert signals[0].evaluate_at(Rational(0, 1)) == signals[1].evaluate_at(Rational(0, 1))
    assert signals[0].evaluate_at(Rational(1, 1)) != signals[1].evaluate_at(Rational(1, 1))

    report_snd_through_fst = verify_bridge_admissibility(
        query=q_snd,
        tower=tower,
        profile=profile_fst,
        test_signals=signals,
    )
    assert report_snd_through_fst.is_fiber_constant is False
    assert report_snd_through_fst.overall_admissible is False
    assert report_snd_through_fst.refusal_code == R_NOT_FIBER_CONSTANT

    report_fst_through_fst = verify_bridge_admissibility(
        query=q_fst,
        tower=tower,
        profile=profile_fst,
        test_signals=signals,
        factored_evaluator=lambda vec: Rational(vec[0, 0]),
        d0_transition=Matrix([[1]]),
        defect_1cochain=Matrix([[0]]),
    )
    assert report_fst_through_fst.is_fiber_constant is True
    assert report_fst_through_fst.is_factorable is True
    assert report_fst_through_fst.overall_admissible is True

    report_snd_through_full = verify_bridge_admissibility(
        query=q_snd,
        tower=tower,
        profile=profile_full,
        test_signals=signals,
        factored_evaluator=lambda vec: Rational(vec[1, 0]),
        d0_transition=Matrix([[1]]),
        defect_1cochain=Matrix([[0]]),
    )
    assert report_snd_through_full.is_fiber_constant is True
    assert report_snd_through_full.is_factorable is True
    assert report_snd_through_full.overall_admissible is True

    # Pre-fix evaluate_query_authority used test_signals=[signal] and inhabited
    # a colliding snd-through-fst packet. The family must refuse.
    inhabited_on_one = evaluate_query_authority(
        signal=signals[0],
        query=q_snd,
        tower=tower,
        profile=profile_fst,
        has_terminalizer=True,
        d0_transition=Matrix([[1]]),
        defect_1cochain=Matrix([[0]]),
    )
    family_gate = evaluate_query_authority(
        signal=signals[0],
        query=q_snd,
        tower=tower,
        profile=profile_fst,
        test_signals=signals,
        has_terminalizer=True,
        d0_transition=Matrix([[1]]),
        defect_1cochain=Matrix([[0]]),
    )
    assert inhabited_on_one.inhabited is True
    assert family_gate.inhabited is False
    assert family_gate.refusal_code == R_NOT_FIBER_CONSTANT


def test_transition_coherence_uses_exact_solver() -> None:
    # Invariant: step 7 is the cochain solver, not a constant True.
    pts = (Rational(0, 1), Rational(1, 1))
    prof = ProfileMap(profile_id="Grid_2", sample_points=pts)
    sig = ContinuumSignal("S", {p: p for p in pts})
    q = ContinuumQuery(query_id="Q", degree_bound=1, evaluator=lambda s: Rational(1, 1))
    tower = ShadowTower("T", (ShadowSlice("S1", 2, True),), True)
    def factored(v):
        return Rational(1, 1)

    missing = verify_bridge_admissibility(
        query=q, tower=tower, profile=prof, test_signals=[sig], factored_evaluator=factored
    )
    assert missing.is_transition_coherent is False
    assert missing.overall_admissible is False
    assert missing.refusal_code == R_SHADOW_COHERENCE_FAILURE

    leftover = Matrix([[1], [0]])
    d0 = Matrix([[1], [2]])
    leftover_report = verify_bridge_admissibility(
        query=q,
        tower=tower,
        profile=prof,
        test_signals=[sig],
        factored_evaluator=factored,
        d0_transition=d0,
        defect_1cochain=leftover,
    )
    dist, _w, is_exact = compute_transition_quotient_obstruction(d0, leftover)
    assert is_exact is False
    assert leftover_report.is_transition_coherent is False
    assert leftover_report.overall_admissible is False
    assert leftover_report.refusal_code == R_SHADOW_COHERENCE_FAILURE
    assert leftover_report.residual_mass == dist

    exact = verify_bridge_admissibility(
        query=q,
        tower=tower,
        profile=prof,
        test_signals=[sig],
        factored_evaluator=factored,
        d0_transition=Matrix([[1]]),
        defect_1cochain=Matrix([[0]]),
    )
    assert exact.is_transition_coherent is True
    assert exact.overall_admissible is True


def test_cs_t2_family_observation_equality() -> None:
    """
    CS-T2: Family observation equality is pointwise.
    (observe_i(X) = observe_i(Y) forall i in I) <=> Prof_I(X) = Prof_I(Y).
    Tests both directions of the equivalence across a family of signals.
    """
    pts = (Rational(0, 4), Rational(1, 4), Rational(2, 4), Rational(3, 4))
    prof = ProfileMap(profile_id="Grid_4", sample_points=pts)

    sig1 = ContinuumSignal("Sig1", {t: Rational(2) * t for t in pts})
    sig2 = ContinuumSignal("Sig2", {t: Rational(2) * t for t in pts})
    sig3 = ContinuumSignal("Sig3", {pts[0]: Rational(0), pts[1]: Rational(9, 10), pts[2]: Rational(1), pts[3]: Rational(3, 2)})
    sig4 = ContinuumSignal("Sig4", {pts[0]: Rational(0), pts[1]: Rational(1, 2), pts[2]: Rational(1), pts[3]: Rational(9, 10)})

    family = [sig1, sig2, sig3, sig4]

    for x in family:
        for y in family:
            pointwise_agree = all(x.evaluate_at(t) == y.evaluate_at(t) for t in pts)
            prof_x = prof.project(x)
            prof_y = prof.project(y)
            profile_agree = (prof_x == prof_y)
            assert pointwise_agree == profile_agree, f"CS-T2 violated for pair ({x.signal_id}, {y.signal_id})"

    assert prof.project(sig1) == prof.project(sig2)
    assert prof.project(sig1) != prof.project(sig3)
    assert prof.project(sig1)[1, 0] != prof.project(sig3)[1, 0]


def test_duplicate_display_ids_cannot_return_another_signals_value() -> None:
    """[P1 Acceptance Regression]: Duplicate signal identifiers raise ValueError."""
    first = ContinuumSignal("same-label", {Rational(0): Rational(0)})
    second = ContinuumSignal("same-label", {Rational(0): Rational(1)})
    query = ContinuumQuery("read-zero", 1, lambda signal: signal.evaluate_at(0))
    tower = ShadowTower("tower", (ShadowSlice("slice", 1, True),), True)
    profile = ProfileMap("profile", (Rational(0),))
    with pytest.raises(ValueError, match="Duplicate signal identifier in test_signals"):
        evaluate_query_authority(
            first,
            query,
            tower=tower,
            profile=profile,
            test_signals=[first, second],
            factored_evaluator=lambda vec: vec[0, 0],
            d0_transition=Matrix([[1]]),
            defect_1cochain=Matrix([[0]]),
        )


def test_verified_result_cannot_depend_on_family_iteration_order() -> None:
    """[P1 Acceptance Regression]: Reordering signals yields identical verified values."""
    sig_a = ContinuumSignal("sig-a", {Rational(0): Rational(0)})
    sig_b = ContinuumSignal("sig-b", {Rational(0): Rational(1)})
    query = ContinuumQuery("read-zero", 1, lambda signal: signal.evaluate_at(0))
    tower = ShadowTower("tower", (ShadowSlice("slice", 1, True),), True)
    profile = ProfileMap("profile", (Rational(0),))
    kwargs = {
        "tower": tower,
        "profile": profile,
        "factored_evaluator": lambda vec: vec[0, 0],
        "d0_transition": Matrix([[1]]),
        "defect_1cochain": Matrix([[0]]),
    }
    res_a1 = evaluate_query_authority(sig_a, query, test_signals=[sig_a, sig_b], **kwargs)
    res_a2 = evaluate_query_authority(sig_a, query, test_signals=[sig_b, sig_a], **kwargs)
    assert (res_a1.inhabited, res_a1.evaluated_value) == (res_a2.inhabited, res_a2.evaluated_value) == (True, Rational(0))

    res_b1 = evaluate_query_authority(sig_b, query, test_signals=[sig_a, sig_b], **kwargs)
    res_b2 = evaluate_query_authority(sig_b, query, test_signals=[sig_b, sig_a], **kwargs)
    assert (res_b1.inhabited, res_b1.evaluated_value) == (res_b2.inhabited, res_b2.evaluated_value) == (True, Rational(1))


def test_signal_exposed_samples_are_immutable() -> None:
    """[P2 Acceptance Regression]: ContinuumSignal.samples rejects assignment and deletion."""
    signal = ContinuumSignal("snapshot", {Rational(0): Rational(0)})
    # Cast only at the deliberate invalid-mutation boundary.
    with pytest.raises(TypeError):
        cast(MutableMapping[Rational, Rational], signal.samples)[Rational(0)] = Rational(9)
    with pytest.raises(TypeError):
        del cast(MutableMapping[Rational, Rational], signal.samples)[Rational(0)]


def test_terminalizer_guard_requires_an_actual_boolean() -> None:
    """[P2 Acceptance Regression]: Policy flags reject non-boolean types."""
    signal = ContinuumSignal("signal", {Rational(0): Rational(0)})
    query = ContinuumQuery("read-zero", 1, lambda s: s.evaluate_at(0))
    tower = ShadowTower("tower", (ShadowSlice("slice", 1, True),), True)
    profile = ProfileMap("profile", (Rational(0),))
    kwargs = {
        "tower": tower,
        "profile": profile,
        "factored_evaluator": lambda vec: vec[0, 0],
        "d0_transition": Matrix([[1]]),
        "defect_1cochain": Matrix([[0]]),
    }
    with pytest.raises(TypeError, match="has_terminalizer must be bool"):
        verify_bridge_admissibility(query, test_signals=[signal], has_terminalizer=cast(bool, "false"), **kwargs)
    with pytest.raises(TypeError, match="has_terminalizer must be bool"):
        verify_bridge_admissibility(query, test_signals=[signal], has_terminalizer=cast(bool, 1), **kwargs)
    with pytest.raises(TypeError, match="has_terminalizer must be bool"):
        verify_bridge_admissibility(query, test_signals=[signal], has_terminalizer=cast(bool, None), **kwargs)

    with pytest.raises(TypeError, match="has_local_authority must be bool"):
        ShadowSlice("S", 1, cast(bool, "true"))
    with pytest.raises(TypeError, match="is_finite must be bool"):
        ShadowSlice("S", 1, True, is_finite=cast(bool, 1))
    with pytest.raises(TypeError, match="is_cofinal must be bool"):
        ShadowTower("T", (ShadowSlice("S", 1, True),), is_cofinal=cast(bool, "yes"))


def test_solver_edge_cases_and_matrix_types() -> None:
    """Independent checks of LinearRepairProblem on zero-maps, redundant columns, and non-diagonal rationals."""
    from cochain_presentation import LinearRepairProblem

    cases = [
        (Matrix.zeros(0, 0), Matrix.zeros(0, 1), "zero-0x0"),
        (Matrix.zeros(0, 2), Matrix.zeros(0, 1), "zero-0x2"),
        (Matrix.zeros(1, 0), Matrix([[Rational(1)]]), "zero-1x0"),
        (Matrix.zeros(2, 0), Matrix([[Rational(1)], [Rational(2)]]), "zero-2x0"),
        (Matrix.zeros(3, 2), Matrix([[Rational(1)], [Rational(2)], [Rational(3)]]), "zero-3x2"),
        (Matrix([[1, 1], [2, 2], [3, 3]]), Matrix([[1], [0], [0]]), "redundant-columns"),
        (Matrix([[Rational(1, 2), Rational(1, 3)], [0, Rational(2, 5)], [Rational(3, 4), 0]]), Matrix([[Rational(2, 3)], [Rational(-4, 7)], [Rational(3, 5)]]), "rational-nondiagonal"),
    ]

    for a, y, _label in cases:
        problem = LinearRepairProblem(a)
        cert = problem.quotient_l1_distance(y)
        assert cert.distance >= 0
        m, n = a.shape
        if m > 0:
            if n > 0:
                expected_res = y - a * cert.repair_witness
            else:
                expected_res = y
            assert cert.residual == expected_res
            l1_norm = sum(abs(cert.residual[i, 0]) for i in range(m))
            assert l1_norm == cert.distance
            dual_pairing = sum(cert.dual_witness[i, 0] * y[i, 0] for i in range(m))
            assert dual_pairing == cert.distance
            for i in range(m):
                assert abs(cert.dual_witness[i, 0]) <= 1
            if n > 0:
                ann = a.T * cert.dual_witness
                for j in range(n):
                    assert ann[j, 0] == 0


def test_cs_d3_refinement_composite_identity() -> None:
    """CS-D3: Refinement composite identity p = forget circ fine.
    Verifies that coarse observation factors through fine observation via forgetful map.
    """
    fine_pts = (Rational(0, 4), Rational(1, 4), Rational(2, 4), Rational(3, 4))
    coarse_pts = (Rational(0, 4), Rational(2, 4))
    fine_prof = ProfileMap("fine", fine_pts)
    coarse_prof = ProfileMap("coarse", coarse_pts)

    def forget(v):
        return Matrix([[v[0, 0]], [v[2, 0]]])

    for i in range(5):
        sig = ContinuumSignal(f"sig_{i}", {t: Rational(i + 1) * t for t in fine_pts})
        fine_vec = fine_prof.project(sig)
        coarse_vec = coarse_prof.project(sig)
        assert coarse_vec == forget(fine_vec)


def test_decoder_cannot_shorten_the_declared_verification_family() -> None:
    """[P1 Acceptance Regression]: Decoder mutating mutable test_signals list cannot bypass verification."""
    first = ContinuumSignal("first", {Rational(0): Rational(0), Rational(1): Rational(0)})
    second = ContinuumSignal("second", {Rational(0): Rational(0), Rational(1): Rational(1)})
    family = [first, second]

    query = ContinuumQuery("read-one", 1, lambda s: s.evaluate_at(Rational(1)))
    profile = ProfileMap("read-zero", (Rational(0),))
    tower = ShadowTower("tower", (ShadowSlice("slice", 1, True),), True)

    def popping_decoder(_vec: Matrix) -> Rational:
        if len(family) > 1:
            family.pop()
        return Rational(0)

    result = evaluate_query_authority(
        second,
        query,
        tower=tower,
        profile=profile,
        test_signals=family,
        factored_evaluator=popping_decoder,
        d0_transition=Matrix([[1]]),
        defect_1cochain=Matrix([[0]]),
    )
    assert not result.inhabited
    assert result.evaluated_value is None


def test_fibre_collision_cannot_be_reported_as_factorable() -> None:
    """[P2 Acceptance Regression]: When fibre collision is witnessed, is_factorable must be False by CS-L1."""
    first = ContinuumSignal("first", {Rational(0): Rational(0), Rational(1): Rational(0)})
    second = ContinuumSignal("second", {Rational(0): Rational(0), Rational(1): Rational(1)})
    query = ContinuumQuery("read-one", 1, lambda s: s.evaluate_at(Rational(1)))
    profile = ProfileMap("read-zero", (Rational(0),))
    tower = ShadowTower("tower", (ShadowSlice("slice", 1, True),), True)

    report = verify_bridge_admissibility(
        query,
        tower=tower,
        profile=profile,
        test_signals=[first, second],
        factored_evaluator=lambda v: Rational(0),
        d0_transition=Matrix([[1]]),
        defect_1cochain=Matrix([[0]]),
    )
    assert not report.is_fiber_constant
    assert not report.is_factorable
    assert not report.overall_admissible


def test_early_decoder_mismatch_must_not_certify_unchecked_fibre_constancy() -> None:
    """[P2 Acceptance Regression]: An early decoder mismatch must not abort fibre constancy check or falsely certify it."""
    first = ContinuumSignal("first", {Rational(0): Rational(0), Rational(1): Rational(0)})
    second = ContinuumSignal("second", {Rational(0): Rational(0), Rational(1): Rational(1)})
    query = ContinuumQuery("read-one", 1, lambda s: s.evaluate_at(Rational(1)))
    profile = ProfileMap("read-zero", (Rational(0),))
    tower = ShadowTower("tower", (ShadowSlice("slice", 1, True),), True)

    report = verify_bridge_admissibility(
        query,
        tower=tower,
        profile=profile,
        test_signals=[first, second],
        factored_evaluator=lambda v: Rational(9),
        d0_transition=Matrix([[1]]),
        defect_1cochain=Matrix([[0]]),
    )
    assert not report.is_fiber_constant
    assert not report.is_factorable
    assert not report.overall_admissible


