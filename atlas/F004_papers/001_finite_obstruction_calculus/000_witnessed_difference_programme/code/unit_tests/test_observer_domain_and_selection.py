
from witnessed_difference.native_functionals import squared_l2
"""Declared observer domains and representative-independent selected witnesses."""

from fractions import Fraction as F

import pytest
from witnessed_difference.cochains import FiniteComplex
from witnessed_difference.obstruction import (
    MatrixQuotientCertificate,
    matrix_quotient_l1,
    verify_matrix_certificate,
)
from witnessed_difference.outcomes import Accepted, RefusalCode, Refused
from witnessed_difference.quotient_observer import (
    evaluate_quotient_profile,
    induced_observer_norm,
    make_linear_quotient_observer,
)


def test_unrealizable_zero_observer_report_is_refused():
    edge = FiniteComplex((0, 1), ((0, 1),))
    admitted = make_linear_quotient_observer(edge, ((0,),))
    assert isinstance(admitted, Accepted)
    zero = induced_observer_norm(admitted.value, (0,))
    assert isinstance(zero, Accepted) and zero.value == 0
    impossible = induced_observer_norm(admitted.value, (1,))
    assert isinstance(impossible, Refused) and impossible.code is RefusalCode.INFEASIBLE


def test_mismatched_repair_image_is_refused_before_numerical_acceptance():
    class_repairs, evaluator_repairs = ((1,), (0,)), ((0,), (1,))
    zero = matrix_quotient_l1(evaluator_repairs, (0, 0))
    equivalent = matrix_quotient_l1(evaluator_repairs, (1, 0))
    assert isinstance(zero, Accepted) and isinstance(equivalent, Accepted)
    assert (zero.value.value, equivalent.value.value) == (0, 1)
    for representative in ((0, 0), (1, 0)):
        refused = evaluate_quotient_profile(class_repairs, evaluator_repairs, representative)
        assert isinstance(refused, Refused) and refused.code is RefusalCode.NOT_REPAIR_COMPATIBLE


def test_compatible_repair_images_preserve_class_values_and_bind_input():
    repairs = ((1,), (0,))
    for representative in ((0, 2), (3, 2), (-5, 2)):
        receipt = evaluate_quotient_profile(repairs, repairs, representative)
        assert isinstance(receipt, Accepted)
        assert receipt.value.class_repairs == ((F(1),), (F(0),))
        assert receipt.value.certificate.delta == tuple(map(F, representative))
        assert receipt.value.certificate.value == 2
    coarser = evaluate_quotient_profile(repairs, ((1, 0), (0, 1)), (0, 2))
    assert isinstance(coarser, Accepted) and coarser.value.certificate.value == 0


@pytest.mark.parametrize("repairs", [((1.0,), (0,)), ((True,), (0,)), ((1,),), ((1,), (0, 1))])
def test_malformed_repair_binding_refuses(repairs):
    result = evaluate_quotient_profile(((1,), (0,)), repairs, (0, 1))
    assert isinstance(result, Refused) and result.code is RefusalCode.INVALID_INPUT


def test_triangle_selection_is_invariant_under_a_repair():
    differential = tuple(tuple(map(F, row)) for row in ((-1, 1, 0), (0, -1, 1), (1, 0, -1)))
    selected = (F(1, 3),) * 3
    dual = (F(1),) * 3
    for delta, potential in (
        ((1, 0, 0), (F(0), F(2, 3), F(1, 3))),
        ((2, -1, 0), (F(0), F(5, 3), F(1, 3))),
    ):
        cert = MatrixQuotientCertificate(differential, 3, tuple(map(F, delta)),
                                         (F(1),) * 3, potential, selected, F(1), dual)
        assert isinstance(verify_matrix_certificate(cert), Accepted)
        assert squared_l2(cert.residual) == F(1, 3)
    # The manuscript proves this identity on the entire real optimal face.
    for denominator in range(1, 8):
        for first in range(denominator + 1):
            for second in range(denominator - first + 1):
                residual = (F(first, denominator), F(second, denominator),
                            F(denominator - first - second, denominator))
                excess = squared_l2(residual) - F(1, 3)
                assert excess == squared_l2(tuple(x-F(1, 3) for x in residual)) >= 0
                assert (excess == 0) == (residual == selected)
