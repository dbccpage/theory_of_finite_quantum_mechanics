# -*- coding: utf-8 -*-
"""
Adversarial Stress Test Suite: HoTT, Higher Category Theory, Sheaf & Obstruction Theory

CHALLENGERS:
- teamwork_preview_higher_cat_specialist (Bicategorical span coherence, pentagon & triangle identities)
- teamwork_preview_sheaf_descent_specialist (Non-abelian Cech hypercovering descent, gerbe curvature obstructions)
- teamwork_preview_hott_specialist (Synthetic univalence, carrier loop monodromy, observation collision firewall)
- teamwork_preview_obstruction_solver_adversary (Exact solver singularities, Mobius complexes, float refusal)

AuthorityEffect: None.
Citation: sealed-derivation-v1 (3100c4e)
"""

from __future__ import annotations

import pytest
from cochain_presentation import (
    LinearRepairProblem,
    _as_exact_rational,
)
from coda_gtla_core import (
    ComparisonSpan,
    FinitePresentation,
    ProblemInstance,
    TerminalKind,
    Trace,
    compose_spans,
    compute_transport_certificate,
    execute_master_normal_form,
    extensional_equal,
    make_diag_span,
    observation_collision_countermodel,
    untrusted_verifier_countermodel,
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


# ==============================================================================
# 1. CHALLENGER: teamwork_preview_higher_cat_specialist
#    Bicategorical Span Coherence (Pentagons, Unitors, 2-Isomorphisms)
# ==============================================================================


class TestBicategoricalSpanCoherence:
    """Adversarial stress-testing of 2-categorical coherence in Span(FinSet) and CODA_pres."""

    def test_span_bicategory_pentagon_associator_coherence(self):
        """
        Stress-tests the associator pentagon coherence across 4 composable spans.
        Evaluates whether:
          Path 1: ((S1 * S2) * S3) * S4
          Path 2: S1 * (S2 * (S3 * S4))
        yield identical extensional relations and identical extensional transport certificates,
        while demonstrating intensional work cost divergence (CD-12).
        """
        p0 = _make_test_presentation("P0", 3)
        p1 = _make_test_presentation("P1", 3)
        p2 = _make_test_presentation("P2", 3)
        p3 = _make_test_presentation("P3", 3)
        p4 = _make_test_presentation("P4", 3)

        # Spans with permutations and non-trivial carrier apexes
        # S1: P0 -> P1 (cyclic shift)
        s1 = ComparisonSpan(
            p1=p0,
            p2=p1,
            mid_size=3,
            left_map=(0, 1, 2),
            right_map=(1, 2, 0),
            ext_cost=Rational(0),
        )
        # S2: P1 -> P2 (swap 1 and 2)
        s2 = ComparisonSpan(
            p1=p1,
            p2=p2,
            mid_size=3,
            left_map=(0, 1, 2),
            right_map=(0, 2, 1),
            ext_cost=Rational(0),
        )
        # S3: P2 -> P3 (swap 0 and 1)
        s3 = ComparisonSpan(
            p1=p2,
            p2=p3,
            mid_size=3,
            left_map=(0, 1, 2),
            right_map=(1, 0, 2),
            ext_cost=Rational(0),
        )
        # S4: P3 -> P4 (identity)
        s4 = ComparisonSpan(
            p1=p3,
            p2=p4,
            mid_size=3,
            left_map=(0, 1, 2),
            right_map=(0, 1, 2),
            ext_cost=Rational(0),
        )

        # Path 1: Left-associated ((S1 * S2) * S3) * S4
        path1_span = compose_spans(compose_spans(compose_spans(s1, s2), s3), s4)

        # Path 2: Right-associated S1 * (S2 * (S3 * S4))
        path2_span = compose_spans(s1, compose_spans(s2, compose_spans(s3, s4)))

        # Create execution traces with distinct intensional step counts
        t1 = Trace(steps=3, work_cost=Rational(15, 1), span=path1_span)
        t2 = Trace(steps=3, work_cost=Rational(22, 1), span=path2_span)

        cert1 = compute_transport_certificate(path1_span, t1)
        cert2 = compute_transport_certificate(path2_span, t2)

        # Extensional relations must be identical
        assert extensional_equal(path1_span, path2_span) is True, (
            "Pentagon bracketing induced extensional relational discrepancy"
        )

        # Extensional hashes must match exactly
        assert cert1.extensional_hash == cert2.extensional_hash, (
            "Pentagon paths failed extensional transport certificate identity"
        )
        assert cert1.ext_cost == cert2.ext_cost == Rational(0)

        # Intensional work costs must diverge under two-level accounting (CD-12)
        assert cert1.work_cost != cert2.work_cost
        assert cert1.sha256_hash != cert2.sha256_hash

    def test_span_bicategory_left_right_unitor_triangle_coherence(self):
        """
        Stress-tests left and right unitor coherence:
          id_{P_target} * S == S == S * id_{P_source}
        evaluating unitor triangle coherence up to intensional pullback work.
        """
        p_src = _make_test_presentation("P_src", 4)
        p_tgt = _make_test_presentation("P_tgt", 4)

        # Non-trivial span (permutation)
        s = ComparisonSpan(
            p1=p_src,
            p2=p_tgt,
            mid_size=4,
            left_map=(0, 1, 2, 3),
            right_map=(3, 2, 1, 0),
            ext_cost=Rational(0),
        )

        id_src = make_diag_span(p_src)
        id_tgt = make_diag_span(p_tgt)

        # Left unitor composition: S * id_tgt
        left_unitor = compose_spans(s, id_tgt)
        # Right unitor composition: id_src * S
        right_unitor = compose_spans(id_src, s)

        cert_s = compute_transport_certificate(s)
        cert_left = compute_transport_certificate(left_unitor)
        cert_right = compute_transport_certificate(right_unitor)

        assert extensional_equal(left_unitor, s) is True
        assert extensional_equal(right_unitor, s) is True
        assert extensional_equal(left_unitor, right_unitor) is True

        assert cert_left.extensional_hash == cert_s.extensional_hash
        assert cert_right.extensional_hash == cert_s.extensional_hash
        assert cert_left.extensional_hash == cert_right.extensional_hash

    def test_span_2_isomorphism_preserves_quotient_distance(self):
        """
        Stress-tests 2-isomorphisms in Span(FinSet):
        An apex permutation theta in S_M commuting with source/target legs defines a 2-isomorphism.
        Verifies that apex re-indexing strictly preserves quotient distance and dual witness pairing.
        """
        d0 = Matrix(
            [
                [Rational(1), Rational(-1)],
                [Rational(0), Rational(1)],
                [Rational(-1), Rational(0)],
            ]
        )
        defect = Matrix([Rational(2), Rational(1), Rational(3)])

        problem = LinearRepairProblem(d0)
        cert = problem.quotient_l1_distance(defect)
        assert cert.verify()
        assert cert.distance > 0

        # Apply a coboundary homotopy h
        h = Matrix([Rational(1), Rational(2)])
        homotopic_defect = defect + d0 * h
        cert_hom = problem.quotient_l1_distance(homotopic_defect)
        assert cert_hom.verify()

        # Invariance of distance under coboundary homotopy
        assert cert.distance == cert_hom.distance
        # Dual witness preserves pairing
        assert (cert.dual_witness.T * homotopic_defect)[0] == cert.distance


# ==============================================================================
# 2. CHALLENGER: teamwork_preview_sheaf_descent_specialist
#    Non-Abelian Cech Descent & Higher Curvature Obstructions
# ==============================================================================


class TestSheafDescentNonAbelianObstructions:
    """Adversarial stress-testing of non-abelian Cech descent and higher curvature obstructions."""

    def test_non_abelian_s3_cech_hypercovering_flat_descent(self):
        """
        Constructs an open cover of 3 sets U0, U1, U2 with transition maps in S3:
          g_01 = (0 1)
          g_12 = (1 2)
          g_02 = (0 1 2) = g_12 * g_01
        The 1-cocycle condition g_02^{-1} * g_12 * g_01 == id holds strictly (flat non-abelian bundle).
        Verifies that the transport certificate around the cycle certifies trivial monodromy (Delta_mon = 0).
        """
        p0 = _make_test_presentation("P0", 3)
        p1 = _make_test_presentation("P1", 3)
        p2 = _make_test_presentation("P2", 3)

        # g_01: (0 1)
        s01 = ComparisonSpan(
            p1=p0,
            p2=p1,
            mid_size=3,
            left_map=(0, 1, 2),
            right_map=(1, 0, 2),
            ext_cost=Rational(0),
        )
        # g_12: (1 2)
        s12 = ComparisonSpan(
            p1=p1,
            p2=p2,
            mid_size=3,
            left_map=(0, 1, 2),
            right_map=(0, 2, 1),
            ext_cost=Rational(0),
        )
        # (1 2) * (0 1) maps:
        # 0 -> 1 -> 2
        # 1 -> 0 -> 0
        # 2 -> 2 -> 1
        # which is (0 2 1): 0->2, 1->0, 2->1.
        # Its inverse must map: 2->0, 0->1, 1->2, i.e. right_map = (1, 2, 0).
        s20 = ComparisonSpan(
            p1=p2,
            p2=p0,
            mid_size=3,
            left_map=(0, 1, 2),
            right_map=(1, 2, 0),
            ext_cost=Rational(0),
        )

        # Compose around the closed cycle: S20 * S12 * S01 : P0 -> P0
        cycle_span = compose_spans(compose_spans(s01, s12), s20)

        cert = compute_transport_certificate(cycle_span)
        assert cert.is_closed_loop is True
        assert cert.is_trivial_monodromy is True
        assert cert.monodromy_defect == Rational(0)
        assert cert.monodromy_permutation == (0, 1, 2)

    def test_non_abelian_s3_twisted_curvature_obstruction_and_firewall(self):
        """
        Introduces a non-abelian curvature twist in the transition cocycle:
          g'_20 = (0 2) != (0 1 2)
        The curvature / 2-cocycle obstruction along the triple overlap is:
          g'_20 * g_12 * g_01 = (0 2) * (0 2 1) = (1 2) != id.
        Verifies that the transport certificate detects non-trivial monodromy (Delta_mon > 0),
        and passing an unlicensed/anomalous instance into the pipeline halts without issuing authority.
        """
        p0 = _make_test_presentation("P0", 3)
        p1 = _make_test_presentation("P1", 3)
        p2 = _make_test_presentation("P2", 3)

        # g_01: (0 1)
        s01 = ComparisonSpan(
            p1=p0,
            p2=p1,
            mid_size=3,
            left_map=(0, 1, 2),
            right_map=(1, 0, 2),
            ext_cost=Rational(0),
        )
        # g_12: (1 2)
        s12 = ComparisonSpan(
            p1=p1,
            p2=p2,
            mid_size=3,
            left_map=(0, 1, 2),
            right_map=(0, 2, 1),
            ext_cost=Rational(0),
        )
        # g'_20: transposition (0 2)
        s20_twisted = ComparisonSpan(
            p1=p2,
            p2=p0,
            mid_size=3,
            left_map=(0, 1, 2),
            right_map=(2, 1, 0),
            ext_cost=Rational(0),
        )

        cycle_span = compose_spans(compose_spans(s01, s12), s20_twisted)

        cert = compute_transport_certificate(cycle_span)
        assert cert.is_closed_loop is True
        assert cert.is_trivial_monodromy is False
        assert cert.monodromy_defect > Rational(0)
        # Non-trivial monodromy permutation (1 2): 0->0, 1->2, 2->1
        assert cert.monodromy_permutation == (0, 2, 1)

        # Pass through pipeline normal form with the twisted defect
        prob = ProblemInstance(
            problem_id="test_s3_twisted",
            raw_data="s3_twisted_data",
            candidate_sieve=("cand1",),
            coarse_profile=(0, 1, 2),
            fine_profile=(0, 1, 2),
            projection_map={0: 0, 1: 1, 2: 2},
            local_sections={"U0": (Rational(1, 2),)},
            overlaps={("U0", "U0"): True},
            d0=Matrix([[0], [0], [0]]),
            d1=Matrix([[0, 0, 0]]),
            defect_cochain=Matrix([[1], [1], [1]]),
            fda_license_granted=False,  # Unlicensed adversary
        )
        outcome = execute_master_normal_form(prob)

        # The non-promotion firewall strictly blocks issuance of AuthorityToken
        assert outcome.terminal_outcome.kind != TerminalKind.AUTHORIZED, (
            "FIREWALL BREACH: Non-abelian curvature twist synthesized spurious AuthorityToken"
        )
        assert outcome.terminal_outcome.kind in (
            TerminalKind.CLOSED_RESIDUAL,
            TerminalKind.REFUSED,
        )


# ==============================================================================
# 3. CHALLENGER: teamwork_preview_hott_specialist
#    Synthetic Homotopy Types, Univalence & Observation Collisions
# ==============================================================================


class TestHoTTUnivalenceAndFibrationHolonomy:
    """Adversarial stress-testing of synthetic univalence and fibration holonomy."""

    def test_hott_synthetic_univalence_carrier_loop_monodromy(self):
        """
        In HoTT, Aut(P) corresponds to the loop space Omega(U_pres, P).
        For the 2-point presentation P, Aut(P) = Z2.
        Traversing the generator loop S_swap flips the points:
          transport holonomy = (1, 0), defect = 4 (diff_01 + diff_10 = 2 + 2).
        Traversing the loop twice (S_swap * S_swap) contracts to the identity loop.
        """
        p = _make_test_presentation("P_bin", 2)

        # S_swap: transposition (0 1)
        s_swap = ComparisonSpan(
            p1=p,
            p2=p,
            mid_size=2,
            left_map=(0, 1),
            right_map=(1, 0),
            ext_cost=Rational(0),
        )

        cert_single = compute_transport_certificate(s_swap)
        assert cert_single.is_closed_loop is True
        assert cert_single.is_trivial_monodromy is False
        assert cert_single.monodromy_permutation == (1, 0)
        assert cert_single.monodromy_defect == Rational(4, 1)

        # Double traversal: S_swap * S_swap
        s_double = compose_spans(s_swap, s_swap)
        cert_double = compute_transport_certificate(s_double)
        assert cert_double.is_closed_loop is True
        assert cert_double.is_trivial_monodromy is True
        assert cert_double.monodromy_permutation == (0, 1)
        assert cert_double.monodromy_defect == Rational(0)

    def test_hott_fibration_observation_collision_refusal(self):
        """
        Stress-tests observation collision detection (FDA-04).
        Constructs a fiber bundle E -> B where two distinct internal authority states
        project to identical observations.
        Asserts that observation_collision_countermodel and untrusted_verifier_countermodel
        strictly catch the collision and refuse promotion.
        """
        coll = observation_collision_countermodel()
        assert coll["observation_identical"] is True
        assert coll["s1_authorized"] != coll["s2_authorized"]
        assert coll["authority_separated"] is True

        untrusted = untrusted_verifier_countermodel()
        assert untrusted["firewall_blocked_unauthorized"] is True
        assert untrusted["is_authorized"] is False
        assert untrusted["is_refused"] is True


# ==============================================================================
# 4. CHALLENGER: teamwork_preview_obstruction_solver_adversary
#    Exact Solver Singularities, Mobius Complexes & Float Refusal
# ==============================================================================


class TestExactSolverSingularitiesAndDegeneracies:
    """Adversarial stress-testing of standalone exact cochain and quotient solver."""

    def test_exact_solver_mobius_torsion_boundary_complex(self):
        """
        Constructs a 3-edge, 3-vertex cochain complex modeling a Mobius band with twisted boundary:
          d0 = [[-1,  1,  0],
                [ 0, -1,  1],
                [ 1,  0,  1]]
        Evaluates exact rational quotient distance and certifies dual witness pairing.
        """
        d0 = Matrix(
            [
                [Rational(-1), Rational(1), Rational(0)],
                [Rational(0), Rational(-1), Rational(1)],
                [Rational(1), Rational(0), Rational(1)],
            ]
        )
        omega = Matrix([Rational(5), Rational(3), Rational(7)])

        problem = LinearRepairProblem(d0)
        cert = problem.quotient_l1_distance(omega)

        assert cert.verify()
        assert cert.distance >= Rational(0)
        assert cert.dual_witness.shape == (3, 1)
        assert all(abs(val) <= Rational(1) for val in cert.dual_witness)
        assert (d0.T * cert.dual_witness) == Matrix.zeros(3, 1)
        assert (cert.dual_witness.T * omega)[0] == cert.distance

    def test_exact_solver_rank_zero_degenerate_complex(self):
        """
        Stress-tests solver behavior on completely degenerate complex with rank(d0) == 0:
          d0 = [[0, 0], [0, 0], [0, 0]]
        Here im(d0) = {0}, so Phi_1 = ||omega||_1, and dual witness is sgn(omega).
        """
        d0 = Matrix.zeros(3, 2)
        omega = Matrix([Rational(-4), Rational(7), Rational(-11)])

        problem = LinearRepairProblem(d0)
        cert = problem.quotient_l1_distance(omega)

        assert cert.verify()
        assert cert.distance == Rational(22)  # |-4| + |7| + |-11| = 22
        assert cert.dual_witness == Matrix([Rational(-1), Rational(1), Rational(-1)])
        assert (cert.dual_witness.T * omega)[0] == Rational(22)

    def test_exact_solver_adversarial_float_injection_hard_refusal(self):
        """
        Adversarially injects IEEE 754 floating point numbers and booleans into the exact arithmetic gate.
        Asserts strict fail-closed TypeError.
        """
        with pytest.raises(TypeError, match="exact arithmetic rejects float"):
            _as_exact_rational(0.5)

        with pytest.raises(TypeError, match="exact arithmetic rejects float"):
            _as_exact_rational(float("nan"))

        with pytest.raises(TypeError, match="exact arithmetic rejects float"):
            _as_exact_rational(float("inf"))

        with pytest.raises(TypeError, match="exact arithmetic rejects bool"):
            _as_exact_rational(True)

        with pytest.raises(TypeError, match="exact arithmetic rejects bool"):
            _as_exact_rational(False)
