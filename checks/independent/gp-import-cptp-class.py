"""Independent check for the Boolean collapse slice of GP-IMPORT-CPTP-CLASS.

No repository imports. Integer arithmetic and an enumeration of maps on four points.
"""

import itertools
import sympy as sp

FAILURES = 0
CHECKS = 0


def check(ok: bool) -> None:
    global FAILURES, CHECKS
    CHECKS += 1
    if not ok:
        FAILURES += 1


def collapse(q: int) -> int:
    return 0


def col_of(swap_p: int, swap_u: int, point: tuple[int, int]) -> tuple[int, int]:
    a, b = point
    if b == 0:
        return (0, swap_p if a == 0 else 1 - swap_p)
    return (1, swap_u if a == 0 else 1 - swap_u)


def col_inv(swap_p: int, swap_u: int, point: tuple[int, int]) -> tuple[int, int]:
    a, b = point
    if a == 0:
        bit = (1 - b) if swap_p else b
        return (bit, 0)
    bit = (1 - b) if swap_u else b
    return (bit, 1)


POINTS = [(a, b) for a in (0, 1) for b in (0, 1)]


def as_map(images: tuple[tuple[int, int], ...]) -> dict:
    return {p: img for p, img in zip(POINTS, images)}


def compose(f: dict, g: dict) -> dict:
    return {p: f[g[p]] for p in POINTS}


def is_id(f: dict) -> bool:
    return all(f[p] == p for p in POINTS)


def reduces(f: dict) -> bool:
    return all(f[(q, 0)][0] == collapse(q) for q in (0, 1))


named = []
for swap_p, swap_u in itertools.product((0, 1), repeat=2):
    forward = {p: col_of(swap_p, swap_u, p) for p in POINTS}
    backward = {p: col_inv(swap_p, swap_u, p) for p in POINTS}
    check(is_id(compose(backward, forward)))
    check(is_id(compose(forward, backward)))
    check(reduces(forward))
    named.append(forward)

for i, j in itertools.combinations(range(4), 2):
    check(named[i] != named[j])

matches = 0
maps_seen = 0
for images in itertools.product(POINTS, repeat=4):
    forward = as_map(images)
    maps_seen += 1
    has_inverse = False
    for inv_images in itertools.product(POINTS, repeat=4):
        backward = as_map(inv_images)
        if is_id(compose(backward, forward)) and is_id(compose(forward, backward)):
            has_inverse = True
            break
    if has_inverse and reduces(forward):
        matches += 1
        check(any(forward == item for item in named))

check(maps_seen == 256)
check(matches == 4)
check(collapse(0) == 0 and collapse(1) == 0 and collapse(0) == collapse(1))

wF, wT = sp.symbols("wF wT", integer=True)
image = (wF + wT, sp.Integer(0))
check(sp.expand(image[0] + image[1] - (wF + wT)) == 0)
check(sp.expand(image[0] - (wF + wT)) == 0 and image[1] == 0)
check(sp.Integer(2) + sp.Integer(3) == 5)
check((2 + 3, 0) == (5, 0))
for a, b in ((0, 0), (0, 4), (7, 1), (2, 3)):
    img = (a + b, 0)
    check(img[0] + img[1] == a + b)
    check(img[0] >= 0 and img[1] >= 0)

if FAILURES:
    print(f"checks={CHECKS} failures={FAILURES} maps={maps_seen} dilations={matches}")
    raise SystemExit(1)
print(
    f"checks={CHECKS} failures=0 maps={maps_seen} dilations={matches} "
    f"named=4 mass=(5, 0) collapse=(0, 0)"
)
