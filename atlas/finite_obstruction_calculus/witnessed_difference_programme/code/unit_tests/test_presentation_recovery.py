
from witnessed_difference.native_functionals import squared_l2
import random
from dataclasses import replace
from fractions import Fraction
from itertools import combinations, product

import pytest
from witnessed_difference.exact_linear import ExactField, congruence_diagonalize, identity
from witnessed_difference.outcomes import Accepted, AuthorityEffect, RefusalCode, Refused
from witnessed_difference.presentation_recovery import (
    DeclaredPresentation,
    InjectivityRecord,
    declare_presentation,
    detection_scope,
    euclidean_recovery_certificate,
    injective_on_subspace,
    kernel_witness,
    noisy_recovery_bound,
    promote_presentation_evidence,
    suite_cost_lower_bound,
    verify_kernel_witness,
    verify_recovery_certificate,
)

Q = ExactField.RATIONAL
COUPLED_BASIS = ((1, 0, 1, 0), (0, 1, 0, 1))
COUPLED_REPORT = ((1, 0, 0, 0), (0, 0, 0, 1))


def accepted(outcome):
    assert isinstance(outcome, Accepted), outcome
    assert outcome.authority_effect is AuthorityEffect.NONE
    return outcome.value


def refused(outcome, code: RefusalCode, fragment: str = "") -> Refused:
    assert isinstance(outcome, Refused), outcome
    assert outcome.code is code, outcome
    assert fragment in outcome.detail, outcome.detail
    return outcome


def norm_squared(vector) -> Fraction:
    return squared_l2(tuple(Fraction(value) for value in vector))


def report(rows, vector):
    return tuple(sum((Fraction(a) * b for a, b in zip(row, vector)), start=Fraction(0)) for row in rows)


def test_coupled_two_edge_carrier_each_read_alone_has_a_kernel_on_y() -> None:
    record = accepted(injective_on_subspace(COUPLED_REPORT, COUPLED_BASIS))
    assert (record.report_coordinates, record.dimension, record.rank) == (2, 2, 2)
    first = refused(injective_on_subspace(COUPLED_REPORT[:1], COUPLED_BASIS), RefusalCode.NOT_INJECTIVE)
    assert "(0, 1, 0, 1)" in first.detail and "1 report coordinates for dim Y = 2" in first.detail
    assert accepted(kernel_witness(COUPLED_REPORT[:1], COUPLED_BASIS)) == (0, 1, 0, 1)
    assert accepted(kernel_witness(COUPLED_REPORT[1:], COUPLED_BASIS)) == (1, 0, 1, 0)
    refused(kernel_witness(COUPLED_REPORT, COUPLED_BASIS), RefusalCode.NO_WITNESS)


def test_coupled_ratio_is_exactly_one_half_and_certified_only_up_to_one_half() -> None:
    for s0, s1 in product(range(-3, 4), repeat=2):
        y = (s0, s1, s0, s1)
        assert norm_squared(report(COUPLED_REPORT, y)) * 2 == norm_squared(y)
    certificate = accepted(euclidean_recovery_certificate(COUPLED_REPORT, COUPLED_BASIS, Fraction(1, 2)))
    assert certificate.constant_squared == 2
    assert certificate.report_gram == identity(2, Q) and certificate.subspace_gram == ((2, 0), (0, 2))
    assert accepted(verify_recovery_certificate(certificate)) is certificate
    assert accepted(euclidean_recovery_certificate(COUPLED_REPORT, COUPLED_BASIS, "1/3")).threshold == Fraction(1, 3)
    refusal = refused(
        euclidean_recovery_certificate(COUPLED_REPORT, COUPLED_BASIS, Fraction(51, 100)),
        RefusalCode.NOT_POSITIVE_SEMIDEFINITE,
        "is not certified",
    )
    assert "||q y||^2 = 1 < t ||y||^2 = 51/50" in refusal.detail
    refused(euclidean_recovery_certificate(COUPLED_REPORT[:1], COUPLED_BASIS, Fraction(1, 100)), RefusalCode.NOT_POSITIVE_SEMIDEFINITE)
    for bad in (0, -1, 0.5, True, "x"):
        refused(euclidean_recovery_certificate(COUPLED_REPORT, COUPLED_BASIS, bad), RefusalCode.INVALID_INPUT, "threshold")


def test_fewer_report_coordinates_than_dim_y_always_yield_a_verified_kernel_witness() -> None:
    basis = ((1, 0, 0), (0, 1, 1))
    for row in product(range(-1, 2), repeat=3):
        witness = accepted(kernel_witness((row,), basis))
        assert accepted(verify_kernel_witness((row,), basis, witness)) == witness
        refused(injective_on_subspace((row,), basis), RefusalCode.NOT_INJECTIVE, "nonzero with q(y) = 0")
    refused(injective_on_subspace((), basis), RefusalCode.NOT_INJECTIVE, "0 report coordinates")


def test_injectivity_matches_a_determinant_test_exhaustively() -> None:
    basis = ((1, 0, 0), (0, 1, 1))
    for first, second in combinations(tuple(product(range(-1, 2), repeat=3)), 2):
        compressed = [report((first, second), vector) for vector in basis]
        determinant = compressed[0][0] * compressed[1][1] - compressed[0][1] * compressed[1][0]
        outcome = injective_on_subspace((first, second), basis)
        assert isinstance(outcome, Accepted) == (determinant != 0)


def test_kernel_witness_verification_refuses_tampered_witnesses() -> None:
    rows = COUPLED_REPORT[:1]
    assert accepted(verify_kernel_witness(rows, COUPLED_BASIS, (0, 3, 0, 3))) == (0, 3, 0, 3)
    refused(verify_kernel_witness(rows, COUPLED_BASIS, (0, 0, 0, 0)), RefusalCode.CERTIFICATE_MISMATCH, "zero vector")
    refused(verify_kernel_witness(rows, COUPLED_BASIS, (0, 1, 0, 0)), RefusalCode.CERTIFICATE_MISMATCH, "outside")
    refused(verify_kernel_witness(rows, COUPLED_BASIS, (1, 0, 1, 0)), RefusalCode.CERTIFICATE_MISMATCH, "kernel of q")
    refused(verify_kernel_witness(rows, COUPLED_BASIS, (0, 1, 0)), RefusalCode.INVALID_INPUT, "length 4")
    refused(verify_kernel_witness(rows, (), (0, 1, 0, 1)), RefusalCode.INVALID_INPUT, "nonzero subspace")


@pytest.mark.parametrize(
    ("rows", "basis", "fragment"),
    [
        (COUPLED_REPORT, (), "nonzero subspace"),
        (COUPLED_REPORT, ((1, 0, 1, 0), (2, 0, 2, 0)), "dependent"),
        (COUPLED_REPORT, ((0.5, 0, 1, 0),), "exact"),
        (COUPLED_REPORT, "basis", "sequence of rows"),
        (((1, 0, 0),), COUPLED_BASIS, "shape"),
        ("rows", COUPLED_BASIS, "sequence of rows"),
    ],
)
def test_declared_presentation_refusals(rows, basis, fragment) -> None:
    refused(declare_presentation(rows, basis), RefusalCode.INVALID_INPUT, fragment)
    refused(injective_on_subspace(rows, basis), RefusalCode.INVALID_INPUT, fragment)
    refused(kernel_witness(rows, basis), RefusalCode.INVALID_INPUT, fragment)
    refused(euclidean_recovery_certificate(rows, basis, 1), RefusalCode.INVALID_INPUT, fragment)


def test_certified_threshold_is_optimal_on_random_rational_presentations() -> None:
    rng = random.Random(3)
    for _ in range(25):
        basis = tuple(tuple(rng.randint(-2, 2) for _ in range(4)) for _ in range(2))
        rows = tuple(tuple(rng.randint(-2, 2) for _ in range(4)) for _ in range(rng.randint(1, 3)))
        if not isinstance(declare_presentation(rows, basis), Accepted):
            continue
        injective = isinstance(injective_on_subspace(rows, basis), Accepted)
        tiny = euclidean_recovery_certificate(rows, basis, Fraction(1, 10**6))
        assert isinstance(tiny, Accepted) == injective
        for coefficients in product(range(-2, 3), repeat=2):
            y = tuple(coefficients[0] * a + coefficients[1] * b for a, b in zip(*basis))
            if injective:
                assert norm_squared(report(rows, y)) >= tiny.value.threshold * norm_squared(y)


def test_verify_recovery_certificate_refuses_tamper() -> None:
    certificate = accepted(euclidean_recovery_certificate(COUPLED_REPORT, COUPLED_BASIS, Fraction(1, 2)))
    refused(verify_recovery_certificate("certificate"), RefusalCode.INVALID_INPUT)
    refused(verify_recovery_certificate(replace(certificate, presentation="p")), RefusalCode.INVALID_INPUT)
    broken = DeclaredPresentation(certificate.presentation.presentation, ((Fraction(1),) * 4,) * 2, 4)
    refused(verify_recovery_certificate(replace(certificate, presentation=broken)), RefusalCode.INVALID_INPUT)
    refused(verify_recovery_certificate(replace(certificate, threshold=1)), RefusalCode.CERTIFICATE_MISMATCH)
    refused(verify_recovery_certificate(replace(certificate, threshold=Fraction(-1))), RefusalCode.CERTIFICATE_MISMATCH)
    refused(
        verify_recovery_certificate(replace(certificate, threshold=Fraction(1, 4))),
        RefusalCode.CERTIFICATE_MISMATCH,
        "does not certify",
    )
    refused(
        verify_recovery_certificate(replace(certificate, report_gram=((Fraction(2), Fraction(0)), (Fraction(0), Fraction(2))))),
        RefusalCode.CERTIFICATE_MISMATCH,
        "Gram",
    )
    bad_congruence = replace(certificate.congruence, diagonal=(Fraction(1), Fraction(1)))
    refused(verify_recovery_certificate(replace(certificate, congruence=bad_congruence)), RefusalCode.CERTIFICATE_MISMATCH)
    negative = accepted(congruence_diagonalize(((-1, 0), (0, -1)), Q))
    refused(
        verify_recovery_certificate(replace(certificate, threshold=Fraction(1), congruence=negative)),
        RefusalCode.CERTIFICATE_MISMATCH,
        "does not certify",
    )


def test_noisy_recovery_bound_holds_exactly_on_a_grid() -> None:
    certificate = accepted(euclidean_recovery_certificate(COUPLED_REPORT, COUPLED_BASIS, Fraction(1, 2)))
    seen_slack = set()
    for s0, s1, e0, e1 in product(range(-2, 3), repeat=4):
        y = (s0, s1, s0, s1)
        noise = (Fraction(e0, 2), Fraction(e1, 3))
        reported = tuple(a + b for a, b in zip(report(COUPLED_REPORT, y), noise))
        epsilon = Fraction(abs(e0), 2) + Fraction(abs(e1), 3)
        record = accepted(noisy_recovery_bound(certificate, y, reported, epsilon))
        assert record.bound_holds
        assert record.constant_squared == 2 and record.noise_norm_squared <= epsilon * epsilon
        seen_slack.add(record.vector_norm_squared * Fraction(1, 2) > record.report_norm_squared + epsilon**2)
    assert seen_slack == {True, False}


def test_noisy_recovery_refusals() -> None:
    certificate = accepted(euclidean_recovery_certificate(COUPLED_REPORT, COUPLED_BASIS, Fraction(1, 2)))
    y = (1, 2, 1, 2)
    refused(noisy_recovery_bound("certificate", y, (1, 2), 0), RefusalCode.INVALID_INPUT)
    refused(noisy_recovery_bound(certificate, (1, 2, 1), (1, 2), 0), RefusalCode.INVALID_INPUT, "length 4")
    refused(noisy_recovery_bound(certificate, y, (1, 2, 3), 0), RefusalCode.INVALID_INPUT, "length 2")
    refused(noisy_recovery_bound(certificate, (1, 0, 0, 0), (1, 0), 0), RefusalCode.OUTSIDE_CARRIER)
    refused(noisy_recovery_bound(certificate, y, (1, 2), 0.1), RefusalCode.INVALID_INPUT, "noise bound")
    refused(noisy_recovery_bound(certificate, y, (1, 2), -1), RefusalCode.OUT_OF_RANGE)
    refused(noisy_recovery_bound(certificate, y, (2, 2), Fraction(1, 2)), RefusalCode.OUT_OF_RANGE, "epsilon")
    assert accepted(noisy_recovery_bound(certificate, y, (2, 2), 1)).bound_holds


def test_scalar_probe_suites_cost_at_least_the_dim_y_cheapest_probes() -> None:
    basis = ((1, 0), (0, 1))
    record = accepted(suite_cost_lower_bound([((1, 0),), ((0, 1),), ((1, 1),), ((2, 2),)], [3, 1, 2, 1], basis))
    assert (record.cheapest_sound_cost, record.cheapest_sound_suite, record.lower_bound) == (2, (1, 3), 2)
    assert record.bound_holds and record.sound_suites == 10 and record.dimension == 2
    rng = random.Random(5)
    for _ in range(30):
        probes = [(tuple(rng.randint(-1, 1) for _ in range(3)),) for _ in range(rng.randint(2, 6))]
        costs = [Fraction(rng.randint(1, 9), rng.randint(1, 3)) for _ in probes]
        outcome = suite_cost_lower_bound(probes, costs, ((1, 0, 0), (0, 1, 1)))
        if isinstance(outcome, Accepted):
            assert outcome.value.bound_holds
        else:
            refused(outcome, RefusalCode.INFEASIBLE)


def test_the_cost_bound_needs_one_scalar_row_per_probe() -> None:
    basis = ((1, 0), (0, 1))
    refused(
        suite_cost_lower_bound([((1, 0), (0, 1)), ((1, 1),)], [1, 5], basis), RefusalCode.SCOPE_VIOLATION, "one scalar row"
    )
    assert isinstance(injective_on_subspace(((1, 0), (0, 1)), basis), Accepted)
    refused(suite_cost_lower_bound([((1, 0),), ((2, 0),)], [1, 1], basis), RefusalCode.INFEASIBLE)
    refused(suite_cost_lower_bound([((1, 0),)], [1, 2], basis), RefusalCode.INVALID_INPUT, "one cost per probe")
    refused(suite_cost_lower_bound("p", [1], basis), RefusalCode.INVALID_INPUT, "one cost per probe")
    refused(suite_cost_lower_bound([((1, 0),)] * 13, [1] * 13, basis), RefusalCode.BUDGET_EXHAUSTED)
    refused(suite_cost_lower_bound([((0.5, 0),)], [1], basis), RefusalCode.INVALID_INPUT, "exact")
    refused(suite_cost_lower_bound([((1, 0),)], [0], basis), RefusalCode.INVALID_INPUT, "positive")
    refused(suite_cost_lower_bound([((1, 0),)], [1], ()), RefusalCode.INVALID_INPUT, "nonzero subspace")


def test_injectivity_on_y_certifies_no_detection_outside_y() -> None:
    record = accepted(injective_on_subspace(COUPLED_REPORT, COUPLED_BASIS))
    inside = accepted(detection_scope(record, (2, -1, 2, -1)))
    assert inside.detected and inside.report == (2, -1)
    assert not accepted(detection_scope(record, (0, 0, 0, 0))).detected
    silent = refused(detection_scope(record, (0, 1, 0, 0)), RefusalCode.SCOPE_VIOLATION, "outside Y")
    assert "reports zero" in silent.detail
    confusable = refused(detection_scope(record, (1, 0, 0, 0)), RefusalCode.SCOPE_VIOLATION, "outside Y")
    assert "reports zero" not in confusable.detail
    assert report(COUPLED_REPORT, (1, 0, 0, 0)) == report(COUPLED_REPORT, (1, 0, 1, 0))
    refused(detection_scope("record", (0, 0, 0, 0)), RefusalCode.INVALID_INPUT)
    refused(detection_scope(record, (0, 0)), RefusalCode.INVALID_INPUT, "length 4")
    blind = DeclaredPresentation(record.presentation.presentation[:1], record.presentation.basis, 4)
    refused(detection_scope(replace(record, presentation=blind), (0, 1, 0, 1)), RefusalCode.NOT_INJECTIVE)
    refused(detection_scope(replace(record, presentation="p"), (0, 1, 0, 1)), RefusalCode.INVALID_INPUT)


def test_presentation_evidence_never_selects_prices_or_authorizes() -> None:
    record = accepted(injective_on_subspace(COUPLED_REPORT, COUPLED_BASIS))
    certificate = accepted(euclidean_recovery_certificate(COUPLED_REPORT, COUPLED_BASIS, Fraction(1, 2)))
    noisy = accepted(noisy_recovery_bound(certificate, (1, 1, 1, 1), (1, 1), 0))
    suite = accepted(suite_cost_lower_bound([((1, 0),), ((0, 1),)], [1, 1], ((1, 0), (0, 1))))
    detection = accepted(detection_scope(record, (1, 1, 1, 1)))
    for evidence in (record, certificate, noisy, suite, detection):
        for target in ("detection certified", "adversarial behaviour detected", "authorize sensor suite"):
            refused(promote_presentation_evidence(evidence, target), RefusalCode.SCOPE_VIOLATION, "does not select")
    refused(promote_presentation_evidence("record", "detection certified"), RefusalCode.INVALID_INPUT)
    assert isinstance(record, InjectivityRecord)


def test_a_forged_ambient_dimension_is_refused_by_every_consumer() -> None:
    record = accepted(injective_on_subspace(((0, 1),), ((0, 1),)))
    forged_record = replace(record, presentation=replace(record.presentation, ambient=1))
    refused(detection_scope(forged_record, [0, 7]), RefusalCode.CERTIFICATE_MISMATCH, "differs from its recomputation")
    assert accepted(detection_scope(record, [0, 7])).detected is True
    certificate = accepted(euclidean_recovery_certificate(((0, 1),), ((0, 1),), 1))
    forged = replace(certificate, presentation=replace(certificate.presentation, ambient=1))
    refused(verify_recovery_certificate(forged), RefusalCode.CERTIFICATE_MISMATCH, "re-admitted form")
    refused(noisy_recovery_bound(forged, [5], [0], 0), RefusalCode.CERTIFICATE_MISMATCH, "re-admitted form")
    assert accepted(noisy_recovery_bound(certificate, [0, 5], [5], 0)).bound_holds is True


# Executable finite evidence; AuthorityEffect: None.
