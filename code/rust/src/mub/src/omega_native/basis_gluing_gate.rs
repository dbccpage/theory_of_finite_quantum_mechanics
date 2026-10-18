
use serde::Serialize;

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Serialize)]
pub enum BasisGluingStatus {
    DeclaredObligationsComplete,
    MissingProofObligation,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct BasisGluingInputs {
    pub pinned_upper_replayed: bool,
    pub exhaustive_triple_cover: bool,
    pub accepted_patch_count: usize,
    pub wall_transport_for_every_class: bool,
    pub overlap_compatibility: bool,
    pub zero_rel_preserved: bool,
    pub terminalizer_preserved: bool,
    pub classwise_fourth_vector_obstruction: bool,
    pub gluing_theorem_present: bool,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct BasisGluingGateReport {
    pub target: &'static str,
    pub status: BasisGluingStatus,
    pub accepted_patch_count: usize,
    pub checked_obligations: Vec<&'static str>,
    pub missing_obligations: Vec<&'static str>,
    pub rejected_escalations: Vec<&'static str>,
    pub boundary: &'static str,
    pub error: Option<String>,
}

pub fn verify_basis_gluing_gate(inputs: BasisGluingInputs) -> BasisGluingGateReport {
    let mut checked = Vec::new();
    let mut missing = Vec::new();

    if inputs.pinned_upper_replayed {
        checked.push("pinned fourth-vector upper obstruction replayed");
    } else {
        missing.push("local replay of the pinned fourth-vector upper obstruction");
    }
    if inputs.exhaustive_triple_cover {
        checked.push("exhaustive cover of admissible MUB(6) triples supplied");
    } else {
        missing.push("exhaustive cover of admissible MUB(6) triples");
    }
    if inputs.accepted_patch_count > 0 && inputs.wall_transport_for_every_class {
        checked.push("wall-certified transport patch for every covered class");
    } else {
        missing.push("wall-certified transport patch for every covered class");
    }
    if inputs.overlap_compatibility {
        checked.push("atlas patch overlaps are compatible");
    } else {
        missing.push("patch-intersection compatibility for atlas patches");
    }
    if inputs.zero_rel_preserved {
        checked.push("ZeroRel preservation across atlas transports");
    } else {
        missing.push("ZeroRel preservation across atlas transports");
    }
    if inputs.terminalizer_preserved {
        checked.push("terminalizer preservation across atlas transports");
    } else {
        missing.push("terminalizer preservation across atlas transports");
    }
    if inputs.classwise_fourth_vector_obstruction {
        checked.push("classwise fourth-vector obstruction supplied");
    } else {
        missing.push("classwise fourth-vector obstruction for every covered triple class");
    }
    if inputs.gluing_theorem_present {
        checked.push(
            "basis-gluing theorem from fourth-vector obstruction to no complete seven-basis set",
        );
    } else {
        missing.push(
            "basis-gluing theorem from fourth-vector obstruction to no complete seven-basis set",
        );
    }

    let status = if missing.is_empty() {
        BasisGluingStatus::DeclaredObligationsComplete
    } else {
        BasisGluingStatus::MissingProofObligation
    };

    BasisGluingGateReport {
        target: "full MUB(6) basis-gluing route checklist",
        status,
        accepted_patch_count: inputs.accepted_patch_count,
        checked_obligations: checked,
        missing_obligations: missing,
        rejected_escalations: vec![
            "a pinned fourth-vector wall does not range over all admissible triples",
            "transport inside one H-symmetry lane is not a global triple cover",
            "classwise fourth-vector obstruction is not complete-set nonexistence without a gluing theorem",
            "basis gluing cannot run before C3 atlas coherence supplies cover and transport compatibility",
            "declared checklist completeness does not constitute verified mathematical proof of missing theorems",
        ],
        boundary: if status == BasisGluingStatus::DeclaredObligationsComplete {
            "basis-gluing checklist complete: declared obligations are satisfied, but unverified external proof artifacts are not checked"
        } else {
            "basis-gluing route is incomplete; no full MUB(6) no-go is authorized"
        },
        error: if status == BasisGluingStatus::DeclaredObligationsComplete {
            None
        } else {
            Some("missing basis-gluing proof obligations".to_string())
        },
    }
}

pub fn current_atlas_basis_gluing_inputs(accepted_patch_count: usize) -> BasisGluingInputs {
    BasisGluingInputs {
        pinned_upper_replayed: true,
        exhaustive_triple_cover: false,
        accepted_patch_count,
        wall_transport_for_every_class: false,
        overlap_compatibility: false,
        zero_rel_preserved: false,
        terminalizer_preserved: false,
        classwise_fourth_vector_obstruction: accepted_patch_count > 0,
        gluing_theorem_present: false,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn basis_gluing_gate_rejects_pinned_wall_without_cover() {
        let report = verify_basis_gluing_gate(BasisGluingInputs {
            pinned_upper_replayed: true,
            exhaustive_triple_cover: false,
            accepted_patch_count: 0,
            wall_transport_for_every_class: false,
            overlap_compatibility: false,
            zero_rel_preserved: false,
            terminalizer_preserved: false,
            classwise_fourth_vector_obstruction: false,
            gluing_theorem_present: false,
        });
        assert_eq!(report.status, BasisGluingStatus::MissingProofObligation);
        assert!(report
            .missing_obligations
            .iter()
            .any(|obligation| obligation.contains("exhaustive cover")));
        assert!(report
            .rejected_escalations
            .iter()
            .any(|item| item.contains("pinned fourth-vector")));
    }

    #[test]
    fn current_atlas_inputs_still_missing_gluing_theorem() {
        let report = verify_basis_gluing_gate(current_atlas_basis_gluing_inputs(7));
        assert_eq!(report.status, BasisGluingStatus::MissingProofObligation);
        assert_eq!(report.accepted_patch_count, 7);
        assert!(report
            .missing_obligations
            .iter()
            .any(|o| o.contains("exhaustive cover")));
        assert!(report
            .missing_obligations
            .iter()
            .any(|o| o.contains("basis-gluing theorem")));
        assert!(report
            .checked_obligations
            .iter()
            .any(|o| o.contains("classwise fourth-vector")));
    }

    #[test]
    fn basis_gluing_gate_accepts_only_complete_certified_route() {
        let report = verify_basis_gluing_gate(BasisGluingInputs {
            pinned_upper_replayed: true,
            exhaustive_triple_cover: true,
            accepted_patch_count: 2,
            wall_transport_for_every_class: true,
            overlap_compatibility: true,
            zero_rel_preserved: true,
            terminalizer_preserved: true,
            classwise_fourth_vector_obstruction: true,
            gluing_theorem_present: true,
        });
        assert_eq!(report.status, BasisGluingStatus::DeclaredObligationsComplete);
        assert!(report.missing_obligations.is_empty());
        assert!(report.error.is_none());
    }
}
