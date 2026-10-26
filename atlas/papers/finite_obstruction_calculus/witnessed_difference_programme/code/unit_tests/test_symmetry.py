from __future__ import annotations

import pytest
from witnessed_difference.symmetry import (
    all_permutations,
    all_relations,
    apply_permutation,
    carrier,
    exhaustive_relation_audit,
    fixed_oriented_edges,
    fixed_points,
    invariant_binary_relations,
    invariant_strict_total_orders,
    is_invariant,
    is_strict_total_order,
    relation_orbits,
    strict_order_from_sequence,
)


def test_three_label_exhaustive_counts() -> None:
    audit = exhaustive_relation_audit(3)
    assert audit["permutation_count"] == 6
    assert audit["relation_count"] == 512
    assert audit["invariant_relation_count"] == 4
    assert audit["invariant_strict_order_count"] == 0
    assert audit["authority_effect"] == "None"


def test_exact_four_relations_for_three_labels() -> None:
    diagonal = frozenset((x, x) for x in range(3))
    off_diagonal = frozenset((x, y) for x in range(3) for y in range(3) if x != y)
    assert set(invariant_binary_relations(3)) == {
        frozenset(), diagonal, off_diagonal, diagonal | off_diagonal
    }


@pytest.mark.parametrize("n", [2, 3, 4])
def test_pair_action_has_diagonal_and_off_diagonal_orbits(n: int) -> None:
    assert {len(orbit) for orbit in relation_orbits(n)} == {n, n * (n - 1)}


def test_empty_carrier_has_no_pair_orbit() -> None:
    assert relation_orbits(0) == ()
    assert tuple(all_relations(0)) == (frozenset(),)


def test_relabeling_preserves_every_invariant_relation() -> None:
    for relation in invariant_binary_relations(3):
        for permutation in all_permutations(3):
            assert apply_permutation(relation, permutation, 3) == relation


def test_chosen_order_is_destroyed_by_swap() -> None:
    order = strict_order_from_sequence((0, 1, 2))
    assert is_strict_total_order(order, 3)
    assert apply_permutation(order, (1, 0, 2), 3) != order
    assert not is_invariant(order, 3)


@pytest.mark.parametrize("n, expected", [(0, ()), (1, (0,)), (2, ()), (3, ())])
def test_fixed_point_boundary(n: int, expected: tuple[int, ...]) -> None:
    assert fixed_points(n) == expected


@pytest.mark.parametrize("n", [0, 1, 2, 3])
def test_no_fixed_oriented_edge(n: int) -> None:
    assert fixed_oriented_edges(n) == ()


def test_strict_order_boundary() -> None:
    assert len(invariant_strict_total_orders(0)) == 1
    assert len(invariant_strict_total_orders(1)) == 1
    assert invariant_strict_total_orders(2) == ()


@pytest.mark.parametrize("n", [-1, True, 1.5])
def test_invalid_carrier_size_is_rejected(n) -> None:
    with pytest.raises(ValueError, match="non-negative integer"):
        carrier(n)


def test_invalid_permutation_and_relation_are_rejected() -> None:
    with pytest.raises(ValueError, match="every carrier label"):
        apply_permutation({(0, 1)}, (0, 0), 2)
    with pytest.raises(ValueError, match="outside"):
        is_invariant({(0, 2)}, 2)


def test_exhaustive_budget_is_explicit() -> None:
    with pytest.raises(ValueError, match="limited"):
        tuple(all_relations(5))


def test_non_orders_are_rejected() -> None:
    assert not is_strict_total_order({(0, 0)}, 1)
    assert not is_strict_total_order(set(), 2)
    assert not is_strict_total_order({(0, 1), (1, 2), (2, 0)}, 3)
# Executable finite evidence; AuthorityEffect: None.
