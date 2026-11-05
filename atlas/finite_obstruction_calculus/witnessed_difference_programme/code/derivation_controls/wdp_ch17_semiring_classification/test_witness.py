"""Exact checks for the integer endpoint-block census."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest


def _load():
    path = Path(__file__).resolve().parent / "witness.py"
    spec = importlib.util.spec_from_file_location(
        "wdp_ch17_semiring_classification_witness", path
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("witness loader is missing")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _independent_one_block_count() -> int:
    count = 0
    for left_a in (-1, 0, 1):
        for left_b in (-1, 0, 1):
            left = left_a + left_b
            for right_a in (-1, 0, 1):
                for right_b in (-1, 0, 1):
                    if right_a + right_b == left:
                        count += 1
    return count


def _independent_square_count() -> int:
    counts = {total: 0 for total in (-2, -1, 0, 1, 2)}
    for left in (-1, 0, 1):
        for right in (-1, 0, 1):
            counts[left + right] += 1
    total = 0
    for count in counts.values():
        total += count * count
    return total


def _expected() -> dict[str, object]:
    return {
        "matrices": 81,
        "partitions_two": 2,
        "pairs": 162,
        "multiplicity": (1, 2, 3, 2, 1),
        "one_block_p1": 19,
        "one_block_p0": 9,
        "one_block_p1_not_p0": 10,
        "discrete_p1": 81,
        "p1_pairs": 100,
        "p1_fail_pairs": 62,
        "p0_pairs": 90,
        "p0_not_p1": 0,
        "census_through": 8,
        "census_powers_match": 1,
        "zerosumfree": 0,
        "ex1_p0": 0,
        "ex1_p1": 1,
        "ex1_p2": 0,
        "ex1_b": ((1, 3), (2, 1)),
        "ex1_row_sums": (4, 4, 3),
        "ex1_pm": ((2, 0, 6), (4, -2, 1)),
        "ex1_dual": 0,
        "ex1_b_unique": 1,
        "ex1_through": 12,
        "ex1_intertwines": 1,
        "ex2_two_block_p0": 0,
        "ex2_one_block_p0": 0,
        "ex2_block_p1": 0,
        "ex2_p2": 1,
        "ex2_b": ((2,),),
        "ex2_b_unique": 1,
        "ex2_through": 6,
        "ex2_sources": (1, 2, 4, 8, 16, 32, 64),
        "ex2_entry_sums": (3, 6, 12, 24, 48, 96, 192),
        "ex2_source_equals_entries": 0,
        "ex3_p0": 0,
        "ex3_p1": 1,
        "ex3_b": ((0,),),
        "ex3_b_unique": 1,
        "ex3_rows": ((1, -1), (0, 0)),
        "ex3_one_block_dual": 0,
        "ex3_length0_accepts_wrong_b": 1,
        "ex3_length1_rejects_wrong_b": 1,
        "ex4_two_block_p0": 0,
        "ex4_block_p1": 0,
        "ex4_one_block_p0": 0,
        "ex4_p2": 1,
        "ex4_b": ((0,),),
        "ex4_b_unique": 1,
        "ex4_length0": 1,
        "ex4_length1": 0,
        "ex4_edge_00": 1,
        "ex4_edge_10": 0,
        "ex4_through": 8,
        "ex4_intertwines": 1,
        "partitions_three": 5,
        "empty_partition_refused": 1,
        "general_semiring_classified": 0,
        "continuum_limit": 0,
        "infinite_sum": 0,
    }

def _assert_exact(value: object) -> None:
    if type(value) is int:
        return
    if type(value) is tuple:
        for item in value:
            _assert_exact(item)
        return
    if type(value) is dict:
        for item in value.values():
            _assert_exact(item)
        return
    raise AssertionError(f"non-exact value {type(value)}")


def test_witness_is_the_integer_endpoint_block_census() -> None:
    result = _load().witness()
    assert result == _expected()
    _assert_exact(result)
    assert result["matrices"] == 81
    assert result["pairs"] == result["matrices"] * result["partitions_two"]
    assert result["p1_pairs"] == result["discrete_p1"] + result["one_block_p1"]
    assert result["p1_fail_pairs"] == result["pairs"] - result["p1_pairs"]
    assert result["one_block_p1"] == _independent_one_block_count()
    assert result["one_block_p1"] == _independent_square_count()
    assert result["one_block_p0"] + result["one_block_p1_not_p0"] == result["one_block_p1"]
    assert result["p0_not_p1"] == 0
    sources = tuple(2**length for length in range(7))
    entries = tuple(3 * value for value in sources)
    assert result["ex2_sources"] == sources
    assert result["ex2_entry_sums"] == entries
    assert sources[6] != entries[6]
    assert result["ex2_source_equals_entries"] == 0
    assert (2 + (-1), 3) == result["ex1_b"][0]
    assert (4 + (-2), 1) == result["ex1_b"][1]
    assert len(set(result["ex1_row_sums"])) == 2
    assert result["ex1_row_sums"] == (4, 4, 3)
    pm = result["ex1_pm"]
    assert (pm[0][0], pm[1][0]) != (pm[0][1], pm[1][1])
    assert result["ex3_rows"][0][0] + result["ex3_rows"][0][1] == result["ex3_b"][0][0]
    assert result["ex3_rows"][0] != result["ex3_rows"][1]
    assert result["ex4_length0"] != result["ex4_length1"]
    assert result["ex4_edge_00"] != result["ex4_edge_10"]
    assert result["general_semiring_classified"] == 0
    assert result["continuum_limit"] == 0
    assert result["infinite_sum"] == 0
    assert _load().witness() == result


def test_two_block_failure_and_out_of_scope_refusal() -> None:
    module = _load()
    result = module.witness()
    ex1 = (
        (2, -1, 3),
        (0, 1, 3),
        (4, -2, 1),
    )
    ex2 = (
        (2, 0, 0),
        (0, 0, 2),
        (0, 0, 2),
    )
    ex3 = ((1, -1), (0, 0))
    assert module.quotient(ex1, ((0, 1), (2,))) == ((1, 3), (2, 1))
    assert module.dual_quotient(ex1, ((0, 1), (2,))) is None
    assert module.quotient(ex2, ((0, 1), (2,))) is None
    assert module.quotient(ex2, ((0, 1, 2),)) == ((2,),)
    assert module.quotient(ex3, ((0, 1),)) == ((0,),)
    assert module.dual_quotient(ex3, ((0, 1),)) is None
    assert len(module.classify(ex3)) == 2
    assert len(module.classify(ex2)) == result["partitions_three"]
    found = dict(module.classify(ex2))
    assert found[((0, 1), (2,))] is None
    assert found[((0, 1, 2),)] == ((2,),)
    with pytest.raises(ValueError, match="nonempty"):
        module.quotient(ex3, ())
    with pytest.raises(ValueError, match="general semiring"):
        module.refuse_general_semiring(result["p1_pairs"])
    with pytest.raises(ValueError, match="1D per-source"):
        module.refuse_source_as_entry_sum(
            result["ex2_sources"][6],
            result["ex2_entry_sums"][6],
            3,
        )
    with pytest.raises(ValueError, match="exact integer"):
        module.quotient(((1.0, 0.0), (0.0, 1.0)), ((0, 1),))
    with pytest.raises(ValueError, match="carrier"):
        module.classify(((0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0)))
    with pytest.raises(ValueError, match="continuum"):
        module.refuse_continuum()
    with pytest.raises(ValueError, match="infinite"):
        module.refuse_infinite_sum()
