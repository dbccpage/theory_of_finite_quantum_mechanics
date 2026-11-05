from fractions import Fraction

import pytest
from hermitianization.model import (
    GaussianRational,
    complex_scalar_action,
    gram_matrix,
    hermitian_pairing,
    matrix,
    matvec,
    require_hermitianization,
    validate_hermitianization,
    vector,
)
from hermitianization.replay import check, produce, reference_problem


def data():
    problem = reference_problem()
    observer = matrix(problem["observer_rows"])
    j = matrix(problem["complex_structure"])
    return problem, observer, j, gram_matrix(observer)


def test_declared_complex_structure_and_gram_are_admitted():
    _, observer, j, _ = data()
    result = require_hermitianization(observer, j)
    assert result.accepted
    assert result.dimension == 4


def test_sesquilinearity_replays_exactly():
    problem, _, j, g = data()
    x = vector(problem["left"])
    y = vector(problem["right"])
    z = GaussianRational.of(*problem["scalar"])
    h = hermitian_pairing(g, j, x, y)
    assert hermitian_pairing(g, j, complex_scalar_action(z, j, x), y) == z.conjugate() * h
    assert hermitian_pairing(g, j, x, complex_scalar_action(z, j, y)) == z * h


def test_diagonal_is_real_and_nonnegative():
    problem, _, j, g = data()
    x = vector(problem["left"])
    value = hermitian_pairing(g, j, x, x)
    assert value == GaussianRational.of(5)


def test_observer_kernel_is_hermitian_radical_in_fixture():
    problem, observer, j, g = data()
    blind = vector(problem["blind_difference"])
    assert all(entry == 0 for entry in matvec(observer, blind))
    for raw in ([1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]):
        assert hermitian_pairing(g, j, blind, vector(raw)) == GaussianRational.of(0)


def test_positive_form_does_not_select_orientation():
    _, observer, j, g = data()
    opposite = tuple(tuple(-value for value in row) for row in j)
    assert require_hermitianization(observer, opposite).accepted
    e0 = vector([1, 0, 0, 0])
    e1 = vector([0, 1, 0, 0])
    assert hermitian_pairing(g, j, e0, e1) == GaussianRational.of(0, 1)
    assert hermitian_pairing(g, opposite, e0, e1) == GaussianRational.of(0, -1)


def test_incompatible_form_is_refused():
    bad_observer = matrix([[1, 0], [0, 2]])
    j = matrix([[0, -1], [1, 0]])
    result = validate_hermitianization(bad_observer, j)
    assert result.complex_square
    assert not result.skew_adjoint
    assert not result.isometry
    with pytest.raises(ValueError, match="incompatible Hermitianization data"):
        require_hermitianization(bad_observer, j)


def test_source_bound_receipt_and_tamper_refusal():
    problem = reference_problem()
    receipt = produce(problem)
    check(problem, receipt)
    tampered = {**receipt, "problem_sha256": "0" * 64}
    with pytest.raises(ValueError, match="does not replay"):
        check(problem, tampered)


def test_gaussian_norm_is_multiplicative_on_exact_fractions():
    z = GaussianRational.of(Fraction(3, 5), Fraction(4, 5))
    w = GaussianRational.of(Fraction(1, 2), Fraction(-2, 3))
    assert (z * w).norm() == z.norm() * w.norm()


@pytest.mark.parametrize("scale", [1, 2])
def test_tensor_balance_does_not_select_hermitian_pairing_scale(scale):
    # Q(i) tensor Q(i) is Q(i) via x tensor u -> x*u. Both forms descend.
    one = GaussianRational.of(1)
    imaginary_unit = GaussianRational.of(0, 1)
    samples = (one, imaginary_unit, GaussianRational.of(Fraction(2, 3), Fraction(-3, 5)))

    def pairing(z, w):
        return GaussianRational.of(scale) * z.conjugate() * w

    for x in samples:
        for u in samples:
            assert (imaginary_unit * x) * u == x * (imaginary_unit * u)
            assert pairing((imaginary_unit * x) * u, one) == pairing(
                x * (imaginary_unit * u), one
            )
            assert pairing(one, (imaginary_unit * x) * u) == pairing(
                one, x * (imaginary_unit * u)
            )
            assert pairing(x * u, x * u).re > 0
            assert pairing(x * u, one) == pairing(one, x * u).conjugate()
    assert pairing(one * one, one * one) == GaussianRational.of(scale)
    product_unit_pairing = one.conjugate() * one * one.conjugate() * one
    assert (pairing(one, one) == product_unit_pairing) == (scale == 1)


def test_boolean_entries_and_bad_enumeration_bounds_are_refused():
    with pytest.raises(TypeError, match="unsupported rational"):
        vector([True, 0])
    with pytest.raises(TypeError, match="unsupported rational"):
        GaussianRational.of(True)
    problem = reference_problem()
    for bad in (True, 1.5, -1):
        changed = {**problem, "enumeration_bound": bad}
        with pytest.raises(ValueError, match="nonnegative integer"):
            produce(changed)
