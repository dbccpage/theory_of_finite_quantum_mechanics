"""One rational instance of the supply threshold and an explicit level bound.

The recurrence here is the constant overhead 4. This script does not
import repository code and does not speak for a device.
"""
from __future__ import annotations

from fractions import Fraction

failures = 0


def check(cond: bool, msg: str) -> None:
    global failures
    if not cond:
        failures += 1
        print("FAIL", msg)


lam = Fraction(1)
g = Fraction(1, 2)
kappa = Fraction(1)
r = Fraction(2)
threshold = lam / ((1 - g) * kappa)
check(threshold == 2, "threshold lam/((1-g)*kappa)")
check(r >= threshold, "supply meets the threshold")

C = Fraction(4)
p0 = Fraction(1, 10)
D = max(C, Fraction(1))
check(D * p0 == Fraction(2, 5), "D*p0 = 2/5")
check(D * p0 < 1, "D*p0 < 1")
check(D * p0 <= Fraction(1, 2), "D*p0 <= 1/2")

p1 = C * p0 * p0
check(p1 == Fraction(1, 25), "p1 = 1/25")
conc1 = (D * p0) ** (2 ** 1) / D
check(p1 == conc1, "one recurrence step meets (D*p0)^(2^k)/D")

eps = Fraction(1)
k = 1
level_bound = eps * D * (2 ** (2 ** k))
check(level_bound == 16, "epsilon * D * 2^(2^k) = 16")
check(level_bound * p1 == Fraction(16, 25), "16/25")
check(level_bound * p1 <= eps, "L * p1 <= epsilon at L = 16")

print(
    "checked threshold 2, D*p0 = 2/5 <= 1/2, p1 = 1/25, "
    "and 16 * p1 = 16/25 <= 1"
)
print(f"failures={failures}")
raise SystemExit(failures)
