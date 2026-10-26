"""Exact finite and adversarial checks for §5.16; no general-proof claim."""

from dataclasses import replace
from math import comb, factorial

import pytest

sp = pytest.importorskip("sympy", reason="install the optional jets extra for exact polynomial onset checks")

from polynomial_onset import certify_onset, polynomial_lift, verify_onset  # noqa: E402


@pytest.mark.parametrize("degree", [1, 2, 3, 5])
def test_lifted_cutoff_is_sharp_and_unlifted_cutoff_is_insufficient(degree):
    # x(t)=exp(t), f(x)=(x-1)^p: onset p, although A has minimal degree one.
    f = [{(j,): (-1) ** (degree - j) * comb(degree, j) for j in range(degree + 1)}]
    certificate = certify_onset([[1]], [1], f)
    assert len(certificate.annihilator) - 1 == degree + 1
    assert certificate.first_onset == degree
    assert certificate.derivatives[-1] == (factorial(degree),)
    assert verify_onset([[1]], [1], f, certificate)


def test_persistent_rotational_invariant_with_nonstationary_trajectory():
    a, m = [[0, -1], [1, 0]], [1, 0]
    f = [{(2, 0): 1, (0, 2): 1, (0, 0): -1}]
    claim = certify_onset(a, m, f)
    assert claim.annihilator == (0, 4, 0, 5, 0, 1)
    assert claim.first_onset is None
    assert verify_onset(a, m, f, claim)


def test_constant_zero_and_kappa_one():
    claim = certify_onset([[7]], [3], [{}])
    assert claim.annihilator == (0, 1)
    assert claim.derivatives == ((0,),)
    assert claim.first_onset is None
    assert verify_onset([[7]], [3], [{}], claim)


@pytest.mark.parametrize("length", [2, 3, 5])
def test_nilpotent_chain_has_no_dimension_free_cutoff(length):
    a = sp.zeros(length)
    for j in range(length - 1):
        a[j + 1, j] = 1
    exponent = (0,) * (length - 1) + (1,)
    claim = certify_onset(a, [1] + [0] * (length - 1), [{exponent: 1}])
    assert len(claim.annihilator) == length + 1
    assert claim.first_onset == length - 1
    assert claim.derivatives[-1] == (1,)


def test_quadratic_quantum_pair_defect_against_direct_product_marginals():
    # cos(t)|00> + sin(t)|11>; coordinates are the two populations and coherence.
    a = [[0, 0, -2], [0, 0, 2], [1, -1, 0]]
    f = [
        {(1, 0, 0): 1, (2, 0, 0): -1},
        {(1, 1, 0): -1},
        {(0, 1, 0): 1, (0, 2, 0): -1},
        {(0, 0, 1): 1},
    ]
    claim = certify_onset(a, [1, 0, 0], f)
    t = sp.symbols("t", real=True)
    x, y, c = sp.cos(t) ** 2, sp.sin(t) ** 2, sp.sin(t) * sp.cos(t)
    residual = [x - x * x, -x * y, y - y * y, c]
    direct = tuple(
        tuple(sp.diff(r, t, j).subs(t, 0) for r in residual) for j in range(len(claim.derivatives))
    )
    assert claim.first_onset == 1
    assert claim.derivatives == direct
    assert verify_onset(a, [1, 0, 0], f, claim)


def test_degree_three_connected_readout():
    # Three identical classical bits, population b=1-exp(-t).
    # This generator is not two-local; no Steiner lower bound is asserted here.
    f = [{(0, 1): 1, (0, 2): -3, (0, 3): 2}]
    a, m = [[-1, 0], [1, 0]], [1, 0]
    claim = certify_onset(a, m, f)
    t = sp.symbols("t")
    b = 1 - sp.exp(-t)
    direct = b - 3 * b * b + 2 * b * b * b
    assert claim.first_onset == 1
    assert claim.derivatives == tuple(
        (sp.diff(direct, t, j).subs(t, 0),) for j in range(len(claim.derivatives))
    )
    assert verify_onset(a, m, f, claim)


def test_zero_jets_without_vector_annihilation_are_refused():
    f = [{(0,): 1, (1,): -2, (2,): 1}]
    valid = certify_onset([[1]], [1], f)
    forged = replace(valid, annihilator=(0, 0, 1), derivatives=((0,), (0,)), first_onset=None)
    assert not verify_onset([[1]], [1], f, forged)
    assert not verify_onset([[1]], [1], f, replace(valid, first_onset=None))
    assert not verify_onset([[1]], [1], f, replace(valid, derivatives=((0,),) * 3))
    assert not verify_onset([[1]], [1], f, replace(valid, annihilator=(0, 2, -3, 2)))
    assert not verify_onset([[1]], [1], f, replace(valid, annihilator=(0, 0, 2, -3, 1)))
    assert not verify_onset([[2]], [1], f, valid)
    assert not verify_onset([[1]], [1], [{(0,): -1, (1,): 1}], valid)


@pytest.mark.parametrize("bad", [0.0, True, sp.Float(1), sp.sqrt(2), sp.oo, "1"])
def test_inexact_or_unsupported_scalars_are_not_rationalized(bad):
    with pytest.raises(TypeError):
        polynomial_lift([[1]], [1], [{(1,): bad}])


@pytest.mark.parametrize("bad", [1.0, True, sp.Float(1), sp.sqrt(2), sp.oo, "1"])
@pytest.mark.parametrize("position", ["generator", "initial"])
def test_matrix_scalars_are_checked_before_sympy_can_coerce_them(bad, position):
    f = [{(0,): -1, (1,): 1}]
    valid = certify_onset([[1]], [1], f)
    a = [[bad]] if position == "generator" else [[1]]
    m = [bad] if position == "initial" else [1]
    with pytest.raises(TypeError):
        polynomial_lift(a, m, f)
    assert not verify_onset(a, m, f, valid)


@pytest.mark.parametrize("bad_row", [{0: 7, 1: 9}, {0, 1}, "01", 0])
def test_every_nested_generator_row_must_be_an_ordered_sequence(bad_row):
    f = [{(0, 0): -1, (1, 0): 1}]
    m = [1, 0]
    valid = certify_onset([[1, 0], [0, 1]], m, f)
    a = [[1, 0], bad_row]
    with pytest.raises(TypeError):
        polynomial_lift(a, m, f)
    assert not verify_onset(a, m, f, valid)


@pytest.mark.parametrize("bad_row", [{0: 9}, {0}, "0", 0])
def test_every_nested_initial_row_must_be_an_ordered_sequence(bad_row):
    a = [[1, 0], [0, 1]]
    f = [{(0, 0): -1, (1, 0): 1}]
    valid = certify_onset(a, [1, 0], f)
    with pytest.raises(TypeError):
        polynomial_lift(a, [[1], bad_row], f)
    assert not verify_onset(a, [[1], bad_row], f, valid)


def test_invalid_shapes_degrees_and_nonzero_initial_defect_are_refused():
    with pytest.raises(ValueError):
        polynomial_lift([[1, 2]], [1], [{(1,): 1}])
    with pytest.raises(ValueError):
        polynomial_lift([[1]], [1], [{(-1,): 1}])
    with pytest.raises(ValueError):
        polynomial_lift([[1]], [1], [{(True,): 1}])
    with pytest.raises(ValueError):
        polynomial_lift([[1]], [1], [{(256,): 1}])
    with pytest.raises(ValueError, match=r"f\(m\)"):
        certify_onset([[1]], [1], [{(1,): 1}])
