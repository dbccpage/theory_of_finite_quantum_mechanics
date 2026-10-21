use super::*;
use crate::omega_native::exact::basis_gluing_gate::BasisGluingStatus;
use crate::omega_native::exact::char_two_parametric_gate::CharTwoParametricStatus;
use omega_quantum_physics::mub::char_two_weyl_board::CharTwoWeylBoardStatus;
use omega_quantum_physics::mub::composite_completion_gate::CompositeCompletionStatus;
use omega_quantum_physics::mub::composite_tensor_family_gate::CompositeTensorFamilyStatus;
use crate::omega_native::exact::gtor_gttc_gate::GtorGttcGateStatus;
use omega_quantum_physics::mub::gtmur_projector_ledger::GtmurProjectorLedgerStatus;
use omega_quantum_physics::mub::hilbert_transport::HilbertTransportStatus;
use omega_quantum_physics::mub::odd_prime_gauss_certificate_gate::OddPrimeGaussCertificateStatus;
use omega_quantum_physics::mub::odd_prime_power_field_theorem_gate::OddPrimePowerFieldTheoremStatus;
use omega_quantum_physics::mub::odd_prime_power_parametric_gate::OddPrimePowerParametricStatus;
use omega_quantum_physics::mub::odd_prime_power_weyl::OddPrimePowerWeylStatus;
use omega_quantum_physics::mub::odd_prime_weyl::OddPrimeWeylStatus;
use omega_quantum_physics::mub::prime_power_gtmur_boundary::PrimePowerGtmurBoundaryStatus;
use omega_quantum_physics::mub::projector_algebra::ProjectorAlgebraStatus;
use omega_quantum_physics::mub::spectral_lift::SpectralLiftStatus;
    use crate::omega_native::float_check::d10_wall_status::{D10StabilizerStatus, D10WallAuthorityStatus};
    use omega_quantum_physics::mub::dimension_stratification::DimensionAuthorityStatus;
    use omega_wdp::ddc::mub_cochain::{
        D2C3Result, FunctionalPacketStatus, MubBasisGluingStatus, MubHigherLayer,
        MubTripleCarrierAtlasDefectKind, MubTripleCarrierAtlasStatus,
    };
    use std::sync::OnceLock;

    fn crate_root() -> &'static Path {
        Path::new(env!("CARGO_MANIFEST_DIR"))
    }

    fn deep_run_report() -> &'static DeepRunReport {
        static REPORT: OnceLock<DeepRunReport> = OnceLock::new();
        REPORT.get_or_init(|| run_deep_mub(crate_root()))
    }

    #[test]
    fn deep_run_replays_are_missing_obligations_without_apache_crate() {
        let report = deep_run_report();
        for (name, terminal) in [
            ("manifest", report.manifest.terminal),
            ("d6_lower_bound", report.d6_lower_bound.terminal),
            ("d6_upper_bound", report.d6_upper_bound.terminal),
        ] {
            assert_eq!(
                terminal,
                ReplayTerminal::MissingProofObligation,
                "{name} must be a missing proof obligation, not a claimed replay"
            );
        }
    }

    #[test]
    fn deep_run_refuses_theorem_promotion_after_pinned_target() {
        let report = deep_run_report();
        assert_eq!(
            report.full_mub6.verdict.terminal,
            ExtensionTerminal::MissingProofObligation
        );
        assert_eq!(
            report.mub10.verdict.terminal,
            ExtensionTerminal::MissingProofObligation
        );
        assert_eq!(
            report.general_mub_n.verdict.terminal,
            ExtensionTerminal::TypedRefusal
        );
        assert_eq!(report.terminal, FinalTerminal::TypedRefusal);
    }

    #[test]
    #[ignore = "needs the ../mub/public-export/evidence receipts, which are not in this repository"]
    fn deep_run_receipt_checks_pinned_h_transport() {
        let report = deep_run_report();
        assert_eq!(
            report.pinned_transport.status,
            LocalTransportStatus::ReceiptChecked
        );
        assert!(report
            .full_mub6
            .verdict
            .discharged_obligations
            .iter()
            .any(|obligation| obligation.contains("pinned H-symmetry")));
        assert!(report
            .full_mub6
            .verdict
            .missing_obligations
            .iter()
            .any(|obligation| obligation.contains("every covered triple class")));
    }

    #[test]
    fn deep_run_audits_current_sources_as_not_global_atlas() {
        let report = deep_run_report();
        assert_eq!(
            report.global_atlas.status,
            AtlasStatus::MissingProofObligation
        );
        assert!(report
            .global_atlas
            .missing_obligations
            .iter()
            .any(|obligation| obligation.contains("exhaustive atlas")));
        let root = std::path::Path::new(env!("CARGO_MANIFEST_DIR"));
        for source in &report.global_atlas.candidate_sources {
            if !root.join(source.relative_path).exists() {
                assert_eq!(
                    source.verdict,
                    crate::omega_native::exact::global_atlas::CandidateCoverVerdict::Missing
                );
            }
        }
    }

    #[test]
    fn deep_run_includes_basis_gluing_gate() {
        let report = deep_run_report();
        assert_eq!(
            report.basis_gluing.status,
            BasisGluingStatus::MissingProofObligation
        );
        assert!(report
            .basis_gluing
            .missing_obligations
            .iter()
            .any(|obligation| obligation.contains("exhaustive cover")));
        assert!(report
            .basis_gluing
            .missing_obligations
            .iter()
            .any(|obligation| obligation.contains("basis-gluing theorem")));
        assert!(report
            .basis_gluing
            .rejected_escalations
            .iter()
            .any(|item| item.contains("pinned fourth-vector") || item.contains("H-symmetry")));
    }

    #[test]
    fn deep_run_includes_mub6_cochain_obstruction() {
        let report = deep_run_report();
        match &report.mub6_cochain_obstruction {
            DeepRunMubCochainObstruction::Completed(cochain) => {
                assert_eq!(cochain.status, "executed");
                assert_eq!(cochain.evidence, MubAtlasEvidence::default());
                assert_eq!(
                    cochain.higher_cn.next_layer,
                    MubHigherLayer::C3AtlasCoherence
                );
                assert_eq!(
                    cochain.c3_d2.result,
                    D2C3Result::AtlasCoherenceObstructed { defect_count: 5 }
                );
                assert_eq!(
                    cochain.basis_gluing_cochain.status,
                    MubBasisGluingStatus::BlockedByC3AtlasCoherence
                );
                assert_eq!(
                    cochain.triple_carrier_analysis.status,
                    MubTripleCarrierAtlasStatus::IncompleteCarrierAtlas
                );
                assert!(cochain
                    .triple_carrier_analysis
                    .defects
                    .iter()
                    .any(|defect| defect.kind
                        == MubTripleCarrierAtlasDefectKind::MissingTransportToPinnedOrOwnCertificate
                        && defect.class_id == Some("general-admissible-triples")));
                assert_eq!(
                    cochain.quotient.replay.packet_status,
                    FunctionalPacketStatus::SyntheticExactObstructionPacket
                );
                assert!(cochain
                    .c3_atlas_coherence
                    .missing_obligations
                    .iter()
                    .any(|obligation| obligation.contains("complete classification")));
            }
            DeepRunMubCochainObstruction::CochainConstructionFailure { error, .. } => {
                panic!("cochain obstruction search should construct: {error}")
            }
        }
    }
    #[test]
    fn deep_run_records_corrected_d10_wall_status() {
        let report = deep_run_report();

        assert_eq!(report.d10_wall_status.recorded.dps, 460);
        assert!(!report.d10_wall_status.recorded.scripts_in_repository);
        assert_eq!(
            report.d10_wall_status.authority_status,
            D10WallAuthorityStatus::EvidenceOnlyCriticalPoint
        );
        assert_eq!(
            report.d10_wall_status.stabilizer_status,
            D10StabilizerStatus::Z2AntiunitaryInvolution
        );
        assert_eq!(
            report.d10_wall_status.single_qudit_clifford_elements,
            72_000
        );
        assert_eq!(report.d10_wall_status.antiunitary_fixers, 1);
        assert!(report
            .d10_wall_status
            .boundary
            .contains("does not authorize a MUB(10)"));
        assert_eq!(
            report.mub10.verdict.terminal,
            ExtensionTerminal::MissingProofObligation
        );
    }

    #[test]
    fn deep_run_includes_exact_prime_controls() {
        let report = deep_run_report();
        assert!(report
            .prime_controls
            .iter()
            .any(|control| control.dimension == 2 && control.basis_count == 3));
        assert!(report
            .prime_controls
            .iter()
            .any(|control| control.dimension == 3 && control.basis_count == 4));
        assert!(report
            .prime_controls
            .iter()
            .any(|control| control.dimension == 7 && control.basis_count == 8));
        assert!(report
            .prime_controls
            .iter()
            .any(|control| control.dimension == 11 && control.basis_count == 12));
        assert!(report
            .prime_controls
            .iter()
            .any(|control| control.dimension == 13 && control.basis_count == 14));
        assert!(report
            .prime_controls
            .iter()
            .all(|control| control.error.is_none()));
        assert!(report
            .general_mub_n
            .verdict
            .discharged_obligations
            .iter()
            .any(|obligation| obligation.contains("exact odd-prime")));
    }

    #[test]
    fn deep_run_includes_odd_prime_gauss_certificate_gate() {
        let report = deep_run_report();
        assert_eq!(
            report.odd_prime_gauss_certificates.status,
            OddPrimeGaussCertificateStatus::FiniteCertificatesVerified
        );
        assert_eq!(
            report.odd_prime_gauss_certificates.certified_dimensions,
            vec![7, 11, 13]
        );
        assert!(report
            .odd_prime_gauss_certificates
            .remaining_theorem_obligations
            .iter()
            .any(|obligation| obligation.contains("dimension-parametric")));
        assert!(report
            .general_mub_n
            .verdict
            .discharged_obligations
            .iter()
            .any(|obligation| obligation.contains("Gauss-certificate")));
        assert_eq!(
            report.general_mub_n.verdict.terminal,
            ExtensionTerminal::TypedRefusal
        );
    }

    #[test]
    fn deep_run_includes_exact_d6_composite_lower_control() {
        let report = deep_run_report();
        assert!(report
            .composite_lower_controls
            .iter()
            .any(|control| control.dimension == 6
                && control.basis_count == 3
                && control.status == CompositeControlStatus::ExactPartialSet));
        assert!(report
            .full_mub6
            .verdict
            .discharged_obligations
            .iter()
            .any(|obligation| obligation.contains("three-MUB lower-control")));
        assert_eq!(
            report.full_mub6.verdict.terminal,
            ExtensionTerminal::MissingProofObligation
        );
    }

    #[test]
    fn deep_run_includes_exact_prime_power_control() {
        let report = deep_run_report();
        assert!(report
            .prime_power_controls
            .iter()
            .any(|control| control.dimension == 4 && control.basis_count == 5));
        assert!(report
            .prime_power_controls
            .iter()
            .all(|control| control.error.is_none()));
    }

    fn assert_exact_complete_control(
        report: &DeepRunReport,
        dim: usize,
        bases: usize,
        ortho: usize,
        cross: usize,
    ) {
        assert!(report.odd_prime_power_controls.iter().any(|control| {
            control.dimension == dim
                && control.basis_count == bases
                && control.status == OddPrimePowerControlStatus::ExactCompleteSet
                && control.orthonormality_checks == ortho
                && control.cross_unbiased_checks == cross
        }));
    }

    fn assert_stratification_control(report: &DeepRunReport, dim: usize, bases: usize) {
        assert!(report.dimension_stratification.iter().any(|entry| {
            entry.dimension == dim
                && entry.status == DimensionAuthorityStatus::ExactCompleteControl
                && entry.guaranteed_basis_count == Some(bases)
        }));
    }

    fn assert_tensor_lower_control(
        report: &DeepRunReport,
        dim: usize,
        guaranteed: usize,
        complete: usize,
    ) {
        assert!(report.dimension_stratification.iter().any(|entry| {
            entry.dimension == dim
                && entry.status == DimensionAuthorityStatus::ExactTensorLowerControl
                && entry.guaranteed_basis_count == Some(guaranteed)
                && entry.complete_basis_count == Some(complete)
        }));
    }

    #[test]
    fn deep_run_includes_exact_d9_odd_prime_power_control() {
        let report = deep_run_report();
        assert_exact_complete_control(report, 9, 10, 450, 3645);
        assert_exact_complete_control(report, 25, 26, 26 * 25 * 26 / 2, 325 * 25 * 25);
        assert_exact_complete_control(report, 27, 28, 28 * 27 * 28 / 2, 378 * 27 * 27);
        assert_exact_complete_control(report, 49, 50, 50 * 49 * 50 / 2, 1225 * 49 * 49);

        assert_stratification_control(report, 9, 10);
        assert_stratification_control(report, 25, 26);
        assert_stratification_control(report, 27, 28);
        assert_stratification_control(report, 49, 50);
        assert_stratification_control(report, 11, 12);
        assert_stratification_control(report, 13, 14);

        assert!(report
            .general_mub_n
            .verdict
            .discharged_obligations
            .iter()
            .any(|obligation| obligation.contains("exact odd-prime-power")));
        assert_eq!(
            report.general_mub_n.verdict.terminal,
            ExtensionTerminal::TypedRefusal
        );
    }

    #[test]
    fn deep_run_includes_finite_projector_prime_power_controls() {
        let report = deep_run_report();
        assert!(report.finite_projector_controls.iter().any(|control| {
            control.dimension == 8
                && control.basis_count == 9
                && control.projector_count == 72
                && control.status == FiniteProjectorControlStatus::CompleteProjectorMubVerified
                && control.rank_one_trace_checks == 72
        }));
        assert!(report.finite_projector_controls.iter().all(|control| {
            control.status == FiniteProjectorControlStatus::CompleteProjectorMubVerified
                && control
                    .rejected_authority_escalations
                    .iter()
                    .any(|item| item.contains("all-N"))
        }));
        assert!(report
            .general_mub_n
            .verdict
            .discharged_obligations
            .iter()
            .any(|obligation| obligation
                .contains("finite characteristic-two projector MUB controls")));
    }

    #[test]
    fn deep_run_includes_odd_prime_power_field_theorem_gate() {
        let report = deep_run_report();
        assert_eq!(
            report.odd_prime_power_field_theorem_gate.status,
            OddPrimePowerFieldTheoremStatus::FiniteFieldTheoremsAccepted
        );
        assert!(report
            .odd_prime_power_field_theorem_gate
            .sampled_dimensions
            .contains(&49));
        assert!(
            report
                .odd_prime_power_field_theorem_gate
                .trace_uniformity_checks
                > 0
        );
        assert!(
            report
                .odd_prime_power_field_theorem_gate
                .gauss_norm_linear_reductions
                > 0
        );
        assert!(report
            .odd_prime_power_field_theorem_gate
            .lean_proof_artifacts
            .contains(&"MUB.finite_character_sum_vanishes_from_nontrivial_translation"));
        assert!(report
            .odd_prime_power_field_theorem_gate
            .lean_proof_artifacts
            .contains(&"MUB.finite_field_nontrivial_additive_character_linear_orthogonality"));
        assert!(report
            .odd_prime_power_field_theorem_gate
            .lean_proof_artifacts
            .contains(&"MUB.odd_prime_power_finite_field_family_exists"));
        assert!(report
            .odd_prime_power_field_theorem_gate
            .lean_proof_artifacts
            .contains(&"MUB.quadraticGauss_complex_normSq"));
        assert!(report
            .odd_prime_power_field_theorem_gate
            .checked_reductions
            .iter()
            .any(|obligation| obligation.contains("additive-character orthogonality")));
        assert!(report
            .odd_prime_power_field_theorem_gate
            .checked_reductions
            .iter()
            .any(|obligation| obligation.contains("finite-field family")));
        assert!(report
            .odd_prime_power_field_theorem_gate
            .checked_reductions
            .iter()
            .any(|obligation| obligation.contains("quadratic Gauss-norm")));
        assert!(report
            .odd_prime_power_field_theorem_gate
            .missing_theorem_families
            .is_empty());
    }

    #[test]
    fn deep_run_includes_odd_prime_power_parametric_gate() {
        let report = deep_run_report();
        assert_eq!(
            report.odd_prime_power_parametric_gate.status,
            OddPrimePowerParametricStatus::FiniteSchemasOnly
        );
        assert!(report
            .odd_prime_power_parametric_gate
            .sampled_dimensions
            .contains(&49));
        assert!(report
            .odd_prime_power_parametric_gate
            .exact_control_dimensions
            .contains(&49));
        assert!(report
            .odd_prime_power_parametric_gate
            .checked_obligations
            .iter()
            .any(|obligation| obligation.contains("finite-field theorem gate")));
        assert!(report
            .odd_prime_power_parametric_gate
            .checked_obligations
            .iter()
            .any(|obligation| obligation.contains("phase-overlap kernel")));
        assert!(report
            .odd_prime_power_parametric_gate
            .checked_obligations
            .iter()
            .any(|obligation| obligation.contains("normalization algebra")));
        assert!(report
            .odd_prime_power_parametric_gate
            .checked_obligations
            .iter()
            .any(|obligation| obligation.contains("Complex coefficient scalar package")));
        assert!(report
            .odd_prime_power_parametric_gate
            .checked_obligations
            .iter()
            .any(|obligation| obligation.contains("coefficient-field contract surface")));
        assert!(report
            .odd_prime_power_parametric_gate
            .checked_obligations
            .iter()
            .any(|obligation| obligation.contains("phase-vector transport")));
        assert!(report
            .odd_prime_power_parametric_gate
            .checked_obligations
            .iter()
            .any(|obligation| obligation.contains("primitive Complex additive characters")));
        assert!(report
            .odd_prime_power_parametric_gate
            .checked_obligations
            .iter()
            .any(|obligation| obligation.contains("q+1 MUB family")));
        assert!(report
            .odd_prime_power_parametric_gate
            .checked_obligations
            .iter()
            .any(|obligation| obligation.contains("coordinate-equivalence transport")));
        assert!(report
            .odd_prime_power_parametric_gate
            .checked_obligations
            .iter()
            .any(|obligation| obligation.contains("structured finite Complex MUB family")));
        assert!(report
            .odd_prime_power_parametric_gate
            .checked_obligations
            .iter()
            .any(|obligation| obligation.contains("finite-function CODA-MUR coordinate ledger")));
        assert!(report
            .odd_prime_power_parametric_gate
            .checked_obligations
            .iter()
            .any(
                |obligation| obligation.contains("finite-function terminalizer coordinate ledger")
            ));
        assert!(report
            .odd_prime_power_parametric_gate
            .checked_obligations
            .iter()
            .any(
                |obligation| obligation.contains("finite-function Hilbert-basis transport object")
            ));
        assert!(report
            .odd_prime_power_parametric_gate
            .checked_obligations
            .iter()
            .any(|obligation| obligation.contains("finite-function CODA-MUR zero-loss ledger")));
        assert!(report
            .odd_prime_power_parametric_gate
            .checked_obligations
            .iter()
            .any(|obligation| obligation.contains("algebraic Hilbert-basis transport contract")));
        assert!(report
            .odd_prime_power_parametric_gate
            .checked_obligations
            .iter()
            .any(|obligation| obligation.contains("algebraic CODA-MUR loss-ledger contract")));
        assert!(report
            .odd_prime_power_parametric_gate
            .checked_obligations
            .iter()
            .any(|obligation| {
                obligation.contains("algebraic terminalizer-preservation contract")
            }));
        assert!(report
            .odd_prime_power_parametric_gate
            .missing_obligations
            .iter()
            .any(|obligation| obligation.contains("coefficient field")));
        assert!(report
            .odd_prime_power_parametric_gate
            .missing_obligations
            .iter()
            .any(|obligation| obligation.contains("terminalizer preservation")));
        assert!(report
            .general_mub_n
            .verdict
            .missing_obligations
            .iter()
            .any(|obligation| obligation.contains("odd-prime-power parametric")));
    }

    #[test]
    fn deep_run_includes_char_two_parametric_gate() {
        let report = deep_run_report();
        assert_eq!(
            report.char_two_parametric_gate.status,
            CharTwoParametricStatus::FiniteSamplesOnly
        );
        assert!(report
            .char_two_parametric_gate
            .sampled_dimensions
            .contains(&8));
        assert!(report
            .char_two_parametric_gate
            .missing_obligations
            .iter()
            .any(|obligation| obligation.contains("GF(2^k)")));
        assert!(report
            .char_two_parametric_gate
            .missing_obligations
            .iter()
            .any(|obligation| obligation.contains("positive rank-one")));
        assert!(report
            .char_two_parametric_gate
            .rejected_escalations
            .iter()
            .any(|item| item.contains("sampled characteristic-two controls")));
        assert!(report
            .general_mub_n
            .verdict
            .missing_obligations
            .iter()
            .any(|obligation| obligation.contains("including characteristic two")));
    }

    #[test]
    fn deep_run_includes_cyclotomic120_d10_lower_control() {
        let report = deep_run_report();
        assert!(report
            .cyclotomic120_controls
            .iter()
            .any(|control| control.dimension == 5
                && control.status == Cyclotomic120Status::ExactCompleteSet));
        assert!(report
            .cyclotomic120_controls
            .iter()
            .any(|control| control.dimension == 10
                && control.basis_count == 3
                && control.status == Cyclotomic120Status::ExactPartialSet));
        assert!(report
            .mub10
            .verdict
            .discharged_obligations
            .iter()
            .any(|obligation| obligation.contains("Q(zeta_120)")));
        assert_eq!(
            report.mub10.verdict.terminal,
            ExtensionTerminal::MissingProofObligation
        );
    }

    #[test]
    fn deep_run_includes_dimension_stratification_gate() {
        let report = deep_run_report();
        assert_stratification_control(report, 4, 5);
        assert_stratification_control(report, 8, 9);
        assert_stratification_control(report, 7, 8);
        assert_stratification_control(report, 9, 10);

        assert_tensor_lower_control(report, 6, 3, 7);
        assert_tensor_lower_control(report, 10, 3, 11);
        assert_tensor_lower_control(report, 26, 3, 27);

        assert!(report
            .general_mub_n
            .verdict
            .discharged_obligations
            .iter()
            .any(|obligation| obligation.contains("stratification")));
        assert_eq!(
            report.general_mub_n.verdict.terminal,
            ExtensionTerminal::TypedRefusal
        );
    }

    #[test]
    fn deep_run_includes_composite_tensor_family_gate() {
        let report = deep_run_report();
        assert_eq!(
            report.composite_tensor_family.status,
            CompositeTensorFamilyStatus::TensorFamilyVerified
        );
        assert!(report.composite_tensor_family.cases.iter().any(|case| {
            case.dimension == 6
                && case.factor_dimensions == vec![2, 3]
                && case.paired_tensor_basis_count == 3
                && case.missing_basis_count == 4
        }));
        assert!(report.composite_tensor_family.cases.iter().any(|case| {
            case.dimension == 10
                && case.factor_dimensions == vec![2, 5]
                && case.paired_tensor_basis_count == 3
                && case.missing_basis_count == 8
        }));
        assert!(report.composite_tensor_family.cases.iter().any(|case| {
            case.dimension == 26
                && case.factor_dimensions == vec![2, 13]
                && case.paired_tensor_basis_count == 3
                && case.missing_basis_count == 24
        }));
        assert!(report
            .composite_tensor_family
            .rejected_escalations
            .iter()
            .any(|item| item.contains("N+1")));
        assert!(report
            .general_mub_n
            .verdict
            .discharged_obligations
            .iter()
            .any(|obligation| obligation.contains("composite tensor-family")));
    }

    #[test]
    fn deep_run_includes_odd_prime_weyl_schema_gate() {
        let report = deep_run_report();
        assert!(report.odd_prime_weyl_schemas.iter().any(|schema| {
            schema.dimension == 7
                && schema.basis_count == 8
                && schema.status == OddPrimeWeylStatus::ProofSchemaVerified
        }));
        assert!(report.odd_prime_weyl_schemas.iter().any(|schema| {
            schema.dimension == 13
                && schema.basis_count == 14
                && schema.status == OddPrimeWeylStatus::ProofSchemaVerified
        }));
        assert!(report.odd_prime_weyl_schemas.iter().all(|schema| {
            schema.status == OddPrimeWeylStatus::ProofSchemaVerified
                && schema
                    .theorem_obligations
                    .iter()
                    .any(|obligation| obligation.contains("Gauss"))
        }));
        assert!(report
            .general_mub_n
            .verdict
            .discharged_obligations
            .iter()
            .any(|obligation| obligation.contains("odd-prime Weyl")));
    }

    #[test]
    fn deep_run_includes_odd_prime_power_weyl_schema_gate() {
        let report = deep_run_report();
        assert!(report.odd_prime_power_weyl_schemas.iter().any(|schema| {
            schema.prime == 3
                && schema.exponent == 2
                && schema.dimension == 9
                && schema.basis_count == 10
                && schema.status == OddPrimePowerWeylStatus::ProofSchemaVerified
        }));
        assert!(report.odd_prime_power_weyl_schemas.iter().all(|schema| {
            schema.status == OddPrimePowerWeylStatus::ProofSchemaVerified
                && schema.trace_uniformity_checks == schema.dimension - 1
                && schema
                    .theorem_obligations
                    .iter()
                    .any(|obligation| obligation.contains("trace"))
        }));
        assert!(report
            .general_mub_n
            .verdict
            .discharged_obligations
            .iter()
            .any(|obligation| obligation.contains("prime-power Weyl")));
        assert_eq!(
            report.general_mub_n.verdict.terminal,
            ExtensionTerminal::TypedRefusal
        );
    }

    #[test]
    fn deep_run_includes_char_two_weyl_board_schema_gate() {
        let report = deep_run_report();
        assert!(report.char_two_weyl_board_schemas.iter().any(|schema| {
            schema.exponent == 3
                && schema.dimension == 8
                && schema.line_count == 9
                && schema.status == CharTwoWeylBoardStatus::BoardSchemaVerified
                && schema.nonzero_vector_cover_count == 63
        }));
        assert!(report.char_two_weyl_board_schemas.iter().all(|schema| {
            schema.status == CharTwoWeylBoardStatus::BoardSchemaVerified
                && schema
                    .theorem_obligations
                    .iter()
                    .any(|obligation| obligation.contains("spectral-projector"))
        }));
        assert!(report
            .general_mub_n
            .verdict
            .discharged_obligations
            .iter()
            .any(|obligation| obligation.contains("characteristic-two")));
        assert!(report
            .general_mub_n
            .verdict
            .missing_obligations
            .iter()
            .any(|obligation| obligation.contains("Hilbert-transport")));
        assert_eq!(
            report.general_mub_n.verdict.terminal,
            ExtensionTerminal::TypedRefusal
        );
    }

    #[test]
    fn deep_run_includes_spectral_lift_schema_gate() {
        let report = deep_run_report();
        assert!(report.spectral_lift_schemas.iter().any(|schema| {
            schema.dimension == 8
                && schema.basis_count == 9
                && schema.projector_count == 72
                && schema.status == SpectralLiftStatus::LiftSchemaVerified
        }));
        assert!(report.spectral_lift_schemas.iter().all(|schema| {
            schema.status == SpectralLiftStatus::LiftSchemaVerified
                && schema
                    .theorem_obligations
                    .iter()
                    .any(|obligation| obligation.contains("positivity"))
        }));
        assert!(report
            .general_mub_n
            .verdict
            .discharged_obligations
            .iter()
            .any(|obligation| obligation.contains("spectral-projector lift schema")));
        assert!(report
            .general_mub_n
            .verdict
            .missing_obligations
            .iter()
            .any(|obligation| obligation.contains("positivity")));
        assert_eq!(
            report.general_mub_n.verdict.terminal,
            ExtensionTerminal::TypedRefusal
        );
    }

    #[test]
    fn deep_run_includes_projector_algebra_schema_gate() {
        let report = deep_run_report();
        assert!(report.projector_algebra_schemas.iter().any(|schema| {
            schema.dimension == 8
                && schema.basis_count == 9
                && schema.projector_count == 72
                && schema.status == ProjectorAlgebraStatus::AlgebraVerified
                && schema.rank_one_trace_checks == 72
        }));
        assert!(report.projector_algebra_schemas.iter().all(|schema| {
            schema.status == ProjectorAlgebraStatus::AlgebraVerified
                && schema
                    .theorem_obligations
                    .iter()
                    .any(|obligation| obligation.contains("positive rank-one"))
        }));
        assert!(report
            .general_mub_n
            .verdict
            .discharged_obligations
            .iter()
            .any(|obligation| obligation.contains("symbolic Pauli projector algebra")));
        assert!(report
            .general_mub_n
            .verdict
            .missing_obligations
            .iter()
            .any(|obligation| obligation.contains("Hilbert-transport")));
        assert_eq!(
            report.general_mub_n.verdict.terminal,
            ExtensionTerminal::TypedRefusal
        );
    }

    #[test]
    fn deep_run_includes_hilbert_transport_schema_gate() {
        let report = deep_run_report();
        assert!(report.hilbert_transport_schemas.iter().any(|schema| {
            schema.dimension == 8
                && schema.basis_count == 9
                && schema.projector_count == 72
                && schema.status == HilbertTransportStatus::TransportVerified
                && schema.projector_rank_one_trace_checks == 72
        }));
        assert!(report.hilbert_transport_schemas.iter().all(|schema| {
            schema.status == HilbertTransportStatus::TransportVerified
                && schema
                    .theorem_obligations
                    .iter()
                    .any(|obligation| obligation.contains("dimension-parametric"))
        }));
        assert!(report
            .general_mub_n
            .verdict
            .discharged_obligations
            .iter()
            .any(|obligation| obligation.contains("Hilbert matrix transport")));
        assert!(report
            .general_mub_n
            .verdict
            .missing_obligations
            .iter()
            .any(|obligation| obligation.contains("CODA-MUR loss ledger")));
        assert_eq!(
            report.general_mub_n.verdict.terminal,
            ExtensionTerminal::TypedRefusal
        );
    }

    #[test]
    fn deep_run_includes_finite_gtmur_projector_ledger_gate() {
        let report = deep_run_report();
        assert!(report.gtmur_projector_ledgers.iter().any(|ledger| {
            ledger.dimension == 8
                && ledger.basis_count == 9
                && ledger.projector_count == 72
                && ledger.status == GtmurProjectorLedgerStatus::FiniteLedgerClosed
                && ledger.representation_edge_checks == 3
        }));
        assert!(report.gtmur_projector_ledgers.iter().all(|ledger| {
            ledger.status == GtmurProjectorLedgerStatus::FiniteLedgerClosed
                && ledger
                    .rejected_authority_escalations
                    .iter()
                    .any(|item| item.contains("all-N"))
        }));
        assert!(report
            .general_mub_n
            .verdict
            .discharged_obligations
            .iter()
            .any(|obligation| obligation.contains("finite CODA-MUR projector ledger")));
        assert!(report
            .general_mub_n
            .verdict
            .missing_obligations
            .iter()
            .any(|obligation| obligation.contains("dimension-parametric")));
        assert_eq!(
            report.general_mub_n.verdict.terminal,
            ExtensionTerminal::TypedRefusal
        );
    }

    #[test]
    fn deep_run_includes_prime_power_gtmur_boundary_gate() {
        let report = deep_run_report();
        assert_eq!(
            report.prime_power_gtmur_boundary.status,
            PrimePowerGtmurBoundaryStatus::BoundaryVerified
        );
        assert!(
            report
                .prime_power_gtmur_boundary
                .odd_prime_gauss_certificate_count
                >= 3
        );
        assert!(report
            .prime_power_gtmur_boundary
            .composite_gaps
            .iter()
            .any(|gap| gap.dimension == 6 && gap.complete_basis_count == 7));
        assert!(report
            .prime_power_gtmur_boundary
            .composite_gaps
            .iter()
            .any(|gap| gap.dimension == 10 && gap.complete_basis_count == 11));
        assert!(report
            .prime_power_gtmur_boundary
            .composite_gaps
            .iter()
            .any(|gap| gap.dimension == 26 && gap.complete_basis_count == 27));
        assert!(report
            .general_mub_n
            .verdict
            .discharged_obligations
            .iter()
            .any(|obligation| obligation.contains("prime-power CODA-MUR boundary ledger")));
        assert!(report
            .general_mub_n
            .verdict
            .missing_obligations
            .iter()
            .any(|obligation| obligation.contains("composite-dimension")));
        assert_eq!(
            report.general_mub_n.verdict.terminal,
            ExtensionTerminal::TypedRefusal
        );
    }

    #[test]
    fn deep_run_includes_composite_completion_gate() {
        let report = deep_run_report();
        assert!(report.composite_completion_gates.iter().any(|gate| {
            gate.dimension == 6
                && gate.status == CompositeCompletionStatus::LowerControlOnly
                && gate.required_complete_basis_count == 7
                && gate.lower_control_basis_count == Some(3)
                && gate.missing_basis_count == Some(4)
        }));
        assert!(report.composite_completion_gates.iter().any(|gate| {
            gate.dimension == 10
                && gate.status == CompositeCompletionStatus::LowerControlOnly
                && gate.required_complete_basis_count == 11
                && gate.lower_control_basis_count == Some(3)
                && gate.missing_basis_count == Some(8)
        }));
        assert!(report.composite_completion_gates.iter().all(|gate| {
            gate.missing_obligations
                .iter()
                .any(|obligation| obligation.contains("witness") || obligation.contains("no-go"))
        }));
    }

    #[test]
    fn deep_run_discards_gtor_gttc_noncreating_gates() {
        let report = deep_run_report();
        assert_eq!(report.gtor_gttc_gates.len(), 2);
        assert!(report
            .gtor_gttc_gates
            .iter()
            .all(|gate| gate.status == GtorGttcGateStatus::DiscardedNonCreating));
        assert!(report.gtor_gttc_gates.iter().all(|gate| {
            gate.finite_component_count > gate.terminalized_component_count
                && !gate.directed_gluing_present
                && !gate.query_relative_authority_present
        }));
        assert!(report.gtor_gttc_gates.iter().any(|gate| {
            gate.missing_obligations
                .iter()
                .any(|obligation| obligation.contains("uniform certificate"))
        }));
    }

    #[test]
    fn deep_run_includes_operator_ladder_failures() {
        let report = deep_run_report();
        assert!(report
            .operator_ladder
            .iter()
            .any(|attempt| attempt.operator.contains("CODA-MUR")));
        assert!(report
            .operator_ladder
            .iter()
            .any(|attempt| attempt.discard_reason.contains("does not create")));
    }
