"""Independent integer check for the GP-IMPORT-CIRCLE-U1 narrowing.

Recomputes sign squares, the two sign pairs, the square norm and product of
the pair 0, 1, and one three-step cycle. Does not import repository code.
"""
from __future__ import annotations

failures = 0


def check(cond: bool, msg: str) -> None:
    global failures
    if not cond:
        failures += 1
        print("FAIL", msg)


def is_sign(a: int) -> bool:
    return a == 1 or a == -1


def gmul(a: int, b: int, c: int, d: int) -> tuple[int, int]:
    return (a * c - b * d, a * d + b * c)


def gnorm(a: int, b: int) -> int:
    return a * a + b * b


def cyc(n: int) -> int:
    if n == 0:
        return 1
    if n == 1:
        return 2
    if n == 2:
        return 0
    return n


for a in (1, -1):
    check(is_sign(a), f"sign {a}")
    check(a * a == 1, f"square {a}")

check((1, 1) != (1, -1), "pairs differ")
check(is_sign(1) and is_sign(1) and is_sign(1) and is_sign(-1), "pair coordinates")
check(gnorm(0, 1) == 1, "square norm")
check(gmul(0, 1, 0, 1) == (-1, 0), "product")
check(gmul(0, 1, 0, 1) != (1, 0), "product differs from 1, 0")
check(cyc(cyc(0)) == 2, "second step")
check(cyc(cyc(cyc(0))) == 0, "third step")

print("sign_squares:", 1 * 1, (-1) * (-1))
print("pairs:", (1, 1), (1, -1))
print("norm:", gnorm(0, 1))
print("product:", gmul(0, 1, 0, 1))
print("cycle:", cyc(0), cyc(cyc(0)), cyc(cyc(cyc(0))))
print(f"failures={failures}")
raise SystemExit(failures)
