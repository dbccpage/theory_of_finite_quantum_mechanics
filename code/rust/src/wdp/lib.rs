
pub mod amplitude_bridge;
pub mod authority_gap;
pub mod bridges;
pub mod cochains;
pub mod composition;
pub mod connection;
pub mod covering_edge_descent;
pub mod difference;
pub mod empirical_adapter;
pub mod error;
pub mod fenchel_duality;
pub mod gauge_classification;
pub mod genesis_carrier;
pub mod genesis_bell;
pub mod genesis_joint_dynamics;
pub mod genesis_construction;
pub mod genesis_geometry;
pub mod genesis_observer;
pub mod genesis_passage;
pub mod genesis_refusal;
pub mod guarded_chain_transport;
pub mod instrument_adapter;
pub mod kan_wdp_bridge;
pub mod meron_time_adapter;
pub mod observer;
pub mod observer_adapter_completeness;
pub mod observer_world_adapter;
pub mod obstruction;
pub mod path_kernel_gluing;
pub mod po000_projection_obstruction;
pub mod policy_observer_adapter;
pub mod presheaf;
pub mod primitive_axiomatics;
pub mod quantum_geometries;
pub mod question_preserving_encoding;
pub mod retention;
pub mod sql_normal_form;
pub mod stochastic_package;
pub mod types;
pub mod wdp_kernel_check;
pub mod wdp_lggr_chromatic;
pub mod wdp_rust_routes;
pub mod wdp_source_packet;
pub mod witnessed_reasoning;
pub mod witnessed_reasoning_replay;

pub mod carrier_binding;
pub mod coda;
pub mod ddc;
pub mod phi1_coda_adapter;
pub mod phi1_d_sel;
pub mod prime_algos;
pub mod solver_of_solvers;

pub use amplitude_bridge::{
    half_exponent_obstruction, readout_quadratic, readout_quartic, same_up_to_common_phase, u_pow,
    u_power_is_never_one, unit_phase, unit_square_root, Amplitude, EdgePath,
    HalfExponentObstruction, OrientedGraph, PathStep,
};
pub use authority_gap::{
    calculate_acr, calculate_acr_rate, calculate_backlog_accumulation, calculate_ngd,
    evaluate_exactness_fraud_criterion, Attestation, AuthorityPacket, GluingEvaluation,
    Institution, ObserverPacket, Proposal, Residual, Terminal, TerminalStatus, TraceRecord,
};
pub use bridges::{
    evaluate_path_homotopy, verify_cabello_18ray_parity, verify_kan_horn_filling,
    verify_sorkin_i3_cancellation, AlgebraicNonFactorableWitness, Cabello18RayWitness,
    Homotopy2CellObstruction, IdentityPathWitness, KanHornFillerWitness,
};
pub use carrier_binding::{
    carrier_manifest, to_homology_carrier, CarrierBindingError, IsingCycleGradientRepair,
};
pub use cochains::{solve_potential, FiniteComplex};
pub use composition::{
    composite_state_from_bilinear, composite_state_from_form, local_decoders, pr_box_fixture,
    BilinearForm, FormReceipt, JointState, PrBoxFixture,
};
pub use connection::U1Connection;
pub use difference::{primitive_difference, Carrier, DifferenceOutcome, PresentationMap};
pub use empirical_adapter::{
    adapt_exact, adapt_tolerant, chsh_cover, chsh_pairwise_box, chsh_value, frequencies,
    global_run_table, l1_distance_to_model, pr_box_run_table, signalling_defect,
    two_context_repair, AdapterRefusal, EmpiricalModel, MeasurementCover, RunTable, TolerantModel,
};
pub use error::WdpError;
pub use fenchel_duality::{EdgeSaturationStatus, FenchelDualityReceipt, WeightedComplex};
pub use gauge_classification::{
    evaluate_countermodels_ce1_to_ce5, single_cycle_quotient_rational,
    verify_triangle_separation_anomaly, ConvexPolyhedralGauge, GaugeClassificationReceipt,
    GraphOrbitWeightFactorizer, MixedClosureBoundChecker, MixedNormJ21, OrbitWeightRigidityReceipt,
    SingleCycleQuotientError, SoKRigidityReceipt, TransformationMonoid,
};
pub use instrument_adapter::{
    complex_phase_instrument, luders_instrument, measure_and_prepare_instrument,
    non_projective_instrument, InstrumentReceipt, OutcomeRunTable, QubitInstrument, QubitState,
};
pub use kan_wdp_bridge::{
    Hott2CellHomotopyWitness, KanHornFillingWitness, KanSimplicialComplex, ZeroDataLossReceipt,
};
pub use observer::{
    adapt_operational, adapt_quotient, adapt_retention, audit_functional_observer_relations,
    FunctionalObserverProfile, ObserverBridge, ObserverObject, OperationalObserverPacket,
    QuotientObserver,
};
pub use obstruction::{
    solve_exact_potential, solve_exact_potential_weighted, CertificateVerificationError, Cochain0,
    Cochain1, DualWitnessCertificate,
};
pub use path_kernel_gluing::{
    generate_canonical_lggr_counterexample, EvaluatedPathKernelGraph, EvaluationColor,
    LggrEvaluationReceipt, RationalMatrix2x2,
};
pub use po000_projection_obstruction::{DeclaredProjectionProblem, ProjectionObstructionReceipt};
pub use presheaf::{
    solve_observer_descent, CoveringSieve, DescentReceipt, LocalReportSection,
    SheafGluingObstruction,
};
pub use primitive_axiomatics::{
    EvaluationCarrier, EvaluationPreorder, GenesisAdmissionKernel, PrimitiveDifferenceAxiom,
    TriadSignature,
};
pub use quantum_geometries::{
    CptpChannel, QuantumDensityStalk, QuantumGeometryReceipt, QuantumObserverBundle,
};
pub use retention::{
    analyze_retention_packet, compute_behavioral_quotient, make_cm1_static_carrier,
    make_cm2_blind_readout, make_cm3_coarse_grained_report, make_cm4_nontrivial_tolerance,
    make_cm5_lossy_reset, make_cm6_trivial_carrier, make_cm7_lossy_blind, make_cm8_lossy_tolerance,
    tree_behavior_equivalent, RetentionPacket, RetentionPropertyVector,
};
pub use stochastic_package::{
    signed_shear_counterexample, ClassicalInstrument, FunctionMixture, LeftInverse,
    SignedShearReport, StochasticUpdate,
};
pub use types::{blake3_digest, sha256_digest, AuthorityEffect};
pub use wdp_lggr_chromatic::{ChromaticCertificate, ChromaticConstraintSystem};

#[cfg(test)]
mod tests {
    use super::*;
    use num_traits::Zero;
    use omega_functional::phi1::Phi1Functional;
    use omega_homology::scalar::{q, qr};
    use omega_solvers::solver_lp_phi1_quotient::solve_exact_phi1;
    use std::collections::{BTreeMap, BTreeSet};

    #[test]
    fn test_end_to_end_wdp_foundations() {
        let carrier = Carrier::new(vec!["p0", "p1", "p2"]).unwrap();
        assert_eq!(carrier.size(), 3);
        assert_eq!(primitive_difference("p0", "p0"), DifferenceOutcome::Same);
        assert_eq!(
            primitive_difference("p0", "p1"),
            DifferenceOutcome::Different
        );

        let cm1 = make_cm1_static_carrier();
        let (num_blocks, _) = compute_behavioral_quotient(&cm1).unwrap();
        assert_eq!(num_blocks, 2);

        let v = BTreeSet::from(["a".to_string(), "b".to_string(), "c".to_string()]);
        let e = vec![
            ("a".to_string(), "b".to_string()),
            ("b".to_string(), "c".to_string()),
            ("c".to_string(), "a".to_string()),
        ];
        let complex = FiniteComplex::new(v, e, vec![]).unwrap();
        let mut cochain = BTreeMap::new();
        cochain.insert(("a".to_string(), "b".to_string()), q(1));
        cochain.insert(("b".to_string(), "c".to_string()), q(1));
        cochain.insert(("c".to_string(), "a".to_string()), q(1));

        let space = complex
            .l1_quotient_presentation(&complex.edge_weights(None))
            .unwrap();
        let cert = solve_exact_phi1(&space, &complex.cochain_vector(&cochain).unwrap()).unwrap();
        assert_eq!(cert.value(), &q(3));
        let replayed =
            Phi1Functional::verify_exact_certificate(cert.certificate().clone()).unwrap();
        assert_eq!(replayed.value(), &q(3));

        let sieve_carrier = BTreeSet::from(["x0".to_string(), "x1".to_string()]);
        let contexts = BTreeMap::from([(
            "U0".to_string(),
            BTreeSet::from(["x0".to_string(), "x1".to_string()]),
        )]);
        let sieve = CoveringSieve::new(sieve_carrier, contexts).unwrap();
        let sec = LocalReportSection::new(
            "U0".to_string(),
            BTreeMap::from([
                ("x0".to_string(), "0".to_string()),
                ("x1".to_string(), "1".to_string()),
            ]),
        );
        let descent = solve_observer_descent(&sieve, &[sec]).unwrap();
        assert!(descent.is_compatible);

        let betti = KanSimplicialComplex::from_wdp_complex(&complex)
            .unwrap()
            .complex
            .rational_betti_numbers()
            .unwrap();
        assert_eq!(betti, vec![1, 1]);

        let cabello = verify_cabello_18ray_parity();
        assert!(cabello.is_parity_obstructed);
        assert_eq!(cabello.authority_effect, AuthorityEffect::None);
    }

    #[test]
    fn test_w10_to_w18_atlas_derivations() {
        let mut kernel =
            GenesisAdmissionKernel::new(BTreeSet::from(["x".to_string(), "y".to_string()]));
        assert!(kernel.admit_difference("x", "y", "token").is_ok());

        let w_complex = WeightedComplex::new(
            vec!["0".to_string(), "1".to_string()],
            vec![("0".to_string(), "1".to_string())],
            vec![q(1)],
        );
        let fenchel = w_complex.solve_fenchel_duality(&[q(1)]).unwrap();
        assert!(fenchel.phi1().value().is_zero());
        Phi1Functional::verify_exact_certificate(fenchel.phi1().certificate().clone()).unwrap();

        let (lggr_graph, cycle) = generate_canonical_lggr_counterexample();
        let (local_g, _) = lggr_graph.check_local_green(qr(1, 2)).unwrap();
        assert!(local_g);
        let (global_g, _) = lggr_graph.check_global_cycle(&cycle, qr(1, 10)).unwrap();
        assert!(!global_g);

        let sys = ChromaticConstraintSystem {
            vertices: vec!["0".into(), "1".into(), "2".into()],
            edges: vec![
                ("0".into(), "1".into()),
                ("1".into(), "2".into()),
                ("2".into(), "0".into()),
            ],
            num_colors: 2,
            forbidden_color_pairs: BTreeSet::from([(0, 0), (1, 1)]),
        };
        assert_eq!(sys.evaluate(8, 24).unwrap().minimum.violated_edges.len(), 1);

        let p =
            linear_algebra::backend::basic_matrix::BasicMatrix::from_row_major(1, 1, vec![q(1)])
                .unwrap();
        let h =
            linear_algebra::backend::basic_matrix::BasicMatrix::from_row_major(1, 1, vec![q(0)])
                .unwrap();
        let problem = DeclaredProjectionProblem {
            first: p.clone(),
            second: p,
            generator: h,
            elapsed: qr(1, 10),
            state: vec![q(1)],
        };
        let bounds = problem.evaluate().unwrap();
        assert!(problem.verify(&bounds).unwrap());

        let rho = QuantumDensityStalk::maximally_mixed(2).unwrap();
        assert!(rho.is_valid_density_matrix());
        let shadow = rho.classical_population_shadow();
        assert_eq!(shadow, vec![qr(1, 2), qr(1, 2)]);

        let gauge = ConvexPolyhedralGauge::standard_l1(2);
        assert_eq!(gauge.evaluate(&[q(1), q(-2)]), q(3));

        let (l11, j21, anomaly) = verify_triangle_separation_anomaly();
        assert!(anomaly);
        assert!(j21 < l11);

        let ce_results = evaluate_countermodels_ce1_to_ce5();
        assert_eq!(ce_results.len(), 5);
        for (_, passes) in ce_results {
            assert!(passes);
        }
    }
}

pub mod calibration_adapter;

pub mod profile_evaluator;

pub mod clock_adequacy_adapter;

pub mod relational_retention;

pub mod functional_classification;

pub mod empirical_repair;
pub mod legacy_observer_adapters;
pub mod legacy_six_observer;
pub mod measurement_packet;
pub mod observer_site;
pub mod rational_phase_bridge;
pub mod self_reference_adapter;
pub mod tolerance_retention;

pub mod finite_cost_report;
pub mod genesis_admission_execution;
pub mod genesis_balance_transition;
pub mod genesis_gauge_result;
pub mod genesis_guard_report;
pub mod genesis_guarded_history;
pub mod genesis_marked_result;
pub mod genesis_ongoing_adapter;
pub mod genesis_primitive_execution;
pub mod genesis_source_execution;
pub mod genesis_transport_descent;
pub mod proposal_admission_bridge;

pub mod dyadic_character_adapter;
pub mod genesis_computation;
pub mod genesis_future_compression;
pub mod genesis_questions;
pub mod genesis_report_runtime;
pub mod genesis_realification_adapter;
pub mod meron_field_adapter;

pub mod calibrated_reports;
pub mod distinct_image_completion;
pub mod joint_support_recovery;
pub mod observation_cost;

pub mod genesis_translation;

pub mod application_kernel;
