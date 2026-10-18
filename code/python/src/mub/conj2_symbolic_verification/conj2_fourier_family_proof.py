#!/usr/bin/env python3
"""Symbolically check Conjecture 2(a) on the Fourier family F6(x, y).

The matrices checked here are the unimodular Fourier-family matrices
themselves. The script does not claim that an arbitrary product
F6(x1, y1)^* F6(x2, y2) is a complex Hadamard transition matrix.
"""

import sys
from itertools import combinations

from sympy import (
    I,
    Matrix,
    Rational,
    exp,
    expand,
    simplify,
    sqrt,
    symbols,
    trigsimp,
)


ETA = -Rational(1, 2) + I * sqrt(3) / 2


def f3_matrix():
    return Matrix(3, 3, lambda row, col: ETA ** (row * col))


def f6_unnormalized(x, y):
    """Return the entrywise-unimodular Fourier-family matrix F6(x, y)."""
    f3 = f3_matrix()
    diagonal = Matrix.diag(1, exp(I * x), exp(I * y))
    phased_f3 = diagonal * f3
    top = f3.row_join(phased_f3)
    bottom = f3.row_join(-phased_f3)
    return top.col_join(bottom)


def gamma1_permutations():
    permutations = []
    for positive_positions in combinations(range(6), 3):
        gamma = [-1] * 6
        for index in positive_positions:
            gamma[index] = 1
        permutations.append(tuple(gamma))
    return permutations


def compute_laurent_sum(matrix, gamma):
    """Compute sum_j prod_k H[k,j]**gamma[k] using Laurent powers."""
    total = 0
    for column in range(6):
        product = 1
        for row in range(6):
            product *= matrix[row, column] ** gamma[row]
        total += product
    return total


def main():
    x, y = symbols("x y", real=True)
    matrix = f6_unnormalized(x, y)
    permutations = gamma1_permutations()

    print(
        "Verifying G_{F6(x,y)}(gamma) = 0 for "
        f"all {len(permutations)} permutations of gamma_1:"
    )
    all_zero = True
    for index, gamma in enumerate(permutations, start=1):
        sys.stdout.write(f"  Perm {index:2d}/20: {gamma}  =>  ")
        sys.stdout.flush()

        inner_sum = compute_laurent_sum(matrix, gamma)
        result = simplify(expand(inner_sum))
        if result != 0:
            result = simplify(trigsimp(result))

        if result == 0:
            print("F_S = 0   [ZERO]")
        else:
            print(f"F_S = {result}")
            all_zero = False

    print()
    if all_zero:
        print("RESULT: Conjecture 2(a) holds symbolically on F6(x, y).")
        print("Scope: the Fourier-family CHMs themselves, for all real x and y.")
        return

    print("RESULT: at least one gamma_1 permutation did not simplify to zero.")
    raise SystemExit(1)


if __name__ == "__main__":
    main()
