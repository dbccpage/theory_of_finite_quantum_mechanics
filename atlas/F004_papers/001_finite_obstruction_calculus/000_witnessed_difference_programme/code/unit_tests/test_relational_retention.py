from itertools import permutations

import pytest
from witnessed_difference.relational_retention import (
    BisimulationReceipt,
    RelationalModel,
    behavioral_quotient,
    bounded_traces,
    greatest_bisimulation,
    is_bisimulation,
    relation_of_partition,
    succession_classification,
    verify_bisimulation_receipt,
)


def graph_model(n: int, report_bits: int, edges: int) -> RelationalModel:
    return RelationalModel(
        tuple((report_bits >> x) & 1 for x in range(n)),
        tuple((frozenset(y for y in range(n) if edges & (1 << (n * x + y))),) for x in range(n)),
    )


def test_exhaustive_three_state_partition_and_succession_classification():
    partitions = ((0, 0, 0), (0, 0, 1), (0, 1, 0), (0, 1, 1), (0, 1, 2))
    for report_bits in range(8):
        for edges in range(512):
            model = graph_model(3, report_bits, edges)
            receipt = greatest_bisimulation(model)
            stable = receipt.relations[-1]
            assert stable == relation_of_partition(receipt.partition)
            assert is_bisimulation(model, stable)
            assert len(receipt.relations) <= 3
            for partition in partitions:
                candidate = relation_of_partition(partition)
                if is_bisimulation(model, candidate):
                    assert candidate <= stable
            succession = succession_classification(model)
            order = succession.component_strict_order
            assert all(x != y for x, y in order)
            assert all((x, z) in order for x, y in order for b, z in order if y == b)
            assert (
                succession.acyclic
                == succession_classification(behavioral_quotient(model, receipt)).acyclic
            )


def test_exhaustive_arbitrary_two_state_bisimulations_not_only_partitions():
    for report_bits in range(4):
        for edges in range(16):
            model = graph_model(2, report_bits, edges)
            greatest = greatest_bisimulation(model).relations[-1]
            union = frozenset()
            for pair_bits in range(16):
                candidate = frozenset(
                    (x, y) for x in range(2) for y in range(2) if pair_bits & (1 << (2 * x + y))
                )
                if is_bisimulation(model, candidate):
                    assert candidate <= greatest
                    union |= candidate
            assert union == greatest


def test_trace_agreement_does_not_imply_strong_bisimilarity():
    # p --a--> r with both b,c choices; q --a--> s or t with separate choices.
    # Every branch ends after the second edge, so depth two includes all traces.
    model = RelationalModel(
        (0,) * 6,
        (
            (frozenset({2}), frozenset(), frozenset()),
            (frozenset({3, 4}), frozenset(), frozenset()),
            (frozenset(), frozenset({5}), frozenset({5})),
            (frozenset(), frozenset({5}), frozenset()),
            (frozenset(), frozenset(), frozenset({5})),
            (frozenset(), frozenset(), frozenset()),
        ),
    )
    assert bounded_traces(model, 0, 2) == bounded_traces(model, 1, 2)
    assert greatest_bisimulation(model).partition[0] != greatest_bisimulation(model).partition[1]


def test_relabelling_is_not_a_constitutive_order():
    model = graph_model(3, 0, (1 << 1) | (1 << 2))
    original = greatest_bisimulation(model).relations[-1]
    reach = succession_classification(model).nonempty_reachability
    assert (1, 2) not in reach and (2, 1) not in reach
    for permutation in permutations(range(3)):
        inverse = tuple(permutation.index(x) for x in range(3))
        renamed = RelationalModel(
            tuple(model.reports[inverse[x]] for x in range(3)),
            tuple(
                tuple(
                    frozenset(permutation[y] for y in targets)
                    for targets in model.successors[inverse[x]]
                )
                for x in range(3)
            ),
        )
        expected = frozenset((permutation[x], permutation[y]) for x, y in original)
        assert greatest_bisimulation(renamed).relations[-1] == expected
        assert succession_classification(renamed).nonempty_reachability == frozenset(
            (permutation[x], permutation[y]) for x, y in reach
        )


def test_cycles_change_carrier_and_do_not_supply_raw_strict_succession():
    model = graph_model(3, 0, (1 << 1) | (1 << 3) | (1 << 5))
    result = succession_classification(model)
    assert not result.acyclic
    assert result.state_to_component == (0, 0, 1)
    assert result.component_strict_order == frozenset({(0, 1)})


def test_receipt_rejects_stable_overrefinement_and_tampering():
    model = graph_model(2, 0, 0)
    forged = BisimulationReceipt((relation_of_partition((0, 1)),), (0, 1))
    assert is_bisimulation(model, forged.relations[-1])
    assert not verify_bisimulation_receipt(model, forged)
    with pytest.raises(ValueError):
        behavioral_quotient(model, forged)


@pytest.mark.parametrize(
    "reports,successors",
    [
        ((), ()),
        ((True,), ((frozenset(),),)),
        ((0,), ((frozenset({True}),),)),
        ((0,), ((frozenset({1}),),)),
        ((0, 0), ((frozenset(),), ())),
    ],
)
def test_invalid_finite_data_fail_closed(reports, successors):
    with pytest.raises(ValueError):
        RelationalModel(reports, successors)


def test_empty_alphabet_retains_report_equivalence_only():
    model = RelationalModel((0, 1, 0), ((), (), ()))
    assert greatest_bisimulation(model).partition == (0, 1, 0)
    assert succession_classification(model).component_strict_order == frozenset()
