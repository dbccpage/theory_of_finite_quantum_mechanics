"""Seeded finite checks of rational coefficient growth and final LP certificate sizes.

# Executable finite evidence; AuthorityEffect: None.
"""

from fractions import Fraction
import random
import pytest

from witnessed_difference.cochains import FiniteComplex
from witnessed_difference.obstruction import (
    DEFAULT_PIVOT_BUDGET,
    _exact_matrix,
    _exact_vector,
    _pivot,
    d0_matrix,
    solve_standard_lp,
    verify_standard_lp,
)
from witnessed_difference.outcomes import Accepted


def _max_bits_in_matrix(matrix: list[list[Fraction]]) -> int:
    max_b = 0
    for row in matrix:
        for val in row:
            if val != 0:
                max_b = max(max_b, val.numerator.bit_length(), val.denominator.bit_length())
    return max_b


def _generate_kn_test_cochain(n: int, bit_len: int, seed: int = 123) -> tuple[FiniteComplex, list[Fraction]]:
    rng = random.Random(seed + n * 100)
    vertices = tuple(f"v{i}" for i in range(n))
    edges = tuple((f"v{i}", f"v{j}") for i in range(n) for j in range(i + 1, n))
    comp = FiniteComplex(vertices, edges)
    cochain = [
        Fraction(rng.randint(-(1 << bit_len), 1 << bit_len), rng.randint(1, 1 << bit_len))
        for _ in edges
    ]
    return comp, cochain


@pytest.mark.parametrize("n", [4, 6, 8])
def test_gaussian_elimination_seeded_growth(n: int):
    """Check the observed 3.5x threshold on these three seeded Gaussian-elimination fixtures."""
    input_bits = 64
    comp, cochain = _generate_kn_test_cochain(n, input_bits)
    d = d0_matrix(comp)
    m = len(d)
    cols = len(comp.vertices)

    aug = [list(row) + [cochain[i]] for i, row in enumerate(d)]
    init_bits = _max_bits_in_matrix(aug)
    peak_bits = init_bits

    lead = 0
    for r in range(m):
        if lead >= cols:
            break
        i = r
        while aug[i][lead] == 0:
            i += 1
            if i == m:
                i = r
                lead += 1
                if lead == cols:
                    break
        if lead == cols:
            break

        aug[i], aug[r] = aug[r], aug[i]
        scale = aug[r][lead]
        if scale != 1:
            aug[r] = [val / scale for val in aug[r]]
            peak_bits = max(peak_bits, _max_bits_in_matrix(aug))

        for other_idx in range(m):
            if other_idx != r and aug[other_idx][lead] != 0:
                factor = aug[other_idx][lead]
                aug[other_idx] = [val - factor * p_val for val, p_val in zip(aug[other_idx], aug[r])]
                peak_bits = max(peak_bits, _max_bits_in_matrix(aug))
        lead += 1

    growth = peak_bits / max(1, init_bits)
    # This is a fixture threshold, not a universal bit-complexity theorem.
    assert growth <= 3.5, f"Gaussian bit growth {growth:.2f}x exceeds the recorded fixture threshold on K_{n}"


@pytest.mark.parametrize("n", [4, 6, 8])
def test_simplex_final_certificate_bitlength(n: int):
    """Measure final primal/dual coordinates on these fixtures; intermediate tableau sizes are not measured."""
    input_bits = 32
    comp, cochain = _generate_kn_test_cochain(n, input_bits)
    d = d0_matrix(comp)
    m = len(d)
    width = len(comp.vertices)
    w = (Fraction(1),) * m

    rows = [
        list(row) + [-entry for entry in row] + [Fraction(int(i == k)) for k in range(m)]
        + [-Fraction(int(i == k)) for k in range(m)]
        for i, row in enumerate(d)
    ]
    costs = [Fraction(0)] * (2 * width) + list(w) + list(w)

    solved = solve_standard_lp(costs, rows, cochain, max_pivots=DEFAULT_PIVOT_BUDGET)
    assert isinstance(solved, Accepted)
    assert verify_standard_lp(costs, rows, cochain, solved.value)

    # Recorded final-certificate threshold for the seeded instances.
    sol_bits = max(
        _max_bits_in_matrix([[v] for v in solved.value.primal]),
        _max_bits_in_matrix([[v] for v in solved.value.dual]),
    )
    # No universal growth bound is inferred from this finite sample.
    assert sol_bits <= (m + 5) * input_bits
