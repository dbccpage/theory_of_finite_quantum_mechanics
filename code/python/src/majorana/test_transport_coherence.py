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
    res1 = chi_F(0.0, None)
    assert res1 is True

    res2 = chi_F(0.5, None)
    assert isinstance(res2, RefusedTransport)


def test_chi_box_square_commuting():
    box = ChiBoxSquare(
        chi_h_top=lambda x: x + 1,
        chi_h_bottom=lambda x: x + 2,
        chi_v_left=lambda x: x * 2,
        chi_v_right=lambda x: x * 2,
    )
    assert box.verify(5) is True

    bad_box = ChiBoxSquare(
        chi_h_top=lambda x: x + 1,
        chi_h_bottom=lambda x: x + 1,
        chi_v_left=lambda x: x * 2,
        chi_v_right=lambda x: x * 2,
    )
    res = bad_box.verify(5)
    assert isinstance(res, DiagonalTransportRefusal)


def test_triangle_witness():
    tw = TriangleWitness(
        [
            lambda x: x + 1,
            lambda x: (x + 1) * 2,
            lambda x: x * 2,
        ]
    )
    assert tw.verify(10) is True

    bad_tw = TriangleWitness(
        [
            lambda x: x + 1,
            lambda x: x * 2,
            lambda x: x * 2,
        ]
    )
    assert bad_tw.verify(10) is False


def test_pentagon_witness():
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
            lambda x: x + 4,
            lambda x: x * 2,
            lambda x: x + 3,
        ]
    )
    assert bad_pw.verify(10) is False


