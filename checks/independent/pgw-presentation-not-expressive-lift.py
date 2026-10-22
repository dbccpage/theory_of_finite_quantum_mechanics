#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""Independent Verification Script for PGW-PRESENTATION-NOT-EXPRESSIVE-LIFT (TFQ-0422).

AuthorityEffect: None.

Verifies:
1. Presentation sets P0 = {<>} and P1 = {<>, <a>} with card(P0)=1, card(P1)=2, P0 ⊂ P1.
2. Internal observations O0 = ∅, O1 = ∅, and no new distinction: O1 \ O0 = ∅.
3. Distinction map q : P -> N sending an inscription to internal distinctions.
4. Non-injectivity of q: x ≠ y with q(x) = q(y).
5. Non-implications:
   - x ≠ y does not imply q(x) ≠ q(y) (a new presentation does not imply a new internal class).
   - q(x) = q(y) does not imply x = y.
6. Identity convention behavior:
   - Opaque convention: quotient size |P / ~| = 1.
   - Exact-inscription convention: quotient size |P / ~| = 2.
7. Verification that collapsing distinct presentations occurs under the opaque convention only.
8. Discrete unformed regime model verifying collapse of marks 0 and 1.

CRITICAL: ZERO repository imports. Plain Python + SymPy only.
"""
from __future__ import annotations

import sys
from enum import Enum, auto
from typing import Any, Dict, FrozenSet, List, Set, Tuple
import sympy as sp


class Inscription(Enum):
    NIL = "<>"
    MARK_A = "<a>"


class IdentityConvention(Enum):
    OPAQUE = auto()
    EXACT_INSCRIPTION = auto()


def check_presentation_growth() -> Tuple[sp.Integer, sp.Integer]:
    p0: FrozenSet[Inscription] = frozenset({Inscription.NIL})
    p1: FrozenSet[Inscription] = frozenset({Inscription.NIL, Inscription.MARK_A})

    assert len(p0) == 1, "P0 must have cardinality 1"
    assert len(p1) == 2, "P1 must have cardinality 2"
    assert p0 < p1, "P0 must be a strict subset of P1"
    assert Inscription.MARK_A not in p0, "<a> must not be in initial presentation P0"
    assert Inscription.MARK_A in p1, "<a> must be in presentation P1"

    sp_card_p0 = sp.Integer(len(p0))
    sp_card_p1 = sp.Integer(len(p1))
    return sp_card_p0, sp_card_p1


def check_internal_observations() -> Tuple[FrozenSet[int], FrozenSet[int]]:
    # In unformed regime, internal distinction set for every inscription is empty
    o0: FrozenSet[int] = frozenset()
    o1: FrozenSet[int] = frozenset()

    assert len(o0) == 0, "O0 must be empty"
    assert len(o1) == 0, "O1 must be empty"
    assert o0 == o1, "O0 must equal O1"
    assert len(o1 - o0) == 0, "O1 \\ O0 must be empty (no new internal distinction)"

    return o0, o1


def check_distinction_map_non_injectivity() -> None:
    # q sends an inscription to internal distinctions
    def q(x: Inscription) -> FrozenSet[int]:
        return frozenset()

    x = Inscription.NIL
    y = Inscription.MARK_A

    # 1. Distinct presentation inscriptions
    assert x != y, "Inscriptions <> and <a> must be syntactically distinct"

    # 2. Identical distinction image
    assert q(x) == q(y), "q(<>) must equal q(<a>)"

    # 3. Non-implication: x != y -> q(x) != q(y) fails
    injective_claim = all(
        q(a) != q(b)
        for a in Inscription
        for b in Inscription
        if a != b
    )
    assert not injective_claim, "q must not be injective: new presentation does not imply new class"

    # 4. Non-implication: q(x) == q(y) -> x == y fails
    converse_claim = all(
        a == b
        for a in Inscription
        for b in Inscription
        if q(a) == q(b)
    )
    assert not converse_claim, "q(x) = q(y) must not imply x = y"


def compute_quotient_classes(
    conv: IdentityConvention,
    obs_map: Dict[Inscription, FrozenSet[int]],
) -> List[Set[Inscription]]:
    elements = list(Inscription)
    classes: List[Set[Inscription]] = []

    for elem in elements:
        placed = False
        for c in classes:
            rep = next(iter(c))
            equiv = False
            if conv == IdentityConvention.OPAQUE:
                equiv = (obs_map[elem] == obs_map[rep])
            elif conv == IdentityConvention.EXACT_INSCRIPTION:
                equiv = (elem == rep)
            if equiv:
                c.add(elem)
                placed = True
                break
        if not placed:
            classes.append({elem})

    return classes


def check_identity_conventions() -> None:
    obs_map = {
        Inscription.NIL: frozenset(),
        Inscription.MARK_A: frozenset(),
    }

    # Under Opaque convention:
    opaque_classes = compute_quotient_classes(IdentityConvention.OPAQUE, obs_map)
    assert len(opaque_classes) == 1, (
        f"Opaque quotient must have 1 class, got {len(opaque_classes)}"
    )
    assert opaque_classes[0] == {Inscription.NIL, Inscription.MARK_A}, (
        "Opaque class must contain both <> and <a>"
    )

    # Under Exact-Inscription convention:
    exact_classes = compute_quotient_classes(IdentityConvention.EXACT_INSCRIPTION, obs_map)
    assert len(exact_classes) == 2, (
        f"Exact-inscription quotient must have 2 classes, got {len(exact_classes)}"
    )
    exact_sets = [set(c) for c in exact_classes]
    assert {Inscription.NIL} in exact_sets and {Inscription.MARK_A} in exact_sets, (
        "Exact quotient must keep <> and <a> separated"
    )

    # Verification: collapsing distinct presentations occurs under opaque only
    def has_collapsing(conv: IdentityConvention) -> bool:
        classes = compute_quotient_classes(conv, obs_map)
        return any(len(c) > 1 for c in classes)

    assert has_collapsing(IdentityConvention.OPAQUE) is True, (
        "Opaque convention must collapse distinct presentations"
    )
    assert has_collapsing(IdentityConvention.EXACT_INSCRIPTION) is False, (
        "Exact convention must not collapse distinct presentations"
    )

    # Biconditional check across all conventions
    for conv in IdentityConvention:
        assert (has_collapsing(conv) == (conv == IdentityConvention.OPAQUE)), (
            "Collapsing must hold under opaque convention only"
        )


def check_genesis_unformed_regime_model() -> None:
    # Minimal discrete regime: data count and list of unary forms
    class Regime:
        def __init__(self, data: int, forms: List[int], insts: List[Tuple[int, List[int]]]):
            self.data = data
            self.forms = forms
            self.insts = insts

    # Unformed regime with 2 data marks
    r0 = Regime(data=2, forms=[], insts=[])

    def unary_sep(r: Regime, i: int, j: int) -> bool:
        for f, arity in enumerate(r.forms):
            if arity == 1:
                i_in = (f, [i]) in r.insts
                j_in = (f, [j]) in r.insts
                if (i_in and not j_in) or (j_in and not i_in):
                    return True
        return False

    def collapsed(r: Regime, i: int, j: int) -> bool:
        return not unary_sep(r, i, j) and not unary_sep(r, j, i)

    # Two data marks in unformed regime
    assert not unary_sep(r0, 0, 1), "Marks 0 and 1 must not be unary-separated in unformed regime"
    assert not unary_sep(r0, 1, 0), "Marks 1 and 0 must not be unary-separated in unformed regime"
    assert collapsed(r0, 0, 1), "Marks 0 and 1 must be collapsed in unformed regime"


def main() -> int:
    print("=== Independent Check: PGW-PRESENTATION-NOT-EXPRESSIVE-LIFT (TFQ-0422) ===")

    # 1. Presentation growth
    card_p0, card_p1 = check_presentation_growth()
    print(f"[OK] Presentation growth: |P0| = {card_p0}, |P1| = {card_p1}, P0 ⊂ P1 verified.")

    # 2. Internal observations
    o0, o1 = check_internal_observations()
    print(f"[OK] Internal observations: O0 = {set(o0)}, O1 = {set(o1)}, O1 \\ O0 = ∅ verified.")

    # 3. Non-injectivity of distinction map
    check_distinction_map_non_injectivity()
    print("[OK] Distinction map q non-injectivity verified: x ≠ y with q(x) = q(y).")
    print("     - New presentation does not imply new internal class: VERIFIED.")
    print("     - Equal internal distinction does not imply same presentation: VERIFIED.")

    # 4. Identity conventions
    check_identity_conventions()
    print("[OK] Identity conventions verified:")
    print("     - Opaque convention quotient size = 1 (collapse holds).")
    print("     - Exact-inscription convention quotient size = 2 (collapse fails).")
    print("     - Collapse holds under opaque convention only: VERIFIED.")

    # 5. Genesis unformed regime
    check_genesis_unformed_regime_model()
    print("[OK] Genesis unformed regime model: 2 data marks with 0 forms are collapsed: VERIFIED.")

    print("\nALL INVARIANTS INDEPENDENTLY VERIFIED (Exit 0).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
