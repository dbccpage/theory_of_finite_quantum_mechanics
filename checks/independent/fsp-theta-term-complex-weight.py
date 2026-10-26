"""Independent integer check for the FSP-THETA-TERM-COMPLEX-WEIGHT narrowing.

Recomputes four quarter turns of (1, 0) by (0, -1), the charge-0 and charge-1
weights, and the product (1, 0) * (0, -1). Does not import repository code.
"""
from __future__ import annotations

failures = 0


def check(cond: bool, msg: str) -> None:
    global failures
    if not cond:
        failures += 1
        print("FAIL", msg)


def mul_neg_i(p: tuple[int, int]) -> tuple[int, int]:
    a, b = p
    return (b, -a)


def gmul(a: int, b: int, c: int, d: int) -> tuple[int, int]:
    return (a * c - b * d, a * d + b * c)


def quarter(k: int) -> tuple[int, int]:
    p = (1, 0)
    for _ in range(k):
        p = mul_neg_i(p)
    return p


def weight(k: int, q: int) -> tuple[int, int]:
    if q == 0:
        return (1, 0)
    if q == 1:
        return quarter(k)
    return (0, 0)


def positive_real(p: tuple[int, int]) -> bool:
    return p[0] > 0 and p[1] == 0


expected = {
    0: (1, 0),
    1: (0, -1),
    2: (-1, 0),
    3: (0, 1),
    4: (1, 0),
}

for k, pair in expected.items():
    check(quarter(k) == pair, f"quarter {k}")

check(mul_neg_i((1, 0)) == gmul(1, 0, 0, -1), "turn is product")
check(gmul(1, 0, 0, -1) == (0, -1), "phase product")

for k in (0, 1, 2, 3):
    check(weight(k, 0) == (1, 0), f"charge 0 at {k}")
    check(weight(k, 1) == expected[k], f"charge 1 at {k}")

check(weight(0, 1)[1] == 0, "im index 0")
check(weight(1, 1)[1] == -1, "im index 1")
check(weight(1, 1)[1] != 0, "im index 1 nonzero")
check(weight(2, 1)[1] == 0, "im index 2")
check(weight(2, 1)[0] == -1, "re index 2")
check(not (weight(2, 1)[0] > 0), "index 2 not positive")
check(weight(3, 1)[1] == 1, "im index 3")
check(weight(3, 1)[1] != 0, "im index 3 nonzero")
check(positive_real(weight(0, 1)), "index 0 positive real")
check(not positive_real(weight(1, 1)), "index 1 not positive real")
check(not positive_real(weight(2, 1)), "index 2 not positive real")
check(not positive_real(weight(3, 1)), "index 3 not positive real")

print("quarters:", [quarter(k) for k in range(5)])
print("charge0:", [weight(k, 0) for k in range(4)])
print("charge1:", [weight(k, 1) for k in range(4)])
print("phase_product:", gmul(1, 0, 0, -1))
print(f"failures={failures}")
raise SystemExit(failures)
