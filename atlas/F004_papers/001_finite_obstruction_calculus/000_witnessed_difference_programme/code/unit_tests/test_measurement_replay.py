from dataclasses import replace
from fractions import Fraction

from witnessed_difference.calibration_composition import AffineCalibrationStage, BoundedReading
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
from witnessed_difference.measurement_replay import (
    replay_composed_measurement,
    verify_measurement_replay,
)
from witnessed_difference.observation import (
    EvaluatorResult,
    EvaluatorStanding,
    EvaluatorStatus,
    Interaction,
    ObservationReceipt,
    classify_observation,
)
from witnessed_difference.outcomes import Accepted, AuthorityEffect, RefusalCode, Refused
from witnessed_difference.receipts import make_receipt
from witnessed_difference.witness import Registration, make_witness


def finite_instance() -> tuple[Measurement, tuple[AffineCalibrationStage, ...], dict[str, int]]:
    mark = {"indication": 2}
    registration = Registration("sensor", mark, 0)
    witness = make_witness(registration, dict(mark), "E")
    assert isinstance(witness, Accepted)
    observation = classify_observation(ObservationReceipt(
        Interaction(("sensor", "sample"), "sensor"),
        registration,
        witness.value,
        EvaluatorResult("E", EvaluatorStatus.ACCEPT, EvaluatorStanding.ACCEPTING),
    ))
    assert isinstance(observation, Accepted)
    stages = (
        AffineCalibrationStage("amplify", 2, 1, Fraction(1, 10), Fraction(1, 20)),
        AffineCalibrationStage("invert", -3, 2, residual_error=Fraction(1, 50)),
    )
    measured = measure(
        observation.value,
        MeasurandSpecification("declared quantity", "sample", ("finite trial",)),
        ReportedValue("display", -13),
        NumericScale("scale", "declared-unit", Fraction(-100), Fraction(100), Fraction(1)),
        Calibration("cal", "scale", "E", Fraction(1)),
        Fraction(7, 5),
        Provenance(("registered", "reaccess matched")),
        MetrologicalTraceability(
            (CalibrationLink("cal", "reference", "declared fixture", Fraction(1, 10)),),
            "reference", "declared_reference", "additive_upper_bound",
        ),
        IndicationValueMap("composed", "sensor", "display", "indication", -6, -1),
    )
    assert isinstance(measured, Accepted)
    return measured.value, stages, mark


def test_end_to_end_registered_observation_measurement_and_bound_replay() -> None:
    measurement, stages, mark = finite_instance()
    replay = replay_composed_measurement(measurement, stages, Fraction(1, 10), dict(mark))
    assert isinstance(replay, Accepted)
    assert tuple(state.center for state in replay.value.states) == (2, 5, -13)
    assert tuple(state.radius for state in replay.value.states) == (Fraction(1, 10), Fraction(23, 50), Fraction(7, 5))
    assert replay.value.corrected_enclosure == BoundedReading(-12, Fraction(3, 2))
    assert measurement.combined_uncertainty == Fraction(3, 2)
    checked = verify_measurement_replay(replay.value, measurement, stages, Fraction(1, 10), mark)
    assert isinstance(checked, Accepted) and checked.value is True
    assert checked.authority_effect is AuthorityEffect.NONE


def test_reaccess_and_fabricated_measurement_fields_fail() -> None:
    measurement, stages, mark = finite_instance()
    for altered_mark in ({"indication": 3}, {"other": 2}):
        assert isinstance(replay_composed_measurement(measurement, stages, Fraction(1, 10), altered_mark), Refused)
    for changed in (
        replace(measurement, raw_value=Fraction(-12)),
        replace(measurement, corrected_value=Fraction(0)),
        replace(measurement, combined_uncertainty=Fraction(0)),
    ):
        result = replay_composed_measurement(changed, stages, Fraction(1, 10), mark)
        assert isinstance(result, Refused) and result.code is RefusalCode.CERTIFICATE_MISMATCH
    too_small = replace(measurement, stated_uncertainty=Fraction(1), combined_uncertainty=Fraction(11, 10))
    result = replay_composed_measurement(too_small, stages, Fraction(1, 10), mark)
    assert isinstance(result, Refused) and result.code is RefusalCode.INVALID_UNCERTAINTY


def test_wrong_map_model_and_nonexact_radius_fail() -> None:
    measurement, stages, mark = finite_instance()
    wrong_map = (replace(stages[0], gain=Fraction(3)), stages[1])
    result = replay_composed_measurement(measurement, wrong_map, Fraction(1, 10), mark)
    assert isinstance(result, Refused) and result.code is RefusalCode.VALUE_MAP_MISMATCH
    for radius in (-1, True, 0.1):
        assert isinstance(replay_composed_measurement(measurement, stages, radius, mark), Refused)
    assert isinstance(replay_composed_measurement(measurement, (object(),), 0, mark), Refused)
    assert isinstance(replay_composed_measurement(object(), stages, 0, mark), Refused)


def test_tamper_rehashed_false_enclosure_and_replayed_model_update_fail() -> None:
    measurement, stages, mark = finite_instance()
    radius = Fraction(1, 10)
    replay = replay_composed_measurement(measurement, stages, radius, mark)
    assert isinstance(replay, Accepted)
    false_enclosure = BoundedReading(-12, 0)
    forged_receipt = make_receipt(
        "composed-finite-measurement",
        (measurement, stages, radius),
        (replay.value.states, false_enclosure),
        ("WDP-CH13-O01", "WDP-CH13-O02"),
    )
    assert isinstance(forged_receipt, Accepted)
    forged = replace(replay.value, corrected_enclosure=false_enclosure, receipt=forged_receipt.value)
    result = verify_measurement_replay(forged, measurement, stages, radius, mark)
    assert isinstance(result, Refused) and result.code is RefusalCode.CERTIFICATE_MISMATCH
    changed = (replace(stages[0], gain_error=Fraction(0)), stages[1])
    updated = replay_composed_measurement(measurement, changed, radius, mark)
    assert isinstance(updated, Accepted)
    assert updated.value.states[-1].radius < replay.value.states[-1].radius
    assert isinstance(verify_measurement_replay(replay.value, measurement, changed, radius, mark), Refused)
    assert isinstance(verify_measurement_replay(object(), measurement, stages, radius, mark), Refused)
