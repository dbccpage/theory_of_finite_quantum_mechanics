from __future__ import annotations

"""FW-5 — per-triple coherence firewall (MS-P22 / MS-C2 / MS-O1 rescope).

THEORETICAL MINIMUM (FW-5)
  INVARIANT  verify_coherence_at(D, h, (c,b,a)) decides K_{c,b,a} h = 0 in
             exact rational arithmetic, K_{c,b,a} = r_{b,a} r_{c,b} - r_{c,a}.
             The verdict is a predicate of (state, triple) and licenses
             NOTHING at any other triple and NOTHING about the operator.
  BREAK      Any of: inheritance without re-check; a bag of statewise greens
             minting the operator claim; a sign flip in K; the checker reading
             only the operator (vacuous when K = 0) or only the state.
  WITNESS    The MS-P22 four-window chain L <= M <= N <= P with truncation
             windows and h_P = (0,0,1,0): INSTANCE_COHERENT at (P,N,M) and
             INCOHERENT at (N,M,L) after pi_NP — the same state, transported,
             flips verdict, so inheritance would have lied.
  MUTATION   In composition_defect, replace the subtraction by addition
             (K = r_{b,a} r_{c,b} + r_{c,a}) -> the exact-control test goes
             red (the coboundary state stops being coherent at (P,N,M)).
             In verify_coherence_at, return INSTANCE_COHERENT unconditionally
             -> the MS-P22 INCOHERENT assertion goes red.
             Remove the `raise` in inherit_coherence -> the F-COH-INHERIT
             kill goes red. Remove the `raise` in
             mint_cochain_complex_established -> the F-COH-PROMOTE kill
             goes red.

Fail conditions pinned here: FW5-FC1 (promote), FW5-FC2 (inherit),
FW5-FC3 (MS-P22 fixture), FW5-FC4 (exact control / anti-vacuity),
FW5-FC6 (status separation), FW5-FC7 (AE None on every receipt surface).

AuthorityEffect: None throughout.
"""

from fractions import Fraction

import pytest

from omega_engine.crates.obstruction_theory.coherence import (
    CoherenceRefusal,
    CoherenceVerdict,
    MalformedDeclaration,
    OperatorVerdict,
    RefusalKind,
    TripleReceipt,
    WindowDeclaration,
    composition_defect,
    inherit_coherence,
    mint_cochain_complex_established,
    restrict,
    verify_coherence_at,
    verify_d1_d0_global,
)

F = Fraction


def _truncation(rows: int, cols: int) -> tuple:
    """Coordinate truncation: keep the first `rows` of `cols` coordinates."""
    return tuple(
        tuple(F(1) if j == i else F(0) for j in range(cols)) for i in range(rows)
    )


def ms_p22_declaration() -> WindowDeclaration:
    """The spine's MS-P22 four-window chain (v0.13.0, section 21.11).

    L <= M <= N <= P with dims 1,2,3,4. Single-step and long maps are
    truncations EXCEPT r_{L,M} = (1 1) and the long maps to L, which sum —
    that mismatch is what makes K_{(N,M,L)} nonzero.
    """
    ones = lambda n: (tuple(F(1) for _ in range(n)),)
    return WindowDeclaration(
        windows=("L", "M", "N", "P"),
        dims={"L": 1, "M": 2, "N": 3, "P": 4},
        restrictions={
            ("N", "P"): _truncation(3, 4),
            ("M", "N"): _truncation(2, 3),
            ("L", "M"): ones(2),
            ("M", "P"): _truncation(2, 4),
            ("L", "N"): ones(3),
            ("L", "P"): ones(4),
        },
    )


def strict_truncation_declaration() -> WindowDeclaration:
    """A chain where EVERY map is a truncation: K = 0 on every triple."""
    return WindowDeclaration(
        windows=("A", "B", "C"),
        dims={"A": 1, "B": 2, "C": 3},
        restrictions={
            ("B", "C"): _truncation(2, 3),
            ("A", "B"): _truncation(1, 2),
            ("A", "C"): _truncation(1, 3),
        },
    )


def d0_P(alpha) -> tuple:
    """Degree-0 coboundary into the P window: alpha -> (alpha, 0, 0, 0).

    Exact-control generator: (W1)-compatible with every declared map of the
    MS-P22 chain (checked in test_exact_control_is_coherent_at_both_triples).
    """
    a = F(alpha)
    return (a, F(0), F(0), F(0))




class TestMsP22Fixture:
    def test_defect_matrices_are_the_spine_values(self):
        D = ms_p22_declaration()
        assert composition_defect(D, ("P", "N", "M")) == (
            (F(0), F(0), F(0), F(0)),
            (F(0), F(0), F(0), F(0)),
        )
        assert composition_defect(D, ("N", "M", "L")) == ((F(0), F(0), F(-1)),)

    def test_h_p_is_coherent_at_top_triple_and_incoherent_below(self):
        D = ms_p22_declaration()
        h_P = (0, 0, 1, 0)
        assert (
            verify_coherence_at(D, h_P, ("P", "N", "M"))
            is CoherenceVerdict.INSTANCE_COHERENT
        )
        h_N = restrict(D, h_P, "P", "N")
        assert h_N == (F(0), F(0), F(1))
        assert (
            verify_coherence_at(D, h_N, ("N", "M", "L"))
            is CoherenceVerdict.INCOHERENT
        )

    def test_incoherence_value_is_the_spine_witness(self):
        """K_{(N,M,L)} (0,0,1) = (-1): the exact number from MS-P22."""
        D = ms_p22_declaration()
        K = composition_defect(D, ("N", "M", "L"))
        h_N = (F(0), F(0), F(1))
        image = tuple(sum(row[j] * h_N[j] for j in range(3)) for row in K)
        assert image == (F(-1),)

    def test_coherence_is_statewise_not_operator_wise(self):
        """Anti-vacuity at a K != 0 triple: the checker reads the STATE.

        At (N,M,L) the defect is nonzero, yet (1,1,0) lies in ker K and is
        INSTANCE_COHERENT while (0,0,1) is INCOHERENT. A checker that only
        inspected K would call both incoherent; one that ignored K would
        call both coherent.
        """
        D = ms_p22_declaration()
        assert (
            verify_coherence_at(D, (1, 1, 0), ("N", "M", "L"))
            is CoherenceVerdict.INSTANCE_COHERENT
        )
        assert (
            verify_coherence_at(D, (0, 0, 1), ("N", "M", "L"))
            is CoherenceVerdict.INCOHERENT
        )




class TestExactControl:
    def test_d0_is_w1_compatible_with_every_declared_map(self):
        """pi . d0_upper = d0_lower for all six maps — the control is not ad hoc."""
        D = ms_p22_declaration()
        d0 = {
            "L": lambda a: (F(a),),
            "M": lambda a: (F(a), F(0)),
            "N": lambda a: (F(a), F(0), F(0)),
            "P": lambda a: (F(a), F(0), F(0), F(0)),
        }
        for (lo, up) in D.restrictions:
            for alpha in (0, 1, -3, F(7, 2)):
                assert restrict(D, d0[up](alpha), up, lo) == d0[lo](alpha), (lo, up)

    def test_exact_control_is_coherent_at_both_triples(self):
        D = ms_p22_declaration()
        for alpha in (5, -2, F(3, 7)):
            h = d0_P(alpha)
            assert (
                verify_coherence_at(D, h, ("P", "N", "M"))
                is CoherenceVerdict.INSTANCE_COHERENT
            )
            h_N = restrict(D, h, "P", "N")
            assert (
                verify_coherence_at(D, h_N, ("N", "M", "L"))
                is CoherenceVerdict.INSTANCE_COHERENT
            )

    def test_zero_state_is_coherent_at_both_triples(self):
        D = ms_p22_declaration()
        assert (
            verify_coherence_at(D, (0, 0, 0, 0), ("P", "N", "M"))
            is CoherenceVerdict.INSTANCE_COHERENT
        )
        assert (
            verify_coherence_at(D, (0, 0, 0), ("N", "M", "L"))
            is CoherenceVerdict.INSTANCE_COHERENT
        )




class TestKillInherit:
    def test_unwitnessed_inheritance_refuses_even_when_true(self):
        """No recheck -> typed refusal, even for the exact control whose
        inherited claim WOULD have been true. Unwitnessed means refused."""
        D = ms_p22_declaration()
        with pytest.raises(CoherenceRefusal) as e:
            inherit_coherence(D, d0_P(5), ("P", "N", "M"), ("N", "M", "L"))
        assert e.value.kind is RefusalKind.F_COH_INHERIT
        assert e.value.authority_effect == "None"

    def test_unwitnessed_inheritance_refuses_on_the_ms_p22_state(self):
        D = ms_p22_declaration()
        with pytest.raises(CoherenceRefusal) as e:
            inherit_coherence(D, (0, 0, 1, 0), ("P", "N", "M"), ("N", "M", "L"))
        assert e.value.kind is RefusalKind.F_COH_INHERIT

    def test_recheck_contradicts_the_would_be_inheritance(self):
        """recheck=True is not inheritance — it re-verifies, and on MS-P22 the
        re-verification returns INCOHERENT where inheritance would say green."""
        D = ms_p22_declaration()
        h_P = (0, 0, 1, 0)
        assert (
            verify_coherence_at(D, h_P, ("P", "N", "M"))
            is CoherenceVerdict.INSTANCE_COHERENT
        )
        assert (
            inherit_coherence(D, h_P, ("P", "N", "M"), ("N", "M", "L"), recheck=True)
            is CoherenceVerdict.INCOHERENT
        )

    def test_refusal_does_not_overclaim_universal_non_transport(self):
        """FW5-FC2b: the refusal names unwitnessed inheritance, not
        transport impossibility."""
        D = ms_p22_declaration()
        with pytest.raises(CoherenceRefusal) as e:
            inherit_coherence(D, d0_P(1), ("P", "N", "M"), ("N", "M", "L"))
        msg = str(e.value)
        assert "unwitnessed" in msg
        assert "transport-with-witness stays open" in msg




class TestKillPromote:
    def _green_receipts(self, D: WindowDeclaration) -> list:
        """An exhaustive-LOOKING bag: every declared triple, several states,
        all INSTANCE_COHERENT. Still must not mint."""
        receipts = []
        for triple in D.triples():
            for h in ((0,) * D.dims[triple[0]], d0_P(3)[: D.dims[triple[0]]]):
                v = verify_coherence_at(D, h, triple)
                if v is CoherenceVerdict.INSTANCE_COHERENT:
                    receipts.append(TripleReceipt(triple=triple, state=tuple(map(F, h)), verdict=v))
        assert receipts, "vacuous kill: bag of receipts is empty"
        return receipts

    def test_bag_of_greens_never_mints(self):
        D = ms_p22_declaration()
        with pytest.raises(CoherenceRefusal) as e:
            mint_cochain_complex_established(self._green_receipts(D))
        assert e.value.kind is RefusalKind.F_COH_PROMOTE

    def test_even_greens_from_a_globally_flat_declaration_never_mint_via_receipts(self):
        """The refusal is about the ROUTE, not the truth of the conclusion:
        on the strict chain K = 0 really does hold, and the receipt route
        still refuses — only the operator check may mint."""
        D = strict_truncation_declaration()
        receipts = [
            TripleReceipt(
                triple=t,
                state=(F(1), F(2), F(3)),
                verdict=verify_coherence_at(D, (1, 2, 3), t),
            )
            for t in D.triples()
        ]
        assert all(r.verdict is CoherenceVerdict.INSTANCE_COHERENT for r in receipts)
        with pytest.raises(CoherenceRefusal) as e:
            mint_cochain_complex_established(receipts)
        assert e.value.kind is RefusalKind.F_COH_PROMOTE

    def test_empty_bag_also_refuses(self):
        with pytest.raises(CoherenceRefusal) as e:
            mint_cochain_complex_established([])
        assert e.value.kind is RefusalKind.F_COH_PROMOTE

    def test_operator_check_is_the_one_honest_mint(self):
        """verify_d1_d0_global: NOT_ESTABLISHED on the MS-P22 chain (a triple
        has K != 0), ESTABLISHED on the strict truncation chain (exact matrix
        equality on every declared triple — basis-complete, FW5-FC1)."""
        assert (
            verify_d1_d0_global(ms_p22_declaration())
            is OperatorVerdict.COCHAIN_COMPLEX_NOT_ESTABLISHED
        )
        assert (
            verify_d1_d0_global(strict_truncation_declaration())
            is OperatorVerdict.COCHAIN_COMPLEX_ESTABLISHED
        )




class TestStatusHygiene:
    def test_statewise_and_operator_verdicts_are_distinct_types(self):
        assert CoherenceVerdict.INSTANCE_COHERENT is not OperatorVerdict.COCHAIN_COMPLEX_ESTABLISHED
        assert not isinstance(CoherenceVerdict.INSTANCE_COHERENT, OperatorVerdict)
        assert not isinstance(OperatorVerdict.COCHAIN_COMPLEX_ESTABLISHED, CoherenceVerdict)
        names = {v.value for v in CoherenceVerdict} | {v.value for v in OperatorVerdict}
        assert len(names) == 4

    def test_receipt_cannot_express_the_operator_claim(self):
        """TripleReceipt has no operator field; storing an OperatorVerdict in
        its verdict slot is a type violation the test pins."""
        fields = set(TripleReceipt.__dataclass_fields__)
        assert fields == {"triple", "state", "verdict", "authority_effect"}

    def test_authority_effect_is_none_on_every_surface(self):
        D = ms_p22_declaration()
        assert D.authority_effect == "None"
        r = TripleReceipt(
            triple=("P", "N", "M"),
            state=(F(0), F(0), F(1), F(0)),
            verdict=verify_coherence_at(D, (0, 0, 1, 0), ("P", "N", "M")),
        )
        assert r.authority_effect == "None"
        with pytest.raises(CoherenceRefusal) as e:
            mint_cochain_complex_established([r])
        assert e.value.authority_effect == "None"




class TestFailClosed:
    def test_misordered_triple_refuses_with_no_verdict(self):
        D = ms_p22_declaration()
        with pytest.raises(MalformedDeclaration):
            verify_coherence_at(D, (0, 0, 1), ("M", "N", "L"))

    def test_unknown_window_refuses(self):
        D = ms_p22_declaration()
        with pytest.raises(MalformedDeclaration):
            verify_coherence_at(D, (0, 0, 1, 0), ("P", "N", "X"))

    def test_wrong_state_dimension_refuses(self):
        D = ms_p22_declaration()
        with pytest.raises(MalformedDeclaration):
            verify_coherence_at(D, (0, 0, 1), ("P", "N", "M"))

    def test_undeclared_restriction_refuses(self):
        D = WindowDeclaration(
            windows=("A", "B", "C"),
            dims={"A": 1, "B": 2, "C": 3},
            restrictions={
                ("B", "C"): _truncation(2, 3),
                ("A", "B"): _truncation(1, 2),
            },
        )
        with pytest.raises(MalformedDeclaration):
            composition_defect(D, ("C", "B", "A"))

    def test_empty_quantifier_never_mints(self):
        """A declaration with no comparable triple cannot be ESTABLISHED
        vacuously — the operator check refuses instead of green-lighting."""
        D = WindowDeclaration(
            windows=("A", "B"),
            dims={"A": 1, "B": 2},
            restrictions={("A", "B"): _truncation(1, 2)},
        )
        with pytest.raises(MalformedDeclaration):
            verify_d1_d0_global(D)

    def test_mixed_complete_incomplete_declaration_abstains(self):
        """PR #1987 review P1: one flat complete triple plus a comparable
        triple with a missing map must NOT mint. The incomplete triple may
        not silently vanish from the quantifier; the check ABSTAINS.

        Chain A<=B<=C<=D. Triple (C,B,A) is complete and flat. Triple
        (D,C,B) — and every other comparable triple through D — lacks maps.
        The old implementation quantified over declared-complete triples
        only and would have minted ESTABLISHED here.
        """
        D = WindowDeclaration(
            windows=("A", "B", "C", "D"),
            dims={"A": 1, "B": 2, "C": 3, "D": 4},
            restrictions={
                ("B", "C"): _truncation(2, 3),
                ("A", "B"): _truncation(1, 2),
                ("A", "C"): _truncation(1, 3),
                ("C", "D"): _truncation(3, 4),
            },
        )
        assert composition_defect(D, ("C", "B", "A")) == ((F(0), F(0), F(0)),)
        with pytest.raises(MalformedDeclaration) as e:
            verify_d1_d0_global(D)
        assert "incomplete quantifier" in str(e.value)

    def test_abstain_is_not_not_established(self):
        """Pass / fail / abstain are three outcomes: a gapped domain raises,
        it does not return COCHAIN_COMPLEX_NOT_ESTABLISHED (which would
        assert a MEASURED non-zero defect that was never measured)."""
        D = WindowDeclaration(
            windows=("A", "B", "C"),
            dims={"A": 1, "B": 2, "C": 3},
            restrictions={
                ("B", "C"): _truncation(2, 3),
                ("A", "B"): _truncation(1, 2),
            },
        )
        try:
            out = verify_d1_d0_global(D)
        except MalformedDeclaration:
            out = None
        assert out is None, f"gapped domain produced an operator verdict: {out!r}"

    def test_receipt_rejects_operator_verdict_injection(self):
        """PR #1987 review P1: annotations do not enforce the firewall —
        the constructor must. Injecting an OperatorVerdict into the verdict
        slot fail-closes at construction."""
        with pytest.raises(MalformedDeclaration) as e:
            TripleReceipt(
                triple=("P", "N", "M"),
                state=(F(0), F(0), F(1), F(0)),
                verdict=OperatorVerdict.COCHAIN_COMPLEX_ESTABLISHED,
            )
        assert "FW5-FC6" in str(e.value)
        with pytest.raises(MalformedDeclaration):
            TripleReceipt(
                triple=("P", "N", "M"),
                state=(F(0),) * 4,
                verdict=CoherenceVerdict.INSTANCE_COHERENT,
                authority_effect="GlobalGreen",
            )

    def test_declaration_rejects_non_none_authority_effect(self):
        """PR #1998 review: WindowDeclaration must carry the same FW5-FC7
        constructor fence as TripleReceipt — a declaration is data and mints
        nothing, so a non-None AE fail-closes at construction."""
        with pytest.raises(MalformedDeclaration) as e:
            WindowDeclaration(
                windows=("A", "B", "C"),
                dims={"A": 1, "B": 2, "C": 3},
                restrictions={
                    ("B", "C"): _truncation(2, 3),
                    ("A", "B"): _truncation(1, 2),
                    ("A", "C"): _truncation(1, 3),
                },
                authority_effect="GlobalGreen",
            )
        assert "FW5-FC7" in str(e.value)

    def test_float_bearing_declaration_is_refused_at_construction(self):
        """PR #1987 review P1: Fraction(0.1) would silently accept the binary
        approximation, so floats are REFUSED, not converted — at the
        declaration boundary, before any verdict arithmetic can run."""
        with pytest.raises(MalformedDeclaration) as e:
            WindowDeclaration(
                windows=("A", "B", "C"),
                dims={"A": 1, "B": 2, "C": 3},
                restrictions={
                    ("B", "C"): ((0.1, 0.0, 0.0), (0.0, 1.0, 0.0)),
                    ("A", "B"): _truncation(1, 2),
                    ("A", "C"): _truncation(1, 3),
                },
            )
        assert "exact-rational only" in str(e.value)

    def test_float_bearing_state_is_refused(self):
        D = ms_p22_declaration()
        with pytest.raises(MalformedDeclaration):
            verify_coherence_at(D, (0.0, 0.0, 1.0, 0.0), ("P", "N", "M"))
        with pytest.raises(MalformedDeclaration):
            TripleReceipt(
                triple=("P", "N", "M"),
                state=(0.0, 0.0, 1.0, 0.0),
                verdict=CoherenceVerdict.INSTANCE_COHERENT,
            )

    def test_exact_string_and_int_scalars_are_accepted(self):
        """The fence rejects floats specifically, not exactness-preserving
        forms: '1/3' and ints pass through and compute exactly."""
        D = WindowDeclaration(
            windows=("A", "B", "C"),
            dims={"A": 1, "B": 1, "C": 1},
            restrictions={
                ("B", "C"): (("1/3",),),
                ("A", "B"): ((3,),),
                ("A", "C"): ((1,),),
            },
        )
        assert composition_defect(D, ("C", "B", "A")) == ((F(0),),)

    def test_exactness_of_arithmetic(self):
        """A near-zero float would corrupt the verdict; Fractions cannot.
        (1/3 + 1/3 + 1/3 - 1) is exactly 0 here, never 1e-16."""
        D = WindowDeclaration(
            windows=("A", "B", "C"),
            dims={"A": 1, "B": 1, "C": 1},
            restrictions={
                ("B", "C"): ((F(1, 3),),),
                ("A", "B"): ((F(3),),),
                ("A", "C"): ((F(1),),),
            },
        )
        assert composition_defect(D, ("C", "B", "A")) == ((F(0),),)
        assert (
            verify_coherence_at(D, (F(22, 7),), ("C", "B", "A"))
            is CoherenceVerdict.INSTANCE_COHERENT
        )


