# Executable finite evidence; AuthorityEffect: None.
"""Typed measurement with distinct WDP provenance and metrological traceability."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from .exact import as_fraction
from .observation import AcceptedObservation, classify_observation
from .outcomes import Accepted, AuthorityEffect, Outcome, RefusalCode, Refused


@dataclass(frozen=True)
class MeasurandSpecification:
    """The quantity intended to be measured, not its reported result."""

    quantity: str
    system: str
    conditions: tuple[str, ...]


@dataclass(frozen=True)
class ReportedValue:
    """A typed result carrier, kept distinct from the measurand."""

    carrier_id: str
    value: int | str | Fraction | None


@dataclass(frozen=True)
class IndicationValueMap:
    """Declared exact map from a retained indication to a reported value."""

    map_id: str
    source_carrier_id: str
    target_carrier_id: str
    source_key: str | None = None
    gain: int | str | Fraction = Fraction(1)
    offset: int | str | Fraction = Fraction(0)


@dataclass(frozen=True)
class NumericScale:
    scale_id: str
    unit: str
    lower: Fraction
    upper: Fraction
    resolution: Fraction


@dataclass(frozen=True)
class Calibration:
    calibration_id: str
    scale_id: str
    evaluator_id: str
    correction: Fraction = Fraction(0)


@dataclass(frozen=True)
class Provenance:
    """WDP artifact history and re-access provenance; not VIM traceability."""

    entries: tuple[str, ...]


@dataclass(frozen=True)
class CalibrationLink:
    source_id: str
    target_id: str
    reference: str
    uncertainty: int | str | Fraction | None


@dataclass(frozen=True)
class MetrologicalTraceability:
    """Documented unbroken calibration hierarchy with uncertainty per link.

    This VIM-style field does not contain WDP provenance or observation
    acceptance; those are separate, stronger preconditions of this package.
    """

    chain: tuple[CalibrationLink, ...]
    terminal_reference_id: str
    terminal_reference_kind: str
    uncertainty_combination: str


@dataclass(frozen=True)
class Measurement:
    observation: AcceptedObservation
    measurand: MeasurandSpecification
    reported: ReportedValue
    value_map: IndicationValueMap
    scale: NumericScale
    raw_value: Fraction
    corrected_value: Fraction
    calibration: Calibration
    stated_uncertainty: Fraction
    combined_uncertainty: Fraction
    provenance: Provenance
    metrological_traceability: MetrologicalTraceability
    authority_effect: AuthorityEffect = AuthorityEffect.NONE

    def __post_init__(self) -> None:
        if self.authority_effect is not AuthorityEffect.NONE:
            raise ValueError("measurements cannot carry an authority effect")
        if not isinstance(self.observation, AcceptedObservation):
            raise ValueError("measurement requires an accepted E-observation")


def _validate_traceability(
    calibration: Calibration,
    traceability: MetrologicalTraceability | Provenance | None,
) -> Outcome[tuple[Fraction, ...]]:
    if isinstance(traceability, Provenance):
        return Refused(
            RefusalCode.TRACEABILITY_TYPE_CONFUSION,
            "artifact provenance cannot stand in for a metrological calibration hierarchy",
        )
    if traceability is None or not isinstance(traceability, MetrologicalTraceability) or not traceability.chain:
        return Refused(RefusalCode.MISSING_TRACEABILITY, "a documented calibration hierarchy is required")
    if (
        not isinstance(traceability.terminal_reference_id, str)
        or not traceability.terminal_reference_id
        or not isinstance(traceability.terminal_reference_kind, str)
        or not traceability.terminal_reference_kind
    ):
        return Refused(
            RefusalCode.BROKEN_TRACEABILITY,
            "the calibration hierarchy needs a declared terminal reference identity and kind",
        )
    if traceability.uncertainty_combination != "additive_upper_bound":
        return Refused(
            RefusalCode.INVALID_UNCERTAINTY,
            "the finite implementation supports only a declared additive_upper_bound",
        )
    expected_source = calibration.calibration_id
    visited = {expected_source}
    uncertainties: list[Fraction] = []
    for link in traceability.chain:
        if not isinstance(link, CalibrationLink):
            return Refused(RefusalCode.BROKEN_TRACEABILITY, "calibration hierarchy contains an invalid link")
        if (
            not isinstance(link.source_id, str)
            or not link.source_id
            or not isinstance(link.target_id, str)
            or not link.target_id
            or not isinstance(link.reference, str)
            or not link.reference
            or link.source_id != expected_source
        ):
            return Refused(RefusalCode.BROKEN_TRACEABILITY, "calibration hierarchy is undocumented or broken")
        if link.source_id == link.target_id or link.target_id in visited:
            return Refused(RefusalCode.BROKEN_TRACEABILITY, "calibration hierarchy contains a cycle")
        if link.uncertainty is None:
            return Refused(
                RefusalCode.MISSING_CHAIN_UNCERTAINTY,
                "every calibration link must contribute an uncertainty",
            )
        try:
            contribution = as_fraction(link.uncertainty)
        except (TypeError, ValueError, ZeroDivisionError):
            return Refused(
                RefusalCode.INVALID_UNCERTAINTY,
                "calibration-link uncertainty must be an exact scalar",
            )
        if contribution < 0:
            return Refused(
                RefusalCode.MISSING_CHAIN_UNCERTAINTY,
                "calibration-link uncertainty must be non-negative",
            )
        uncertainties.append(contribution)
        expected_source = link.target_id
        visited.add(expected_source)
    if expected_source != traceability.terminal_reference_id:
        return Refused(
            RefusalCode.BROKEN_TRACEABILITY,
            "calibration hierarchy does not terminate at its declared reference",
        )
    return Accepted(tuple(uncertainties))


def measure(
    observation: AcceptedObservation | None,
    measurand: MeasurandSpecification | None,
    reported: ReportedValue | None,
    scale: NumericScale | None,
    calibration: Calibration | None,
    uncertainty: int | str | Fraction,
    provenance: Provenance | None,
    traceability: MetrologicalTraceability | Provenance | None,
    value_map: IndicationValueMap | None,
) -> Outcome[Measurement]:
    if not isinstance(observation, AcceptedObservation):
        return Refused(RefusalCode.MISSING_OBSERVATION, "measurement requires an accepted E-observation")
    observation_check = classify_observation(observation.receipt)
    if isinstance(observation_check, Refused):
        return observation_check
    observation = observation_check.value
    if (
        not isinstance(measurand, MeasurandSpecification)
        or not isinstance(measurand.quantity, str)
        or not measurand.quantity
        or not isinstance(measurand.system, str)
        or not measurand.system
        or not isinstance(measurand.conditions, tuple)
        or any(not isinstance(condition, str) or not condition for condition in measurand.conditions)
    ):
        return Refused(RefusalCode.MISSING_MEASURAND, "the intended quantity and system must be specified")
    if (
        not isinstance(reported, ReportedValue)
        or not isinstance(reported.carrier_id, str)
        or not reported.carrier_id
        or reported.value is None
    ):
        return Refused(RefusalCode.MISSING_REPORTED_VALUE, "a typed reported-value carrier is required")
    if (
        not isinstance(value_map, IndicationValueMap)
        or not isinstance(value_map.map_id, str)
        or not value_map.map_id
        or not isinstance(value_map.source_carrier_id, str)
        or not value_map.source_carrier_id
        or not isinstance(value_map.target_carrier_id, str)
        or not value_map.target_carrier_id
        or (
            value_map.source_key is not None
            and (
                not isinstance(value_map.source_key, str)
                or not value_map.source_key
            )
        )
    ):
        return Refused(RefusalCode.MISSING_VALUE_MAP, "a typed indication-to-value map is required")
    if (
        value_map.source_carrier_id != observation.registration.carrier_id
        or value_map.target_carrier_id != reported.carrier_id
    ):
        return Refused(
            RefusalCode.VALUE_MAP_MISMATCH,
            "the value map does not bind the observed and reported carriers",
        )
    indication = observation.registration.mark
    if value_map.source_key is not None:
        if not isinstance(indication, dict) or value_map.source_key not in indication:
            return Refused(
                RefusalCode.VALUE_MAP_MISMATCH,
                "the declared indication field is absent from the retained record",
            )
        indication = indication[value_map.source_key]
    try:
        indication_value = as_fraction(indication)
        gain = as_fraction(value_map.gain)
        offset = as_fraction(value_map.offset)
        raw = as_fraction(reported.value)
    except (TypeError, ValueError, ZeroDivisionError, OverflowError):
        return Refused(
            RefusalCode.INVALID_INPUT,
            "indication, value-map parameters, and reported value must be exact rational scalars",
        )
    if gain * indication_value + offset != raw:
        return Refused(
            RefusalCode.VALUE_MAP_MISMATCH,
            "the reported value is not the declared image of the retained indication",
        )
    if not isinstance(scale, NumericScale) or not isinstance(scale.scale_id, str) or not scale.scale_id:
        return Refused(RefusalCode.MISSING_SCALE, "a declared scale is required")
    if not isinstance(scale.unit, str) or not scale.unit:
        return Refused(RefusalCode.MISSING_UNIT, "a declared unit is required")
    try:
        lower = as_fraction(scale.lower)
        upper = as_fraction(scale.upper)
        resolution = as_fraction(scale.resolution)
    except (TypeError, ValueError, ZeroDivisionError, OverflowError):
        return Refused(
            RefusalCode.INVALID_INPUT,
            "scale bounds and resolution must be exact rational scalars",
        )
    if lower > upper or resolution <= 0:
        return Refused(RefusalCode.INVALID_INPUT, "scale bounds and positive resolution are required")
    if (
        not isinstance(calibration, Calibration)
        or not isinstance(calibration.calibration_id, str)
        or not calibration.calibration_id
    ):
        return Refused(RefusalCode.MISSING_CALIBRATION, "a local calibration receipt is required")
    if calibration.scale_id != scale.scale_id:
        return Refused(RefusalCode.ADAPTER_MISMATCH, "calibration names a different scale")
    if calibration.evaluator_id != observation.evaluator_result.evaluator_id:
        return Refused(RefusalCode.EVALUATOR_MISMATCH, "calibration and observation use different evaluators")
    if (
        not isinstance(provenance, Provenance)
        or not provenance.entries
        or any(not isinstance(entry, str) or not entry for entry in provenance.entries)
    ):
        return Refused(RefusalCode.MISSING_PROVENANCE, "WDP provenance and re-access history are required")
    hierarchy = _validate_traceability(calibration, traceability)
    if isinstance(hierarchy, Refused):
        return hierarchy
    try:
        corrected = raw + as_fraction(calibration.correction)
    except (TypeError, ValueError, ZeroDivisionError, OverflowError):
        return Refused(
            RefusalCode.INVALID_INPUT,
            "reported value and calibration correction must be exact rational scalars",
        )
    try:
        stated = as_fraction(uncertainty)
    except (TypeError, ValueError, ZeroDivisionError, OverflowError):
        return Refused(
            RefusalCode.INVALID_UNCERTAINTY,
            "stated uncertainty must be an exact rational scalar",
        )
    if stated < 0:
        return Refused(RefusalCode.INVALID_UNCERTAINTY, "stated uncertainty must be non-negative")
    if corrected < lower or corrected > upper:
        return Refused(RefusalCode.OUT_OF_RANGE, "corrected value lies outside the declared scale")
    grid_position = (corrected - lower) / resolution
    if grid_position.denominator != 1:
        return Refused(RefusalCode.OFF_GRID, "corrected value is not on the declared resolution grid")
    normalized_scale = NumericScale(scale.scale_id, scale.unit, lower, upper, resolution)
    combined = stated + sum(hierarchy.value, start=Fraction(0))
    assert isinstance(traceability, MetrologicalTraceability)
    return Accepted(
        Measurement(
            observation=observation,
            measurand=measurand,
            reported=reported,
            value_map=value_map,
            scale=normalized_scale,
            raw_value=raw,
            corrected_value=corrected,
            calibration=calibration,
            stated_uncertainty=stated,
            combined_uncertainty=combined,
            provenance=provenance,
            metrological_traceability=traceability,
        )
    )
