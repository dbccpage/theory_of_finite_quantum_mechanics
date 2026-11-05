"""Independent schedule enumeration for Appendix P.15's integer checker."""

from __future__ import annotations

from itertools import permutations

from scripts.check_ideal_prices import CurlWitness, ExactPrices, analyze_prices


def _edges(predecessors: tuple[int, ...]):
    n = len(predecessors)
    for mask in range(1 << n):
        if any(mask & (1 << e) and before & ~mask for e, before in enumerate(predecessors)):
            continue
        for e, before in enumerate(predecessors):
            if not mask & (1 << e) and not before & ~mask:
                yield mask, e


def _schedule_totals(predecessors: tuple[int, ...], weights):
    totals = {}
    for order in permutations(range(len(predecessors))):
        mask, price = 0, 0
        for e in order:
            if predecessors[e] & ~mask:
                break
            price += weights[(mask, e)][0]
            mask |= 1 << e
        else:
            totals[order] = price
    return totals


def test_native_addition_pair_is_exact_on_two_independent_edits():
    weights = {
        (0, 0): (1, 0), (0, 1): (0, 1),
        (1, 1): (0, 1), (2, 0): (1, 0),
    }
    result = analyze_prices((0, 0), weights)
    assert isinstance(result, ExactPrices)
    assert result.potential == {0: (0, 0), 1: (1, 0), 2: (0, 1), 3: (1, 1)}


def test_state_dependent_assertion_fee_has_replayable_two_schedule_witness():
    # Initial carrier has one term and zero counts. Event 0 adds a term;
    # event 1 adds an assertion on the original loop. The source size before
    # the assertion is 1 or 2 depending on the schedule.
    weights = {
        (0, 0): (0,), (0, 1): (1,),
        (1, 1): (2,), (2, 0): (0,),
    }
    result = analyze_prices((0, 0), weights)
    assert isinstance(result, CurlWitness)
    assert result.ideal == 0
    assert (result.first_order, result.second_order) == ((0, 1), (1, 0))
    assert (result.first_total, result.second_total) == ((2,), (1,))


def test_all_four_event_forward_dags_against_independent_full_schedule_sums():
    # Every subset of the six possible forward edges gives a DAG. The oracle
    # enumerates actual topological schedules; it does not inspect curls.
    pairs = tuple((i, j) for i in range(4) for j in range(i + 1, 4))
    for graph in range(1 << len(pairs)):
        before = [0] * 4
        for k, (i, j) in enumerate(pairs):
            if graph & (1 << k):
                before[j] |= 1 << i
        predecessor_masks = tuple(before)
        for salt in range(4):
            weights = {
                edge: (((edge[0] * 7 + edge[1] * 3 + salt * 5) % 9) - 4,)
                for edge in _edges(predecessor_masks)
            }
            totals = _schedule_totals(predecessor_masks, weights)
            result = analyze_prices(predecessor_masks, weights)
            if len(set(totals.values())) == 1:
                assert isinstance(result, ExactPrices)
                assert result.potential[15] == (next(iter(totals.values())),)
            else:
                assert isinstance(result, CurlWitness)
                assert result.first_order in totals and result.second_order in totals
                assert totals[result.first_order] == result.first_total[0]
                assert totals[result.second_order] == result.second_total[0]
                assert result.first_total != result.second_total


def test_malformed_edge_domain_and_cycles_are_refused():
    for expected, before, weights in (
        ("edge domain mismatch", (0, 0), {(0, 0): (1,)}),
        ("cycle", (2, 1), {}),
    ):
        try:
            analyze_prices(before, weights)
        except ValueError as error:
            assert expected in str(error)
        else:
            raise AssertionError(f"accepted malformed input: {expected}")


if __name__ == "__main__":
    test_native_addition_pair_is_exact_on_two_independent_edits()
    test_state_dependent_assertion_fee_has_replayable_two_schedule_witness()
    test_all_four_event_forward_dags_against_independent_full_schedule_sums()
    test_malformed_edge_domain_and_cycles_are_refused()
    print("ideal-price independent schedule checks passed")
