#!/usr/bin/env python3
"""Independent Nat check for L1-WDP-CH08-C01-REPLICA-L1.

Recomputes coordinate-sum scaling and sum-of-squares scaling.
Does not import repository code. Does not classify l1 or exclude l2.
"""

from __future__ import annotations


def main() -> None:
    checks = 0
    failed = 0

    def record(cond: bool, msg: str) -> None:
        nonlocal checks, failed
        checks += 1
        if not cond:
            failed += 1
            raise AssertionError(msg)

    for c, a, b in (
        (0, 0, 0),
        (1, 3, 4),
        (2, 3, 4),
        (5, 7, 1),
        (8, 9, 2),
        (4, 0, 6),
    ):
        record(c * a + c * b == c * (a + b), f"sum scale c={c} a={a} b={b}")
        left = (c * a) * (c * a) + (c * b) * (c * b)
        right = (c * c) * (a * a + b * b)
        record(left == right, f"square scale c={c} a={a} b={b}")

    record(3 + 4 == 7, "3+4=7")
    record(3 * 3 + 4 * 4 == 25, "squares 25")
    record(5 * 5 == 25, "5*5=25")
    record((3 + 4) * (3 + 4) == 49, "sum square 49")
    record(25 != 49, "25 != 49")
    record(2 * (3 + 4) == 14, "scaled sum 14")
    record((2 * 3) * (2 * 3) + (2 * 4) * (2 * 4) == 100, "scaled squares 100")
    record(2 * (3 * 3 + 4 * 4) == 50, "linear scale 50")
    record(100 != 50, "100 != 50")
    record((2 * 2) * (3 * 3 + 4 * 4) == 100, "square factor 100")

    print(
        "scale sum and squares on six triples; sample 3+4=7 squares=25 five=25 "
        "sumsq=49 scaledSum=14 scaledSquares=100 linear=50 100!=50"
    )
    print(
        "L1-WDP-CH08-C01-REPLICA-L1 INDEPENDENT CHECKER PASSED: "
        f"checks={checks} failed={failed}"
    )


if __name__ == "__main__":
    main()
