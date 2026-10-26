"""Integer check of the two-label Gleason slice. This file imports no repository code."""

from __future__ import annotations


def weight(amplitude: int) -> int:
    return amplitude * amplitude


def pair(effect_false: int, effect_true: int) -> int:
    return weight(2) * effect_false + weight(1) * effect_true


def main() -> None:
    failures = 0
    if not (2 < 3):
        failures += 1
    if 3 <= 2:
        failures += 1
    labels = [False, True]
    triple_found = False
    for a in labels:
        for b in labels:
            for c in labels:
                if a != b and a != c and b != c:
                    triple_found = True
    if triple_found:
        failures += 1
    if weight(2) != 4 or weight(1) != 1:
        failures += 1
    unit_direct = pair(1, 1)
    unit_swapped = pair(1, 1)
    if unit_direct != 5 or unit_swapped != 5:
        failures += 1
    false_direct = pair(1, 0)
    false_swapped = pair(0, 1)
    if false_direct != 4 or false_swapped != 1 or false_direct == false_swapped:
        failures += 1
    print(
        "checks=6 failures="
        f"{failures} w2={weight(2)} w1={weight(1)} unit={unit_direct} "
        f"direct={false_direct} swapped={false_swapped}"
    )
    raise SystemExit(failures)


if __name__ == "__main__":
    main()
