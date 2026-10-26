"""Independent integer check for MAJ-IMPORT-KITAEV-CHAIN.

Recomputes sweet-spot index separation and two comparisons of mu * mu with (2 * t) * (2 * t).
No repository imports.
"""

from __future__ import annotations


def main() -> int:
    failures: list[str] = []

    def check(name: str, ok: bool) -> None:
        print(f"{name}: {ok}")
        if not ok:
            failures.append(name)

    bad = 0
    seen = 0
    for length in range(2, 13):
        for j in range(1, length):
            seen += 1
            left = 2 * j
            right = 2 * j + 1
            edge = 2 * length
            if not (left != 1 and left != edge and right != 1 and right != edge):
                bad += 1
    check("edge_box", bad == 0 and seen == sum(range(1, 12)))

    pair_left = 2 * 1
    pair_right = 2 * 1 + 1
    edge = 2 * 2
    print(f"witness_parts {pair_left} {pair_right} {edge}")
    check(
        "edge_witness",
        pair_left == 2
        and pair_right == 3
        and edge == 4
        and pair_left != 1
        and pair_left != 4
        and pair_right != 1
        and pair_right != 4,
    )

    inside_left = 1 * 1
    inside_right = (2 * 1) * (2 * 1)
    print(f"inside_parts {inside_left} {inside_right}")
    check("inside_point", inside_left == 1 and inside_right == 4 and inside_left < inside_right and 1 != 0)

    outside_left = 3 * 3
    outside_right = (2 * 1) * (2 * 1)
    print(f"outside_parts {outside_left} {outside_right}")
    check(
        "outside_point",
        outside_left == 9 and outside_right == 4 and not (outside_left < outside_right) and 1 != 0,
    )

    if failures:
        print("FAIL", ",".join(failures))
        return 1
    print("checked edge box through L=12, witness (2, 3) against 1 and 4, inside 1<4, outside 9<4 false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
