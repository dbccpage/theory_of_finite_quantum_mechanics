// AuthorityEffect: None. Citation: sealed-derivation-v1 (3100c4e)

//! Integration tests for `finite_qm` under `omega_quantum_physics`.
//!
//! Validates the full algebraic pipeline:
//! - Target 22: Maximal discrete MUBs in d=3 and exact linear inversion state tomography.
//! - Target 13: Discrete Gross Wigner phase space in d=5, covariance, and magic negativity.
//! - Target 19: Finite Stone-von Neumann and commutator trace obstruction Tr([Q, P]) = 0.
//! - Cyclotomic embeddings and exact rational arithmetic.

use finite_qm_native::campaigns::carrier::{
    carrier_d3_mub_tomography, carrier_d5_wigner_phase_space,
    carrier_finite_commutator_obstruction, DiscreteCarrierStatus,
};
use finite_qm_native::run_finite_qm_verification_suite;
use linear_algebra::backend::basic_matrix::BasicMatrix;
use linear_algebra::exact_field::matrix;
use omega_number_theory::cyclotomic_field::CyclotomicNumber;
use omega_number_theory::cyclotomic_ordered::standard_real_sign;
use omega_number_theory::{
    r_zero, ri, rq, Cyc12, Cyc24, Cyc5, Cyc8, EisensteinRat, GaussianRat, Rational,
};
use omega_quantum_physics::commutator::{
    audit_commutator_obstruction_d3, discrete_momentum_d3, discrete_position_d3,
    verify_trace_cyclicity_d3,
};
use omega_quantum_physics::mub::MubSystem;
use omega_quantum_physics::tomography::{
    state_cyclotomic_coherence_d3, state_mixed_rational_d3, ExactStateTomographerSystem,
};
use omega_quantum_physics::wigner::{state_ground_d5, state_magic_d5, DiscreteWignerSystemD5};

#[test]
fn test_integration_full_suite_report() {
    let report = run_finite_qm_verification_suite();
    assert!(report.d3_mub_exhaustive);
    assert!(report.d3_tomography_ground_state_verified);
    assert!(report.d3_tomography_magic_state_verified);
    assert!(report.d3_tomography_mixed_state_verified);
    assert!(report.d4_mub_exhaustive);
    assert!(report.d4_tomography_bell_state_verified);
    assert!(report.clifton_kent_all_1024_non_psd_certified);
    assert!(report.d5_wigner_algebra_verified);
    assert!(report.d5_magic_state_negativity_witnessed);
    assert_eq!(report.d5_magic_point_value, rq(-1, 5));
    assert!(report.commutator_trace_obstruction_verified);
}

#[test]
fn test_integration_target22_mub_orthogonality_and_unbiasedness() {
    let mub = MubSystem::mub_d3();

    // 4 bases, each with 3 states
    assert_eq!(mub.bases.len(), 4);
    for b in 0..4 {
        assert_eq!(mub.bases[b].len(), 3);
    }

    assert!(mub.verify_hermiticity());
    assert!(mub.verify_idempotence());
    assert!(mub.verify_rank_one_trace());
    assert!(mub.verify_same_basis_orthogonality());
    assert!(mub.verify_resolution_of_identity());
    assert!(mub.verify_cross_basis_unbiasedness());
}

#[test]
fn test_integration_target22_exact_tomography_all_computational_states() {
    let tomographer =
        ExactStateTomographerSystem::new(omega_quantum_physics::mub::MubSystem::mub_d3());

    for k in 0..3 {
        let mut rho_k = matrix::zeros(3, 3).unwrap();
        rho_k.set(k, k, Cyc24::one()).unwrap();
        assert!(tomographer.verify_exact_reconstruction(&rho_k));
    }
}

#[test]
fn test_integration_target22_exact_tomography_coherent_phase_states() {
    let tomographer =
        ExactStateTomographerSystem::new(omega_quantum_physics::mub::MubSystem::mub_d3());

    // Pure state |psi> = 1/sqrt(3)(|0> + zeta_3 |1> + zeta_3^2 |2>)
    // (This is one of the MUB states in Basis 1, index 1)
    let rho_phase = mub_state_density(1, 1);
    assert!(tomographer.verify_exact_reconstruction(&rho_phase));

    // Complex density matrix with cyclotomic coherence
    let rho_coh = state_cyclotomic_coherence_d3();
    assert!(tomographer.verify_exact_reconstruction(&rho_coh));
}

fn mub_state_density(basis: usize, index: usize) -> BasicMatrix<Cyc24> {
    let mub = MubSystem::mub_d3();
    mub.try_projector(basis, index).unwrap().clone()
}

#[test]
fn test_integration_target22_exact_tomography_convex_combinations() {
    let tomographer =
        ExactStateTomographerSystem::new(omega_quantum_physics::mub::MubSystem::mub_d3());

    // Convex combination: rho = 1/2 |0><0| + 1/3 |1><1| + 1/6 |2><2|
    let rho_mixed = state_mixed_rational_d3();
    let probs = tomographer.try_measure_state(&rho_mixed).unwrap();
    assert!(probs.iter().all(|basis| basis
        .iter()
        .fold(Cyc24::zero(), |sum, value| sum.add(value))
        == Cyc24::one()));

    let rho_reconstructed = tomographer.try_reconstruct_state(&probs).unwrap();
    assert_eq!(rho_reconstructed, rho_mixed);
}

#[test]
fn test_integration_target13_d5_phase_point_operators_algebra() {
    let wsys = DiscreteWignerSystemD5::new();

    assert!(wsys.verify_hermiticity());
    assert!(wsys.verify_unit_trace());
    assert!(wsys.verify_orthogonality());
    assert!(wsys.verify_resolution());
    assert!(wsys.verify_gross_covariance());
}

#[test]
fn test_integration_target13_d5_magic_state_point_negativity() {
    let wsys = DiscreteWignerSystemD5::new();
    let rho_magic = state_magic_d5();

    let grid = wsys
        .evaluate_exact(&rho_magic)
        .expect("declared exact Wigner fixture");

    // Only the origin is projected to Q; other real entries retain their field coordinates.
    assert_eq!(
        CyclotomicNumber::from(&grid[0][0]).as_rational(),
        Some(rq(-1, 5))
    );
    assert_eq!(
        wsys.evaluate_wigner(&rho_magic),
        Err(omega_quantum_physics::wigner::WignerError::NonRational)
    );

    // Unit sum normalization in the full exact field.
    let sum = grid
        .iter()
        .flatten()
        .fold(Cyc5::zero(), |sum, value| sum.add(value));
    assert_eq!(sum, Cyc5::one());

    // The standard embedding sign is checked for every exact real point.
    let signs = grid
        .iter()
        .flatten()
        .map(|value| standard_real_sign(&CyclotomicNumber::from(value)))
        .collect::<Result<Vec<_>, _>>()
        .expect("the exact Wigner grid is real in the declared embedding");
    assert!(signs.iter().any(|&sign| sign < 0));
}

#[test]
fn test_integration_target13_d5_stabilizer_state_wigner_positivity() {
    let wsys = DiscreteWignerSystemD5::new();

    // Check ground stabilizer state |0><0|
    let rho_ground = state_ground_d5();
    let grid_ground = wsys
        .evaluate_wigner(&rho_ground)
        .expect("declared rational Wigner fixture");

    for row in &grid_ground {
        for val in row {
            assert!(val >= &r_zero());
        }
    }

    let sum_ground: Rational = grid_ground.iter().flat_map(|r| r.iter()).cloned().sum();
    assert_eq!(sum_ground, ri(1));
}

#[test]
fn test_integration_target19_trace_obstruction_and_stone_von_neumann() {
    let report = audit_commutator_obstruction_d3().unwrap();

    // 1. Commutator trace is exactly zero
    assert!(report.commutator_trace_is_zero);

    // 2. Canonical commutation relation [Q, P] = i*N is obstructed
    assert!(report.hypothetical_ccr_trace_non_zero);

    // 3. Weyl group form Z X = omega X Z is satisfied
    assert!(report.weyl_relation_satisfied);

    // 4. Trace of Weyl commutator is identically zero
    assert!(report.weyl_commutator_trace_is_zero);

    // Discrete position and momentum operators have trace zero commutator
    let q = discrete_position_d3();
    let p = discrete_momentum_d3().unwrap();
    let (tr_qp, is_zero) = verify_trace_cyclicity_d3(&q, &p).unwrap();
    assert!(is_zero);
    assert_eq!(tr_qp, Cyc24::zero());
}

#[test]
fn test_integration_cyclotomic_fields_and_subrings() {
    // 1. Gaussian integers Z[i]
    let g1 = GaussianRat::from_ints(1, 2);
    let g2 = GaussianRat::from_ints(3, -1);
    let g_prod = g1.mul(&g2);
    assert_eq!(g_prod, GaussianRat::from_ints(5, 5));
    assert!(g_prod.is_integer_ring_element());

    // 2. Eisenstein integers Z[zeta_3]
    let e1 = EisensteinRat::zeta3();
    let e2 = EisensteinRat::zeta3_sq();
    let e_prod = e1.mul(&e2);
    assert_eq!(e_prod, EisensteinRat::one());

    // 3. 8th cyclotomic field sqrt(2) identity: (zeta_8 + zeta_8^7)^2 = 2
    let z8 = Cyc8::zeta8(1);
    let z8_conj = Cyc8::zeta8(7);
    let sqrt2 = z8.add(&z8_conj);
    let two = sqrt2.mul(&sqrt2);
    assert_eq!(two.a[0], rq(2, 1));
    assert_eq!(two.a[1], rq(0, 1));
    assert_eq!(two.a[2], rq(0, 1));
    assert_eq!(two.a[3], rq(0, 1));

    // 4. 12th cyclotomic field: zeta_12^3 = i, zeta_12^4 = zeta_3
    let z12 = Cyc12::zeta12(1);
    let i_12 = z12.mul(&z12).mul(&z12);
    assert_eq!(i_12, Cyc12::i());

    // 5. 5th cyclotomic field: 1 + zeta_5 + zeta_5^2 + zeta_5^3 + zeta_5^4 = 0
    let sum5 = (0..5).fold(Cyc5::zero(), |acc, k| acc.add(&Cyc5::zeta5(k)));
    assert!(sum5.is_zero());

    // 6. Cyc24 ambient unification
    let i_24 = Cyc24::i();
    let z3_24 = Cyc24::zeta3();
    let z8_24 = Cyc24::zeta8();
    let z12_24 = Cyc24::zeta12();

    assert_eq!(i_24.mul(&i_24), Cyc24::one().neg());
    assert_eq!(z3_24.mul(&z3_24).mul(&z3_24), Cyc24::one());
    assert_eq!(z8_24.mul(&z8_24), i_24);
    assert_eq!(z12_24.mul(&z12_24), Cyc24::zeta24(4));
}

#[test]
fn test_integration_carrier_declarations() {
    // The property-name inventory is declarative; verification runs in the physical tests.
    let c3 = carrier_d3_mub_tomography();
    assert_eq!(c3.dimension, 3);
    assert_eq!(c3.status, DiscreteCarrierStatus::Declared);
    assert!(c3.verified_properties.len() >= 6);

    let c5 = carrier_d5_wigner_phase_space();
    assert_eq!(c5.dimension, 5);
    assert_eq!(c5.status, DiscreteCarrierStatus::Declared);
    assert!(c5.verified_properties.len() >= 6);

    let c_obs = carrier_finite_commutator_obstruction(3);
    assert_eq!(c_obs.dimension, 3);
    assert_eq!(c_obs.status, DiscreteCarrierStatus::Declared);
}

#[test]
fn test_integration_target22_d4_mub_galois_field_and_clifton_kent_obstruction() {
    let mub4 = MubSystem::mub_d4();
    assert_eq!(mub4.bases.len(), 5);
    for b in 0..5 {
        assert_eq!(mub4.bases[b].len(), 4);
    }
    assert!(mub4.verify_hermiticity());
    assert!(mub4.verify_idempotence());
    assert!(mub4.verify_rank_one_trace());
    assert!(mub4.verify_same_basis_orthogonality());
    assert!(mub4.verify_resolution_of_identity());
    assert!(mub4.verify_cross_basis_unbiasedness());
    assert!(mub4.verify_clifton_kent_purity_obstruction());
}
