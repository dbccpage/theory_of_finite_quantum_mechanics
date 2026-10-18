"""Tests for CODA-MUR transport coherence (chi_F, ChiBoxSquare, TriangleWitness, PentagonWitness)."""

from omega_engine.crates.operator.transforms.transport import (
    chi_F,
    ChiBoxSquare,
    TriangleWitness,
    PentagonWitness,
    RefusedTransport,
    DiagonalTransportRefusal,
)


def test_chi_F_licensing():
    # q_F == 0 is licensed
    res1 = chi_F(0.0, None)
    assert res1 is True

    # q_F != 0 is refused
    res2 = chi_F(0.5, None)
    assert isinstance(res2, RefusedTransport)


def test_chi_box_square_commuting():
    # Commuting square: horizontal top and bottom, vertical left and right
    # Let's define simple functions: f(x) = x + 1, g(x) = x * 2
    # chi_h_top = +1, chi_v_right = *2  =>  (x + 1) * 2 = 2x + 2
    # chi_v_left = *2, chi_h_bottom = +2 =>  (x * 2) + 2 = 2x + 2
    box = ChiBoxSquare(
        chi_h_top=lambda x: x + 1,
        chi_h_bottom=lambda x: x + 2,
        chi_v_left=lambda x: x * 2,
        chi_v_right=lambda x: x * 2,
    )
    assert box.verify(5) is True

    # Non-commuting square:
    # chi_h_bottom = +1  =>  (x * 2) + 1 = 2x + 1 != 2x + 2
    bad_box = ChiBoxSquare(
        chi_h_top=lambda x: x + 1,
        chi_h_bottom=lambda x: x + 1,
        chi_v_left=lambda x: x * 2,
        chi_v_right=lambda x: x * 2,
    )
    res = bad_box.verify(5)
    assert isinstance(res, DiagonalTransportRefusal)


def test_triangle_witness():
    # Triangle: map2 o map0 == map1
    # map0: x -> x + 1
    # map2: x -> x * 2
    # map1: x -> (x + 1) * 2
    tw = TriangleWitness(
        [
            lambda x: x + 1,
            lambda x: (x + 1) * 2,
            lambda x: x * 2,
        ]
    )
    assert tw.verify(10) is True

    # Non-cohering triangle
    bad_tw = TriangleWitness(
        [
            lambda x: x + 1,
            lambda x: x * 2,
            lambda x: x * 2,
        ]
    )
    assert bad_tw.verify(10) is False


def test_pentagon_witness():
    # Pentagon identity: maps[4] o maps[3] o maps[0] == maps[2] o maps[1]
    # Let:
    # maps[0]: x -> x + 1
    # maps[3]: x -> x * 2
    # maps[4]: x -> x + 3
    # Left side: ((x + 1) * 2) + 3 = 2x + 5
    # maps[1]: x -> x * 2
    # maps[2]: x -> x + 5
    # Right side: (x * 2) + 5 = 2x + 5
    pw = PentagonWitness(
        [
            lambda x: x + 1,
            lambda x: x * 2,
            lambda x: x + 5,
            lambda x: x * 2,
            lambda x: x + 3,
        ]
    )
    assert pw.verify(10) is True

    bad_pw = PentagonWitness(
        [
            lambda x: x + 1,
            lambda x: x * 2,
            lambda x: x + 4,  # bad transition
            lambda x: x * 2,
            lambda x: x + 3,
        ]
    )
    assert bad_pw.verify(10) is False


