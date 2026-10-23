//! The residual density calculus at the L1-to-diagonal-density boundary:
//! normalisation, the diagonal density and its read-back, orientation
//! blindness, phase non-determination, licensed coherence and stochastic
//! pushforward. All exact.

use linear_algebra::backend::basic_matrix::BasicMatrix;
use linear_algebra::exact_field::matrix;
use num_traits::Zero;
use omega_number_theory::cyclotomic::GaussianRat;
use omega_number_theory::rational::{ri, rq, Rational};
use omega_quantum_physics::exact_hermitian::{self, gi, gq};

use finite_qm_native::campaigns::residual_density_calculus::{
    evaluate_coherence, ledger_from_diagonal_density, licensed_coherent_density, ResidualLedger,
};
use omega_quantum_physics::residual_density_calculus::{
    conjugate, row_stochastic_pushforward, sector_measurement, ResidualDensityError,
};

fn rats(values: &[i64]) -> Vec<Rational> {
    values.iter().map(|&v| ri(v)).collect()
}

fn plus_state() -> BasicMatrix<GaussianRat> {
    matrix::from_rows(vec![
        vec![gq(1, 2, 0, 1), gq(1, 2, 0, 1)],
        vec![gq(1, 2, 0, 1), gq(1, 2, 0, 1)],
    ])
    .unwrap()
}

fn minus_state() -> BasicMatrix<GaussianRat> {
    matrix::from_rows(vec![
        vec![gq(1, 2, 0, 1), gq(-1, 2, 0, 1)],
        vec![gq(-1, 2, 0, 1), gq(1, 2, 0, 1)],
    ])
    .unwrap()
}

#[test]
fn the_worked_ledger_normalises_to_a_mixed_diagonal_density() {
    let ledger = ResidualLedger::new(rats(&[3, 1, 0])).unwrap();
    assert_eq!(ledger.weights(), vec![rq(3, 4), rq(1, 4), Rational::zero()]);
    let rho = ledger.diagonal_density();
    assert!(exact_hermitian::is_positive_semidefinite(&rho));
    assert_eq!(matrix::trace(&rho).unwrap(), GaussianRat::one());
    assert_eq!(sector_measurement(&rho).unwrap(), ledger.weights());
    assert_eq!(ledger.purity(), rq(5, 8));
    assert_eq!(
        matrix::trace(&matrix::multiply(&rho, &rho).unwrap())
            .unwrap()
            .re,
        rq(5, 8)
    );
}

#[test]
fn the_report_is_orientation_blind() {
    let a = ResidualLedger::from_signed_residual(&rats(&[2, -3])).unwrap();
    let b = ResidualLedger::from_signed_residual(&rats(&[-2, 3])).unwrap();
    assert_eq!(a, b);
    assert_eq!(a.weights(), vec![rq(2, 5), rq(3, 5)]);
}

#[test]
fn sector_weights_do_not_determine_phase() {
    let plus = plus_state();
    let minus = minus_state();
    assert_eq!(
        sector_measurement(&plus).unwrap(),
        sector_measurement(&minus).unwrap()
    );
    // A rational rotation mixes the two phase witnesses into different weights.
    let rotation = matrix::from_rows(vec![
        vec![gq(3, 5, 0, 1), gq(-4, 5, 0, 1)],
        vec![gq(4, 5, 0, 1), gq(3, 5, 0, 1)],
    ])
    .unwrap();
    assert_eq!(
        sector_measurement(&conjugate(&rotation, &plus).unwrap()).unwrap(),
        vec![rq(1, 50), rq(49, 50)]
    );
    assert_eq!(
        sector_measurement(&conjugate(&rotation, &minus).unwrap()).unwrap(),
        vec![rq(49, 50), rq(1, 50)]
    );
}

#[test]
fn a_diagonal_density_reads_back_as_a_ledger_and_normalised_ledgers_are_fixed() {
    let ledger = ResidualLedger::new(rats(&[3, 1, 0])).unwrap();
    let back = ledger_from_diagonal_density(&ledger.diagonal_density()).unwrap();
    assert_eq!(back.masses(), ledger.weights().as_slice());
    assert_eq!(back.weights(), back.masses());
    // Refusals: coherence, negativity, wrong trace.
    assert!(matches!(
        ledger_from_diagonal_density(&plus_state()),
        Err(ResidualDensityError::OffDiagonal { row: 0, col: 1 })
    ));
    let negative = matrix::diagonal(&[gq(3, 2, 0, 1), gq(-1, 2, 0, 1)]).unwrap();
    assert_eq!(
        ledger_from_diagonal_density(&negative),
        Err(ResidualDensityError::NotADensity)
    );
    let heavy = matrix::diagonal(&[gi(1, 0), gi(1, 0)]).unwrap();
    assert_eq!(
        ledger_from_diagonal_density(&heavy),
        Err(ResidualDensityError::NotADensity)
    );
}

#[test]
fn coherence_is_admitted_only_under_a_complete_license() {
    let ledger = ResidualLedger::new(rats(&[1, 1])).unwrap();
    assert_eq!(
        licensed_coherent_density(&ledger, plus_state(), true),
        Ok(plus_state())
    );
    // Without a declared observer basis the same matrix is refused.
    let refused = licensed_coherent_density(&ledger, plus_state(), false).unwrap_err();
    assert!(!refused.observer_basis_declared() && refused.psd_condition_satisfied());
    // A phase relation alone is not enough: too much coherence breaks PSD.
    let too_coherent = matrix::from_rows(vec![
        vec![gq(1, 2, 0, 1), gi(1, 0)],
        vec![gi(1, 0), gq(1, 2, 0, 1)],
    ])
    .unwrap();
    let license = evaluate_coherence(&ledger, &too_coherent, true);
    assert!(
        license.phase_relation_declared()
            && !license.psd_condition_satisfied()
            && !license.is_licensed()
    );
    // Changing the diagonal breaks sector identity.
    let shifted = matrix::from_rows(vec![
        vec![gi(1, 0), gq(0, 1, 0, 1)],
        vec![gq(0, 1, 0, 1), gi(0, 0)],
    ])
    .unwrap();
    assert!(!evaluate_coherence(&ledger, &shifted, true).sector_identity_preserved());
    // The plain diagonal density declares no phase at all.
    assert!(
        !evaluate_coherence(&ledger, &ledger.diagonal_density(), true).phase_relation_declared()
    );
}

#[test]
fn a_row_stochastic_channel_preserves_mass_and_nonnegativity() {
    let masses = rats(&[3, 1, 0]);
    let channel = matrix::from_rows(vec![
        vec![rq(1, 2), rq(1, 2), Rational::zero()],
        vec![Rational::zero(), ri(1), Rational::zero()],
        vec![rq(1, 3), rq(1, 3), rq(1, 3)],
    ])
    .unwrap();
    let out = row_stochastic_pushforward(&channel, &masses).unwrap();
    assert_eq!(out, vec![rq(3, 2), rq(5, 2), Rational::zero()]);
    assert_eq!(
        out.iter().sum::<Rational>(),
        masses.iter().sum::<Rational>()
    );
    let negative = matrix::from_rows(vec![vec![rq(3, 2), rq(-1, 2)], vec![ri(0), ri(1)]]).unwrap();
    assert_eq!(
        row_stochastic_pushforward(&negative, &rats(&[1, 1])),
        Err(ResidualDensityError::NotRowStochastic { row: 0 })
    );
    let leaky = matrix::from_rows(vec![vec![rq(1, 2), rq(1, 4)], vec![ri(0), ri(1)]]).unwrap();
    assert_eq!(
        row_stochastic_pushforward(&leaky, &rats(&[1, 1])),
        Err(ResidualDensityError::NotRowStochastic { row: 0 })
    );
}

#[test]
fn ledgers_refuse_empty_negative_and_zero_mass() {
    assert_eq!(
        ResidualLedger::new(vec![]),
        Err(ResidualDensityError::Empty)
    );
    assert_eq!(
        ResidualLedger::new(rats(&[1, -1])),
        Err(ResidualDensityError::NegativeMass { index: 1 })
    );
    assert_eq!(
        ResidualLedger::new(rats(&[0, 0])),
        Err(ResidualDensityError::ZeroTotalMass)
    );
}
