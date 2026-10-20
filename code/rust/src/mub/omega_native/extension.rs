
use serde::Serialize;

use omega_quantum_physics::mub::char_two_weyl_board::{CharTwoWeylBoardReport, CharTwoWeylBoardStatus};
use omega_quantum_physics::mub::composite_tensor_family_gate::{
    CompositeTensorFamilyReport, CompositeTensorFamilyStatus,
};
use omega_quantum_physics::mub::dimension_stratification::DimensionStratificationReport;
use omega_quantum_physics::mub::finite_projector_control::{
    FiniteProjectorControlReport, FiniteProjectorControlStatus,
};
use omega_quantum_physics::mub::gtmur_projector_ledger::{
    GtmurProjectorLedgerReport, GtmurProjectorLedgerStatus,
};
use omega_quantum_physics::mub::hilbert_transport::{HilbertTransportReport, HilbertTransportStatus};
use omega_quantum_physics::mub::odd_prime_gauss_certificate_gate::{
    OddPrimeGaussCertificateReport, OddPrimeGaussCertificateStatus,
};
use omega_quantum_physics::mub::odd_prime_power_controls::{
    OddPrimePowerControlReport, OddPrimePowerControlStatus,
};
use omega_quantum_physics::mub::odd_prime_power_parametric_gate::{
    OddPrimePowerParametricGateReport, OddPrimePowerParametricStatus,
};
use omega_quantum_physics::mub::odd_prime_power_weyl::{OddPrimePowerWeylReport, OddPrimePowerWeylStatus};
use omega_quantum_physics::mub::odd_prime_weyl::{OddPrimeWeylReport, OddPrimeWeylStatus};
use omega_quantum_physics::mub::prime_controls::{BenchmarkStatus, PrimeControlReport};
use omega_quantum_physics::mub::prime_power_gtmur_boundary::{
    PrimePowerGtmurBoundaryReport, PrimePowerGtmurBoundaryStatus,
};
use omega_quantum_physics::mub::projector_algebra::{ProjectorAlgebraReport, ProjectorAlgebraStatus};
use omega_quantum_physics::mub::spectral_lift::{SpectralLiftReport, SpectralLiftStatus};

use crate::omega_native::exact::char_two_parametric_gate::{
    CharTwoParametricGateReport, CharTwoParametricStatus,
};

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Serialize)]
pub enum ExtensionTarget {
    FullMub6,
    Mub10,
    GeneralMubN,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Serialize)]
pub enum ExtensionTerminal {
    ExactObstruction,
    MissingProofObligation,
    TypedRefusal,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct ExtensionVerdict {
    pub target: ExtensionTarget,
    pub terminal: ExtensionTerminal,
    pub obstruction: &'static str,
    pub discharged_obligations: Vec<&'static str>,
    pub missing_obligations: Vec<&'static str>,
    pub claim_boundary: &'static str,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct FullMub6Census {
    pub upper_bound_replayed: bool,
    pub local_transport_checked: bool,
    pub product_lower_control_verified: bool,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Mub10Census {
    pub cyclotomic120_lower_control_verified: bool,
}

pub struct GeneralMubEvidence<'a> {
    pub dimension_stratification: &'a [DimensionStratificationReport],
    pub composite_tensor_family: &'a CompositeTensorFamilyReport,
    pub prime_controls: &'a [PrimeControlReport],
    pub odd_prime_gauss_certificates: &'a OddPrimeGaussCertificateReport,
    pub odd_prime_weyl_schemas: &'a [OddPrimeWeylReport],
    pub odd_prime_power_weyl_schemas: &'a [OddPrimePowerWeylReport],
    pub odd_prime_power_controls: &'a [OddPrimePowerControlReport],
    pub odd_prime_power_parametric_gate: &'a OddPrimePowerParametricGateReport,
    pub char_two_weyl_board_schemas: &'a [CharTwoWeylBoardReport],
    pub spectral_lift_schemas: &'a [SpectralLiftReport],
    pub projector_algebra_schemas: &'a [ProjectorAlgebraReport],
    pub hilbert_transport_schemas: &'a [HilbertTransportReport],
    pub gtmur_projector_ledgers: &'a [GtmurProjectorLedgerReport],
    pub finite_projector_controls: &'a [FiniteProjectorControlReport],
    pub char_two_parametric_gate: &'a CharTwoParametricGateReport,
    pub prime_power_gtmur_boundary: &'a PrimePowerGtmurBoundaryReport,
}

const FULL_MUB6_OPEN_OBLIGATIONS: [&str; 3] = [
    "exhaustive cover or classification of admissible MUB(6) triples",
    "certified transport from every covered triple class into a wall-certified lane",
    "basis-gluing theorem upgrading fourth-vector obstruction to complete-set nonexistence",
];

pub fn assess_full_mub6(census: &FullMub6Census) -> ExtensionVerdict {
    let mut discharged = Vec::new();
    let mut missing = Vec::new();
    if census.product_lower_control_verified {
        discharged.push("exact d=6 tensor-product three-MUB lower-control verified");
    }
    if census.upper_bound_replayed {
        discharged.push("local replay of the d=6 loaded Q and PSD witness artifacts");
    } else {
        missing.push("local replay of the d=6 loaded Q and PSD witness artifacts");
    }
    if census.local_transport_checked {
        discharged.push("deterministic transport closure inside the pinned H-symmetry certificate lane is receipt-checked");
    } else {
        missing.push("receipt check for deterministic transport inside the pinned H-symmetry certificate lane");
    }
    missing.extend(FULL_MUB6_OPEN_OBLIGATIONS);
    ExtensionVerdict {
        target: ExtensionTarget::FullMub6,
        terminal: ExtensionTerminal::MissingProofObligation,
        obstruction: "Pinned T0 fourth-vector wall does not range over all MUB(6) triples.",
        discharged_obligations: discharged,
        missing_obligations: missing,
        claim_boundary: "No full MUB(6) solution follows from the current pinned-wall artifact.",
    }
}

pub fn attempt_full_mub6_from_pinned_t0(upper_bound_replayed: bool) -> ExtensionVerdict {
    assess_full_mub6(&FullMub6Census {
        upper_bound_replayed,
        local_transport_checked: false,
        product_lower_control_verified: false,
    })
}

pub fn assess_mub10(census: &Mub10Census) -> ExtensionVerdict {
    let mut discharged = Vec::new();
    let mut missing = Vec::new();
    if census.cyclotomic120_lower_control_verified {
        discharged.push(
            "exact Q(zeta_120) lower-control field with three tensor-product MUBs in d=10 verified",
        );
    } else {
        missing.push("exact d=10 lower-control replay in a declared coefficient field");
    }
    missing.extend([
        "exact complete d=10 carrier and equivalence policy",
        "declared repair group and observer for the complete eleven-basis target",
        "exact complete MUB(10) witness or no-go certificate with independent replay",
        "separation of numerical discovery from proof path",
    ]);
    ExtensionVerdict {
        target: ExtensionTarget::Mub10,
        terminal: ExtensionTerminal::MissingProofObligation,
        obstruction: "The exact d=10 tensor lower-control is not a complete MUB(10) construction or obstruction.",
        discharged_obligations: discharged,
        missing_obligations: missing,
        claim_boundary: "No complete MUB(10) theorem is authorized.",
    }
}

pub fn attempt_mub10() -> ExtensionVerdict {
    assess_mub10(&Mub10Census {
        cyclotomic120_lower_control_verified: false,
    })
}

fn collect_stratification_and_odd_prime_obligations(
    evidence: &GeneralMubEvidence<'_>,
    discharged: &mut Vec<&'static str>,
) {
    if !evidence.dimension_stratification.is_empty() {
        discharged.push("finite dimension stratification separates supported prime-power controls from composite lower-controls");
    }
    if evidence.composite_tensor_family.status == CompositeTensorFamilyStatus::TensorFamilyVerified {
        discharged.push("composite tensor-family gate verifies the min-factor paired-basis lower-control formula and composite basis-count gaps");
    }
    if evidence.prime_controls.iter().any(|control| {
        matches!(control.dimension, 7 | 11 | 13)
            && control.status == BenchmarkStatus::ExactCompleteSet
    }) {
        discharged.push(
            "exact odd-prime Hilbert controls include d=7, d=11, and d=13 quadratic Weyl MUBs in declared cyclotomic fields",
        );
    }
    if evidence.odd_prime_gauss_certificates.status
        == OddPrimeGaussCertificateStatus::FiniteCertificatesVerified
    {
        discharged.push("finite odd-prime Gauss-certificate gate aligns declared Hilbert controls with character-sum and Gauss-norm obligations");
    }
}

fn collect_odd_prime_power_obligations(
    evidence: &GeneralMubEvidence<'_>,
    discharged: &mut Vec<&'static str>,
) {
    if evidence
        .odd_prime_weyl_schemas
        .iter()
        .any(|schema| schema.status == OddPrimeWeylStatus::ProofSchemaVerified)
    {
        discharged.push("odd-prime Weyl proof schema reduces prime-dimensional MUB controls to finite-field character obligations");
    }
    if evidence
        .odd_prime_power_weyl_schemas
        .iter()
        .any(|schema| schema.status == OddPrimePowerWeylStatus::ProofSchemaVerified)
    {
        discharged.push("odd prime-power Weyl proof schema reduces GF(p^k) MUB controls to trace and Gauss-norm obligations");
    }
    if evidence
        .odd_prime_power_controls
        .iter()
        .any(|control| control.status == OddPrimePowerControlStatus::ExactCompleteSet)
    {
        discharged.push(
            "exact odd-prime-power trace-character Hilbert controls verified in declared cyclotomic fields",
        );
    }
    if evidence.odd_prime_power_parametric_gate.status
        == OddPrimePowerParametricStatus::ParametricFamilyAccepted
    {
        discharged.push(
            "dimension-parametric odd-prime-power Hilbert/CODA-MUR family is accepted for all odd p^k prime-power dimensions",
        );
    }
}

fn collect_char_two_schema_obligations(
    evidence: &GeneralMubEvidence<'_>,
    discharged: &mut Vec<&'static str>,
) {
    if evidence
        .char_two_weyl_board_schemas
        .iter()
        .any(|schema| schema.status == CharTwoWeylBoardStatus::BoardSchemaVerified)
    {
        discharged.push("characteristic-two Weyl-board spread schema verifies GF(2^k)^2 isotropic-line incidence obligations");
    }
    if evidence
        .spectral_lift_schemas
        .iter()
        .any(|schema| schema.status == SpectralLiftStatus::LiftSchemaVerified)
    {
        discharged.push("finite-field spectral-projector lift schema reduces board sectors to rank-one projector and unbiasedness obligations");
    }
    if evidence
        .projector_algebra_schemas
        .iter()
        .any(|schema| schema.status == ProjectorAlgebraStatus::AlgebraVerified)
    {
        discharged.push("symbolic Pauli projector algebra verifies characteristic-two idempotence, rank-one trace, resolution, and unbiased trace reductions");
    }
    if evidence
        .hilbert_transport_schemas
        .iter()
        .any(|schema| schema.status == HilbertTransportStatus::TransportVerified)
    {
        discharged.push("exact finite Hilbert matrix transport verifies sampled characteristic-two projector positivity factors and rank-one resolutions");
    }
}

fn collect_char_two_projector_and_boundary_obligations(
    evidence: &GeneralMubEvidence<'_>,
    discharged: &mut Vec<&'static str>,
) {
    if evidence
        .gtmur_projector_ledgers
        .iter()
        .any(|ledger| ledger.status == GtmurProjectorLedgerStatus::FiniteLedgerClosed)
    {
        discharged.push("finite CODA-MUR projector ledger preserves sampled ZeroRel and terminalizer boundaries across board, algebra, and Hilbert representations");
    }
    if evidence.finite_projector_controls.iter().any(|control| {
        control.status == FiniteProjectorControlStatus::CompleteProjectorMubVerified
    }) {
        discharged.push("finite characteristic-two projector MUB controls verify declared prime-power dimensions without coordinate witnesses");
    }
    if evidence.char_two_parametric_gate.status == CharTwoParametricStatus::DeclaredObligationsComplete
    {
        discharged.push("dimension-parametric characteristic-two projector family is accepted for all 2^k prime-power dimensions");
    }
    if evidence.prime_power_gtmur_boundary.status == PrimePowerGtmurBoundaryStatus::BoundaryVerified
    {
        discharged.push("prime-power CODA-MUR boundary ledger separates finite-field schema authority from composite tensor lower-control gaps");
    }
}

pub fn assess_general_mub_n(evidence: &GeneralMubEvidence<'_>) -> ExtensionVerdict {
    let mut discharged = Vec::new();
    collect_stratification_and_odd_prime_obligations(evidence, &mut discharged);
    collect_odd_prime_power_obligations(evidence, &mut discharged);
    collect_char_two_schema_obligations(evidence, &mut discharged);
    collect_char_two_projector_and_boundary_obligations(evidence, &mut discharged);
    general_mub_n_refusal(discharged)
}

pub fn attempt_general_mub_n() -> ExtensionVerdict {
    general_mub_n_refusal(Vec::new())
}

fn general_mub_n_refusal(discharged: Vec<&'static str>) -> ExtensionVerdict {
    ExtensionVerdict {
        target: ExtensionTarget::GeneralMubN,
        terminal: ExtensionTerminal::TypedRefusal,
        obstruction: "No composite/all-N dimension-parametric carrier, ZeroRel, repair class, or certificate family is present.",
        discharged_obligations: discharged,
        missing_obligations: vec![
            "dimension-parametric carrier family",
            "dimension-parametric exact equality protocol",
            "accepted odd-prime-power parametric Hilbert/CODA-MUR family beyond finite d=9, d=25, d=27, and d=49 controls",
            "formal dimension-parametric positivity/Hilbert-transport theorem and CODA-MUR loss ledger for every prime-power projector schema, including characteristic two",
            "complete composite-dimension witness or no-go certificate for non-prime-power targets",
            "uniform certificate family or certified dimension stratification",
            "proof that finite benchmark obstructions transport to the claimed all-N theorem",
        ],
        claim_boundary: "General MUB(n) remains outside the current authority boundary.",
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn full_mub6_attempt_refuses_transport_from_unreplayed_pinned_wall() {
        let verdict = attempt_full_mub6_from_pinned_t0(false);
        assert_eq!(verdict.target, ExtensionTarget::FullMub6);
        assert_eq!(verdict.terminal, ExtensionTerminal::MissingProofObligation);
        assert!(verdict
            .missing_obligations
            .iter()
            .any(|obligation| obligation.contains("loaded Q")));
        assert!(verdict
            .missing_obligations
            .iter()
            .any(|obligation| obligation.contains("exhaustive cover")));
    }

    #[test]
    fn full_mub6_still_needs_cover_even_after_pinned_upper_replay() {
        let verdict = attempt_full_mub6_from_pinned_t0(true);
        assert!(!verdict
            .missing_obligations
            .iter()
            .any(|obligation| obligation.contains("loaded Q")));
        assert!(verdict
            .missing_obligations
            .iter()
            .any(|obligation| obligation.contains("pinned H-symmetry")));
        assert!(verdict
            .missing_obligations
            .iter()
            .any(|obligation| obligation.contains("basis-gluing")));
    }

    #[test]
    fn local_transport_and_lower_control_do_not_solve_full_mub6() {
        let verdict = assess_full_mub6(&FullMub6Census {
            upper_bound_replayed: true,
            local_transport_checked: true,
            product_lower_control_verified: true,
        });
        assert_eq!(verdict.terminal, ExtensionTerminal::MissingProofObligation);
        assert!(verdict
            .discharged_obligations
            .iter()
            .any(|obligation| obligation.contains("pinned H-symmetry")));
        assert!(verdict
            .discharged_obligations
            .iter()
            .any(|obligation| obligation.contains("three-MUB lower-control")));
        assert!(verdict
            .missing_obligations
            .iter()
            .any(|obligation| obligation.contains("every covered triple class")));
        assert!(verdict
            .missing_obligations
            .iter()
            .all(|obligation| !obligation.contains("not consumed")));
    }

    #[test]
    fn mub10_and_general_targets_do_not_promote_evidence_to_theorem() {
        assert_eq!(
            attempt_mub10().terminal,
            ExtensionTerminal::MissingProofObligation
        );
        let with_lower = assess_mub10(&Mub10Census {
            cyclotomic120_lower_control_verified: true,
        });
        assert_eq!(
            with_lower.terminal,
            ExtensionTerminal::MissingProofObligation
        );
        assert!(with_lower
            .discharged_obligations
            .iter()
            .any(|obligation| obligation.contains("three tensor-product")));
        assert!(with_lower
            .missing_obligations
            .iter()
            .any(|obligation| obligation.contains("complete MUB(10)")));
        let general = attempt_general_mub_n();
        assert_eq!(general.terminal, ExtensionTerminal::TypedRefusal);
        assert!(general.discharged_obligations.is_empty());
        assert!(general
            .missing_obligations
            .iter()
            .any(|obligation| obligation.contains("dimension-parametric")));
        assert!(general
            .missing_obligations
            .iter()
            .any(|obligation| obligation.contains("positivity")));
    }
}
