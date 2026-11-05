from dataclasses import replace
from fractions import Fraction

import pytest
from witnessed_difference.calibration_composition import AffineCalibrationStage, BoundedReading
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
from witnessed_difference.outcomes import Accepted, RefusalCode, Refused
from witnessed_difference.quantum_measurement_replay import (
    FiniteInstrumentModel,
    FinitePositiveMixture,
    GaussianRational,
    QuantumMeasurementProblem,
    exact_matrix,
    is_outcome_repeatable,
    outcome_record,
    replay_quantum_measurement,
    verify_quantum_measurement,
)
from witnessed_difference.receipts import make_receipt, verify_receipt
from witnessed_difference.witness import Registration, make_witness


def unit(row: int, col: int, coefficient: GaussianRational | int = 1):
    return exact_matrix(tuple(tuple(coefficient if (r, c) == (row, col) else 0
                                    for c in range(3)) for r in range(3)))


def instrument() -> FiniteInstrumentModel:
    half_phase = GaussianRational(Fraction(1, 2), Fraction(1, 2))
    return FiniteInstrumentModel(3, (
        (unit(0, 0), unit(0, 2, half_phase)),
        (unit(1, 1), unit(1, 2, half_phase)),
    ))


def pure(i: int) -> FinitePositiveMixture:
    vector = tuple(GaussianRational(int(j == i)) for j in range(3))
    return FinitePositiveMixture(((Fraction(1), vector),))


def packet(mark_override=None):
    model = instrument()
    state = pure(2)
    record = outcome_record(model, state, 0)
    mark = {"instrument_record": record, "indication": Fraction(4)}
    if mark_override is not None:
        mark = mark_override
    registration = Registration("detector", mark, 0)
    witness = make_witness(registration, dict(mark), "E")
    assert isinstance(witness, Accepted)
    observation = classify_observation(ObservationReceipt(
        Interaction(("qutrit", "detector"), "detector"), registration, witness.value,
        EvaluatorResult("E", EvaluatorStatus.ACCEPT, EvaluatorStanding.ACCEPTING),
    ))
    assert isinstance(observation, Accepted)
    stages = (
        AffineCalibrationStage("first", 2, 1, Fraction(1, 100), Fraction(1, 20), Fraction(1, 25)),
        AffineCalibrationStage("second", -1, 3, offset_error=Fraction(1, 50)),
    )
    measurement = measure(
        observation.value, MeasurandSpecification("voltage", "declared finite apparatus", ("finite bounds",)),
        ReportedValue("result", -6),
        NumericScale("scale", "V", Fraction(-20), Fraction(20), Fraction(1, 100)),
        Calibration("calibration", "scale", "E", Fraction(1, 2)), Fraction(1, 2),
        Provenance(("retained", "independently reaccessed")),
        MetrologicalTraceability((
            CalibrationLink("calibration", "transfer", "document-a", Fraction(1, 10)),
            CalibrationLink("transfer", "reference", "document-b", Fraction(1, 5)),
        ), "reference", "declared_documentary_reference", "additive_upper_bound"),
        IndicationValueMap("ordered-map", "detector", "result", "indication", -2, 2),
    )
    assert isinstance(measurement, Accepted)
    return QuantumMeasurementProblem(model, state, 0, (Fraction(4), Fraction(-3)),
                                     measurement.value, stages, Fraction(1, 10)), mark


def test_repeatability_mirror_includes_grouped_nonprojective_and_switching_instances():
    model = instrument()
    assert is_outcome_repeatable(model)
    record = outcome_record(model, pure(2), 0)
    assert record.probability == Fraction(1, 2)
    assert record.post_state == unit(0, 0)
    replacement = FiniteInstrumentModel(3, tuple((unit(0, i),) for i in range(3)))
    assert not is_outcome_repeatable(replacement)
    # Same projective POVM does not imply the same repeatability property.
    projective = FiniteInstrumentModel(3, tuple((unit(i, i),) for i in range(3)))
    assert is_outcome_repeatable(projective)
    for i in range(3):
        assert outcome_record(projective, pure(i), i).probability == 1
        assert outcome_record(replacement, pure(i), i).probability == 1
    assert outcome_record(replacement, pure(1), 1).post_state == unit(0, 0)


def test_full_existing_measurement_ladder_replays_the_actual_instrument_record():
    actual, mark = packet()
    replay = replay_quantum_measurement(actual, dict(mark))
    assert isinstance(replay, Accepted)
    assert replay.value.instrument_record.probability == Fraction(1, 2)
    assert replay.value.measurement_replay.corrected_enclosure == BoundedReading(Fraction(-11, 2), Fraction(651, 1000))
    assert actual.measurement.combined_uncertainty == Fraction(4, 5)
    assert verify_quantum_measurement(replay.value, actual, mark) == Accepted(True)


def test_freshly_rehashed_false_record_and_matching_false_registration_are_rejected():
    actual, mark = packet()
    replay = replay_quantum_measurement(actual, mark)
    assert isinstance(replay, Accepted)
    false_record = replace(replay.value.instrument_record, probability=Fraction(1))
    fresh = make_receipt("complete-declared-quantum-measurement", actual,
                         (false_record, replay.value.measurement_replay),
                         ("WDP-CH19-O04", "WDP-CH13-O01", "WDP-CH13-O02"))
    assert isinstance(fresh, Accepted)
    forged = replace(replay.value, instrument_record=false_record, receipt=fresh.value)
    assert verify_receipt(forged.receipt, actual, (forged.instrument_record, forged.measurement_replay)) == Accepted(True)
    checked = verify_quantum_measurement(forged, actual, mark)
    assert isinstance(checked, Refused) and checked.code is RefusalCode.CERTIFICATE_MISMATCH
    forged_problem, forged_mark = packet({"instrument_record": false_record, "indication": Fraction(4)})
    # Its retained mark and witness match, and the existing Measurement is valid;
    # the new actual-instrument binding independently detects the false probability.
    checked = replay_quantum_measurement(forged_problem, forged_mark)
    assert isinstance(checked, Refused) and checked.code is RefusalCode.CERTIFICATE_MISMATCH


def test_rehashed_false_inner_and_outer_enclosures_cannot_pass_full_replay():
    actual, mark = packet()
    replay = replay_quantum_measurement(actual, mark)
    assert isinstance(replay, Accepted)
    inner = replay.value.measurement_replay
    false_enclosure = BoundedReading(Fraction(-11, 2), 0)
    inner_hash = make_receipt("composed-finite-measurement",
                              (actual.measurement, actual.stages, actual.input_radius),
                              (inner.states, false_enclosure), ("WDP-CH13-O01", "WDP-CH13-O02"))
    assert isinstance(inner_hash, Accepted)
    false_inner = replace(inner, corrected_enclosure=false_enclosure, receipt=inner_hash.value)
    outer_hash = make_receipt("complete-declared-quantum-measurement", actual,
                              (replay.value.instrument_record, false_inner),
                              ("WDP-CH19-O04", "WDP-CH13-O01", "WDP-CH13-O02"))
    assert isinstance(outer_hash, Accepted)
    forged = replace(replay.value, measurement_replay=false_inner, receipt=outer_hash.value)
    checked = verify_quantum_measurement(forged, actual, mark)
    assert isinstance(checked, Refused) and checked.code is RefusalCode.CERTIFICATE_MISMATCH


def test_actual_input_reaccess_and_documentary_hierarchy_are_independent_requirements():
    actual, mark = packet()
    replay = replay_quantum_measurement(actual, mark)
    assert isinstance(replay, Accepted)
    assert isinstance(verify_quantum_measurement(replay.value, replace(actual, state=pure(0)), mark), Refused)
    assert isinstance(replay_quantum_measurement(actual, {"indication": 4}), Refused)
    broken = replace(actual.measurement.metrological_traceability,
                     chain=(CalibrationLink("elsewhere", "reference", "document", Fraction(0)),))
    checked = replay_quantum_measurement(replace(actual, measurement=replace(actual.measurement, metrological_traceability=broken)), mark)
    assert isinstance(checked, Refused) and checked.code is RefusalCode.BROKEN_TRACEABILITY
    with pytest.raises(ValueError):
        FiniteInstrumentModel(3, ((unit(0, 0),),))
    with pytest.raises((TypeError, ValueError)):
        GaussianRational(0.5)
