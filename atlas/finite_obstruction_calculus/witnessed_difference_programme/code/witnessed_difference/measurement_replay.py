"""Replay composed affine uncertainty through the existing WDP measurement API.

Acceptance verifies a finite conditional model and the supplied artifact bytes.
A documented hierarchy remains caller data, never proof of physical traceability.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from .calibration_composition import (
    AffineCalibrationStage,
    BoundedReading,
    compose_nominal,
    propagate_chain,
)
from .exact import as_fraction
from .measurement import Measurement, measure
from .outcomes import Accepted, Outcome, RefusalCode, Refused
from .receipts import Receipt, make_receipt, verify_receipt
from .witness import verify_witness


@dataclass(frozen=True)
class MeasurementReplay:
    states: tuple[BoundedReading, ...]
    corrected_enclosure: BoundedReading
    receipt: Receipt


def replay_composed_measurement(
    measurement: Measurement,
    stages: tuple[AffineCalibrationStage, ...],
    input_radius: int | str | Fraction,
    reaccessed_mark: object,
) -> Outcome[MeasurementReplay]:
    """Revalidate packet, replay indication, and bind uncertainty to every stage.

    Recompute the original measure() rather than trusting a constructed
    Measurement. The composed nominal map must match the declared packet map.
    The stage enclosure must fit inside stated uncertainty. The exact correction
    translates its center and the hierarchy's additive bounds enlarge its radius.
    No stage-error bound is inferred from the documentary hierarchy.
    """
    if not isinstance(measurement, Measurement):
        return Refused(RefusalCode.INVALID_INPUT, "measurement has the wrong type")
    witness_check = verify_witness(measurement.observation.witness, reaccessed_mark)
    if isinstance(witness_check, Refused):
        return witness_check
    checked = measure(
        measurement.observation,
        measurement.measurand,
        measurement.reported,
        measurement.scale,
        measurement.calibration,
        measurement.stated_uncertainty,
        measurement.provenance,
        measurement.metrological_traceability,
        measurement.value_map,
    )
    if isinstance(checked, Refused):
        return checked
    if checked.value != measurement:
        return Refused(RefusalCode.CERTIFICATE_MISMATCH, "measurement fields differ from their checked replay")
    indication = measurement.observation.registration.mark
    if measurement.value_map.source_key is not None:
        indication = indication[measurement.value_map.source_key]
    try:
        radius = as_fraction(input_radius)
        states = propagate_chain(BoundedReading(as_fraction(indication), radius), stages)
        gain, offset = compose_nominal(stages)
    except (TypeError, ValueError, ZeroDivisionError, OverflowError):
        return Refused(RefusalCode.INVALID_INPUT, "composed calibration needs exact declared stage bounds")
    if gain != as_fraction(measurement.value_map.gain) or offset != as_fraction(measurement.value_map.offset):
        return Refused(RefusalCode.VALUE_MAP_MISMATCH, "stage composition does not equal the packet value map")
    if states[-1].center != measurement.raw_value:
        return Refused(RefusalCode.VALUE_MAP_MISMATCH, "stage replay does not produce the packet raw value")
    if states[-1].radius > measurement.stated_uncertainty:
        return Refused(RefusalCode.INVALID_UNCERTAINTY, "stated uncertainty understates propagated stage errors")
    hierarchy_bound = measurement.combined_uncertainty - measurement.stated_uncertainty
    corrected = BoundedReading(measurement.corrected_value, states[-1].radius + hierarchy_bound)
    inputs = (measurement, stages, radius)
    outputs = (states, corrected)
    receipt = make_receipt(
        "composed-finite-measurement",
        inputs,
        outputs,
        ("WDP-CH13-O01", "WDP-CH13-O02"),
    )
    if isinstance(receipt, Refused):
        return receipt
    return Accepted(MeasurementReplay(states, corrected, receipt.value))


def verify_measurement_replay(
    candidate: MeasurementReplay,
    measurement: Measurement,
    stages: tuple[AffineCalibrationStage, ...],
    input_radius: int | str | Fraction,
    reaccessed_mark: object,
) -> Outcome[bool]:
    """Bind candidate to independently supplied packet/model and recompute all data.

    Hash consistency alone is insufficient: a freshly rehashed false enclosure
    still fails comparison with the recomputed sequential enclosure.
    """
    if not isinstance(candidate, MeasurementReplay):
        return Refused(RefusalCode.INVALID_INPUT, "measurement replay has the wrong type")
    replayed = replay_composed_measurement(measurement, stages, input_radius, reaccessed_mark)
    if isinstance(replayed, Refused):
        return replayed
    receipt_check = verify_receipt(
        candidate.receipt,
        (measurement, stages, as_fraction(input_radius)),
        (candidate.states, candidate.corrected_enclosure),
    )
    if isinstance(receipt_check, Refused):
        return receipt_check
    if candidate != replayed.value:
        return Refused(RefusalCode.CERTIFICATE_MISMATCH, "candidate differs from recomputed measurement replay")
    return Accepted(True)
