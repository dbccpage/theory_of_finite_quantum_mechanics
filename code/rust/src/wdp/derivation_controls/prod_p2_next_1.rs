//! Finite executable witness for `PROD-P2-NEXT-1`.
//!
//! Models the 12-step WDP Appendix G.5 `OutputGate` validator (`G5Step` order,
//! single-step mutation isolation, and receipt-iff-pass invariant) with fixed
//! `authority_effect = "None"`.

#![forbid(unsafe_code)]

pub const AUTHORITY_EFFECT_NONE: &str = "None";

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum G5Step {
    Ids,
    RawRecordHash,
    WitnessSemantics,
    ReAccess,
    LadderAccept,
    Measurand,
    UnitScale,
    CalibrationRange,
    Uncertainty,
    ProvenanceChain,
    Traceability,
    AuthoritySeparate,
}

impl G5Step {
    pub const ALL: [G5Step; 12] = [
        Self::Ids,
        Self::RawRecordHash,
        Self::WitnessSemantics,
        Self::ReAccess,
        Self::LadderAccept,
        Self::Measurand,
        Self::UnitScale,
        Self::CalibrationRange,
        Self::Uncertainty,
        Self::ProvenanceChain,
        Self::Traceability,
        Self::AuthoritySeparate,
    ];
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct CandidateRecord {
    pub interaction_carrier: String,
    pub registration_carrier: String,
    pub mark_value: i64,
    pub raw_record_hash_matches: bool,
    pub witness_target: String,
    pub witness_context: String,
    pub observed_mark_value: i64,
    pub evaluator_accepting: bool,
    pub reported_value: i64,
    pub unit_non_empty: bool,
    pub scale_lower: i64,
    pub scale_upper: i64,
    pub calibration_correction: i64,
    pub uncertainty_non_negative: bool,
    pub provenance_non_empty: bool,
    pub traceability_valid: bool,
    pub authority_decision_inline: bool,
}

impl CandidateRecord {
    pub fn valid() -> Self {
        Self {
            interaction_carrier: "sensor-carrier".to_string(),
            registration_carrier: "sensor-carrier".to_string(),
            mark_value: 6,
            raw_record_hash_matches: true,
            witness_target: "target-system".to_string(),
            witness_context: "finite_lattice".to_string(),
            observed_mark_value: 6,
            evaluator_accepting: true,
            reported_value: 6,
            unit_non_empty: true,
            scale_lower: 0,
            scale_upper: 10,
            calibration_correction: 1,
            uncertainty_non_negative: true,
            provenance_non_empty: true,
            traceability_valid: true,
            authority_decision_inline: false,
        }
    }

    pub fn mutate_for_step(step: G5Step) -> Self {
        let mut r = Self::valid();
        match step {
            G5Step::Ids => r.interaction_carrier = "other-carrier".to_string(),
            G5Step::RawRecordHash => r.raw_record_hash_matches = false,
            G5Step::WitnessSemantics => r.witness_target.clear(),
            G5Step::ReAccess => r.observed_mark_value = 999,
            G5Step::LadderAccept => r.evaluator_accepting = false,
            G5Step::Measurand => r.reported_value = 7,
            G5Step::UnitScale => r.unit_non_empty = false,
            G5Step::CalibrationRange => r.calibration_correction = 20,
            G5Step::Uncertainty => r.uncertainty_non_negative = false,
            G5Step::ProvenanceChain => r.provenance_non_empty = false,
            G5Step::Traceability => r.traceability_valid = false,
            G5Step::AuthoritySeparate => r.authority_decision_inline = true,
        }
        r
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ValidationReport {
    pub claim_id: String,
    pub failures: Vec<G5Step>,
    pub receipt_claim_id: Option<String>,
    pub authority_effect: &'static str,
}

impl ValidationReport {
    pub fn emitted(&self) -> bool {
        self.failures.is_empty() && self.receipt_claim_id.as_deref() == Some(self.claim_id.as_str())
    }
}

pub fn gate_candidate(claim_id: &str, rec: &CandidateRecord) -> Result<ValidationReport, &'static str> {
    if claim_id.is_empty() {
        return Err("invalid_input: claim_id must be non-empty");
    }
    let mut failures = Vec::new();
    if rec.interaction_carrier != rec.registration_carrier {
        failures.push(G5Step::Ids);
    }
    if !rec.raw_record_hash_matches {
        failures.push(G5Step::RawRecordHash);
    }
    if rec.witness_target.is_empty() || rec.witness_context.is_empty() {
        failures.push(G5Step::WitnessSemantics);
    }
    if rec.observed_mark_value != rec.mark_value {
        failures.push(G5Step::ReAccess);
    }
    if !rec.evaluator_accepting {
        failures.push(G5Step::LadderAccept);
    }
    if rec.reported_value != rec.mark_value {
        failures.push(G5Step::Measurand);
    }
    if !rec.unit_non_empty || rec.scale_lower > rec.scale_upper {
        failures.push(G5Step::UnitScale);
    }
    let corrected = rec.reported_value + rec.calibration_correction;
    if corrected < rec.scale_lower || corrected > rec.scale_upper {
        failures.push(G5Step::CalibrationRange);
    }
    if !rec.uncertainty_non_negative {
        failures.push(G5Step::Uncertainty);
    }
    if !rec.provenance_non_empty {
        failures.push(G5Step::ProvenanceChain);
    }
    if !rec.traceability_valid {
        failures.push(G5Step::Traceability);
    }
    if rec.authority_decision_inline {
        failures.push(G5Step::AuthoritySeparate);
    }

    let receipt_claim_id = if failures.is_empty() {
        Some(claim_id.to_string())
    } else {
        None
    };
    Ok(ValidationReport {
        claim_id: claim_id.to_string(),
        failures,
        receipt_claim_id,
        authority_effect: AUTHORITY_EFFECT_NONE,
    })
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn valid_record_emits_receipt_and_each_step_mutation_is_isolated() {
        let pass = gate_candidate("claim.1", &CandidateRecord::valid()).unwrap();
        assert!(pass.emitted());
        assert!(pass.failures.is_empty());
        assert_eq!(pass.receipt_claim_id.as_deref(), Some("claim.1"));
        assert_eq!(pass.authority_effect, "None");

        for step in G5Step::ALL {
            let mutated = CandidateRecord::mutate_for_step(step);
            let rep = gate_candidate("claim.1", &mutated).unwrap();
            assert!(!rep.emitted());
            assert_eq!(rep.receipt_claim_id, None);
            assert_eq!(rep.failures, vec![step]);
        }
    }
}
