"""Independent integer check for the TFQ-0008 finite case.

No repository imports. AuthorityEffect: None.
"""

from __future__ import annotations


def cayley(t: int) -> int:
    return (1 - t * t) ** 2 + (2 * t) ** 2


def euler(t: int) -> int:
    return 1 + t * t


def sum_len1(edges: list[tuple[int, int, int]]) -> int:
    acc = 0
    for src, dst, weight in edges:
        if src == 0 and dst == 2:
            acc += weight
    return acc


def sum_len2(edges: list[tuple[int, int, int]]) -> int:
    acc = 0
    for src1, dst1, weight1 in edges:
        for src2, dst2, weight2 in edges:
            if src1 == 0 and dst1 == src2 and dst2 == 2:
                acc += weight1 * weight2
    return acc


def mask(w0: int, w1: int) -> tuple[int, int]:
    return (0, w1)


def main() -> int:
    for t in range(-12, 13):
        if cayley(t) != (1 + t * t) ** 2:
            raise SystemExit(f"cayley identity failed at {t}")
        if (euler(t) == 1) != (t == 0):
            raise SystemExit(f"euler unit test failed at {t}")
    if cayley(1) != 4:
        raise SystemExit("cayley(1)")
    if euler(2) != 5 or euler(2) - 1 != 4:
        raise SystemExit("euler(2)")
    if cayley(2) != 25 or (1 + 2 * 2) ** 2 != 25:
        raise SystemExit("cayley(2)")
    for a in range(-5, 6):
        for b in range(-5, 6):
            graph = [(0, 1, a), (1, 2, b)]
            if sum_len1(graph) != 0 or sum_len2(graph) != a * b:
                raise SystemExit(f"path sum failed at {(a, b)}")
    for w0 in range(-3, 4):
        for w1 in range(-3, 4):
            image = mask(w0, w1)
            if image != (0, w1) or mask(*image) != image:
                raise SystemExit(f"mask failed at {(w0, w1)}")
        if mask(w0, 0) != (0, 0):
            raise SystemExit(f"zero mass failed at {w0}")
    exact = (2, 0, 0, 2)
    near = (2, 0, 0, 3)
    distance = max(abs(near[i] - exact[i]) for i in range(4))
    if distance != 1:
        raise SystemExit("distance")
    if (exact[0] + exact[1], exact[2] + exact[3]) != (2, 2):
        raise SystemExit("exact rows")
    if (near[0] + near[1], near[2] + near[3]) != (2, 3):
        raise SystemExit("near rows")
    print(
        "checked path sums a,b in -5..5, sector mask on -3..3, "
        "Cayley identity for t in -12..12, cayley(1)=4, "
        "euler(2)=5 inflation 4, cayley(2)=25, entry distance 1 with row sums 2,2 against 2,3"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
