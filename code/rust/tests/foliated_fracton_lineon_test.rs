//! Integration tests for 1D hinge lineon collision avoidance and sign invariants (TFQ-1219).
//!
//! AuthorityEffect: None.

#![forbid(unsafe_code)]

use num_rational::Rational64;
use num_traits::Zero;
use tfqm_fsp::foliated_fracton_lineon::{
    ComplexRat, HingeOrientation, LineonHingeConfig, Mat2x2, QuaternionRat,
};

#[test]
fn test_lineon_hinge_config_ordering() {
    let cfg = LineonHingeConfig::new(HingeOrientation::XAxis, -2, 3);
    assert!(cfg.is_ok());
    let unwrapped = cfg.unwrap();
    assert_eq!(unwrapped.pos1, -2);
    assert_eq!(unwrapped.pos2, 3);
    assert_eq!(unwrapped.hinge, HingeOrientation::XAxis);

    // Collision at identical site is refused
    assert!(LineonHingeConfig::new(HingeOrientation::YAxis, 4, 4).is_err());

    // Inverted ordering is refused
    assert!(LineonHingeConfig::new(HingeOrientation::ZAxis, 5, 2).is_err());
}

#[test]
fn test_1d_collision_avoidance_hops() {
    let cfg = LineonHingeConfig::new(HingeOrientation::XAxis, 0, 3).unwrap();

    // Valid collision-free hops
    let hops = vec![
        (1, 1),   // (1, 4)
        (-1, 0),  // (0, 4)
        (1, -1),  // (1, 3)
        (0, 1),   // (1, 4)
        (1, 0),   // (2, 4)
    ];
    let res = cfg.apply_hops(&hops);
    assert!(res.is_ok());
    let final_cfg = res.unwrap();
    assert_eq!(final_cfg.pos1, 2);
    assert_eq!(final_cfg.pos2, 4);

    // Hop that causes collision pos1 == pos2 is refused
    let collision_hops = vec![
        (1, -1), // (1, 2)
        (1, 0),  // (2, 2) -> collision!
    ];
    assert!(cfg.apply_hops(&collision_hops).is_err());

    // Hop exceeding unit lattice bound is refused
    let invalid_hop = vec![(2, 0)];
    assert!(cfg.apply_hops(&invalid_hop).is_err());
}

#[test]
fn test_discrete_ivt_collision_and_exchange_obstruction() {
    let cfg = LineonHingeConfig::new(HingeOrientation::XAxis, 0, 4).unwrap();
    assert!(!cfg.can_exchange_without_collision());
    assert_eq!(cfg.permutation_parity(), 1);

    // Exchange trajectory swapping (0, 4) -> (4, 0)
    let traj1 = vec![0, 1, 2, 2, 3, 4];
    let traj2 = vec![4, 4, 3, 2, 1, 0];
    let collision_idx = LineonHingeConfig::verify_discrete_ivt_collision(0, 4, &traj1, &traj2);
    assert!(collision_idx.is_ok());
    let idx = collision_idx.unwrap();
    assert_eq!(traj1[idx], traj2[idx]);
    assert_eq!(traj1[idx], 2);

    // Simultaneous crossing collision:
    // t=0: (0, 1) -> t=1: (1, 0)
    let cross1 = vec![0, 1];
    let cross2 = vec![1, 0];
    let cross_res = LineonHingeConfig::verify_discrete_ivt_collision(0, 1, &cross1, &cross2);
    assert!(cross_res.is_ok());
}

#[test]
fn test_exact_character_traces_and_defect_mass() {
    // 1. Classical API & Character trace backward compatibility
    // Abelian 2-gauge defect sheets
    assert_eq!(LineonHingeConfig::hinge_commutator_trace(false), 2);
    assert_eq!(LineonHingeConfig::fracton_defect_mass(false), 0);
    assert_eq!(LineonHingeConfig::foliated_projected_trace(false, false), 4);
    assert_eq!(LineonHingeConfig::foliated_projected_trace(true, false), 2);

    // Non-abelian 2-gauge defect sheets
    assert_eq!(LineonHingeConfig::hinge_commutator_trace(true), -2);
    assert_eq!(LineonHingeConfig::fracton_defect_mass(true), 2);
    // Decoupled sheets: foliated projection squares trace -> 4 >= 0
    assert_eq!(LineonHingeConfig::foliated_projected_trace(false, true), 4);
    // Corner lineon turns: uncancelled negative curvature persists
    assert_eq!(LineonHingeConfig::foliated_projected_trace(true, true), -2);

    // 2. Direct Mat2x2 Gaussian rational matrix inverses
    let eye = Mat2x2::identity();
    let px = Mat2x2::pauli_x();
    let py = Mat2x2::pauli_y();
    let pz = Mat2x2::pauli_z();

    assert_eq!(eye.inv().expect("Identity invertible"), eye);
    assert_eq!(px.inv().expect("sigma_x invertible"), px);
    assert_eq!(py.inv().expect("sigma_y invertible"), py);
    assert_eq!(pz.inv().expect("sigma_z invertible"), pz);

    // 3. Pauli anti-commutation: sigma_z sigma_x = - sigma_x sigma_z
    let zx = pz.mul(&px);
    let xz = px.mul(&pz);
    assert_eq!(zx.m00, -xz.m00);
    assert_eq!(zx.m01, -xz.m01);
    assert_eq!(zx.m10, -xz.m10);
    assert_eq!(zx.m11, -xz.m11);

    // 4. Exact commutator holonomy matrix products: M = A B A^-1 B^-1
    // Abelian sheets (I, I) => M = I
    let m_abelian = eye.commutator_holonomy(&eye).expect("Abelian commutator");
    assert_eq!(m_abelian, eye);
    assert_eq!(m_abelian.trace(), ComplexRat::from_integer(2));

    // Non-abelian sheets (sigma_z, sigma_x) => M = -I
    let m_nonab_zx = pz.commutator_holonomy(&px).expect("Nonabelian z-x commutator");
    assert_eq!(m_nonab_zx.trace(), ComplexRat::from_integer(-2));
    assert_eq!(m_nonab_zx.m00, ComplexRat::from_integer(-1));
    assert_eq!(m_nonab_zx.m11, ComplexRat::from_integer(-1));
    assert_eq!(m_nonab_zx.m01, ComplexRat::zero());
    assert_eq!(m_nonab_zx.m10, ComplexRat::zero());

    // Alternative Pauli generators also yield M = -I and Tr = -2
    let m_nonab_xy = px.commutator_holonomy(&py).expect("Nonabelian x-y commutator");
    assert_eq!(m_nonab_xy.trace(), ComplexRat::from_integer(-2));
    let m_nonab_yz = py.commutator_holonomy(&pz).expect("Nonabelian y-z commutator");
    assert_eq!(m_nonab_yz.trace(), ComplexRat::from_integer(-2));

    // 5. Arbitrary defect sheet trace evaluation API
    let tr_ab = LineonHingeConfig::compute_defect_sheet_trace(&eye, &eye).unwrap();
    assert_eq!(tr_ab, ComplexRat::from_integer(2));
    let tr_nonab = LineonHingeConfig::compute_defect_sheet_trace(&pz, &px).unwrap();
    assert_eq!(tr_nonab, ComplexRat::from_integer(-2));

    // 6. Defect mass mapping function: Phi1(trace)
    assert_eq!(LineonHingeConfig::fracton_defect_mass_from_trace(2), 0);
    assert_eq!(LineonHingeConfig::fracton_defect_mass_from_trace(1), 0);
    assert_eq!(LineonHingeConfig::fracton_defect_mass_from_trace(0), 0);
    assert_eq!(LineonHingeConfig::fracton_defect_mass_from_trace(-1), 2);
    assert_eq!(LineonHingeConfig::fracton_defect_mass_from_trace(-2), 2);

    // 7. Exact rational quaternion commutator holonomy
    let q_one = QuaternionRat::one();
    let q_i = QuaternionRat::i_unit();
    let q_j = QuaternionRat::j_unit();
    let q_k = QuaternionRat::k_unit();

    let q_m_abelian = q_one.commutator_holonomy(&q_one).unwrap();
    assert_eq!(q_m_abelian, q_one);
    assert_eq!(q_m_abelian.character_trace(), Rational64::from_integer(2));

    let q_m_ij = q_i.commutator_holonomy(&q_j).unwrap();
    assert_eq!(q_m_ij.character_trace(), Rational64::from_integer(-2));
    let q_m_jk = q_j.commutator_holonomy(&q_k).unwrap();
    assert_eq!(q_m_jk.character_trace(), Rational64::from_integer(-2));
    let q_m_ki = q_k.commutator_holonomy(&q_i).unwrap();
    assert_eq!(q_m_ki.character_trace(), Rational64::from_integer(-2));
}

#[test]
fn test_adversarial_complex_rat_field_properties() {
    // 1. Division by zero in ComplexRat
    assert!(ComplexRat::zero().inv().is_err());
    assert_eq!(
        ComplexRat::zero().inv().unwrap_err(),
        "Division by zero in ComplexRat inverse"
    );

    // 2. Inversion of imaginary unit i: i^-1 = -i
    let i = ComplexRat::i();
    let i_inv = i.inv().expect("i is invertible");
    assert_eq!(i_inv, -i);
    assert_eq!(i * i_inv, ComplexRat::one());

    // 3. Inversion of arbitrary Gaussian rationals
    let samples = [
        ComplexRat::new(Rational64::new(3, 5), Rational64::new(4, 5)),
        ComplexRat::new(Rational64::new(7, 3), Rational64::new(-2, 9)),
        ComplexRat::new(Rational64::new(-10, 7), Rational64::new(1, 2)),
    ];
    for z in samples {
        let z_inv = z.inv().expect("Non-zero ComplexRat invertible");
        let prod = z * z_inv;
        assert_eq!(prod.re, Rational64::new(1, 1));
        assert_eq!(prod.im, Rational64::new(0, 1));

        // Conjugation properties: (z*)* = z, z * z* = norm_sq(z)
        assert_eq!(z.conj().conj(), z);
        let z_z_star = z * z.conj();
        assert_eq!(z_z_star.re, z.norm_sq());
        assert_eq!(z_z_star.im, Rational64::new(0, 1));
    }
}

#[test]
fn test_adversarial_mat2x2_singular_matrix_handling() {
    let zero = ComplexRat::zero();
    let one = ComplexRat::one();
    let eye = Mat2x2::identity();

    // 1. Zero matrix: det = 0, inv = Err
    let z_mat = Mat2x2::new(zero, zero, zero, zero);
    assert_eq!(z_mat.det(), zero);
    assert_eq!(z_mat.inv().unwrap_err(), "Singular matrix: zero determinant");

    // 2. Real rank-1 projection and scaled matrices: det = 0, inv = Err
    let p1 = Mat2x2::new(one, zero, zero, zero);
    assert_eq!(p1.det(), zero);
    assert_eq!(p1.inv().unwrap_err(), "Singular matrix: zero determinant");

    let p_ones = Mat2x2::new(one, one, one, one);
    assert_eq!(p_ones.det(), zero);
    assert_eq!(p_ones.inv().unwrap_err(), "Singular matrix: zero determinant");

    let p_scaled = Mat2x2::new(
        ComplexRat::from_integer(2),
        ComplexRat::from_integer(4),
        ComplexRat::from_integer(3),
        ComplexRat::from_integer(6),
    );
    assert_eq!(p_scaled.det(), zero);
    assert_eq!(p_scaled.inv().unwrap_err(), "Singular matrix: zero determinant");

    // 3. Complex rank-1 singular matrices: det = 0, inv = Err
    // c1: [1, i; -i, 1] -> det = 1 - (-i * i) = 1 - 1 = 0
    let c1 = Mat2x2::new(one, ComplexRat::i(), -ComplexRat::i(), one);
    assert_eq!(c1.det(), zero);
    assert_eq!(c1.inv().unwrap_err(), "Singular matrix: zero determinant");

    // c2: [1+i, 2; i, 1+i] -> det = (1+i)^2 - 2i = 2i - 2i = 0
    let one_plus_i = ComplexRat::new(Rational64::new(1, 1), Rational64::new(1, 1));
    let c2 = Mat2x2::new(one_plus_i, ComplexRat::from_integer(2), ComplexRat::i(), one_plus_i);
    assert_eq!(c2.det(), zero);
    assert_eq!(c2.inv().unwrap_err(), "Singular matrix: zero determinant");

    // 4. Inversion error propagation into commutator_holonomy
    assert_eq!(p1.commutator_holonomy(&eye).unwrap_err(), "Singular matrix: zero determinant");
    assert_eq!(eye.commutator_holonomy(&p1).unwrap_err(), "Singular matrix: zero determinant");
    assert_eq!(p1.commutator_holonomy(&p_ones).unwrap_err(), "Singular matrix: zero determinant");
    assert!(LineonHingeConfig::compute_defect_sheet_trace(&p1, &eye).is_err());
    assert!(LineonHingeConfig::compute_defect_sheet_trace(&eye, &c1).is_err());
}

#[test]
fn test_adversarial_mat2x2_algebra_invariants() {
    let eye = Mat2x2::identity();

    // 1. General invertible matrices over Q(i)
    let a = Mat2x2::new(
        ComplexRat::new(Rational64::new(1, 2), Rational64::new(0, 1)),
        ComplexRat::new(Rational64::new(2, 3), Rational64::new(0, 1)),
        ComplexRat::new(Rational64::new(-1, 4), Rational64::new(0, 1)),
        ComplexRat::new(Rational64::new(3, 5), Rational64::new(0, 1)),
    );
    let b = Mat2x2::new(
        ComplexRat::new(Rational64::new(-3, 2), Rational64::new(0, 1)),
        ComplexRat::new(Rational64::new(1, 7), Rational64::new(0, 1)),
        ComplexRat::new(Rational64::new(2, 3), Rational64::new(0, 1)),
        ComplexRat::new(Rational64::new(5, 4), Rational64::new(0, 1)),
    );

    // Matrix inverse axiom: A * A^-1 = I, A^-1 * A = I
    let a_inv = a.inv().expect("a is invertible");
    let a_a_inv = a.mul(&a_inv);
    let a_inv_a = a_inv.mul(&a);
    assert_eq!(a_a_inv, eye);
    assert_eq!(a_inv_a, eye);

    // Determinant multiplicativity: det(AB) = det(A) * det(B)
    let ab = a.mul(&b);
    let det_ab = ab.det();
    let det_a_times_det_b = a.det() * b.det();
    assert_eq!(det_ab, det_a_times_det_b);

    // Trace cyclicity: Tr(AB) = Tr(BA) even though AB != BA
    let ba = b.mul(&a);
    assert_ne!(ab, ba);
    assert_eq!(ab.trace(), ba.trace());

    // 2. Complex Gaussian rational non-commuting matrices
    let c1 = Mat2x2::new(
        ComplexRat::new(Rational64::new(1, 1), Rational64::new(1, 1)),
        ComplexRat::from_integer(2),
        -ComplexRat::i(),
        ComplexRat::new(Rational64::new(3, 1), Rational64::new(-2, 1)),
    );
    let c2 = Mat2x2::new(
        ComplexRat::new(Rational64::new(2, 1), Rational64::new(-1, 1)),
        ComplexRat::new(Rational64::new(1, 1), Rational64::new(3, 1)),
        ComplexRat::from_integer(4),
        -ComplexRat::one(),
    );

    let c1_inv = c1.inv().expect("c1 invertible");
    assert_eq!(c1.mul(&c1_inv), eye);
    assert_eq!(c1_inv.mul(&c1), eye);

    let c1c2 = c1.mul(&c2);
    let c2c1 = c2.mul(&c1);
    assert_ne!(c1c2, c2c1);
    assert_eq!(c1c2.trace(), c2c1.trace());
    assert_eq!(c1c2.det(), c1.det() * c2.det());
}

#[test]
fn test_adversarial_commutator_holonomy_generator_selections() {
    let px = Mat2x2::pauli_x();
    let py = Mat2x2::pauli_y();
    let pz = Mat2x2::pauli_z();
    let eye = Mat2x2::identity();

    // 1. All 3 canonical Pauli pairs: Z/X, X/Y, Y/Z
    let m_zx = pz.commutator_holonomy(&px).unwrap();
    let m_xy = px.commutator_holonomy(&py).unwrap();
    let m_yz = py.commutator_holonomy(&pz).unwrap();

    assert_eq!(m_zx.trace(), ComplexRat::from_integer(-2));
    assert_eq!(m_xy.trace(), ComplexRat::from_integer(-2));
    assert_eq!(m_yz.trace(), ComplexRat::from_integer(-2));

    // 2. All 3 reversed Pauli pairs: X/Z, Y/X, Z/Y
    let m_xz = px.commutator_holonomy(&pz).unwrap();
    let m_yx = py.commutator_holonomy(&px).unwrap();
    let m_zy = pz.commutator_holonomy(&py).unwrap();

    assert_eq!(m_xz.trace(), ComplexRat::from_integer(-2));
    assert_eq!(m_yx.trace(), ComplexRat::from_integer(-2));
    assert_eq!(m_zy.trace(), ComplexRat::from_integer(-2));

    // 3. In SL(2), all commutator holonomies have exact determinant 1
    for m in [&m_zx, &m_xy, &m_yz, &m_xz, &m_yx, &m_zy] {
        assert_eq!(m.det(), ComplexRat::one());
    }

    // 4. Commutator with self or identity yields I and trace +2
    let self_pairs = [
        (&eye, &eye),
        (&px, &px),
        (&py, &py),
        (&pz, &pz),
        (&eye, &px),
        (&eye, &py),
        (&eye, &pz),
    ];
    for (a, b) in self_pairs {
        let m = a.commutator_holonomy(b).unwrap();
        assert_eq!(m, eye);
        assert_eq!(m.trace(), ComplexRat::from_integer(2));
        assert_eq!(m.det(), ComplexRat::one());
    }

    // 5. Phase gate S = diag(1, i): non-involutory commutator
    let s = Mat2x2::new(
        ComplexRat::one(),
        ComplexRat::zero(),
        ComplexRat::zero(),
        ComplexRat::i(),
    );
    let m_s_x = s.commutator_holonomy(&px).unwrap();
    assert_eq!(m_s_x.det(), ComplexRat::one());
    // Tr(S X S^-1 X^-1) = Tr(diag(-i, i)) = 0
    assert_eq!(m_s_x.trace(), ComplexRat::zero());
    assert_eq!(LineonHingeConfig::fracton_defect_mass_from_trace(0), 0);
}

#[test]
fn test_adversarial_defect_mass_boundary_step_function() {
    // Step function: Tr < 0 => Phi1 = 2, Tr >= 0 => Phi1 = 0
    let negative_traces = [-10, -5, -3, -2, -1];
    for tr in negative_traces {
        assert_eq!(LineonHingeConfig::fracton_defect_mass_from_trace(tr), 2);
    }

    let non_negative_traces = [0, 1, 2, 3, 5, 10];
    for tr in non_negative_traces {
        assert_eq!(LineonHingeConfig::fracton_defect_mass_from_trace(tr), 0);
    }

    // Boundary jump across 0
    assert_eq!(LineonHingeConfig::fracton_defect_mass_from_trace(-1), 2);
    assert_eq!(LineonHingeConfig::fracton_defect_mass_from_trace(0), 0);
    assert_eq!(LineonHingeConfig::fracton_defect_mass_from_trace(1), 0);
}

#[test]
fn test_adversarial_corner_coupling_and_foliated_projection() {
    // Corner lineon coupling: sign obstruction is strictly preserved (-2 < 0)
    assert_eq!(LineonHingeConfig::foliated_projected_trace(true, true), -2);
    assert_eq!(LineonHingeConfig::foliated_projected_trace(true, false), 2);

    // Decoupled foliation: trace projected to positive semi-definite values (|tr|^2 = 4 >= 0)
    assert_eq!(LineonHingeConfig::foliated_projected_trace(false, true), 4);
    assert_eq!(LineonHingeConfig::foliated_projected_trace(false, false), 4);
    assert!(LineonHingeConfig::foliated_projected_trace(false, true) >= 0);
    assert!(LineonHingeConfig::foliated_projected_trace(false, false) >= 0);
}

#[test]
fn test_adversarial_quaternion_algebra_and_holonomy() {
    // Zero inversion refusal
    assert!(QuaternionRat::zero().inv().is_err());
    assert_eq!(
        QuaternionRat::zero().inv().unwrap_err(),
        "Division by zero in QuaternionRat inverse"
    );

    let qi = QuaternionRat::i_unit();
    let qj = QuaternionRat::j_unit();
    let qk = QuaternionRat::k_unit();
    let q1 = QuaternionRat::one();

    // Inverses: q * q^-1 = 1
    for q in [qi, qj, qk] {
        let q_inv = q.inv().expect("Basis quaternion invertible");
        assert_eq!(q.mul(&q_inv), q1);
        assert_eq!(q_inv.mul(&q), q1);
    }

    // All 6 pairs of distinct quaternion units have commutator = -1, character trace = -2
    let pairs = [
        (qi, qj),
        (qj, qi),
        (qj, qk),
        (qk, qj),
        (qk, qi),
        (qi, qk),
    ];
    for (a, b) in pairs {
        let m = a.commutator_holonomy(&b).unwrap();
        assert_eq!(m.character_trace(), Rational64::from_integer(-2));
        assert_eq!(m, QuaternionRat::new(Rational64::from_integer(-1), Rational64::zero(), Rational64::zero(), Rational64::zero()));
    }

    // Commutator with self yields 1 and character trace +2
    for q in [q1, qi, qj, qk] {
        let m = q.commutator_holonomy(&q).unwrap();
        assert_eq!(m, q1);
        assert_eq!(m.character_trace(), Rational64::from_integer(2));
    }
}

#[test]
fn test_multi_hinge_y_junction_exchange_and_axis_conservation() {
    let (steps, collision_free, valid_hops, exchanged, sign, ab_w, nonab_w, axis_swap_allowed) =
        LineonHingeConfig::verify_y_junction_exchange_statistics();
    assert_eq!(steps, 6);
    assert!(collision_free);
    assert!(valid_hops);
    assert!(exchanged);
    assert_eq!(sign, -1);
    assert_eq!(ab_w, -2);
    assert_eq!(nonab_w, 2);
    assert!(!axis_swap_allowed);
}


