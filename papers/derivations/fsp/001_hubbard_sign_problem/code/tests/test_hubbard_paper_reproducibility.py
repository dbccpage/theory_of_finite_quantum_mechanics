"""Reproducibility tests for the Fermi-Hubbard sign-problem deposit.

These checks replay the finite witnesses recorded in paper.md.
"""

from __future__ import annotations

import sys
from fractions import Fraction
from pathlib import Path

import pytest

CODE_DIR = Path(__file__).resolve().parents[1]
if str(CODE_DIR) not in sys.path:
    sys.path.insert(0, str(CODE_DIR))

import hubbard_exact_model as hem

RING = [(0, 1), (1, 2), (2, 3), (0, 3)]
STAR = [(0, 1), (0, 2), (0, 3)]
OPEN = [(0, 1), (1, 2), (2, 3)]
TRIANGLE = [(0, 1), (1, 2), (0, 2)]


def test_approximate_inputs_are_rejected():
    with pytest.raises((TypeError, ValueError)):
        hem.rational(1.0)
    with pytest.raises((TypeError, ValueError)):
        hem.rational("1.0e-3")


def test_occupation_gauge_open_chain_succeeds():
    res = hem.run_occupation_analysis(4, OPEN, 2, 1)
    assert res["basis_states"] == 24
    assert res["diagonal_sign_gauge"] is True
    assert res["negative_cycle"] is None
    assert all(sign == 1 for _, sign in res["gauge"])


def test_occupation_gauge_ring_and_star_obstructed():
    res_ring = hem.run_occupation_analysis(4, RING, 2, 1)
    assert res_ring["diagonal_sign_gauge"] is False
    assert res_ring["negative_cycle"] == [19, 21, 22, 26, 19]

    res_star = hem.run_occupation_analysis(4, STAR, 2, 1)
    assert res_star["diagonal_sign_gauge"] is False
    assert res_star["negative_cycle"] == [19, 22, 21, 28, 25, 26, 19]


def test_kinetic_suzuki_palindromic_symmetry():
    con = hem.connection()
    matrix = hem.kinetic_matrix(con, 4, RING, "3/2")
    eta = [1, -1, 1, -1]
    inverse = [[eta[i] * matrix[i][j] * eta[j] for j in range(4)] for i in range(4)]
    prod = hem.sql_matrix_product(con, matrix, inverse)
    assert prod == [[Fraction(int(i == j)) for j in range(4)] for i in range(4)]


def test_gauge_cycle_independent_of_interaction():
    low = hem.run_occupation_analysis(4, RING, 2, 1, interaction="4")
    high = hem.run_occupation_analysis(4, RING, 2, 1, interaction="9")
    assert low["diagonal_sign_gauge"] is False
    assert low["negative_cycle"] == high["negative_cycle"] == [19, 21, 22, 26, 19]


def test_repulsive_half_filled_bipartite_positivity():
    summary = hem.run_auxiliary_field_analysis(4, RING, slices=2, r="3/2", hs="2", fugacity="1")
    assert summary["fields"] == 256
    assert summary["pairing_verified"] is True
    assert summary["negative_fields"] == 0
    assert summary["average_sign"] == "1"
    assert summary["particle_number_expectation"] == "4"


def test_attractive_frustrated_triangle_positivity():
    summary = hem.run_auxiliary_field_analysis(3, TRIANGLE, slices=2, r="3/2", hs="2", fugacity="3/2", attractive=True)
    assert summary["fields"] == 64
    assert summary["pairing_verified"] is True
    assert summary["negative_fields"] == 0
    assert summary["average_sign"] == "1"
    assert summary["particle_number_expectation"] == (
        "1776585892008474078571024122583556/557308765039728024001166872319977"
    )
    replay = hem.verify_direct_fock_trace(
        3, TRIANGLE, slices=2, r="3/2", hs="2", fugacity="3/2", attractive=True
    )
    assert replay["trace_matches"] is True
    assert replay["number_matches"] is True
    assert replay["particle_number_expectation"] == summary["particle_number_expectation"]


def test_auxiliary_to_fock_trace_reconstruction():
    rep = hem.verify_direct_fock_trace(2, [(0, 1)], slices=2, r="3/2", hs="2", fugacity="3/2", attractive=False)
    assert rep["trace_matches"] is True
    assert rep["number_matches"] is True
    assert rep["direct_trace"] == "172283601361/21233664"
    assert rep["particle_number_expectation"] == "412347680162/172283601361"

    att = hem.verify_direct_fock_trace(2, [(0, 1)], slices=2, r="3/2", hs="2", fugacity="3/2", attractive=True)
    assert att["trace_matches"] is True
    assert att["number_matches"] is True
    assert att["direct_trace"] == "180365586961/21233664"
    assert att["particle_number_expectation"] == "452633269922/180365586961"


def test_explicit_negative_field_existence_witnesses():
    res_ring = hem.run_auxiliary_field_analysis(4, RING, slices=4, r="2", hs="8", fugacity="2", field_masks=[15721])
    assert res_ring["negative_fields"] == 1
    assert res_ring["selected_subset_average_sign"] == "-1"
    witness = res_ring["first_negative"]
    assert witness["mask"] == 15721
    assert witness["up"] == "11072073737867929807204939234025/2305843009213693952"
    assert witness["down"] == "-1034021712177776419381618902295/147573952589676412928"

    res_tri = hem.run_auxiliary_field_analysis(3, TRIANGLE, slices=4, r="2", hs="8", fugacity="1", field_masks=[1281])
    assert res_tri["negative_fields"] == 1
    assert res_tri["selected_subset_average_sign"] == "-1"
    assert res_tri["pairing_verified"] is False
    triangle = res_tri["first_negative"]
    assert triangle["mask"] == 1281
    assert triangle["up"] == "2661572208368287551525625/9223372036854775808"
    assert triangle["down"] == "-323903084369592224375/35184372088832"
