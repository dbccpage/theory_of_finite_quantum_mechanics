from fractions import Fraction

from witnessed_difference.cochains import FiniteComplex
from witnessed_difference.complex_growth import (
    attach_face,
    claim_growth_repair,
    growth_receipt,
    make_window,
    restrict_complex,
    subdivide_edge,
)
from witnessed_difference.contraction import (
    assemble_map,
    homology_dimensions,
    is_normalized,
    make_complex,
    normalize_homotopy,
    perturb,
    retraction_defect,
    validate_contraction,
)
from witnessed_difference.interference import (
    power_readout,
    quadratic_readout,
    sorkin_alternating_sum,
)
from witnessed_difference.obstruction import (
    DiagnosticClass,
    promote_diagnostic,
    verify_quotient_certificate,
)
from witnessed_difference.outcomes import Accepted, AuthorityEffect, RefusalCode, Refused
from witnessed_difference.pointed_relation import closed_form_census, enumerate_pointed_relations
from witnessed_difference.presentation_descent import all_sections, factor_through, section_test
from witnessed_difference.presentation_recovery import (
    detection_scope,
    euclidean_recovery_certificate,
    injective_on_subspace,
    noisy_recovery_bound,
    promote_presentation_evidence,
)
from witnessed_difference.receipts import make_receipt, verify_receipt
from witnessed_difference.state_spaces import is_simplex_decomposition_unique, square_state_space
from witnessed_difference.truncation import (
    kernel_matches_components,
    promote_truncation_zero,
    reduced_zero_is_genuine,
    truncation_leakage,
    weighted_form_operator,
)


def _value(outcome):
    assert isinstance(outcome, Accepted), outcome
    assert outcome.authority_effect is AuthorityEffect.NONE
    return outcome.value


def _refused(outcome, code: RefusalCode) -> Refused:
    assert isinstance(outcome, Refused), outcome
    assert outcome.code is code, outcome
    return outcome


def test_growth_chain_never_lowers_phi_and_is_never_a_repair() -> None:
    path = FiniteComplex((0, 1, 2), ((0, 1), (1, 2)))
    start = _value(make_window(path, {(0, 1): 1, (1, 2): 1}, {(0, 1): 2, (1, 2): 1}))
    triangle = FiniteComplex((0, 1, 2), ((0, 1), (1, 2), (0, 2)))
    grown = _value(make_window(triangle, {(0, 1): 1, (1, 2): 1, (0, 2): -1}, {(0, 1): 2, (1, 2): 1, (0, 2): 3}))
    assert _value(restrict_complex(grown, (0, 1, 2), ((0, 1), (1, 2)))) == start
    filled = _value(attach_face(grown, (0, 1, 2)))
    split = _value(subdivide_edge(grown, (0, 2), "m", Fraction(-1, 3)))
    chain = [start, grown, filled]
    receipts = [_value(growth_receipt(before, after)) for before, after in zip(chain, chain[1:])]
    receipts.append(_value(growth_receipt(grown, split)))
    assert [receipt.phi1_change >= 0 for receipt in receipts] == [True] * 3
    assert receipts[0].after_phi1 == 3 and receipts[1].phi1_change == 0 and receipts[2].phi1_change == 0
    assert receipts[1].after_class is DiagnosticClass.ACTIVE_CLOSURE_FAILURE
    for receipt in receipts:
        _refused(claim_growth_repair(receipt), RefusalCode.SCOPE_VIOLATION)
        assert _value(verify_quotient_certificate(receipt.after_certificate)) is receipt.after_certificate
        _refused(promote_diagnostic(receipt.after_certificate, "ExactRepair"), RefusalCode.SCOPE_VIOLATION)


def test_presentation_recovery_pipeline_binds_a_receipt_and_stops_at_the_subspace() -> None:
    basis, rows = ((1, 0, 1, 0), (0, 1, 0, 1)), ((1, 0, 0, 0), (0, 0, 0, 1))
    record = _value(injective_on_subspace(rows, basis))
    certificate = _value(euclidean_recovery_certificate(rows, basis, Fraction(1, 2)))
    noisy = _value(noisy_recovery_bound(certificate, (3, -1, 3, -1), (Fraction(5, 2), Fraction(-1)), Fraction(1, 2)))
    assert noisy.bound_holds
    receipt = _value(
        make_receipt(
            "coupled-two-edge-recovery",
            {"basis": basis, "rows": rows},
            {"constant_squared": certificate.constant_squared, "threshold": certificate.threshold},
            ("WDP-CH14-P02", "WDP-CH14-P03"),
        )
    )
    outputs = {"constant_squared": Fraction(2), "threshold": Fraction(1, 2)}
    assert _value(verify_receipt(receipt, {"basis": basis, "rows": rows}, outputs)) is True
    _refused(verify_receipt(receipt, {"basis": basis, "rows": rows}, {**outputs, "threshold": Fraction(51, 100)}), RefusalCode.DIGEST_MISMATCH)
    _refused(detection_scope(record, (0, 1, 0, 0)), RefusalCode.SCOPE_VIOLATION)
    for evidence in (record, certificate, noisy):
        _refused(promote_presentation_evidence(evidence, "authorize sensor suite"), RefusalCode.SCOPE_VIOLATION)


def test_weighted_forms_and_truncation_leakage_pipeline() -> None:
    form = _value(weighted_form_operator((((1, 0, 0),), ((0, 1, 0),)), (((2,),), ((3,),)), 3))
    comparison = _value(kernel_matches_components(form))
    assert comparison.matches and len(comparison.operator_kernel) == 1
    projector = ((1, 0, 0), (0, 1, 0), (0, 0, 0))
    operator = ((0, 0, 0), (0, 0, 0), (0, 5, 0))
    leakage = _value(truncation_leakage(operator, projector))
    assert leakage.identity_holds and not leakage.leakage_free
    genuine = _value(reduced_zero_is_genuine(operator, projector, (1, 0, 0)))
    spurious = _value(reduced_zero_is_genuine(operator, projector, (0, 1, 0)))
    assert genuine.genuine and not spurious.genuine and spurious.leakage_energy == 25
    for evidence in (leakage, genuine, spurious):
        _refused(promote_truncation_zero(evidence, "physical zero-mode"), RefusalCode.SCOPE_VIOLATION)


def test_contraction_pipeline_from_per_degree_blocks_to_a_perturbed_normalized_contraction() -> None:
    big = _value(make_complex((2, 2, 1), (((0, 0), (0, 1)), ((0, 0),))))
    small = _value(make_complex((1, 1, 1), (((0,),), ((0,),))))
    inclusion = _value(assemble_map(small.dims, big.dims, 0, (((1,), (0,)), ((1,), (0,)), ((1,),))))
    retraction = _value(assemble_map(big.dims, small.dims, 0, (((1, 0),), ((1, 0),), ((1,),))))
    defect = _value(retraction_defect(big, small, inclusion, retraction))
    assert defect.kernel_acyclic and defect.diagnostic_class is DiagnosticClass.EXACT_CLASS
    raw = _value(validate_contraction(big, small, inclusion, retraction, defect.homotopy))
    contraction = _value(normalize_homotopy(raw))
    assert _value(is_normalized(contraction)).normalized
    delta = _value(assemble_map(big.dims, big.dims, 1, (((1, 1), (1, 0)), ((1, -1),), ())))
    perturbed = _value(perturb(contraction, delta))
    assert _value(is_normalized(perturbed)).normalized
    assert _value(homology_dimensions(perturbed.big)) == _value(homology_dimensions(perturbed.small)) == (1, 0, 0)


def test_finite_census_descent_state_space_and_interference_agree() -> None:
    assert _value(enumerate_pointed_relations()) == _value(closed_form_census())
    domain, codomain = (0, 1, 2), ("p", "q")
    quotient, target = {0: "p", 1: "p", 2: "q"}, {0: "a", 1: "a", 2: "b"}
    assert dict(_value(factor_through(domain, codomain, quotient, target)).factor) == {"p": "a", "q": "b"}
    for section in _value(all_sections(domain, codomain, quotient)):
        assert _value(section_test(domain, codomain, quotient, target, dict(section))).zero_defect
    verdict = _value(is_simplex_decomposition_unique(square_state_space(), (0, 0)))
    assert not verdict.simplex and not verdict.unique
    amplitudes = (1, 1, 1)
    assert _value(sorkin_alternating_sum(amplitudes, (0, 1, 2), quadratic_readout())) == 0
    assert _value(sorkin_alternating_sum(amplitudes, (0, 1, 2), _value(power_readout(2)))) == 36


# Executable finite evidence; AuthorityEffect: None.
