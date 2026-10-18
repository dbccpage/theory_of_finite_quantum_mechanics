//! Corrected d=10 canonical-triple wall status.
//!
//! This records the reproducible d=10 wall-value/stabilizer evidence without
//! promoting it to a complete MUB(10) existence or nonexistence theorem. The
//! authority boundary is deliberately narrower: high-precision critical value,
//! PSLQ-miss evidence, and full single-qudit Clifford stabilizer census.
//!
//! The census, the f64 wall comparison and every status derived from them are
//! computed by [`crate::omega_native::d10_gtfoc_cross_validation`]. The dps=460
//! critical value, the Noah anchor and the PSLQ search come from high-precision
//! scripts that are not in this repository. They are reported under
//! [`D10RecordedHighPrecisionEvidence`] and never counted as discharged here.

use crate::omega_native::float_check::d10_gtfoc_cross_validation::{
    d10_gtfoc_cross_validation_report, D10GtfocCrossValidationReport, MatchStatus,
};
use serde::Serialize;

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Serialize)]
pub enum D10WallValueStatus {
    CriticalValueReproduced,
    CriticalValueMismatch,
    NotChecked,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Serialize)]
pub enum D10StabilizerStatus {
    Z2AntiunitaryInvolution,
    TrivialStabilizerRefuted,
    CensusMismatch,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Serialize)]
pub enum D10ClosedFormStatus {
    OpenAfterZ2RealStructure,
    NoLowDegreePslqRelationFound,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Serialize)]
pub enum D10WallAuthorityStatus {
    EvidenceOnlyCriticalPoint,
    MissingGlobalWallCertificate,
}

/// Values from high-precision runs whose scripts are not in this repository.
///
/// Nothing here is recomputed. `agrees_with_f64_wall` is the one check this
/// crate can make: the recorded wall prefix against the f64 wall value, within
/// the f64 comparison tolerance.
#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct D10RecordedHighPrecisionEvidence {
    pub dps: usize,
    pub stationarity_residual: &'static str,
    pub wall_value_prefix: &'static str,
    pub noah_anchor_error: &'static str,
    pub pslq_status: D10ClosedFormStatus,
    pub scripts: Vec<&'static str>,
    pub scripts_in_repository: bool,
    pub agrees_with_f64_wall: bool,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct D10WallStatusReport {
    pub target: &'static str,
    pub value_status: D10WallValueStatus,
    pub authority_status: D10WallAuthorityStatus,
    pub f64_certified_digits: usize,
    pub stabilizer_status: D10StabilizerStatus,
    pub single_qudit_clifford_elements: usize,
    pub nontrivial_unitary_fixers: usize,
    pub antiunitary_fixers: usize,
    pub antiunitary_involutions: usize,
    pub antiunitary_generator: &'static str,
    pub antiunitary_generator_transport: MatchStatus,
    pub real_fixed_locus_dimension: usize,
    pub recorded: D10RecordedHighPrecisionEvidence,
    pub corrected_claims: Vec<String>,
    pub discharged_obligations: Vec<String>,
    pub missing_obligations: Vec<String>,
    pub computed_by: &'static str,
    pub boundary: &'static str,
}

const RECORDED_WALL_VALUE_PREFIX: &str =
    "0.977554318518754902764547046932516478532498129172001960635014";

pub fn current_d10_wall_status() -> D10WallStatusReport {
    d10_wall_status_from(d10_gtfoc_cross_validation_report())
}

/// Derives the wall status from a cross-validation report.
///
/// Every census count and status comes from `validation`; only the fields of
/// [`D10RecordedHighPrecisionEvidence`] are recorded constants.
pub fn d10_wall_status_from(validation: &D10GtfocCrossValidationReport) -> D10WallStatusReport {
    let comparison = &validation.wall_comparison;
    let value_reproduced = comparison.obstruction_matches && comparison.wall_matches;
    let scanned = validation.clifford_elements_scanned;
    let unitary = validation.unitary_fixers.computed;
    let antiunitary = validation.antiunitary_fixers.computed;
    let involutions = validation.z2_real_structure.computed;
    let z2_structure = unitary == 0 && antiunitary == 1 && involutions == 1;
    let transport = validation.named_antiunitary_transport.status;

    let recorded_wall: f64 = RECORDED_WALL_VALUE_PREFIX
        .parse()
        .expect("the recorded wall prefix is a decimal literal");
    let agrees_with_f64_wall =
        (recorded_wall - validation.wall_value).abs() <= comparison.tolerance;

    let mut corrected_claims = Vec::new();
    if unitary + antiunitary > 0 {
        corrected_claims.push(
            "the earlier trivial-stabilizer claim is refuted by the full Cl(2) tensor Cl(5) census"
                .to_string(),
        );
    }
    corrected_claims.push(format!(
        "the d=10 maximizer has {antiunitary} antiunitary Clifford fixer(s) and {unitary} nontrivial unitary fixer(s) among {scanned} scanned elements"
    ));
    corrected_claims.push(
        "the closed-form no-go remains evidence only; PSLQ misses do not prove nonexistence of a relation"
            .to_string(),
    );
    corrected_claims.push(
        "the wall value is a high-precision critical value/lower bound, not a certified global wall maximum"
            .to_string(),
    );

    let mut discharged_obligations = Vec::new();
    let mut missing_obligations = Vec::new();
    if value_reproduced {
        discharged_obligations.push(format!(
            "d=10 wall critical value reproduced by the f64 optimizer to {} digits",
            comparison.certified_digits
        ));
    } else {
        missing_obligations
            .push("f64 reproduction of the d=10 wall critical value".to_string());
    }
    discharged_obligations.push(format!(
        "full single-qudit Clifford census scanned {scanned} elements of Cl(2) tensor Cl(5)"
    ));
    if z2_structure {
        discharged_obligations.push(
            "antiunitary fixer verified as a K^2 = I involution with no nontrivial unitary fixer"
                .to_string(),
        );
    } else {
        missing_obligations.push(format!(
            "Clifford census matching the Z/2 antiunitary structure (computed: {unitary} unitary, {antiunitary} antiunitary fixers, {involutions} involutions)"
        ));
    }
    if transport == MatchStatus::Match {
        discharged_obligations.push(
            "antiunitary fixer transports to the named HXZ tensor V representative".to_string(),
        );
    } else {
        missing_obligations.push(
            "transport of the antiunitary fixer to the named HXZ tensor V representative"
                .to_string(),
        );
    }
    if agrees_with_f64_wall {
        discharged_obligations.push(format!(
            "recorded dps=460 wall prefix agrees with the f64 wall value within {:e}",
            comparison.tolerance
        ));
    } else {
        missing_obligations.push(
            "agreement between the recorded dps=460 wall prefix and the f64 wall value"
                .to_string(),
        );
    }
    missing_obligations.extend(
        [
            "in-repository reproduction of the dps=460 critical value and the Noah 50-digit anchor",
            "exact upper-bound certificate proving the d=10 critical value is the global wall",
            "closed-form derivation or exact elimination inside the Z/2 real fixed locus",
            "proof that low-degree PSLQ failure implies no closed form is forbidden; PSLQ remains evidence only",
            "complete eleven-basis MUB(10) witness or proof-carrying no-go certificate",
        ]
        .map(str::to_string),
    );

    D10WallStatusReport {
        target: "d=10 canonical triple fourth-vector wall",
        value_status: if value_reproduced {
            D10WallValueStatus::CriticalValueReproduced
        } else {
            D10WallValueStatus::CriticalValueMismatch
        },
        authority_status: if value_reproduced {
            D10WallAuthorityStatus::EvidenceOnlyCriticalPoint
        } else {
            D10WallAuthorityStatus::MissingGlobalWallCertificate
        },
        f64_certified_digits: if value_reproduced {
            comparison.certified_digits
        } else {
            0
        },
        stabilizer_status: if z2_structure {
            D10StabilizerStatus::Z2AntiunitaryInvolution
        } else {
            D10StabilizerStatus::CensusMismatch
        },
        single_qudit_clifford_elements: scanned,
        nontrivial_unitary_fixers: unitary,
        antiunitary_fixers: antiunitary,
        antiunitary_involutions: involutions,
        antiunitary_generator: "K = conjugation after (HXZ tensor V), K^2 = I",
        antiunitary_generator_transport: transport,
        real_fixed_locus_dimension: validation.real_fixed_locus_dim,
        recorded: D10RecordedHighPrecisionEvidence {
            dps: 460,
            stationarity_residual: "4.6721e-462",
            wall_value_prefix: RECORDED_WALL_VALUE_PREFIX,
            noah_anchor_error: "1.9606e-51",
            pslq_status: D10ClosedFormStatus::OpenAfterZ2RealStructure,
            scripts: vec![
                "crates/mub/mub_d10_wall/d10_phase_a.py",
                "crates/mub/mub_d10_wall/d10_full_clifford_census.py",
                "crates/mub/mub_d10_wall/d10_census_verify.py",
                "crates/mub/mub_d10_wall/d10_symmetry_characterize.py",
            ],
            scripts_in_repository: false,
            agrees_with_f64_wall,
        },
        corrected_claims,
        discharged_obligations,
        missing_obligations,
        computed_by: "omega_mub::omega_native::float_check::d10_gtfoc_cross_validation::run_d10_gtfoc_cross_validation",
        boundary: "This is a corrected d=10 canonical-triple wall evidence report. It does not authorize a MUB(10) existence or nonexistence theorem.",
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn validation() -> D10GtfocCrossValidationReport {
        d10_gtfoc_cross_validation_report().clone()
    }

    #[test]
    fn d10_wall_status_is_derived_from_the_computed_census() {
        let validation = validation();
        let report = d10_wall_status_from(&validation);

        assert_eq!(
            report.single_qudit_clifford_elements,
            validation.clifford_elements_scanned
        );
        assert_eq!(
            report.nontrivial_unitary_fixers,
            validation.unitary_fixers.computed
        );
        assert_eq!(
            report.antiunitary_fixers,
            validation.antiunitary_fixers.computed
        );
        assert_eq!(
            report.real_fixed_locus_dimension,
            validation.real_fixed_locus_dim
        );

        assert_eq!(report.single_qudit_clifford_elements, 24 * 3000);
        assert_eq!(report.nontrivial_unitary_fixers, 0);
        assert_eq!(report.antiunitary_fixers, 1);
        assert_eq!(report.antiunitary_involutions, 1);
        assert_eq!(report.real_fixed_locus_dimension, 10);
        assert_eq!(
            report.stabilizer_status,
            D10StabilizerStatus::Z2AntiunitaryInvolution
        );
        assert_eq!(
            report.value_status,
            D10WallValueStatus::CriticalValueReproduced
        );
        assert_eq!(
            report.authority_status,
            D10WallAuthorityStatus::EvidenceOnlyCriticalPoint
        );
        assert!(report
            .corrected_claims
            .iter()
            .any(|claim| claim.contains("trivial-stabilizer claim is refuted")));
        assert!(report
            .missing_obligations
            .iter()
            .any(|obligation| obligation.contains("complete eleven-basis MUB(10)")));
    }

    #[test]
    fn recorded_high_precision_evidence_is_never_discharged() {
        let report = current_d10_wall_status();

        assert!(!report.recorded.scripts_in_repository);
        assert!(report.recorded.agrees_with_f64_wall);
        assert!(report
            .discharged_obligations
            .iter()
            .all(|obligation| !obligation.contains("reproduced at dps=460")));
        assert!(report
            .missing_obligations
            .iter()
            .any(|obligation| obligation.contains("in-repository reproduction of the dps=460")));
    }

    #[test]
    fn census_mismatch_is_reported_not_masked() {
        let mut validation = validation();
        validation.unitary_fixers.computed = 1;
        let report = d10_wall_status_from(&validation);

        assert_eq!(report.stabilizer_status, D10StabilizerStatus::CensusMismatch);
        assert_eq!(report.nontrivial_unitary_fixers, 1);
        assert!(report
            .missing_obligations
            .iter()
            .any(|obligation| obligation.contains("Z/2 antiunitary structure")));
        assert!(report
            .discharged_obligations
            .iter()
            .all(|obligation| !obligation.contains("K^2 = I involution")));
    }

    #[test]
    fn wall_mismatch_downgrades_value_and_authority() {
        let mut validation = validation();
        validation.wall_comparison.wall_matches = false;
        let report = d10_wall_status_from(&validation);

        assert_eq!(report.value_status, D10WallValueStatus::CriticalValueMismatch);
        assert_eq!(
            report.authority_status,
            D10WallAuthorityStatus::MissingGlobalWallCertificate
        );
        assert_eq!(report.f64_certified_digits, 0);
    }

    #[test]
    fn recorded_prefix_disagreement_is_detected() {
        let mut validation = validation();
        validation.wall_value += 1e-6;
        let report = d10_wall_status_from(&validation);

        assert!(!report.recorded.agrees_with_f64_wall);
        assert!(report
            .missing_obligations
            .iter()
            .any(|obligation| obligation.contains("recorded dps=460 wall prefix")));
    }
}
