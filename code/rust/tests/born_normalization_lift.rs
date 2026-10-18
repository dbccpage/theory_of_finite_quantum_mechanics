//! Born normalization and the conditional Hilbert lift: direct normalization
//! of sector weights, l1 as the additive aggregation norm, row-sparse descent,
//! and the phase-averaged shadow as dephasing, all exact.

use finite_qm_native::campaigns::residual_density_calculus::ResidualLedger;
use linear_algebra::backend::basic_matrix::BasicMatrix;
use linear_algebra::exact_field::{involution, matrix};
use num_traits::{Signed, Zero};
use omega_number_theory::cyclotomic::GaussianRat;
use omega_number_theory::rational::{ri, rq, Rational};
use omega_quantum_physics::exact_hermitian::{gi, gq};
use omega_quantum_physics::phase_blind_quotient::{classify_descent, Descent, UnitPhaseGroup};
use omega_solvers::data_cochain_packet::FiniteCochainPacket;

use omega_quantum_physics::phase_averaged_shadow::{
    averages_to_dephasing, phase_group_average, ShadowError, AVERAGE_BUDGET,
};

fn rats(values: &[i64]) -> Vec<Rational> {
    values.iter().map(|v| ri(*v)).collect()
}

fn group(elements: Vec<GaussianRat>) -> UnitPhaseGroup {
    UnitPhaseGroup::new(elements).unwrap()
}

fn signs() -> UnitPhaseGroup {
    group(vec![gi(1, 0), gi(-1, 0)])
}

fn quarter_turns() -> UnitPhaseGroup {
    group(vec![gi(1, 0), gi(0, 1), gi(-1, 0), gi(0, -1)])
}

// ---------------------------------------------------------------------------
// Theorems 1 and 2: normalization and additive aggregation
// ---------------------------------------------------------------------------

#[test]
fn direct_normalization_is_a_unit_sum_ray_invariant_and_idempotent() {
    let weights = ResidualLedger::new(rats(&[2, 1, 1])).unwrap().weights();
    assert_eq!(weights, vec![rq(1, 2), rq(1, 4), rq(1, 4)]);
    assert_eq!(weights.iter().sum::<Rational>(), ri(1));
    assert_eq!(
        ResidualLedger::new(weights.clone()).unwrap().weights(),
        weights
    );
    assert_eq!(
        ResidualLedger::new(rats(&[6, 3, 3])).unwrap().weights(),
        weights
    );
    assert_ne!(
        ResidualLedger::new(rats(&[1, 2, 1])).unwrap().weights(),
        weights
    );
}

#[test]
fn the_coordinate_additivity_defect_vanishes_exactly_on_same_sign_pairs() {
    // D1(x, y) = |x| + |y| - |x + y| >= 0, and D1 = 0 iff x y >= 0.
    for x in -6..=6i64 {
        for y in -6..=6i64 {
            let d1 = ri(x).abs() + ri(y).abs() - ri(x + y).abs();
            assert!(!d1.is_negative());
            assert_eq!(d1.is_zero(), x * y >= 0, "x = {x}, y = {y}");
        }
    }
}

#[test]
fn l1_adds_on_disjoint_supports_and_l2_does_not() {
    // Disjoint blocks x = (3, 4) and y = (5, 12): l1 norms 7 and 17, l2 norms 5 and 13.
    let (x, y) = (rats(&[3, 4]), rats(&[5, 12]));
    let l1 = |v: &[Rational]| v.iter().map(|a| a.abs()).sum::<Rational>();
    let l2_sq = |v: &[Rational]| v.iter().map(|a| a * a).sum::<Rational>();
    let joined: Vec<Rational> = x.iter().chain(&y).cloned().collect();
    assert_eq!(l1(&joined), l1(&x) + l1(&y));
    // ||x (+) y||_2^2 = 194 < (5 + 13)^2 = 324.
    assert_eq!(l2_sq(&joined), ri(194));
    assert!(l2_sq(&joined) < (ri(5) + ri(13)) * (ri(5) + ri(13)));
    // The unit blocks of the worked replay: sqrt(2) < 2, compared through squares.
    assert!(ri(1 + 1) < ri(2) * ri(2));
    // The l2 defect ratio (||x|| + ||y||)^2 / ||x (+) y||^2 is at most 2 and
    // reaches 2 exactly at equal norms.
    for (a, b) in [(5, 13), (5, 5), (3, 4), (7, 7), (1, 9)] {
        let ratio = (ri(a) + ri(b)) * (ri(a) + ri(b)) / (ri(a * a) + ri(b * b));
        assert!(ratio <= ri(2));
        assert_eq!(ratio == ri(2), a == b);
    }
}

#[test]
fn the_crate_l1_quotient_mass_adds_over_disjoint_blocks() {
    // The l1 aggregation the crate uses is Phi1 from omega_functional. On a
    // triangle and a square, as separate packets and as one disjoint packet,
    // the mass of the joined cochain is the sum of the blocks' masses.
    let packet = |vertices: &[&str], edges: &[(&str, &str)]| {
        FiniteCochainPacket::with_unit_weights(
            FiniteCochainPacket::build_complex(vertices, edges, &[]).unwrap(),
        )
        .unwrap()
    };
    let triangle_edges = [("a", "b"), ("b", "c"), ("c", "a")];
    let square_edges = [("p", "q"), ("q", "r"), ("r", "s"), ("s", "p")];
    let triangle = packet(&["a", "b", "c"], &triangle_edges);
    let square = packet(&["p", "q", "r", "s"], &square_edges);
    let joined_edges: Vec<(&str, &str)> = triangle_edges
        .iter()
        .chain(&square_edges)
        .copied()
        .collect();
    let both = packet(&["a", "b", "c", "p", "q", "r", "s"], &joined_edges);
    let phi = |p: &FiniteCochainPacket, x: &[Rational]| p.quotient_mass(x).unwrap().value().clone();
    // With unit weights a cycle's mass is its absolute circulation: 7 and 17.
    assert_eq!(phi(&triangle, &rats(&[3, 4, 0])), ri(7));
    assert_eq!(phi(&square, &rats(&[5, 0, 12, 0])), ri(17));
    for (x, y) in [
        (rats(&[3, 4, 0]), rats(&[5, 0, 12, 0])),
        (rats(&[1, -1, 2]), rats(&[-2, 3, 0, 1])),
    ] {
        let joined: Vec<Rational> = x.iter().chain(&y).cloned().collect();
        assert_eq!(phi(&both, &joined), phi(&triangle, &x) + phi(&square, &y));
    }
}

// ---------------------------------------------------------------------------
// Theorem 3: descent-compatible maps are row-sparse
// ---------------------------------------------------------------------------

#[test]
fn descent_compatible_maps_have_one_entry_per_row_and_unitary_ones_are_monomial() {
    let descends = |m: &BasicMatrix<GaussianRat>| {
        matches!(classify_descent(m).unwrap(), Descent::Monopolar(_))
    };
    let mut cnot = matrix::zeros(4, 4).unwrap();
    for (r, c) in [(0, 0), (1, 1), (2, 3), (3, 2)] {
        cnot.set(r, c, gi(1, 0)).unwrap();
    }
    assert!(descends(&cnot));
    let monomial = matrix::from_rows(vec![
        vec![gi(0, 0), gi(0, 1)],
        vec![gq(-3, 5, 4, 5), gi(0, 0)],
    ])
    .unwrap();
    assert_eq!(
        matrix::multiply(&involution::adjoint(&monomial).unwrap(), &monomial).unwrap(),
        matrix::identity(2).unwrap()
    );
    assert!(descends(&monomial));
    let rotation = matrix::from_rows(vec![
        vec![gq(3, 5, 0, 1), gq(-4, 5, 0, 1)],
        vec![gq(4, 5, 0, 1), gq(3, 5, 0, 1)],
    ])
    .unwrap();
    assert!(!descends(&rotation));
    let all_ones =
        matrix::from_rows(vec![vec![gi(1, 0), gi(1, 0)], vec![gi(1, 0), gi(1, 0)]]).unwrap();
    assert!(!descends(&all_ones));
}

// ---------------------------------------------------------------------------
// Theorem 5: the phase-averaged shadow is dephasing
// ---------------------------------------------------------------------------

#[test]
fn averaging_over_a_nontrivial_phase_group_is_dephasing_on_every_matrix() {
    for n in 1..=3 {
        assert!(averages_to_dephasing(n, &signs()).unwrap());
        assert!(averages_to_dephasing(n, &quarter_turns()).unwrap());
    }
    // The trivial group averages nothing: coherence survives.
    let trivial = group(vec![gi(1, 0)]);
    assert!(averages_to_dephasing(1, &trivial).unwrap());
    assert!(!averages_to_dephasing(2, &trivial).unwrap());
    assert_eq!(
        averages_to_dephasing(0, &signs()),
        Err(ShadowError::ZeroDimension)
    );
}

#[test]
fn the_phase_averaged_readout_of_a_lift_is_the_weighted_l1_readout() {
    // A lift with rational amplitudes sqrt(w) for w = (4, 1, 1), readout u = (1, -1/2, 1/4).
    let u = [gi(1, 0), gq(-1, 2, 0, 1), gq(1, 4, 0, 1)];
    let amplitudes = [gi(2, 0), gi(1, 0), gi(1, 0)];
    let weights = rats(&[4, 1, 1]);
    let expected: Rational = u.iter().zip(&weights).map(|(ui, w)| ui.norm_sq() * w).sum();
    assert_eq!(expected, ri(4) + rq(1, 4) + rq(1, 16));
    // Replay the experiment exactly: every quarter-turn phase choice on every sector.
    let phases = quarter_turns();
    let mut total = Rational::zero();
    let mut count = 0;
    for a in phases.elements() {
        for b in phases.elements() {
            for c in phases.elements() {
                let psi = [
                    amplitudes[0].mul(a),
                    amplitudes[1].mul(b),
                    amplitudes[2].mul(c),
                ];
                let inner = u
                    .iter()
                    .zip(&psi)
                    .fold(gi(0, 0), |acc, (x, y)| acc.add(&x.conj().mul(y)));
                total += inner.norm_sq();
                count += 1;
            }
        }
    }
    assert_eq!(total / ri(count), expected);
    // The same number from the averaged density u* avg(c c*) u.
    let lift = involution::outer_product(&amplitudes, &amplitudes).unwrap();
    let averaged = phase_group_average(&lift, &phases).unwrap();
    let readout =
        involution::inner_product(&u, &matrix::multiply_vector(&averaged, &u).unwrap()).unwrap();
    assert_eq!(
        (readout.re, readout.im),
        (expected.clone(), Rational::zero())
    );
    // The paper's w = (2, 1, 1) has an irrational amplitude, but only the
    // diagonal survives the average, so its shadow is 2 + 1/4 + 1/16 = 37/16.
    let paper: Rational = u
        .iter()
        .zip(&rats(&[2, 1, 1]))
        .map(|(ui, w)| ui.norm_sq() * w)
        .sum();
    assert_eq!(paper, rq(37, 16));
}

#[test]
fn oversized_and_non_square_averages_are_refused() {
    let big = matrix::identity(7).unwrap();
    assert!(matches!(
        phase_group_average(&big, &quarter_turns()),
        Err(ShadowError::Budget { .. })
    ));
    assert!(4usize.pow(7) > AVERAGE_BUDGET);
    let wide = linear_algebra::backend::basic_matrix::BasicMatrix::from_row_major(
        1,
        2,
        vec![gi(1, 0), gi(0, 0)],
    )
    .unwrap();
    assert_eq!(
        phase_group_average(&wide, &signs()),
        Err(ShadowError::NotSquare { rows: 1, cols: 2 })
    );
}
