# Status: independent check for TFQ-0319. No repository imports.
"""Finite unjoined receipt and two-mark carrier.

Recomputes the seven nibbles of the prefix 3100c4e, the four functions
Fin 2 -> Fin 2, their coboundaries, and the four pairings of one green receipt.
"""

from __future__ import annotations


def coboundary(values, u, v):
    return (values[v] - values[u]) % 2


def main():
    failures = 0
    checked = 0

    def expect(cond):
        nonlocal failures, checked
        checked += 1
        if not cond:
            failures += 1

    nibbles = [3, 1, 0, 0, 12, 4, 14]
    expect(len(nibbles) == 7)
    value = 0
    for digit in nibbles:
        value = value * 16 + digit
    expect(value == 0x3100C4E)
    expect(format(value, "x") == "3100c4e")
    green = True

    maps = {
        0: (0, 0),
        1: (0, 1),
        2: (1, 0),
        3: (1, 1),
    }
    expect(len(maps) == 4)
    for _i, values in maps.items():
        expect(coboundary(values, 0, 0) == 0)
        expect(coboundary(values, 1, 1) == 0)

    expect(coboundary(maps[0], 0, 1) == 0)
    expect(coboundary(maps[1], 0, 1) == 1)
    expect(coboundary(maps[2], 0, 1) == 1)
    expect(coboundary(maps[3], 0, 1) == 0)

    images = [maps[i] for i in range(4)]
    expect(len(set(images)) == 4)
    for a in range(4):
        for b in range(a + 1, 4):
            expect(images[a] != images[b])

    listed = {(0, 0), (0, 1), (1, 0), (1, 1)}
    seen = 0
    for x in (0, 1):
        for y in (0, 1):
            seen += 1
            expect((x, y) in listed)
    expect(seen == 4)

    # One receipt record paired with each map index.
    receipt = (tuple(nibbles), green)
    pairings = [(receipt, i) for i in range(4)]
    expect(len(pairings) == 4)
    for i in range(4):
        expect(pairings[i][0] == receipt)
        expect(pairings[i][0][1] is True)
        expect(pairings[i][1] == i)
    for a in range(4):
        for b in range(a + 1, 4):
            expect(pairings[a] != pairings[b])
            expect(pairings[a][0] == pairings[b][0])

    edge0 = coboundary(maps[pairings[0][1]], 0, 1)
    edge1 = coboundary(maps[pairings[1][1]], 0, 1)
    expect(pairings[0][0] == pairings[1][0])
    expect(pairings[0][1] != pairings[1][1])
    expect(edge0 == 0)
    expect(edge1 == 1)
    expect(edge0 != edge1)

    print(f"checked {checked} conditions, {failures} failures")
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
