//! The General Obstruction Management Calculus, computed: observer
//! nonfaithfulness and its composition, local-green/global-red cochains, Born
//! pairing non-selection, exact branch search, packet-relative reconstruction
//! terminals, the coherence-lift gate, and the authority-null composed report.
use linear_algebra::exact_field::matrix;

use num_traits::Zero;
use omega_number_theory::rational::{ri, rq, Rational};
use omega_policy::trichotomy::ObstructionDiagnosticClass;
use omega_quantum_physics::exact_hermitian::{gi, gq};
use omega_quantum_physics::mass_phase_embedding::MassPhaseEmbedding;
use omega_solvers::data_cochain_packet::FiniteCochainPacket;

use finite_qm_native::campaigns::residual_density_calculus::{evaluate_coherence, ResidualLedger};
use finite_qm_native::obstruction_management_calculus::{
    evaluate_lift_candidate, gomc_report, licensed_coherence_lift, obstruction_branch_search,
    terminalize_reconstruction, GomcError, ImprovementTier, ObstructionPoint, ReconstructionImport,
    ReconstructionTerminal, ReportAuthorityTag,
};

use omega_quantum_physics::pairing_audit::{born_pairing, dephased_pairing, PairingError};
use omega_solvers::solver_cohomology_quotient_phi1::{lggr_cochain_witness, CertifiedPhi1Error};
use omega_types::observer_quotient::{
    hidden_separation, pair_observer, HiddenSeparation, ReadoutLengthMismatch,
};

fn rats(values: &[i64]) -> Vec<Rational> {
    values.iter().map(|&v| ri(v)).collect()
}

fn point(phi1: Rational, gamma2: Rational, xi: Option<Rational>) -> ObstructionPoint {
    ObstructionPoint { phi1, gamma2, xi }
}

fn square() -> FiniteCochainPacket {
    FiniteCochainPacket::with_unit_weights(
        FiniteCochainPacket::build_complex(
            &["a", "b", "c", "d"],
            &[("a", "b"), ("b", "c"), ("c", "d"), ("d", "a")],
            &[],
        )
        .unwrap(),
    )
    .unwrap()
}

#[test]
fn an_observer_that_merges_states_a_hidden_readout_separates_is_nonfaithful() {
    assert_eq!(
        hidden_separation(&[0, 0, 1], &[5, 7, 5]).unwrap(),
        Some(HiddenSeparation {
            first: 0,
            second: 1
        })
    );
    assert_eq!(hidden_separation(&[0, 1, 2], &[5, 7, 5]).unwrap(), None);
    assert!(matches!(
        hidden_separation(&[0, 1], &[5]),
        Err(ReadoutLengthMismatch {
            first: 2,
            second: 1
        })
    ));
}

#[test]
fn locally_green_fragments_compose_while_a_hidden_glue_stays_red() {
    let first = [0, 0, 1, 1];
    let second = [0, 0, 0, 1];
    let pair = pair_observer(&first, &second).unwrap();
    // Each fragment, and the visible pair, identifies states 0 and 1.
    assert_eq!(pair[0], pair[1]);
    let glue = [0, 1, 0, 0];
    assert_eq!(
        hidden_separation(&pair, &glue).unwrap(),
        Some(HiddenSeparation {
            first: 0,
            second: 1
        })
    );
}

#[test]
fn equal_edge_masses_can_hide_different_quotient_classes() {
    let packet = square();
    let repair = packet.primitive_difference(&rats(&[0, 1, 0, 1])).unwrap();
    assert_eq!(repair, rats(&[1, -1, 1, -1]));
    let circulation = rats(&[1, 1, 1, 1]);
    let witness = lggr_cochain_witness(
        packet.vertex_count(),
        packet.d0(),
        packet.d1(),
        packet.weights(),
        &repair,
        &circulation,
        10000,
    )
    .unwrap()
    .unwrap();
    assert_eq!(witness.first_class, ObstructionDiagnosticClass::ExactRepair);
    assert_eq!(
        witness.second_class,
        ObstructionDiagnosticClass::ClosedResidual
    );
    assert_eq!(
        lggr_cochain_witness(
            packet.vertex_count(),
            packet.d0(),
            packet.d1(),
            packet.weights(),
            &circulation,
            &circulation,
            10000
        )
        .unwrap(),
        None
    );
    assert_eq!(
        lggr_cochain_witness(
            packet.vertex_count(),
            packet.d0(),
            packet.d1(),
            packet.weights(),
            &circulation,
            &rats(&[2, 1, 1, 1]),
            10000
        )
        .unwrap(),
        None
    );
    // Zero cochains have equal (zero) masses and one class: no witness, not a refusal.
    let zero = rats(&[0, 0, 0, 0]);
    assert_eq!(
        lggr_cochain_witness(
            packet.vertex_count(),
            packet.d0(),
            packet.d1(),
            packet.weights(),
            &zero,
            &zero,
            10000
        )
        .unwrap(),
        None
    );
    assert_eq!(
        lggr_cochain_witness(
            packet.vertex_count(),
            packet.d0(),
            packet.d1(),
            packet.weights(),
            &zero,
            &circulation,
            10000
        )
        .unwrap(),
        None
    );
    assert!(matches!(
        lggr_cochain_witness(
            packet.vertex_count(),
            packet.d0(),
            packet.d1(),
            packet.weights(),
            &zero,
            &rats(&[0, 0]),
            10000
        ),
        Err(CertifiedPhi1Error::Shape)
    ));
}

#[test]
fn simplex_readouts_do_not_select_the_born_pairing() {
    let plus = matrix::from_rows(vec![
        vec![gq(1, 2, 0, 1), gq(1, 2, 0, 1)],
        vec![gq(1, 2, 0, 1), gq(1, 2, 0, 1)],
    ])
    .unwrap();
    let minus = matrix::sub(&matrix::identity(2).unwrap(), &plus).unwrap();
    let rho = matrix::diagonal(&[gq(3, 4, 0, 1), gq(1, 4, 0, 1)]).unwrap();
    let e0 = matrix::diagonal(&[gi(1, 0), gi(0, 0)]).unwrap();
    // They agree on diagonal data...
    assert_eq!(born_pairing(&e0, &rho).unwrap(), rq(3, 4));
    assert_eq!(dephased_pairing(&e0, &rho).unwrap(), rq(3, 4));
    // ...both are normalised on the POVM {|+><+|, |-><-|}...
    for pairing in [born_pairing, dephased_pairing] {
        let total = pairing(&plus, &plus).unwrap() + pairing(&minus, &plus).unwrap();
        assert_eq!(total, ri(1));
    }
    // ...and they disagree off the diagonal.
    assert_eq!(born_pairing(&plus, &plus).unwrap(), ri(1));
    assert_eq!(dephased_pairing(&plus, &plus).unwrap(), rq(1, 2));
    assert!(matches!(
        born_pairing(&e0, &matrix::identity(3).unwrap()),
        Err(PairingError::Shape)
    ));
}

#[test]
fn amplitude_coordinates_do_not_fix_coherence() {
    // Weights (9/25, 16/25) have exact amplitudes, so the two presentations can be compared.
    let masses = rats(&[9, 16]);
    let a = MassPhaseEmbedding::new(&masses, &[gi(1, 0), gi(1, 0)]).unwrap();
    let b = MassPhaseEmbedding::new(&masses, &[gi(1, 0), gi(-1, 0)]).unwrap();
    assert_eq!(a.born_weights(), b.born_weights());
    assert_eq!(
        a.exact_amplitudes().unwrap(),
        vec![gq(3, 5, 0, 1), gq(4, 5, 0, 1)]
    );
    assert_eq!(
        b.exact_amplitudes().unwrap(),
        vec![gq(3, 5, 0, 1), gq(-4, 5, 0, 1)]
    );
}

#[test]
fn branch_search_ranks_strict_descent_lexicographically() {
    let current = point(ri(3), ri(2), Some(ri(5)));
    let candidates = vec![
        ("a".to_string(), point(ri(1), ri(9), None)),
        ("b".to_string(), point(ri(3), rq(1, 2), None)),
        ("c".to_string(), point(ri(3), ri(2), Some(ri(4)))),
        ("d".to_string(), point(ri(4), ri(0), Some(ri(0)))),
        ("e".to_string(), point(ri(3), ri(2), Some(ri(5)))),
    ];
    let report = obstruction_branch_search(&current, &candidates).unwrap();
    let tiers: Vec<Option<ImprovementTier>> = report.proposals.iter().map(|p| p.tier).collect();
    assert_eq!(
        tiers,
        vec![
            Some(ImprovementTier::Phi1),
            Some(ImprovementTier::Gamma2),
            Some(ImprovementTier::Xi),
            None,
            None
        ]
    );
    assert_eq!(
        report.probabilities,
        vec![ri(1), ri(0), ri(0), Rational::zero(), Rational::zero()]
    );
    assert_eq!(report.ranking, vec![0, 1, 2]);
    // Worse Phi1 is never rescued by better Gamma2 or Xi.
    assert!(report.proposals[3].mass.is_zero());
    let bad = obstruction_branch_search(&point(ri(-1), ri(0), None), &[]);
    assert!(matches!(bad, Err(GomcError::NegativeCoordinate { .. })));
}

#[test]
fn the_ranking_follows_the_points_not_the_masses() {
    // Masses are not comparable across tiers: b improves Gamma2 by 10, a only
    // Phi1 by 1, yet a's point (2, 10) precedes b's point (3, 0).
    let current = point(ri(3), ri(10), None);
    let candidates = vec![
        ("a".to_string(), point(ri(2), ri(10), None)),
        ("b".to_string(), point(ri(3), ri(0), None)),
    ];
    let report = obstruction_branch_search(&current, &candidates).unwrap();
    assert_eq!(
        report
            .proposals
            .iter()
            .map(|p| p.mass.clone())
            .collect::<Vec<_>>(),
        vec![ri(1), ri(10)]
    );
    assert_eq!(report.ranking, vec![0, 1]);
    // Within one tier equal masses are separated by the next coordinate, not the label.
    let candidates = vec![
        ("p".to_string(), point(ri(1), ri(5), None)),
        ("q".to_string(), point(ri(1), ri(2), None)),
    ];
    let report = obstruction_branch_search(&current, &candidates).unwrap();
    assert_eq!(report.proposals[0].mass, report.proposals[1].mass);
    assert_eq!(report.ranking, vec![1, 0]);
}

fn ranked_labels(
    current: &ObstructionPoint,
    candidates: &[(String, ObstructionPoint)],
) -> Vec<String> {
    let report = obstruction_branch_search(current, candidates).unwrap();
    report
        .ranking
        .iter()
        .map(|&i| candidates[i].0.clone())
        .collect()
}

#[test]
fn the_ranking_is_total_when_xi_is_declared_on_some_candidates_only() {
    // At equal (Phi1, Gamma2) the old comparator treated a missing Xi as Equal and
    // fell through to the label: z < m (label), m < a (label), a < z (Xi), a cycle
    // whose result depended on the input order.
    let current = point(ri(3), ri(2), Some(ri(5)));
    let all = [
        ("z".to_string(), point(ri(1), ri(9), Some(ri(1)))),
        ("m".to_string(), point(ri(1), ri(9), None)),
        ("a".to_string(), point(ri(1), ri(9), Some(ri(2)))),
    ];
    let orders = [
        [0, 1, 2],
        [0, 2, 1],
        [1, 0, 2],
        [1, 2, 0],
        [2, 0, 1],
        [2, 1, 0],
    ];
    for order in orders {
        let candidates: Vec<_> = order.iter().map(|&i| all[i].clone()).collect();
        // A declared Xi precedes an undeclared one; among declared Xi the least first.
        assert_eq!(
            ranked_labels(&current, &candidates),
            ["z", "a", "m"],
            "input order {order:?}"
        );
    }
}

#[test]
fn the_ranking_is_a_strict_total_order_for_many_mixed_candidates() {
    let current = point(ri(10), ri(10), Some(ri(10)));
    let mut state = 0x2545_f491_4f6c_dd1d_u64;
    let mut next = |modulus: u64| {
        state = state
            .wrapping_mul(6_364_136_223_846_793_005)
            .wrapping_add(1_442_695_040_888_963_407);
        (state >> 33) % modulus
    };
    let candidates: Vec<(String, ObstructionPoint)> = (0..64)
        .map(|n| {
            let xi = if next(3) == 0 {
                None
            } else {
                Some(ri(next(6) as i64))
            };
            let phi1 = ri(8 + next(3) as i64);
            let gamma2 = ri(8 + next(3) as i64);
            (format!("c{n:02}"), point(phi1, gamma2, xi))
        })
        .collect();
    let report = obstruction_branch_search(&current, &candidates).unwrap();
    let strict: Vec<usize> = (0..candidates.len())
        .filter(|&i| report.proposals[i].tier.is_some())
        .collect();
    assert!(
        strict.len() > 16,
        "the fixture must exercise many strict candidates"
    );
    // The expected order, from an independent key: Xi declared before undeclared.
    let key = |i: usize| {
        let p = &candidates[i].1;
        (
            p.phi1.clone(),
            p.gamma2.clone(),
            p.xi.is_none(),
            p.xi.clone(),
            candidates[i].0.clone(),
        )
    };
    let mut expected = strict.clone();
    expected.sort_by_key(|&i| key(i));
    assert_eq!(report.ranking, expected);
    // Permutation invariance: reversing the input gives the same sequence of labels.
    let reversed: Vec<_> = candidates.iter().rev().cloned().collect();
    assert_eq!(
        ranked_labels(&current, &reversed),
        ranked_labels(&current, &candidates)
    );
    // Strictness of every adjacent pair.
    for pair in report.ranking.windows(2) {
        assert!(key(pair[0]) < key(pair[1]), "{pair:?}");
    }
}

#[test]
fn missing_imports_terminalize_as_packet_relative_obstruction() {
    use ReconstructionImport::*;
    let all = [
        FiniteHilbertCarrier,
        ComplexScalars,
        BornPairing,
        CptpDynamics,
        TensorComposition,
    ];
    assert_eq!(
        terminalize_reconstruction(&all),
        ReconstructionTerminal::Hosted
    );
    assert_eq!(
        terminalize_reconstruction(&[FiniteHilbertCarrier, ComplexScalars, CptpDynamics]),
        ReconstructionTerminal::PacketRelativeObstruction {
            missing: vec![BornPairing, TensorComposition]
        }
    );
    assert_eq!(
        terminalize_reconstruction(&[]),
        ReconstructionTerminal::PacketRelativeObstruction {
            missing: all.to_vec()
        }
    );
}

#[test]
fn a_complete_coherence_license_does_not_license_a_lift() {
    let filled = FiniteCochainPacket::with_unit_weights(
        FiniteCochainPacket::build_complex(
            &["a", "b", "c"],
            &[("a", "b"), ("b", "c"), ("c", "a")],
            &[&["a", "b", "c"]],
        )
        .unwrap(),
    )
    .unwrap();
    let certified = |x: &[Rational]| {
        let t = filled.classify(x).unwrap();
        point(t.phi1_value().clone(), t.gamma2_value().clone(), None)
    };
    let before = certified(&rats(&[1, 1, 1]));
    let after = certified(&rats(&[1, 0, 0]));
    assert_eq!((before.phi1.clone(), before.gamma2.clone()), (ri(3), ri(3)));
    assert_eq!((after.phi1.clone(), after.gamma2.clone()), (ri(1), ri(1)));
    let ledger = ResidualLedger::new(rats(&[1, 1])).unwrap();
    let plus = matrix::from_rows(vec![
        vec![gq(1, 2, 0, 1), gq(1, 2, 0, 1)],
        vec![gq(1, 2, 0, 1), gq(1, 2, 0, 1)],
    ])
    .unwrap();
    let license = evaluate_coherence(&ledger, &plus, true);
    assert!(license.is_licensed());
    // A move that reduces Phi1 with declared carrier and replay is a licensed lift.
    let lift = evaluate_lift_candidate(&before, &after, true, true).unwrap();
    assert!(lift.source_obstruction() && lift.reduces_phi() && lift.preserves_closure());
    assert!(licensed_coherence_lift(&license, &lift));
    // The same license with a move that does not reduce Phi1 licenses nothing.
    let backwards = evaluate_lift_candidate(&after, &before, true, true).unwrap();
    assert!(!backwards.reduces_phi() && !backwards.preserves_closure());
    assert!(!licensed_coherence_lift(&license, &backwards));
    // Nor without a declared replay, and without a declared observer basis the license fails.
    assert!(!licensed_coherence_lift(
        &license,
        &evaluate_lift_candidate(&before, &after, true, false).unwrap()
    ));
    assert!(!licensed_coherence_lift(
        &evaluate_coherence(&ledger, &plus, false),
        &lift
    ));
    // Negative coordinates are refused, as in the branch search.
    assert!(matches!(
        evaluate_lift_candidate(&point(ri(-1), ri(0), None), &after, true, true),
        Err(GomcError::NegativeCoordinate { .. })
    ));
    assert!(matches!(
        evaluate_lift_candidate(&before, &point(ri(0), ri(-1), None), true, true),
        Err(GomcError::NegativeCoordinate { .. })
    ));
}

#[test]
fn the_composed_report_is_authority_null_on_every_path() {
    let ledger = ResidualLedger::new(rats(&[3, 1, 0])).unwrap();
    let channel = matrix::from_rows(vec![
        vec![rq(1, 2), rq(1, 2), Rational::zero()],
        vec![Rational::zero(), ri(1), Rational::zero()],
        vec![rq(1, 3), rq(1, 3), rq(1, 3)],
    ])
    .unwrap();
    let current = point(ri(3), ri(3), None);
    let strict = vec![("repair".to_string(), point(ri(0), ri(0), None))];
    let report = gomc_report(
        &ledger,
        &[0, 0, 1],
        2,
        Some(&channel),
        Some((&current, &strict)),
    )
    .unwrap();
    assert_eq!(report.observed_weights(), &[ri(1), Rational::zero()]);
    assert_eq!(
        report.pushed_weights().unwrap(),
        &[rq(3, 8), rq(5, 8), Rational::zero()]
    );
    assert_eq!(report.branch().unwrap().ranking, vec![0]);
    assert_eq!(report.authority_effect(), ReportAuthorityTag::None);
    let plain = gomc_report(&ledger, &[0, 1, 1], 2, None, None).unwrap();
    assert_eq!(plain.authority_effect(), ReportAuthorityTag::None);
    assert!(matches!(
        gomc_report(&ledger, &[0, 0, 5], 2, None, None),
        Err(GomcError::ObserverLabel {
            label: 5,
            classes: 2
        })
    ));
    // The class count is bounded by the states before anything is allocated.
    assert!(matches!(
        gomc_report(&ledger, &[0, 0, 1], usize::MAX, None, None),
        Err(GomcError::ClassCount {
            classes: usize::MAX,
            states: 3
        })
    ));
}
