//! Omega-native operator ladder for attempting to escape coordinate-only MUB work.
//!
//! Each rung is a representation or comparison layer. A rung may refine the
//! search space, but it can authorize a MUB theorem only when it carries the
//! exact proof obligations needed by that layer.

use serde::Serialize;

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Serialize)]
pub enum OperatorLayer {
    CoordinateExact,
    CompositeTensorControl,
    ProjectorPolytope,
    WeylBoard,
    FiniteFieldWeylSchema,
    GtmurRepresentationTransport,
    GtorComparisonEnvelope,
    GttcContinuumShadow,
    Cyclotomic120TensorControl,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Serialize)]
pub enum AttemptTarget {
    FullMub6,
    Mub10,
    GeneralMubN,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Serialize)]
pub enum AttemptDisposition {
    Candidate,
    Discarded,
    LiveButBlocked,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Serialize)]
pub enum OperatorObstruction {
    MissingLoadedUpperReplay,
    MissingTripleClassCover,
    MissingTransportCertificate,
    MissingBasisGluing,
    MissingExactCarrier,
    MissingWitnessOrNoGoCertificate,
    RepresentationLossUnclosed,
    CompletionNonCreation,
    ContinuumNonCreation,
    NumericalOnly,
    PartialLowerControlOnly,
    ProofSchemaOnly,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct OperatorAttempt {
    pub target: AttemptTarget,
    pub layer: OperatorLayer,
    pub disposition: AttemptDisposition,
    pub operator: &'static str,
    pub preserved_structure: Vec<&'static str>,
    pub obstruction: OperatorObstruction,
    pub missing_obligations: Vec<&'static str>,
    pub discard_reason: &'static str,
}

pub fn full_mub6_operator_ladder(upper_bound_replayed: bool) -> Vec<OperatorAttempt> {
    let coordinate_obstruction = if upper_bound_replayed {
        OperatorObstruction::MissingTripleClassCover
    } else {
        OperatorObstruction::MissingLoadedUpperReplay
    };
    let coordinate_missing = if upper_bound_replayed {
        vec![
            "exhaustive classification or cover of admissible MUB(6) triples",
            "transport of the pinned wall to every covered class",
            "basis-gluing theorem from no fourth vector to no complete seven-basis set",
        ]
    } else {
        vec![
            "loaded Q artifact",
            "PSD witness artifact",
            "exhaustive classification or cover of admissible MUB(6) triples",
            "basis-gluing theorem from no fourth vector to no complete seven-basis set",
        ]
    };

    vec![
        OperatorAttempt {
            target: AttemptTarget::FullMub6,
            layer: OperatorLayer::CoordinateExact,
            disposition: AttemptDisposition::LiveButBlocked,
            operator: "exact coordinate verifier for the pinned T0 wall",
            preserved_structure: vec![
                "normalization",
                "orthonormality",
                "mutual unbiasedness for the fixed triple",
                "pinned wall functional",
            ],
            obstruction: coordinate_obstruction,
            missing_obligations: coordinate_missing,
            discard_reason: "kept as a benchmark, but insufficient as a full MUB(6) proof",
        },
        OperatorAttempt {
            target: AttemptTarget::FullMub6,
            layer: OperatorLayer::CompositeTensorControl,
            disposition: AttemptDisposition::LiveButBlocked,
            operator: "Q(zeta_24) tensor-product d=2 x d=3 lower-control",
            preserved_structure: vec![
                "exact Q(zeta_24) coefficient field",
                "orthonormality for three d=6 bases",
                "mutual unbiasedness for the three-basis lower-control",
                "composite tensor-family min-factor basis-count gate",
            ],
            obstruction: OperatorObstruction::PartialLowerControlOnly,
            missing_obligations: vec![
                "complete seven-basis MUB(6) carrier or no-go target",
                "exhaustive cover of admissible complete-set configurations",
                "basis-gluing theorem from lower-control/pinned wall to the complete target",
            ],
            discard_reason: "kept as a lower-control benchmark, but insufficient as a complete MUB(6) theorem",
        },
        OperatorAttempt {
            target: AttemptTarget::FullMub6,
            layer: OperatorLayer::ProjectorPolytope,
            disposition: AttemptDisposition::LiveButBlocked,
            operator: "centered-projector residual quotient on Herm0(6)",
            preserved_structure: vec!["ray phase quotient", "projector overlaps", "pinned residual"],
            obstruction: OperatorObstruction::MissingTripleClassCover,
            missing_obligations: vec![
                "projector-polytope atlas covering all admissible triples",
                "proof that the pinned residual quotient is functorial across atlas overlaps",
            ],
            discard_reason: "does not yet range over every MUB(6) triple class",
        },
        OperatorAttempt {
            target: AttemptTarget::FullMub6,
            layer: OperatorLayer::WeylBoard,
            disposition: AttemptDisposition::Discarded,
            operator: "Weyl-board incidence and sector cap",
            preserved_structure: vec!["line incidence", "sector combinatorics"],
            obstruction: OperatorObstruction::MissingBasisGluing,
            missing_obligations: vec![
                "exact spectral-projector lift from board sectors to Hilbert-space bases",
                "proof that the board sector cap is equivalent to complete MUB(6) nonexistence",
            ],
            discard_reason: "finite board obstruction is not yet equivalent to the analytic complete-basis problem",
        },
        OperatorAttempt {
            target: AttemptTarget::FullMub6,
            layer: OperatorLayer::GtmurRepresentationTransport,
            disposition: AttemptDisposition::LiveButBlocked,
            operator: "CODA-MUR loss-ledger transport between representation regimes",
            preserved_structure: vec![
                "declared carrier",
                "ZeroRel",
                "terminalizer boundary",
                "loss ledger",
            ],
            obstruction: OperatorObstruction::RepresentationLossUnclosed,
            missing_obligations: vec![
                "lossless transport certificate from coordinate/projector/Weyl regimes",
                "2-cell coherence certificate for all regime changes used in the proof",
                "terminal non-bypass proof for the target theorem",
            ],
            discard_reason: "representation change cannot create authority without a closed loss ledger",
        },
        OperatorAttempt {
            target: AttemptTarget::FullMub6,
            layer: OperatorLayer::GtorComparisonEnvelope,
            disposition: AttemptDisposition::Discarded,
            operator: "CODA-OR comparison/completion envelope over candidate representations",
            preserved_structure: vec!["comparison object membership"],
            obstruction: OperatorObstruction::CompletionNonCreation,
            missing_obligations: vec![
                "component descent certificates",
                "edge transport certificates",
                "local terminalization for every component",
                "directed-limit or certified finite-shape gluing theorem",
            ],
            discard_reason: "completion membership does not create MUB authority",
        },
    ]
}

pub fn mub10_operator_ladder() -> Vec<OperatorAttempt> {
    vec![
        OperatorAttempt {
            target: AttemptTarget::Mub10,
            layer: OperatorLayer::Cyclotomic120TensorControl,
            disposition: AttemptDisposition::LiveButBlocked,
            operator: "Q(zeta_120) tensor-product d=2 x d=5 lower-control",
            preserved_structure: vec![
                "exact Q(zeta_120) coefficient field",
                "orthonormality for three d=10 bases",
                "mutual unbiasedness for the three-basis lower-control",
                "composite tensor-family min-factor basis-count gate",
            ],
            obstruction: OperatorObstruction::PartialLowerControlOnly,
            missing_obligations: vec![
                "complete eleven-basis MUB(10) carrier",
                "repair group and observer for complete d=10 configurations",
                "replayable complete witness or no-go certificate",
            ],
            discard_reason:
                "kept as a lower-control benchmark, but insufficient as a complete MUB(10) theorem",
        },
        OperatorAttempt {
            target: AttemptTarget::Mub10,
            layer: OperatorLayer::CoordinateExact,
            disposition: AttemptDisposition::LiveButBlocked,
            operator: "d=10 canonical-triple wall critical value and corrected Clifford stabilizer census",
            preserved_structure: vec![
                "W10 critical value reproduced at dps=460 with stationarity residual 4.6721e-462",
                "Noah 50-digit anchor cross-check reproduced",
                "full Cl(2) tensor Cl(5) census has zero nontrivial unitary fixers and one antiunitary involution",
                "Z/2 real-structure reduction to a 10-real-dimensional fixed locus",
            ],
            obstruction: OperatorObstruction::NumericalOnly,
            missing_obligations: vec![
                "exact upper-bound certificate proving the d=10 critical value is a global wall maximum",
                "closed-form derivation or exact elimination inside the Z/2 real fixed locus",
                "complete eleven-basis MUB(10) witness or proof-carrying no-go certificate",
            ],
            discard_reason: "corrected d=10 wall evidence is valuable but remains critical-value/stabilizer evidence, not MUB(10) theorem authority",
        },
        OperatorAttempt {
            target: AttemptTarget::Mub10,
            layer: OperatorLayer::GtmurRepresentationTransport,
            disposition: AttemptDisposition::LiveButBlocked,
            operator: "representation transport candidate for d=10",
            preserved_structure: vec!["declared only after an exact carrier exists"],
            obstruction: OperatorObstruction::MissingExactCarrier,
            missing_obligations: vec![
                "exact d=10 carrier",
                "declared repair group",
                "observer and terminalizer policy",
            ],
            discard_reason:
                "cannot transport a theorem before the source and target regimes are declared",
        },
    ]
}

pub fn general_mub_n_operator_ladder() -> Vec<OperatorAttempt> {
    vec![
        OperatorAttempt {
            target: AttemptTarget::GeneralMubN,
            layer: OperatorLayer::FiniteFieldWeylSchema,
            disposition: AttemptDisposition::LiveButBlocked,
            operator: "finite-field Weyl trace/Gauss/spread schema for prime and prime-power dimensions",
            preserved_structure: vec![
                "finite-field carrier",
                "field trace",
                "same-basis trace-linear reductions",
                "cross-basis quadratic Gauss reductions",
                "Lean finite translation-scaling cancellation sublemma for nontrivial character sums",
                "Lean odd-prime-power finite-field family witness",
                "Lean finite-field AddChar linear orthogonality theorem",
                "Lean quadratic Gauss complex squared-norm theorem",
                "Lean trace-character phase-overlap kernel for odd prime-power fields",
                "Lean Complex 1/sqrt(q) normalization algebra for odd prime-power phase overlaps",
                "Lean Complex coefficient scalar package for primitive additive characters and sqrt-card normalizers",
                "Lean algebraic coefficient-field contract surface for lifted characters and normalizers",
                "Lean finite-function Hilbert phase-vector transport for odd prime-power trace-character bases",
                "Lean primitive Complex additive-character existence for finite fields",
                "Lean existential Complex finite-function q+1 MUB family for odd-characteristic finite fields",
                "Lean coordinate-equivalence transport preserving finite-function Hilbert MUB identities",
                "Lean structured finite Complex MUB family object with coordinate-equivalence transport",
                "Lean finite-function CODA-MUR coordinate ledger preserving ZeroRel and squared overlaps",
                "Lean finite-function terminalizer coordinate ledger preserving complete basis/label profile and ZeroRel",
                "Lean finite-function Hilbert-basis transport object packaging coordinate transport and basis identities",
                "Lean finite-function CODA-MUR zero-loss ledger for coordinate-equivalence Hilbert-basis transport",
                "Lean algebraic Hilbert-basis transport contract surface for lifted vectors and inner products",
                "Lean algebraic CODA-MUR loss-ledger contract surface for lifted ZeroRel and squared overlaps",
                "Lean algebraic terminalizer-preservation contract surface for complete basis, ZeroRel, and squared overlaps",
                "finite odd-prime Gauss-certificate Hilbert controls",
                "characteristic-two isotropic spread incidence",
                "spectral-projector counting reductions",
                "symbolic Pauli projector algebra reductions",
                "exact finite Hilbert matrix transport reductions",
                "finite CODA-MUR projector loss-ledger reductions",
                "exact d=7, d=11, and d=13 odd-prime quadratic Weyl Hilbert controls",
                "finite characteristic-two projector MUB controls for sampled prime powers",
                "exact d=9, d=25, d=27, and d=49 odd-prime-power trace-character Hilbert controls",
                "odd-prime-power dimension-parametric Hilbert/CODA-MUR family gate",
                "characteristic-two dimension-parametric projector family gate",
                "prime-power/composite CODA-MUR boundary reductions",
                "composite tensor-family lower-control gaps",
            ],
            obstruction: OperatorObstruction::ProofSchemaOnly,
            missing_obligations: vec![
                "uniform algebraic coefficient-field carrier for trace-character Hilbert normalizers",
                "dimension-parametric extension of the finite odd-prime Gauss-certificate gate",
                "dimension-parametric extension of the exact d=7, d=11, and d=13 odd-prime Hilbert controls",
                "algebraic coefficient-field carrier, Hilbert-basis transport object, and CODA-MUR family beyond the Complex finite-function theorem",
                "dimension-parametric terminalizer-preservation family beyond finite coordinate reindexing and algebraic contract surfaces",
                "accepted characteristic-two parametric projector family gate beyond sampled finite controls",
                "dimension-parametric extension of Hilbert positivity and CODA-MUR loss ledger for every prime-power projector schema",
                "complete composite-dimension witness or no-go certificate for non-prime-power targets",
                "dimension-parametric certificate family covering the all-N query",
                "proof that prime-power schemas transport to the claimed general theorem",
            ],
            discard_reason:
                "kept as a prime-power proof schema, but insufficient as a composite or all-N theorem",
        },
        OperatorAttempt {
            target: AttemptTarget::GeneralMubN,
            layer: OperatorLayer::GttcContinuumShadow,
            disposition: AttemptDisposition::Discarded,
            operator: "dimension-indexed continuum/pro-object shadow",
            preserved_structure: vec!["dimension-indexed bookkeeping"],
            obstruction: OperatorObstruction::ContinuumNonCreation,
            missing_obligations: vec![
                "finite-shadow terminalization for each declared dimension stratum",
                "uniform certificate family or certified stratification",
                "query-relative authority proof for the all-N statement",
            ],
            discard_reason: "a continuum or pro-object shadow does not create an all-N MUB theorem",
        },
        OperatorAttempt {
            target: AttemptTarget::GeneralMubN,
            layer: OperatorLayer::GtorComparisonEnvelope,
            disposition: AttemptDisposition::Discarded,
            operator: "comparison envelope over finite benchmark dimensions",
            preserved_structure: vec!["benchmark ledger"],
            obstruction: OperatorObstruction::CompletionNonCreation,
            missing_obligations: vec![
                "directed comparison system with component terminalization",
                "proof that benchmark obstructions transport to the target all-N query",
            ],
            discard_reason: "finite benchmark comparison does not authorize the general theorem",
        },
    ]
}

pub fn current_operator_ladder(upper_bound_replayed: bool) -> Vec<OperatorAttempt> {
    let mut attempts = full_mub6_operator_ladder(upper_bound_replayed);
    attempts.extend(mub10_operator_ladder());
    attempts.extend(general_mub_n_operator_ladder());
    attempts
}

pub fn retained_live_attempts(attempts: &[OperatorAttempt]) -> Vec<&OperatorAttempt> {
    attempts
        .iter()
        .filter(|attempt| attempt.disposition == AttemptDisposition::LiveButBlocked)
        .collect()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn full_mub6_ladder_keeps_pinned_wall_but_does_not_promote_it() {
        let attempts = full_mub6_operator_ladder(true);
        let coordinate = attempts
            .iter()
            .find(|attempt| attempt.layer == OperatorLayer::CoordinateExact)
            .expect("coordinate attempt present");
        assert_eq!(coordinate.disposition, AttemptDisposition::LiveButBlocked);
        assert_eq!(
            coordinate.obstruction,
            OperatorObstruction::MissingTripleClassCover
        );
        assert!(coordinate
            .missing_obligations
            .iter()
            .any(|obligation| obligation.contains("basis-gluing")));
    }

    #[test]
    fn gtmur_attempt_requires_closed_loss_ledger() {
        let attempts = full_mub6_operator_ladder(false);
        let gtmur = attempts
            .iter()
            .find(|attempt| attempt.layer == OperatorLayer::GtmurRepresentationTransport)
            .expect("CODA-MUR attempt present");
        assert_eq!(
            gtmur.obstruction,
            OperatorObstruction::RepresentationLossUnclosed
        );
        assert!(gtmur
            .missing_obligations
            .iter()
            .any(|obligation| obligation.contains("lossless transport")));
    }

    #[test]
    fn gtor_and_gttc_layers_are_non_creation_firewalls() {
        let attempts = current_operator_ladder(false);
        assert!(attempts.iter().any(|attempt| {
            attempt.layer == OperatorLayer::GtorComparisonEnvelope
                && attempt.obstruction == OperatorObstruction::CompletionNonCreation
        }));
        assert!(attempts.iter().any(|attempt| {
            attempt.layer == OperatorLayer::GttcContinuumShadow
                && attempt.obstruction == OperatorObstruction::ContinuumNonCreation
        }));
    }

    #[test]
    fn general_ladder_records_finite_field_weyl_schema_as_schema_only() {
        let attempts = general_mub_n_operator_ladder();
        let finite_field = attempts
            .iter()
            .find(|attempt| attempt.layer == OperatorLayer::FiniteFieldWeylSchema)
            .expect("finite-field Weyl schema attempt present");
        assert_eq!(finite_field.disposition, AttemptDisposition::LiveButBlocked);
        assert_eq!(
            finite_field.obstruction,
            OperatorObstruction::ProofSchemaOnly
        );
        assert!(finite_field
            .missing_obligations
            .iter()
            .any(|obligation| obligation.contains("positivity")));
        assert!(finite_field
            .missing_obligations
            .iter()
            .any(|obligation| obligation.contains("all-N")));
    }

    #[test]
    fn retained_live_attempts_are_blocked_not_authoritative() {
        let attempts = current_operator_ladder(false);
        let live = retained_live_attempts(&attempts);
        assert!(!live.is_empty());
        assert!(live
            .iter()
            .all(|attempt| attempt.disposition == AttemptDisposition::LiveButBlocked));
    }

    #[test]
    fn mub10_ladder_records_qzeta120_lower_control() {
        let attempts = mub10_operator_ladder();
        let lower = attempts
            .iter()
            .find(|attempt| attempt.layer == OperatorLayer::Cyclotomic120TensorControl)
            .expect("Q(zeta_120) d=10 lower-control attempt present");
        assert_eq!(
            lower.obstruction,
            OperatorObstruction::PartialLowerControlOnly
        );
        assert!(lower
            .missing_obligations
            .iter()
            .any(|obligation| obligation.contains("eleven-basis")));
    }

    #[test]
    fn full_mub6_ladder_records_tensor_lower_control() {
        let attempts = full_mub6_operator_ladder(false);
        let lower = attempts
            .iter()
            .find(|attempt| attempt.layer == OperatorLayer::CompositeTensorControl)
            .expect("d=6 tensor lower-control attempt present");
        assert_eq!(
            lower.obstruction,
            OperatorObstruction::PartialLowerControlOnly
        );
        assert!(lower
            .missing_obligations
            .iter()
            .any(|obligation| obligation.contains("seven-basis")));
    }
}
