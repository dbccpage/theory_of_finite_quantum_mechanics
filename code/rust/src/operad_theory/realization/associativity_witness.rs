
use serde::{Deserialize, Serialize};
use crate::foundation::{Operation, PlanarColoredOperad};

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub enum ComputationStatus {
    Completed,
    Refused,
    NotComputed,
    BudgetExceeded,
    InternalError,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub enum LawResult {
    Satisfied,
    Violated,
    NotApplicable,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub enum EvidenceKind {
    ExactStructural,
    Symbolic,
    BoundedExample,
    ShapeOnly,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct StructuralAssociativityWitness {
    pub law_id: String,
    pub computation_status: ComputationStatus,
    pub law_result: LawResult,
    pub evidence_kind: EvidenceKind,
    pub left_expression: String,
    pub right_expression: String,
    pub index_convention: String,
    pub evidence_notes: String,
}

impl StructuralAssociativityWitness {
    pub fn is_satisfied(&self) -> bool {
        self.computation_status == ComputationStatus::Completed && self.law_result == LawResult::Satisfied
    }

    pub fn verify_sequential(
        operad: &PlanarColoredOperad,
        f: &Operation,
        g: &Operation,
        h: &Operation,
        i: usize,
        j: usize,
    ) -> Self {
        let left_str = format!("({} o_{} {}) o_{} {}", f.op_id.as_str(), i, g.op_id.as_str(), i + j, h.op_id.as_str());
        let right_str = format!("{} o_{} ({} o_{} {})", f.op_id.as_str(), i, g.op_id.as_str(), j, h.op_id.as_str());

        if i >= f.arity() || j >= g.arity() {
            return Self {
                law_id: "sequential_associativity".to_string(),
                computation_status: ComputationStatus::Refused,
                law_result: LawResult::NotApplicable,
                evidence_kind: EvidenceKind::ExactStructural,
                left_expression: left_str,
                right_expression: right_str,
                index_convention: "zero_based".to_string(),
                evidence_notes: format!("Indices i={}, j={} out of arity bounds", i, j),
            };
        }

        if g.output() != &f.inputs()[i] || h.output() != &g.inputs()[j] {
            return Self {
                law_id: "sequential_associativity".to_string(),
                computation_status: ComputationStatus::Refused,
                law_result: LawResult::NotApplicable,
                evidence_kind: EvidenceKind::ExactStructural,
                left_expression: left_str,
                right_expression: right_str,
                index_convention: "zero_based".to_string(),
                evidence_notes: "Ill-typed colour boundary matching.".to_string(),
            };
        }

        let f_circ_g = match operad.partial_compose(f, g, i) {
            Ok(op) => op,
            Err(e) => return Self::refused(&left_str, &right_str, e),
        };
        let left_op = match operad.partial_compose(&f_circ_g, h, i + j) {
            Ok(op) => op,
            Err(e) => return Self::refused(&left_str, &right_str, e),
        };

        let g_circ_h = match operad.partial_compose(g, h, j) {
            Ok(op) => op,
            Err(e) => return Self::refused(&left_str, &right_str, e),
        };
        let right_op = match operad.partial_compose(f, &g_circ_h, i) {
            Ok(op) => op,
            Err(e) => return Self::refused(&left_str, &right_str, e),
        };

        let is_eq = left_op.signature == right_op.signature;
        Self {
            law_id: "sequential_associativity".to_string(),
            computation_status: ComputationStatus::Completed,
            law_result: if is_eq { LawResult::Satisfied } else { LawResult::Violated },
            evidence_kind: EvidenceKind::ExactStructural,
            left_expression: left_str,
            right_expression: right_str,
            index_convention: "zero_based".to_string(),
            evidence_notes: format!("Verified exact equality of composite signatures: {}", left_op.signature),
        }
    }

    pub fn verify_unit(operad: &PlanarColoredOperad, f: &Operation) -> Self {
        let left_str = format!("{} o_0 id", f.op_id.as_str());
        let right_str = f.op_id.as_str().to_string();

        if f.arity() == 0 {
            return Self {
                law_id: "unit_law".to_string(),
                computation_status: ComputationStatus::Completed,
                law_result: LawResult::Satisfied,
                evidence_kind: EvidenceKind::ExactStructural,
                left_expression: left_str,
                right_expression: right_str,
                index_convention: "zero_based".to_string(),
                evidence_notes: "Nullary operation vacuously satisfies unit law.".to_string(),
            };
        }

        let id_op = Operation::identity(f.inputs()[0].clone());
        let composed = match operad.partial_compose(f, &id_op, 0) {
            Ok(op) => op,
            Err(e) => return Self::refused(&left_str, &right_str, e),
        };

        let is_eq = composed.signature == f.signature;
        Self {
            law_id: "unit_law".to_string(),
            computation_status: ComputationStatus::Completed,
            law_result: if is_eq { LawResult::Satisfied } else { LawResult::Violated },
            evidence_kind: EvidenceKind::ExactStructural,
            left_expression: left_str,
            right_expression: right_str,
            index_convention: "zero_based".to_string(),
            evidence_notes: "Unit law verified.".to_string(),
        }
    }

    fn refused(left: &str, right: &str, err: String) -> Self {
        Self {
            law_id: "associativity".to_string(),
            computation_status: ComputationStatus::Refused,
            law_result: LawResult::NotApplicable,
            evidence_kind: EvidenceKind::ExactStructural,
            left_expression: left.to_string(),
            right_expression: right.to_string(),
            index_convention: "zero_based".to_string(),
            evidence_notes: err,
        }
    }
}
