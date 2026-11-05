"""Finite falsification of signed-word reduction, with independent relations."""
import itertools
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from preservation import free_reduce, protocol  # noqa: E402


def slow_reduce(word: str) -> str:
    """Repeated leftmost deletion, independent of the stack implementation."""
    for i in range(len(word)-1):
        if word[i] == word[i+1].swapcase():
            return slow_reduce(word[:i]+word[i+2:])
    return word


def test_exhaustive_reduction_and_abelian_coordinates():
    for size in range(9):
        for letters in itertools.product("abAB", repeat=size):
            word = "".join(letters)
            reduced = free_reduce(word)
            assert reduced == slow_reduce(word)
            assert free_reduce(reduced) == reduced
            assert len(reduced) <= len(word)
            assert (len(word)-len(reduced)) % 2 == 0
            for positive, negative in (("a", "A"), ("b", "B")):
                assert reduced.count(positive)-reduced.count(negative) == (
                    word.count(positive)-word.count(negative))


def test_local_relations_in_arbitrary_small_contexts():
    contexts = ["".join(w) for n in range(4) for w in itertools.product("abAB", repeat=n)]
    for left, right in itertools.product(contexts, repeat=2):
        for letter in "abAB":
            assert free_reduce(left+letter+letter.swapcase()+right) == free_reduce(left+right)


def test_inverse_and_commutator():
    for n in range(7):
        for letters in itertools.product("abAB", repeat=n):
            word = "".join(letters)
            inverse = word.swapcase()[::-1]
            assert free_reduce(word+inverse) == ""
    assert free_reduce("abAB") == "abAB"
    assert free_reduce("abBA") == ""
    assert free_reduce("ab") != free_reduce("ba")


@pytest.mark.parametrize("word", ["c", "á", "a"*65, "a\tb"])
def test_protocol_refuses_outside_declared_domain(word):
    assert protocol("v1\tfreeword\t"+word) == "REFUSE"
