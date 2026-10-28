
use serde::Serialize;

use engine_quantum_physics::mub::finite_projector_control::{
    verify_current_finite_projector_controls, FiniteProjectorControlReport,
    FiniteProjectorControlStatus,
};

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Serialize)]
pub enum CharTwoParametricStatus {
    DeclaredObligationsComplete,
    FiniteSamplesOnly,
    MissingFiniteSamples,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct CharTwoParametricInputs {
    pub finite_controls: Vec<FiniteProjectorControlReport>,
    pub binary_field_family: bool,
    pub irreducible_modulus_family: bool,
    pub symplectic_spread_family: bool,
    pub board_incidence_family: bool,
    pub spectral_projector_lift_family: bool,
    pub pauli_phase_family: bool,
    pub positive_projector_family: bool,
    pub hilbert_transport_family: bool,
    pub gtmur_loss_ledger_family: bool,
    pub terminalizer_preserved_family: bool,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct CharTwoParametricGateReport {
    pub source: &'static str,
    pub status: CharTwoParametricStatus,
    pub finite_sample_count: usize,
    pub sampled_exponents: Vec<usize>,
    pub sampled_dimensions: Vec<usize>,
    pub checked_obligations: Vec<&'static str>,
    pub missing_obligations: Vec<&'static str>,
    pub rejected_escalations: Vec<&'static str>,
    pub boundary: &'static str,
    pub error: Option<String>,
}

pub fn verify_current_char_two_parametric_gate() -> CharTwoParametricGateReport {
    verify_char_two_parametric_gate(CharTwoParametricInputs {
        finite_controls: verify_current_finite_projector_controls(),
        binary_field_family: false,
        irreducible_modulus_family: false,
        symplectic_spread_family: false,
        board_incidence_family: false,
        spectral_projector_lift_family: false,
        pauli_phase_family: false,
        positive_projector_family: false,
        hilbert_transport_family: false,
        gtmur_loss_ledger_family: false,
        terminalizer_preserved_family: false,
    })
}

pub fn verify_char_two_parametric_gate(
    inputs: CharTwoParametricInputs,
) -> CharTwoParametricGateReport {
    let complete_controls = inputs
        .finite_controls
        .iter()
        .filter(|control| {
            control.status == FiniteProjectorControlStatus::CompleteProjectorMubVerified
        })
        .collect::<Vec<_>>();
    let finite_sample_count = complete_controls.len();
    let sampled_exponents = complete_controls
        .iter()
        .map(|control| control.exponent)
        .collect::<Vec<_>>();
    let sampled_dimensions = complete_controls
        .iter()
        .map(|control| control.dimension)
        .collect::<Vec<_>>();

    let mut checked = Vec::new();
    let mut missing = Vec::new();
    if finite_sample_count > 0 {
        checked.push(
            "finite characteristic-two projector controls are replayed for sampled exponents",
        );
    } else {
        missing.push("at least one finite characteristic-two projector control sample");
    }

    push_obligation(
        inputs.binary_field_family,
        "dimension-parametric binary finite-field family GF(2^k)",
        &mut checked,
        &mut missing,
    );
    push_obligation(
        inputs.irreducible_modulus_family,
        "uniform irreducible-modulus or field-existence theorem for every k",
        &mut checked,
        &mut missing,
    );
    push_obligation(
        inputs.symplectic_spread_family,
        "dimension-parametric symplectic spread construction in GF(2^k)^2",
        &mut checked,
        &mut missing,
    );
    push_obligation(
        inputs.board_incidence_family,
        "formal isotropic-line intersection and nonzero-cover proof for every k",
        &mut checked,
        &mut missing,
    );
    push_obligation(
        inputs.spectral_projector_lift_family,
        "dimension-parametric spectral-projector lift from spread lines",
        &mut checked,
        &mut missing,
    );
    push_obligation(
        inputs.pauli_phase_family,
        "uniform characteristic-two Pauli phase convention and multiplication law",
        &mut checked,
        &mut missing,
    );
    push_obligation(
        inputs.positive_projector_family,
        "formal positive rank-one projector theorem for every k",
        &mut checked,
        &mut missing,
    );
    push_obligation(
        inputs.hilbert_transport_family,
        "dimension-parametric Hilbert-space transport from projector algebra",
        &mut checked,
        &mut missing,
    );
    push_obligation(
        inputs.gtmur_loss_ledger_family,
        "dimension-parametric CODA-MUR loss ledger preserving ZeroRel",
        &mut checked,
        &mut missing,
    );
    push_obligation(
        inputs.terminalizer_preserved_family,
        "dimension-parametric terminalizer preservation across the representation stack",
        &mut checked,
        &mut missing,
    );

    let status = if missing.is_empty() {
        CharTwoParametricStatus::DeclaredObligationsComplete
    } else if finite_sample_count == 0 {
        CharTwoParametricStatus::MissingFiniteSamples
    } else {
        CharTwoParametricStatus::FiniteSamplesOnly
    };

    CharTwoParametricGateReport {
        source: "characteristic-two dimension-parametric projector family gate checklist",
        status,
        finite_sample_count,
        sampled_exponents,
        sampled_dimensions,
        checked_obligations: checked,
        missing_obligations: missing,
        rejected_escalations: if status == CharTwoParametricStatus::DeclaredObligationsComplete {
            vec![
                "declared checklist completeness does not constitute verified mathematical proof of missing theorems",
            ]
        } else {
            vec![
                "sampled characteristic-two controls do not prove a theorem for every exponent",
                "finite CODA-MUR ledgers do not close a dimension-parametric loss ledger",
                "a prime-power family still does not settle composite MUB(6) or MUB(10)",
            ]
        },
        boundary: if status == CharTwoParametricStatus::DeclaredObligationsComplete {
            "characteristic-two checklist complete: declared obligations satisfied, but unverified external proof artifacts are not checked"
        } else {
            "finite characteristic-two samples remain non-parametric; no all-2^k family authority is accepted"
        },
        error: if status == CharTwoParametricStatus::DeclaredObligationsComplete {
            None
        } else {
            Some("missing characteristic-two parametric family obligations".to_string())
        },
    }
}

fn push_obligation(
    present: bool,
    obligation: &'static str,
    checked: &mut Vec<&'static str>,
    missing: &mut Vec<&'static str>,
) {
    if present {
        checked.push(obligation);
    } else {
        missing.push(obligation);
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn char_two_parametric_gate_rejects_finite_sample_extrapolation() {
        let report = verify_current_char_two_parametric_gate();
        assert_eq!(report.status, CharTwoParametricStatus::FiniteSamplesOnly);
        assert!(report.sampled_dimensions.contains(&8));
        assert!(report
            .missing_obligations
            .iter()
            .any(|obligation| obligation.contains("GF(2^k)")));
        assert!(report
            .missing_obligations
            .iter()
            .any(|obligation| obligation.contains("CODA-MUR loss ledger")));
        assert!(report
            .rejected_escalations
            .iter()
            .any(|item| item.contains("sampled characteristic-two controls")));
    }

    #[test]
    fn char_two_parametric_gate_accepts_only_complete_family_obligations() {
        let report = verify_char_two_parametric_gate(CharTwoParametricInputs {
            finite_controls: verify_current_finite_projector_controls(),
            binary_field_family: true,
            irreducible_modulus_family: true,
            symplectic_spread_family: true,
            board_incidence_family: true,
            spectral_projector_lift_family: true,
            pauli_phase_family: true,
            positive_projector_family: true,
            hilbert_transport_family: true,
            gtmur_loss_ledger_family: true,
            terminalizer_preserved_family: true,
        });
        assert_eq!(
            report.status,
            CharTwoParametricStatus::DeclaredObligationsComplete
        );
        assert!(report.missing_obligations.is_empty());
        assert!(report.error.is_none());
    }
}
