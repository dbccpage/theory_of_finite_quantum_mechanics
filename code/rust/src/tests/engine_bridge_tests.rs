// AuthorityEffect: None. Citation: sealed-derivation-v1 (3100c4e)

use finite_qm_native::campaigns::born_gleason::{FrameFunction, GleasonAssumptions};
use finite_qm_native::campaigns::engine_bridge::*;
use linear_algebra::backend::basic_matrix::BasicMatrix;
use omega_number_theory::rational::Rational;
use omega_quantum_physics::composition_tomography::PhaseCarrier;
use omega_quantum_physics::engine_bridge::domain_diagonal_to_prod_density;

#[test]
fn test_engine_bridge_d2_states() {
    let rep_ground = verify_exact_state_with_engine("ground", 2).expect("d=2 ground state");
    assert!(rep_ground.diagnostic_trace_matches);
    assert!(rep_ground.expected_pure);
    assert!(rep_ground.purity_matches_expectation);
    assert!((rep_ground.observables.purity - 1.0).abs() < 1e-5);
    assert!(rep_ground.observables.von_neumann_entropy < 1e-5);

    let rep_sup =
        verify_exact_state_with_engine("superposition", 2).expect("d=2 superposition state");
    assert!(rep_sup.diagnostic_trace_matches);
    assert!(rep_sup.expected_pure);
    assert!(rep_sup.purity_matches_expectation);
    assert!((rep_sup.observables.purity - 1.0).abs() < 1e-5);
}

#[test]
fn test_engine_bridge_d3_states() {
    let rep_ground = verify_exact_state_with_engine("ground", 3).expect("d=3 ground state");
    assert!(rep_ground.diagnostic_trace_matches);
    assert!(rep_ground.expected_pure);
    assert!(rep_ground.purity_matches_expectation);
    assert!((rep_ground.observables.purity - 1.0).abs() < 1e-5);

    let rep_magic = verify_exact_state_with_engine("magic", 3).expect("d=3 magic state");
    assert!(rep_magic.diagnostic_trace_matches);
    assert!(rep_magic.expected_pure);
    assert!(rep_magic.purity_matches_expectation);
    assert!((rep_magic.observables.purity - 1.0).abs() < 1e-5);

    let rep_mixed = verify_exact_state_with_engine("mixed", 3).expect("d=3 mixed state");
    assert!(rep_mixed.diagnostic_trace_matches);
    assert!(!rep_mixed.expected_pure);
    assert!(rep_mixed.purity_matches_expectation);
    assert!(rep_mixed.observables.purity < 0.9);
    assert!(rep_mixed.observables.von_neumann_entropy > 0.1);
}

#[test]
fn test_engine_bridge_d4_states() {
    let rep_ground = verify_exact_state_with_engine("ground", 4).expect("d=4 ground state");
    assert!(rep_ground.diagnostic_trace_matches);
    assert!(rep_ground.expected_pure);
    assert!(rep_ground.purity_matches_expectation);

    let rep_bell = verify_exact_state_with_engine("bell", 4).expect("d=4 Bell state");
    assert!(rep_bell.diagnostic_trace_matches);
    assert!(rep_bell.expected_pure);
    assert!(rep_bell.purity_matches_expectation);
    assert!((rep_bell.observables.purity - 1.0).abs() < 1e-4);

    let rep_mixed = verify_exact_state_with_engine("mixed", 4).expect("d=4 mixed state");
    assert!(rep_mixed.diagnostic_trace_matches);
    assert!(!rep_mixed.expected_pure);
    assert!(rep_mixed.purity_matches_expectation);
    assert!(rep_mixed.observables.purity < 0.9);
}

#[test]
fn test_engine_bridge_domain_diagonal_density() {
    let h_space = omega_quantum_physics::hilbert_space::HilbertSpace::new(4, "H4");
    let r_fourth = num_rational::Ratio::new(1, 4);
    let domain_dm = omega_quantum_physics::density_matrix::DensityMatrix::try_from_rational_probs(
        &h_space,
        vec![r_fourth, r_fourth, r_fourth, r_fourth],
        "maximally_mixed_d4",
    )
    .expect("domain density matrix");

    let prod_dm = domain_diagonal_to_prod_density(&domain_dm, None).expect("prod density");
    let obs = evaluate_state_observables(&prod_dm);
    assert!((obs.trace - 1.0).abs() < 1e-6);
    assert!((obs.purity - 0.25).abs() < 1e-5);
    assert!(!obs.is_pure);
    assert!((obs.von_neumann_entropy - (4.0f64).ln()).abs() < 1e-4);
}

fn r(n: i64, d: i64) -> Rational {
    Rational::new(n.into(), d.into())
}

fn rational_matrix(n: usize, entries: &[(i64, i64)]) -> BasicMatrix<Rational> {
    BasicMatrix::from_row_major(n, n, entries.iter().map(|&(p, q)| r(p, q)).collect())
        .expect("declared rational fixture")
}

fn paid(dimension: usize) -> GleasonAssumptions {
    GleasonAssumptions {
        dimension,
        noncontextual: true,
        finite_additivity: true,
        complex_scalars: true,
        no_silent_continuum: true,
    }
}

#[test]
fn test_engine_bridge_domain_derivation_targets() {
    // A coherent qutrit state: the engine's classical projection reads its exact Born weights.
    let rho = rational_matrix(
        3,
        &[
            (1, 2),
            (1, 4),
            (0, 1),
            (1, 4),
            (1, 3),
            (0, 1),
            (0, 1),
            (0, 1),
            (1, 6),
        ],
    );
    assert!(verify_born_gleason_domain_bridge(&rho, &paid(3)).expect("born gleason bridge"));
    // The comparison can fail: a projection off by 1e-9 in one weight does not match.
    let frame = FrameFunction::try_new(vec![r(1, 2), r(1, 3), r(1, 6)]).unwrap();
    assert!(born_weights_match_projection(
        &frame,
        &[0.5, 1.0 / 3.0, 1.0 / 6.0],
        BORN_BRIDGE_TOLERANCE
    ));
    assert!(!born_weights_match_projection(
        &frame,
        &[0.5, 1.0 / 3.0 + 1e-9, 1.0 / 6.0],
        BORN_BRIDGE_TOLERANCE
    ));
    assert!(!born_weights_match_projection(
        &frame,
        &[0.5, 0.5],
        BORN_BRIDGE_TOLERANCE
    ));

    // Local tomography: complex products span, real products do not, and the count agrees with the rank.
    assert!(
        verify_composition_tomography_domain_bridge(2, 2, PhaseCarrier::ComplexU1)
            .expect("complex 2x2")
    );
    assert!(
        verify_composition_tomography_domain_bridge(2, 3, PhaseCarrier::ComplexU1)
            .expect("complex 2x3")
    );
    assert!(
        !verify_composition_tomography_domain_bridge(2, 2, PhaseCarrier::RealOnly)
            .expect("real 2x2")
    );
    assert!(
        verify_composition_tomography_domain_bridge(1, 3, PhaseCarrier::RealOnly)
            .expect("real 1x3")
    );
}

#[test]
fn test_engine_bridge_domain_derivation_refusals() {
    let rho = rational_matrix(
        3,
        &[
            (1, 2),
            (0, 1),
            (0, 1),
            (0, 1),
            (1, 3),
            (0, 1),
            (0, 1),
            (0, 1),
            (1, 6),
        ],
    );
    // Unpaid assumptions refuse before anything is compared.
    let mut contextual = paid(3);
    contextual.noncontextual = false;
    assert!(verify_born_gleason_domain_bridge(&rho, &contextual).is_err());
    let qubit = rational_matrix(2, &[(1, 2), (0, 1), (0, 1), (1, 2)]);
    assert!(verify_born_gleason_domain_bridge(&qubit, &paid(2)).is_err());
    // A state of the wrong size, and weights that are not a probability vector.
    assert!(verify_born_gleason_domain_bridge(&qubit, &paid(3)).is_err());
    let negative = rational_matrix(
        3,
        &[
            (3, 2),
            (0, 1),
            (0, 1),
            (0, 1),
            (-1, 3),
            (0, 1),
            (0, 1),
            (0, 1),
            (-1, 6),
        ],
    );
    assert!(verify_born_gleason_domain_bridge(&negative, &paid(3)).is_err());
    assert!(verify_composition_tomography_domain_bridge(0, 2, PhaseCarrier::ComplexU1).is_err());
    assert!(verify_composition_tomography_domain_bridge(2, 0, PhaseCarrier::RealOnly).is_err());
}
