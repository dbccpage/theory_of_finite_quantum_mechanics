"""Independent integer check for DS-QM204-BORN-UNIQUENESS-IMPORT-BOUNDARY.

Recomputes the pair-sum identity, the pair (3, 4) splits, and the rotation identity.
No repository imports.
"""

from __future__ import annotations


def main() -> int:
    failures: list[str] = []

    def check(name: str, ok: bool) -> None:
        print(f"{name}: {ok}")
        if not ok:
            failures.append(name)

    pair_bad = [
        (a, b)
        for a in range(-5, 6)
        for b in range(-5, 6)
        if a + b != (a + b) * 1
    ]
    check("pair_norm_box", pair_bad == [])

    check("denom", 3 + 4 == 7 and 7 != 0)
    sq3, sq4, sq5 = 3 * 3, 4 * 4, 5 * 5
    print(f"squares_parts {sq3} {sq4} {sq3 + sq4} {sq5}")
    check("squares", sq3 == 9 and sq4 == 16 and sq3 + sq4 == 25 and sq5 == 25)
    p3, p4 = 3 * 3 * 3 * 3, 4 * 4 * 4 * 4
    fourths = p3 + p4
    print(f"fourths_parts {p3} {p4} {fourths}")
    check("fourths", p3 == 81 and p4 == 256 and fourths == 337)

    quartic_left = (3 * 3) * (3 * 3 * 3 * 3 + 4 * 4 * 4 * 4)
    quartic_right = (3 * 3 * 3 * 3) * (5 * 5)
    print(f"quartic_split {quartic_left} != {quartic_right}")
    check("quartic_split", quartic_left == 3033 and quartic_right == 2025 and quartic_left != quartic_right)

    linear_left = 3 * (3 * 3 + 4 * 4)
    linear_right = (3 * 3) * (3 + 4)
    print(f"linear_split {linear_left} != {linear_right}")
    check("linear_split", linear_left == 75 and linear_right == 63 and linear_left != linear_right)

    rot_bad = 0
    for a in range(-3, 4):
        for b in range(-3, 4):
            for r in range(-3, 4):
                for s in range(-3, 4):
                    left = (r * a - s * b) ** 2 + (s * a + r * b) ** 2
                    right = (r * r + s * s) * (a * a + b * b)
                    if left != right:
                        rot_bad += 1
    check("rotation_box", rot_bad == 0)

    cross_a = 3 * 3 - 4 * 4
    cross_b = 4 * 3 + 3 * 4
    witness_left = cross_a * cross_a + cross_b * cross_b
    witness_right = (3 * 3 + 4 * 4) * (3 * 3 + 4 * 4)
    print(f"witness_parts {cross_a} {cross_b} {cross_a * cross_a} {cross_b * cross_b} {witness_left} {witness_right}")
    check(
        "witness",
        cross_a == -7
        and cross_b == 24
        and cross_a * cross_a == 49
        and cross_b * cross_b == 576
        and witness_left == 625
        and witness_right == 625,
    )

    if failures:
        print("FAIL", ",".join(failures))
        return 1
    print(
        "checked pair-sum, squares 25, fourths 337, "
        "splits 3033!=2025 and 75!=63, rotation box, witness 625"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
