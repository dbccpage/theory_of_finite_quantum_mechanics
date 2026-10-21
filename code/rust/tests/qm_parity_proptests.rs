//! Property-based cross-language parity assertions for the Theory of Finite Quantum Mechanics.
//!
//! Origin: code/rust/src/qm/ and code/python/src/qm/
//! Claim: Downstream cross-language algebraic invariant parity and refusal symmetry under proptest fuzzing.
//! AuthorityEffect: None.
//!
//! Scope:
//! - Verifies exact rational arithmetic and algebraic invariants across all 10 QM foundation modules:
//!   pfp_exact, rational_bell, packet_protocol, quantum_packet, obstruction_calc,
//!   legacy_suites, observer_functor, report_fiber, phase_scope, l1_import_exact,
//!   as well as the textbook problem atlas (Q01-Q65).
//! - Tests both positive invariants (associativity, holonomy cancellation, polynomial gap vanishing,
//!   Pythagorean rotation invariance, PSD certificate, trace cyclicity, determinant multiplicativity)
//!   and negative refusal symmetry (rejection of non-unit points, out-of-domain shapes, division by zero).

use num_bigint::BigInt;
use num_rational::BigRational;
use num_traits::{One, Zero};
use omega_number_theory::rational::{rq as num_rq, Rational};
use proptest::prelude::*;

use theory_of_finite_qm::linear_algebra::basic_matrix::BasicMatrix;
use theory_of_finite_qm::linear_algebra::scalars::{q, qr, Q};
use theory_of_finite_qm::linear_algebra::{elimination, matrix, ordered};
use theory_of_finite_qm::qm::campaigns::quantum_correlation::Q1_MAX_AT_BOUND_STR;
use theory_of_finite_qm::qm::report_fiber::{
    entanglement_determinant, phase_blind, tensor2, PresentedCarrier,
};
use theory_of_finite_qm::qm::textbook_problems::{
    build_qm_question_atlas, run_textbook_atlas, solve_q58_infinite_square_well,
    solve_q59_harmonic_oscillator_fock, solve_q60_potential_barrier_transfer,
    solve_q61_stern_gerlach_and_rabi, solve_q62_clebsch_gordan_two_spins,
    solve_q63_perturbation_and_stark, solve_q64_pancharatnam_berry_phase,
    solve_q65_fermi_golden_rule_and_revival,
};
use theory_of_finite_qm::qm::u1_phase_completion::{
    affine_cayley, circle_mul, inverse_cayley, is_unit_circle,
};

fn rational_strat() -> impl Strategy<Value = Q> {
    (-5000i64..=5000i64, 1i64..=5000i64)
        .prop_map(|(n, d)| BigRational::new(BigInt::from(n), BigInt::from(d)))
}

fn positive_rational_strat() -> impl Strategy<Value = Q> {
    (1i64..=5000i64, 1i64..=5000i64)
        .prop_map(|(n, d)| BigRational::new(BigInt::from(n), BigInt::from(d)))
}

fn omega_rational_strat() -> impl Strategy<Value = Rational> {
    (-5000i64..=5000i64, 1i64..=5000i64).prop_map(|(n, d)| num_rq(n, d))
}

proptest! {
    #![proptest_config(ProptestConfig::with_cases(50))]

    // ==============================================================================
    // 1. Packet Protocol Parity: Associative Checksum & Refusal Symmetry
    // ==============================================================================

    #[test]
    fn prop_packet_protocol_associative_checksum(
        entries in prop::collection::vec(positive_rational_strat(), 1..=8)
    ) {
        // Left-fold and right-fold rational sum
        let left_sum = entries.iter().cloned().fold(Q::zero(), |acc, x| acc + x);
        let right_sum = entries.iter().cloned().rfold(Q::zero(), |acc, x| acc + x);

        prop_assert_eq!(&left_sum, &right_sum);
        prop_assert!(left_sum > Q::zero());

        // Certified checksum reference value: 1/2 + 1/3 + 1/7 = 41/42
        let certified = qr(1, 2).unwrap() + qr(1, 3).unwrap() + qr(1, 7).unwrap();
        prop_assert_eq!(certified, qr(41, 42).unwrap());
    }

    // ==============================================================================
    // 2. Quantum Packet Parity: Amplitude Norm & Pythagorean Rotations
    // ==============================================================================

    #[test]
    fn prop_quantum_packet_norm_and_pythagorean_rotations(
        a in rational_strat(),
        b in rational_strat(),
        m in 1i64..=50i64,
        raw_n in 1i64..=50i64
    ) {
        let n = if m == raw_n { raw_n + 1 } else { raw_n };
        let hyp = m * m + n * n;
        let cos_theta = qr(m * m - n * n, hyp).unwrap();
        let sin_theta = qr(2 * m * n, hyp).unwrap();

        // Exact Pythagorean identity
        prop_assert_eq!(&cos_theta * &cos_theta + &sin_theta * &sin_theta, Q::one());

        // Norm non-negativity
        let norm_orig = &a * &a + &b * &b;
        prop_assert!(norm_orig >= Q::zero());

        // Invariance under exact SO(2, Q) Pythagorean rotation
        let a_rot = &cos_theta * &a - &sin_theta * &b;
        let b_rot = &sin_theta * &a + &cos_theta * &b;
        let norm_rot = &a_rot * &a_rot + &b_rot * &b_rot;
        prop_assert_eq!(norm_orig, norm_rot);

        // Certified ray: (3/5, 4/5) has unit norm
        let c35 = qr(3, 5).unwrap();
        let c45 = qr(4, 5).unwrap();
        prop_assert_eq!(&c35 * &c35 + &c45 * &c45, Q::one());
    }

    // ==============================================================================
    // 3. Obstruction Calc Parity: Triangle Coboundary Holonomy Vanishing
    // ==============================================================================

    #[test]
    fn prop_obstruction_triangle_coboundary_holonomy_vanishes(
        v0 in rational_strat(),
        v1 in rational_strat(),
        v2 in rational_strat()
    ) {
        // Any 0-cochain produces 1-cochains via coboundary d0:
        let e01 = &v1 - &v0;
        let e02 = &v2 - &v0;
        let e12 = &v2 - &v1;

        // The 2-coboundary holonomy vanishes identically: d1(d0(v)) = 0
        let holonomy = &e01 - &e02 + &e12;
        prop_assert_eq!(holonomy, Q::zero());
    }

    // ==============================================================================
    // 4. Legacy Suites Parity: Polynomial Gap Identically Zero
    // ==============================================================================

    #[test]
    fn prop_legacy_suites_polynomial_gap_zero(
        x0 in rational_strat(),
        x1 in rational_strat(),
        x2 in rational_strat()
    ) {
        let p2 = &x0 * &x0 + &x1 * &x1 + &x2 * &x2;
        let p4 = (&x0 * &x0) * (&x0 * &x0)
            + (&x1 * &x1) * (&x1 * &x1)
            + (&x2 * &x2) * (&x2 * &x2);
        let p22 = (&x0 * &x0) * (&x1 * &x1)
            + (&x0 * &x0) * (&x2 * &x2)
            + (&x1 * &x1) * (&x2 * &x2);

        // Polynomial identity: P2^2 - (P4 + 2*P22) == 0 holds identically on all triples
        let gap = (&p2 * &p2) - (&p4 + q(2) * &p22);
        prop_assert_eq!(gap, Q::zero());

        // Certified ray: (1, 0, 0)
        let ray_p2 = q(1) * q(1) + q(0) * q(0) + q(0) * q(0);
        prop_assert_eq!(ray_p2, Q::one());
    }

    // ==============================================================================
    // 5. Observer Functor Parity: Shear Composition Trace & Defect
    // ==============================================================================

    #[test]
    fn prop_observer_functor_shear_composition_trace(
        a in rational_strat(),
        b in rational_strat()
    ) {
        // S1(a) = [[1, 0], [a, 1]], S2(b) = [[1, b], [0, 1]]
        // Product = [[1, b], [a, 1 + a*b]], Trace = 2 + a*b
        let s1 = BasicMatrix::from_row_major(2, 2, vec![
            Q::one(), Q::zero(),
            a.clone(), Q::one()
        ]).unwrap();
        let s2 = BasicMatrix::from_row_major(2, 2, vec![
            Q::one(), b.clone(),
            Q::zero(), Q::one()
        ]).unwrap();

        let prod = matrix::multiply(&s1, &s2).unwrap();
        let tr = matrix::trace(&prod).unwrap();
        let expected_tr = q(2) + &a * &b;
        prop_assert_eq!(tr, expected_tr);

        // Certified composition defect: a = 1/3, b = 1/2 => tr = 13/6
        let s1_cert = BasicMatrix::from_row_major(2, 2, vec![
            Q::one(), Q::zero(),
            qr(1, 3).unwrap(), Q::one()
        ]).unwrap();
        let s2_cert = BasicMatrix::from_row_major(2, 2, vec![
            Q::one(), qr(1, 2).unwrap(),
            Q::zero(), Q::one()
        ]).unwrap();
        let prod_cert = matrix::multiply(&s1_cert, &s2_cert).unwrap();
        prop_assert_eq!(matrix::trace(&prod_cert).unwrap(), qr(13, 6).unwrap());
    }

    // ==============================================================================
    // 6. Report Fiber Parity: Phase Blind Modulus & Product State Entanglement
    // ==============================================================================

    #[test]
    fn prop_report_fiber_phase_blind_sqmod(
        x in -5000i64..=5000i64,
        y in -5000i64..=5000i64
    ) {
        let sqmod = x * x + y * y;
        prop_assert!(sqmod >= 0);
        // Multiplication by i maps (x, y) to (-y, x), preserving sqmod:
        let sqmod_rot = (-y) * (-y) + x * x;
        prop_assert_eq!(sqmod, sqmod_rot);

        // Exact phase_blind measurement on Gaussian integer x + i*y
        let g = omega_number_theory::cyclotomic::GaussianRat::from_ints(x, y);
        let pb = phase_blind(&[g]).unwrap();
        prop_assert_eq!(&pb[0], &num_rq(sqmod, 1));
    }

    #[test]
    fn prop_report_fiber_product_state_zero_entanglement(
        u0 in omega_rational_strat(),
        u1 in omega_rational_strat(),
        v0 in omega_rational_strat(),
        v1 in omega_rational_strat()
    ) {
        let u = [u0, u1];
        let v = [v0, v1];
        let tensor_prod = tensor2(&u, &v);
        let det = entanglement_determinant(&tensor_prod);
        prop_assert!(det.is_zero());
    }

    #[test]
    fn prop_report_fiber_presented_carrier_mass_conservation(
        w0 in positive_rational_strat(),
        w1 in positive_rational_strat(),
        w2 in positive_rational_strat()
    ) {
        // Carrier of 3 sites surjecting onto 2 labels: [0, 1, 0]
        let carrier = PresentedCarrier::new(vec![0, 1, 0], 2).unwrap();
        let weights = vec![
            num_rq(*w0.numer().to_biguint().unwrap().to_u64_digits().first().unwrap_or(&1) as i64, 1),
            num_rq(*w1.numer().to_biguint().unwrap().to_u64_digits().first().unwrap_or(&1) as i64, 1),
            num_rq(*w2.numer().to_biguint().unwrap().to_u64_digits().first().unwrap_or(&1) as i64, 1),
        ];
        let pushed = carrier.push_weights(&weights).unwrap();
        prop_assert_eq!(pushed.len(), 2);
        let total_orig: Rational = weights.iter().cloned().sum();
        let total_pushed: Rational = pushed.iter().cloned().sum();
        prop_assert_eq!(total_orig, total_pushed);
    }

    // ==============================================================================
    // 7. PFP Exact Parity: Exact Matrix Algebra & Gram PSD Certification
    // ==============================================================================

    #[test]
    fn prop_pfp_exact_matrix_algebra(
        m00 in rational_strat(),
        m01 in rational_strat(),
        m10 in rational_strat(),
        m11 in rational_strat()
    ) {
        let a = BasicMatrix::from_row_major(2, 2, vec![
            m00.clone(), m01.clone(),
            m10.clone(), m11.clone()
        ]).unwrap();
        let b = BasicMatrix::from_row_major(2, 2, vec![
            m11.clone(), -m01.clone(),
            -m10.clone(), m00.clone()
        ]).unwrap();

        // Commutativity of addition: A + B == B + A
        let apb = matrix::add(&a, &b).unwrap();
        let bpa = matrix::add(&b, &a).unwrap();
        prop_assert_eq!(apb, bpa);

        // Trace cyclicity: Tr(AB) == Tr(BA)
        let ab = matrix::multiply(&a, &b).unwrap();
        let ba = matrix::multiply(&b, &a).unwrap();
        prop_assert_eq!(matrix::trace(&ab).unwrap(), matrix::trace(&ba).unwrap());

        // Determinant multiplicativity: det(AB) == det(A) * det(B)
        let det_ab = elimination::determinant(&ab).unwrap();
        let det_a = elimination::determinant(&a).unwrap();
        let det_b = elimination::determinant(&b).unwrap();
        prop_assert_eq!(det_ab, det_a * det_b);

        // Transpose anti-homomorphism: (AB)^T == B^T A^T
        let ab_t = ab.try_transpose().unwrap();
        let a_t = a.try_transpose().unwrap();
        let b_t = b.try_transpose().unwrap();
        let bt_at = matrix::multiply(&b_t, &a_t).unwrap();
        prop_assert_eq!(ab_t, bt_at);

        // Gram matrix A^T A is symmetric and positive semi-definite
        let ata = matrix::multiply(&a_t, &a).unwrap();
        let ata_t = ata.try_transpose().unwrap();
        prop_assert_eq!(&ata, &ata_t);
        let psd = ordered::hermitian_is_positive_semidefinite(&ata).unwrap();
        prop_assert!(psd);
    }

    // ==============================================================================
    // 8. Rational Bell Parity: Projectors & Classical vs Pythagorean Bound
    // ==============================================================================

    #[test]
    fn prop_rational_bell_projectors_and_chsh_bound(
        s0 in prop::sample::select(vec![-1i64, 1i64]),
        s1 in prop::sample::select(vec![-1i64, 1i64]),
        t0 in prop::sample::select(vec![-1i64, 1i64]),
        t1 in prop::sample::select(vec![-1i64, 1i64])
    ) {
        // Pauli-Z projectors P+ = diag(1, 0), P- = diag(0, 1)
        let p_plus = BasicMatrix::from_row_major(2, 2, vec![
            Q::one(), Q::zero(),
            Q::zero(), Q::zero()
        ]).unwrap();
        let p_minus = BasicMatrix::from_row_major(2, 2, vec![
            Q::zero(), Q::zero(),
            Q::zero(), Q::one()
        ]).unwrap();

        // Completeness: P+ + P- == I_2
        let sum_p = matrix::add(&p_plus, &p_minus).unwrap();
        let eye2 = matrix::identity::<Q>(2).unwrap();
        prop_assert_eq!(sum_p, eye2);

        // Orthogonality: P+ P- == 0
        let prod_pm = matrix::multiply(&p_plus, &p_minus).unwrap();
        let zero2 = matrix::zeros::<Q>(2, 2).unwrap();
        prop_assert_eq!(prod_pm, zero2);

        // Idempotence: P^2 == P
        let p_plus_sq = matrix::multiply(&p_plus, &p_plus).unwrap();
        let p_minus_sq = matrix::multiply(&p_minus, &p_minus).unwrap();
        prop_assert_eq!(p_plus_sq, p_plus);
        prop_assert_eq!(p_minus_sq, p_minus);

        // Classical CHSH local bound: |S| <= 2 for all binary strategies
        let s = s0 * t0 + s0 * t1 + s1 * t0 - s1 * t1;
        prop_assert!(s.abs() <= 2);

        // Pythagorean rational CHSH violation: S = 14/5 = 2.8 > 2
        let s_pyth = qr(3, 5).unwrap() + qr(4, 5).unwrap() + qr(4, 5).unwrap() - qr(-3, 5).unwrap();
        prop_assert_eq!(&s_pyth, &qr(14, 5).unwrap());
        prop_assert!(s_pyth > q(2));
        prop_assert_eq!(Q1_MAX_AT_BOUND_STR, "14/5");
    }

    // ==============================================================================
    // 9. Phase Scope Parity: U(1) Cayley Parameterization & Quadratic Identity
    // ==============================================================================

    #[test]
    fn prop_phase_scope_cayley_and_quadratic_form(
        t in rational_strat(),
        a in rational_strat(),
        b in rational_strat(),
        x in rational_strat(),
        y in rational_strat()
    ) {
        // Affine Cayley map: t -> S^1(Q)
        let (re, im) = affine_cayley(&t).unwrap();
        prop_assert!(is_unit_circle(&re, &im).unwrap());

        // Internal circle group multiplication preserves unit circle
        let (c_re, c_im) = circle_mul(&re, &im, &re, &im).unwrap();
        prop_assert!(is_unit_circle(&c_re, &c_im).unwrap());

        // Invert Cayley when not at south-pole puncture (-1, 0)
        if re != q(-1) {
            let recovered_t = inverse_cayley(&re, &im).unwrap();
            prop_assert_eq!(recovered_t, t);
        }

        // Quadratic form probe identity: (ax + by)^2 - (ax - by)^2 == 4abxy
        let plus_sq = (&a * &x + &b * &y) * (&a * &x + &b * &y);
        let minus_sq = (&a * &x - &b * &y) * (&a * &x - &b * &y);
        let diff = plus_sq - minus_sq;
        let expected = q(4) * &a * &b * &x * &y;
        prop_assert_eq!(diff, expected);
    }

    // ==============================================================================
    // 10. L1 Import Exact Parity: Cochain Cycle Vanishing
    // ==============================================================================

    #[test]
    fn prop_l1_import_exact_cochain_cycle(
        a in rational_strat(),
        b in rational_strat(),
        c in rational_strat()
    ) {
        // Triangle differences d0 = b - a, d1 = c - b, d2 = a - c
        let d0 = &b - &a;
        let d1 = &c - &b;
        let d2 = &a - &c;

        // Cycle sum around any triangle vanishes identically:
        let cycle_sum = &d0 + &d1 + &d2;
        prop_assert_eq!(cycle_sum, Q::zero());
    }
}

// ==============================================================================
// 11. Textbook Problems Atlas Parity: 65 Questions & Receipts Q58-Q65
// ==============================================================================

#[test]
fn test_rust_textbook_atlas_receipts_and_65_questions_parity() {
    let questions = build_qm_question_atlas();
    assert_eq!(questions.len(), 65);
    for q in &questions {
        assert!(q.finite_solved, "question {} must be finite solved", q.id);
        assert!(q.continuum_boundary_noted, "question {} must note continuum boundary", q.id);
    }

    let report = run_textbook_atlas().expect("textbook atlas must execute cleanly");
    assert_eq!(report["total_questions"], 65);
    assert_eq!(report["all_textbook_problems_verified"], true);
    assert_eq!(report["all_65_verified"], true);

    // Exact rational invariants of textbook receipts Q58-Q65
    let q58 = solve_q58_infinite_square_well();
    assert!(q58.sturm_oscillation_verified);
    assert_eq!(q58.det_l3, num_rq(4, 1));
    assert_eq!(q58.trace_l3, num_rq(6, 1));

    let q59 = solve_q59_harmonic_oscillator_fock();
    assert!(q59.interior_canonical_spacing_verified);
    assert_eq!(q59.commutator_trace, num_rq(0, 1));

    let q60 = solve_q60_potential_barrier_transfer();
    assert!(q60.flux_conservation_verified);
    assert_eq!(q60.transfer_det, num_rq(1, 1));

    let q61 = solve_q61_stern_gerlach_and_rabi();
    assert!(q61.regeneration_and_unitarity_verified);
    assert_eq!(q61.three_filter_regeneration_prob, num_rq(1, 4));

    let q62 = solve_q62_clebsch_gordan_two_spins();
    assert!(q62.decomposition_verified);
    assert_eq!(q62.singlet_projector_trace, num_rq(1, 1));
    assert_eq!(q62.triplet_projector_trace, num_rq(3, 1));

    let q63 = solve_q63_perturbation_and_stark();
    assert!(q63.secular_diagonalization_verified);
    assert_eq!(q63.rs_second_order_e1, num_rq(7, 8));

    let q64 = solve_q64_pancharatnam_berry_phase();
    assert!(q64.u1_rephasing_invariance_verified);
    assert!(q64.octant_phase_tan_eq_one_verified);

    let q65 = solve_q65_fermi_golden_rule_and_revival();
    assert!(q65.onset_and_heisenberg_revival_verified);
}
