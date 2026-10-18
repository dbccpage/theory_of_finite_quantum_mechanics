"""Tests for Local-Green / Global-Red (LGGR) path-kernel gluing and cyclic parity obstructions."""

from fractions import Fraction
from src.local_green_global_red_lggr.lggr_presheaf import (
    evaluate_cyclic_parity_lggr,
    evaluate_path_kernel_gluing,
)


def test_path_kernel_exact_vs_defective_gluing() -> None:
    k_ab = ((Fraction(1, 2), Fraction(1, 2)), (Fraction(0), Fraction(1)))
    k_bc = ((Fraction(1), Fraction(0)), (Fraction(1, 3), Fraction(2, 3)))
    exact_ac = ((Fraction(1, 2), Fraction(1, 2)), (Fraction(1, 6), Fraction(5, 6)))
    broken_ac = ((Fraction(1, 2), Fraction(0)), (Fraction(1, 6), Fraction(5, 6)))

    assert evaluate_path_kernel_gluing(k_ab, k_bc, exact_ac) == Fraction(0)
    assert evaluate_path_kernel_gluing(k_ab, k_bc, broken_ac) == Fraction(1, 2)


def test_cyclic_parity_local_green_global_red() -> None:
    even_cycle = evaluate_cyclic_parity_lggr([1, 1, 0])
    assert even_cycle.local_green is True
    assert even_cycle.global_red is False
    assert even_cycle.holonomy_residue == 0

    odd_cycle = evaluate_cyclic_parity_lggr([1, 1, 1])
    assert odd_cycle.local_green is True
    assert odd_cycle.global_red is True
    assert odd_cycle.holonomy_residue == 1
    assert odd_cycle.gluing_defect_l1 == Fraction(1)
