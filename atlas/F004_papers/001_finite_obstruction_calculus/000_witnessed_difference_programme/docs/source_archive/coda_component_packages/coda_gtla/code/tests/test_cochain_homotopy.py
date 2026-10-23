# -*- coding: utf-8 -*-
r"""
test_cochain_homotopy.py: Exact cochain homotopy and gauge transformation invariance test suite for CODA-GTLA.

Governing Claims:
- GTLA-01 / MUR-01: Transport certificates \tau^\sharp compose associatively and are invariant under
  intermediate carrier gauge transformations.
- CD-12: Two-level cost accounting separates extensional certificate identity (\tau_1^\sharp \equiv \tau_2^\sharp)
  from intensional execution trace divergence (c_trace(T_1) != c_trace(T_2)).
- FOC-05 / A-02: Cochain coboundary shifts \delta_2 = \delta_1 + d_0 h preserve exact rational
  quotient distances \Phi_1([\delta_1]) = \Phi_1([\delta_2]) and dual witness pairing certificates.

AuthorityEffect: None.
"""

from __future__ import annotations

import pytest
from coda_gtla_core import (
    ComparisonSpan,
    FinitePresentation,
    ProblemInstance,
    Trace,
    apply_carrier_gauge_transformation,
    apply_cochain_homotopy,
    compose_spans,
    compute_transport_certificate,
    evaluate_span_homotopy_transport,
    execute_master_normal_form,
    extensional_equal,
    make_diag_span,
    verify_cochain_homotopy_invariance,
)
from sympy import Matrix, Rational


def _make_test_presentation(name: str, size: int) -> FinitePresentation:
    """Create a presentation with distinct non-zero off-diagonal distances."""
    diff = [
        [Rational(0, 1) if r == c else Rational(abs(r - c) + 1, 1) for c in range(size)]
        for r in range(size)
    ]
    return FinitePresentation(
        name=name,
        carrier_size=size,
        diff_matrix=tuple(tuple(row) for row in diff),
    )


# ---------------------------------------------------------------------------
# 1. Carrier Gauge Transformation Preserves Composite Span and Tau^Sharp
# ---------------------------------------------------------------------------


def test_carrier_gauge_transformation_preserves_composite_span_and_tau():
    r"""
    Evaluates whether an intermediate carrier gauge transformation g in S_{V_mid}
    leaves the composite span S_2^g * S_1^g extensionally identical to S_2 * S_1
    and yields byte-identical transport certificates \tau_1^\sharp \equiv \tau_2^\sharp.
    """
    p0 = _make_test_presentation("P0", size=2)
    p1 = _make_test_presentation("P1", size=3)
    p2 = _make_test_presentation("P2", size=2)

    # S1: P0 <- M1 -> P1 (mid_size=3, left surjective to 2, right surjective to 3)
    s1 = ComparisonSpan(
        p1=p0,
        p2=p1,
        mid_size=3,
        left_map=(0, 1, 0),
        right_map=(0, 1, 2),
        ext_cost=Rational(1, 2),
    )
    # S2: P1 <- M2 -> P2 (mid_size=3, left surjective to 3, right surjective to 2)
    s2 = ComparisonSpan(
        p1=p1,
        p2=p2,
        mid_size=3,
        left_map=(0, 1, 2),
        right_map=(1, 0, 1),
        ext_cost=Rational(3, 4),
    )

    # Gauge transformation: cyclic permutation on P1 (0->1, 1->2, 2->0)
    gauge_g = (1, 2, 0)
    s1_g, s2_g = apply_carrier_gauge_transformation(s1, s2, gauge_g)

    # Verify intermediate presentation name and validity
    assert s1_g.p2.name == "P1_gauge"
    assert s2_g.p1.name == "P1_gauge"
    assert s1_g.p2 == s2_g.p1

    # Compose original and gauge-transformed pairs
    s12 = compose_spans(s1, s2)
    s12_g = compose_spans(s1_g, s2_g)

    # Assert exact extensional equality
    assert extensional_equal(s12, s12_g) is True
    assert s12.relation() == s12_g.relation()
    assert s12.ext_cost == s12_g.ext_cost == Rational(5, 4)

    # Compute transport certificates
    tau1 = compute_transport_certificate(s12)
    tau2 = compute_transport_certificate(s12_g)

    assert tau1.extensional_hash == tau2.extensional_hash
    assert tau1.is_closed_loop == tau2.is_closed_loop
    assert tau1.monodromy_defect == tau2.monodromy_defect
    assert tau1.ext_cost == tau2.ext_cost


# ---------------------------------------------------------------------------
# 2. Cochain Homotopy Preserves Phi_1 and Dual Witness Certificates
# ---------------------------------------------------------------------------


def test_cochain_homotopy_preserves_phi1_and_dual_witness():
    r"""
    Evaluates whether two defect cochains differing by coboundary d_0 h
    induce identical exact rational quotient distances \Phi_1 and that
    verified dual witnesses pair identically with both representations.
    """
    d0 = Matrix(
        [
            [1, 0],
            [-1, 1],
            [0, -1],
        ]
    )
    # Base defect cochain
    delta_1 = Matrix(
        [
            [2],
            [1],
            [0],
        ]
    )
    # Homotopy 0-cochain
    h = Matrix(
        [
            [3],
            [-2],
        ]
    )

    delta_2 = apply_cochain_homotopy(delta_1, d0, h)
    # delta_2 = delta_1 + d0 * h = [2+3, 1-3-2, 0-(-2)]^T = [5, -4, 2]^T
    assert delta_2 == Matrix([[5], [-4], [2]])

    result = verify_cochain_homotopy_invariance(d0, delta_1, delta_2, h)
    assert result["is_exact_homotopy"] is True
    assert result["distances_equal"] is True
    assert result["invariance_holds"] is True
    assert result["witness1_certifies_defect2"] is True
    assert result["witness2_certifies_defect1"] is True
    assert Rational(result["phi1_defect1"]) == Rational(result["phi1_defect2"])


# ---------------------------------------------------------------------------
# 3. Adversarial Non-Homotopy Breaks Invariance
# ---------------------------------------------------------------------------


def test_adversarial_non_homotopy_breaks_invariance():
    """
    Confirms that when a cochain perturbation v does NOT belong to im(d_0),
    homotopy invariance is broken, resulting in divergent quotient distances
    or failed dual witness verification.
    """
    d0 = Matrix(
        [
            [1, 0],
            [-1, 1],
            [0, -1],
        ]
    )
    delta_1 = Matrix([[2], [1], [0]])
    # Non-coboundary perturbation orthogonal to im(d0)
    # Here sum of rows of d0 is [0, 0, 0], so (1, 1, 1)^T is in ker(d0^T)
    v_non_coboundary = Matrix([[2], [2], [2]])
    delta_broken = delta_1 + v_non_coboundary

    result = verify_cochain_homotopy_invariance(d0, delta_1, delta_broken)
    assert result["is_exact_homotopy"] is False
    assert result["distances_equal"] is False
    assert result["invariance_holds"] is False


# ---------------------------------------------------------------------------
# 4. Homotopic Span Sequences: Identical Tau^Sharp with Distinct Trace Work Costs
# ---------------------------------------------------------------------------


def test_homotopic_span_sequences_identical_tau_with_distinct_work_costs():
    r"""
    CD-12 Two-Level Cost Accounting:
    Two distinct span sequences (2-step direct vs 2-step with intermediate gauge permutation)
    evaluate to identical extensional transport certificates \tau_1^\sharp \equiv \tau_2^\sharp,
    while their intensional execution trace costs diverge (c_trace(T_1) != c_trace(T_2)).
    """
    p0 = _make_test_presentation("P_start", size=2)
    p1 = _make_test_presentation("P_mid", size=2)
    p2 = _make_test_presentation("P_end", size=2)

    s1 = ComparisonSpan(
        p1=p0,
        p2=p1,
        mid_size=2,
        left_map=(0, 1),
        right_map=(0, 1),
        ext_cost=Rational(1, 1),
    )
    s2 = ComparisonSpan(
        p1=p1,
        p2=p2,
        mid_size=2,
        left_map=(0, 1),
        right_map=(1, 0),
        ext_cost=Rational(1, 1),
    )

    # Apply transposition gauge on intermediate presentation P_mid
    gauge_perm = (1, 0)
    s1_g, s2_g = apply_carrier_gauge_transformation(s1, s2, gauge_perm)

    # Assign distinct physical work costs to each execution trace
    t1_1 = Trace(steps=1, work_cost=Rational(2, 1), span=s1)
    t1_2 = Trace(steps=1, work_cost=Rational(3, 1), span=s2)

    t2_1 = Trace(steps=2, work_cost=Rational(7, 2), span=s1_g)
    t2_2 = Trace(steps=2, work_cost=Rational(9, 2), span=s2_g)

    report = evaluate_span_homotopy_transport(
        seq1=(s1, s2),
        seq2=(s1_g, s2_g),
        traces1=(t1_1, t1_2),
        traces2=(t2_1, t2_2),
    )

    # Extensional identity
    assert report["spans_extensionally_equal"] is True
    assert report["extensional_hashes_equal"] is True
    assert report["certificates_identical"] is True
    assert report["ext_cost_1"] == report["ext_cost_2"] == "2"

    # Intensional trace cost divergence
    assert report["two_level_cost_divergence"] is True
    assert report["work_cost_1"] == "5"  # 2 + 3
    assert report["work_cost_2"] == "8"  # 7/2 + 9/2 = 16/2 = 8


# ---------------------------------------------------------------------------
# 5. Closed Loop Monodromy Invariance under Intermediate Gauge Transformations
# ---------------------------------------------------------------------------


def test_closed_loop_monodromy_gauge_invariance():
    r"""
    Evaluates a closed loop P_0 -> P_1 -> P_2 -> P_0 with non-trivial monodromy.
    Verifies that applying gauge transformations g_1 \in S_{V1} and g_2 \in S_{V2}
    to intermediate carriers does NOT change the boundary monodromy certificate \tau^\sharp.
    """
    p0 = _make_test_presentation("P0", size=2)
    p1 = _make_test_presentation("P1", size=3)
    p2 = _make_test_presentation("P2", size=3)

    # Leg 1: P0 -> P1
    s1 = ComparisonSpan(p1=p0, p2=p1, mid_size=3, left_map=(0, 1, 0), right_map=(0, 1, 2))
    # Leg 2: P1 -> P2
    s2 = ComparisonSpan(p1=p1, p2=p2, mid_size=3, left_map=(0, 1, 2), right_map=(1, 0, 2))
    # Leg 3: P2 -> P0 (induces transposition on P0)
    s3 = ComparisonSpan(p1=p2, p2=p0, mid_size=3, left_map=(0, 1, 2), right_map=(1, 0, 1))

    # Original closed loop: s3 * s2 * s1
    loop_orig = compose_spans(compose_spans(s1, s2), s3)
    cert_orig = compute_transport_certificate(loop_orig)
    assert cert_orig.is_closed_loop is True
    assert cert_orig.is_trivial_monodromy is False

    # Apply gauge g1 on P1 between s1 and s2
    g1 = (2, 0, 1)
    s1_g1, s2_g1 = apply_carrier_gauge_transformation(s1, s2, g1)

    # Apply gauge g2 on P2 between s2_g1 and s3
    g2 = (1, 2, 0)
    s2_g1g2, s3_g2 = apply_carrier_gauge_transformation(s2_g1, s3, g2)

    # Gauge-transformed loop: s3_g2 * s2_g1g2 * s1_g1
    loop_gauged = compose_spans(compose_spans(s1_g1, s2_g1g2), s3_g2)
    cert_gauged = compute_transport_certificate(loop_gauged)

    assert extensional_equal(loop_orig, loop_gauged) is True
    assert cert_orig.extensional_hash == cert_gauged.extensional_hash
    assert cert_orig.monodromy_permutation == cert_gauged.monodromy_permutation
    assert cert_orig.monodromy_defect == cert_gauged.monodromy_defect


# ---------------------------------------------------------------------------
# 6. Pipeline Normal Form Invariance under Cochain Homotopy
# ---------------------------------------------------------------------------


def test_pipeline_normal_form_invariance_under_cochain_homotopy():
    r"""
    Evaluates the 5-stage Master Normal Form pipeline under cochain coboundary homotopy.
    Verifies that \Pi^\sharp returns identical terminal kinds and quotient distances.
    """
    d0 = Matrix([[1], [-1], [0]])
    d1 = Matrix([[0, 0, 0]])  # d1 * d0 = [0]

    delta_base = Matrix([[0], [0], [2]])  # d1 * delta_base = 0 => Gamma_2 = 0, Phi_1 = 2
    h = Matrix([[1]])
    delta_hom = apply_cochain_homotopy(delta_base, d0, h)  # [1, -1, 2]^T, Gamma_2 = 0, Phi_1 = 2

    p_base = ProblemInstance(
        problem_id="prob_base",
        raw_data="base_payload",
        candidate_sieve=("cand1",),
        coarse_profile=(0, 1),
        fine_profile=(0, 1),
        projection_map={0: 0, 1: 1},
        local_sections={"U1": (Rational(1),)},
        overlaps={("U1", "U1"): True},
        d0=d0,
        d1=d1,
        defect_cochain=delta_base,
        fda_license_granted=False,
    )

    p_hom = ProblemInstance(
        problem_id="prob_hom",
        raw_data="hom_payload",
        candidate_sieve=("cand1",),
        coarse_profile=(0, 1),
        fine_profile=(0, 1),
        projection_map={0: 0, 1: 1},
        local_sections={"U1": (Rational(1),)},
        overlaps={("U1", "U1"): True},
        d0=d0,
        d1=d1,
        defect_cochain=delta_hom,
        fda_license_granted=False,
    )

    rec_base = execute_master_normal_form(p_base)
    rec_hom = execute_master_normal_form(p_hom)

    assert rec_base.terminal_outcome.kind == rec_hom.terminal_outcome.kind
    assert rec_base.is_anomalon() is True
    assert rec_hom.is_anomalon() is True
    assert (
        rec_base.terminal_outcome.phi1_distance
        == rec_hom.terminal_outcome.phi1_distance
        == Rational(2, 1)
    )
    assert (
        rec_base.terminal_outcome.gamma2_distance
        == rec_hom.terminal_outcome.gamma2_distance
        == Rational(0, 1)
    )


# ---------------------------------------------------------------------------
# 7. Error Handling & Validation Fail-Closed Guards
# ---------------------------------------------------------------------------


def test_gauge_transformation_validation_branches():
    """Fail-closed validation on invalid gauge permutations and non-composable spans."""
    p0 = _make_test_presentation("P0", size=2)
    p1 = _make_test_presentation("P1", size=3)
    p2 = _make_test_presentation("P2", size=2)

    s1 = make_diag_span(p0)
    s2 = make_diag_span(p2)

    # 1. Non-composable spans (p0 != p2)
    with pytest.raises(ValueError, match="Spans must be composable"):
        apply_carrier_gauge_transformation(s1, s2, (0, 1))

    # 2. Permutation length mismatch
    s1_comp = ComparisonSpan(p1=p0, p2=p1, mid_size=3, left_map=(0, 1, 0), right_map=(0, 1, 2))
    s2_comp = ComparisonSpan(p1=p1, p2=p2, mid_size=3, left_map=(0, 1, 2), right_map=(0, 1, 0))
    with pytest.raises(ValueError, match="does not match intermediate carrier size"):
        apply_carrier_gauge_transformation(s1_comp, s2_comp, (0, 1))

    # 3. Non-bijective permutation (duplicate index)
    with pytest.raises(ValueError, match="must be a bijective permutation"):
        apply_carrier_gauge_transformation(s1_comp, s2_comp, (0, 1, 1))

    # 4. Cochain homotopy dimension mismatch
    d0 = Matrix([[1], [1]])
    defect = Matrix([[1], [0]])
    bad_h = Matrix([[1], [1]])  # d0 is 2x1, h must be 1x1, not 2x1
    with pytest.raises(ValueError, match="d0 cols 1 must match h rows 2"):
        apply_cochain_homotopy(defect, d0, bad_h)

    # 5. Empty sequence in evaluate_span_homotopy_transport
    with pytest.raises(ValueError, match="Span sequences must be non-empty"):
        evaluate_span_homotopy_transport((), ())
