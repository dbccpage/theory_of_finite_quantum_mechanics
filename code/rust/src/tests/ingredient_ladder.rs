//! The finite QM ingredient ladder, rung by rung on exact data: `l1`
//! normalization and the redundant Born square, the diagonal density and its
//! purity, the population shadow of a Kraus channel and what it forgets, path
//! sums as kernel powers, the phase fiber over one law, and the mixing that no
//! function of the weights reproduces. The normalization countermodel behind
//! the imported Born-square uniqueness closes the file.

use finite_qm_native::campaigns::residual_density_calculus::{
    ledger_from_diagonal_density, ResidualLedger,
};
use linear_algebra::backend::basic_matrix::BasicMatrix;
use linear_algebra::exact_field::matrix;
use omega_number_theory::cyclotomic::GaussianRat;
use omega_number_theory::rational::{ri, rq, Rational};
use omega_quantum_physics::coherent_interference::{cross_term, interfered_weight};
use omega_quantum_physics::exact_channel::ExactKrausChannel;
use omega_quantum_physics::exact_hermitian::{gi, gq, is_positive_semidefinite};
use omega_quantum_physics::mass_phase_embedding::MassPhaseEmbedding;
use omega_quantum_physics::phase_blind_quotient::{
    classify_descent, discrete_fiber, gaussian_lift, phase_blind_projection, separates, Descent,
    FiberPoint, UnitPhaseGroup,
};
use omega_quantum_physics::residual_density_calculus::{
    row_stochastic_pushforward, sector_measurement, ResidualDensityError,
};

use omega_quantum_physics::population_shadow::{
    compose_channels, compose_kernels, composition_defect, population_shadow, ShadowError,
};

fn rats(values: &[i64]) -> Vec<Rational> {
    values.iter().map(|&v| ri(v)).collect()
}

fn ledger(values: &[i64]) -> ResidualLedger {
    ResidualLedger::new(rats(values)).unwrap()
}

fn qi(rows: Vec<Vec<GaussianRat>>) -> BasicMatrix<GaussianRat> {
    matrix::from_rows(rows).unwrap()
}

fn half() -> GaussianRat {
    gq(1, 2, 0, 1)
}

fn plus_state() -> BasicMatrix<GaussianRat> {
    qi(vec![vec![half(), half()], vec![half(), half()]])
}

fn density(p: &[Rational]) -> BasicMatrix<GaussianRat> {
    matrix::diagonal(
        &p.iter()
            .cloned()
            .map(GaussianRat::from_rational)
            .collect::<Vec<_>>(),
    )
    .unwrap()
}

fn identity_channel() -> ExactKrausChannel {
    ExactKrausChannel::from_operators(vec![matrix::identity(2).unwrap()]).unwrap()
}

fn bit_flip() -> ExactKrausChannel {
    ExactKrausChannel::from_operators(vec![qi(vec![
        vec![gi(0, 0), gi(1, 0)],
        vec![gi(1, 0), gi(0, 0)],
    ])])
    .unwrap()
}

fn dephasing() -> ExactKrausChannel {
    ExactKrausChannel::from_operators(vec![density(&rats(&[1, 0])), density(&rats(&[0, 1]))])
        .unwrap()
}

/// The rational rotation with `cos = 3/5`, `sin = 4/5`.
fn rotation() -> ExactKrausChannel {
    ExactKrausChannel::from_operators(vec![qi(vec![
        vec![gq(3, 5, 0, 1), gq(-4, 5, 0, 1)],
        vec![gq(4, 5, 0, 1), gq(3, 5, 0, 1)],
    ])])
    .unwrap()
}

fn amplitude_damping() -> ExactKrausChannel {
    ExactKrausChannel::from_operators(vec![
        qi(vec![
            vec![gi(1, 0), gi(0, 0)],
            vec![gi(0, 0), gq(3, 5, 0, 1)],
        ]),
        qi(vec![
            vec![gi(0, 0), gq(4, 5, 0, 1)],
            vec![gi(0, 0), gi(0, 0)],
        ]),
    ])
    .unwrap()
}

/// A qubit-to-qutrit isometry.
fn embedding() -> ExactKrausChannel {
    ExactKrausChannel::from_operators(vec![qi(vec![
        vec![gq(3, 5, 0, 1), gi(0, 0)],
        vec![gq(4, 5, 0, 1), gi(0, 0)],
        vec![gi(0, 0), gi(1, 0)],
    ])])
    .unwrap()
}

fn kernel(rows: &[&[(i64, i64)]]) -> linear_algebra::backend::basic_matrix::BasicMatrix<Rational> {
    matrix::from_rows(
        rows.iter()
            .map(|row| row.iter().map(|&(n, d)| rq(n, d)).collect())
            .collect(),
    )
    .unwrap()
}

// ---------------------------------------------------------------------------
// QM-121-C1: probability is l1 normalization; the Born square re-encodes it.
// ---------------------------------------------------------------------------

#[test]
fn rung_one_normalizes_weights_and_every_exact_lift_returns_the_same_law() {
    assert_eq!(ledger(&[3, 1]).weights(), vec![rq(3, 4), rq(1, 4)]);
    // The source's lift (sqrt 3, 1) is irrational: (3/4, 1/4) has no preimage in Q(i)^2.
    assert_eq!(gaussian_lift(&[rq(3, 4), rq(1, 4)]).unwrap(), None);
    let worked = MassPhaseEmbedding::new(&rats(&[3, 1]), &[gi(1, 0), gi(0, 1)]).unwrap();
    assert_eq!(worked.born_weights(), vec![rq(3, 4), rq(1, 4)]);
    assert_eq!(worked.exact_amplitudes(), None);
    // On w = (9, 16) every exact lift with moduli (3, 4) gives back the l1 law.
    let law = ledger(&[9, 16]).weights();
    let lifts = [
        [gi(3, 0), gi(4, 0)],
        [gi(3, 0), gi(-4, 0)],
        [gi(0, 3), gi(4, 0)],
        [gi(-3, 0), gi(0, 4)],
        [gq(9, 5, 12, 5), gq(-16, 5, 12, 5)],
    ];
    for lift in &lifts {
        assert_eq!(phase_blind_projection(lift).unwrap(), law, "lift {lift:?}");
    }
    // Moduli that are not the square roots of w give a different law.
    assert_eq!(
        phase_blind_projection(&[gi(3, 0), gi(3, 0)]).unwrap(),
        vec![rq(1, 2), rq(1, 2)]
    );
    assert_ne!(phase_blind_projection(&[gi(9, 0), gi(16, 0)]).unwrap(), law);
}

// ---------------------------------------------------------------------------
// QM-121-C2: the diagonal density, its purity, and coherence that is not forced.
// ---------------------------------------------------------------------------

#[test]
fn rung_two_places_the_law_on_the_diagonal_with_purity_computed_two_ways() {
    let mixed = ledger(&[3, 1]);
    let rho = mixed.diagonal_density();
    assert!(is_positive_semidefinite(&rho));
    assert_eq!(matrix::trace(&rho).unwrap(), gi(1, 0));
    assert_eq!(
        matrix::trace(&matrix::multiply(&rho, &rho).unwrap()).unwrap(),
        GaussianRat::from_rational(rq(5, 8))
    );
    assert_eq!(mixed.purity(), rq(5, 8));
    assert_eq!(ri(1) - mixed.purity(), rq(3, 8));
    let pure = ledger(&[4, 0]);
    assert_eq!(pure.weights(), vec![ri(1), ri(0)]);
    assert_eq!(pure.purity(), ri(1));
    let rho_pure = pure.diagonal_density();
    assert_eq!(matrix::multiply(&rho_pure, &rho_pure).unwrap(), rho_pure);
    // |+><+| has the diagonal of diag(1/2, 1/2) and is pure, yet it is not a
    // diagonal density: the coherence is extra data, not a function of w.
    let plus = plus_state();
    assert!(is_positive_semidefinite(&plus));
    assert_eq!(sector_measurement(&plus).unwrap(), vec![rq(1, 2), rq(1, 2)]);
    assert_eq!(
        matrix::trace(&matrix::multiply(&plus, &plus).unwrap()).unwrap(),
        gi(1, 0)
    );
    assert_eq!(ledger(&[1, 1]).purity(), rq(1, 2));
    assert_eq!(
        ledger_from_diagonal_density(&plus),
        Err(ResidualDensityError::OffDiagonal { row: 0, col: 1 })
    );
}

// ---------------------------------------------------------------------------
// QM-121-C3: kernels compose; a CPTP map has a population shadow that
// forgets coherence and does not compose like the channel.
// ---------------------------------------------------------------------------

#[test]
fn rung_three_the_bit_flip_shadow_is_the_swap_kernel_and_moves_the_worked_law() {
    let swap = population_shadow(&bit_flip()).unwrap();
    assert_eq!(swap, kernel(&[&[(0, 1), (1, 1)], &[(1, 1), (0, 1)]]));
    assert_eq!(
        row_stochastic_pushforward(&swap, &[rq(3, 4), rq(1, 4)]).unwrap(),
        vec![rq(1, 4), rq(3, 4)]
    );
    let rho = ledger(&[3, 1]).diagonal_density();
    assert_eq!(
        sector_measurement(&bit_flip().apply(&rho).unwrap()).unwrap(),
        vec![rq(1, 4), rq(3, 4)]
    );
    // Rung 4 on the same kernel: two swaps return, so M^2 = I and M^3 = M.
    let identity = kernel(&[&[(1, 1), (0, 1)], &[(0, 1), (1, 1)]]);
    assert_eq!(compose_kernels(&swap, &swap).unwrap(), identity);
    assert_eq!(
        compose_kernels(&compose_kernels(&swap, &swap).unwrap(), &swap).unwrap(),
        swap
    );
    let twice = compose_channels(&bit_flip(), &bit_flip()).unwrap();
    assert_eq!(population_shadow(&twice).unwrap(), identity);
}

#[test]
fn population_shadows_are_row_stochastic_and_agree_with_the_channel_on_diagonal_inputs() {
    assert_eq!(
        population_shadow(&amplitude_damping()).unwrap(),
        kernel(&[&[(1, 1), (0, 1)], &[(16, 25), (9, 25)]])
    );
    assert_eq!(
        population_shadow(&embedding()).unwrap(),
        kernel(&[&[(9, 25), (16, 25), (0, 1)], &[(0, 1), (0, 1), (1, 1)]])
    );
    let laws = [
        rats(&[1, 0]),
        rats(&[0, 1]),
        vec![rq(3, 4), rq(1, 4)],
        vec![rq(2, 7), rq(5, 7)],
    ];
    for channel in [
        identity_channel(),
        bit_flip(),
        dephasing(),
        rotation(),
        amplitude_damping(),
        embedding(),
    ] {
        let shadow = population_shadow(&channel).unwrap();
        for p in &laws {
            let pushed = row_stochastic_pushforward(&shadow, p).unwrap();
            let populations = sector_measurement(&channel.apply(&density(p)).unwrap()).unwrap();
            assert_eq!(pushed, populations);
            assert_eq!(pushed.iter().sum::<Rational>(), ri(1));
        }
    }
}

#[test]
fn the_shadow_forgets_coherence_in_both_directions() {
    // Identity and complete dephasing share the identity shadow ...
    assert_eq!(
        population_shadow(&identity_channel()).unwrap(),
        population_shadow(&dephasing()).unwrap()
    );
    // ... and act differently on |+><+|.
    let plus = plus_state();
    assert_eq!(identity_channel().apply(&plus).unwrap(), plus);
    assert_eq!(
        dephasing().apply(&plus).unwrap(),
        density(&[rq(1, 2), rq(1, 2)])
    );
    // A diagonal input can leave coherent.
    let out = rotation().apply(&density(&rats(&[1, 0]))).unwrap();
    assert_eq!(
        out,
        qi(vec![
            vec![gq(9, 25, 0, 1), gq(12, 25, 0, 1)],
            vec![gq(12, 25, 0, 1), gq(16, 25, 0, 1)]
        ])
    );
    assert_eq!(
        ledger_from_diagonal_density(&out),
        Err(ResidualDensityError::OffDiagonal { row: 0, col: 1 })
    );
    assert_eq!(
        population_shadow(&rotation()).unwrap(),
        kernel(&[&[(9, 25), (16, 25)], &[(16, 25), (9, 25)]])
    );
}

#[test]
fn the_shadow_of_a_composite_is_not_the_composite_of_the_shadows() {
    let r = rotation();
    let rr = compose_channels(&r, &r).unwrap();
    assert_eq!(
        population_shadow(&rr).unwrap(),
        kernel(&[&[(49, 625), (576, 625)], &[(576, 625), (49, 625)]])
    );
    assert_eq!(
        compose_kernels(
            &population_shadow(&r).unwrap(),
            &population_shadow(&r).unwrap()
        )
        .unwrap(),
        kernel(&[&[(337, 625), (288, 625)], &[(288, 625), (337, 625)]])
    );
    assert_eq!(
        composition_defect(&r, &r).unwrap(),
        kernel(&[&[(-288, 625), (288, 625)], &[(288, 625), (-288, 625)]])
    );
    // A first step that keeps diagonals diagonal, or a second step whose output
    // populations read only input populations, leaves no defect.
    let zero = kernel(&[&[(0, 1), (0, 1)], &[(0, 1), (0, 1)]]);
    let pairs = [
        (dephasing(), r.clone()),
        (bit_flip(), r.clone()),
        (amplitude_damping(), r.clone()),
        (r.clone(), dephasing()),
        (r.clone(), amplitude_damping()),
    ];
    for (first, second) in &pairs {
        assert_eq!(composition_defect(first, second).unwrap(), zero);
    }
    // The rotation makes coherence that a second rotation turns into population.
    assert_ne!(composition_defect(&r, &r).unwrap(), zero);
}

#[test]
fn shadow_composition_refuses_malformed_kernels_and_shapes() {
    let swap = population_shadow(&bit_flip()).unwrap();
    assert_eq!(
        compose_kernels(&kernel(&[&[(1, 2), (1, 4)]]), &swap),
        Err(ShadowError::NotRowStochastic { row: 0 })
    );
    assert_eq!(
        compose_kernels(&swap, &kernel(&[&[(3, 2), (-1, 2)], &[(0, 1), (1, 1)]])),
        Err(ShadowError::NotRowStochastic { row: 0 })
    );
    assert_eq!(
        matrix::from_rows(vec![vec![ri(1)], vec![ri(0), ri(1)]]),
        Err(linear_algebra::exact_field::ExactFieldError::RaggedRows {
            row: 1,
            len: 2,
            expected: 1,
        })
    );
    assert_eq!(
        compose_kernels(&matrix::zeros(0, 0).unwrap(), &swap),
        Err(ShadowError::Shape)
    );
    let three = kernel(&[
        &[(1, 1), (0, 1), (0, 1)],
        &[(0, 1), (1, 1), (0, 1)],
        &[(0, 1), (0, 1), (1, 1)],
    ]);
    assert_eq!(
        compose_kernels(&swap, &three),
        Err(ShadowError::Mismatch {
            left_outputs: 2,
            right_inputs: 3
        })
    );
    assert_eq!(
        compose_channels(&embedding(), &bit_flip()).map(|_| ()),
        Err(ShadowError::Mismatch {
            left_outputs: 3,
            right_inputs: 2
        })
    );
    assert!(compose_channels(&bit_flip(), &embedding()).is_ok_and(|c| c.dim_out() == 3));
}

// ---------------------------------------------------------------------------
// QM-121-C5, C6: the phase fiber over one law, and mixing that separates it.
// ---------------------------------------------------------------------------

#[test]
fn rungs_five_and_six_the_fiber_over_one_law_and_the_mixing_that_separates_it() {
    let same = [gi(1, 0), gi(1, 0)];
    let flipped = [gi(1, 0), gi(-1, 0)];
    assert_eq!(
        phase_blind_projection(&same).unwrap(),
        vec![rq(1, 2), rq(1, 2)]
    );
    assert_eq!(
        phase_blind_projection(&same).unwrap(),
        phase_blind_projection(&flipped).unwrap()
    );
    let point = FiberPoint::of(&same).unwrap();
    assert_eq!(point.relative_phase_dimension(), 1);
    // A zero-weight coordinate carries no phase: support two, dimension one.
    let padded = FiberPoint::of(&[gi(1, 0), gi(1, 0), gi(0, 0)]).unwrap();
    assert_eq!(
        (padded.support(), padded.relative_phase_dimension()),
        (&[0usize, 1][..], 1)
    );
    // Over the declared quarter turns the fiber through (1, 1) has 4 = 4^(2 - 1) classes;
    // the circle itself is not enumerated.
    let quarter_turns =
        UnitPhaseGroup::new(vec![gi(1, 0), gi(0, 1), gi(-1, 0), gi(0, -1)]).unwrap();
    let fiber = discrete_fiber(&same, &quarter_turns).unwrap();
    assert_eq!(fiber.len(), 4);
    assert!(fiber
        .iter()
        .all(|c| phase_blind_projection(c).unwrap() == vec![rq(1, 2), rq(1, 2)]));
    // The two-row mix sends the fiber pair to (2, 0) and (0, 2): weights 4 and 0 on the first outcome.
    let mix = qi(vec![vec![gi(1, 0), gi(1, 0)], vec![gi(1, 0), gi(-1, 0)]]);
    assert_eq!(
        matrix::multiply_vector(&mix, &same).unwrap(),
        vec![gi(2, 0), gi(0, 0)]
    );
    assert_eq!(
        matrix::multiply_vector(&mix, &flipped).unwrap(),
        vec![gi(0, 0), gi(2, 0)]
    );
    assert_eq!(
        (
            interfered_weight(&same).unwrap(),
            interfered_weight(&flipped).unwrap()
        ),
        (ri(4), ri(0))
    );
    assert_eq!(
        (cross_term(&same).unwrap(), cross_term(&flipped).unwrap()),
        (ri(2), ri(-2))
    );
    // So the mix does not descend through the phase-blind quotient.
    match classify_descent(&mix).unwrap() {
        Descent::Obstructed(obstruction) => {
            assert!(separates(&mix, &obstruction.cancelled, &obstruction.reinforced).unwrap());
        }
        Descent::Monopolar(_) => panic!("the two-row mix has two nonzero entries in a row"),
    }
}

// ---------------------------------------------------------------------------
// QM-121-C9 support: normalization alone does not pick the square.
// ---------------------------------------------------------------------------

#[test]
fn every_power_readout_normalizes_and_only_one_is_the_square() {
    let laws: Vec<Vec<Rational>> = (1..=4)
        .map(|p| {
            let (a, b) = (ri(3).pow(p), ri(4).pow(p));
            let total = &a + &b;
            vec![a / &total, b / total]
        })
        .collect();
    assert_eq!(
        laws,
        vec![
            vec![rq(3, 7), rq(4, 7)],
            vec![rq(9, 25), rq(16, 25)],
            vec![rq(27, 91), rq(64, 91)],
            vec![rq(81, 337), rq(256, 337)],
        ]
    );
    assert!(laws.iter().all(|law| law.iter().sum::<Rational>() == ri(1)));
    for i in 0..4 {
        for j in (i + 1)..4 {
            assert_ne!(laws[i], laws[j]);
        }
    }
    assert_eq!(
        laws[1],
        phase_blind_projection(&[gi(3, 0), gi(4, 0)]).unwrap()
    );
}
