//! Diagonal densities read off residual sector weights: every ledger is a
//! state, its purity is one exactly on single-sector ledgers, scalar multiples
//! give one density, and the diagonal belongs to the declared sector basis.

use finite_qm_native::campaigns::residual_density_calculus::ResidualLedger;
use linear_algebra::exact_field::matrix;
use num_traits::Zero;
use omega_number_theory::cyclotomic::GaussianRat;
use omega_number_theory::rational::{ri, rq, Rational};
use omega_quantum_physics::exact_hermitian::{self, gq};
use omega_quantum_physics::residual_density_calculus::{
    conjugate, sector_measurement, ResidualDensityError,
};

fn rats(values: &[i64]) -> Vec<Rational> {
    values.iter().map(|v| ri(*v)).collect()
}

#[test]
fn the_worked_example_gives_a_mixed_and_a_pure_diagonal_density() {
    let mixed = ResidualLedger::new(rats(&[3, 1])).unwrap();
    assert_eq!(
        mixed.diagonal_density(),
        matrix::diagonal(&[gq(3, 4, 0, 1), gq(1, 4, 0, 1)]).unwrap()
    );
    assert_eq!(mixed.purity(), rq(5, 8));
    assert_eq!(ri(1) - mixed.purity(), rq(3, 8));
    let pure = ResidualLedger::new(rats(&[4, 0])).unwrap();
    assert_eq!(pure.weights(), rats(&[1, 0]));
    assert_eq!(pure.purity(), ri(1));
}

#[test]
fn every_small_ledger_is_a_state_whose_purity_is_one_exactly_on_one_sector() {
    // Every ledger with masses 0..=3 on one, two or three sectors.
    let mut checked = 0;
    for sectors in 1..=3u32 {
        for code in 0..4usize.pow(sectors) {
            let masses: Vec<Rational> = (0..sectors)
                .map(|k| ri(((code / 4usize.pow(k)) % 4) as i64))
                .collect();
            let Ok(ledger) = ResidualLedger::new(masses.clone()) else {
                assert!(
                    masses.iter().all(Zero::is_zero),
                    "only the zero ledger is refused"
                );
                continue;
            };
            let rho = ledger.diagonal_density();
            assert!(exact_hermitian::is_positive_semidefinite(&rho));
            assert_eq!(matrix::trace(&rho).unwrap(), GaussianRat::one());
            let purity = ledger.purity();
            assert_eq!(
                matrix::trace(&matrix::multiply(&rho, &rho).unwrap())
                    .unwrap()
                    .re,
                purity
            );
            assert!(purity > ri(0) && purity <= ri(1));
            let support = masses.iter().filter(|m| !m.is_zero()).count();
            assert_eq!(purity == ri(1), support == 1);
            checked += 1;
        }
    }
    assert_eq!(checked, 3 + 15 + 63);
}

#[test]
fn scalar_multiples_give_one_density_and_other_distributions_do_not() {
    let base = ResidualLedger::new(rats(&[3, 1]))
        .unwrap()
        .diagonal_density();
    for k in [2, 5, 7] {
        assert_eq!(
            ResidualLedger::new(rats(&[3 * k, k]))
                .unwrap()
                .diagonal_density(),
            base
        );
    }
    assert_ne!(
        ResidualLedger::new(rats(&[1, 3]))
            .unwrap()
            .diagonal_density(),
        base
    );
    assert_ne!(
        ResidualLedger::new(rats(&[2, 2]))
            .unwrap()
            .diagonal_density(),
        base
    );
}

#[test]
fn the_diagonal_is_relative_to_the_declared_sector_basis() {
    let rho = ResidualLedger::new(rats(&[3, 1]))
        .unwrap()
        .diagonal_density();
    let rotation = matrix::from_rows(vec![
        vec![gq(3, 5, 0, 1), gq(-4, 5, 0, 1)],
        vec![gq(4, 5, 0, 1), gq(3, 5, 0, 1)],
    ])
    .unwrap();
    let rotated = conjugate(&rotation, &rho).unwrap();
    // A non-unitary or mis-sized conjugator is refused.
    assert_eq!(
        conjugate(&matrix::scale(&rotation, &gq(2, 1, 0, 1)).unwrap(), &rho),
        Err(ResidualDensityError::NotUnitary)
    );
    assert_eq!(
        conjugate(&matrix::identity(3).unwrap(), &rho),
        Err(ResidualDensityError::Shape)
    );
    // The same state read in the rotated basis: new populations and a coherence.
    assert_eq!(
        sector_measurement(&rotated).unwrap(),
        vec![rq(43, 100), rq(57, 100)]
    );
    assert_eq!(rotated.get_ref(0, 1).unwrap().re, rq(6, 25));
    // Its purity tr(rho^2) is basis independent; the purity of its diagonal is not.
    assert_eq!(
        matrix::trace(&matrix::multiply(&rotated, &rotated).unwrap())
            .unwrap()
            .re,
        rq(5, 8)
    );
    let diagonal_purity: Rational = sector_measurement(&rotated)
        .unwrap()
        .iter()
        .map(|p| p * p)
        .sum();
    assert_eq!(diagonal_purity, rq(2549, 5000));
}
