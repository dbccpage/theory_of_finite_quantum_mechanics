//! Measurement as conditioning on a declared outcome sector: collapse,
//! idempotence, repeatability and the Born share, checked exhaustively on
//! small ledgers; agreement with the Lüders rule on diagonal densities; and the
//! two things conditioning does not describe, within-sector coherence and
//! incompatible measurements.

use finite_qm_native::campaigns::residual_density_calculus::ResidualLedger;
use finite_qm_native::campaigns::sector_conditioning::{condition, sector_probability};
use linear_algebra::exact_field::matrix;
use num_traits::Zero;
use omega_number_theory::rational::{ri, rq, Rational};
use omega_quantum_physics::exact_hermitian::gq;

use omega_quantum_physics::sector_conditioning::{
    luders_update, sector_projector, ConditioningError,
};

fn rats(values: &[i64]) -> Vec<Rational> {
    values.iter().map(|v| ri(*v)).collect()
}

/// Every ledger with masses 0..=3 on three outcomes and positive total.
fn ledgers() -> Vec<ResidualLedger> {
    (0..64usize)
        .filter_map(|code| {
            ResidualLedger::new((0..3).map(|k| ri(((code >> (2 * k)) & 3) as i64)).collect()).ok()
        })
        .collect()
}

/// Every nonempty sector of three outcomes.
fn sectors() -> Vec<Vec<bool>> {
    (1..8usize)
        .map(|code| (0..3).map(|k| code >> k & 1 == 1).collect())
        .collect()
}

#[test]
fn the_worked_example_collapses_repeats_and_reads_its_born_share() {
    let ledger = ResidualLedger::new(rats(&[3, 1])).unwrap();
    let sector = [false, true];
    assert_eq!(sector_probability(&ledger, &sector).unwrap(), rq(1, 4));
    let after = condition(&ledger, &sector).unwrap();
    assert_eq!(after.masses(), &rats(&[0, 1])[..]);
    assert_eq!(condition(&after, &sector).unwrap(), after);
    assert_eq!(sector_probability(&after, &sector).unwrap(), ri(1));
    // The off-sector share the update removes.
    assert_eq!(
        ri(1) - sector_probability(&ledger, &sector).unwrap(),
        rq(3, 4)
    );
}

#[test]
fn conditioning_collapses_is_idempotent_repeatable_and_reads_the_sector_weight() {
    let mut checked = 0;
    for ledger in ledgers() {
        for sector in sectors() {
            let weight: Rational = ledger
                .masses()
                .iter()
                .zip(&sector)
                .filter(|(_, s)| **s)
                .map(|(m, _)| m.clone())
                .sum();
            assert_eq!(
                sector_probability(&ledger, &sector).unwrap(),
                &weight / ledger.total()
            );
            let Ok(after) = condition(&ledger, &sector) else {
                assert!(weight.is_zero(), "only a null sector is refused");
                continue;
            };
            assert!(after
                .masses()
                .iter()
                .zip(&sector)
                .all(|(m, s)| *s || m.is_zero()));
            assert_eq!(condition(&after, &sector).unwrap(), after);
            assert_eq!(sector_probability(&after, &sector).unwrap(), ri(1));
            // Weights already normalized on the sector are the fixed points.
            let fixed = ledger.total() == weight && ledger.total() == ri(1);
            assert_eq!(fixed, after == ledger);
            checked += 1;
        }
    }
    assert!(checked > 300);
}

#[test]
fn refining_sectors_compose_and_different_partitions_give_different_updates() {
    let ledger = ResidualLedger::new(rats(&[3, 1, 2])).unwrap();
    let coarse = [true, true, false];
    let fine = [false, true, false];
    let composed = condition(&condition(&ledger, &coarse).unwrap(), &fine).unwrap();
    assert_eq!(composed, condition(&ledger, &fine).unwrap());
    // The same weights under two declared observables.
    let other = [false, true, true];
    assert_eq!(
        condition(&ledger, &coarse).unwrap().masses(),
        &[rq(3, 4), rq(1, 4), ri(0)][..]
    );
    assert_eq!(
        condition(&ledger, &other).unwrap().masses(),
        &[ri(0), rq(1, 3), rq(2, 3)][..]
    );
}

#[test]
fn on_diagonal_densities_conditioning_is_the_luders_rule() {
    for ledger in ledgers() {
        for sector in sectors() {
            let rho = ledger.diagonal_density();
            match (
                condition(&ledger, &sector),
                luders_update(&rho, &sector_projector(&sector).unwrap()),
            ) {
                (Ok(after), Ok(updated)) => assert_eq!(updated, after.diagonal_density()),
                (Err(ConditioningError::NullSector), Err(ConditioningError::NullSector)) => {}
                other => panic!("conditioning and the Lüders rule disagree: {other:?}"),
            }
        }
    }
}

#[test]
fn the_luders_rule_keeps_coherence_inside_the_sector_that_weights_cannot_carry() {
    // |psi> = (1, 1, 1)/sqrt 3 has the rational density J/3.
    let third = gq(1, 3, 0, 1);
    let rho = matrix::from_rows(vec![vec![third.clone(); 3]; 3]).unwrap();
    let sector = [true, true, false];
    let updated = luders_update(&rho, &sector_projector(&sector).unwrap()).unwrap();
    let half = gq(1, 2, 0, 1);
    let zero = gq(0, 1, 0, 1);
    assert_eq!(
        updated,
        matrix::from_rows(vec![
            vec![half.clone(), half.clone(), zero.clone()],
            vec![half.clone(), half.clone(), zero.clone()],
            vec![zero.clone(), zero.clone(), zero],
        ])
        .unwrap()
    );
    // Conditioning the diagonal gives the same diagonal and no coherence.
    let weights = ResidualLedger::new(vec![rq(1, 3); 3]).unwrap();
    let shadow = condition(&weights, &sector).unwrap().diagonal_density();
    assert_eq!(
        shadow,
        matrix::diagonal(&[half.clone(), half, gq(0, 1, 0, 1)]).unwrap()
    );
    assert_ne!(shadow, updated);
}

#[test]
fn incompatible_projectors_do_not_commute_and_malformed_updates_are_refused() {
    let half = gq(1, 2, 0, 1);
    let zero_projector = sector_projector(&[true, false]).unwrap();
    let plus_projector = matrix::from_rows(vec![vec![half.clone(); 2]; 2]).unwrap();
    let mixed = matrix::scale(&matrix::identity(2).unwrap(), &half).unwrap();
    let z_then_x = luders_update(
        &luders_update(&mixed, &zero_projector).unwrap(),
        &plus_projector,
    )
    .unwrap();
    let x_then_z = luders_update(
        &luders_update(&mixed, &plus_projector).unwrap(),
        &zero_projector,
    )
    .unwrap();
    assert_eq!(z_then_x, plus_projector);
    assert_eq!(x_then_z, zero_projector);
    // Compatible sector projectors commute.
    let a = sector_projector(&[true, true, false]).unwrap();
    let b = sector_projector(&[false, true, true]).unwrap();
    assert_eq!(
        matrix::multiply(&a, &b).unwrap(),
        matrix::multiply(&b, &a).unwrap()
    );
    // Refusals.
    let not_projector = matrix::scale(&matrix::identity(2).unwrap(), &gq(2, 1, 0, 1)).unwrap();
    assert_eq!(
        luders_update(&mixed, &not_projector),
        Err(ConditioningError::NotProjector)
    );
    assert_eq!(
        luders_update(&zero_projector, &sector_projector(&[false, true]).unwrap()),
        Err(ConditioningError::NullSector)
    );
    assert_eq!(
        luders_update(&mixed, &sector_projector(&[true, false, false]).unwrap()),
        Err(ConditioningError::Shape)
    );
    let ledger = ResidualLedger::new(rats(&[3, 1])).unwrap();
    assert_eq!(
        condition(&ledger, &[true]),
        Err(ConditioningError::SectorLength {
            expected: 2,
            actual: 1
        })
    );
    assert_eq!(
        condition(&ResidualLedger::new(rats(&[0, 1])).unwrap(), &[true, false]),
        Err(ConditioningError::NullSector)
    );
}
