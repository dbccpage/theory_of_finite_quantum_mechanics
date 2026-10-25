"""Nat square gap, zero-input equality, cubic sum, and one disjoint pair.

No repository imports. Exact integers only.
"""

from __future__ import annotations


def main() -> None:
    bound = 12
    failures = 0
    pairs = 0
    for a in range(bound + 1):
        for b in range(bound + 1):
            pairs += 1
            expanded = (a + b) * (a + b)
            parts = a * a + b * b + 2 * (a * b)
            if expanded != parts:
                failures += 1
            cubic = (a + b) * (a + b) * (a + b)
            cubic_parts = a * a * a + b * b * b + 3 * a * b * (a + b)
            if cubic != cubic_parts:
                failures += 1
            pair = (a + 0) * (a + 0) + (0 + b) * (0 + b)
            if pair != a * a + b * b:
                failures += 1
            if a > 0 and b > 0:
                if not (2 * (a * b) > 0 and a * a + b * b < expanded):
                    failures += 1
            if a == 0 and (2 * (0 * b) != 0 or (0 + b) * (0 + b) != b * b):
                failures += 1
            if b == 0 and (2 * (a * 0) != 0 or (a + 0) * (a + 0) != a * a):
                failures += 1
    witness_square = (3 + 5) * (3 + 5)
    witness_parts = 3 * 3 + 5 * 5 + 2 * (3 * 5)
    witness_cross = 2 * (3 * 5)
    witness_masses = 3 * 3 + 5 * 5
    witness_cubic = (3 + 5) * (3 + 5) * (3 + 5)
    witness_cubic_parts = 3 * 3 * 3 + 5 * 5 * 5 + 3 * 3 * 5 * (3 + 5)
    if witness_square != 64 or witness_parts != 64 or witness_cross != 30:
        failures += 1
    if witness_masses != 34 or not (34 < 64):
        failures += 1
    if witness_cubic != 512 or witness_cubic_parts != 512:
        failures += 1
    if (3 * 3 * 3) != 27 or (5 * 5 * 5) != 125:
        failures += 1
    print(
        f"bound={bound} pairs={pairs} failures={failures} "
        f"witness_square={witness_square} witness_cross={witness_cross} "
        f"witness_masses={witness_masses} witness_cubic={witness_cubic}"
    )
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
