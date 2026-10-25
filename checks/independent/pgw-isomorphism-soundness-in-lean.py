"""Independent check of the two-data coloring key.

Recomputes the lexicographic minimum of a bit pair and its swap.
Does not import repository code. Does not replay an implemented regime key.
"""
from __future__ import annotations


def bit(flag):
    return 1 if flag else 0


def ser(color):
    return (bit(color[0]), bit(color[1]))


def swap(color):
    return (color[1], color[0])


def key(color):
    left = ser(color)
    right = ser(swap(color))
    return left if left <= right else right


UNIVERSE = [(False, False), (False, True), (True, False), (True, True)]


def main():
    checks = []

    def add(condition):
        checks.append(bool(condition))

    pairs = [(a, b) for a in (False, True) for b in (False, True)]
    add(pairs == UNIVERSE)
    add(len(UNIVERSE) == 4)
    for color in UNIVERSE:
        add(swap(swap(color)) == color)
        add(key(swap(color)) == key(color))
    add(key((False, False)) == (0, 0))
    add(key((False, True)) == (0, 1))
    add(key((True, False)) == (0, 1))
    add(key((True, True)) == (1, 1))
    add(sum(1 for color in UNIVERSE if key(color) == (0, 1)) == 2)
    add(swap((False, False)) == (False, False))
    add(swap((True, True)) == (True, True))
    add(key((False, False)) != key((True, True)))
    for left in UNIVERSE:
        for right in UNIVERSE:
            add((key(left) == key(right)) == (left == right or left == swap(right)))
    failed = sum(1 for item in checks if not item)
    print(f"checked {len(checks)} conditions, {failed} failures")
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
