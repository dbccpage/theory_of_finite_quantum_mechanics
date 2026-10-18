"""Tests for Majorana modes and Clifford algebra anticommutation."""

from fractions import Fraction
from src.majorana.majorana_modes import (
    MajoranaMonomial,
    MajoranaOperator,
    anticommutator,
    commutator,
    kitaev_chain_parity,
)


def test_majorana_clifford_relations():
    # gamma_0, gamma_1, gamma_2
    g0 = MajoranaOperator.mode(0)
    g1 = MajoranaOperator.mode(1)

    # gamma_0^2 = 1
    g0_sq = g0.multiply(g0)
    assert g0_sq.is_scalar()
    assert g0_sq.scalar_value() == Fraction(1)

    # {gamma_0, gamma_1} = 0
    anticomm_01 = anticommutator(g0, g1)
    assert anticomm_01.is_zero()

    # {gamma_0, gamma_0} = 2
    anticomm_00 = anticommutator(g0, g0)
    assert anticomm_00.is_scalar()
    assert anticomm_00.scalar_value() == Fraction(2)


def test_braid_generator_action():
    # Braid tau = (1 + gamma_0 gamma_1) / 2
    g0 = MajoranaOperator.mode(0)
    g1 = MajoranaOperator.mode(1)
    g01 = g0.multiply(g1)

    # g01 squared = (gamma_0 gamma_1)^2 = -1
    g01_sq = g01.multiply(g01)
    assert g01_sq.is_scalar()
    assert g01_sq.scalar_value() == Fraction(-1)


def test_kitaev_chain_parity_commutes_with_quadratic_terms():
    # 2 sites -> 4 Majorana modes (0, 1, 2, 3)
    parity = kitaev_chain_parity(2)

    # Intra-site coupling h_intra = gamma_0 gamma_1
    h_intra = MajoranaOperator.mode(0).multiply(MajoranaOperator.mode(1))
    comm_intra = commutator(parity, h_intra)
    assert comm_intra.is_zero()

    # Inter-site coupling h_inter = gamma_1 gamma_2
    h_inter = MajoranaOperator.mode(1).multiply(MajoranaOperator.mode(2))
    comm_inter = commutator(parity, h_inter)
    assert comm_inter.is_zero()
