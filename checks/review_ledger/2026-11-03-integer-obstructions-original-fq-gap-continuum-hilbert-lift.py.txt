"""Integer-slice audit for the continuum Hilbert-lift campaign module.

Recomputes 2 * a != 1, the discriminant identity, squares against 5, and
the vanishing of t * t - t - 1 on a finite window. Does not import
repository code. The window is an audit. The general argument is the
Lean module.
"""
from __future__ import annotations

FAILURES = 0


def fail(message: str) -> None:
    global FAILURES
    FAILURES += 1
    print(message)


def main() -> int:
    if 1 % 2 != 1:
        fail("1 is not odd")
    for a in range(-32, 33):
        if (2 * a) % 2 != 0 or 2 * a == 1:
            fail(f"2 * {a} = 1")
    for t in range(-32, 33):
        left = 4 * (t * t - t - 1) + 5
        right = (2 * t - 1) * (2 * t - 1)
        expanded = 4 * (t * t) - 4 * t + 1
        if left != right or left != expanded:
            fail(f"identity t={t}: {left} vs {right}")
    for n in range(-32, 33):
        if n * n == 5:
            fail(f"square {n}")
        if abs(n) >= 3 and n * n < 9:
            fail(f"square bound {n}")
    for t in range(-32, 33):
        if t * t - t - 1 == 0:
            fail(f"root t={t}")
    print(f"failures={FAILURES}")
    print("finite window is an audit, not the general argument")
    return FAILURES


if __name__ == "__main__":
    raise SystemExit(main())
