"""Witness soundness and receipt canonicality for PO-OE-CORE-001.

Every test here names the production defect it would catch:

- ``test_witness_word_actually_separates`` fails if the distinguishing word is
  truncated instead of carried across refinement rounds.
- ``test_witness_rejects_non_separating_word`` fails if ``ReturningProjectionWitness``
  can be constructed without exhibiting a difference.
- ``test_receipt_hash_is_permutation_invariant`` fails if the receipt hashes
  insertion order instead of the semantic quotient.
- ``test_generator_leaving_state_space_is_refused`` /
  ``test_colliding_state_ids_are_refused`` fail if unchecked preconditions
  silently corrupt the partition.
"""

import pytest

from omega_engine.crates.representation.projection_context_congruence import (
    ProjectionContextCongruenceEngine,
    ReturningProjectionWitness,
)


def _two_chain_engine():
    """A -a-> B -a-> D(obs 1) and P -a-> Q -a-> R(obs 0).

    Only ``D`` is observable, so ``A`` and ``P`` agree on every prefix of length
    < 2 and are separated only by the word ``("a", "a")``. Any implementation
    that reports a length-1 word here is emitting a false witness.
    """
    table = {"A": "B", "B": "D", "D": "D", "P": "Q", "Q": "R", "R": "R"}
    generators = {"a": lambda s: table[s]}
    obs = lambda s: 1 if s == "D" else 0
    states = ["A", "B", "D", "P", "Q", "R"]
    return ProjectionContextCongruenceEngine(states, generators, obs), generators, obs


def test_partition_is_the_correct_behavioural_quotient():
    engine, _, _ = _two_chain_engine()
    result = engine.compute_core_c()

    blocks = sorted(sorted(b) for b in result.final_blocks)
    assert blocks == [["A"], ["B"], ["D"], ["P", "Q", "R"]]


def test_witness_word_actually_separates():
    """Replay each emitted word independently; it must produce differing observations."""
    engine, generators, obs = _two_chain_engine()
    result = engine.compute_core_c()

    assert result.witnesses, "refinement split blocks but emitted no witness"

    for witness in result.witnesses:
        end_x, end_y = witness.state_x, witness.state_y
        for symbol in witness.context_word:
            end_x = generators[symbol](end_x)
            end_y = generators[symbol](end_y)

        assert obs(end_x) != obs(end_y), (
            f"witness {witness.state_x}/{witness.state_y} word "
            f"{witness.context_word} does not separate: both observe {obs(end_x)}"
        )
        assert witness.obs_x_after != witness.obs_y_after, (
            f"witness {witness.state_x}/{witness.state_y} records identical "
            f"observations {witness.obs_x_after}"
        )


def test_every_returning_pair_has_a_witness():
    """Completeness over the pairs the witness class is actually about.

    A pair already split by ``ker o`` needs no context word and is not a
    *returning* witness. The claim to discharge is: every pair that ``ker o``
    identifies but ``Core_C(ker o)`` separates carries a non-empty word.
    """
    engine, _, _ = _two_chain_engine()
    result = engine.compute_core_c()

    witnessed = {frozenset((w.state_x, w.state_y)) for w in result.witnesses}
    initial_of = {
        sid: idx for idx, block in enumerate(result.initial_blocks) for sid in block
    }
    final_of = {
        sid: idx for idx, block in enumerate(result.final_blocks) for sid in block
    }
    returning = {
        frozenset((x, y))
        for x in final_of
        for y in final_of
        if x != y and initial_of[x] == initial_of[y] and final_of[x] != final_of[y]
    }

    assert returning <= witnessed, (
        "unwitnessed returning pairs: "
        f"{sorted(tuple(sorted(p)) for p in returning - witnessed)}"
    )
    assert all(w.context_word for w in result.witnesses), (
        "a returning witness must carry a non-empty context word"
    )


def test_witness_rejects_non_separating_word():
    """A witness recording identical observations is a contradiction; refuse it."""
    with pytest.raises(ValueError):
        ReturningProjectionWitness(
            state_x="A",
            state_y="P",
            context_word=("a",),
            obs_x_after="0",
            obs_y_after="0",
        )


def test_receipt_hash_is_permutation_invariant():
    """Same quotient from a permuted state list must produce the same receipt."""
    table = {"S0": "S2", "S1": "S0", "S2": "S2"}
    generators = {"a": lambda s: table[s]}
    obs = lambda s: 0 if s in ("S0", "S1") else 1

    first = ProjectionContextCongruenceEngine(
        ["S0", "S1", "S2"], generators, obs
    ).compute_core_c()
    second = ProjectionContextCongruenceEngine(
        ["S2", "S1", "S0"], generators, obs
    ).compute_core_c()

    assert first.receipt_hash == second.receipt_hash


def test_receipt_hash_separates_distinct_quotients():
    """The receipt must not collapse genuinely different refinements."""
    table = {"S0": "S2", "S1": "S0", "S2": "S2"}
    generators = {"a": lambda s: table[s]}

    split = ProjectionContextCongruenceEngine(
        ["S0", "S1", "S2"], generators, lambda s: 0 if s in ("S0", "S1") else 1
    ).compute_core_c()
    collapsed = ProjectionContextCongruenceEngine(
        ["S0", "S1", "S2"], generators, lambda s: 0
    ).compute_core_c()

    assert split.receipt_hash != collapsed.receipt_hash


def test_generator_leaving_state_space_is_refused():
    """Successors outside X must not be silently collapsed into a sentinel block."""
    with pytest.raises(ValueError, match="outside"):
        ProjectionContextCongruenceEngine(
            ["p", "q"], {"g": lambda s: "ESCAPED"}, lambda s: 0
        )


def test_colliding_state_ids_are_refused():
    """Two states sharing an id would silently vanish from the partition."""
    with pytest.raises(ValueError, match="collision"):
        ProjectionContextCongruenceEngine(
            [(1, "a"), (1, "b")],
            {"g": lambda s: s},
            lambda s: 0,
            state_id_fn=lambda s: str(s[0]),
        )


def test_discrete_partition_is_already_a_congruence():
    """Core_C(bot) = bot.

    An injective observation leaves nothing to refine. This is the degenerate
    case the calculus demo hit; keeping it as an explicit test stops it from
    being presented as a verification result.
    """
    grid = list(range(11))
    engine = ProjectionContextCongruenceEngine(
        grid, {"shift": lambda x: min(10, x + 1)}, observation_fn=lambda x: x
    )
    result = engine.compute_core_c()

    assert result.splits_count == 0
    assert result.witnesses == []
    assert result.is_invariant is True
    assert len(result.final_blocks) == 11


