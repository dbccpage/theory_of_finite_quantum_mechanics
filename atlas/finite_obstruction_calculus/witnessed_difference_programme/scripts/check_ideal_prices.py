"""Exact integer price test on the order ideals of an admitted event poset.

This checks the price layer of Appendix P.15. It does not admit Source-25
edits or verify that every event schedule is legal; P.14 supplies that premise.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping, Sequence


Vector = tuple[int, ...]
Edge = tuple[int, int]  # (order-ideal bitmask, newly executed event)


@dataclass(frozen=True)
class ExactPrices:
    potential: dict[int, Vector]


@dataclass(frozen=True)
class CurlWitness:
    ideal: int
    first: int
    second: int
    first_route: Vector
    second_route: Vector
    first_order: tuple[int, ...]
    second_order: tuple[int, ...]
    first_total: Vector
    second_total: Vector


def _sum(a: Vector, b: Vector) -> Vector:
    return tuple(x + y for x, y in zip(a, b))


def _extension(predecessors: tuple[int, ...], start: int, target: int) -> tuple[int, ...]:
    """Lexicographic legal continuation from one ideal to a larger ideal."""
    current = start
    order: list[int] = []
    while current != target:
        available = [
            e for e, before in enumerate(predecessors)
            if target & (1 << e) and not current & (1 << e) and before & ~current == 0
        ]
        if not available:
            raise ValueError("predecessors contain a cycle or target is not an ideal")
        e = available[0]
        order.append(e)
        current |= 1 << e
    return tuple(order)


def analyze_prices(
    predecessors: Sequence[int], weights: Mapping[Edge, Sequence[int]]
) -> ExactPrices | CurlWitness:
    """Return an integer potential, or two complete runs witnessing nonzero curl.

    `predecessors[e]` is a bitmask of required prior events. `weights[(J,e)]`
    is the integer-vector edge price. Every edge of the full ideal lattice
    must have one price; missing/extra edges and cyclic inputs are invalid.
    """
    before = tuple(predecessors)
    n = len(before)
    if n > 20:
        raise ValueError("resource cap: at most 20 events in this enumerating checker")
    full = (1 << n) - 1
    if any(type(p) is not int or p < 0 or p & ~full or p & (1 << e)
           for e, p in enumerate(before)):
        raise ValueError("invalid predecessor mask")
    _extension(before, 0, full)  # Refuse cycles before constructing an ideal lattice.

    ideals = [
        j for j in range(1 << n)
        if all(not j & (1 << e) or p & ~j == 0 for e, p in enumerate(before))
    ]
    edges = {
        (j, e) for j in ideals for e, p in enumerate(before)
        if not j & (1 << e) and p & ~j == 0
    }
    if any(type(edge) is not tuple or len(edge) != 2
           or any(type(index) is not int for index in edge) for edge in weights):
        raise ValueError("edge identifiers must be pairs of integers")
    if set(weights) != edges:
        missing, extra = edges - set(weights), set(weights) - edges
        raise ValueError(f"edge domain mismatch: missing={sorted(missing)}, extra={sorted(extra)}")
    values: dict[Edge, Vector] = {}
    dimension: int | None = None
    for edge in sorted(edges):
        value = tuple(weights[edge])
        if not value or any(type(x) is not int for x in value):
            raise ValueError(f"edge {edge} needs a nonempty integer vector")
        if dimension is None:
            dimension = len(value)
        elif len(value) != dimension:
            raise ValueError("edge price dimensions differ")
        values[edge] = value
    zero = (0,) * (dimension or 0)

    def total(order: tuple[int, ...]) -> Vector:
        j, price = 0, zero
        for e in order:
            if (j, e) not in values:
                raise AssertionError("constructed an inadmissible schedule")
            price = _sum(price, values[(j, e)])
            j |= 1 << e
        if j != full:
            raise AssertionError("constructed an incomplete schedule")
        return price

    for j in ideals:
        available = [e for e in range(n) if (j, e) in edges]
        for i, e in enumerate(available):
            for f in available[i + 1:]:
                after = j | (1 << e) | (1 << f)
                ef = _sum(values[(j, e)], values[(j | (1 << e), f)])
                fe = _sum(values[(j, f)], values[(j | (1 << f), e)])
                if ef != fe:
                    prefix = _extension(before, 0, j)
                    suffix = _extension(before, after, full)
                    first = prefix + (e, f) + suffix
                    second = prefix + (f, e) + suffix
                    return CurlWitness(j, e, f, ef, fe, first, second,
                                       total(first), total(second))

    potential: dict[int, Vector] = {0: zero}
    for j in sorted(ideals, key=lambda ideal: (ideal.bit_count(), ideal)):
        for e in range(n):
            if (j, e) not in edges:
                continue
            target = j | (1 << e)
            candidate = _sum(potential[j], values[(j, e)])
            if target in potential and potential[target] != candidate:
                raise AssertionError("zero square curls gave inconsistent potential")
            potential[target] = candidate
    if len(potential) != len(ideals):
        raise AssertionError("potential did not reach every ideal")
    return ExactPrices(potential)


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
        epilog='Input: {"predecessors":[0,0],"weights":'
               '[{"ideal":0,"event":0,"value":[1]}, ...]}; '
               'supply exactly one entry for every ideal cover.',
    )
    parser.add_argument("input", type=Path, help="JSON with predecessors and edge weights")
    args = parser.parse_args()
    payload = strict_json(args.input.read_text(encoding="utf-8"))
    weights: dict[Edge, Vector] = {}
    for item in payload["weights"]:
        edge = (item["ideal"], item["event"])
        if edge in weights:
            raise ValueError(f"duplicate edge {edge}")
        weights[edge] = tuple(item["value"])
    result = analyze_prices(payload["predecessors"], weights)
    if isinstance(result, ExactPrices):
        report = {"status": "EXACT", "potential": {str(j): v for j, v in result.potential.items()}}
    else:
        report = {"status": "CURL", **result.__dict__}
    print(json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    main()
