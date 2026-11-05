from fractions import Fraction
from itertools import product as cartesian_product

import pytest
from semiring_coarse_graining import classify, membership, partitions, product, quotient


def test_signed_intertwining_preserves_all_checked_lengths():
    matrix = ((2, -1, 3), (0, 1, 3), (4, -2, 1))
    blocks = ((0, 1), (2,))
    reduced = quotient(matrix, blocks)
    assert reduced == ((Fraction(1), Fraction(3)), (Fraction(2), Fraction(1)))
    left = right = membership(3, blocks)
    for _ in range(12):
        assert left == right
        left = product(matrix, left)
        right = product(right, reduced)


def test_exhaustive_two_vertex_classification_and_length_one_necessity():
    assert len(tuple(partitions(4))) == 15
    for entries in cartesian_product((-1, 0, 1), repeat=4):
        matrix = (entries[:2], entries[2:])
        results = classify(matrix)
        assert len(results) == 2
        for blocks, reduced in results:
            h = membership(2, blocks)
            if reduced is not None:
                assert product(matrix, h) == product(h, reduced)
            else:
                # Only the one-block partition can fail for two vertices.
                assert blocks == ((0, 1),)
                assert sum(matrix[0]) != sum(matrix[1])


def test_equal_total_path_aggregate_does_not_preserve_endpoint_blocks():
    matrix = ((2, 0, 0), (0, 0, 2), (0, 0, 2))
    assert quotient(matrix, ((0, 1), (2,))) is None
    # All row totals, and hence all unrestricted length-n path sums, are 2^n.
    h = membership(3, ((0, 1, 2),))
    for n in range(7):
        assert h == ((Fraction(2 ** n),),) * 3
        h = product(matrix, h)


def test_signed_cancellation_preserves_blocks_without_preserving_paths():
    matrix = ((1, -1), (0, 0))
    assert quotient(matrix, ((0, 1),)) == ((Fraction(0),),)
    assert matrix[0] != matrix[1]


def test_empty_and_invalid_inputs():
    assert classify(()) == (((), ()),)
    for blocks in ((), ((0,), (0,)), ((1,),), ((), (0,))):
        with pytest.raises(ValueError):
            quotient(((1,),), blocks)
    with pytest.raises(TypeError):
        quotient(((0.5,),), ((0,),))
    with pytest.raises(TypeError):
        quotient(((True,),), ((0,),))
    with pytest.raises(ValueError):
        quotient(((1, 2),), ((0,),))
