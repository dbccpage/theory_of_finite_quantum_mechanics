"""Independent finite characterizations of the distinct word contracts."""
import itertools
import sys
from collections import Counter
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from preservation import (
    decimal_decode,
    decimal_encode,
    erase_word,
    protocol,
    recover_word,
    rename_word,
    reverse_trace,
)


def words(alphabet, length):
    return ("".join(word) for size in range(length+1)
            for word in itertools.product(alphabet, repeat=size))


def test_fixed_width_encoding_roundtrip_length_and_injectivity():
    population = list(words("0123456789", 4))
    encoded = [decimal_encode(word) for word in population]
    assert len(set(encoded)) == len(population)
    for word, bits in zip(population, encoded, strict=True):
        assert decimal_decode(bits) == word
        assert len(bits) == 4 * len(word)
    for x, y in itertools.product(words("019", 2), repeat=2):
        assert decimal_encode(x+y) == decimal_encode(x)+decimal_encode(y)


def test_decoder_domain_is_exactly_complete_decimal_nibbles():
    for bits in words("01", 8):
        belongs = len(bits) % 4 == 0 and all(int(bits[i:i+4], 2) < 10 for i in range(0, len(bits), 4))
        if belongs:
            assert decimal_encode(decimal_decode(bits)) == bits
        else:
            with pytest.raises(ValueError):
                decimal_decode(bits)
    for word in ("a", "١", "+1", " 0"):
        with pytest.raises(ValueError):
            decimal_encode(word)
    assert decimal_encode("0") != decimal_encode("00")


def test_typed_recovery_and_total_erasure_have_different_domains():
    for word in words("abc", 6):
        recovered = recover_word(word)
        assert (recovered is not None) == ("c" not in word)
        assert erase_word(word) == word.replace("c", "")
        if recovered is not None:
            assert recovered == erase_word(word) == word
    for x, y in itertools.product(words("abc", 3), repeat=2):
        assert erase_word(x+y) == erase_word(x)+erase_word(y)
    assert protocol("v1\trecover\tacb") == "NON_DESCENT"
    assert protocol("v1\terase\tacb") == "ab"


def test_renaming_inverse_characterization_by_all_small_maps():
    for n, m in itertools.product(range(4), repeat=2):
        for mapping in itertools.product(range(m), repeat=n):
            injective = len(set(mapping)) == n
            surjective = set(mapping) == set(range(m))
            inverse_exists = any(
                all(inverse[mapping[a]] == a for a in range(n)) and
                all(mapping[inverse[b]] == b for b in range(m))
                for inverse in itertools.product(range(n), repeat=m))
            assert inverse_exists == (injective and surjective)
            for source in itertools.product(range(n), repeat=2):
                renamed = rename_word(mapping, source)
                if injective:
                    image_inverse = {mapping[a]: a for a in range(n)}
                    assert tuple(image_inverse[b] for b in renamed) == source
    with pytest.raises(ValueError):
        rename_word([0, 1], [-1])


def test_arrow_and_traversal_reversal_preserves_directed_edge_multiset():
    possible = list(itertools.product((-1, 0, 1), (False, True), (-1, 0, 1)))
    for trace in itertools.product(possible, repeat=2):
        reversed_edges = reverse_trace(trace)
        assert reverse_trace(reversed_edges) == trace
        old = [(a, b) if direction else (b, a) for a, direction, b in trace]
        new = [(a, b) if direction else (b, a) for a, direction, b in reversed_edges]
        assert new == old[::-1]
        assert Counter(new) == Counter(old)


@pytest.mark.parametrize("record", ["v1\tdecimal\t١", "v1\tdecimal\t"+"0"*17,
    "v1\tdecimal_decode\t0", "v1\tdecimal_decode\t1010", "v1\tdecimal_decode\t0020",
    "v1\tdecimal_decode\t"+"0"*65, "v1\trecover\td", "v1\terase\t"+"a"*65,
    "v1\trename\t1,2\t2", "v1\trename\t1,2\t-1", "v1\ttrace\t0,2,1",
    "v1\ttrace\t0,1", "v1\ttrace\t0,01,1"])
def test_word_protocol_refuses_undeclared_or_out_of_budget_inputs(record):
    assert protocol(record) == "REFUSE"
