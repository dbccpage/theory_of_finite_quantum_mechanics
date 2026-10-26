# -*- coding: utf-8 -*-
r"""
test_coda_gtla.py: Comprehensive test suite for CODA-GTLA (Layered Authority and the Master Normal Form).

Governing Claims:
- GTLA-01: Master Normal Form 5-stage factorization in CODA_pres.
- GTLA-02: Nine-layer authority conservation & non-promotion firewall ([delta_b] in Q^1_b -/-> Auth).
- GTLA-03: Two-rule core loop & tie retention.
- GTLA-04: Sealed Genesis demarcation & blind evaluation kernel.
- CD-12: Faithful groupoid embedding with two-level cost accounting.
- Zero Floats Invariant: strictly zero IEEE 754 floats in exact decision paths.
- Standalone cochain solver bridge: LinearRepairProblem & mechanical dual witness validation.

AuthorityEffect: None.
"""

from __future__ import annotations

import coda_gtla_engine
import pytest
from coda_gtla_core import (
    AuthorityToken,
    ComparisonSpan,
    DSharpOutput,
    FaithfulGroupoidEmbedding,
    FiniteGroupoid,
    FinitePresentation,
    FocSharpOutput,
    LinearRepairProblem,
    ProblemInstance,
    RSharpOutput,
    TerminalKind,
    TerminalOutcome,
    Trace,
    _validate_exact_int,
    _validate_exact_rational,
    compose_spans,
    erase_trace,
    evaluate_authority_firewall,
    execute_master_normal_form,
    execute_two_rule_repair_loop,
    extensional_equal,
    functor_d_sharp,
    functor_foc_sharp,
    functor_r_sharp,
    functor_rho_sharp,
    functor_tau_sharp,
    make_diag_span,
    make_id_trace,
    make_z2_groupoid,
    make_z3_groupoid,
    observation_collision_countermodel,
    reproduce_master_normal_form_example,
    untrusted_verifier_countermodel,
    validate_dual_witness,
)
from sympy import Float, Matrix, Rational


def _authorized_packet() -> ProblemInstance:
    """Exact repair with license: same payload as test_master_normal_form_authorized_case."""
    return ProblemInstance(
        problem_id="test_auth",
        raw_data="authorized_data",
        candidate_sieve=("cand1",),
        coarse_profile=(0, 1),
        fine_profile=(0, 1),
        projection_map={0: 0, 1: 1},
        local_sections={"U0": (Rational(0, 1),)},
        overlaps={("U0", "U0"): True},
        d0=Matrix([[1], [-1]]),
        d1=Matrix([[1, 1]]),
        defect_cochain=Matrix([[1], [-1]]),
        fda_license_granted=True,
    )


def _anomalon_packet(*, problem_id: str = "test_anomalon", defect=None) -> ProblemInstance:
    """Closed residual: same payload as test_master_normal_form_closed_residual_anomalon."""
    return ProblemInstance(
        problem_id=problem_id,
        raw_data="anomalon_data",
        candidate_sieve=("cand1",),
        coarse_profile=(0, 1),
        fine_profile=(0, 1),
        projection_map={0: 0, 1: 1},
        local_sections={"U0": (Rational(1, 2),)},
        overlaps={("U0", "U0"): True},
        d0=Matrix([[0], [0]]),
        d1=Matrix([[0, 0]]),
        defect_cochain=Matrix([[1], [1]]) if defect is None else defect,
        fda_license_granted=False,
    )


def _empty_sieve_packet() -> ProblemInstance:
    """Empty candidate sieve: same payload as test_master_normal_form_refusal_empty_sieve."""
    return ProblemInstance(
        problem_id="test_empty_sieve",
        raw_data="empty_sieve_data",
        candidate_sieve=(),
        coarse_profile=(0,),
        fine_profile=(0,),
        projection_map={0: 0},
        local_sections={},
        overlaps={},
        d0=Matrix([[1]]),
        d1=None,
        defect_cochain=Matrix([[1]]),
        fda_license_granted=False,
    )


def _nonclosed_packet() -> ProblemInstance:
    """Gamma_2 > 0: same payload as test_master_normal_form_refusal_nonclosed_defect."""
    return ProblemInstance(
        problem_id="test_nonclosed",
        raw_data="nonclosed_data",
        candidate_sieve=("cand1",),
        coarse_profile=(0, 1),
        fine_profile=(0, 1),
        projection_map={0: 0, 1: 1},
        local_sections={"U0": (Rational(0, 1),)},
        overlaps={("U0", "U0"): True},
        d0=Matrix([[1], [1]]),
        d1=Matrix([[1, -1]]),
        defect_cochain=Matrix([[2], [0]]),
        fda_license_granted=True,
    )


# ---------------------------------------------------------------------------
# 1. Zero Floats Invariant Tests
# ---------------------------------------------------------------------------


def test_zero_floats_invariant_scalar_rational():
    """Exact integers, fractions, and Rationals are admitted; floats/booleans raise TypeError."""
    assert _validate_exact_rational(42, "test_int") == Rational(42, 1)
    assert _validate_exact_rational("3/5", "test_str") == Rational(3, 5)
    assert _validate_exact_rational(Rational(7, 3), "test_rat") == Rational(7, 3)

    # Forbidden: floats
    with pytest.raises(TypeError, match="floats strictly forbidden"):
        _validate_exact_rational(3.14159, "float_val")

    with pytest.raises(TypeError, match="floats strictly forbidden"):
        _validate_exact_rational(Float(2.718), "sympy_float_val")

    # Forbidden: booleans
    with pytest.raises(TypeError, match="got bool"):
        _validate_exact_rational(True, "bool_val")

    with pytest.raises(TypeError, match="got bool"):
        _validate_exact_rational(False, "bool_val")


def test_zero_floats_invariant_scalar_int():
    """Exact integers are admitted; floats/booleans raise TypeError; negatives raise ValueError."""
    assert _validate_exact_int(10, "int_val") == 10
    with pytest.raises(TypeError, match="got bool"):
        _validate_exact_int(True, "bool_int")
    with pytest.raises(TypeError, match="must be an integer"):
        _validate_exact_int(5.5, "float_int")
    with pytest.raises(ValueError, match="must be non-negative"):
        _validate_exact_int(-3, "neg_int")


# ---------------------------------------------------------------------------
# 2. Categorical Foundations: CODA_pres and CODA_trace Tests
# ---------------------------------------------------------------------------


def test_presentation_validation():
    """Finite presentations enforce carrier size, square symmetry, diagonal zero, and non-negativity."""
    zero_diff = ((Rational(0, 1), Rational(1, 2)), (Rational(1, 2), Rational(0, 1)))
    p = FinitePresentation(name="P2", carrier_size=2, diff_matrix=zero_diff)
    assert p.carrier_size == 2
    assert p.diff_matrix[0][1] == Rational(1, 2)

    # Asymmetry rejection
    asym_diff = ((Rational(0, 1), Rational(1, 1)), (Rational(2, 1), Rational(0, 1)))
    with pytest.raises(ValueError, match="must be symmetric"):
        FinitePresentation(name="P_asym", carrier_size=2, diff_matrix=asym_diff)

    # Non-zero diagonal rejection
    diag_diff = ((Rational(1, 1), Rational(1, 1)), (Rational(1, 1), Rational(0, 1)))
    with pytest.raises(ValueError, match="Self-difference on diagonal must be zero"):
        FinitePresentation(name="P_diag", carrier_size=2, diff_matrix=diag_diff)


def test_span_composition_pullback_and_subadditivity():
    """Pullback composition of spans is associative and cost is subadditive."""
    p1 = FinitePresentation(
        name="P1",
        carrier_size=2,
        diff_matrix=((Rational(0), Rational(1)), (Rational(1), Rational(0))),
    )
    p2 = FinitePresentation(
        name="P2",
        carrier_size=2,
        diff_matrix=((Rational(0), Rational(1)), (Rational(1), Rational(0))),
    )
    p3 = FinitePresentation(
        name="P3",
        carrier_size=2,
        diff_matrix=((Rational(0), Rational(1)), (Rational(1), Rational(0))),
    )

    s1 = ComparisonSpan(
        p1=p1,
        p2=p2,
        mid_size=2,
        left_map=(0, 1),
        right_map=(0, 1),
        ext_cost=Rational(1, 2),
    )
    s2 = ComparisonSpan(
        p1=p2,
        p2=p3,
        mid_size=2,
        left_map=(0, 1),
        right_map=(0, 1),
        ext_cost=Rational(3, 4),
    )

    s_comp = compose_spans(s1, s2)
    assert s_comp.p1 == p1
    assert s_comp.p2 == p3
    assert s_comp.mid_size == 2
    assert s_comp.ext_cost == Rational(5, 4)

    # Diagonal identity span cost is zero
    diag = make_diag_span(p1)
    assert diag.ext_cost == Rational(0, 1)

    # Identity composition
    s1_diag = compose_spans(diag, s1)
    assert s1_diag.ext_cost == s1.ext_cost
    assert s1_diag.mid_size == s1.mid_size


def test_trace_and_two_level_cost_accounting():
    """Two-level cost: extensional round-trip cost is zero, intensional work is strictly positive."""
    z2 = make_z2_groupoid()
    assert z2.validate()
    emb = FaithfulGroupoidEmbedding(z2)
    assert emb.check_faithfulness()

    cost_report = emb.check_two_level_cost_accounting(mor="g", work=Rational(3, 1))
    assert cost_report["extensional_is_zero"] is True
    assert cost_report["extensional_cost"] == Rational(0, 1)
    assert cost_report["intensional_is_positive"] is True
    assert cost_report["intensional_work_cost"] == Rational(6, 1)
    assert cost_report["trace_steps"] == 2


def test_z3_groupoid_embedding():
    """Z3 groupoid embedding validates identity and non-trivial morphism round-trips."""
    z3 = make_z3_groupoid()
    assert z3.validate()
    emb = FaithfulGroupoidEmbedding(z3)
    assert emb.check_faithfulness()

    report_g = emb.check_two_level_cost_accounting(mor="g", work=Rational(2, 1))
    assert report_g["extensional_is_zero"] is True
    assert report_g["intensional_is_positive"] is True


# ---------------------------------------------------------------------------
# 3. Master Normal Form 5-Stage Pipeline Tests (GTLA-01)
# ---------------------------------------------------------------------------


def test_master_normal_form_authorized_case():
    """Case 1: Exact repair with granted license lands in T_auth."""
    receipt = execute_master_normal_form(_authorized_packet())
    assert receipt.is_authorized() is True
    assert receipt.is_anomalon() is False
    assert receipt.is_refused() is False
    assert receipt.terminal_outcome.kind == TerminalKind.AUTHORIZED
    assert receipt.terminal_outcome.phi1_distance == Rational(0, 1)


def test_master_normal_form_closed_residual_anomalon():
    """Case 2: Closed non-bounding residual lands in T_res (The Anomalon)."""
    receipt = execute_master_normal_form(_anomalon_packet())
    assert receipt.is_authorized() is False
    assert receipt.is_anomalon() is True
    assert receipt.is_refused() is False
    assert receipt.terminal_outcome.kind == TerminalKind.CLOSED_RESIDUAL
    assert receipt.terminal_outcome.phi1_distance == Rational(2, 1)
    assert receipt.terminal_outcome.dual_witness is not None


def test_master_normal_form_refusal_empty_sieve():
    """Case 3: Empty candidate repair sieve halts at R^sharp into F_term."""
    receipt = execute_master_normal_form(_empty_sieve_packet())
    assert receipt.is_authorized() is False
    assert receipt.is_anomalon() is False
    assert receipt.is_refused() is True
    assert receipt.terminal_outcome.kind == TerminalKind.REFUSED
    assert "empty" in (receipt.terminal_outcome.refusal_reason or "").lower()


def test_master_normal_form_refusal_nonclosed_defect():
    """Case 4: Nonclosed higher coboundary defect (Gamma_2 > 0) lands in F_term."""
    receipt = execute_master_normal_form(_nonclosed_packet())
    assert receipt.is_authorized() is False
    assert receipt.is_refused() is True
    assert receipt.terminal_outcome.kind == TerminalKind.REFUSED
    assert receipt.terminal_outcome.gamma2_distance > Rational(0, 1)


# ---------------------------------------------------------------------------
# 4. Strict Non-Promotion Authority Firewall & Countermodels (GTLA-02, FDA-04)
# ---------------------------------------------------------------------------


def test_non_promotion_firewall_zero_defect_unlicensed():
    """GTLA-02: Zero residual without external sovereign license routes to F_term, NOT T_auth."""
    d0 = Matrix([[1], [-1]])
    d1 = Matrix([[1, 1]])
    p = ProblemInstance(
        problem_id="test_unlicensed_zero",
        raw_data="zero_defect_unlicensed",
        candidate_sieve=("cand1",),
        coarse_profile=(0, 1),
        fine_profile=(0, 1),
        projection_map={0: 0, 1: 1},
        local_sections={"U0": (Rational(0, 1),)},
        overlaps={("U0", "U0"): True},
        d0=d0,
        d1=d1,
        defect_cochain=Matrix([[1], [-1]]),  # Phi_1 = 0
        fda_license_granted=False,  # NO LICENSE!
    )
    receipt = execute_master_normal_form(p)
    assert receipt.is_authorized() is False
    assert receipt.is_refused() is True
    assert receipt.terminal_outcome.kind == TerminalKind.REFUSED
    assert "non-promotion" in (receipt.terminal_outcome.refusal_reason or "").lower()

    # Verify firewall audit
    fw_report = evaluate_authority_firewall(receipt)
    assert fw_report["firewall_intact"] is True
    assert fw_report["disjoint_partition_holds"] is True
    assert fw_report["authority_effect"] == "None"


def test_untrusted_verifier_countermodel():
    """FDA-04 Countermodel 1: Verifier reports valid, but firewall prevents unauthorized action."""
    report = untrusted_verifier_countermodel()
    assert report["verifier_claimed_valid"] is True
    assert report["is_authorized"] is False
    assert report["is_refused"] is True
    assert report["firewall_blocked_unauthorized"] is True


def test_observation_collision_countermodel():
    """FDA-04 Countermodel 2: Observation profiles coincide while authority standing is separated."""
    report = observation_collision_countermodel()
    assert report["observation_identical"] is True
    assert report["s1_authorized"] is True
    assert report["s2_authorized"] is False
    assert report["authority_separated"] is True


# ---------------------------------------------------------------------------
# 5. End-to-End Reproducible Example Test
# ---------------------------------------------------------------------------


def test_reproduce_master_normal_form_example():
    """End-to-end trace correctly classifies all three canonical cases under AuthorityEffect: None."""
    res = reproduce_master_normal_form_example()
    assert res["case_1_auth"]["is_authorized"] is True
    assert res["case_1_auth"]["kind"] == "T_auth"
    assert res["case_2_anomalon"]["is_anomalon"] is True
    assert res["case_2_anomalon"]["kind"] == "T_res"
    assert res["case_3_refusal"]["is_refused"] is True
    assert res["case_3_refusal"]["kind"] == "F_term"
    assert res["partition_disjoint"] is True
    assert res["authority_effect"] == "None"


# ---------------------------------------------------------------------------
# 6. Additional Boundary & Error Branch Tests for Full Coverage
# ---------------------------------------------------------------------------


def test_validation_and_presentation_error_branches():
    """Test malformed rational strings, carrier size, diff shape, and negative values."""
    with pytest.raises(TypeError, match="could not be converted"):
        _validate_exact_rational("invalid_rat", "bad_str")

    with pytest.raises(TypeError, match="must be an exact rational"):
        _validate_exact_rational(object(), "bad_obj")

    with pytest.raises(ValueError, match="Carrier size must be at least 1"):
        FinitePresentation(name="P0", carrier_size=0, diff_matrix=())

    with pytest.raises(ValueError, match="Diff matrix rows"):
        FinitePresentation(name="P1", carrier_size=2, diff_matrix=((Rational(0),),))

    with pytest.raises(ValueError, match="row length must match"):
        FinitePresentation(name="P2", carrier_size=2, diff_matrix=((Rational(0),), (Rational(0),)))

    with pytest.raises(ValueError, match="must be non-negative"):
        FinitePresentation(name="P_neg", carrier_size=1, diff_matrix=((Rational(-1),),))


def test_comparison_span_and_trace_error_branches():
    """Test ComparisonSpan dimension mismatches, negative costs, and trace helpers."""
    p1 = FinitePresentation(name="P1", carrier_size=1, diff_matrix=((Rational(0),),))
    p2 = FinitePresentation(name="P2", carrier_size=1, diff_matrix=((Rational(0),),))
    p3 = FinitePresentation(name="P3", carrier_size=1, diff_matrix=((Rational(0),),))

    with pytest.raises(ValueError, match="length must match mid_size"):
        ComparisonSpan(p1=p1, p2=p2, mid_size=2, left_map=(0,), right_map=(0, 0))

    with pytest.raises(ValueError, match="Extensional cost must be non-negative"):
        ComparisonSpan(
            p1=p1,
            p2=p2,
            mid_size=1,
            left_map=(0,),
            right_map=(0,),
            ext_cost=Rational(-1),
        )

    s1 = ComparisonSpan(
        p1=p1, p2=p2, mid_size=1, left_map=(0,), right_map=(0,), ext_cost=Rational(0)
    )
    s3 = ComparisonSpan(
        p1=p3, p2=p3, mid_size=1, left_map=(0,), right_map=(0,), ext_cost=Rational(0)
    )
    with pytest.raises(ValueError, match="target/source mismatch"):
        compose_spans(s1, s3)

    # Trace helpers
    id_tr = make_id_trace(p1)
    assert id_tr.steps == 0
    assert id_tr.work_cost == Rational(0)
    assert erase_trace(id_tr) == id_tr.span

    with pytest.raises(ValueError, match="Work cost must be non-negative"):
        Trace(steps=1, work_cost=Rational(-1), span=s1)


def test_finite_groupoid_validation_branches():
    """Test groupoid validation failures on missing ID, composition, or inverse."""
    g_bad_id = FiniteGroupoid(
        objects=["A"],
        morphisms={"A": {"A": ["idA"]}},
        id_map={},  # missing
        comp_table={("idA", "idA"): "idA"},
        inv_map={"idA": "idA"},
    )
    assert g_bad_id.validate() is False

    g_bad_comp = FiniteGroupoid(
        objects=["A"],
        morphisms={"A": {"A": ["idA"]}},
        id_map={"A": "idA"},
        comp_table={("idA", "idA"): ""},  # empty
        inv_map={"idA": "idA"},
    )
    assert g_bad_comp.validate() is False

    g_bad_inv = FiniteGroupoid(
        objects=["A"],
        morphisms={"A": {"A": ["idA"]}},
        id_map={"A": "idA"},
        comp_table={("idA", "idA"): "idA"},
        inv_map={"idA": ""},  # empty
    )
    assert g_bad_inv.validate() is False


def test_terminal_outcome_post_init_invariants():
    """Test invalid parameter combinations and semantic invariants in TerminalOutcome (B7)."""
    valid_token = AuthorityToken(
        token_id="tok_1",
        issuer="TEST_ISSUER",
        subject="p1",
        scope="STANDARD",
        is_valid=True,
        signature_hash="sha256:abc",
    )

    # AUTHORIZED without valid AuthorityToken must fail
    with pytest.raises(ValueError, match="valid AuthorityToken"):
        TerminalOutcome(
            kind=TerminalKind.AUTHORIZED,
            payload_id="p1",
            phi1_distance=Rational(0),
            gamma2_distance=Rational(0),
            authority_token=None,
        )

    # AUTHORIZED with non-zero Phi_1 must fail
    with pytest.raises(ValueError, match="phi1=0 and gamma2=0"):
        TerminalOutcome(
            kind=TerminalKind.AUTHORIZED,
            payload_id="p1",
            phi1_distance=Rational(1),
            gamma2_distance=Rational(0),
            authority_token=valid_token,
        )

    # CLOSED_RESIDUAL with phi1 = 0 must fail
    with pytest.raises(ValueError, match="phi1 > 0"):
        TerminalOutcome(
            kind=TerminalKind.CLOSED_RESIDUAL,
            payload_id="p2",
            phi1_distance=Rational(0),
            gamma2_distance=Rational(0),
            dual_witness=(Rational(1),),
        )

    # CLOSED_RESIDUAL without dual witness must fail
    with pytest.raises(ValueError, match="verified dual witness"):
        TerminalOutcome(
            kind=TerminalKind.CLOSED_RESIDUAL,
            payload_id="p2",
            phi1_distance=Rational(1),
            gamma2_distance=Rational(0),
            dual_witness=None,
        )

    # REFUSED without refusal reason must fail
    with pytest.raises(ValueError, match="refusal reason"):
        TerminalOutcome(
            kind=TerminalKind.REFUSED,
            payload_id="p3",
            refusal_reason=None,
        )


def test_functors_edge_cases():
    """Test functor rho, d, foc, and tau edge cases and refusals."""
    d0 = Matrix([[1], [-1]])
    d1 = Matrix([[1, 1]])

    prob = ProblemInstance(
        problem_id="p_edge",
        raw_data="data",
        candidate_sieve=("c1",),
        coarse_profile=(0, 1),
        fine_profile=(0, 1),
        projection_map={0: 0, 1: 0},  # 1 -> 0 != 1: inconsistent!
        local_sections={"U1": (Rational(1),), "U2": (Rational(2),)},
        overlaps={("U1", "U2"): False},  # overlap disagreement
        d0=d0,
        d1=d1,
        defect_cochain=Matrix([[1], [-1]]),
        fda_license_granted=True,
    )

    r_ref = RSharpOutput(is_refused=True, refusal_reason="test")
    with pytest.raises(ValueError, match="Cannot apply rho"):
        functor_rho_sharp(prob, r_ref)

    r_ok = functor_r_sharp(prob)
    rho_out = functor_rho_sharp(prob, r_ok)
    assert rho_out.refinement_consistent is False

    d_out = functor_d_sharp(prob, rho_out)
    assert d_out.gluing_succeeded is False

    with pytest.raises(ValueError, match="distances are uncomputed"):
        functor_foc_sharp(prob, d_out)

    term_out = functor_tau_sharp(prob, r_ok, d_out, None)
    assert term_out.is_refused is True
    assert term_out.phi1_distance is None
    assert term_out.gamma2_distance is None


def test_faithful_groupoid_embedding_distinguishes_morphisms():
    """CD-12 / B2: Verify that Z_2 morphisms e and g have distinct extensional spans (E(e) != E(g))."""
    z2 = make_z2_groupoid()
    emb = FaithfulGroupoidEmbedding(z2)
    pres = emb.embed_object("*")
    assert pres.name == "Pres_*"
    assert pres.carrier_size == 2

    s_e = emb.embed_morphism("e")
    s_g = emb.embed_morphism("g")

    # E(e) != E(g): non-trivial automorphism is not collapsed!
    assert not extensional_equal(s_e, s_g)
    assert s_e.right_map == (0, 1)
    assert s_g.right_map == (1, 0)

    # Faithful injectivity check on hom-sets
    assert emb.check_faithfulness() is True

    # Pullback composition: E(g) * E(g) == E(e)
    s_gg = compose_spans(s_g, s_g)
    assert extensional_equal(s_gg, s_e)


def test_descent_overlap_disagreement_refuses_gluing():
    """Consistent refinement still refuses D^sharp when a declared overlap disagrees."""
    problem = ProblemInstance(
        problem_id="overlap_disagree",
        raw_data="data",
        candidate_sieve=("cand1",),
        coarse_profile=(0, 1),
        fine_profile=(0, 1),
        projection_map={0: 0, 1: 1},
        local_sections={"U1": (Rational(0, 1),), "U2": (Rational(1, 1),)},
        overlaps={("U1", "U2"): False},
        d0=Matrix([[1], [-1]]),
        d1=Matrix([[1, 1]]),
        defect_cochain=Matrix([[1], [-1]]),
        fda_license_granted=True,
    )
    r_out = functor_r_sharp(problem)
    rho_out = functor_rho_sharp(problem, r_out)
    assert rho_out.refinement_consistent is True
    d_out = functor_d_sharp(problem, rho_out)
    assert d_out.gluing_succeeded is False
    assert d_out.descent_cocycle_zero is False
    receipt = execute_master_normal_form(problem)
    assert receipt.is_authorized() is False
    assert receipt.is_refused() is True
    assert "Descent gluing failure" in (receipt.terminal_outcome.refusal_reason or "")


def test_dual_witness_validation_rejects_invalid_counterexamples():
    """
    B3: Test that validate_dual_witness strictly rejects invalid fallback witnesses:
    1. d0 = 0_{2x1}, defect = (0, 1)^T, candidate y = (1, 0)^T (fails pairing <y, delta> = 0 != 1).
    2. d0 = 0_{2x1}, defect = (1, 1)^T, candidate y = (2, 0)^T (violates norm ||y||_infty = 2 > 1).
    """
    d0 = Matrix([[0], [0]])

    # Counterexample 1: does not separate the class (inner product is 0)
    defect_1 = Matrix([[0], [1]])
    phi1_1 = Rational(1, 1)
    invalid_candidate_1 = (Rational(1, 1), Rational(0, 1))
    assert validate_dual_witness(d0, defect_1, invalid_candidate_1, phi1_1) is False

    # True witness for defect_1 is (0, 1)
    valid_witness_1 = (Rational(0, 1), Rational(1, 1))
    assert validate_dual_witness(d0, defect_1, valid_witness_1, phi1_1) is True

    # Counterexample 2: violates dual feasibility bound ||y||_infty <= 1
    defect_2 = Matrix([[1], [1]])
    phi1_2 = Rational(2, 1)
    invalid_candidate_2 = (Rational(2, 1), Rational(0, 1))
    assert validate_dual_witness(d0, defect_2, invalid_candidate_2, phi1_2) is False

    # True witness for defect_2 is (1, 1)
    valid_witness_2 = (Rational(1, 1), Rational(1, 1))
    assert validate_dual_witness(d0, defect_2, valid_witness_2, phi1_2) is True


def test_foc_sharp_produces_verified_dual_witness():
    """B3: FOC^sharp computes exact rational dual witness and verifies all 3 conditions."""
    inner_nonzero = _anomalon_packet()
    glued = DSharpOutput(
        gluing_succeeded=True,
        descent_cocycle_zero=True,
        global_section=(Rational(0, 1),),
    )
    foc_out = functor_foc_sharp(inner_nonzero, glued)
    assert foc_out.is_coherent_residual is True
    assert foc_out.phi1_distance == Rational(2, 1)
    assert foc_out.dual_witness is not None

    # Mechanically verify the returned witness
    is_valid = validate_dual_witness(
        d0=inner_nonzero.d0,
        defect=inner_nonzero.defect_cochain,
        dual_witness=foc_out.dual_witness,
        phi1=foc_out.phi1_distance,
    )
    assert is_valid is True


def test_tau_unclassified_foc_flags_refuses():
    """Tau^sharp refuses when FOC^sharp reports none of exact, residual, or nonclosed."""
    problem = _authorized_packet()
    r_out = RSharpOutput(is_refused=False, active_complex="ActiveComplex_test_auth")
    d_out = DSharpOutput(
        gluing_succeeded=True,
        descent_cocycle_zero=True,
        global_section=(Rational(0, 1),),
    )
    foc_out = FocSharpOutput(
        phi1_distance=Rational(1, 1),
        gamma2_distance=Rational(0, 1),
        is_exact_repair=False,
        is_coherent_residual=False,
        is_nonclosed_defect=False,
    )
    term = functor_tau_sharp(problem, r_out, d_out, foc_out)
    assert term.kind == TerminalKind.REFUSED
    assert term.is_refused is True
    assert term.is_authorized is False
    assert term.is_anomalon is False
    assert term.payload_id == "invalid_stage_test_auth"
    assert term.refusal_reason == "Stage evidence does not match the supplied problem"
    assert term.phi1_distance is None


def test_engine_facade_matches_core_on_authorized_packet():
    """coda_gtla_engine re-exports execute the same authorized packet as coda_gtla_core."""
    problem = _authorized_packet()
    core_receipt = execute_master_normal_form(problem)
    engine_receipt = coda_gtla_engine.execute_master_normal_form(problem)
    assert engine_receipt.is_authorized() is True
    assert engine_receipt.terminal_outcome.kind == core_receipt.terminal_outcome.kind
    assert engine_receipt.terminal_outcome.phi1_distance == Rational(0, 1)
    assert coda_gtla_engine.functor_r_sharp is functor_r_sharp
    assert "execute_master_normal_form" in coda_gtla_engine.__all__


def test_descent_empty_local_sections_fails_gluing():
    """B6: Empty local sections cannot produce a valid global section and must fail gluing."""
    problem = ProblemInstance(
        problem_id="empty_sections",
        raw_data="data",
        candidate_sieve=("cand1",),
        coarse_profile=(0, 1),
        fine_profile=(0, 1),
        projection_map={0: 0, 1: 1},
        local_sections={},
        overlaps={},
        d0=Matrix([[1], [-1]]),
        d1=Matrix([[1, 1]]),
        defect_cochain=Matrix([[1], [-1]]),
        fda_license_granted=True,
    )
    r_out = functor_r_sharp(problem)
    rho_out = functor_rho_sharp(problem, r_out)
    assert rho_out.refinement_consistent is True
    d_out = functor_d_sharp(problem, rho_out)
    assert d_out.gluing_succeeded is False
    assert d_out.global_section is None


# ---------------------------------------------------------------------------
# 7. Regressions for Republication Review Findings (B4, B5, B6, B7, B8, M1, M2, M5)
# ---------------------------------------------------------------------------


def test_problem_instance_rejects_two_column_defect():
    """B4: Defect cochain with 2 columns must be rejected at construction time."""
    d0 = Matrix([[1], [-1]])
    d1 = Matrix([[1, 1]])
    two_col_defect = Matrix([[0, 7], [0, -7]])
    with pytest.raises(ValueError, match="must have exactly 1 column"):
        ProblemInstance(
            problem_id="two_col",
            raw_data="data",
            candidate_sieve=("cand1",),
            coarse_profile=(0, 1),
            fine_profile=(0, 1),
            projection_map={0: 0, 1: 1},
            local_sections={"U0": (Rational(0),)},
            overlaps={("U0", "U0"): True},
            d0=d0,
            d1=d1,
            defect_cochain=two_col_defect,
        )


def test_problem_instance_rejects_broken_chain_complex():
    """B4: ProblemInstance rejects non-complex where d1 * d0 != 0."""
    d0 = Matrix([[1], [1]])
    d1 = Matrix([[1, 1]])  # d1 * d0 = [[2]] != 0
    defect = Matrix([[1], [1]])
    with pytest.raises(ValueError, match="Cochain complex condition failed: d1 \\* d0 != 0"):
        ProblemInstance(
            problem_id="broken_complex",
            raw_data="data",
            candidate_sieve=("cand1",),
            coarse_profile=(0, 1),
            fine_profile=(0, 1),
            projection_map={0: 0, 1: 1},
            local_sections={"U0": (Rational(0),)},
            overlaps={("U0", "U0"): True},
            d0=d0,
            d1=d1,
            defect_cochain=defect,
        )


def test_problem_instance_rejects_floats_everywhere():
    """B5: Reject IEEE 754 floats in matrices and local sections."""
    d0_float = Matrix([[1.5], [-1.5]])
    d0_exact = Matrix([[Rational(3, 2)], [Rational(-3, 2)]])
    defect_exact = Matrix([[Rational(1)], [Rational(-1)]])

    # Float in d0
    with pytest.raises(TypeError, match="floats strictly forbidden"):
        ProblemInstance(
            problem_id="float_d0",
            raw_data="data",
            candidate_sieve=("cand1",),
            coarse_profile=(0, 1),
            fine_profile=(0, 1),
            projection_map={0: 0, 1: 1},
            local_sections={"U0": (Rational(0),)},
            overlaps={("U0", "U0"): True},
            d0=d0_float,
            d1=None,
            defect_cochain=defect_exact,
        )

    # Float in local section
    with pytest.raises(TypeError, match="floats strictly forbidden"):
        ProblemInstance(
            problem_id="float_sec",
            raw_data="data",
            candidate_sieve=("cand1",),
            coarse_profile=(0, 1),
            fine_profile=(0, 1),
            projection_map={0: 0, 1: 1},
            local_sections={"U0": (0.5,)},
            overlaps={("U0", "U0"): True},
            d0=d0_exact,
            d1=None,
            defect_cochain=defect_exact,
        )


def test_descent_restriction_domain_agreement_and_disagreement():
    """B6: Test presheaf descent detects section disagreement on overlaps."""
    d0 = Matrix([[1], [-1]])
    defect = Matrix([[0], [0]])

    # Problem with two sections that disagree on overlap point 1: U1 has value 0, U2 has value 1
    p_disagree = ProblemInstance(
        problem_id="presheaf_disagree",
        raw_data="data",
        candidate_sieve=("c1",),
        coarse_profile=(0, 1),
        fine_profile=(0, 1),
        projection_map={0: 0, 1: 1},
        local_sections={
            "U1": (Rational(0), Rational(0)),
            "U2": (Rational(1), Rational(2)),
        },
        cover={
            "U1": (0, 1),  # contains point 1
            "U2": (1, 2),  # contains point 1: value is 1 != 0!
        },
        overlaps={("U1", "U2"): True},
        d0=d0,
        d1=None,
        defect_cochain=defect,
        fda_license_granted=True,
    )
    r_out = functor_r_sharp(p_disagree)
    rho_out = functor_rho_sharp(p_disagree, r_out)
    d_out = functor_d_sharp(p_disagree, rho_out)
    assert d_out.gluing_succeeded is False
    assert d_out.descent_cocycle_zero is False


def test_authority_firewall_rejects_forged_receipt_with_invalid_semantics():
    """B7: Firewall and constructor refuse outcome claiming authorized but carrying invalid distances/tokens."""
    bad_token = AuthorityToken(
        token_id="fake_tok",
        issuer="MALICIOUS",
        subject="forged",
        scope="NONE",
        is_valid=False,
        signature_hash="invalid",
    )

    # 1. Negative distance is rejected at constructor
    with pytest.raises(ValueError, match="gamma2_distance must be non-negative"):
        TerminalOutcome(
            kind=TerminalKind.REFUSED,
            payload_id="bad_dist",
            gamma2_distance=Rational(-2, 1),
            refusal_reason="negative distance",
        )

    # 2. Forged outcome claiming authorization with phi1 > 0 is rejected at constructor
    with pytest.raises(ValueError, match="phi1=0 and gamma2=0"):
        TerminalOutcome(
            kind=TerminalKind.AUTHORIZED,
            payload_id="forged_auth",
            phi1_distance=Rational(9, 1),
            gamma2_distance=Rational(0, 1),
            authority_token=bad_token,
        )

    # 3. Unsound verifier attempt (phi1=0 but no valid authority token)
    p_unlicensed = ProblemInstance(
        problem_id="p_unlic",
        raw_data="data",
        candidate_sieve=("cand1",),
        coarse_profile=(0, 1),
        fine_profile=(0, 1),
        projection_map={0: 0, 1: 1},
        local_sections={"U0": (Rational(0),)},
        overlaps={("U0", "U0"): True},
        d0=Matrix([[1], [-1]]),
        d1=Matrix([[1, 1]]),
        defect_cochain=Matrix([[1], [-1]]),
        fda_license_granted=False,
    )
    receipt = execute_master_normal_form(p_unlicensed)
    fw_report = evaluate_authority_firewall(receipt)
    assert fw_report["is_authorized"] is False
    assert fw_report["firewall_intact"] is True


def test_comparison_span_surjectivity_and_bounds_validation():
    """M1: ComparisonSpan checks out-of-range indices, non-surjective maps, and mid_size >= 1."""
    p1 = FinitePresentation("P1", 2, ((Rational(0), Rational(0)), (Rational(0), Rational(0))))
    p2 = FinitePresentation("P2", 2, ((Rational(0), Rational(0)), (Rational(0), Rational(0))))

    # Out of bounds index
    with pytest.raises(ValueError, match="out of range"):
        ComparisonSpan(p1=p1, p2=p2, mid_size=2, left_map=(0, 99), right_map=(0, 1))

    # Non-surjective map: misses element 1 of carrier size 2
    with pytest.raises(ValueError, match="must be surjective"):
        ComparisonSpan(p1=p1, p2=p2, mid_size=2, left_map=(0, 0), right_map=(0, 1))

    # mid_size < 1
    with pytest.raises(ValueError, match="intermediate carrier size must be >= 1"):
        ComparisonSpan(p1=p1, p2=p2, mid_size=0, left_map=(), right_map=())


def test_quotient_representative_invariance():
    """M5: Quotient distance Phi_1([delta + d0 f]) == Phi_1([delta])."""
    d0 = Matrix([[1], [-1]])
    delta = Matrix([[2], [0]])  # not in im(d0)
    solver = LinearRepairProblem(d0)

    cert1 = solver.quotient_l1_distance(delta)
    phi1_original = cert1.distance

    # Shift by d0 * f where f = [[3]]
    f = Matrix([[3]])
    shifted_delta = delta + d0 * f
    cert2 = solver.quotient_l1_distance(shifted_delta)
    phi1_shifted = cert2.distance

    assert phi1_original == phi1_shifted


def test_pipeline_result_sha256_digest():
    """B8: PipelineResult produces a valid deterministic 64-character SHA-256 digest."""
    p = _authorized_packet()
    receipt = execute_master_normal_form(p)
    digest = receipt.sha256_digest()
    assert isinstance(digest, str)
    assert len(digest) == 64
    assert int(digest, 16) > 0


def test_two_rule_repair_loop():
    """GTLA-03: execute_two_rule_repair_loop applies Rule 1 on repair and Rule 2 on residual."""
    p_auth = _authorized_packet()
    res1 = execute_two_rule_repair_loop(p_auth)
    assert res1["rule_applied"] == "Rule 1: Same-Grain Repair"
    assert res1["phi1"] == Rational(0, 1)
    assert res1["ties_retained"] is None
    assert res1["extension_constructed"] is False

    p_anom = _anomalon_packet()
    res2 = execute_two_rule_repair_loop(p_anom)
    assert res2["rule_applied"] == "Positive residual: extension remains open"
    assert res2["phi1"] == Rational(2, 1)
    assert res2["ties_retained"] is None
    assert res2["extension_constructed"] is False
    assert len(res2["dual_witness"]) == 2
