"""Independent exact finite audit of the sign, pair and three-cycle examples.

Uses a matrix for multiplication by i and a permutation table for the cycle.
These finite examples do not construct U(1) or a continuous phase parameter.
"""
from __future__ import annotations


def main() -> None:
    failures: list[str] = []
    signs = (1, -1)
    for value in signs:
        if value * value != 1:
            failures.append(f"sign square: {value}")

    pairs = ((1, 1), (1, -1))
    if pairs[0] == pairs[1]:
        failures.append("pairs are not distinct")
    if any(coordinate not in signs for pair in pairs for coordinate in pair):
        failures.append("pair coordinate is not a sign")

    imaginary_unit = (0, 1)
    norm = sum(coordinate * coordinate for coordinate in imaginary_unit)
    if norm != 1:
        failures.append("imaginary unit square norm")
    rotation = ((0, -1), (1, 0))
    square = tuple(sum(a * b for a, b in zip(row, imaginary_unit)) for row in rotation)
    if square != (-1, 0) or square == (1, 0):
        failures.append("imaginary unit square")

    successor = (1, 2, 0)
    orbits: list[tuple[int, ...]] = []
    for start in range(3):
        state = start
        orbit = []
        for _ in range(3):
            state = successor[state]
            orbit.append(state)
        if state != start or len(set(orbit)) != 3:
            failures.append(f"three-cycle from {start}")
        orbits.append(tuple(orbit))
    if orbits[0] != (1, 2, 0):
        failures.append("specified orbit from zero")

    for failure in failures:
        print("FAIL", failure)
    print(f"sign_cases={len(signs)} pairs={pairs} norm={norm} square={square}")
    print(f"cycle_cases={len(orbits)} orbit_from_zero={orbits[0]} failures={len(failures)}")
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
