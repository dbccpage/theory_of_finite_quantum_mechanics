"""Exact finite obstruction to {0,1}-valued frame functions on Q(i)^3.

No repository imports or external solvers. All vectors used are in Z^3, so
the obstruction also rules out colourings of all rational real rays. This
does not classify arbitrary signed or nonnegative rational frame functions.
Run: python -I -X utf8 checks/independent/fq-gleason-qi3-frame-functions.py
"""
from __future__ import annotations

import itertools
import json
import math

Vector = tuple[int, int, int]
Pair = tuple[int, int]
Triple = tuple[int, int, int]


def dot(u: Vector, v: Vector) -> int:
    return sum(a * b for a, b in zip(u, v))


def cross(u: Vector, v: Vector) -> Vector:
    return (
        u[1] * v[2] - u[2] * v[1],
        u[2] * v[0] - u[0] * v[2],
        u[0] * v[1] - u[1] * v[0],
    )


def witness() -> tuple[list[Vector], list[Pair], list[Triple]]:
    """All primitive real integer rays in the radius-two box, once each."""
    rays = [
        v for v in itertools.product(range(-2, 3), repeat=3)
        if math.gcd(*v) == 1 and next(x for x in v if x) > 0
    ]
    pairs = [
        (i, j) for i, j in itertools.combinations(range(len(rays)), 2)
        if dot(rays[i], rays[j]) == 0
    ]
    edge_set = set(pairs)
    triples = [
        (i, j, k)
        for i, j, k in itertools.combinations(range(len(rays)), 3)
        if {(i, j), (i, k), (j, k)} <= edge_set
    ]
    return rays, pairs, triples


def satisfying_assignment(
    size: int, pairs: list[Pair], triples: list[Triple]
) -> tuple[dict[int, int] | None, int]:
    """Complete binary search, with exact unit propagation; no search cutoff.

    Pairs impose c_i+c_j <= 1. Triples impose c_i+c_j+c_k = 1.
    Each recursion assigns one previously unassigned binary variable, so
    termination and coverage of all assignments are immediate.
    """
    neighbours = [set() for _ in range(size)]
    for i, j in pairs:
        neighbours[i].add(j)
        neighbours[j].add(i)
    nodes = 0

    def search(values: dict[int, int]) -> dict[int, int] | None:
        nonlocal nodes
        nodes += 1
        while True:
            changed = False
            for i, value in list(values.items()):
                if value == 1:
                    for j in sorted(neighbours[i]):
                        if values.get(j) == 1:
                            return None
                        if j not in values:
                            values[j] = 0
                            changed = True
            for triple in triples:
                total = sum(values.get(i, 0) for i in triple)
                missing = [i for i in triple if i not in values]
                if total > 1 or (not missing and total != 1):
                    return None
                if total == 1 or len(missing) == 1:
                    for i in missing:
                        values[i] = 1 - total
                        changed = True
            if not changed:
                break
        if len(values) == size:
            return values
        variable = max(
            (i for i in range(size) if i not in values),
            key=lambda i: len(neighbours[i]),
        )
        for value in (0, 1):
            result = search(values | {variable: value})
            if result is not None:
                return result
        return None

    return search({}), nodes


def check_assignment(
    values: dict[int, int], size: int, pairs: list[Pair], triples: list[Triple]
) -> bool:
    """Separate direct verification of a returned SAT control assignment."""
    return (
        set(values) == set(range(size))
        and all(type(v) is int and v in (0, 1) for v in values.values())
        and all(values[i] + values[j] <= 1 for i, j in pairs)
        and all(sum(values[i] for i in t) == 1 for t in triples)
    )


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def main() -> None:
    rays, pairs, triples = witness()
    require((len(rays), len(pairs), len(triples)) == (49, 138, 26),
            "Unexpected witness census")
    # Every pair inequality is a consequence of an actual frame equation:
    # w=u cross v is a nonzero integer vector perpendicular to both, and
    # c(w)>=0 implies c(u)+c(v)<=1. No closure of the box is presumed.
    outside = 0
    for i, j in pairs:
        u, v = rays[i], rays[j]
        w = cross(u, v)
        require(w != (0, 0, 0), "Degenerate completion")
        require(dot(u, v) == dot(u, w) == dot(v, w) == 0,
                "Nonorthogonal completion")
        outside += int(max(map(abs, w)) > 2)
    result, nodes = satisfying_assignment(len(rays), pairs, triples)
    require(result is None, "Obstruction unexpectedly has a binary colouring")

    # Negative control: keeping internal triples but forgetting completions
    # must NOT prove an obstruction. Check the returned model independently.
    triples_only, _ = satisfying_assignment(len(rays), [], triples)
    require(triples_only is not None, "Triple-only negative control failed")
    require(check_assignment(triples_only, len(rays), [], triples),
            "Invalid triple-only control model")
    # Without frame normalization, the all-zero assignment satisfies pairs.
    pairs_only, _ = satisfying_assignment(len(rays), pairs, [])
    require(pairs_only is not None, "Pair-only negative control failed")
    require(check_assignment(pairs_only, len(rays), pairs, []),
            "Invalid pair-only control model")
    # A small independently enumerable instance checks both solver outcomes.
    for size in (3, 4):
        small_pairs = list(itertools.combinations(range(size), 2))
        small_triples = list(itertools.combinations(range(size), 3))
        exact = any(
            check_assignment(dict(enumerate(v)), size, small_pairs, small_triples)
            for v in itertools.product((0, 1), repeat=size)
        )
        require(exact == (size == 3), "Unexpected exhaustive control result")
        found, _ = satisfying_assignment(size, small_pairs, small_triples)
        require((found is not None) == exact, "Exhaustive solver control failed")
    print(json.dumps({
        "status": "PASS", "authority_effect": "None",
        "claim": "No {0,1}-valued frame function on all Q^3 or Q(i)^3 rays",
        "rays": len(rays), "orthogonal_pairs": len(pairs),
        "internal_frames": len(triples), "completed_pairs": len(pairs),
        "raw_cross_products_outside_box": outside,
        "binary_search_nodes": nodes,
        "controls": ["triples-only SAT", "pairs-only SAT", "exhaustive small instances"],
        "not_established": ["signed rigidity", "nonnegative rigidity", "exotic extension"],
    }, indent=2))


if __name__ == "__main__":
    main()
