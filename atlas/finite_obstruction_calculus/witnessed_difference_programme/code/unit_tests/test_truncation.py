import random
from dataclasses import replace
from fractions import Fraction

import pytest
from witnessed_difference.exact_linear import (
    ExactField,
    add,
    adjoint,
    apply,
    identity,
    inverse,
    is_zero,
    kernel_basis,
    matmul,
    subtract,
    verify_congruence,
)
from witnessed_difference.outcomes import Accepted, AuthorityEffect, RefusalCode, Refused
from witnessed_difference.projective import GaussianRational
from witnessed_difference.truncation import (
    ReducedZero,
    TruncationLeakage,
    kernel_matches_components,
    promote_truncation_zero,
    reduced_zero_is_genuine,
    truncation_leakage,
    validate_projector,
    weighted_form_operator,
)

QI = ExactField.GAUSSIAN
P3 = ((1, 0, 0), (0, 1, 0), (0, 0, 0))
A3 = ((0, 0, 0), (0, 0, 0), (0, 1, 0))


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


def random_gaussian(rng: random.Random) -> GaussianRational:
    return g(Fraction(rng.randint(-3, 3), rng.randint(1, 2)), Fraction(rng.randint(-3, 3), rng.randint(1, 2)))


def random_matrix(rng: random.Random, rows: int, columns: int):
    return tuple(tuple(random_gaussian(rng) for _ in range(columns)) for _ in range(rows))


def random_projector(rng: random.Random, size: int, rank_: int):
    while True:
        basis = random_matrix(rng, size, rank_)
        gram = inverse(matmul(adjoint(basis, rank_), basis, rank_, QI), QI)
        if gram is not None:
            return matmul(matmul(basis, gram, rank_, QI), adjoint(basis, rank_), size, QI)


def test_audit_counterexample_genuine_zero_despite_leakage_and_a_spurious_zero() -> None:
    record = accepted(truncation_leakage(A3, P3))
    assert record.identity_holds
    assert record.leakage == tuple(tuple(g(int(i == j == 1)) for j in range(3)) for i in range(3))
    assert not record.leakage_free and not record.range_invariant
    assert accepted(verify_congruence(record.leakage_certificate)).positive_semidefinite
    genuine = accepted(reduced_zero_is_genuine(A3, P3, (1, 0, 0)))
    assert genuine.genuine and genuine.image_is_zero and genuine.leakage_energy == 0
    assert not genuine.leakage_free
    spurious = accepted(reduced_zero_is_genuine(A3, P3, (0, 1, 0)))
    assert not spurious.genuine and not spurious.image_is_zero
    assert spurious.leakage_energy == 1 and spurious.image == (g(0), g(0), g(1))


def test_leakage_norm_is_unbounded_while_a_genuine_zero_persists() -> None:
    for scale in (10, 1000, 10**6):
        operator = ((0, 0, 0), (0, 0, 0), (0, scale, 0))
        record = accepted(truncation_leakage(operator, P3))
        assert record.leakage[1][1] == g(scale * scale)
        assert accepted(reduced_zero_is_genuine(operator, P3, (1, 0, 0))).genuine


def test_compression_identity_and_leakage_positivity_on_random_gaussian_data() -> None:
    rng = random.Random(20260929)
    for _ in range(12):
        size, rank_ = rng.choice(((3, 1), (3, 2), (4, 2)))
        projector = random_projector(rng, size, rank_)
        operator = random_matrix(rng, size, size)
        record = accepted(truncation_leakage(operator, projector))
        assert record.identity_holds
        assert accepted(verify_congruence(record.leakage_certificate)).positive_semidefinite
        assert record.leakage_free == record.range_invariant


def test_leakage_vanishes_exactly_for_invariant_ranges() -> None:
    invariant = ((1, 2, 5), (3, g(0, 1), 7), (0, 0, 4))
    record = accepted(truncation_leakage(invariant, P3))
    assert record.leakage_free and record.range_invariant and record.identity_holds
    shift = ((0, 1), (0, 0))
    first = ((1, 0), (0, 0))
    leakage_free = accepted(truncation_leakage(shift, first))
    assert leakage_free.leakage_free
    complement = subtract(identity(2, QI), leakage_free.projector)
    descent_defect = matmul(matmul(leakage_free.projector, leakage_free.operator, 2, QI), complement, 2, QI)
    assert not is_zero(descent_defect, QI)


def _remove_along(operator, image, psi):
    """operator - image psi* / (psi* psi), so the new operator sends psi to operator psi - image."""

    norm = sum((entry.conjugate() * entry for entry in psi), start=g(0))
    outer = tuple(tuple(a * b.conjugate() / norm for b in psi) for a in image)
    return subtract(operator, outer)


def test_every_reduced_zero_is_genuine_exactly_when_its_leakage_energy_vanishes() -> None:
    rng = random.Random(7)
    genuine = spurious = 0
    for trial in range(16):
        projector = random_projector(rng, 4, 2)
        psi = apply(projector, tuple(random_gaussian(rng) for _ in range(4)), QI)
        if all(value == g(0) for value in psi):
            continue
        operator = random_matrix(rng, 4, 4)
        image = apply(operator, psi, QI)
        removed = image if trial % 2 else apply(projector, image, QI)
        operator = _remove_along(operator, removed, psi)
        compression = matmul(matmul(projector, operator, 4, QI), projector, 4, QI)
        stacked = subtract(identity(4, QI), projector) + compression
        zeros = kernel_basis(stacked, 4, QI)
        assert zeros
        for vector in zeros + (psi,):
            record = accepted(reduced_zero_is_genuine(operator, projector, vector))
            assert record.genuine == record.image_is_zero
            genuine += record.genuine
            spurious += not record.genuine
    assert genuine > 0 and spurious > 0


def test_constructed_genuine_and_spurious_zeros_on_gaussian_data() -> None:
    projector = ((Fraction(1, 2), g(0, Fraction(-1, 2))), (g(0, Fraction(1, 2)), Fraction(1, 2)))
    assert accepted(validate_projector(projector, 2))[0][1] == g(0, Fraction(-1, 2))
    psi = (g(1), g(0, 1))
    kills_psi = ((g(0, -1), g(1)), (g(0), g(0)))
    genuine = accepted(reduced_zero_is_genuine(kills_psi, projector, psi))
    assert genuine.genuine and genuine.image_is_zero
    escapes = ((g(1), g(0, -1)), (g(0, -1), g(-1)))
    spurious = accepted(reduced_zero_is_genuine(escapes, projector, psi))
    assert not spurious.genuine and not spurious.image_is_zero and spurious.leakage_energy > 0


def test_weighted_form_kernel_equals_common_kernel_for_positive_definite_weights() -> None:
    rng = random.Random(11)
    for _ in range(10):
        dimension = rng.randint(2, 4)
        maps, weights = [], []
        for _ in range(rng.randint(1, 3)):
            rows = rng.randint(1, 3)
            maps.append(
                tuple(tuple(random_gaussian(rng) if column else g(0) for column in range(dimension)) for _ in range(rows))
            )
            root = random_matrix(rng, rows, rows)
            weights.append(add(matmul(adjoint(root, rows), root, rows, QI), identity(rows, QI)))
        form = accepted(weighted_form_operator(maps, weights, dimension))
        assert form.weights_positive_definite
        assert adjoint(form.operator, dimension) == form.operator
        assert accepted(verify_congruence(form.operator_certificate)).positive_semidefinite
        comparison = accepted(kernel_matches_components(form))
        assert comparison.matches and comparison.separating_vector is None
        assert comparison.weights_positive_definite
        assert len(comparison.operator_kernel) >= 1


def test_semidefinite_weights_can_break_the_kernel_equivalence() -> None:
    zero_weight = accepted(weighted_form_operator((((1, 0), (0, 0)),), (((0, 0), (0, 0)),), 2))
    comparison = accepted(kernel_matches_components(zero_weight))
    assert not comparison.matches and not comparison.weights_positive_definite
    witness = comparison.separating_vector
    assert witness is not None and apply(zero_weight.maps[0], witness, QI) != (g(0), g(0))
    partial = accepted(weighted_form_operator((identity(2, QI),), (((1, 0), (0, 0)),), 2))
    assert not accepted(kernel_matches_components(partial)).matches
    definite = accepted(weighted_form_operator((identity(2, QI),), (((2, g(0, 1)), (g(0, -1), 1)),), 2))
    assert accepted(kernel_matches_components(definite)).matches
    empty = accepted(weighted_form_operator((), (), 2))
    assert accepted(kernel_matches_components(empty)).matches


def test_weighted_form_refusals_and_tamper() -> None:
    refused(weighted_form_operator((), (), -1), RefusalCode.INVALID_INPUT, "dimension")
    refused(weighted_form_operator((), (), True), RefusalCode.INVALID_INPUT, "dimension")
    refused(weighted_form_operator(((1, 0),), (), 2), RefusalCode.INVALID_INPUT, "one weight per map")
    refused(weighted_form_operator("maps", "w", 2), RefusalCode.INVALID_INPUT, "one weight per map")
    refused(weighted_form_operator((((1, 0, 0),),), (((1,),),), 2), RefusalCode.INVALID_INPUT, "shape")
    refused(weighted_form_operator((((1, 0),),), (((1, 0),),), 2), RefusalCode.INVALID_INPUT, "shape")
    refused(weighted_form_operator((((0.5, 0),),), (((1,),),), 2), RefusalCode.INVALID_INPUT)
    refused(weighted_form_operator((identity(2, QI),), (((1, 1), (0, 1)),), 2), RefusalCode.NOT_HERMITIAN)
    refused(
        weighted_form_operator((identity(2, QI),), (((1, 0), (0, -1)),), 2),
        RefusalCode.NOT_POSITIVE_SEMIDEFINITE,
        "weight 0",
    )
    form = accepted(weighted_form_operator((identity(2, QI),), (identity(2, QI),), 2))
    refused(kernel_matches_components("form"), RefusalCode.INVALID_INPUT)
    tampered = replace(form, operator=add(form.operator, identity(2, QI)))
    refused(kernel_matches_components(tampered), RefusalCode.CERTIFICATE_MISMATCH, "sum_a")
    indefinite = replace(form, weights=(((g(1), g(0)), (g(0), g(-1))),))
    refused(kernel_matches_components(indefinite), RefusalCode.NOT_POSITIVE_SEMIDEFINITE)


@pytest.mark.parametrize(
    ("projector", "fragment"),
    [
        (((1, 1), (0, 0)), "self-adjoint"),
        (((1, 0), (0, Fraction(1, 2))), "idempotent"),
        (((2, 0), (0, 0)), "idempotent"),
    ],
)
def test_projector_validation_refuses_non_orthogonal_projectors(projector, fragment) -> None:
    refused(validate_projector(projector, 2), RefusalCode.NOT_ORTHOGONAL_PROJECTOR, fragment)
    refused(truncation_leakage(((0, 0), (0, 0)), projector), RefusalCode.NOT_ORTHOGONAL_PROJECTOR, fragment)
    refused(reduced_zero_is_genuine(((0, 0), (0, 0)), projector, (1, 0)), RefusalCode.NOT_ORTHOGONAL_PROJECTOR)


def test_truncation_input_refusals() -> None:
    refused(truncation_leakage(((1, 2),), ((1,),)), RefusalCode.INVALID_INPUT, "square")
    refused(truncation_leakage(((0.5,),), ((1,),)), RefusalCode.INVALID_INPUT)
    refused(truncation_leakage(((1, 0), (0, 1)), ((1,),)), RefusalCode.INVALID_INPUT, "shape")
    refused(reduced_zero_is_genuine(((1, 2),), ((1,),), (1,)), RefusalCode.INVALID_INPUT, "square")
    refused(reduced_zero_is_genuine(A3, P3, (1, 0)), RefusalCode.INVALID_INPUT, "length 3")
    refused(reduced_zero_is_genuine(A3, P3, (0, 0, 0)), RefusalCode.INVALID_INPUT, "zero vector")
    refused(reduced_zero_is_genuine(A3, P3, (0, 0, 1)), RefusalCode.OUTSIDE_CARRIER, "range of P")
    refused(reduced_zero_is_genuine(identity(3, QI), P3, (1, 0, 0)), RefusalCode.NOT_A_REDUCED_ZERO)


def test_truncation_zero_is_never_a_physical_zero_mode() -> None:
    record = accepted(truncation_leakage(A3, P3))
    zero = accepted(reduced_zero_is_genuine(A3, P3, (1, 0, 0)))
    assert isinstance(record, TruncationLeakage) and isinstance(zero, ReducedZero)
    for evidence in (record, zero):
        for target in ("physical zero-mode", "Hamiltonian ground state", "probability leak"):
            refused(promote_truncation_zero(evidence, target), RefusalCode.SCOPE_VIOLATION, "zero-mode")
    refused(promote_truncation_zero("zero", "physical zero-mode"), RefusalCode.INVALID_INPUT)


# Executable finite evidence; AuthorityEffect: None.
