"""Minimum adjacent-swap receipt for two admitted causal event schedules.

This checks the poset layer of Appendix P.16. The caller must separately
establish P.14's all-order native Source-25 admission criterion.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence


@dataclass(frozen=True)
class Swap:
    ideal: int
    left: int
    right: int
    position: int


@dataclass(frozen=True)
class SwapReceipt:
    start_ideal: int
    end_ideal: int
    source: tuple[int, ...]
    target: tuple[int, ...]
    inversion_count: int
    swaps: tuple[Swap, ...]


def _validate_poset(predecessors: tuple[int, ...]) -> None:
    n = len(predecessors)
    if n > 20:
        raise ValueError("resource cap: at most 20 events")
    full = (1 << n) - 1
    for e, before in enumerate(predecessors):
        if type(before) is not int or before < 0 or before & ~full or before & (1 << e):
            raise ValueError("invalid predecessor mask")
    reached = 0
    while reached != full:
        choices = [
            e for e, before in enumerate(predecessors)
            if not reached & (1 << e) and before & ~reached == 0
        ]
        if not choices:
            raise ValueError("predecessors contain a cycle")
        reached |= 1 << choices[0]


def _validate_order(
    label: str, order: tuple[int, ...], before: tuple[int, ...], start: int, end: int
) -> None:
    if any(type(event) is not int for event in order):
        raise ValueError(f"{label} needs integer event identifiers")
    remaining = end & ~start
    if len(order) != remaining.bit_count() or set(order) != {
        e for e in range(len(before)) if remaining & (1 << e)
    }:
        raise ValueError(f"{label} is not a permutation of the interval events")
    current = start
    for e in order:
        if before[e] & ~current:
            raise ValueError(f"{label} executes event {e} before its predecessors")
        current |= 1 << e
    if current != end:
        raise AssertionError("validated interval order missed its endpoint")


def minimum_swap_receipt(
    predecessors: Sequence[int], start_ideal: int, end_ideal: int,
    source: Sequence[int], target: Sequence[int],
) -> SwapReceipt:
    """Construct a shortest swap path and give each diamond's prefix ideal."""
    before = tuple(predecessors)
    _validate_poset(before)
    full = (1 << len(before)) - 1
    if any(type(x) is not int or x < 0 or x & ~full for x in (start_ideal, end_ideal)):
        raise ValueError("invalid ideal bitmask")
    if start_ideal & ~end_ideal:
        raise ValueError("start ideal is not contained in end ideal")
    for name, ideal in (("start", start_ideal), ("end", end_ideal)):
        if any(ideal & (1 << e) and required & ~ideal
               for e, required in enumerate(before)):
            raise ValueError(f"{name} is not an order ideal")
    first, last = tuple(source), tuple(target)
    _validate_order("source", first, before, start_ideal, end_ideal)
    _validate_order("target", last, before, start_ideal, end_ideal)

    rank = {event: i for i, event in enumerate(last)}
    inversions = sum(
        rank[first[i]] > rank[first[j]]
        for i in range(len(first)) for j in range(i + 1, len(first))
    )
    current = list(first)
    swaps: list[Swap] = []
    for i, wanted in enumerate(last):
        position = current.index(wanted)
        while position > i:
            k = position - 1
            left, right = current[k], current[position]
            ideal = start_ideal
            for event in current[:k]:
                ideal |= 1 << event
            if (before[left] & ~ideal) or (before[right] & ~ideal):
                raise AssertionError("adjacent swap did not form an available-event diamond")
            swaps.append(Swap(ideal, left, right, k))
            current[k], current[position] = current[position], current[k]
            position = k
    if tuple(current) != last or len(swaps) != inversions:
        raise AssertionError("bubble certificate failed its inversion bound")
    return SwapReceipt(start_ideal, end_ideal, first, last, inversions, tuple(swaps))


def strict_json(text: str):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate JSON key: {key}")
            result[key] = value
        return result

    def refuse_number(value):
        raise ValueError(f"expected integer JSON number: {value}")

    return json.loads(text, object_pairs_hook=unique,
                      parse_float=refuse_number, parse_constant=refuse_number)


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__,
        epilog='Input: {"predecessors":[0,0],"start_ideal":0,'
               '"end_ideal":3,"source":[0,1],"target":[1,0]}.',
    )
    parser.add_argument("input", type=Path, help="JSON causal schedule pair")
    args = parser.parse_args()
    payload = strict_json(args.input.read_text(encoding="utf-8"))
    result = minimum_swap_receipt(
        payload["predecessors"], payload["start_ideal"], payload["end_ideal"],
        payload["source"], payload["target"],
    )
    print(json.dumps({
        "status": "SWAP_RECEIPT",
        "start_ideal": result.start_ideal,
        "end_ideal": result.end_ideal,
        "source": result.source,
        "target": result.target,
        "inversion_count": result.inversion_count,
        "swaps": [swap.__dict__ for swap in result.swaps],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
