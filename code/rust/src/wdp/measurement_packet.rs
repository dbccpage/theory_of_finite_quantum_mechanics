
use std::collections::BTreeSet;

use num_rational::BigRational;
use num_traits::Zero;
use engine_measurement::affine_calibration::{BoundedReading, CalibrationError};
use engine_measurement::documentary_traceability::{
    validate_documentary_traceability, DocumentaryTraceabilityError, DocumentaryTraceabilityGraph,
    DocumentaryTraceabilityReport,
};
use engine_measurement::{MeasurementValue, UnitSpec};
use engine_quantum_physics::exact_instrument::{ExactDensityState, ExactInstrumentError};
use engine_quantum_physics::instrument_repeatability::{is_outcome_repeatable, RepeatabilityError};
use serde::Serialize;
use serde_json::{json, Value};

use crate::calibration_adapter::{
    evaluate_calibration_packet, CalibrationPacket, CalibrationPacketError, CalibrationReceipt,
};
use crate::instrument_adapter::{FiniteInstrumentReceipt, FiniteQuantumInstrument};
use crate::types::{blake3_digest, AuthorityEffect};

#[derive(Debug, Clone, PartialEq, Eq, thiserror::Error)]
pub enum MeasurementPacketError {
    #[error("instrument refusal: {0}")]
    Instrument(#[from] ExactInstrumentError),
    #[error("repeatability refusal: {0}")]
    Repeatability(#[from] RepeatabilityError),
    #[error("calibration refusal: {0}")]
    CalibrationPacket(#[from] CalibrationPacketError),
    #[error("calibration arithmetic refusal: {0}")]
    Calibration(#[from] CalibrationError),
    #[error("documentary graph refusal: {0}")]
    Traceability(#[from] DocumentaryTraceabilityError),
    #[error("required identity {field} is empty")]
    EmptyIdentity { field: &'static str },
    #[error("field {field} is not a valid exact rational")]
    InvalidRational { field: &'static str },
    #[error("the interaction must contain distinct poles including the mark carrier")]
    Interaction,
    #[error("no retained mark-capable registration was supplied")]
    NotRetained,
    #[error("retained mark differs from the actual instrument/state/outcome/indication")]
    RegistrationMismatch,
    #[error("reaccessed artifact differs from the retained mark")]
    ReaccessMismatch,
    #[error("observation lacks Accept and accepting evaluator standing")]
    NonAcceptingObservation,
    #[error("witness and observation context disagree")]
    WitnessMismatch,
    #[error("a zero-probability outcome cannot be admitted as the selected event")]
    ImpossibleOutcome,
    #[error("one exact indication must be declared per instrument outcome")]
    IndicationShape,
    #[error("same-instrument outcome repeatability was required but does not hold")]
    NonRepeatable,
    #[error("indication/carrier/value-map/nominal-calibration binding disagrees")]
    ValueMapMismatch,
    #[error("documentary traceability is not bound to this calibration and result unit")]
    TraceabilityBinding,
    #[error("declared uncertainty is negative or smaller than the propagated error")]
    UncertaintyUnderstated,
    #[error("declared numeric scale is invalid or does not contain the corrected enclosure")]
    Scale,
    #[error("packet needs explicit artifact provenance")]
    MissingProvenance,
    #[error("receipt encoding failed: {detail}")]
    Encoding { detail: String },
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct MeasurandSpecification {
    pub quantity_id: String,
    pub system_id: String,
    pub conditions: Vec<String>,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct NumericMeasurementScale {
    pub scale_id: String,
    pub unit: UnitSpec,
    pub lower: BigRational,
    pub upper: BigRational,
    pub resolution: BigRational,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct IndicationValueMap {
    pub map_id: String,
    pub source_carrier_id: String,
    pub result_carrier_id: String,
    pub gain: BigRational,
    pub offset: BigRational,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize)]
pub enum ObservationStatus {
    Accept,
    Reject,
    Refuse,
    Undetermined,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct InstrumentObservationContext {
    pub interaction_id: String,
    pub poles: Vec<String>,
    pub registration_carrier_id: String,
    pub mark_capacity: bool,
    pub evaluator_id: String,
    pub evaluator_status: ObservationStatus,
    pub accepting_standing: bool,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct InstrumentMark {
    pub instrument: FiniteInstrumentReceipt,
    pub indication: BigRational,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct InstrumentRegistration {
    pub registration_id: String,
    pub carrier_id: String,
    pub retained: bool,
    pub mark: InstrumentMark,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct InstrumentWitness {
    pub registration_id: String,
    pub carrier_id: String,
    pub evaluator_id: String,
    pub retained_mark_digest: String,
    pub reaccessed_mark_digest: String,
    pub authority_effect: AuthorityEffect,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct AcceptedInstrumentObservation {
    pub context: InstrumentObservationContext,
    pub registration: InstrumentRegistration,
    pub witness: InstrumentWitness,
    pub authority_effect: AuthorityEffect,
}

#[derive(Debug, Clone)]
pub struct QuantumMeasurementProblem {
    pub packet_id: String,
    pub instrument: FiniteQuantumInstrument,
    pub input_state: ExactDensityState,
    pub selected_outcome: usize,
    pub outcome_indications: Vec<BigRational>,
    pub context: InstrumentObservationContext,
    pub registration: InstrumentRegistration,
    pub calibration: CalibrationPacket,
    pub calibration_scale_id: String,
    pub calibration_evaluator_id: String,
    pub value_map: IndicationValueMap,
    pub measurand: MeasurandSpecification,
    pub scale: NumericMeasurementScale,
    pub declared_raw_value: BigRational,
    pub correction: BigRational,
    pub stated_uncertainty: BigRational,
    pub traceability: DocumentaryTraceabilityGraph,
    pub artifact_provenance: Vec<String>,
    pub require_outcome_repeatability: bool,
}

#[derive(Debug, Clone, PartialEq, Serialize)]
pub struct DeclaredMeasurementResult {
    pub measurand: MeasurandSpecification,
    pub result_carrier_id: String,
    pub scale: NumericMeasurementScale,
    pub raw_value: BigRational,
    pub corrected_value: BigRational,
    pub stated_uncertainty: BigRational,
    pub combined_uncertainty: BigRational,
    pub native_value: MeasurementValue,
    pub authority_effect: AuthorityEffect,
}

#[derive(Debug, Clone, PartialEq)]
pub struct QuantumMeasurementReceipt {
    pub problem_digest: String,
    pub observation: AcceptedInstrumentObservation,
    pub calibration: CalibrationReceipt,
    pub traceability: DocumentaryTraceabilityReport,
    pub result: DeclaredMeasurementResult,
    pub corrected_enclosure: BoundedReading,
    pub repeatability_checked: bool,
    pub artifact_provenance: Vec<String>,
    pub authority_effect: AuthorityEffect,
    pub receipt_digest: String,
}

fn identity(value: &str, field: &'static str) -> Result<(), MeasurementPacketError> {
    if value.trim().is_empty() {
        return Err(MeasurementPacketError::EmptyIdentity { field });
    }
    Ok(())
}
fn rational(value: &BigRational, field: &'static str) -> Result<(), MeasurementPacketError> {
    if value.denom() <= &0.into() {
        return Err(MeasurementPacketError::InvalidRational { field });
    }
    Ok(())
}
fn digest<T: Serialize>(value: &T) -> Result<String, MeasurementPacketError> {
    let bytes = serde_json::to_vec(value).map_err(|error| MeasurementPacketError::Encoding {
        detail: error.to_string(),
    })?;
    Ok(blake3_digest(&bytes))
}
fn reading_payload(reading: &BoundedReading) -> Value {
    json!({ "center": reading.center(), "radius": reading.radius() })
}
fn calibration_packet_payload(packet: &CalibrationPacket) -> Value {
    let stages: Vec<Value> = packet
        .stages
        .iter()
        .map(|stage| {
            let calibration = &stage.calibration;
            json!({
                "stage_id": stage.stage_id,
                "gain": calibration.gain(), "offset": calibration.offset(),
                "gain_error": calibration.gain_error(),
                "offset_error": calibration.offset_error(),
                "residual_error": calibration.residual_error(),
            })
        })
        .collect();
    json!({ "packet_id": packet.packet_id, "input": reading_payload(&packet.input), "stages": stages })
}
fn calibration_receipt_payload(receipt: &CalibrationReceipt) -> Value {
    json!({
        "packet": calibration_packet_payload(&receipt.packet),
        "readings": receipt.readings.iter().map(reading_payload).collect::<Vec<_>>(),
        "nominal_gain": receipt.nominal_gain, "nominal_offset": receipt.nominal_offset,
        "authority_effect": receipt.authority_effect,
    })
}

pub fn register_instrument_problem(
    actual: &QuantumMeasurementProblem,
) -> Result<InstrumentRegistration, MeasurementPacketError> {
    let registration = &actual.registration;
    identity(&registration.registration_id, "registration_id")?;
    identity(&registration.carrier_id, "carrier_id")?;
    if !registration.retained || !actual.context.mark_capacity {
        return Err(MeasurementPacketError::NotRetained);
    }
    if actual.outcome_indications.len() != actual.instrument.instrument().outcomes() {
        return Err(MeasurementPacketError::IndicationShape);
    }
    for value in &actual.outcome_indications {
        rational(value, "outcome_indication")?;
    }
    let instrument_receipt = actual
        .instrument
        .receipt(actual.selected_outcome, &actual.input_state)?;
    if instrument_receipt.probability.is_zero() {
        return Err(MeasurementPacketError::ImpossibleOutcome);
    }
    let expected = InstrumentMark {
        instrument: instrument_receipt,
        indication: actual.outcome_indications[actual.selected_outcome].clone(),
    };
    if registration.mark != expected {
        return Err(MeasurementPacketError::RegistrationMismatch);
    }
    Ok(registration.clone())
}

pub fn witness_instrument_registration(
    registration: &InstrumentRegistration,
    evaluator_id: &str,
    reaccessed_mark: &InstrumentMark,
) -> Result<InstrumentWitness, MeasurementPacketError> {
    identity(evaluator_id, "evaluator_id")?;
    identity(&registration.registration_id, "registration_id")?;
    identity(&registration.carrier_id, "carrier_id")?;
    if !registration.retained {
        return Err(MeasurementPacketError::NotRetained);
    }
    if &registration.mark != reaccessed_mark {
        return Err(MeasurementPacketError::ReaccessMismatch);
    }
    Ok(InstrumentWitness {
        registration_id: registration.registration_id.clone(),
        carrier_id: registration.carrier_id.clone(),
        evaluator_id: evaluator_id.into(),
        retained_mark_digest: digest(
            &json!({ "kind": "wdp-instrument-mark-v1", "mark": registration.mark }),
        )?,
        reaccessed_mark_digest: digest(
            &json!({ "kind": "wdp-instrument-mark-v1", "mark": reaccessed_mark }),
        )?,
        authority_effect: AuthorityEffect::None,
    })
}

pub fn accept_instrument_observation(
    context: &InstrumentObservationContext,
    registration: &InstrumentRegistration,
    witness: &InstrumentWitness,
) -> Result<AcceptedInstrumentObservation, MeasurementPacketError> {
    identity(&context.interaction_id, "interaction_id")?;
    identity(&context.evaluator_id, "evaluator_id")?;
    identity(&context.registration_carrier_id, "registration_carrier_id")?;
    let distinct: BTreeSet<_> = context.poles.iter().collect();
    if context.poles.len() < 2
        || distinct.len() != context.poles.len()
        || context.poles.iter().any(|pole| pole.trim().is_empty())
        || !context.poles.contains(&context.registration_carrier_id)
        || context.registration_carrier_id != registration.carrier_id
    {
        return Err(MeasurementPacketError::Interaction);
    }
    if context.evaluator_status != ObservationStatus::Accept || !context.accepting_standing {
        return Err(MeasurementPacketError::NonAcceptingObservation);
    }
    let expected_witness =
        witness_instrument_registration(registration, &context.evaluator_id, &registration.mark)?;
    if witness != &expected_witness || !context.mark_capacity {
        return Err(MeasurementPacketError::WitnessMismatch);
    }
    Ok(AcceptedInstrumentObservation {
        context: context.clone(),
        registration: registration.clone(),
        witness: witness.clone(),
        authority_effect: AuthorityEffect::None,
    })
}

fn actual_problem_digest(
    actual: &QuantumMeasurementProblem,
) -> Result<String, MeasurementPacketError> {
    let instrument = actual
        .instrument
        .receipt(actual.selected_outcome, &actual.input_state)?;
    digest(&json!({
        "kind": "wdp-quantum-measurement-problem-v1", "packet_id": actual.packet_id,
        "instrument": instrument, "outcome_indications": actual.outcome_indications,
        "context": actual.context, "registration": actual.registration,
        "calibration": calibration_packet_payload(&actual.calibration),
        "calibration_scale_id": actual.calibration_scale_id,
        "calibration_evaluator_id": actual.calibration_evaluator_id,
        "value_map": actual.value_map, "measurand": actual.measurand,
        "scale": actual.scale, "declared_raw_value": actual.declared_raw_value,
        "correction": actual.correction, "stated_uncertainty": actual.stated_uncertainty,
        "traceability": actual.traceability, "artifact_provenance": actual.artifact_provenance,
        "require_outcome_repeatability": actual.require_outcome_repeatability,
    }))
}

impl QuantumMeasurementReceipt {
    pub fn refresh_digest(&mut self) -> Result<(), MeasurementPacketError> {
        self.receipt_digest = digest(&json!({
            "kind": "wdp-quantum-measurement-receipt-v1", "problem_digest": self.problem_digest,
            "observation": self.observation,
            "calibration": calibration_receipt_payload(&self.calibration),
            "traceability": self.traceability, "result": self.result,
            "corrected_enclosure": reading_payload(&self.corrected_enclosure),
            "repeatability_checked": self.repeatability_checked,
            "artifact_provenance": self.artifact_provenance,
            "authority_effect": self.authority_effect,
        }))?;
        Ok(())
    }
}

pub fn evaluate_quantum_measurement(
    actual: &QuantumMeasurementProblem,
    reaccessed_mark: &InstrumentMark,
) -> Result<QuantumMeasurementReceipt, MeasurementPacketError> {
    identity(&actual.packet_id, "packet_id")?;
    identity(&actual.measurand.quantity_id, "quantity_id")?;
    identity(&actual.measurand.system_id, "system_id")?;
    identity(&actual.value_map.map_id, "map_id")?;
    identity(&actual.value_map.result_carrier_id, "result_carrier_id")?;
    identity(&actual.scale.scale_id, "scale_id")?;
    identity(&actual.scale.unit.unit_name, "unit_name")?;
    identity(&actual.calibration.packet_id, "calibration_packet_id")?;
    identity(&actual.calibration_scale_id, "calibration_scale_id")?;
    identity(&actual.calibration_evaluator_id, "calibration_evaluator_id")?;
    for stage in &actual.calibration.stages {
        identity(&stage.stage_id, "calibration_stage_id")?;
    }
    for condition in &actual.measurand.conditions {
        identity(condition, "measurand_condition")?;
    }
    if actual.artifact_provenance.is_empty()
        || actual
            .artifact_provenance
            .iter()
            .any(|id| id.trim().is_empty())
    {
        return Err(MeasurementPacketError::MissingProvenance);
    }
    for (value, field) in [
        (&actual.value_map.gain, "value_map_gain"),
        (&actual.value_map.offset, "value_map_offset"),
        (&actual.declared_raw_value, "declared_raw_value"),
        (&actual.correction, "correction"),
        (&actual.stated_uncertainty, "stated_uncertainty"),
        (&actual.scale.lower, "scale_lower"),
        (&actual.scale.upper, "scale_upper"),
        (&actual.scale.resolution, "scale_resolution"),
    ] {
        rational(value, field)?;
    }
    let registration = register_instrument_problem(actual)?;
    let witness = witness_instrument_registration(
        &registration,
        &actual.context.evaluator_id,
        reaccessed_mark,
    )?;
    let observation = accept_instrument_observation(&actual.context, &registration, &witness)?;
    if actual.require_outcome_repeatability
        && !is_outcome_repeatable(actual.instrument.instrument())?
    {
        return Err(MeasurementPacketError::NonRepeatable);
    }
    if actual.calibration.input.center() != &registration.mark.indication
        || actual.value_map.source_carrier_id != registration.carrier_id
        || actual.calibration_scale_id != actual.scale.scale_id
        || actual.calibration_evaluator_id != actual.context.evaluator_id
    {
        return Err(MeasurementPacketError::ValueMapMismatch);
    }
    let calibration = evaluate_calibration_packet(&actual.calibration)?;
    let output = calibration
        .readings
        .last()
        .expect("calibration includes the initial reading");
    if calibration.nominal_gain != actual.value_map.gain
        || calibration.nominal_offset != actual.value_map.offset
        || output.center() != &actual.declared_raw_value
    {
        return Err(MeasurementPacketError::ValueMapMismatch);
    }
    if actual.stated_uncertainty < *output.radius() {
        return Err(MeasurementPacketError::UncertaintyUnderstated);
    }
    let traceability = validate_documentary_traceability(&actual.traceability)?;
    if traceability.graph().origin_id != actual.calibration.packet_id
        || traceability.graph().result_unit != actual.scale.unit.unit_name
    {
        return Err(MeasurementPacketError::TraceabilityBinding);
    }
    let corrected_value = output.center() + &actual.correction;
    let corrected_enclosure = BoundedReading::new(
        corrected_value.clone(),
        output.radius() + traceability.additive_bound(),
    )?;
    if actual.scale.resolution <= BigRational::zero()
        || actual.scale.lower > actual.scale.upper
        || corrected_enclosure.center() - corrected_enclosure.radius() < actual.scale.lower
        || corrected_enclosure.center() + corrected_enclosure.radius() > actual.scale.upper
    {
        return Err(MeasurementPacketError::Scale);
    }
    let grid_position = (&corrected_value - &actual.scale.lower) / &actual.scale.resolution;
    if !grid_position.is_integer() {
        return Err(MeasurementPacketError::Scale);
    }
    let result = DeclaredMeasurementResult {
        measurand: actual.measurand.clone(),
        result_carrier_id: actual.value_map.result_carrier_id.clone(),
        scale: actual.scale.clone(),
        raw_value: output.center().clone(),
        corrected_value: corrected_value.clone(),
        stated_uncertainty: actual.stated_uncertainty.clone(),
        combined_uncertainty: &actual.stated_uncertainty + traceability.additive_bound(),
        native_value: MeasurementValue::ExactRational(corrected_value),
        authority_effect: AuthorityEffect::None,
    };
    let mut receipt = QuantumMeasurementReceipt {
        problem_digest: actual_problem_digest(actual)?,
        observation,
        calibration,
        traceability,
        result,
        corrected_enclosure,
        repeatability_checked: actual.require_outcome_repeatability,
        artifact_provenance: actual.artifact_provenance.clone(),
        authority_effect: AuthorityEffect::None,
        receipt_digest: String::new(),
    };
    receipt.refresh_digest()?;
    Ok(receipt)
}

pub fn verify_quantum_measurement(
    actual: &QuantumMeasurementProblem,
    reaccessed_mark: &InstrumentMark,
    candidate: &QuantumMeasurementReceipt,
) -> Result<bool, MeasurementPacketError> {
    Ok(candidate == &evaluate_quantum_measurement(actual, reaccessed_mark)?)
}
