"""Independent BFS and replay controls for Appendix P.16 swap receipts."""

from __future__ import annotations

from collections import deque
from itertools import permutations

from scripts.check_ideal_swaps import minimum_swap_receipt


def _valid(order, before, start=0):
    done = start
    for event in order:
        if before[event] & ~done:
            return False
        done |= 1 << event
    return True


def _shortest_distance(source, target, before):
    queue = deque([(source, 0)])
    seen = {source}
    while queue:
        current, depth = queue.popleft()
        if current == target:
            return depth
        for k in range(len(current) - 1):
            neighbor = current[:k] + (current[k + 1], current[k]) + current[k + 2:]
            if neighbor not in seen and _valid(neighbor, before):
                seen.add(neighbor)
                queue.append((neighbor, depth + 1))
    raise AssertionError("linear-extension graph was disconnected")


def _replay(receipt, before):
    current = list(receipt.source)
    assert _valid(current, before, receipt.start_ideal)
    for swap in receipt.swaps:
        k = swap.position
        assert (current[k], current[k + 1]) == (swap.left, swap.right)
        ideal = receipt.start_ideal
        for event in current[:k]:
            ideal |= 1 << event
        assert ideal == swap.ideal
        assert before[swap.left] & ~ideal == 0
        assert before[swap.right] & ~ideal == 0
        current[k], current[k + 1] = current[k + 1], current[k]
        assert _valid(current, before, receipt.start_ideal)
    assert tuple(current) == receipt.target
    assert len(receipt.swaps) == receipt.inversion_count


def test_all_four_event_forward_dags_against_independent_bfs():
    pairs = tuple((i, j) for i in range(4) for j in range(i + 1, 4))
    for graph in range(1 << len(pairs)):
        before = [0] * 4
        for k, (i, j) in enumerate(pairs):
            if graph & (1 << k):
                before[j] |= 1 << i
        predecessor_masks = tuple(before)
        extensions = tuple(
            order for order in permutations(range(4)) if _valid(order, predecessor_masks)
        )
        for source, target in ((extensions[0], extensions[-1]),
                               (extensions[len(extensions) // 2], extensions[0])):
            receipt = minimum_swap_receipt(predecessor_masks, 0, 15, source, target)
            _replay(receipt, predecessor_masks)
            assert receipt.inversion_count == _shortest_distance(
                source, target, predecessor_masks
            )


def test_nonempty_start_ideal_and_three_free_events():
    interval = minimum_swap_receipt((0, 0, 1), 1, 7, (1, 2), (2, 1))
    assert interval.inversion_count == 1
    _replay(interval, (0, 0, 1))
    free = minimum_swap_receipt((0, 0, 0), 0, 7, (0, 1, 2), (2, 1, 0))
    assert free.inversion_count == 3
    _replay(free, (0, 0, 0))


def test_invalid_boundary_and_precedence_are_refused():
    cases = (
        ((0, 1), 0, 3, (1, 0), (0, 1), "source executes event"),
        ((0, 0), 1, 3, (0,), (1,), "not a permutation"),
        ((2, 1), 0, 3, (0, 1), (1, 0), "cycle"),
    )
    for args in cases:
        *parameters, expected = args
        try:
            minimum_swap_receipt(*parameters)
        except ValueError as error:
            assert expected in str(error)
        else:
            raise AssertionError(f"accepted invalid schedule: {expected}")


if __name__ == "__main__":
    test_all_four_event_forward_dags_against_independent_bfs()
    test_nonempty_start_ideal_and_three_free_events()
    test_invalid_boundary_and_precedence_are_refused()
    print("ideal-swap independent BFS checks passed")
