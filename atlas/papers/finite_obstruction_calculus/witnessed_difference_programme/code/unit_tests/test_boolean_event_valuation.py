from itertools import product

import pytest
from witnessed_difference.finite_adequacy import BooleanEventValuation


def test_algebra_atoms_reconstruct_every_event_and_extensions() -> None:
    # The algebra distinguishes {0,1} from {2}, but cannot distinguish 0 from 1.
    for left, right in product(range(3), repeat=2):
        valuation = BooleanEventValuation(3, (0, 3, 4, 7), (0, left, right, left + right))
        assert valuation.atoms() == (3, 4)
        atomic = valuation.atomic_representation()
        for event, value in zip(valuation.events, valuation.values):
            assert atomic.event_mass(valuation.atom_event(event)) == value
            assert valuation.singleton_extension().event_mass(event) == value
            assert valuation.singleton_extension(True).event_mass(event) == value
        assert valuation.singleton_extension_is_unique() == (left == 0)
        assert (valuation.singleton_extension() == valuation.singleton_extension(True)) == (left == 0)


def test_full_algebra_and_empty_carrier_have_unique_representations() -> None:
    valuation = BooleanEventValuation(2, (0, 1, 2, 3), (0, 2, 3, 5))
    assert valuation.atoms() == (1, 2)
    assert valuation.singleton_extension_is_unique()
    empty = BooleanEventValuation(0, (0,), (0,))
    assert empty.atoms() == ()
    assert empty.atomic_representation().masses == ()
    assert empty.singleton_extension_is_unique()


@pytest.mark.parametrize("args", [
    (2, (0, 1, 3), (0, 1, 2)),  # Complement closure fails.
    (2, (0, 1, 2, 3), (0, 1, 2, 4)),  # Disjoint additivity fails.
    (2, (0, 3), (1, 2)),  # Empty event must have zero mass.
    (2, (0, 3), (0, -1)),
    (2, (0, 3, 3), (0, 1, 1)),
    (2, (0, 3), (0, 1.0)),
    (True, (0, 1), (0, 1)),
])
def test_missing_representation_hypotheses_are_rejected(args) -> None:
    with pytest.raises((TypeError, ValueError)):
        BooleanEventValuation(*args)


def test_nonmeasurable_singleton_is_not_an_event() -> None:
    valuation = BooleanEventValuation(2, (0, 3), (0, 1))
    with pytest.raises(ValueError, match="measurable"):
        valuation.atom_event(1)
