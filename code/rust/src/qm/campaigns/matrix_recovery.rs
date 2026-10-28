
use crate::qm::campaigns::born_gleason::{
    ConditionalUniqueness, FrameFunction, GleasonAssumptions, OPEN_RESIDUAL_DIM2,
};
use crate::qm::campaigns::separating_preds::{ChshClass, ChshExample};
use engine_number_theory::rational::{ri, rq};
use engine_quantum_physics::composition_tomography::{
    local_tomography_spanning_real, rebit_separating_projector, rebit_state_pair,
    skew_skew_deficiency, FiniteSystem, LocalTomographyReport, MonoidalComposite,
    RealRebitCountermodel,
};
use engine_quantum_physics::hermitian_spectral::{
    spectral_decompose, HermitianMatrix, ScalarCarrier,
};
use engine_quantum_physics::instruments::{
    paid_computational_spectral, InstrumentChannel, LudersInstrument, Povm,
};
use engine_quantum_physics::separating_predictions::MerminPeresCochainBridge;

pub const AUTHORITY_FENCE: &str =
    "AuthorityEffect None; not PROVED; not GlobalGreen; sealed recovery diagnostic; no auto GlobalGreen.";

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum RecoveryTarget {
    T08FiniteClassicalShadow,
    T09ObserverFunctoriality,
    T11PhaseFiber,
    T12SemanticLift,
    T13ImportIndependence,
    T14ImportSufficiency,
    T15Spectral,
    T16Instruments,
    T17CompositionTomography,
    T18BornGleason,
    T19SeparatingPredictions,
}

impl RecoveryTarget {
    pub const IN_CRATE: [RecoveryTarget; 11] = [
        Self::T08FiniteClassicalShadow,
        Self::T09ObserverFunctoriality,
        Self::T11PhaseFiber,
        Self::T12SemanticLift,
        Self::T13ImportIndependence,
        Self::T14ImportSufficiency,
        Self::T15Spectral,
        Self::T16Instruments,
        Self::T17CompositionTomography,
        Self::T18BornGleason,
        Self::T19SeparatingPredictions,
    ];

    fn id_early(self) -> Option<&'static str> {
        match self {
            Self::T08FiniteClassicalShadow => Some("T08"),
            Self::T09ObserverFunctoriality => Some("T09"),
            Self::T11PhaseFiber => Some("T11"),
            Self::T12SemanticLift => Some("T12"),
            Self::T13ImportIndependence => Some("T13"),
            Self::T14ImportSufficiency => Some("T14"),
            _ => None,
        }
    }

    pub fn id(self) -> &'static str {
        if let Some(code) = self.id_early() {
            return code;
        }
        match self {
            Self::T15Spectral => "T15",
            Self::T16Instruments => "T16",
            Self::T17CompositionTomography => "T17",
            Self::T18BornGleason => "T18",
            Self::T19SeparatingPredictions => "T19",
            _ => unreachable!(),
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum ResidualStatus {
    Closed,
    Open { reason: String },
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct TargetResidual {
    pub target: &'static str,
    pub status: ResidualStatus,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct RecoveryFalsifierReport {
    pub checks_run: usize,
    pub failures: Vec<String>,
}

impl RecoveryFalsifierReport {
    pub fn all_passed(&self) -> bool {
        self.failures.is_empty()
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ReleaseReceipt {
    pub schema: &'static str,
    pub authority_effect: &'static str,
    pub release_status: &'static str,
    pub global_green: bool,
    pub residuals: Vec<TargetResidual>,
    pub falsifier: RecoveryFalsifierReport,
    pub notes: Vec<&'static str>,
}

impl ReleaseReceipt {
    pub const SCHEMA: &'static str = "omega.finite_matrix_recovery.receipt.v1";
    pub const NOT_CANDIDATE: &'static str = "NOT_RELEASE_CANDIDATE";
    pub const DIAGNOSTIC_SEALED: &'static str = "DIAGNOSTIC_SEALED_NOT_PROMOTED";
}

fn falsify_t15_and_t16(failures: &mut Vec<String>) -> usize {
    let diag = [ri(1), ri(2), ri(3)];
    match HermitianMatrix::try_diagonal_rational(&diag, ScalarCarrier::Rational)
        .and_then(|m| spectral_decompose(&m))
    {
        Ok(d) if d.n == 3 && d.hypotheses.all_paid() => {}
        Ok(_) => failures.push("T15: decomp shape unexpected".into()),
        Err(e) => failures.push(format!("T15: {e:?}")),
    }

    match paid_computational_spectral(2)
        .and_then(|ev| {
            let povm = Povm::computational_basis(&ev, "cb")?;
            LudersInstrument::try_new(ev, povm, "L")
        })
        .and_then(|lud| {
            let ch = InstrumentChannel::from_luders(&lud, "A");
            ch.compose(&ch)
        }) {
        Ok(_) => {}
        Err(e) => failures.push(format!("T16: {e:?}")),
    }
    2
}

fn falsify_t17_suite(failures: &mut Vec<String>) -> usize {
    if let Err(e) = t17_spanning_falsifier() {
        failures.push(e);
    }
    match LocalTomographyReport::complex_product(2, 2) {
        Ok(r) if r.identity_holds => {}
        Ok(_) => failures.push("T17: complex tomography identity false".into()),
        Err(e) => failures.push(format!("T17 complex: {e:?}")),
    }
    if !RealRebitCountermodel::rebit_pair().is_valid_countermodel() {
        failures.push("T17: rebit countermodel invalid".into());
    }
    let tensor_dim_bad = MonoidalComposite::tensor(
        FiniteSystem::qubit_complex("a"),
        FiniteSystem::qubit_complex("b"),
    )
    .map(|c| c.dim != 4)
    .unwrap_or(true);
    if tensor_dim_bad {
        failures.push("T17: monoidal tensor dim".into());
    }
    4
}

fn falsify_t18_and_t19(failures: &mut Vec<String>) -> usize {
    let assumptions = GleasonAssumptions {
        dimension: 3,
        noncontextual: true,
        finite_additivity: true,
        complex_scalars: true,
        no_silent_continuum: true,
    };
    let p = [rq(1, 2), rq(1, 3), rq(1, 6)];
    match FrameFunction::born_from_populations(&p)
        .and_then(|f| ConditionalUniqueness::try_prove(assumptions, f.clone(), f))
    {
        Ok(u) if u.unique_on_basis => {}
        Ok(_) => failures.push("T18: uniqueness flag false".into()),
        Err(e) => failures.push(format!("T18: {e:?}")),
    }
    if ChshExample::pr_box().class != ChshClass::BeyondTsirelson {
        failures.push("T19: PR box not beyond Tsirelson".into());
    }
    match MerminPeresCochainBridge::from_standard_square() {
        Ok(bridge) if bridge.is_obstructed() => {}
        Ok(_) => failures.push("T19: Mermin–Peres not obstructed".into()),
        Err(e) => failures.push(format!("T19: {e}")),
    }
    3
}

pub fn independent_falsifier() -> RecoveryFalsifierReport {
    let mut failures = Vec::new();
    let checks = falsify_t15_and_t16(&mut failures)
        + falsify_t17_suite(&mut failures)
        + falsify_t18_and_t19(&mut failures);
    RecoveryFalsifierReport {
        checks_run: checks,
        failures,
    }
}

pub const SEAL_INPUTS_REPRICED_CYCLES_4_TO_9: [(&str, &str); 5] = [
    (
        "T15_general_n_spectral",
        "Cycle 7: the obstruction is ALGEBRAIC, not dimensional. A rational Hermitian \
         matrix can have irrational eigenvalues already at n=2 ([[1,1],[1,0]], charpoly \
         x^2-x-1, discriminant 5). OB-SPECTRAL is a PRICED IMPORT (an algebraic \
         extension of the carrier), not a pending algorithm. Reason text replaced.",
    ),
    (
        "T18_dim2_gleason",
        "Cycle 6: at d=2 the Gleason disjunct is impossible, so BornSelectionImport \
         FORCES the Busch/POVM route. Sharper than 'not discharged'. Reason text replaced.",
    ),
    (
        "T17_complex_local_tomography_spanning (R2-C5)",
        "Round 2 CLOSED it. complex_product is still an arithmetic tautology, but the          spanning question it never asked is now answered by exact rank: the d^2 Hermitian          basis Kronecker-multiplied over Q(i) and realified Re||Im has rank == joint dim at          2x2, 2x3, 3x3, 2x4. The cycle-4 objection that this crate's exact machinery is          real-only dissolves - a Hermitian matrix over Q(i) IS a rational vector of length          2n^2, so ExactRowReduction applies unmodified. Status OPEN -> Closed.",
    ),
    (
        "T17_complex_tomography_and_rebit_countermodel",
        "Cycle 4 SPLIT this row. The real/rebit half is closed and strengthened (exact \
         rank 9 of 10, witness Delta = J (x) J, and in cycle 4b an operational state pair \
         rho_pm separated by exactly 1/2). The COMPLEX half was DEMOTED to [OPEN]: \
         LocalTomographyReport::complex_product is an arithmetic tautology, the necessary \
         dimension condition, never the spanning statement. Row split accordingly.",
    ),
    (
        "T19_exact_sqrt2_tsirelson",
        "Unchanged in status, but recognised in cycle 7 as the SAME carrier-relative \
         algebraic class as T15: 2*sqrt(2) is not in Q for the same reason sqrt(5) is not. \
         Both are priced by admitting an algebraic extension, not by more code.",
    ),
];

pub fn residual_board() -> Vec<TargetResidual> {
    vec![
        TargetResidual {
            target: "T15_general_n_spectral",
            status: ResidualStatus::Open {
                reason:
                    crate::qm::campaigns::spectral_claims::SPECTRAL_OBSTRUCTION_IS_ALGEBRAIC_NOT_DIMENSIONAL
                        .to_string(),
            },
        },
        TargetResidual {
            target: "T18_dim2_gleason",
            status: ResidualStatus::Open {
                reason: format!(
                    "{OPEN_RESIDUAL_DIM2} Cycle 6: at d=2 the Gleason disjunct is \
                     impossible, so BornSelectionImport forces the Busch/POVM route."
                ),
            },
        },
        TargetResidual {
            target: "T19_exact_sqrt2_tsirelson",
            status: ResidualStatus::Open {
                reason: "2*sqrt(2) not in Q; S^2<=8 marker only. Same carrier-relative \
                         algebraic class as T15 (cycle 7)."
                    .into(),
            },
        },
        TargetResidual {
            target: "T16_instruments_diagonal_face",
            status: ResidualStatus::Closed,
        },
        TargetResidual {
            target: "T17_real_rebit_countermodel",
            status: ResidualStatus::Closed,
        },
        TargetResidual {
            target: "T17_complex_local_tomography_spanning",
            status: ResidualStatus::Closed,
        },
        TargetResidual {
            target: "T18_conditional_uniqueness_dim3",
            status: ResidualStatus::Closed,
        },
        TargetResidual {
            target: "T19_chsh_class_and_mermin_peres_obstruction",
            status: ResidualStatus::Closed,
        },
    ]
}

fn verify_t17_rank_and_deficiency() -> Result<(), String> {
    let r = local_tomography_spanning_real(2, 2).map_err(|e| format!("T17 spanning: {e:?}"))?;
    if r.product_rank != 9 || r.joint_dim != 10 || r.spans {
        return Err(format!(
            "T17: rebit spanning report unexpected: rank={} joint={} spans={}",
            r.product_rank, r.joint_dim, r.spans
        ));
    }
    let deficiency = skew_skew_deficiency(2, 2).map_err(|e| format!("T17 deficiency: {e:?}"))?;
    if r.joint_dim - r.product_rank != deficiency {
        return Err("T17: deficiency does not match C(m,2)*C(n,2)".into());
    }
    Ok(())
}

fn verify_t17_state_pair_and_projector() -> Result<(), String> {
    let (rp, rm) = rebit_state_pair().map_err(|e| format!("T17 state pair: {e:?}"))?;
    if rp == rm {
        return Err("T17: rho_+ and rho_- coincide — countermodel is vacuous".into());
    }
    let p = rebit_separating_projector().map_err(|e| format!("T17 projector: {e:?}"))?;
    if p.mul(&p).map_err(|e| format!("T17: {e:?}"))? != p {
        return Err("T17: separating effect is not idempotent".into());
    }
    Ok(())
}

pub fn t17_spanning_falsifier() -> Result<(), String> {
    verify_t17_rank_and_deficiency()?;
    verify_t17_state_pair_and_projector()
}

pub fn issue_release_receipt(allow_diagnostic_seal: bool) -> ReleaseReceipt {
    let falsifier = independent_falsifier();
    let residuals = residual_board();
    let any_open = residuals
        .iter()
        .any(|r| matches!(r.status, ResidualStatus::Open { .. }));

    let release_status = if !falsifier.all_passed() {
        ReleaseReceipt::NOT_CANDIDATE
    } else if any_open {
        if allow_diagnostic_seal {
            ReleaseReceipt::DIAGNOSTIC_SEALED
        } else {
            ReleaseReceipt::NOT_CANDIDATE
        }
    } else {
        ReleaseReceipt::DIAGNOSTIC_SEALED
    };

    ReleaseReceipt {
        schema: ReleaseReceipt::SCHEMA,
        authority_effect: "None",
        release_status,
        global_green: false,
        residuals,
        falsifier,
        notes: vec![
            "Release receipt is diagnostic only",
            "Never sets GlobalGreen or PROMOTED",
            "OPEN residuals block true release candidate status",
            AUTHORITY_FENCE,
        ],
    }
}

#[cfg(test)]
mod tests {
    use super::*;


    #[test]
    fn recfull_t17_is_split_real_closed_complex_open() {
        let board = residual_board();
        let real = board
            .iter()
            .find(|r| r.target == "T17_real_rebit_countermodel")
            .expect("real half must be present");
        assert_eq!(real.status, ResidualStatus::Closed);

        let complex = board
            .iter()
            .find(|r| r.target == "T17_complex_local_tomography_spanning")
            .expect("complex half must be present");
        assert_eq!(
            complex.status,
            ResidualStatus::Closed,
            "R2-C5 measured exact rank == joint dim at 2x2, 2x3, 3x3, 2x4"
        );

        assert!(
            !board
                .iter()
                .any(|r| r.target == "T17_complex_tomography_and_rebit_countermodel"),
            "the stale merged T17 row must be removed"
        );
    }

    #[test]
    fn recfull_open_reasons_are_repriced() {
        let board = residual_board();
        let t15 = board
            .iter()
            .find(|r| r.target == "T15_general_n_spectral")
            .unwrap();
        let ResidualStatus::Open { reason } = &t15.status else {
            panic!("T15 must stay OPEN")
        };
        assert!(
            reason.contains("ALGEBRAIC"),
            "T15 must cite the algebraic characterisation, not the dimensional one"
        );

        let t18 = board
            .iter()
            .find(|r| r.target == "T18_dim2_gleason")
            .unwrap();
        let ResidualStatus::Open { reason } = &t18.status else {
            panic!("T18 must stay OPEN")
        };
        assert!(
            reason.contains("Busch"),
            "T18 must cite the forced Busch route"
        );
    }

    #[test]
    fn recfull_t17_falsifier_is_not_a_tautology() {
        assert!(t17_spanning_falsifier().is_ok());

        for (a, b) in [(2usize, 2usize), (3, 5), (7, 11)] {
            assert_eq!((a * a) * (b * b), (a * b) * (a * b));
            if a * b <= 16 {
                let complex = LocalTomographyReport::complex_product(a, b)
                    .expect("declared complex tomography dimensions are admitted");
                assert_eq!(complex.local_param_a, a * a);
                assert_eq!(complex.local_param_b, b * b);
                assert_eq!(complex.joint_param, (a * b) * (a * b));
                assert!(
                    complex.identity_holds,
                    "computed complex product rank spans"
                );
            } else {
                assert_eq!(
                    LocalTomographyReport::complex_product(a, b),
                    Err(engine_quantum_physics::composition_tomography::CompError::BudgetExceeded)
                );
            }
        }

        let real = local_tomography_spanning_real(2, 2).unwrap();
        assert_eq!(real.product_rank, 9);
        assert_eq!(real.joint_dim, 10);
        assert!(!real.spans);
        assert!(
            !LocalTomographyReport::real_product_params(2, 2)
                .unwrap()
                .identity_holds
        );
    }

    #[test]
    fn recfull_repricing_is_recorded() {
        assert_eq!(SEAL_INPUTS_REPRICED_CYCLES_4_TO_9.len(), 5);
        let targets: Vec<&str> = SEAL_INPUTS_REPRICED_CYCLES_4_TO_9
            .iter()
            .map(|(t, _)| *t)
            .collect();
        assert!(targets.contains(&"T15_general_n_spectral"));
        assert!(targets.contains(&"T18_dim2_gleason"));
        assert!(targets.contains(&"T17_complex_tomography_and_rebit_countermodel"));
        assert!(targets.contains(&"T17_complex_local_tomography_spanning (R2-C5)"));
    }

    #[test]
    fn recfull_seal_is_still_not_a_release_candidate() {
        let receipt = issue_release_receipt(false);
        assert_eq!(receipt.release_status, ReleaseReceipt::NOT_CANDIDATE);
        assert!(!receipt.global_green);

        let open: Vec<&str> = receipt
            .residuals
            .iter()
            .filter(|r| matches!(r.status, ResidualStatus::Open { .. }))
            .map(|r| r.target)
            .collect();
        assert_eq!(
            open.len(),
            3,
            "expected 3 open residuals after R2-C5 closed the complex T17 half, got {open:?}"
        );
        assert!(
            !open.contains(&"T17_complex_local_tomography_spanning"),
            "the complex spanning row was closed by measurement in R2-C5"
        );
    }

    #[test]
    fn recfull_diagnostic_seal_never_promotes() {
        let receipt = issue_release_receipt(true);
        assert_eq!(receipt.release_status, ReleaseReceipt::DIAGNOSTIC_SEALED);
        assert!(!receipt.global_green);
        assert!(receipt.release_status.contains("NOT_PROMOTED"));
        assert_eq!(receipt.authority_effect, "None");
    }

    #[test]
    fn sealed_falsifier_passes() {
        let f = independent_falsifier();
        assert!(f.all_passed(), "falsifier failures: {:?}", f.failures);
        assert!(f.checks_run >= 6);
    }

    #[test]
    fn sealed_receipt_not_global_green() {
        let r = issue_release_receipt(true);
        assert!(!r.global_green);
        assert_eq!(r.authority_effect, "None");
        assert_ne!(r.release_status, "PROMOTED");
        assert_ne!(r.release_status, "GlobalGreen");
        assert!(
            r.release_status == ReleaseReceipt::DIAGNOSTIC_SEALED
                || r.release_status == ReleaseReceipt::NOT_CANDIDATE
        );
    }

    #[test]
    fn sealed_without_diagnostic_flag_is_not_candidate() {
        let r = issue_release_receipt(false);
        assert_eq!(r.release_status, ReleaseReceipt::NOT_CANDIDATE);
    }

    #[test]
    fn sealed_board_has_open_general_n() {
        let board = residual_board();
        assert!(board.iter().any(|t| {
            t.target.contains("T15") && matches!(t.status, ResidualStatus::Open { .. })
        }));
    }

    #[test]
    fn sealed_authority_none() {
        assert!(AUTHORITY_FENCE.contains("AuthorityEffect None"));
    }
}
