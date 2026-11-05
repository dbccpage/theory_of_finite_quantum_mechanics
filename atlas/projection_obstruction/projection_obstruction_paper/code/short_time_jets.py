"""Exact finite-matrix Taylor coefficients for the product-of-marginals defect.

The matrix computations below are symbolic examples, not a verification of the
general local-Hamiltonian estimates in the manuscript.
"""

from __future__ import annotations

from itertools import product
from math import comb, factorial, prod

import sympy as sp


I2 = sp.eye(2)
X = sp.Matrix([[0, 1], [1, 0]])
Y = sp.Matrix([[0, -sp.I], [sp.I, 0]])
Z = sp.diag(1, -1)
ZERO = sp.diag(1, 0)
PLUS = (I2 + X) / 2


def tensor(*matrices: sp.MatrixBase) -> sp.Matrix:
    return sp.Matrix(sp.kronecker_product(*matrices))


def partial_trace(
    matrix: sp.MatrixBase, dimensions: tuple[int, ...], keep: tuple[int, ...]
) -> sp.Matrix:
    """Trace out all other factors, retaining factors in increasing order."""
    if any(d < 1 for d in dimensions) or matrix.shape != (prod(dimensions),) * 2:
        raise ValueError("matrix shape must match positive tensor dimensions")
    if tuple(sorted(set(keep))) != keep or any(i < 0 or i >= len(dimensions) for i in keep):
        raise ValueError("retained factors must be distinct, ordered and in range")
    discarded = tuple(i for i in range(len(dimensions)) if i not in keep)
    kept_indices = list(product(*(range(dimensions[i]) for i in keep)))
    traced_indices = list(product(*(range(dimensions[i]) for i in discarded)))

    def flat(coords: list[int]) -> int:
        result = 0
        for coordinate, dimension in zip(coords, dimensions):
            result = result * dimension + coordinate
        return result

    result = sp.zeros(len(kept_indices))
    for row, left in enumerate(kept_indices):
        for col, right in enumerate(kept_indices):
            for traced in traced_indices:
                a, b = [0] * len(dimensions), [0] * len(dimensions)
                for site, x, y in zip(keep, left, right):
                    a[site], b[site] = x, y
                for site, value in zip(discarded, traced):
                    a[site] = b[site] = value
                result[row, col] += matrix[flat(a), flat(b)]
    return result.applyfunc(sp.simplify)


def state_jets(hamiltonian: sp.MatrixBase, rho: sp.MatrixBase, order: int) -> list[sp.Matrix]:
    """Return derivatives, without dividing by factorials."""
    if order < 0 or hamiltonian.shape != rho.shape or rho.rows != rho.cols:
        raise ValueError("nonnegative order and matching square matrices required")
    derivatives = [sp.Matrix(rho)]
    for _ in range(order):
        current = derivatives[-1]
        derivatives.append(
            (-sp.I * (hamiltonian * current - current * hamiltonian)).applyfunc(sp.simplify)
        )
    return derivatives


def defect_jets(
    hamiltonian: sp.MatrixBase,
    rho: sp.MatrixBase,
    dimensions: tuple[int, ...],
    edge: tuple[int, int],
    order: int,
) -> list[sp.Matrix]:
    """Return F^(j)(0), including every derivative of both moving marginals."""
    if len(edge) != 2 or edge[0] >= edge[1]:
        raise ValueError("an ordered pair of distinct sites is required")
    derivatives = state_jets(hamiltonian, rho, order)
    pairs = [partial_trace(d, dimensions, edge) for d in derivatives]
    left = [partial_trace(d, dimensions, (edge[0],)) for d in derivatives]
    right = [partial_trace(d, dimensions, (edge[1],)) for d in derivatives]
    result = []
    for j in range(order + 1):
        moving_product = sum(
            (comb(j, m) * tensor(left[m], right[j - m]) for m in range(j + 1)),
            sp.zeros(pairs[j].rows),
        )
        result.append((pairs[j] - moving_product).applyfunc(sp.simplify))
    return result


def normal_rate(
    interaction: sp.MatrixBase, rho_a: sp.MatrixBase, rho_b: sp.MatrixBase
) -> sp.Matrix:
    """Edge contribution after subtracting both one-site tangent terms."""
    pair = tensor(rho_a, rho_b)
    derivative = -sp.I * (interaction * pair - pair * interaction)
    dimensions = (rho_a.rows, rho_b.rows)
    return (
        derivative
        - tensor(partial_trace(derivative, dimensions, (0,)), rho_b)
        - tensor(rho_a, partial_trace(derivative, dimensions, (1,)))
    ).applyfunc(sp.simplify)


def remainder_bound(order: int, g: sp.Expr, t: sp.Expr) -> sp.Expr:
    """Remainder constant; the theorem requires real g,t >= 0 and order >= 0."""
    if order < 0:
        raise ValueError("nonnegative Taylor order required")
    return 2 ** (order + 2) * (order + 2) * g ** (order + 1) * t ** (order + 1)


def derivative_factor(order: int) -> int:
    if order < 0:
        raise ValueError("nonnegative derivative order required")
    return 2 ** (order + 1) * factorial(order + 1)


def exact_examples() -> dict[str, object]:
    j, h = sp.symbols("J h", real=True)
    hamiltonian = -j * tensor(Z, Z) - h * (tensor(X, I2) + tensor(I2, X))
    jets = defect_jets(hamiltonian, tensor(ZERO, ZERO), (2, 2), (0, 1), 3)
    second_order = defect_jets(
        tensor(Z, Z) + tensor(X, I2), tensor(ZERO, PLUS), (2, 2), (0, 1), 2
    )
    return {
        "ising_zero_first": str(jets[1]),
        "ising_zero_second": str(jets[2]),
        "ising_zero_third": str(jets[3]),
        "ising_zero_third_eigenvalues": str(jets[3].eigenvals()),
        "quadratic_example_first": str(second_order[1]),
        "quadratic_example_second": str(second_order[2]),
        "quadratic_example_second_eigenvalues": str(second_order[2].eigenvals()),
        "remainder_coefficients": [remainder_bound(k, 1, 1) for k in (1, 2, 3)],
    }


if __name__ == "__main__":
    import json

    print(json.dumps(exact_examples(), indent=2))
