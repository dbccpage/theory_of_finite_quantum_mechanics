"""Exact formula, separation, and calibration-mutation checks; not an SVD proof."""
from fractions import Fraction as Q
from itertools import product

import pytest
from src.linear_algebra.scalars import GaussianRational as G, ScalarError
from src.qm import tensor_composition as t


@pytest.mark.parametrize("d", [1, 2, 3, 4])
def test_fiducial_projectors_are_a_real_basis(d):
    basis = t.fiducial_projectors(d)
    assert len(basis) == d * d
    assert all(t.multiply(p, p) == p and t.trace(p) == 1 for p in basis)
    assert t.real_rank([t.hermitian_coordinates(p) for p in basis]) == d * d


@pytest.mark.parametrize("n,m", [(1, 3), (2, 2), (2, 3), (3, 2)])
def test_product_statistics_span_full_hermitian_coordinates(n, m):
    basis = [t.tensor(a, b) for a in t.fiducial_projectors(n) for b in t.fiducial_projectors(m)]
    assert t.real_rank([t.hermitian_coordinates(p) for p in basis]) == (n * m) ** 2


@pytest.mark.parametrize("n,m", [(1, 1), (1, 3), (2, 2), (2, 3), (3, 2), (3, 5)])
def test_controlled_shift_is_unitary_with_the_stated_action(n, m):
    c = t.controlled_shift(n, m)
    assert t.multiply(t.adjoint(c), c) == t.identity(n * m)
    for a, b in product(range(n), range(m)):
        inp = t.outer([int(j == a * m + b) for j in range(n * m)])
        out = t.outer([int(j == a * m + (a + b) % m) for j in range(n * m)])
        assert t.conjugate(c, inp) == out


@pytest.mark.parametrize("coeff,m", [([G(Q(3, 5)), G(0, Q(4, 5))], 3),
                                    ([G(Q(1, 3)), G(Q(2, 3)), G(0, Q(2, 3))], 5)])
def test_controlled_shift_prepares_declared_schmidt_coefficients(coeff, m):
    n = len(coeff)
    assert sum(z.norm_sq() for z in coeff) == 1
    inp = t.tensor(t.outer(coeff), t.outer([1] + [0] * (m - 1)))
    target = [coeff[a] if a == b else G(0) for a in range(n) for b in range(m)]
    assert t.conjugate(t.controlled_shift(n, m), inp) == t.outer(target)


def bell_and_swap():
    bell = t.scale(Q(1, 2), t.outer([1, 0, 0, 1]))
    swap = t.partial_transpose_first(bell, 2, 2)
    return bell, swap


def test_minimum_cone_excluded_by_one_coherent_gate():
    bell, swap = bell_and_swap()
    separable = t.tensor(t.scale(Q(1, 2), t.outer([1, 1])), t.outer([1, 0]))
    assert t.conjugate(t.controlled_shift(2, 2), separable) == bell
    # Partial transpose of every separable positive operator is PSD.
    assert t.quadratic(swap, [0, 1, -1, 0]) == -1


def test_maximum_cone_witness_has_positive_product_tests_but_negative_orbit_test():
    _, swap = bell_and_swap()
    vectors = [[1, 0], [0, 1], [1, 1], [1, G(0, 1)], [Q(3, 5), Q(4, 5)]]
    for a, b in product(vectors, repeat=2):
        overlap = sum(G(x).conjugate() * y for x, y in zip(a, b))
        ab = [G(x) * y for x in a for y in b]
        assert t.quadratic(swap, ab) == overlap.norm_sq() / 2
    c = t.controlled_shift(2, 2)
    # This product seed is mapped to the antisymmetric vector by C.
    assert t.quadratic(t.conjugate(t.adjoint(c), swap), [0, 1, 0, -1]) == -1


def test_full_calibration_rejects_twisted_gate_despite_same_classical_truth_table():
    c = t.controlled_shift(2, 2)
    ordinary = lambda s: t.conjugate(c, s)
    twisted = lambda s: t.twisted_gate(c, s, 2, 2)
    for k in range(4):
        classical = t.outer([int(j == k) for j in range(4)])
        assert ordinary(classical) == twisted(classical)
    assert t.calibration_table(ordinary, 2, 2) != t.calibration_table(twisted, 2, 2)
    bell, swap = bell_and_swap()
    assert t.partial_transpose_first(swap, 2, 2) == bell


def test_dephasing_mutation_passes_truth_table_but_fails_coherent_calibration():
    c = t.controlled_shift(2, 2)
    ordinary = lambda s: t.conjugate(c, s)
    def dephased(s):
        a = ordinary(s)
        return t.matrix([[a[i][j] if i == j else 0 for j in range(4)] for i in range(4)])
    for k in range(4):
        classical = t.outer([int(j == k) for j in range(4)])
        assert ordinary(classical) == dephased(classical)
    assert t.calibration_table(ordinary, 2, 2) != t.calibration_table(dephased, 2, 2)


def test_exact_input_and_shape_boundaries():
    with pytest.raises(ScalarError):
        t.matrix([[0.5]])
    with pytest.raises(ScalarError):
        t.matrix([[True]])
    for d in (0, -1, True, 2.0):
        with pytest.raises(ValueError):
            t.controlled_shift(d, 2)
    with pytest.raises(ValueError):
        t.partial_transpose_first(t.identity(3), 2, 2)
    with pytest.raises(ValueError):
        t.hermitian_coordinates([[0, G(0, 1)], [G(0, 1), 0]])
    with pytest.raises(ValueError):
        t.multiply([[1, 0]], [[1]])
    with pytest.raises(TypeError):
        t.real_rank([[0.5]])
