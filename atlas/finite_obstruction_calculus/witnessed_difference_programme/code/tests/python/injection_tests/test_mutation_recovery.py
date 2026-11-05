"""Adversarial negative controls complement the source-mutation harness."""

from __future__ import annotations

import hashlib
from pathlib import Path

import pytest
from witnessed_difference.cochains import FiniteComplex, cochain_l1, finite_quotient_l1
from witnessed_difference.duration import (
    ClockProfile,
    DurationClass,
    check_clock,
    classify_duration,
    duration_sum,
)
from witnessed_difference.histories import (
    FiniteHistoryGraph,
    WeightedEdge,
    cancellation_report,
    finite_history_sum,
)
from witnessed_difference.measurement import (
    Calibration,
    CalibrationLink,
    IndicationValueMap,
    MeasurandSpecification,
    MetrologicalTraceability,
    NumericScale,
    Provenance,
    ReportedValue,
    measure,
)
from witnessed_difference.observation import (
    EvaluatorResult,
    EvaluatorStanding,
    EvaluatorStatus,
    Interaction,
    ObservationReceipt,
    classify_observation,
)
from witnessed_difference.observer import (
    OperationalObserverPacket,
    validate_report_profile_separation,
)
from witnessed_difference.outcomes import Accepted, AuthorityEffect, RefusalCode, Refused
from witnessed_difference.quantum import (
    QuantumEvidence,
    fixed_scale_phase,
    holonomy,
    make_connection,
    supports_quantum_reconstruction,
)
from witnessed_difference.receipts import make_receipt, verify_receipt
from witnessed_difference.relative_status import Claim, ClaimStatus, EvaluationProfile, route_claim
from witnessed_difference.witness import Registration, make_witness


def _source_digest() -> str:
    package = Path(__file__).resolve().parents[3] / "witnessed_difference"
    digest = hashlib.sha256()
    for path in sorted(package.glob("*.py")):
        digest.update(path.name.encode("utf-8"))
        digest.update(path.read_bytes())
    return digest.hexdigest()


def _observation():
    registration = Registration("log", "1", 0)
    witness = make_witness(registration, "1", "E")
    assert isinstance(witness, Accepted)
    observation = classify_observation(
        ObservationReceipt(
            Interaction(("source", "log"), "log"),
            registration,
            witness.value,
            EvaluatorResult("E", EvaluatorStatus.ACCEPT, EvaluatorStanding.ACCEPTING),
        )
    )
    assert isinstance(observation, Accepted)
    return observation.value


def _orientation_flip() -> bool:
    complex_ = FiniteComplex(("a", "b", "c"), (("a", "b"), ("b", "c"), ("a", "c")), (("a", "b", "c"),))
    result = classify_duration(complex_, {("a", "b"): -1, ("b", "c"): 1, ("a", "c"): 2})
    return result.kind is DurationClass.ACTIVE_CLOSURE_FAILURE


def _d1d0_break() -> bool:
    complex_ = FiniteComplex(("a", "b", "c"), (("a", "b"), ("b", "c"), ("a", "c")), (("a", "b", "c"),))
    result = classify_duration(complex_, {("a", "b"): 1, ("b", "c"): 1, ("a", "c"): 3})
    return result.kind is DurationClass.ACTIVE_CLOSURE_FAILURE


def _occurrence_change(mutated: tuple[str, ...]) -> bool:
    baseline = make_receipt("occurrences", ("a", "b", "c"), 3, ("WDP-CH07-P03",))
    assert isinstance(baseline, Accepted)
    result = verify_receipt(baseline.value, mutated, 3)
    return isinstance(result, Refused) and result.code is RefusalCode.DIGEST_MISMATCH


def _raw_l1_substitution() -> bool:
    complex_ = FiniteComplex(("a", "b"), (("a", "b"),))
    cochain = {("a", "b"): 2}
    quotient = finite_quotient_l1(complex_, cochain, ({"a": 0, "b": 0}, {"a": 0, "b": 2}))
    assert isinstance(quotient, Accepted)
    return quotient.value[0] == 0 and cochain_l1(complex_, cochain) == 2


def _bad_weight(value: int) -> bool:
    result = duration_sum((value,))
    return isinstance(result, Refused) and result.code is RefusalCode.INVALID_INPUT


def _open_holonomy() -> bool:
    connection = make_connection(("a", "b"), (("a", "b", 1 + 0j),))
    assert isinstance(connection, Accepted)
    result = holonomy(connection.value, ("a", "b"))
    return isinstance(result, Refused) and result.code is RefusalCode.OPEN_PATH


def _reverse_not_conjugate() -> bool:
    result = make_connection(("a", "b"), (("a", "b", 1j), ("b", "a", 1j)))
    return isinstance(result, Refused) and result.code is RefusalCode.NON_UNIT_PHASE


def _missing_phase_scale() -> bool:
    result = fixed_scale_phase(1, 0)
    return isinstance(result, Refused) and result.code is RefusalCode.INVALID_INPUT


def _report_profile_collapse() -> bool:
    observer = OperationalObserverPacket(
        ("s0", "s1"), "s0", ("x",), (),
        (("s0", "same"), ("s1", "same")),
        (("s0", "p0"), ("s1", "p1")),
    )
    result = validate_report_profile_separation(observer)
    return isinstance(result, Refused) and result.code is RefusalCode.REPORT_PROFILE_COLLAPSE


def _accept_without_reaccess() -> bool:
    result = classify_observation(
        ObservationReceipt(
            Interaction(("source", "log"), "log"),
            Registration("log", "mark", 0),
            None,
            EvaluatorResult("E", EvaluatorStatus.ACCEPT, EvaluatorStanding.ACCEPTING),
        )
    )
    return isinstance(result, Refused) and result.code is RefusalCode.NO_WITNESS


def _measurement_args() -> list[object]:
    return [
        _observation(),
        MeasurandSpecification("temperature", "sample", ("ambient",)),
        ReportedValue("display", 1),
        NumericScale("s", "u", 0, 2, 1),
        Calibration("c", "s", "E", 0),
        0,
        Provenance(("registration", "reaccess")),
        MetrologicalTraceability(
            (CalibrationLink("c", "SI", "reference", 0),),
            "SI",
            "external_standard",
            "additive_upper_bound",
        ),
        IndicationValueMap("log-to-display", "log", "display"),
    ]


def _measurement_missing_scale() -> bool:
    args = _measurement_args()
    args[3] = None
    result = measure(*args)
    return isinstance(result, Refused) and result.code is RefusalCode.MISSING_SCALE


def _measurement_from_attempt_receipt() -> bool:
    args = _measurement_args()
    args[0] = args[0].receipt
    result = measure(*args)
    return isinstance(result, Refused) and result.code is RefusalCode.MISSING_OBSERVATION


def _measurement_missing_value() -> bool:
    args = _measurement_args()
    args[2] = ReportedValue("display", None)
    result = measure(*args)
    return isinstance(result, Refused) and result.code is RefusalCode.MISSING_REPORTED_VALUE


def _measurement_value_map_mismatch() -> bool:
    args = _measurement_args()
    args[2] = ReportedValue("display", 2)
    result = measure(*args)
    return isinstance(result, Refused) and result.code is RefusalCode.VALUE_MAP_MISMATCH


def _evaluator_mismatch() -> bool:
    args = _measurement_args()
    args[4] = Calibration("c", "s", "other", 0)
    result = measure(*args)
    return isinstance(result, Refused) and result.code is RefusalCode.EVALUATOR_MISMATCH


def _missing_chain_uncertainty() -> bool:
    args = _measurement_args()
    args[7] = MetrologicalTraceability(
        (CalibrationLink("c", "SI", "reference", None),),
        "SI",
        "external_standard",
        "additive_upper_bound",
    )
    result = measure(*args)
    return isinstance(result, Refused) and result.code is RefusalCode.MISSING_CHAIN_UNCERTAINTY


def _provenance_as_traceability() -> bool:
    args = _measurement_args()
    args[7] = args[6]
    result = measure(*args)
    return isinstance(result, Refused) and result.code is RefusalCode.TRACEABILITY_TYPE_CONFUSION


def _clock_mutation(profile: ClockProfile, code: RefusalCode) -> bool:
    result = check_clock(profile)
    return isinstance(result, Refused) and result.code is code


def _aggregate_as_pointwise() -> bool:
    report = cancellation_report((1, -1))
    return report["aggregate_zero"] is True and report["pointwise_zero"] is False


def _unbounded_star() -> bool:
    graph = FiniteHistoryGraph(("a",), (WeightedEdge("a", "a", 1),))
    result = finite_history_sum(graph, "a", "a", None)
    return isinstance(result, Refused) and result.code is RefusalCode.BUDGET_REQUIRED


def _classical_shadow_promotion() -> bool:
    result = supports_quantum_reconstruction(QuantumEvidence.CLASSICAL_SHADOW)
    return result.code is RefusalCode.SCOPE_VIOLATION


def _outside_profile_as_refuted() -> bool:
    routed = route_claim(Claim("C", ClaimStatus.CONJECTURE), EvaluationProfile("E", frozenset()))
    return routed.relative_status is ClaimStatus.OUTSIDE_PROFILE and routed.relative_status is not ClaimStatus.REFUTED


def _observer_acceptance_as_authority() -> bool:
    observation = _observation()
    return observation.authority_effect is AuthorityEffect.NONE and not hasattr(observation, "authority")


NEGATIVE_CONTROLS = {
    "orientation_flip": _orientation_flip,
    "d1d0_break": _d1d0_break,
    "deleted_occurrence": lambda: _occurrence_change(("a", "c")),
    "duplicated_occurrence": lambda: _occurrence_change(("a", "b", "b", "c")),
    "raw_l1_for_quotient": _raw_l1_substitution,
    "zero_duration_weight": lambda: _bad_weight(0),
    "negative_duration_weight": lambda: _bad_weight(-1),
    "open_path_as_holonomy": _open_holonomy,
    "reverse_without_conjugation": _reverse_not_conjugate,
    "missing_phase_scale": _missing_phase_scale,
    "report_profile_collapse": _report_profile_collapse,
    "accept_without_reaccess": _accept_without_reaccess,
    "measurement_without_scale": _measurement_missing_scale,
    "measurement_from_attempt_receipt": _measurement_from_attempt_receipt,
    "measurement_without_value": _measurement_missing_value,
    "measurement_value_map_mismatch": _measurement_value_map_mismatch,
    "measurement_evaluator_mismatch": _evaluator_mismatch,
    "calibration_chain_missing_uncertainty": _missing_chain_uncertainty,
    "provenance_as_traceability": _provenance_as_traceability,
    "clock_zero_denominator": lambda: _clock_mutation(
        ClockProfile("s", 0, frozenset({0}), frozenset({0}), True), RefusalCode.INVALID_INPUT
    ),
    "clock_missing_coverage": lambda: _clock_mutation(
        ClockProfile("s", 1, frozenset(), frozenset({0}), True), RefusalCode.OUTSIDE_CARRIER
    ),
    "clock_uncoupled": lambda: _clock_mutation(
        ClockProfile("s", 1, frozenset({0}), frozenset({0}), False), RefusalCode.REACCESS_FAILED
    ),
    "aggregate_as_pointwise": _aggregate_as_pointwise,
    "unbounded_history_star": _unbounded_star,
    "classical_shadow_as_quantum": _classical_shadow_promotion,
    "outside_profile_as_refuted": _outside_profile_as_refuted,
    "observer_acceptance_as_authority": _observer_acceptance_as_authority,
}


@pytest.mark.parametrize("control_id", tuple(NEGATIVE_CONTROLS), ids=tuple(NEGATIVE_CONTROLS))
def test_negative_control_is_refused_and_pristine_receipt_recovers(control_id: str) -> None:
    source_before = _source_digest()
    baseline = make_receipt(
        "negative-control-baseline",
        {"control_id": control_id},
        {"state": "pristine"},
        ("WDP-CH00-N03",),
    )
    assert isinstance(baseline, Accepted)
    tampered = verify_receipt(
        baseline.value,
        {"control_id": control_id},
        {"state": "mutated"},
    )
    assert isinstance(tampered, Refused) and tampered.code is RefusalCode.DIGEST_MISMATCH
    assert NEGATIVE_CONTROLS[control_id](), f"negative control was not refused: {control_id}"
    recovered = make_receipt(
        "negative-control-baseline",
        {"control_id": control_id},
        {"state": "pristine"},
        ("WDP-CH00-N03",),
    )
    assert isinstance(recovered, Accepted)
    assert recovered.value.receipt_digest == baseline.value.receipt_digest
    assert _source_digest() == source_before


# --- Obstruction-branch negative controls (ported primitive-axiomatics evidence) ---


def _refused_with(outcome: object, code: RefusalCode) -> bool:
    return isinstance(outcome, Refused) and outcome.code is code


def _square_graph() -> FiniteComplex:
    return FiniteComplex((0, 1, 2, 3), ((0, 1), (1, 2), (2, 3), (0, 3), (0, 2)))


def _dual_bound_tamper() -> bool:
    from dataclasses import replace
    from fractions import Fraction

    from witnessed_difference.obstruction import exact_quotient_l1, verify_quotient_certificate

    graph = _square_graph()
    certificate = exact_quotient_l1(graph, dict(zip(graph.edges, (1, 0, 0, 0, 0))))
    assert isinstance(certificate, Accepted)
    oversized = tuple(Fraction(value) for value in (1, 1, 5, -5, 4))
    tampered = verify_quotient_certificate(replace(certificate.value, dual=oversized))
    return _refused_with(tampered, RefusalCode.CERTIFICATE_MISMATCH)


def _closure_undeclared() -> bool:
    from witnessed_difference.obstruction import obstruction_signature

    graph = _square_graph()
    outcome = obstruction_signature(graph, dict(zip(graph.edges, (1, 0, 0, 0, 0))), closure_declared=False)
    return _refused_with(outcome, RefusalCode.NO_RULE)


def _diagnostic_as_terminal() -> bool:
    from witnessed_difference.obstruction import obstruction_signature, promote_diagnostic

    graph = _square_graph()
    signature = obstruction_signature(graph, dict(zip(graph.edges, (1, 0, 0, 0, 0))), closure_declared=True)
    assert isinstance(signature, Accepted)
    return all(
        _refused_with(promote_diagnostic(signature.value, target), RefusalCode.SCOPE_VIOLATION)
        for target in ("ExactRepair", "StabilizedSurvivor", "OpenObstruction", "authority")
    )


def _observer_sees_repairs() -> bool:
    from witnessed_difference.quotient_observer import make_linear_quotient_observer

    return _refused_with(
        make_linear_quotient_observer(_square_graph(), ((1, 0, 0, 0, 0),)), RefusalCode.NOT_REPAIR_COMPATIBLE
    )


def _observer_authority_layer() -> bool:
    from witnessed_difference.quotient_observer import (
        make_linear_quotient_observer,
        quotient_observer_layers,
    )

    observer = make_linear_quotient_observer(_square_graph(), ((1, 1, 0, 0, -1),))
    assert isinstance(observer, Accepted)
    return _refused_with(quotient_observer_layers(observer.value, ("authority",)), RefusalCode.SCOPE_VIOLATION)


def _net_charge_gauss_law() -> bool:
    from witnessed_difference.simplicial import gauss_law_solvable

    return _refused_with(gauss_law_solvable(_square_graph(), {0: 1, 1: 0, 2: 0, 3: 0}), RefusalCode.INFEASIBLE)


def _non_unit_rephasing() -> bool:
    from witnessed_difference.projective import GaussianRational, klein_four_pauli, rephase

    representation = klein_four_pauli()
    lam = dict.fromkeys(representation.elements, GaussianRational(1, 1))
    return _refused_with(rephase(representation, lam), RefusalCode.NON_UNIT_PHASE)


def _singular_coordinate_change() -> bool:
    from witnessed_difference.context_witness import ContextualSystem, apply_coordinate_change

    system = ContextualSystem(("a", "b"), {}, {"a": (0, 1), "b": (1, 0)})
    return _refused_with(apply_coordinate_change(system, ((1, 1), (1, 1))), RefusalCode.NOT_INVERTIBLE)


def _report_outside_grammar() -> bool:
    from witnessed_difference.quotient_observer import grammar_resolution

    return _refused_with(grammar_resolution(("q",), {"q": "zz"}, ("a",)), RefusalCode.GRAMMAR_VIOLATION)


def _float_quotient_weight() -> bool:
    from witnessed_difference.obstruction import exact_quotient_l1

    graph = _square_graph()
    weights = dict.fromkeys(graph.edges, 0.5)
    return _refused_with(
        exact_quotient_l1(graph, dict(zip(graph.edges, (1, 0, 0, 0, 0))), weights), RefusalCode.INVALID_INPUT
    )


OBSTRUCTION_NEGATIVE_CONTROLS = {
    "dual_bound_tamper": _dual_bound_tamper,
    "closure_undeclared": _closure_undeclared,
    "diagnostic_as_terminal": _diagnostic_as_terminal,
    "observer_sees_repairs": _observer_sees_repairs,
    "observer_authority_layer": _observer_authority_layer,
    "net_charge_gauss_law": _net_charge_gauss_law,
    "non_unit_rephasing": _non_unit_rephasing,
    "singular_coordinate_change": _singular_coordinate_change,
    "report_outside_grammar": _report_outside_grammar,
    "float_quotient_weight": _float_quotient_weight,
}


@pytest.mark.parametrize(
    "control_id", tuple(OBSTRUCTION_NEGATIVE_CONTROLS), ids=tuple(OBSTRUCTION_NEGATIVE_CONTROLS)
)
def test_obstruction_negative_control_is_refused_and_source_is_unchanged(control_id: str) -> None:
    source_before = _source_digest()
    assert OBSTRUCTION_NEGATIVE_CONTROLS[control_id](), f"negative control was not refused: {control_id}"
    assert _source_digest() == source_before


# --- Absorbed finite-proposition negative controls (sibling-paper evidence) ---


def _non_relation_as_pointed_relation() -> bool:
    from witnessed_difference.pointed_relation import make_pointed_relation

    return _refused_with(make_pointed_relation((0, 1), [(0, 1, 1)], 0, 1), RefusalCode.INVALID_INPUT)


def _growth_as_repair() -> bool:
    from witnessed_difference.complex_growth import (
        claim_growth_repair,
        growth_receipt,
        make_window,
        restrict_complex,
    )

    triangle = FiniteComplex((0, 1, 2), ((0, 1), (1, 2), (0, 2)))
    big = make_window(triangle, {(0, 1): 1, (1, 2): 1, (0, 2): -1})
    assert isinstance(big, Accepted)
    small = restrict_complex(big.value, (0, 1, 2), ((0, 1), (1, 2)))
    assert isinstance(small, Accepted)
    receipt = growth_receipt(big.value, small.value)
    assert isinstance(receipt, Accepted) and receipt.value.phi1_change < 0
    return _refused_with(claim_growth_repair(receipt.value), RefusalCode.SCOPE_VIOLATION)


def _non_idempotent_projector() -> bool:
    from fractions import Fraction

    from witnessed_difference.truncation import truncation_leakage

    return _refused_with(
        truncation_leakage(((0, 0), (0, 0)), ((1, 0), (0, Fraction(1, 2)))), RefusalCode.NOT_ORTHOGONAL_PROJECTOR
    )


def _indefinite_weight() -> bool:
    from witnessed_difference.truncation import weighted_form_operator

    return _refused_with(
        weighted_form_operator((((1, 0), (0, 1)),), (((1, 0), (0, -1)),), 2), RefusalCode.NOT_POSITIVE_SEMIDEFINITE
    )


def _truncation_zero_as_physical_mode() -> bool:
    from witnessed_difference.truncation import promote_truncation_zero, reduced_zero_is_genuine

    zero = reduced_zero_is_genuine(((0, 0, 0), (0, 0, 0), (0, 1, 0)), ((1, 0, 0), (0, 1, 0), (0, 0, 0)), (0, 1, 0))
    assert isinstance(zero, Accepted) and zero.value.genuine is False
    return _refused_with(promote_truncation_zero(zero.value, "physical zero-mode"), RefusalCode.SCOPE_VIOLATION)


def _uncertified_recovery_constant() -> bool:
    from fractions import Fraction

    from witnessed_difference.presentation_recovery import euclidean_recovery_certificate

    rows, basis = ((1, 0, 0, 0), (0, 0, 0, 1)), ((1, 0, 1, 0), (0, 1, 0, 1))
    return _refused_with(
        euclidean_recovery_certificate(rows, basis, Fraction(51, 100)), RefusalCode.NOT_POSITIVE_SEMIDEFINITE
    )


def _detection_outside_subspace() -> bool:
    from witnessed_difference.presentation_recovery import detection_scope, injective_on_subspace

    record = injective_on_subspace(((1, 0, 0, 0), (0, 0, 0, 1)), ((1, 0, 1, 0), (0, 1, 0, 1)))
    assert isinstance(record, Accepted)
    return _refused_with(detection_scope(record.value, (0, 1, 0, 0)), RefusalCode.SCOPE_VIOLATION)


def _non_surjective_unique_factor() -> bool:
    from witnessed_difference.presentation_descent import factor_through

    return _refused_with(factor_through((0,), ("a", "b"), {0: "a"}, {0: 0}), RefusalCode.NOT_SURJECTIVE)


def _missing_homotopy_equation() -> bool:
    from witnessed_difference.contraction import make_total_complex, validate_contraction

    big, small = make_total_complex((2,), ((0, 0), (0, 0))), make_total_complex((1,), ((0,),))
    assert isinstance(big, Accepted) and isinstance(small, Accepted)
    outcome = validate_contraction(big.value, small.value, ((1,), (0,)), ((1, 0),), ((0, 0), (0, 0)))
    return _refused_with(outcome, RefusalCode.HOMOTOPY_MISMATCH)


def _singular_perturbation() -> bool:
    from witnessed_difference.contraction import make_total_complex, perturb, validate_contraction

    big, small = make_total_complex((2, 1), ((0, 0, 0), (0, 0, 0), (0, 1, 0))), make_total_complex((1, 0), ((0,),))
    assert isinstance(big, Accepted) and isinstance(small, Accepted)
    contraction = validate_contraction(big.value, small.value, ((1,), (0,), (0,)), ((1, 0, 0),), ((0, 0, 0), (0, 0, 1), (0, 0, 0)))
    assert isinstance(contraction, Accepted)
    return _refused_with(perturb(contraction.value, ((0, 0, 0), (0, 0, 0), (0, -1, 0))), RefusalCode.NOT_INVERTIBLE)


def _float_amplitude() -> bool:
    from witnessed_difference.interference import quadratic_readout, sorkin_alternating_sum

    return _refused_with(sorkin_alternating_sum((0.6, 0.8), (0, 1), quadratic_readout()), RefusalCode.INVALID_INPUT)


def _square_as_simplex() -> bool:
    from witnessed_difference.state_spaces import (
        is_simplex_decomposition_unique,
        square_state_space,
    )

    verdict = is_simplex_decomposition_unique(square_state_space(), (0, 0))
    return isinstance(verdict, Accepted) and not verdict.value.simplex and not verdict.value.unique


ABSORBED_NEGATIVE_CONTROLS = {
    "non_relation_as_pointed_relation": _non_relation_as_pointed_relation,
    "growth_as_repair": _growth_as_repair,
    "non_idempotent_projector": _non_idempotent_projector,
    "indefinite_weight": _indefinite_weight,
    "truncation_zero_as_physical_mode": _truncation_zero_as_physical_mode,
    "uncertified_recovery_constant": _uncertified_recovery_constant,
    "detection_outside_subspace": _detection_outside_subspace,
    "non_surjective_unique_factor": _non_surjective_unique_factor,
    "missing_homotopy_equation": _missing_homotopy_equation,
    "singular_perturbation": _singular_perturbation,
    "float_amplitude": _float_amplitude,
    "square_as_simplex": _square_as_simplex,
}


@pytest.mark.parametrize("control_id", tuple(ABSORBED_NEGATIVE_CONTROLS), ids=tuple(ABSORBED_NEGATIVE_CONTROLS))
def test_absorbed_negative_control_is_refused_and_source_is_unchanged(control_id: str) -> None:
    source_before = _source_digest()
    assert ABSORBED_NEGATIVE_CONTROLS[control_id](), f"negative control was not refused: {control_id}"
    assert _source_digest() == source_before
# Executable finite evidence; AuthorityEffect: None.
