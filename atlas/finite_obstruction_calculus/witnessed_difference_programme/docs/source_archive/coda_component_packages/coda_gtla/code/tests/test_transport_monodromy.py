# -*- coding: utf-8 -*-
r"""
test_transport_monodromy.py: Adversarial fiber-perturbation test suite for CODA-GTLA.

Governing Claims:
- GTLA-01 / MUR-01: Transport certificates \tau^\sharp compose associatively across spans.
- GTLA-02: Terminal partition T_auth \sqcup T_res \sqcup F_term and strict non-promotion firewall.
- CD-12: Faithful groupoid representation with two-level cost accounting.
- Adversarial Fiber Perturbation Invariant:
  Small mutations in carrier presentation size:
  1. Pure spectator mutations (|X| -> |X| + 1, unentangled) preserve base carrier flatness (trivial monodromy).
  2. Entangled fiber mutations (|X| -> |X| + 1, braided through ancilla) induce non-trivial monodromy (\tau^\sharp \neq id).
  3. Mismatched dimensional transitions along open legs fail closed (ValueError / D^\sharp descent failure).
  4. Pipeline terminalization strictly enforces the non-promotion firewall under perturbed states.

AuthorityEffect: None.
"""

from __future__ import annotations

import pytest
from coda_gtla_core import (
    ComparisonSpan,
    FaithfulGroupoidEmbedding,
    FinitePresentation,
    ProblemInstance,
    build_monodromy_transport_loop,
    compose_spans,
    compose_traces,
    compute_transport_certificate,
    evaluate_authority_firewall,
    execute_master_normal_form,
    make_diag_span,
    make_z2_groupoid,
    make_z3_groupoid,
    perturb_presentation_carrier_size,
    validate_dual_witness,
)
from sympy import Matrix, Rational


def _make_metric_presentation(
    name: str, size: int, default_dist: Rational = Rational(1, 1)
) -> FinitePresentation:
    """Helper to create a finite presentation with symmetric, irreflexive difference matrix."""
    diff = [[Rational(0, 1) if r == c else default_dist for c in range(size)] for r in range(size)]
    return FinitePresentation(
        name=name,
        carrier_size=size,
        diff_matrix=tuple(tuple(row) for row in diff),
    )


# ---------------------------------------------------------------------------
# 1. Unperturbed Flat Loop: Trivial Monodromy & Two-Level Cost Accounting
# ---------------------------------------------------------------------------


def test_transport_certificate_unperturbed_flat_loop_trivial_monodromy():
    """
    Regime A: Baseline closed loop with canceling inverse pairs on unperturbed carrier.
    Verifies that tau^sharp has trivial monodromy (Mon = id, defect = 0, c_mor = 0)
    while intensional work cost is strictly positive (c_trace > 0) under CD-12.
    """
    pres = _make_metric_presentation("P_base", size=3, default_dist=Rational(2, 1))
    s_comp, tr_comp = build_monodromy_transport_loop(pres, mode="unperturbed")

    cert = compute_transport_certificate(s_comp, trace=tr_comp)

    assert cert.is_closed_loop is True
    assert cert.is_trivial_monodromy is True
    assert cert.monodromy_permutation == (0, 1, 2)
    assert cert.monodromy_defect == Rational(0, 1)
    assert cert.ext_cost == Rational(0, 1)
    assert cert.work_cost == Rational(3, 1)  # Two steps * (3/2) = 3
    assert len(cert.sha256_hash) == 64


# ---------------------------------------------------------------------------
# 2. Spectator Fiber Mutation: Preserves Trivial Monodromy on Base Carrier
# ---------------------------------------------------------------------------


def test_spectator_fiber_mutation_preserves_base_monodromy():
    """
    Regime B: Carrier presentation size mutated |X| -> |X| + 1 by adding an isolated spectator point.
    Transport acts trivially on both base and spectator elements.
    Verifies that spectator size extensions do NOT induce non-trivial monodromy.
    """
    pres = _make_metric_presentation("P_base", size=3, default_dist=Rational(3, 1))
    s_comp, tr_comp = build_monodromy_transport_loop(pres, mode="spectator_mutation")

    cert = compute_transport_certificate(s_comp, trace=tr_comp)

    assert cert.is_closed_loop is True
    assert cert.is_trivial_monodromy is True
    assert cert.span.p1.carrier_size == 4
    assert cert.monodromy_permutation == (0, 1, 2, 3)
    assert cert.monodromy_defect == Rational(0, 1)

    # Restriction of monodromy to base carrier points {0, 1, 2} is identity
    base_restriction = cert.monodromy_permutation[:3]
    assert base_restriction == (0, 1, 2)


# ---------------------------------------------------------------------------
# 3. Entangled Fiber Mutation: Induces Non-Trivial Permutation Monodromy
# ---------------------------------------------------------------------------


def test_entangled_fiber_mutation_induces_nontrivial_monodromy():
    """
    Regime C: Carrier presentation size mutated |X| -> |X| + 1 with ancilla point n.
    Spans along the cycle route base elements through the ancilla: (0 n) o (1 n) o (0 n) = (0 1)(n).
    Verifies that the composite transport certificate tau^sharp accumulates non-trivial monodromy:
    Mon(tau^sharp) = (0 1), with strictly positive metric defect Delta_mon > 0.
    """
    # Base presentation with carrier size 2 and explicit metric distance delta(0, 1) = 5
    diff = ((Rational(0, 1), Rational(5, 1)), (Rational(5, 1), Rational(0, 1)))
    pres = FinitePresentation(name="P_base_metric", carrier_size=2, diff_matrix=diff)

    s_comp, tr_comp = build_monodromy_transport_loop(pres, mode="entangled_mutation")
    cert = compute_transport_certificate(s_comp, trace=tr_comp)

    assert cert.is_closed_loop is True
    assert cert.is_trivial_monodromy is False

    # The ancilla is at index 2; base elements 0 and 1 are swapped!
    assert cert.monodromy_permutation == (1, 0, 2)

    # The metric defect reflects the swapped base elements: delta(0, 1) + delta(1, 0) = 5 + 5 = 10
    assert cert.monodromy_defect > Rational(0, 1)
    assert cert.monodromy_defect == Rational(10, 1)
    assert cert.work_cost == Rational(3, 1)


# ---------------------------------------------------------------------------
# 4. Incompatible Carrier Size Mutation: Fail-Closed Dimensional Guards
# ---------------------------------------------------------------------------


def test_incompatible_carrier_size_mismatch_fails_closed():
    """
    Regime D: Fail-closed boundary testing on carrier presentation size mutations.
    1. Composing spans across mismatched carrier size targets strictly raises ValueError.
    2. Constructing comparison spans with out-of-range projections raises ValueError.
    3. Mutating presentation size below 1 raises ValueError.
    """
    p2 = _make_metric_presentation("P_dim2", size=2)
    p3 = _make_metric_presentation("P_dim3", size=3)

    s_2to2 = make_diag_span(p2)
    s_3to3 = make_diag_span(p3)

    # 1. Target/source mismatch in span composition
    with pytest.raises(ValueError, match="Span composition target/source mismatch"):
        compose_spans(s_2to2, s_3to3)

    # 2. Out of range projection map
    with pytest.raises(ValueError, match="out of range for carrier size"):
        ComparisonSpan(
            p1=p2,
            p2=p2,
            mid_size=2,
            left_map=(0, 2),  # index 2 is invalid for carrier size 2
            right_map=(0, 1),
        )

    # 3. Non-surjective projection map
    with pytest.raises(ValueError, match="must be surjective"):
        ComparisonSpan(
            p1=p2,
            p2=p2,
            mid_size=2,
            left_map=(0, 0),  # covers only {0}, misses 1
            right_map=(0, 1),
        )

    # 4. Negative size reduction below 1
    with pytest.raises(ValueError, match="Perturbed carrier size must be >= 1"):
        perturb_presentation_carrier_size(p2, delta_size=-2)


# ---------------------------------------------------------------------------
# 5. Multi-Valued Fiber Branching: Non-Bijective Monodromy Defect
# ---------------------------------------------------------------------------


def test_branching_mutation_induces_multivalued_monodromy_defect():
    """
    Adversarial branching perturbation: intermediate apex M is inflated such that
    a single carrier fiber splits into multiple target images.
    Verifies that tau^sharp detects non-bijectivity and computes symmetric difference defect.
    """
    pres = _make_metric_presentation("P_base", size=2)
    s_branch, tr_branch = build_monodromy_transport_loop(pres, mode="branching_mutation")

    cert = compute_transport_certificate(s_branch, trace=tr_branch)

    assert cert.is_closed_loop is True
    assert cert.is_trivial_monodromy is False
    assert cert.monodromy_permutation is None  # Non-bijective!
    # Symmetric difference between relation {(0,0), (1,1), (0,1)} and diagonal {(0,0), (1,1)} is {(0,1)} -> defect 1
    assert cert.monodromy_defect == Rational(1, 1)


# ---------------------------------------------------------------------------
# 6. Groupoid CD-12 Monodromy under Carrier Size Thresholds
# ---------------------------------------------------------------------------


def test_groupoid_cd12_monodromy_under_carrier_size_threshold():
    """
    CD-12: Evaluates monodromy in faithful groupoid embeddings (Z_2 and Z_3).
    - Single-generator traversal induces non-trivial monodromy.
    - Full-order cyclic traversal returns trivial monodromy with positive intensional trace cost.
    """
    z2 = make_z2_groupoid()
    emb_z2 = FaithfulGroupoidEmbedding(z2)
    s_g = emb_z2.embed_morphism("g")
    tr_g = emb_z2.lift_trace("g", work_cost=Rational(2, 1))

    cert_g = compute_transport_certificate(s_g, trace=tr_g)
    assert cert_g.is_trivial_monodromy is False
    assert cert_g.monodromy_permutation == (1, 0)
    assert cert_g.monodromy_defect == Rational(2, 1)

    # Full round trip g^2 = e
    s_g2 = compose_spans(s_g, s_g)
    tr_g2 = compose_traces(tr_g, tr_g)
    cert_g2 = compute_transport_certificate(s_g2, trace=tr_g2)
    assert cert_g2.is_trivial_monodromy is True
    assert cert_g2.monodromy_permutation == (0, 1)
    assert cert_g2.monodromy_defect == Rational(0, 1)
    assert cert_g2.work_cost == Rational(4, 1)  # Strictly positive trace cost

    # Z_3 groupoid
    z3 = make_z3_groupoid()
    emb_z3 = FaithfulGroupoidEmbedding(z3)
    s_z3_g = emb_z3.embed_morphism("g")
    cert_z3_g = compute_transport_certificate(s_z3_g)
    assert cert_z3_g.is_trivial_monodromy is False
    assert cert_z3_g.monodromy_permutation == (1, 2, 0)

    # Three-fold cycle g^3 = e
    s_z3_g2 = emb_z3.embed_morphism("g2")
    s_z3_g3 = compose_spans(s_z3_g, s_z3_g2)
    cert_z3_g3 = compute_transport_certificate(s_z3_g3)
    assert cert_z3_g3.is_trivial_monodromy is True
    assert cert_z3_g3.monodromy_permutation == (0, 1, 2)
    assert cert_z3_g3.monodromy_defect == Rational(0, 1)


# ---------------------------------------------------------------------------
# 7. Pipeline Tau^Sharp Terminal Partition under Fiber Perturbations
# ---------------------------------------------------------------------------


def test_pipeline_tau_sharp_terminal_partition_under_fiber_perturbations():
    """
    Regime E: Evaluates Master Normal Form pipeline Pi^sharp under adversarial perturbations:
    1. Overlap agreement failure -> D^sharp gluing fails -> tau^sharp outputs F_term.
    2. Non-closed defect (Gamma_2 > 0) -> tau^sharp outputs F_term.
    3. Closed residual survivor (Phi_1 > 0, Gamma_2 = 0) -> tau^sharp outputs T_res (Anomalon).
    4. Non-promotion firewall: Phi_1 = 0 without authority token -> tau^sharp outputs F_term.
    """
    d0 = Matrix([[1], [-1]])
    d1 = Matrix([[1, 1]])

    # 1. Overlap disagreement
    p_disagree = ProblemInstance(
        problem_id="p_disagree",
        raw_data="data",
        candidate_sieve=("cand1",),
        coarse_profile=(0, 1),
        fine_profile=(0, 1),
        projection_map={0: 0, 1: 1},
        local_sections={"U1": (Rational(0, 1),), "U2": (Rational(1, 1),)},
        overlaps={("U1", "U2"): False},  # Adversarial overlap break
        d0=d0,
        d1=d1,
        defect_cochain=Matrix([[1], [-1]]),
        fda_license_granted=True,
    )
    receipt_disagree = execute_master_normal_form(p_disagree)
    assert receipt_disagree.is_authorized() is False
    assert receipt_disagree.is_refused() is True
    assert "Descent gluing failure" in (receipt_disagree.terminal_outcome.refusal_reason or "")

    # 2. Non-closed defect (Gamma_2 > 0)
    p_nonclosed = ProblemInstance(
        problem_id="p_nonclosed",
        raw_data="data",
        candidate_sieve=("cand1",),
        coarse_profile=(0, 1),
        fine_profile=(0, 1),
        projection_map={0: 0, 1: 1},
        local_sections={"U1": (Rational(0, 1),)},
        overlaps={("U1", "U1"): True},
        d0=d0,
        d1=d1,
        defect_cochain=Matrix([[1], [1]]),  # d1 * defect = [2] != 0 -> Gamma_2 = 2
        fda_license_granted=True,
    )
    receipt_nonclosed = execute_master_normal_form(p_nonclosed)
    assert receipt_nonclosed.is_authorized() is False
    assert receipt_nonclosed.is_refused() is True
    assert "Nonclosed higher coboundary defect" in (
        receipt_nonclosed.terminal_outcome.refusal_reason or ""
    )

    # 3. Closed residual survivor (Phi_1 > 0, Gamma_2 = 0)
    d0_res = Matrix([[0], [0]])
    d1_res = Matrix([[0, 0]])
    p_anomalon = ProblemInstance(
        problem_id="p_anomalon",
        raw_data="data",
        candidate_sieve=("cand1",),
        coarse_profile=(0, 1),
        fine_profile=(0, 1),
        projection_map={0: 0, 1: 1},
        local_sections={"U1": (Rational(0, 1),)},
        overlaps={("U1", "U1"): True},
        d0=d0_res,
        d1=d1_res,
        defect_cochain=Matrix([[1], [1]]),  # Phi_1 = 2, Gamma_2 = 0
        fda_license_granted=False,
    )
    receipt_anomalon = execute_master_normal_form(p_anomalon)
    assert receipt_anomalon.is_authorized() is False
    assert receipt_anomalon.is_anomalon() is True
    assert receipt_anomalon.terminal_outcome.phi1_distance == Rational(2, 1)
    assert receipt_anomalon.terminal_outcome.dual_witness is not None

    # Mechanically verify dual witness
    assert (
        validate_dual_witness(
            d0=d0_res,
            defect=Matrix([[1], [1]]),
            dual_witness=receipt_anomalon.terminal_outcome.dual_witness,
            phi1=Rational(2, 1),
        )
        is True
    )

    # 4. Strict non-promotion firewall under zero residual
    p_unauth = ProblemInstance(
        problem_id="p_unauth",
        raw_data="data",
        candidate_sieve=("cand1",),
        coarse_profile=(0, 1),
        fine_profile=(0, 1),
        projection_map={0: 0, 1: 1},
        local_sections={"U1": (Rational(0, 1),)},
        overlaps={("U1", "U1"): True},
        d0=d0,
        d1=d1,
        defect_cochain=Matrix([[1], [-1]]),  # Phi_1 = 0 (exact repair)
        fda_license_granted=False,  # NO AUTHORITY TOKEN!
    )
    receipt_unauth = execute_master_normal_form(p_unauth)
    assert receipt_unauth.is_authorized() is False
    assert receipt_unauth.is_refused() is True
    assert "Non-promotion firewall" in (receipt_unauth.terminal_outcome.refusal_reason or "")

    # Firewall report
    fw_report = evaluate_authority_firewall(receipt_unauth)
    assert fw_report["firewall_intact"] is True
    assert fw_report["disjoint_partition_holds"] is True
    assert fw_report["authority_effect"] == "None"
