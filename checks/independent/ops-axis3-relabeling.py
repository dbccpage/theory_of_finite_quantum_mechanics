"""Length export under the token map that swaps 0 with 1.

Recomputes the finite lists in the narrowed slice. No repository imports.
AuthorityEffect: None.
"""

from __future__ import annotations


def swap01(n: int) -> int:
    if n == 0:
        return 1
    if n == 1:
        return 0
    return n


def words(bound: int) -> list[list[int]]:
    out: list[list[int]] = [[]]
    level = [[]]
    for _ in range(bound):
        nxt: list[list[int]] = []
        for xs in level:
            nxt.append(xs + [0])
            nxt.append(xs + [1])
        out.extend(nxt)
        level = nxt
    out.append([2, 0, 1])
    out.append([3])
    return out


def main() -> int:
    failures: list[str] = []
    bound = 3
    rows = words(bound)
    if swap01(0) != 1 or swap01(1) != 0 or swap01(2) != 2 or swap01(3) != 3:
        failures.append("swap01 table")
    for xs in rows:
        ys = [swap01(x) for x in xs]
        if len(ys) != len(xs):
            failures.append(f"length {xs}")
        if (len(ys) % 2) != (len(xs) % 2):
            failures.append(f"parity {xs}")
        for a, b in zip(xs, ys):
            if a >= 2 and a != b:
                failures.append(f"fixed {xs}")
    print(f"bound={bound}")
    print(f"lists={len(rows)}")
    print("swap01(0)=1")
    print("swap01(1)=0")
    print("swap01(2)=2")
    print("swap01(3)=3")
    print(f"failures={len(failures)}")
    for item in failures:
        print(item)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
