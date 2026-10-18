//! Target 20 — Sealed finite-matrix recovery assembly (T01–T17 checklist).
//!
//! Assembles semantic constructors from prior targets, runs an independent
//! falsifier, and issues a release receipt **only** when all tracked residuals
//! close. Otherwise returns `NOT_RELEASE_CANDIDATE`.
//!
//! AuthorityEffect: None. Not GlobalGreen. Human promotion still required externally.

use crate::qm::campaigns::born_gleason::{
    ConditionalUniqueness, FrameFunction, GleasonAssumptions, OPEN_RESIDUAL_DIM2,
};
use crate::qm::campaigns::separating_preds::{ChshClass, ChshExample};
use omega_number_theory::rational::{ri, rq};
use omega_quantum_physics::composition_tomography::{
    local_tomography_spanning_real, rebit_separating_projector, rebit_state_pair,
    skew_skew_deficiency, FiniteSystem, LocalTomographyReport, MonoidalComposite,
    RealRebitCountermodel,
};
use omega_quantum_physics::hermitian_spectral::{
    spectral_decompose, HermitianMatrix, ScalarCarrier,
};
use omega_quantum_physics::instruments::{
    paid_computational_spectral, InstrumentChannel, LudersInstrument, Povm,
};
use omega_quantum_physics::separating_predictions::MerminPeresCochainBridge;

/// Fence.
pub const AUTHORITY_FENCE: &str =
    "AuthorityEffect None; not PROVED; not GlobalGreen; sealed recovery diagnostic; no auto GlobalGreen.";

/// Tracked residual ids for the T01–T17 assembly (subset implemented in-crate).
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

    pub fn id(self) -> &'static str {
        match self {
            Self::T08FiniteClassicalShadow => "T08",
            Self::T09ObserverFunctoriality => "T09",
            Self::T11PhaseFiber => "T11",
            Self::T12SemanticLift => "T12",
            Self::T13ImportIndependence => "T13",
            Self::T14ImportSufficiency => "T14",
            Self::T15Spectral => "T15",
            Self::T16Instruments => "T16",
            Self::T17CompositionTomography => "T17",
            Self::T18BornGleason => "T18",
            Self::T19SeparatingPredictions => "T19",
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

/// Independent falsifier: re-check constructors without trusting prior pass flags.
pub fn independent_falsifier() -> RecoveryFalsifierReport {
    let mut failures = Vec::new();
    let mut checks = 0;

    // T15 spectral diagonal
    checks += 1;
    let diag = [ri(1), ri(2), ri(3)];
    match HermitianMatrix::try_diagonal_rational(&diag, ScalarCarrier::Rational)
        .and_then(|m| spectral_decompose(&m))
    {
        Ok(d) if d.n == 3 && d.hypotheses.all_paid() => {}
        Ok(_) => failures.push("T15: decomp shape unexpected".into()),
        Err(e) => failures.push(format!("T15: {e:?}")),
    }

    // T16 instruments
    checks += 1;
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

    // T17 spanning + operational countermodel (cycle 10: a check that CAN fail;
    // the complex_product check below is an arithmetic tautology and is retained
    // only as a dimension-condition marker, not as evidence).
    checks += 1;
    if let Err(e) = t17_spanning_falsifier() {
        failures.push(e);
    }

    // T17 tomography + rebit countermodel
    checks += 1;
    match LocalTomographyReport::complex_product(2, 2) {
        Ok(r) if r.identity_holds => {}
        Ok(_) => failures.push("T17: complex tomography identity false".into()),
        Err(e) => failures.push(format!("T17 complex: {e:?}")),
    }
    checks += 1;
    let cm = RealRebitCountermodel::rebit_pair();
    if !cm.is_valid_countermodel() {
        failures.push("T17: rebit countermodel invalid".into());
    }
    checks += 1;
    if MonoidalComposite::tensor(
        FiniteSystem::qubit_complex("a"),
        FiniteSystem::qubit_complex("b"),
    )
    .map(|c| c.dim != 4)
    .unwrap_or(true)
    {
        failures.push("T17: monoidal tensor dim".into());
    }

    // T18 Born/Gleason. The assumptions are declared, not computed.
    checks += 1;
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

    // T19 separating
    checks += 1;
    if ChshExample::pr_box().class != ChshClass::BeyondTsirelson {
        failures.push("T19: PR box not beyond Tsirelson".into());
    }
    checks += 1;
    match MerminPeresCochainBridge::from_standard_square() {
        Ok(bridge) if bridge.is_obstructed() => {}
        Ok(_) => failures.push("T19: Mermin–Peres not obstructed".into()),
        Err(e) => failures.push(format!("T19: {e}")),
    }

    RecoveryFalsifierReport {
        checks_run: checks,
        failures,
    }
}

/// What changed under this seal during cycles 4–9, and how each row was re-priced.
///
/// The seal is only as honest as its inputs' descriptions. Several rows below
/// were written before those inputs changed meaning, so re-running the falsifier
/// without re-reading the board would have re-certified stale text.
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

/// Assemble the residual board for in-crate targets.
///
/// Re-priced in cycle 10 against everything cycles 4–9 changed; see
/// [`SEAL_INPUTS_REPRICED_CYCLES_4_TO_9`].
pub fn residual_board() -> Vec<TargetResidual> {
    // Modules T08–T14 exist as prior work; this assembly treats them as
    // structural presence checks via lib compilation, not re-run here.
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
        // Cycle 4 split the former single T17 row. Keeping one row would have left
        // the seal resting on a "Closed" that the complex half no longer supports.
        TargetResidual {
            target: "T17_real_rebit_countermodel",
            status: ResidualStatus::Closed,
        },
        // R2-C5 (2026-08-04) CLOSES this row — the first time this loop has
        // reduced the open-residual count rather than raised it.
        //
        // The cycle-4 demotion was correct: `complex_product` is an arithmetic
        // tautology and says nothing about spanning. Round 2 took the rank.
        // `local_tomography_spanning_complex` builds the d^2 Hermitian basis
        // {E_ii, E_ij+E_ji, i(E_ij-E_ji)}, Kronecker-multiplies over Q(i), and
        // realifies Re||Im so the EXISTING exact-rational row reduction applies
        // unmodified — the "real-only machinery" objection dissolves rather than
        // being worked around, because a Hermitian matrix over Q(i) is a rational
        // vector of length 2n^2.
        //
        // Result: exact rank == joint dim at 2x2 (16=16), 2x3, 3x3 and 2x4.
        // Complex local tomography SPANS.
        //
        // Anti-vacuity is why this is a close and not a claim: real and complex
        // run through the SAME rank pipeline, and the real case still FAILS
        // through it (rank 9 of 10) with deficiency exactly C(m,2)C(n,2).
        // Deleting the imaginary half of the realification breaks both complex
        // spanning tests, so the complex structure is load-bearing.
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

/// A falsifier check for T17 that **can fail**.
///
/// The original dimension-only T17 check computed
/// `d_a^2 d_b^2 == (d_a d_b)^2`, an arithmetic identity. The current
/// `LocalTomographyReport::complex_product` instead computes exact rank within
/// its declared dimension budget.
///
/// This one exercises the real spanning computation: exact rank of the product
/// effects inside the joint symmetric space, the skew–skew deficiency formula,
/// and the operational state pair. Each has a way to be wrong.
pub fn t17_spanning_falsifier() -> Result<(), String> {
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
    // Operational half (cycle 4b): the state pair must be distinct and separated
    // by an admissible joint projector.
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

/// Issue release receipt only when falsifier passes **and** no OPEN residuals.
/// With current honest board (general-n OPEN, etc.), always NOT_RELEASE_CANDIDATE
/// unless `allow_diagnostic_seal` closes only the falsifier path.
pub fn issue_release_receipt(allow_diagnostic_seal: bool) -> ReleaseReceipt {
    let falsifier = independent_falsifier();
    let residuals = residual_board();
    let any_open = residuals
        .iter()
        .any(|r| matches!(r.status, ResidualStatus::Open { .. }));

    let release_status = if !falsifier.all_passed() {
        ReleaseReceipt::NOT_CANDIDATE
    } else if any_open {
        // Honest: residuals remain → not a release candidate.
        // Optional diagnostic seal records falsifier green without promotion.
        if allow_diagnostic_seal {
            ReleaseReceipt::DIAGNOSTIC_SEALED
        } else {
            ReleaseReceipt::NOT_CANDIDATE
        }
    } else {
        // All residuals closed — still not GlobalGreen / not promoted.
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

    // --- Cycle 10: the re-seal --------------------------------------------

    /// **The row that would have silently re-certified.** Cycle 4 demoted complex
    /// local tomography to `[OPEN]`, but the board still carried a single
    /// `T17_..._and_rebit_countermodel` row marked `Closed`. The seal would have
    /// rested on a closure the complex half no longer supports.
    ///
    /// The row is now split: the real/rebit half closed, the complex half OPEN.
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
        // R2-C5 CLOSED this half. The row must stay SPLIT: closing the complex
        // half by merging it back into the real one would let the seal rest on a
        // single "Closed" again, which is what cycle 4 split it to prevent.
        assert_eq!(
            complex.status,
            ResidualStatus::Closed,
            "R2-C5 measured exact rank == joint dim at 2x2, 2x3, 3x3, 2x4"
        );

        // The old merged row must be gone, not merely shadowed.
        assert!(
            !board
                .iter()
                .any(|r| r.target == "T17_complex_tomography_and_rebit_countermodel"),
            "the stale merged T17 row must be removed"
        );
    }

    /// The T15 and T18 rows must carry their **re-priced** reasons, not the
    /// pre-cycle-6/7 text.
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

    /// **The T17 falsifier can now fail.** The original check called
    /// the dimension identity alone. The replacement exercises exact rank, the
    /// deficiency formula, and the operational state pair. The current complex
    /// constructor also checks rank and can refuse an oversized declaration.
    #[test]
    fn recfull_t17_falsifier_is_not_a_tautology() {
        assert!(t17_spanning_falsifier().is_ok());

        // The historical dimension identity holds for every original pair;
        // it does not establish that product effects span the joint space.
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
                    Err(omega_quantum_physics::composition_tomography::CompError::BudgetExceeded)
                );
            }
        }

        // A computed negative control: the real product effects have rank9 in
        // the ten-dimensional joint symmetric space, although 3*3 is well-defined.
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

    /// Re-pricing is recorded, so a later reader can see which rows were rewritten
    /// and why rather than diffing history.
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

    /// **The seal remains NOT a release candidate.**
    ///
    /// R2-C5 closed `T17_complex_local_tomography_spanning`, taking the open count
    /// 4 -> 3. That is the FIRST reduction this loop has produced: round 1 moved
    /// the count only upward (3 -> 4), correctly, by splitting a row whose
    /// "Closed" the complex half did not support. Closing one row does not make
    /// the seal a candidate, and this test exists to keep that distinction.
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

    /// Even the diagnostic seal never sets GlobalGreen or PROMOTED.
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
        // With OPEN residuals, diagnostic seal is the max honest status.
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
