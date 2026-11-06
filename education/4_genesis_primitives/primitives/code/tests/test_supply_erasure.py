"""Replay-level supply erasure on the Python copy of the Genesis regime.

Companion to ``primitives/lean4/SupplyErasure.lean``.  The Lean theorem
``replayE_filter_supply`` is about the token-erased Lean ``replayE``; this
suite checks the same identity on the token-aware Python ``replay`` of
``seed_and_regime.py`` (a copy of 19L57G1 ``code/derivation/model.py``
semantics) over seeded random well-formed histories.  It is evidence for
the tested histories only, not a proof about the Python model.

AuthorityEffect: None.
"""

from __future__ import annotations

import importlib.util
import random
import sys
from pathlib import Path

PRIMITIVES_DIR = Path(__file__).resolve().parent.parent


def _load_seed_and_regime():
    """Load the primitives package by path (its directory name is digit-prefixed)."""
    init_path = PRIMITIVES_DIR / "__init__.py"
    spec = importlib.util.spec_from_file_location(
        "genesis_primitives",
        init_path,
        submodule_search_locations=[str(PRIMITIVES_DIR)],
    )
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load spec for {init_path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["genesis_primitives"] = mod
    spec.loader.exec_module(mod)
    return importlib.import_module("genesis_primitives.seed_and_regime")


sr = _load_seed_and_regime()

SEEDS = range(20)
LENGTH = 40


def _is_supply(e) -> bool:
    return isinstance(e, sr.Supply)


def _random_history(rng: random.Random, length: int):
    """A well-formed history: every admission is legal at the regime it hits."""
    r = sr.EMPTY
    history = []
    for k in range(length):
        choice = rng.random()
        if choice < 0.30:
            e = sr.Supply(f"t{rng.randrange(6)}")
        elif choice < 0.50:
            e = sr.AdmitDatum(f"t{rng.randrange(6)}")
        elif choice < 0.62:
            e = sr.AdmitForm(rng.randrange(1, 3))
        elif choice < 0.80 and r.forms and r.data:
            form = rng.randrange(len(r.forms))
            args = tuple(rng.randrange(len(r.data)) for _ in range(r.forms[form]))
            e = sr.AdmitInst(form, args)
        elif choice < 0.90 and r.forms:
            e = sr.AdmitRuleAll(rng.randrange(len(r.forms)))
        elif len(r.data) >= 2:
            i = rng.randrange(len(r.data) - 1)
            j = rng.randrange(i + 1, len(r.data))
            e = sr.Impose(i, j)
        else:
            e = sr.Supply(f"t{k}")
        r = sr.step(r, e)
        history.append(e)
    return history


def test_step_supply_no_op():
    rng = random.Random(0)
    for _ in range(50):
        r = sr.replay(_random_history(rng, 10))
        assert sr.step(r, sr.Supply("x")) == r


def test_replay_filter_supply():
    for seed in SEEDS:
        h = _random_history(random.Random(seed), LENGTH)
        assert any(_is_supply(e) for e in h), "history must contain a supply to be a test"
        kept = [e for e in h if not _is_supply(e)]
        assert sr.replay(kept) == sr.replay(h)


def test_replay_supply_only():
    for seed in SEEDS:
        rng = random.Random(seed)
        base = sr.replay(_random_history(rng, 10))
        supplies = [sr.Supply(f"s{rng.randrange(9)}") for _ in range(rng.randrange(0, 8))]
        assert sr.replay(supplies, base) == base


def test_replay_interleaving_invariance():
    for seed in SEEDS:
        rng = random.Random(seed)
        h = _random_history(rng, LENGTH)
        kept = [e for e in h if not _is_supply(e)]
        other = []
        for e in kept:
            for _ in range(rng.randrange(0, 3)):
                other.append(sr.Supply(f"u{rng.randrange(9)}"))
            other.append(e)
        assert [e for e in other if not _is_supply(e)] == kept
        assert sr.replay(other) == sr.replay(h)
