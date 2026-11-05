from fractions import Fraction

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
    ObserverBridge,
    OperationalObserverPacket,
    adapt_operational,
    validate_report_profile_separation,
)
from witnessed_difference.outcomes import Accepted, AuthorityEffect
from witnessed_difference.receipts import make_receipt, verify_receipt
from witnessed_difference.witness import Registration, make_witness, verify_witness


def test_registration_to_measurement_preserves_evaluator_and_authority_firewall() -> None:
    packet = OperationalObserverPacket(
        ("idle", "marked"),
        "idle",
        ("record",),
        (("idle", "record", "marked"),),
        (("idle", "none"), ("marked", "value=12")),
        (("idle", "p0"), ("marked", "p1")),
    )
    assert isinstance(validate_report_profile_separation(packet), Accepted)
    bridge = ObserverBridge("operational", "finite state", "delta", "repair", None, "identity", "report", "accept")
    observer = adapt_operational(packet, bridge)
    assert isinstance(observer, Accepted)

    registration = Registration("sensor-7", {"value": 12, "unit": "degC"}, 0)
    witness = make_witness(registration, {"unit": "degC", "value": 12}, "E-lab")
    assert isinstance(witness, Accepted)
    assert isinstance(verify_witness(witness.value, {"value": 12, "unit": "degC"}), Accepted)

    observation = classify_observation(
        ObservationReceipt(
            Interaction(("sensor-7", "sample"), "sensor-7"),
            registration,
            witness.value,
            EvaluatorResult("E-lab", EvaluatorStatus.ACCEPT, EvaluatorStanding.ACCEPTING),
        )
    )
    assert isinstance(observation, Accepted)
    measured = measure(
        observation.value,
        MeasurandSpecification("thermodynamic temperature", "sample", ("ambient pressure",)),
        ReportedValue("display", 12),
        NumericScale("temp", "degC", Fraction(-40), Fraction(100), Fraction(1, 2)),
        Calibration("cal-ice", "temp", "E-lab", Fraction(0)),
        Fraction(1, 4),
        Provenance(("sensor-7", "witness:E-lab", "reaccess:matched")),
        MetrologicalTraceability(
            (CalibrationLink("cal-ice", "SI-temperature", "ice point", Fraction(1, 10)),),
            "SI-temperature",
            "external_standard",
            "additive_upper_bound",
        ),
        IndicationValueMap("sensor-to-display", "sensor-7", "display", "value"),
    )
    assert isinstance(measured, Accepted)
    assert measured.value.authority_effect is AuthorityEffect.NONE

    receipt = make_receipt(
        "measurement-pipeline",
        registration,
        measured.value,
        ("WDP-CH12-D01", "WDP-CH13-D01"),
    )
    assert isinstance(receipt, Accepted)
    assert isinstance(verify_receipt(receipt.value, registration, measured.value), Accepted)
# Executable finite evidence; AuthorityEffect: None.
