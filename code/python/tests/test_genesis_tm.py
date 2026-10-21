"""Tests for the independent Genesis computation checker.

Origin: code/python/src/qm/genesis_tm.py
Claim: urn:omega:fqm:genesis-computation:word-rewriting-tm0-simulation:v1
AuthorityEffect: None
Mutation-Kills: 0 non-equivalent
"""

from __future__ import annotations

import pytest

from src.qm.genesis_tm import (
    FIRST_SEPARATION,
    canonical_regime,
    collapsed,
    pairwise_separated,
    LEND,
    REND,
    Machine,
    all_two_state_machines,
    bounded_reach,
    busy_beaver_2,
    code_width,
    config_space_size,
    context_counts,
    decide_reach,
    decode,
    decode_binary,
    encode,
    encode_binary,
    incrementer,
    is_irreducible,
    replay,
    right_runner,
    rules_for,
    run_checked,
    step_e,
    successors,
)


def test_rewrite_in_context_and_empty_lhs():
    rules = [("ab", "ba")]
    assert successors(rules, "aabb") == {"abab"}
    assert successors(rules, "abab") == {"baab", "abba"}
    assert is_irreducible(rules, "bbaa")
    assert len(successors([("", "x")], "ab")) == 3


def test_bounded_decider_exact_when_closed():
    rules = [("ab", "ba")]
    seen, exceeded = bounded_reach(rules, "aabb", 4)
    assert exceeded is None
    assert len(seen) == 6
    assert decide_reach(rules, "aabb", "bbaa", 4)[0] == "reachable"
    # the search is closed, so unreachable is a complete answer
    assert decide_reach(rules, "bbaa", "aabb", 4)[0] == "unreachable"
    assert len(seen) <= config_space_size(2, 4)


@pytest.mark.parametrize("bound", range(1, 13))
def test_growth_rule_is_refused_with_bound_exceeded(bound):
    verdict, witness = decide_reach([("a", "aa")], "a", "b", bound)
    assert verdict == "bound_exceeded"
    frm, to = witness
    assert len(frm) == bound and len(to) == bound + 1


def test_start_outside_bound_is_refused():
    with pytest.raises(ValueError):
        decide_reach([], "aaa", "a", 2)


def test_encode_decode_roundtrip():
    m = incrementer()
    word = encode(m, 1, {-3: 1, -1: 1, 1: 1, 2: 0}, 0)
    state, head_sym, cells = decode(m, word)
    assert state == 1 and head_sym == 0
    assert dict(cells) == {-3: 1, -1: 1, 1: 1}
    assert decode(m, "[]") is None
    # two state marks: not a configuration word
    assert decode(m, LEND + "B0B0" + REND) is None


@pytest.mark.parametrize("n", range(0, 65))
def test_incrementer_matches_machine(n):
    m = incrementer()
    bits = [(n >> j) & 1 for j in range(n.bit_length())]
    steps, final = run_checked(m, bits, 400)
    carries = (n ^ (n + 1)).bit_length() - 1  # number of trailing one bits of n
    assert steps == 2 * carries + 1
    state, head_sym, cells = final
    assert state == 2
    # read the result from cell 0: the head ended at offset `carries`
    value = 0
    for j in range(0, carries + 1):
        off = j - carries
        s = head_sym if off == 0 else dict(cells).get(off, 0)
        value |= s << j
    for off, s in cells:
        if off > 0:
            value |= s << (off + carries)
    assert value == n + 1


def test_busy_beaver_2():
    m = busy_beaver_2()
    steps, final = run_checked(m, [], 100)
    assert steps == 12
    state, head_sym, cells = final
    assert state == 2
    ones = head_sym + sum(s for _, s in cells)
    assert ones == 4


def test_right_runner_needs_unbounded_blanks():
    m = right_runner()
    rules = rules_for(m)
    start = encode(m, 0, {}, 0)
    assert start == LEND + "A0" + REND
    for bound in range(len(start), 25):
        verdict, witness = decide_reach(rules, start, LEND + REND, bound)
        assert verdict == "bound_exceeded"
        assert len(witness[1]) == bound + 1
    seen, _ = bounded_reach(rules, start, 10)
    assert len(seen) == 7


def test_all_two_state_two_symbol_machines_step_simulation():
    """Exhaustive: 9^4 = 6561 machines, 20 steps from the blank tape (or until halting)."""
    count = 0
    halted = 0
    for m in all_two_state_machines():
        count += 1
        result = run_checked(m, [], 20)
        if result is not None:
            halted += 1
    assert count == 6561
    assert halted > 0


def test_genesis_events_and_uncapped_admission():
    r = replay(FIRST_SEPARATION)
    assert r == {"data": 2, "forms": [1], "insts": [(0, [0])], "rules": [], "reqs": [(0, 1)]}
    for k in (0, 1, 7, 300):
        assert replay([("admitDatum",)] * k)["data"] == k
    assert replay([("supply", 3), ("supply", 4)]) == {"data": 0, "forms": [], "insts": [], "rules": [], "reqs": []}
    assert step_e({"data": 0, "forms": [], "insts": [], "rules": [], "reqs": []}, ("admitForm", 0)) is None


@pytest.mark.parametrize("n", range(0, 4))
@pytest.mark.parametrize("a", range(1, 5))
def test_context_counts(n, a):
    total, one = context_counts(n, a)
    assert total == (n + 1) ** a - n ** a
    expected_one = a * n ** (a - 1) if n > 0 else (1 if a == 1 else 0)
    assert one == expected_one


@pytest.mark.parametrize("card", range(1, 10))
def test_binary_coding_roundtrip_and_injective(card):
    from itertools import product

    k = code_width(card)
    assert card < 2 ** k
    seen = set()
    for length in range(0, 4):
        for w in product(range(card), repeat=length):
            bits = encode_binary(card, w)
            assert len(bits) == k * length
            assert decode_binary(card, bits) == list(w)
            assert (length, bits) not in seen
            seen.add((length, bits))
    assert decode_binary(3, "11" + "0") is None


def test_machine_is_frozen_dataclass():
    m = Machine(1, 2, {})
    with pytest.raises(Exception):
        m.n_states = 3  # type: ignore[misc]


def test_separated_alphabets_and_collapse():
    for n in range(0, 9):
        assert pairwise_separated(canonical_regime(n)), n
    bare = {"data": 2, "forms": [], "insts": [], "rules": [], "reqs": []}
    assert collapsed(bare, 0, 1)
    first = replay(FIRST_SEPARATION)
    assert pairwise_separated(first)
    assert not collapsed(first, 0, 1)
