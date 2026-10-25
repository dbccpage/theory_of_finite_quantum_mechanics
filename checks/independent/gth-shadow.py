"""One triangle, one reach map, and one pair of parallel edges.

Recomputes the three face identities, the collapsed reach pair, and
the agreeing source and target values. No repository import. Integers only.
"""
from __future__ import annotations


def src(edge: tuple[int, int]) -> int:
    return edge[0]


def tgt(edge: tuple[int, int]) -> int:
    return edge[1]


def reach(v: int) -> int:
    return 0


def edge_source(_e: int) -> int:
    return 0


def edge_target(_e: int) -> int:
    return 1


def main() -> None:
    checks = 0
    failures = 0

    def expect(condition: bool) -> None:
        nonlocal checks, failures
        checks += 1
        if not condition:
            failures += 1

    face2 = (0, 1)
    face1 = (0, 2)
    face0 = (1, 2)
    expect(tgt(face1) == 2)
    expect(tgt(face0) == 2)
    expect(tgt(face1) == tgt(face0))
    expect(tgt(face2) == 1)
    expect(src(face0) == 1)
    expect(tgt(face2) == src(face0))
    expect(src(face2) == 0)
    expect(src(face1) == 0)
    expect(src(face2) == src(face1))
    expect(reach(0) == 0)
    expect(reach(1) == 0)
    expect((reach(0), reach(1)) == (0, 0))
    expect((reach(0), reach(1)) != face2)
    expect(edge_source(0) == 0)
    expect(edge_source(1) == 0)
    expect(edge_target(0) == 1)
    expect(edge_target(1) == 1)
    expect(edge_source(0) == edge_source(1))
    expect(edge_target(0) == edge_target(1))
    print(f"checked {checks} conditions, {failures} failures")
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
