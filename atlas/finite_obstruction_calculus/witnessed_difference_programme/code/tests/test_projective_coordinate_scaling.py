"""Test bit-length growth under exact projective coordinate scaling (homogeneous integer arithmetic).

Evaluates whether row-wise clearing of denominators avoids Phase 1 common denominator swell.
AuthorityEffect: None.
"""

from fractions import Fraction
import random
import pytest

from witnessed_difference.cochains import FiniteComplex
from witnessed_difference.obstruction import (
    DEFAULT_PIVOT_BUDGET,
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


@pytest.mark.parametrize("n", [6, 8, 10, 12])
def test_projective_clearing_avoids_phase1_denominator_swell(n: int):
    """Verify that projective row-wise denominator clearing eliminates O(m * B) Phase 1 swell."""
    bit_length = 64
    rng = random.Random(42 + n * 100)
    vertices = tuple(f"v{i}" for i in range(n))
    edges = tuple((f"v{i}", f"v{j}") for i in range(n) for j in range(i + 1, n))
    comp = FiniteComplex(vertices, edges)
    m = len(edges)
    width = len(vertices)
    w = (Fraction(1),) * m

    # Generate random rational edge cochain with 64-bit numerators and denominators
    cochain = [
        Fraction(rng.randint(-(1 << bit_length), 1 << bit_length), rng.randint(1, 1 << bit_length))
        for _ in edges
    ]

    d = d0_matrix(comp)

    # 1. Standard rational constraint matrix
    rows_std = [
        list(row) + [-entry for entry in row] + [Fraction(int(i == k)) for k in range(m)]
        + [-Fraction(int(i == k)) for k in range(m)]
        for i, row in enumerate(d)
    ]
    costs = [Fraction(0)] * (2 * width) + list(w) + list(w)

    # 2. Projective / row-cleared formulation: multiply row i by denominator of cochain[i]
    rows_proj = []
    cochain_proj = []
    for i in range(m):
        q_i = cochain[i].denominator
        rows_proj.append([q_i * val for val in rows_std[i]])
        cochain_proj.append(cochain[i].numerator)  # Pure integer RHS!

    # Initial Phase 1 objective row bit-length comparison
    std_phase1_obj_sum = sum((abs(x) for x in cochain), start=Fraction(0))
    std_phase1_bits = max(std_phase1_obj_sum.numerator.bit_length(), std_phase1_obj_sum.denominator.bit_length())

    proj_phase1_obj_sum = sum((abs(b.numerator) for b in cochain), start=0)
    proj_phase1_bits = proj_phase1_obj_sum.bit_length()

    # Assert dramatic bit-length reduction at initialization
    assert proj_phase1_bits <= bit_length + (m.bit_length() + 2)
    assert std_phase1_bits >= (m // 2) * (bit_length // 2)  # Swells as O(m * B)

    reduction_factor = std_phase1_bits / proj_phase1_bits
    assert reduction_factor >= 5.0, f"Expected >= 5x reduction, got {reduction_factor:.2f}x"

    # Solve both formulations
    solved_std = solve_standard_lp(costs, rows_std, cochain, max_pivots=DEFAULT_PIVOT_BUDGET)
    solved_proj = solve_standard_lp(costs, rows_proj, cochain_proj, max_pivots=DEFAULT_PIVOT_BUDGET)

    assert isinstance(solved_std, Accepted)
    assert isinstance(solved_proj, Accepted)

    # Both must pass primal/dual verification
    assert verify_standard_lp(costs, rows_std, cochain, solved_std.value)
    assert verify_standard_lp(costs, rows_proj, cochain_proj, solved_proj.value)

    # Solutions must yield identical exact optimal value
    assert solved_std.value.value == solved_proj.value.value
