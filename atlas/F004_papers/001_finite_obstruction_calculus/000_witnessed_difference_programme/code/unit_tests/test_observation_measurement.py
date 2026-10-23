from dataclasses import replace
from fractions import Fraction

import pytest
from witnessed_difference.measurement import (
    Calibration,
    CalibrationLink,
    IndicationValueMap,
    MeasurandSpecification,
    Measurement,
    MetrologicalTraceability,
    NumericScale,
    Provenance,
    ReportedValue,
    measure,
)
from witnessed_difference.observation import (
    AcceptedObservation,
    EvaluatorResult,
    EvaluatorStanding,
    EvaluatorStatus,
    Interaction,
    ObservationReceipt,
    classify_observation,
)
from witnessed_difference.outcomes import (
    Accepted,
    AuthorityEffect,
    RefusalCode,
    Refused,
)
from witnessed_difference.witness import Registration, make_witness


def accepted_observation() -> AcceptedObservation:
    registration = Registration("sensor-log", "12", 0)
    witness = make_witness(registration, "12", "E-lab")
    assert isinstance(witness, Accepted)
    result = classify_observation(
        ObservationReceipt(
            Interaction(("sensor-log", "sample"), "sensor-log"),
            registration,
            witness.value,
            EvaluatorResult(
                "E-lab", EvaluatorStatus.ACCEPT, EvaluatorStanding.ACCEPTING
            ),
        )
    )
    assert isinstance(result, Accepted)
    return result.value


def valid_measurement_inputs() -> tuple[object, ...]:
    return (
        accepted_observation(),
        MeasurandSpecification(
            "thermodynamic temperature", "sample-7", ("ambient pressure",)
        ),
        ReportedValue("display-channel-1", 12),
        NumericScale("temperature", "degC", Fraction(0), Fraction(100), Fraction(1, 2)),
        Calibration("cal-1", "temperature", "E-lab", Fraction(1, 2)),
        Fraction(1, 4),
        Provenance(("registration:sensor-log:0", "witness:E-lab", "reaccess:matched")),
        MetrologicalTraceability(
            (
                CalibrationLink("cal-1", "lab-primary", "ice-point", Fraction(1, 10)),
                CalibrationLink(
                    "lab-primary", "SI-K", "national-standard", Fraction(1, 20)
                ),
            ),
            "SI-K",
            "external_standard",
            "additive_upper_bound",
        ),
        IndicationValueMap(
            "sensor-to-display",
            "sensor-log",
            "display-channel-1",
        ),
    )


def traceability(
    chain: tuple[CalibrationLink, ...],
    terminal: str,
    kind: str = "external_standard",
    combination: str = "additive_upper_bound",
) -> MetrologicalTraceability:
    return MetrologicalTraceability(chain, terminal, kind, combination)


def test_interaction_requires_two_named_poles() -> None:
    with pytest.raises(ValueError, match="two .*named"):
        Interaction(("one",), "one")
    with pytest.raises(ValueError, match="two .*named"):
        Interaction(("one", ""), "one")
    with pytest.raises(ValueError, match="registration carrier"):
        Interaction(("one", "two"), "elsewhere")
    with pytest.raises(ValueError, match="distinct named poles"):
        Interaction(("one", "one"), "one")
    with pytest.raises(ValueError, match="boolean"):
        Interaction(("one", "two"), "one", 1)


def test_observation_record_types_and_authority_are_enforced() -> None:
    # Invariant: only typed evaluator decisions with zero authority enter the ladder.
    with pytest.raises(ValueError, match="evaluator_id"):
        EvaluatorResult("", EvaluatorStatus.ACCEPT, EvaluatorStanding.ACCEPTING)
    with pytest.raises(ValueError, match="EvaluatorStatus"):
        EvaluatorResult("E", "Accept", EvaluatorStanding.ACCEPTING)
    with pytest.raises(ValueError, match="EvaluatorStanding"):
        EvaluatorResult("E", EvaluatorStatus.ACCEPT, "accepting")
    with pytest.raises(ValueError, match="authority effect"):
        ObservationReceipt(None, None, None, None, authority_effect="promoted")

    accepted = accepted_observation()
    with pytest.raises(ValueError, match="authority effect"):
        AcceptedObservation(accepted.receipt, authority_effect="promoted")

    wrong_type = classify_observation(object())
    assert isinstance(wrong_type, Refused)
    assert wrong_type.code is RefusalCode.INVALID_INPUT


def test_observation_ladder_refuses_each_missing_or_weakened_step() -> None:
    registration = Registration("log", "m", 0)
    witness = make_witness(registration, "m", "E")
    assert isinstance(witness, Accepted)
    decision = EvaluatorResult("E", EvaluatorStatus.ACCEPT, EvaluatorStanding.ACCEPTING)
    interaction = Interaction(("log", "other"), "log")
    cases = [
        (None, registration, witness.value, decision, RefusalCode.NO_INTERACTION),
        (
            Interaction(("log", "other"), "log", False),
            registration,
            witness.value,
            decision,
            RefusalCode.NO_INTERACTION,
        ),
        (interaction, None, witness.value, decision, RefusalCode.NO_REGISTRATION),
        (
            interaction,
            replace(registration, retained=False),
            witness.value,
            decision,
            RefusalCode.NO_REGISTRATION,
        ),
        (
            Interaction(("alien", "other"), "alien"),
            registration,
            witness.value,
            decision,
            RefusalCode.COUPLING_MISMATCH,
        ),
        (interaction, registration, None, decision, RefusalCode.NO_WITNESS),
        (
            interaction,
            registration,
            witness.value,
            None,
            RefusalCode.NO_ACCEPTING_EVALUATOR,
        ),
        (
            interaction,
            registration,
            witness.value,
            replace(decision, status=EvaluatorStatus.REJECT),
            RefusalCode.NO_ACCEPTING_EVALUATOR,
        ),
        (
            interaction,
            registration,
            witness.value,
            replace(decision, status=EvaluatorStatus.REFUSE),
            RefusalCode.NO_ACCEPTING_EVALUATOR,
        ),
        (
            interaction,
            registration,
            witness.value,
            replace(decision, status=EvaluatorStatus.UNDETERMINED),
            RefusalCode.NO_ACCEPTING_EVALUATOR,
        ),
        (
            interaction,
            registration,
            witness.value,
            replace(decision, standing=EvaluatorStanding.NON_ACCEPTING),
            RefusalCode.NON_ACCEPTING_STANDING,
        ),
        (
            interaction,
            registration,
            witness.value,
            replace(decision, evaluator_id="other"),
            RefusalCode.EVALUATOR_MISMATCH,
        ),
    ]
    for interaction, registered, witnessed, evaluated, code in cases:
        receipt = ObservationReceipt(interaction, registered, witnessed, evaluated)
        assert receipt.authority_effect is AuthorityEffect.NONE
        result = classify_observation(receipt)
        assert isinstance(result, Refused) and result.code is code


def test_observation_rejects_witness_for_another_registration() -> None:
    registration = Registration("log", "m", 0)
    other = Registration("log", "m", 1)
    witness = make_witness(other, "m", "E")
    assert isinstance(witness, Accepted)
    result = classify_observation(
        ObservationReceipt(
            Interaction(("log", "other"), "log"),
            registration,
            witness.value,
            EvaluatorResult("E", EvaluatorStatus.ACCEPT, EvaluatorStanding.ACCEPTING),
        )
    )
    assert isinstance(result, Refused) and result.code is RefusalCode.DIGEST_MISMATCH


def test_accepted_observation_cannot_wrap_a_rejected_or_tampered_attempt() -> None:
    accepted = accepted_observation()
    rejected = replace(
        accepted.receipt,
        evaluator_result=replace(
            accepted.evaluator_result, status=EvaluatorStatus.REJECT
        ),
    )
    with pytest.raises(ValueError, match="no_accepting_evaluator"):
        AcceptedObservation(rejected)
    tampered_witness = replace(accepted.witness, receipt_digest="0" * 64)
    result = classify_observation(replace(accepted.receipt, witness=tampered_witness))
    assert isinstance(result, Refused) and result.code is RefusalCode.RECEIPT_MISMATCH


def test_observation_authority_tamper_cannot_be_laundered() -> None:
    accepted = accepted_observation()
    forged_receipt = replace(accepted.receipt)
    object.__setattr__(forged_receipt, "authority_effect", "promoted")
    classified = classify_observation(forged_receipt)
    assert isinstance(classified, Refused)
    assert classified.code is RefusalCode.CLAIM_STATUS_FIREWALL
    with pytest.raises(ValueError, match="claim_status_firewall"):
        AcceptedObservation(forged_receipt)
    with pytest.raises(ValueError, match="claim_status_firewall"):
        replace(accepted, receipt=forged_receipt)

    nested = accepted_observation()
    object.__setattr__(nested.receipt, "authority_effect", "promoted")
    measurement_inputs = list(valid_measurement_inputs())
    measurement_inputs[0] = nested
    measured = measure(*measurement_inputs)
    assert isinstance(measured, Refused)
    assert measured.code is RefusalCode.CLAIM_STATUS_FIREWALL


def test_accepted_observation_has_no_authority_promotion() -> None:
    observation = accepted_observation()
    assert observation.interaction.poles == ("sensor-log", "sample")
    assert (
        observation.interaction.registration_carrier_id
        == observation.registration.carrier_id
    )
    assert observation.registration.carrier_id == "sensor-log"
    assert observation.witness.reaccess.matches
    assert observation.evaluator_result.status is EvaluatorStatus.ACCEPT
    assert observation.authority_effect is AuthorityEffect.NONE
    assert not hasattr(observation, "authority_certificate")
    assert not hasattr(observation, "promote")


def test_measurement_separates_measurand_result_provenance_and_traceability() -> None:
    result = measure(*valid_measurement_inputs())
    assert isinstance(result, Accepted)
    assert isinstance(result.value, Measurement)
    assert result.value.measurand.quantity == "thermodynamic temperature"
    assert result.value.reported.carrier_id == "display-channel-1"
    assert result.value.value_map.map_id == "sensor-to-display"
    assert result.value.corrected_value == Fraction(25, 2)
    assert result.value.stated_uncertainty == Fraction(1, 4)
    assert result.value.combined_uncertainty == Fraction(2, 5)
    assert isinstance(result.value.provenance, Provenance)
    assert isinstance(result.value.metrological_traceability, MetrologicalTraceability)
    assert result.value.authority_effect is AuthorityEffect.NONE
    with pytest.raises(ValueError, match="accepted E-observation"):
        replace(result.value, observation=result.value.observation.receipt)
    with pytest.raises(ValueError, match="authority effect"):
        replace(result.value, authority_effect="promoted")


def test_measurement_refusal_surface() -> None:
    base = list(valid_measurement_inputs())
    cases: list[tuple[int, object, RefusalCode]] = [
        (0, None, RefusalCode.MISSING_OBSERVATION),
        (0, accepted_observation().receipt, RefusalCode.MISSING_OBSERVATION),
        (1, None, RefusalCode.MISSING_MEASURAND),
        (1, MeasurandSpecification("", "sample", ()), RefusalCode.MISSING_MEASURAND),
        (
            1,
            MeasurandSpecification("temperature", "", ()),
            RefusalCode.MISSING_MEASURAND,
        ),
        (2, None, RefusalCode.MISSING_REPORTED_VALUE),
        (2, ReportedValue("", 12), RefusalCode.MISSING_REPORTED_VALUE),
        (2, ReportedValue("display", None), RefusalCode.MISSING_REPORTED_VALUE),
        (3, None, RefusalCode.MISSING_SCALE),
        (3, replace(base[3], scale_id=""), RefusalCode.MISSING_SCALE),
        (3, replace(base[3], unit=""), RefusalCode.MISSING_UNIT),
        (3, replace(base[3], lower=2, upper=1), RefusalCode.INVALID_INPUT),
        (3, replace(base[3], resolution=0), RefusalCode.INVALID_INPUT),
        (3, replace(base[3], lower=object()), RefusalCode.INVALID_INPUT),
        (4, None, RefusalCode.MISSING_CALIBRATION),
        (4, replace(base[4], calibration_id=""), RefusalCode.MISSING_CALIBRATION),
        (4, replace(base[4], scale_id="other"), RefusalCode.ADAPTER_MISMATCH),
        (4, replace(base[4], evaluator_id="other"), RefusalCode.EVALUATOR_MISMATCH),
        (6, None, RefusalCode.MISSING_PROVENANCE),
        (6, Provenance(()), RefusalCode.MISSING_PROVENANCE),
        (6, Provenance(("",)), RefusalCode.MISSING_PROVENANCE),
        (7, None, RefusalCode.MISSING_TRACEABILITY),
        (7, traceability((), "SI-K"), RefusalCode.MISSING_TRACEABILITY),
        (7, base[6], RefusalCode.TRACEABILITY_TYPE_CONFUSION),
        (7, traceability((object(),), "SI-K"), RefusalCode.BROKEN_TRACEABILITY),
        (
            7,
            traceability((CalibrationLink("wrong", "lab", "ref", 0),), "lab"),
            RefusalCode.BROKEN_TRACEABILITY,
        ),
        (
            7,
            traceability((CalibrationLink("", "lab", "ref", 0),), "lab"),
            RefusalCode.BROKEN_TRACEABILITY,
        ),
        (
            7,
            traceability((CalibrationLink("cal-1", "", "ref", 0),), "lab"),
            RefusalCode.BROKEN_TRACEABILITY,
        ),
        (
            7,
            traceability((CalibrationLink("cal-1", "lab", "", 0),), "lab"),
            RefusalCode.BROKEN_TRACEABILITY,
        ),
        (
            7,
            traceability((CalibrationLink("cal-1", "lab", "ref", None),), "lab"),
            RefusalCode.MISSING_CHAIN_UNCERTAINTY,
        ),
        (
            7,
            traceability(
                (CalibrationLink("cal-1", "lab", "ref", "not-a-rational"),), "lab"
            ),
            RefusalCode.INVALID_UNCERTAINTY,
        ),
        (
            7,
            traceability((CalibrationLink("cal-1", "lab", "ref", -1),), "lab"),
            RefusalCode.MISSING_CHAIN_UNCERTAINTY,
        ),
        (
            7,
            traceability((CalibrationLink("cal-1", "cal-1", "self", 0),), "cal-1"),
            RefusalCode.BROKEN_TRACEABILITY,
        ),
        (
            7,
            traceability(
                (
                    CalibrationLink("cal-1", "lab", "forward", 0),
                    CalibrationLink("lab", "cal-1", "back", 0),
                ),
                "cal-1",
            ),
            RefusalCode.BROKEN_TRACEABILITY,
        ),
        (
            7,
            traceability((CalibrationLink("cal-1", "lab", "ref", 0),), "SI-K"),
            RefusalCode.BROKEN_TRACEABILITY,
        ),
        (
            7,
            traceability((CalibrationLink("cal-1", "lab", "ref", 0),), ""),
            RefusalCode.BROKEN_TRACEABILITY,
        ),
        (
            7,
            traceability((CalibrationLink("cal-1", "lab", "ref", 0),), "lab", ""),
            RefusalCode.BROKEN_TRACEABILITY,
        ),
        (
            7,
            traceability(
                (CalibrationLink("cal-1", "lab", "ref", 0),),
                "lab",
                combination="root_sum_square",
            ),
            RefusalCode.INVALID_UNCERTAINTY,
        ),
        (8, None, RefusalCode.MISSING_VALUE_MAP),
        (
            8,
            IndicationValueMap("", "sensor-log", "display-channel-1"),
            RefusalCode.MISSING_VALUE_MAP,
        ),
        (
            8,
            IndicationValueMap("map", "other-sensor", "display-channel-1"),
            RefusalCode.VALUE_MAP_MISMATCH,
        ),
        (
            8,
            IndicationValueMap("map", "sensor-log", "other-display"),
            RefusalCode.VALUE_MAP_MISMATCH,
        ),
        (
            8,
            IndicationValueMap(
                "map", "sensor-log", "display-channel-1", source_key="value"
            ),
            RefusalCode.VALUE_MAP_MISMATCH,
        ),
        (
            8,
            IndicationValueMap(
                "map", "sensor-log", "display-channel-1", gain=2
            ),
            RefusalCode.VALUE_MAP_MISMATCH,
        ),
        (5, -1, RefusalCode.INVALID_UNCERTAINTY),
        (3, replace(base[3], upper=12), RefusalCode.OUT_OF_RANGE),
        (
            4,
            replace(base[4], correction=Fraction(1, 3)),
            RefusalCode.OFF_GRID,
        ),
    ]
    for index, mutation, code in cases:
        arguments = list(base)
        arguments[index] = mutation
        result = measure(*arguments)
        assert isinstance(result, Refused) and result.code is code


def test_measurement_refuses_malformed_exact_values() -> None:
    for malformed in (12.0, "not-a-rational"):
        arguments = list(valid_measurement_inputs())
        arguments[2] = ReportedValue("display-channel-1", malformed)
        result = measure(*arguments)
        assert isinstance(result, Refused)
        assert result.code is RefusalCode.INVALID_INPUT
    arguments = list(valid_measurement_inputs())
    arguments[5] = "not-an-uncertainty"
    result = measure(*arguments)
    assert isinstance(result, Refused)
    assert result.code is RefusalCode.INVALID_UNCERTAINTY
    arguments = list(valid_measurement_inputs())
    arguments[8] = IndicationValueMap(
        "map", "sensor-log", "display-channel-1", gain=object()
    )
    result = measure(*arguments)
    assert isinstance(result, Refused)
    assert result.code is RefusalCode.INVALID_INPUT
    arguments = list(valid_measurement_inputs())
    arguments[4] = replace(arguments[4], correction=object())
    result = measure(*arguments)
    assert isinstance(result, Refused)
    assert result.code is RefusalCode.INVALID_INPUT
