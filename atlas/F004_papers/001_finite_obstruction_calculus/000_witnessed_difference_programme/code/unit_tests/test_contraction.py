import random
from dataclasses import replace
from fractions import Fraction
from itertools import product

import pytest
from witnessed_difference.contraction import (
    Contraction,
    GradedComplex,
    assemble_map,
    homology_dimensions,
    is_normalized,
    make_complex,
    make_total_complex,
    normalize_homotopy,
    perturb,
    retraction_defect,
    validate_contraction,
)
from witnessed_difference.exact_linear import (
    ExactField,
    add,
    identity,
    inverse,
    is_zero,
    matmul,
    subtract,
)
from witnessed_difference.obstruction import DiagnosticClass, verify_matrix_certificate
from witnessed_difference.outcomes import Accepted, AuthorityEffect, RefusalCode, Refused

Q = ExactField.RATIONAL


def accepted(outcome):
    assert isinstance(outcome, Accepted), outcome
    assert outcome.authority_effect is AuthorityEffect.NONE
    return outcome.value


def refused(outcome, code: RefusalCode, fragment: str = "") -> Refused:
    assert isinstance(outcome, Refused), outcome
    assert outcome.code is code, outcome
    assert fragment in outcome.detail, outcome.detail
    return outcome


def mul(left, right, columns):
    return matmul(left, right, columns, Q)


def sparse(rows: int, columns: int, entries: dict) -> tuple:
    return tuple(tuple(Fraction(entries.get((a, b), 0)) for b in range(columns)) for a in range(rows))


def zero_complex(dims: tuple[int, ...]) -> GradedComplex:
    size = sum(dims)
    return accepted(make_total_complex(dims, sparse(size, size, {})))


def shift_contraction() -> Contraction:
    """C = D + (e0 -> e1) with basis x0, e0 | x1, e1 | x2 and D = (x0 | x1 | x2) with d_D = 0."""

    big = accepted(make_total_complex((2, 2, 1), sparse(5, 5, {(3, 1): 1})))
    inclusion = sparse(5, 3, {(0, 0): 1, (2, 1): 1, (4, 2): 1})
    retraction = sparse(3, 5, {(0, 0): 1, (1, 2): 1, (2, 4): 1})
    return accepted(validate_contraction(big, zero_complex((1, 1, 1)), inclusion, retraction, sparse(5, 5, {(1, 3): 1})))


SHIFT_DELTA = sparse(5, 5, {(2, 0): 1, (3, 0): 1, (2, 1): 1, (4, 2): 1, (4, 3): -1})


def simple_contraction() -> Contraction:
    """C = (x, e0 | e1) with d e0 = e1 and D = (x | 0)."""

    big = accepted(make_total_complex((2, 1), sparse(3, 3, {(2, 1): 1})))
    return accepted(
        validate_contraction(
            big, zero_complex((1, 0)), sparse(3, 1, {(0, 0): 1}), sparse(1, 3, {(0, 0): 1}), sparse(3, 3, {(1, 2): 1})
        )
    )


def source_convention(contraction: Contraction, delta):
    """The source's formulas: A = (1 - delta h)^-1 delta with plus signs throughout."""

    n, m = contraction.big.size, contraction.small.size
    twisted = inverse(subtract(identity(n, Q), mul(delta, contraction.homotopy, n)), Q)
    a = mul(twisted, delta, n)
    small = add(contraction.small.differential, mul(mul(contraction.retraction, a, n), contraction.inclusion, m))
    inclusion = add(contraction.inclusion, mul(mul(contraction.homotopy, a, n), contraction.inclusion, m))
    retraction = add(contraction.retraction, mul(mul(contraction.retraction, a, n), contraction.homotopy, n))
    homotopy = add(contraction.homotopy, mul(mul(contraction.homotopy, a, n), contraction.homotopy, n))
    return small, inclusion, retraction, homotopy


def test_sign_corrected_perturbation_lemma_on_the_shift_instance() -> None:
    contraction = shift_contraction()
    assert accepted(is_normalized(contraction)).normalized
    perturbed = accepted(perturb(contraction, SHIFT_DELTA))
    assert accepted(is_normalized(perturbed)).normalized
    assert perturbed.small.differential == sparse(3, 3, {(2, 1): 1})
    assert perturbed.inclusion == sparse(5, 3, {(0, 0): 1, (1, 0): -1, (2, 1): 1, (4, 2): 1})
    assert perturbed.retraction == sparse(3, 5, {(0, 0): 1, (1, 2): 1, (1, 3): -1, (2, 4): 1})
    assert perturbed.homotopy == contraction.homotopy
    assert accepted(homology_dimensions(perturbed.big)) == accepted(homology_dimensions(perturbed.small)) == (1, 0, 0)


def test_source_convention_fails_to_give_a_differential_on_d() -> None:
    contraction = shift_contraction()
    small, inclusion, retraction, homotopy = source_convention(contraction, SHIFT_DELTA)
    assert small == sparse(3, 3, {(1, 0): 2, (2, 1): 1})
    refused(make_total_complex((1, 1, 1), small), RefusalCode.NOT_A_DIFFERENTIAL)


def test_source_convention_fails_the_chain_map_check_where_the_corrected_formula_passes() -> None:
    contraction = simple_contraction()
    delta = sparse(3, 3, {(2, 0): 1})
    perturbed = accepted(perturb(contraction, delta))
    assert perturbed.inclusion == sparse(3, 1, {(0, 0): 1, (1, 0): -1})
    assert accepted(homology_dimensions(perturbed.big)) == accepted(homology_dimensions(perturbed.small)) == (1, 0)
    small, inclusion, retraction, homotopy = source_convention(contraction, delta)
    big = accepted(make_total_complex((2, 1), add(contraction.big.differential, delta)))
    small_complex = accepted(make_total_complex((1, 0), small))
    refused(validate_contraction(big, small_complex, inclusion, retraction, homotopy), RefusalCode.NOT_CHAIN_MAP)


def _random_graded(rng: random.Random, source, target, degree, low=-1, high=1):
    labels_source = [k for k, n in enumerate(source) for _ in range(n)]
    labels_target = [k for k, n in enumerate(target) for _ in range(n)]
    return tuple(
        tuple(
            Fraction(rng.randint(low, high)) if labels_source[b] + degree == labels_target[a] else Fraction(0)
            for b in range(len(labels_source))
        )
        for a in range(len(labels_target))
    )


def _conjugated_contraction(rng: random.Random) -> Contraction:
    """C = D + (e0 -> e1a) + (e1b -> e2) with D = (x0 | x1 | x2), hidden by a degree-0 automorphism."""

    dims = (2, 3, 2)
    d = sparse(7, 7, {(3, 1): 1, (6, 4): 1})
    h = sparse(7, 7, {(1, 3): 1, (4, 6): 1})
    i = sparse(7, 3, {(0, 0): 1, (2, 1): 1, (5, 2): 1})
    r = sparse(3, 7, {(0, 0): 1, (1, 2): 1, (2, 5): 1})
    while True:
        g = add(_random_graded(rng, dims, dims, 0), tuple(tuple(Fraction(2 * (a == b)) for b in range(7)) for a in range(7)))
        g_inverse = inverse(g, Q)
        if g_inverse is not None:
            break
    big = accepted(make_total_complex(dims, mul(mul(g, d, 7), g_inverse, 7)))
    return accepted(
        validate_contraction(big, zero_complex((1, 1, 1)), mul(g, i, 3), mul(r, g_inverse, 7), mul(mul(g, h, 7), g_inverse, 7))
    )


def test_sign_corrected_formulas_pass_on_several_random_exact_instances() -> None:
    rng = random.Random(20260929)
    passed = singular = 0
    for trial in range(12):
        contraction = _conjugated_contraction(rng)
        n = contraction.big.size
        while True:
            k = add(_random_graded(rng, (2, 3, 2), (2, 3, 2), 0), identity(n, Q))
            k_inverse = inverse(k, Q)
            if k_inverse is not None:
                break
        gauge = subtract(mul(mul(k, contraction.big.differential, n), k_inverse, n), contraction.big.differential)
        twist = sparse(3, 3, {(1, 0): trial % 3 - 1}) if trial % 2 else sparse(3, 3, {(2, 1): 1})
        delta = gauge if trial % 4 == 0 else mul(mul(contraction.inclusion, twist, 3), contraction.retraction, n)
        outcome = perturb(contraction, delta)
        if isinstance(outcome, Refused):
            refused(outcome, RefusalCode.NOT_INVERTIBLE)
            singular += 1
            continue
        perturbed = outcome.value
        assert accepted(is_normalized(perturbed)).normalized
        assert accepted(homology_dimensions(perturbed.big)) == accepted(homology_dimensions(perturbed.small))
        passed += 1
    assert passed >= 6


def test_perturbation_of_a_non_normalized_contraction_is_refused_because_it_can_break() -> None:
    big = zero_complex((1, 1))
    unit = identity(2, Q)
    raw = accepted(validate_contraction(big, big, unit, unit, sparse(2, 2, {(0, 1): 1})))
    report = accepted(is_normalized(raw))
    assert not report.hi_zero and not report.rh_zero and report.hh_zero and not report.normalized
    delta = sparse(2, 2, {(1, 0): 1})
    # The formulas themselves break r' i' = 1 on this input, which is why the lemma needs normalization.
    a = mul(inverse(add(unit, mul(delta, raw.homotopy, 2)), Q), delta, 2)
    included = subtract(raw.inclusion, mul(mul(raw.homotopy, a, 2), raw.inclusion, 2))
    retracted = subtract(raw.retraction, mul(mul(raw.retraction, a, 2), raw.homotopy, 2))
    assert mul(retracted, included, 2) != unit
    refused(perturb(raw, delta), RefusalCode.SCOPE_VIOLATION, "normalized contractions")
    refused(perturb(raw, sparse(2, 2, {})), RefusalCode.SCOPE_VIOLATION, "normalized contractions")
    normalized = accepted(normalize_homotopy(raw))
    assert accepted(is_normalized(normalized)).normalized
    perturbed = accepted(perturb(normalized, delta))
    assert perturbed.small.differential == delta


def test_operation_three_side_conditions_without_the_homotopy_equation_are_refused() -> None:
    big, small = zero_complex((2,)), zero_complex((1,))
    inclusion, retraction, homotopy = sparse(2, 1, {(0, 0): 1}), sparse(1, 2, {(0, 0): 1}), sparse(2, 2, {})
    assert mul(retraction, inclusion, 1) == identity(1, Q)
    assert is_zero(mul(homotopy, inclusion, 1), Q) and is_zero(mul(retraction, homotopy, 2), Q)
    assert is_zero(mul(homotopy, homotopy, 2), Q)
    refused(validate_contraction(big, small, inclusion, retraction, homotopy), RefusalCode.HOMOTOPY_MISMATCH)
    assert accepted(homology_dimensions(big)) == (2,) and accepted(homology_dimensions(small)) == (1,)
    defect = accepted(retraction_defect(big, small, inclusion, retraction))
    assert defect.kernel_cohomology == (1,) and not defect.kernel_acyclic and not defect.nullhomotopic
    assert defect.diagnostic_class is DiagnosticClass.CLOSED_RESIDUAL
    assert defect.class_certificate.value == 1
    zero_budget = accepted(retraction_defect(big, small, inclusion, retraction, max_pivots=0))
    assert zero_budget.class_certificate.value == defect.class_certificate.value


def test_retraction_defect_class_is_exact_iff_kernel_acyclic_and_never_active() -> None:
    rng = random.Random(4)
    seen = set()
    for a, c in product((-1, 0, 1), repeat=2):
        for _ in range(3):
            dims = (2, 2)
            d = sparse(4, 4, {(2, 0): a, (3, 1): c})
            g = None
            while g is None:
                candidate = add(_random_graded(rng, dims, dims, 0), tuple(tuple(Fraction(2 * (x == y)) for y in range(4)) for x in range(4)))
                g = candidate if inverse(candidate, Q) is not None else None
            g_inverse = inverse(g, Q)
            big = accepted(make_total_complex(dims, mul(mul(g, d, 4), g_inverse, 4)))
            small = accepted(make_total_complex((1, 1), sparse(2, 2, {(1, 0): a})))
            inclusion = mul(g, sparse(4, 2, {(0, 0): 1, (2, 1): 1}), 2)
            retraction = mul(sparse(2, 4, {(0, 0): 1, (1, 2): 1}), g_inverse, 4)
            defect = accepted(retraction_defect(big, small, inclusion, retraction))
            assert defect.idempotent and defect.commutes_with_differential and defect.closure_mass == 0
            assert accepted(verify_matrix_certificate(defect.class_certificate)) is defect.class_certificate
            assert defect.kernel_acyclic == (c != 0) == defect.nullhomotopic
            assert (defect.class_certificate.value == 0) == defect.nullhomotopic
            assert defect.diagnostic_class is not DiagnosticClass.ACTIVE_CLOSURE_FAILURE
            seen.add(defect.diagnostic_class)
            if defect.nullhomotopic:
                contraction = accepted(validate_contraction(big, small, inclusion, retraction, defect.homotopy))
                normalized = accepted(normalize_homotopy(contraction))
                assert accepted(is_normalized(normalized)).normalized
    assert seen == {DiagnosticClass.EXACT_CLASS, DiagnosticClass.CLOSED_RESIDUAL}


def test_shift_retraction_defect_is_exact_with_a_found_homotopy() -> None:
    contraction = shift_contraction()
    defect = accepted(retraction_defect(contraction.big, contraction.small, contraction.inclusion, contraction.retraction))
    assert defect.kernel_cohomology == (0, 0, 0) and defect.diagnostic_class is DiagnosticClass.EXACT_CLASS
    assert defect.defect == sparse(5, 5, {(1, 1): 1, (3, 3): 1})
    assert accepted(validate_contraction(contraction.big, contraction.small, contraction.inclusion, contraction.retraction, defect.homotopy))


def test_complex_constructors_and_block_assembly() -> None:
    complex_ = accepted(make_complex((1, 2, 1), (((1,), (0,)), ((0, 1),))))
    assert complex_.differential == sparse(4, 4, {(1, 0): 1, (3, 2): 1})
    assert accepted(homology_dimensions(complex_)) == (0, 0, 0)
    assert accepted(assemble_map((1, 1), (1, 1), -1, ((), ((1,),)))) == sparse(2, 2, {(0, 1): 1})
    refused(make_complex((1, 1), ()), RefusalCode.INVALID_INPUT, "one differential block")
    refused(make_complex([1, 1], (((1,),),)), RefusalCode.INVALID_INPUT, "one differential block")
    refused(make_complex((1, 1), (((1, 2),),)), RefusalCode.INVALID_INPUT, "shape")
    refused(make_complex((1, 1, 1), (((1,),), ((1,),))), RefusalCode.NOT_A_DIFFERENTIAL)
    refused(assemble_map((1,), (1,), 0.5, (((1,),),)), RefusalCode.INVALID_INPUT, "integer degree")
    refused(assemble_map((1,), (1,), 0, ()), RefusalCode.INVALID_INPUT, "one block per source degree")
    for dims in ((), (1, -1), [1], (True,)):
        refused(make_total_complex(dims, ()), RefusalCode.INVALID_INPUT, "dims")
    refused(make_total_complex((1, 1), ((0, 0),)), RefusalCode.INVALID_INPUT, "shape")
    refused(make_total_complex((1, 1), ((0, 1), (0, 0))), RefusalCode.INVALID_INPUT, "degree +1")
    refused(make_total_complex((1, 1), ((0, 0), (0.5, 0))), RefusalCode.INVALID_INPUT, "exact")
    refused(homology_dimensions("complex"), RefusalCode.INVALID_INPUT)


def test_contraction_validation_refusals() -> None:
    contraction = shift_contraction()
    big, small = contraction.big, contraction.small
    i, r, h = contraction.inclusion, contraction.retraction, contraction.homotopy
    refused(validate_contraction("C", small, i, r, h), RefusalCode.INVALID_INPUT, "graded complex")
    refused(validate_contraction(big, "D", i, r, h), RefusalCode.INVALID_INPUT, "graded complex")
    refused(validate_contraction(big, zero_complex((1, 1)), i, r, h), RefusalCode.INVALID_INPUT, "same degree range")
    refused(validate_contraction(big, small, i[:4], r, h), RefusalCode.INVALID_INPUT, "shape")
    refused(validate_contraction(big, small, i, r[:2], h), RefusalCode.INVALID_INPUT, "shape")
    refused(validate_contraction(big, small, sparse(5, 3, {(0, 0): 1, (2, 1): 1, (4, 2): 1, (0, 1): 1}), r, h), RefusalCode.INVALID_INPUT, "preserve degree")
    refused(validate_contraction(big, small, sparse(5, 3, {(0, 0): 1, (2, 1): 1, (4, 2): 1, (1, 0): 1}), r, h), RefusalCode.NOT_CHAIN_MAP)
    refused(validate_contraction(big, small, i, sparse(3, 5, {(0, 0): 1, (1, 2): 1, (2, 4): 1, (1, 3): 1}), h), RefusalCode.NOT_CHAIN_MAP)
    refused(validate_contraction(big, small, sparse(5, 3, {(0, 0): 2, (2, 1): 1, (4, 2): 1}), r, h), RefusalCode.NOT_A_RETRACTION)
    refused(validate_contraction(big, small, i, r, h[:3]), RefusalCode.INVALID_INPUT, "shape")
    refused(validate_contraction(big, small, i, r, sparse(5, 5, {(3, 1): 1})), RefusalCode.INVALID_INPUT, "degree -1")
    refused(validate_contraction(big, small, i, r, sparse(5, 5, {})), RefusalCode.HOMOTOPY_MISMATCH)
    for operation in (is_normalized, normalize_homotopy, lambda c: perturb(c, SHIFT_DELTA)):
        refused(operation("contraction"), RefusalCode.INVALID_INPUT, "contraction is required")
        refused(operation(replace(contraction, homotopy=sparse(5, 5, {}))), RefusalCode.HOMOTOPY_MISMATCH)
    refused(retraction_defect(big, small, i, sparse(3, 5, {(0, 0): 1})), RefusalCode.NOT_A_RETRACTION)


def test_perturbation_refusals() -> None:
    contraction = simple_contraction()
    refused(perturb(contraction, sparse(2, 2, {})), RefusalCode.INVALID_INPUT, "shape")
    refused(perturb(contraction, sparse(3, 3, {(0, 1): 1})), RefusalCode.INVALID_INPUT, "degree +1")
    refused(perturb(contraction, ((0, 0, 0), (0, 0, 0), (1, 0.5, 0))), RefusalCode.INVALID_INPUT, "exact")
    shift = shift_contraction()
    refused(perturb(shift, sparse(5, 5, {(2, 0): 1, (4, 2): 1})), RefusalCode.NOT_A_DIFFERENTIAL)
    refused(perturb(contraction, sparse(3, 3, {(2, 1): -1})), RefusalCode.NOT_INVERTIBLE, "singular")


@pytest.mark.parametrize("scale", [Fraction(1, 2), 2, -3])
def test_rescaled_twist_perturbations_on_the_simple_instance(scale) -> None:
    contraction = simple_contraction()
    delta = sparse(3, 3, {(2, 0): 1, (2, 1): scale})
    perturbed = accepted(perturb(contraction, delta))
    assert perturbed.inclusion == sparse(3, 1, {(0, 0): 1, (1, 0): Fraction(-1) / (1 + scale)})
    assert accepted(is_normalized(perturbed)).normalized


def test_a_perturbed_contraction_that_is_not_normalized_is_refused(monkeypatch) -> None:
    import witnessed_difference.contraction as contraction_module

    big = zero_complex((1, 1))
    unit = identity(2, Q)
    normalized = accepted(normalize_homotopy(accepted(validate_contraction(big, big, unit, unit, sparse(2, 2, {(0, 1): 1})))))
    genuine = contraction_module.is_normalized
    calls = []

    def second_call_fails(contraction):
        calls.append(contraction)
        report = genuine(contraction)
        if len(calls) == 1:
            return report
        return Accepted(replace(report.value, hh_zero=False))

    monkeypatch.setattr(contraction_module, "is_normalized", second_call_fails)
    refused(perturb(normalized, sparse(2, 2, {(1, 0): 1})), RefusalCode.CERTIFICATE_MISMATCH, "not normalized")
    assert len(calls) == 2


def test_revalidation_catches_a_corrupted_perturbation_of_a_normalized_contraction(monkeypatch) -> None:
    import witnessed_difference.contraction as contraction_module

    monkeypatch.setattr(contraction_module, "inverse", lambda matrix, field: identity(len(matrix), field))
    rng = random.Random(20260929)
    caught = 0
    for trial in range(12):
        contraction = _conjugated_contraction(rng)
        n = contraction.big.size
        while True:
            k = add(_random_graded(rng, (2, 3, 2), (2, 3, 2), 0), identity(n, Q))
            k_inverse = inverse(k, Q)
            if k_inverse is not None:
                break
        delta = subtract(mul(mul(k, contraction.big.differential, n), k_inverse, n), contraction.big.differential)
        if is_zero(mul(delta, contraction.homotopy, n), Q):
            continue
        outcome = perturb(contraction, delta)
        if isinstance(outcome, Refused) and "fail re-validation" in outcome.detail:
            caught += 1
        else:
            assert isinstance(outcome, Accepted), outcome
    assert caught >= 3


# Executable finite evidence; AuthorityEffect: None.
