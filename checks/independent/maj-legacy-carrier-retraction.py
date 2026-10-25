"""Independent check for the identity coboundary on Fin t -> Bool.

No repository imports. Sizes 1, 2, 3 and 4 are enumerated in full.
"""

from itertools import product


def vectors(t: int) -> list[tuple[bool, ...]]:
    return list(product((False, True), repeat=t))


def d0(a: tuple[bool, ...]) -> tuple[bool, ...]:
    return tuple(a)


def d1(w: tuple[bool, ...]) -> tuple[bool, ...]:
    return (False,)


def zero1() -> tuple[bool, ...]:
    return (False,)


def is_exact(w: tuple[bool, ...], rows: list[tuple[bool, ...]]) -> bool:
    return any(d0(a) == w for a in rows)


def is_cocycle(w: tuple[bool, ...]) -> bool:
    return d1(w) == zero1()


def is_closed(w: tuple[bool, ...], rows: list[tuple[bool, ...]]) -> bool:
    return is_cocycle(w) and not is_exact(w, rows)


def main() -> None:
    failures = 0
    counts: list[int] = []
    closed_counts: list[int] = []
    for t in (1, 2, 3, 4):
        rows = vectors(t)
        counts.append(len(rows))
        if len(rows) != 2**t:
            failures += 1
        closed = 0
        for a in rows:
            if d0(a) != a:
                failures += 1
            if d1(d0(a)) != zero1():
                failures += 1
        for w in rows:
            if not is_cocycle(w) or not is_exact(w, rows):
                failures += 1
            if is_closed(w, rows):
                closed += 1
                failures += 1
        closed_counts.append(closed)
    if counts != [2, 4, 8, 16] or sum(counts) != 30 or closed_counts != [0, 0, 0, 0]:
        failures += 1
    # A constant-false coboundary on size 1 leaves the true cochain unhit.
    contrast_rows = vectors(1)
    contrast_closed = 0
    for w in contrast_rows:
        hit = any(tuple(False for _ in a) == w for a in contrast_rows)
        if is_cocycle(w) and not hit:
            contrast_closed += 1
    if contrast_closed != 1:
        failures += 1
    print(f"failures={failures}")
    print("sizes 1 2 3 4 vector counts 2 4 8 16")
    print("sum of those counts is 30")
    print("closed residual counts 0 0 0 0")
    print("constant-false coboundary on size 1 has 1 unhit cocycle")
    print("finite window is an audit of sizes 1, 2, 3 and 4, not a substitute for the argument at every size")
    raise SystemExit(failures)


if __name__ == "__main__":
    main()
