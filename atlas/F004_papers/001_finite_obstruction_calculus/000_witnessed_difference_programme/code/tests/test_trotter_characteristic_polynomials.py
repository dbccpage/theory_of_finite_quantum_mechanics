"""Unit tests for trotter_characteristic_polynomials; AuthorityEffect: None."""

import sympy as sp
from trotter_characteristic_polynomials import (
    closed_form_lambda_stag_m1,
    closed_form_lambda_stag_m2,
    compute_exact_response_matrix,
)


def test_closed_form_m1_at_one_tenth():
    """Verify closed form for M=1 at r=1/10 against exact arithmetic."""
    r = sp.Rational(1, 10)
    val = closed_form_lambda_stag_m1(r)
    expected = sp.Rational(-1, 706440)
    assert val == expected


def test_closed_form_m2_at_one_tenth():
    """Verify closed form for M=2 at r=1/10 against exact arithmetic."""
    r = sp.Rational(1, 10)
    val = closed_form_lambda_stag_m2(r)
    expected = sp.Rational(-35281, 90644998440)
    assert val == expected


def test_exact_response_matrix_m1():
    """Test exact response matrix at M=1: dimension, zero modes, and negative eigenvalue."""
    res = compute_exact_response_matrix(1, sp.Rational(1, 10))
    assert res['dim_G'] == 8
    assert res['zero_modes'] == 3  # 4M - 1
    assert res['negative_count'] == 1
    assert sp.Rational(res['rayleigh_stag']) == sp.Rational(-1, 706440)
    assert res['eigenvalues']['-1/706440'] == 1


def test_exact_response_matrix_m2():
    """Test exact response matrix at M=2: dimension, zero modes, and negative eigenvalue."""
    res = compute_exact_response_matrix(2, sp.Rational(1, 10))
    assert res['dim_G'] == 16
    assert res['zero_modes'] == 7  # 4M - 1
    assert res['negative_count'] == 1
    assert sp.Rational(res['rayleigh_stag']) == sp.Rational(-35281, 90644998440)
    assert res['eigenvalues']['-35281/90644998440'] == 1


def test_exact_response_matrix_m3():
    """Test exact response matrix at M=3: dimension, zero modes, and negative eigenvalue."""
    res = compute_exact_response_matrix(3, sp.Rational(1, 10))
    assert res['dim_G'] == 24
    assert res['zero_modes'] == 11  # 4M - 1
    assert res['negative_count'] == 1
    assert sp.Rational(res['rayleigh_stag']) == sp.Rational(-12188547841, 55802492242070440)
    assert res['eigenvalues']['-12188547841/55802492242070440'] == 1


def test_exact_response_matrix_m4():
    """Test exact response matrix at M=4: 15 zero modes (4M-1) and strictly 1 negative mode."""
    res = compute_exact_response_matrix(4, sp.Rational(1, 10))
    assert res['dim_G'] == 32
    assert res['zero_modes'] == 15  # 4M - 1 = 15
    assert res['negative_count'] == 1
    expected_rayleigh = sp.Rational(-14588472130734881, 95169874374532062745640)
    assert sp.Rational(res['rayleigh_stag']) == expected_rayleigh


def test_staggered_negative_variance_decay():
    """Closed forms at r=1/10 are negative, and the M=2 value is smaller in magnitude."""
    r = sp.Rational(1, 10)
    m1 = closed_form_lambda_stag_m1(r)
    m2 = closed_form_lambda_stag_m2(r)
    assert m1 < 0
    assert m2 < 0
    assert abs(m1) > abs(m2)
