"""Unit Tests: Primitive Difference Germ: Void to <arb> (Fermion) and <ara> (Boson).
AuthorityEffect: None.
"""

from __future__ import annotations
from pathlib import Path
import sys
import pytest

code_dir = Path(__file__).resolve().parent.parent.parent
if str(code_dir) not in sys.path:
    sys.path.insert(0, str(code_dir))

from fermion_boson_germ import (
    GermState,
    DirectedCutD2,
    SymmetricLinkS2,
    verify_invariant_blindness,
)


def test_germ_genesis_walk():
    """Validates the 5-step genesis walk from void to fermion cut and boson link."""
    state = GermState()
    # Stage 0: Void
    state.step_00_void()
    assert state.stage == 0
    assert len(state.carrier) == 0

    # Stage 1: Lone Mark
    state.step_01_lone_mark("x")
    assert state.stage == 1
    assert state.carrier == {"x"}

    # Stage 2: Unmarked Pair
    state.step_02_unmarked_pair("x", "y")
    assert state.stage == 2
    assert state.carrier == {"x", "y"}

    # Stage 3: Directed Cut (Fermion germ)
    d2 = state.step_03_directed_cut("x", "y")
    assert d2.source == "x"
    assert d2.target == "y"
    assert d2.boundary_0chain == {"y": 1, "x": -1}
    assert len(d2.automorphism_group()) == 1  # Rigid

    # Stage 4: Refused Self-Loop
    success, reason = state.step_04_refuse_self_loop("x")
    assert not success
    assert "boundary a - a = 0" in reason

    # Stage 5: Symmetric Link (Boson germ)
    s2 = state.step_05_symmetric_link("x", "y")
    assert len(s2.automorphism_group()) == 2  # Swap Z2


def test_invariant_blindness():
    """Validates that swap-invariant predicates cannot distinguish D2 from D2_rev."""
    d2 = DirectedCutD2(source="a", target="b")
    preds = [
        lambda pair: set(pair),
        lambda pair: len(pair),
        lambda pair: pair[0] == pair[1],
    ]
    results = verify_invariant_blindness(d2, preds)
    assert all(results.values())
