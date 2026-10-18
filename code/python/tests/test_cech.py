"""Tests for Čech cochain complex and cohomology."""

from fractions import Fraction
from src.sheaf_theory.cech import (
    OpenSet,
    CechCochain,
    cech_coboundary_rational,
    compute_cech_h0,
    is_1_cocycle,
)


def test_open_set_intersections():
    u0 = OpenSet.from_iterable([1, 2, 3])
    u1 = OpenSet.from_iterable([2, 3, 4])
    u2 = OpenSet.from_iterable([5, 6])

    inter01 = u0.intersection(u1)
    assert not inter01.is_empty()
    assert inter01.points == frozenset([2, 3])

    inter02 = u0.intersection(u2)
    assert inter02.is_empty()


def test_cech_h0_constant_sheaf():
    # 3 pairwise overlapping open sets covering a connected space
    u0 = OpenSet.from_iterable([0, 1])
    u1 = OpenSet.from_iterable([1, 2])
    u2 = OpenSet.from_iterable([2, 0])
    cover = [u0, u1, u2]

    # Constant 0-cochain
    h0 = compute_cech_h0(cover, Fraction(7, 3))
    assert h0 is not None
    assert h0.get((0,)) == Fraction(7, 3)
    assert h0.get((1,)) == Fraction(7, 3)
    assert h0.get((2,)) == Fraction(7, 3)


def test_cech_coboundary_nilpotence():
    # delta^2 circ delta^1 = 0 on any 0-cochain
    u0 = OpenSet.from_iterable([0, 1, 2])
    u1 = OpenSet.from_iterable([1, 2, 3])
    u2 = OpenSet.from_iterable([2, 3, 0])
    cover = [u0, u1, u2]

    # Non-constant 0-cochain
    c0 = CechCochain(0, {
        (0,): Fraction(1),
        (1,): Fraction(2),
        (2,): Fraction(5),
    })

    # 1-cochain delta c0
    d_c0 = cech_coboundary_rational(c0, cover)
    assert not d_c0.is_zero()

    # 2-cochain delta(delta c0) must be identically zero by d^2 = 0
    d2_c0 = cech_coboundary_rational(d_c0, cover)
    assert d2_c0.is_zero()
    assert is_1_cocycle(d_c0, cover) is True
