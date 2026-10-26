"""Independent check for the two-coordinate signed-permutation shadow.

Recomputes sign, swap, edge additivity, absolute homogeneity, the eight
images of (1, 2), the weight-swap criterion, and the equal-length split.
Does not import repository code.
"""
from __future__ import annotations

failures = 0
checks = 0


def check(name: str, cond: bool) -> None:
    global failures, checks
    checks += 1
    if not cond:
        failures += 1
        print(f"FAIL {name}")


def l1(x: int, y: int) -> int:
    return abs(x) + abs(y)


def weighted(w1: int, w2: int, x: int, y: int) -> int:
    return w1 * abs(x) + w2 * abs(y)


def apply_gauge(swap: bool, sx: bool, sy: bool, x: int, y: int) -> tuple[int, int]:
    xp = -x if sx else x
    yp = -y if sy else y
    if swap:
        return (yp, xp)
    return (xp, yp)


bools = (False, True)
images = [apply_gauge(swap, sx, sy, 1, 2) for swap in bools for sx in bools for sy in bools]
expected = [
    (1, 2),
    (1, -2),
    (-1, 2),
    (-1, -2),
    (2, 1),
    (-2, 1),
    (2, -1),
    (-2, -1),
]
lean_order = [
    (1, 2),
    (-1, 2),
    (1, -2),
    (-1, -2),
    (2, 1),
    (2, -1),
    (-2, 1),
    (-2, -1),
]

check("eight_images", images == expected)
check("eight_distinct", len(set(images)) == 8)
check("same_set_as_lean_order", set(images) == set(lean_order))

for swap in bools:
    for sx in bools:
        for sy in bools:
            for x in range(-4, 5):
                for y in range(-4, 5):
                    a, b = apply_gauge(swap, sx, sy, x, y)
                    check(f"preserve_{swap}_{sx}_{sy}_{x}_{y}", l1(a, b) == l1(x, y))

for x in range(-6, 7):
    for y in range(-6, 7):
        check(f"edge_{x}_{y}", l1(x, 0) + l1(0, y) == l1(x, y))
        for k in range(-5, 6):
            check(
                f"homog_{k}_{x}_{y}",
                l1(k * x, k * y) == abs(k) * l1(x, y),
            )

for w1 in range(0, 5):
    for w2 in range(0, 5):
        invariant = all(
            weighted(w1, w2, x, y) == weighted(w1, w2, y, x)
            for x in range(-3, 4)
            for y in range(-3, 4)
        )
        check(f"sample_swap_iff_{w1}_{w2}", invariant == (w1 == w2))
        if w1 == w2:
            for x in range(-4, 5):
                for y in range(-4, 5):
                    check(
                        f"scaled_{w1}_{x}_{y}",
                        weighted(w1, w1, x, y) == w1 * l1(x, y),
                    )

check("axes_1", weighted(1, 2, 1, 0) == 1)
check("axes_2", weighted(1, 2, 0, 1) == 2)
check("axes_differ", 1 != 2)
check("sq_34", 3 * 3 + 4 * 4 == 25)
check("sq_50", 5 * 5 + 0 * 0 == 25)
check("l1_34", l1(3, 4) == 7)
check("l1_50", l1(5, 0) == 5)
check("l1_split", 7 != 5)

# The coordinate criterion is exact, not only the sample: evaluate (1, 0).
for w1 in range(0, 8):
    for w2 in range(0, 8):
        left = weighted(w1, w2, 1, 0)
        right = weighted(w1, w2, 0, 1)
        check(f"axis_criterion_{w1}_{w2}", (left == right) == (w1 == w2))

print(f"images={images}")
print(f"squared_length_25_aggregates={l1(3, 4)},{l1(5, 0)}")
print(f"axis_weights={weighted(1, 2, 1, 0)},{weighted(1, 2, 0, 1)}")
print(f"checks={checks}")
print(f"failures={failures}")
raise SystemExit(failures)
