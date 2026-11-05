from itertools import product

import pytest
from witnessed_difference.finite_observer_adapter_completeness import (
    DescentError,
    Operation,
    Predicate,
    Structure,
    descend,
    verify,
)


def test_exhaustive_1296_partial_operation_and_relation_pairs():
    for values in product((None, 0, 1), repeat=4):
        for truth in product((False, True), repeat=4):
            s = Structure((4, 2), (Operation((0,), 1, values),), (Predicate((0,), truth),))
            expected = (
                values[0] == values[1]
                and values[2] == values[3]
                and truth[0] == truth[1]
                and truth[2] == truth[3]
            )
            try:
                target = descend(s, (2, 2), ((0, 0, 1, 1), (0, 1)))
            except DescentError:
                assert not expected
            else:
                assert expected
                verify(s, (2, 2), ((0, 0, 1, 1), (0, 1)), target)


def test_definedness_omission_empty_and_nullary_boundaries():
    s = Structure((2, 1), (Operation((0,), 1, (None, 0)),))
    with pytest.raises(DescentError, match="operation conflict"):
        descend(s, (1, 1), ((0, 0), (0,)))
    s = Structure((0, 1), (Operation((0,), 1, ()), Operation((), 1, (0,))))
    assert descend(s, (0, 1), ((), (0,))) == s
    assert descend(Structure((1,)), (1,), ((0,),)).operations == ()
    with pytest.raises(DescentError, match="invalid sort map"):
        descend(s, (0, 2), ((), (0,)))


def test_binary_context_operation_and_forged_output():
    s = Structure((2, 3), (Operation((0, 1), 1, (0, 0, 2, 2, 2, 2)),))
    target = descend(s, (2, 2), ((0, 1), (0, 0, 1)))
    assert target.operations[0].values == (0, 1, 1, 1)
    forged = Structure((2, 2), (Operation((0, 1), 1, (0, 1, 0, 1)),))
    with pytest.raises(DescentError, match="receipt mismatch"):
        verify(s, (2, 2), ((0, 1), (0, 0, 1)), forged)


def test_operation_with_none_output_sort_rejected():
    source = Structure(
        sizes=(1,),
        operations=(Operation(inputs=(0,), output=None, values=(True,)),),
    )
    with pytest.raises(DescentError, match="invalid operation output sort"):
        descend(source, (1,), ((0,),))

