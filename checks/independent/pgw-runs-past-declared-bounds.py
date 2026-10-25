"""Independent check of five records against the declared bound line.

A record is inside when rounds are at most 15, nodes are at most 250,
data is below 4, and items are at most 2. Does not import repository
code and does not replay a forward run.
"""
from __future__ import annotations


def inside(rounds, nodes, data, items):
    return rounds <= 15 and nodes <= 250 and data < 4 and items <= 2


RECORDS = (
    (15, 250, 3, 2, True),
    (16, 250, 3, 2, False),
    (15, 251, 3, 2, False),
    (15, 250, 4, 2, False),
    (15, 250, 3, 3, False),
)


def main():
    checks = []

    def add(condition):
        checks.append(bool(condition))

    add(len(RECORDS) == 5)
    for rounds, nodes, data, items, expected in RECORDS:
        add(inside(rounds, nodes, data, items) == expected)
    add((15 <= 15) and (250 <= 250) and (3 < 4) and (2 <= 2))
    add(16 > 15)
    add(251 > 250)
    add(not (4 < 4))
    add(3 > 2)
    failed = sum(1 for item in checks if not item)
    print(f"checked {len(checks)} conditions, {failed} failures")
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
