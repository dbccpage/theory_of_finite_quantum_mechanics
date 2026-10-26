"""Independent check for the Boolean toggle slice of GP-IMPORT-CONTINUOUS-TIME.

No repository imports. Integer arithmetic, an enumeration of maps on two labels,
and a symbolic Gaussian-integer expansion.
"""

import itertools
import sympy as sp

FAILURES = 0
CHECKS = 0


def check(ok: bool) -> None:
    global CHECKS, FAILURES
    CHECKS += 1
    if not ok:
        FAILURES += 1


def toggle(q: int) -> int:
    return 1 - q


check(toggle(0) == 1 and toggle(1) == 0)

maps = []
for images in itertools.product((0, 1), repeat=2):
    sigma = {0: images[0], 1: images[1]}
    maps.append(sigma)
    squares = all(sigma[sigma[q]] == toggle(q) for q in (0, 1))
    check(not squares)
check(len(maps) == 4)

a, b, c, d = sp.symbols("a b c d", integer=True)


def gadd(x, y):
    return (sp.expand(x[0] + y[0]), sp.expand(x[1] + y[1]))


def gmul(x, y):
    return (
        sp.expand(x[0] * y[0] - x[1] * y[1]),
        sp.expand(x[0] * y[1] + x[1] * y[0]),
    )


def gneg(x):
    return (sp.expand(-x[0]), sp.expand(-x[1]))


def interp(v):
    x, y = v
    return (
        gadd(gmul((1, 1), x), gmul((1, -1), y)),
        gadd(gmul((1, -1), x), gmul((1, 1), y)),
    )


def interp_neg(v):
    left, right = interp(v)
    return (gneg(left), gneg(right))


x = (a, b)
y = (c, d)
twice = interp(interp((x, y)))
neg_twice = interp_neg(interp_neg((x, y)))
want = ((4 * c, 4 * d), (4 * a, 4 * b))
check(twice[0] == want[0] and twice[1] == want[1])
check(neg_twice[0] == want[0] and neg_twice[1] == want[1])
check(sp.expand(gmul((4, 0), x)[0] - 4 * a) == 0)
check(sp.expand(gmul((4, 0), x)[1] - 4 * b) == 0)

sample = interp((((1, 0), (0, 0))))
sample_neg = interp_neg((((1, 0), (0, 0))))
check(sample == ((1, 1), (1, -1)))
check(sample_neg == ((-1, -1), (-1, 1)))
check(sample != sample_neg)
check(4 * 1 == 4 and 4 * 0 == 0)

if FAILURES:
    print(f"checks={CHECKS} failures={FAILURES}")
    raise SystemExit(1)
print(
    f"checks={CHECKS} failures=0 maps=4 "
    f"witness=(((1, 1), (1, -1)), ((-1, -1), (-1, 1))) scale=4"
)
