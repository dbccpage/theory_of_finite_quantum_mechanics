from dataclasses import replace
from fractions import Fraction
from itertools import product

import pytest
from witnessed_difference.exact_linear import (
    CongruenceCertificate,
    ExactField,
    adjoint,
    apply,
    coerce_matrix,
    coerce_vector,
    congruence_diagonalize,
    constant,
    identity,
    inner,
    inverse,
    kernel_basis,
    matmul,
    rank,
    scale,
    solve,
    subtract,
    verify_congruence,
    zero_matrix,
)
from witnessed_difference.outcomes import Accepted, AuthorityEffect, RefusalCode, Refused
from witnessed_difference.projective import GaussianRational

Q = ExactField.RATIONAL
QI = ExactField.GAUSSIAN


def accepted(outcome):
    assert isinstance(outcome, Accepted), outcome
    assert outcome.authority_effect is AuthorityEffect.NONE
    return outcome.value


def refused(outcome, code: RefusalCode, fragment: str = "") -> Refused:
    assert isinstance(outcome, Refused), outcome
    assert outcome.code is code, outcome
    assert fragment in outcome.detail, outcome.detail
    return outcome


def g(real, imag=0) -> GaussianRational:
    return GaussianRational(Fraction(real), Fraction(imag))


def test_coercion_admits_exact_scalars_and_refuses_floats_bools_and_shapes() -> None:
    assert accepted(coerce_vector((1, "1/2", Fraction(3)), 3, Q)) == (Fraction(1), Fraction(1, 2), Fraction(3))
    assert accepted(coerce_vector((g(1, 1), 2), None, QI)) == (g(1, 1), g(2))
    for bad in ((0.5,), (True,), (1j,), (g(1, 1),), "12", {0: 1}, 5, ("1/0",), ("x",)):
        refused(coerce_vector(bad, None, Q), RefusalCode.INVALID_INPUT, "exact")
    refused(coerce_vector((1, 2), 3, Q), RefusalCode.INVALID_INPUT, "length 3")
    assert accepted(coerce_matrix(((1, 2), (3, 4)), (2, 2), Q))[1] == (Fraction(3), Fraction(4))
    assert accepted(coerce_matrix((), (0, 3), Q)) == ()
    assert accepted(coerce_matrix(((), ()), (2, 0), Q)) == ((), ())
    refused(coerce_matrix("ab", (None, None), Q), RefusalCode.INVALID_INPUT, "sequence of rows")
    refused(coerce_matrix(((1, 2), (3,)), (None, None), Q), RefusalCode.INVALID_INPUT, "shape")
    refused(coerce_matrix(((1, 2),), (2, 2), Q), RefusalCode.INVALID_INPUT, "shape")
    refused(coerce_matrix(((1, 2),), (1, 3), Q), RefusalCode.INVALID_INPUT, "shape")
    refused(coerce_matrix(((0.1, 2),), (None, None), Q), RefusalCode.INVALID_INPUT, "exact")


def test_products_adjoints_and_zero_extent_shapes() -> None:
    left = accepted(coerce_matrix(((g(1, 1), g(0, 2)),), (1, 2), QI))
    assert adjoint(left, 2) == ((g(1, -1),), (g(0, -2),))
    assert matmul(left, adjoint(left, 2), 1, QI) == ((g(6),),)
    assert matmul((), (), 3, Q) == ()
    assert matmul(((), ()), (), 2, Q) == zero_matrix(2, 2, Q)
    assert apply(identity(2, Q), (Fraction(3), Fraction(4)), Q) == (Fraction(3), Fraction(4))
    assert inner((g(0, 1),), (g(0, 1),), QI) == g(1)
    assert scale(identity(2, Q), Fraction(2)) == subtract(scale(identity(2, Q), Fraction(3)), identity(2, Q))
    assert constant(QI, 2) == g(2) and constant(Q, 2) == Fraction(2)


def test_row_reduction_rank_kernel_solve_and_inverse_over_both_fields() -> None:
    singular = accepted(coerce_matrix(((1, 2, 3), (2, 4, 6), (1, 0, 1)), (3, 3), Q))
    assert rank(singular, 3, Q) == 2
    (kernel,) = kernel_basis(singular, 3, Q)
    assert apply(singular, kernel, Q) == (Fraction(0),) * 3 and any(kernel)
    assert solve(singular, (Fraction(1), Fraction(3), Fraction(0)), 3, Q) is None
    particular = solve(singular, (Fraction(4), Fraction(8), Fraction(2)), 3, Q)
    assert apply(singular, particular, Q) == (Fraction(4), Fraction(8), Fraction(2))
    assert inverse(singular, Q) is None
    rotation = ((g(0), g(0, 1)), (g(0, 1), g(0)))
    inverted = inverse(rotation, QI)
    assert matmul(rotation, inverted, 2, QI) == identity(2, QI)
    assert kernel_basis((), 2, Q) == ((Fraction(1), Fraction(0)), (Fraction(0), Fraction(1)))
    assert inverse((), Q) == ()


def _all_small_symmetric() -> list[tuple[tuple[int, ...], ...]]:
    values = (-1, 0, 1)
    matrices = []
    for a, b, c, d, e, f in product(values, repeat=6):
        matrices.append(((a, b, c), (b, d, e), (c, e, f)))
    return matrices


def _laplace(rows: list[list[Fraction]]) -> Fraction:
    if not rows:
        return Fraction(1)
    return sum(
        ((-1) ** j * rows[0][j] * _laplace([row[:j] + row[j + 1 :] for row in rows[1:]]) for j in range(len(rows))),
        start=Fraction(0),
    )


def _determinant(matrix, subset) -> Fraction:
    return _laplace([[matrix[a][b] for b in subset] for a in subset])


def test_congruence_certificates_are_verified_and_decide_positivity_exhaustively() -> None:
    subsets = [(0,), (1,), (2,), (0, 1), (0, 2), (1, 2), (0, 1, 2)]
    for rows in _all_small_symmetric():
        certificate = accepted(congruence_diagonalize(rows, Q))
        assert accepted(verify_congruence(certificate)) is certificate
        matrix = certificate.matrix
        minors_nonnegative = all(_determinant(matrix, subset) >= 0 for subset in subsets)
        assert certificate.positive_semidefinite == minors_nonnegative
        if certificate.positive_semidefinite:
            assert certificate.negative_vector() is None
        else:
            witness = certificate.negative_vector()
            assert inner(witness, apply(matrix, witness, Q), Q) < 0
        positive, negative, zero = certificate.inertia
        assert positive + negative + zero == 3
        assert zero == 3 - rank(matrix, 3, Q)
        assert certificate.positive_definite == (positive == 3)


def test_zero_diagonal_hermitian_forms_over_gaussian_rationals() -> None:
    hermitian = ((g(0), g(0, 1)), (g(0, -1), g(0)))
    certificate = accepted(congruence_diagonalize(hermitian, QI))
    assert certificate.inertia == (1, 1, 0)
    witness = certificate.negative_vector()
    assert inner(witness, apply(hermitian, witness, QI), QI).real < 0
    refused(congruence_diagonalize(((g(0), g(0, 1)), (g(0, 1), g(0))), QI), RefusalCode.NOT_HERMITIAN)
    refused(congruence_diagonalize(((1, 2),), Q), RefusalCode.INVALID_INPUT, "square")
    refused(congruence_diagonalize(((1,),), "Q"), RefusalCode.INVALID_INPUT, "declared")
    refused(congruence_diagonalize(((0.5,),), Q), RefusalCode.INVALID_INPUT)
    assert accepted(congruence_diagonalize((), Q)).diagonal == ()


def test_verify_congruence_refuses_every_tamper() -> None:
    certificate = accepted(congruence_diagonalize(((2, 1), (1, 2)), Q))
    refused(verify_congruence("certificate"), RefusalCode.INVALID_INPUT)
    refused(verify_congruence(replace(certificate, field="Q")), RefusalCode.INVALID_INPUT)
    refused(verify_congruence(replace(certificate, diagonal=(2, Fraction(3, 2)))), RefusalCode.CERTIFICATE_MISMATCH)
    refused(verify_congruence(replace(certificate, diagonal=(Fraction(2),))), RefusalCode.CERTIFICATE_MISMATCH)
    refused(verify_congruence(replace(certificate, field=QI)), RefusalCode.CERTIFICATE_MISMATCH)
    refused(
        verify_congruence(replace(certificate, diagonal=(Fraction(2), Fraction(1)))),
        RefusalCode.CERTIFICATE_MISMATCH,
        "differs",
    )
    singular = CongruenceCertificate(Q, ((Fraction(0),),), ((Fraction(0),),), (Fraction(0),))
    refused(verify_congruence(singular), RefusalCode.CERTIFICATE_MISMATCH, "singular")


@pytest.mark.parametrize("field", [Q, QI])
def test_identity_is_positive_definite_in_both_fields(field) -> None:
    certificate = accepted(congruence_diagonalize(identity(3, field), field))
    assert certificate.positive_definite and certificate.inertia == (3, 0, 0)


# Executable finite evidence; AuthorityEffect: None.
