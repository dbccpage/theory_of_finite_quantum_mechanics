#!/usr/bin/env python3
"""Exact symbolic check for the displayed two-phase affine ansatz.

The matrix is the object named ``karlssonMatrix`` in
``lean4/research_programs/mub6/MasterClassification.lean``. That source says
the name is a legacy label and does not identify the ansatz with the complete
Karlsson family from the literature. This checker preserves that scope.

AuthorityEffect: None
Firewall: stated region only; mints no authority
"""

from itertools import combinations

from sympy import I, Matrix, Rational, expand, simplify, sqrt, symbols

OMEGA = -Rational(1, 2) + I * sqrt(3) / 2


def sign_patterns(magnitude):
    """Return the 20 distinct patterns with three +n and three -n entries."""
    patterns = []
    for positive_positions in combinations(range(6), 3):
        pattern = [-magnitude] * 6
        for index in positive_positions:
            pattern[index] = magnitude
        patterns.append(tuple(pattern))
    return patterns


def displayed_affine_ansatz(x, y):
    """Return the exact ansatz encoded by ``karlssonMatrix``."""
    omega_squared = OMEGA**2
    return Matrix(
        [
            [1, 1, 1, 1, 1, 1],
            [1, -1, x, -x, y, -y],
            [1, 1, OMEGA, OMEGA, omega_squared, omega_squared],
            [1, -1, OMEGA * x, -OMEGA * x, omega_squared * y, -omega_squared * y],
            [1, 1, omega_squared, omega_squared, OMEGA, OMEGA],
            [1, -1, omega_squared * x, -omega_squared * x, OMEGA * y, -OMEGA * y],
        ]
    )


def signed_laurent_sum(matrix, pattern):
    """Compute ``sum_j prod_k matrix[k,j]**pattern[k]`` exactly."""
    total = 0
    for column in range(6):
        product = 1
        for row in range(6):
            product *= matrix[row, column] ** pattern[row]
        total += product
    return simplify(expand(total))


def verify_magnitude(matrix, magnitude):
    """Return every nonzero result; an empty list is a complete pass."""
    failures = []
    for pattern in sign_patterns(magnitude):
        result = signed_laurent_sum(matrix, pattern)
        if result != 0:
            failures.append((pattern, result))
    return failures


def main():
    x, y = symbols("x y", nonzero=True)
    matrix = displayed_affine_ansatz(x, y)

    all_failures = []
    for magnitude, label in ((1, "gamma_1"), (3, "gamma_2")):
        failures = verify_magnitude(matrix, magnitude)
        print(f"{label}: {20 - len(failures)}/20 exact symbolic zeros")
        all_failures.extend((label, pattern, result) for pattern, result in failures)

    if all_failures:
        for label, pattern, result in all_failures:
            print(f"NONZERO {label} {pattern}: {result}")
        raise SystemExit(1)

    broken_pair = matrix.copy()
    broken_pair[1, 1] = 1
    if not verify_magnitude(broken_pair, 1):
        raise RuntimeError("discriminant failed to detect a broken column pair")

    print("discriminant: broken column pair detected")
    print("Scope: displayed two-phase affine ansatz only; no full-family identification.")


if __name__ == "__main__":
    main()
