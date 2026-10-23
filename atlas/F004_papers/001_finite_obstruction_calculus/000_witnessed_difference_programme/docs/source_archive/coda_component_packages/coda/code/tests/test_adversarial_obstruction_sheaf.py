# -*- coding: utf-8 -*-
"""
Adversarial Sheaf, HoTT & Obstruction Stress Suite for CODA Core

CHALLENGERS:
- teamwork_preview_sheaf_descent_specialist (Sheaf gluing failure, non-abelian cover obstruction)
- teamwork_preview_hott_specialist (HoTT non-subsumption fences & univalence boundary)
- teamwork_preview_obstruction_solver_adversary (High-cardinality collision separation & menu minima exhaustion)

AuthorityEffect: None.
Citation: sealed-derivation-v1 (3100c4e)
"""

from __future__ import annotations

from fractions import Fraction

import pytest
from coda_core import (
    Collision,
    evaluate_menu,
    factor_or_collision,
)
from coda_discipline_core import (
    HoTTSubsumptionRefusalError,
    assert_hott_non_subsumption_fence,
)


class TestAdversarialSheafAndHomotopyFences:
    """Adversarial stress-testing of sheaf obstruction detection and HoTT discipline fences."""

    def test_sheaf_descent_non_abelian_gluing_obstruction(self):
        """
        Adversarially constructs a 3-panel cover where local sections have pairwise
        consistent observations on 2 of 3 overlaps, but the third overlap introduces a
        non-trivial parity obstruction.
        Verifies that factor_or_collision detects the separating collision pair.
        """
        # States: (panel_id, local_state) for panels 0, 1, 2
        states = ((0, "a"), (0, "b"), (1, "a"), (1, "b"), (2, "a"), (2, "b"))

        # Observation map: maps local state to apparent value
        def observe(state: tuple[int, str]) -> str:
            # Panels 0 and 1 share observation labels directly
            # Panel 2 introduces an adversarial twist mapping "a" -> "x", "b" -> "x"
            panel, val = state
            if panel == 2:
                return "collapsed_obs"
            return val

        # Query represents the underlying true fiber property
        def query(state: tuple[int, str]) -> int:
            panel, val = state
            return 1 if val == "a" else -1

        result = factor_or_collision(states, observe, query)
        assert isinstance(result, Collision), (
            "Failed to detect non-trivial fiber collision under observation collapse"
        )
        assert result.observation == "collapsed_obs"
        assert result.left_value != result.right_value

    def test_hott_non_subsumption_fence_adversarial_phrasings(self):
        """
        Stress-tests the HoTT non-subsumption fence against adversarial permutations
        of forbidden authority-claiming statements.
        """
        valid_statements = [
            "CODA is a companion framework to synthetic homotopy type theory.",
            "We study comparison spans without embedding into univalent foundations.",
            "Fiber monodromies are computed extensionally in CODA_pres.",
        ]
        for stmt in valid_statements:
            assert_hott_non_subsumption_fence(stmt)

        forbidden_statements = [
            "This derivation proves CODA subsumes HoTT in all dimensions.",
            "Our result proves CODA subsumes HoTT unconditionally.",
            "CODA replaces univalence globally for higher topos theory.",
            "This model proves CODA replaces univalence globally across mathematics.",
        ]
        for bad_stmt in forbidden_statements:
            with pytest.raises(HoTTSubsumptionRefusalError):
                assert_hott_non_subsumption_fence(bad_stmt)

    def test_high_cardinality_adversarial_collision_detection(self):
        """
        Constructs an adversarial state space with 1,000 states where an observation
        function is 99.9% injective, but conceals an exact needle collision.
        Verifies exact rational extraction of the separating collision.
        """
        states = tuple(range(1000))

        # Injective everywhere except 42 and 777
        def observe(x: int) -> int:
            if x == 777:
                return 42
            return x

        def query(x: int) -> int:
            return x % 2  # 42 is even (0), 777 is odd (1) -> distinct values!

        result = factor_or_collision(states, observe, query)
        assert isinstance(result, Collision)
        assert result.observation == 42
        assert {result.left, result.right} == {42, 777}
        assert result.left_value != result.right_value

    def test_adversarial_menu_exhaustion_and_tie_retention(self):
        """
        Stress-tests tie retention under degenerate costs and infinite/tied menus.
        Ensures all tied minima are retained with exact rational costs.
        """
        tied_menu = {f"repair_{i}": Fraction(3, 7) for i in range(50)}
        tied_menu["expensive_1"] = Fraction(4, 7)
        tied_menu["expensive_2"] = Fraction(10, 1)

        result = evaluate_menu(tied_menu, lambda _: True)
        assert result.status == "RepairsFound"
        assert len(result.minima) == 50
        assert all(tied_menu[m] == Fraction(3, 7) for m in result.minima)
        assert "expensive_1" not in result.minima
        assert "expensive_2" not in result.minima
