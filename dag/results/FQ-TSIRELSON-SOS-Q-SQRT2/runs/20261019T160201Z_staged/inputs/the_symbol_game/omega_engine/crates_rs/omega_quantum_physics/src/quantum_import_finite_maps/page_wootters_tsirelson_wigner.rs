// AuthorityEffect: None.
//! QM-218 Page-Wootters clock dressing, Tsirelson SOS, and (Z_3)^2 Wigner.
//! Re-exported from `quantum_import_finite_maps`.

use num_bigint::BigInt;
use num_rational::BigRational;
use num_traits::{One, Signed, Zero};

use super::q;
use super::*;

pub(crate) mod cyclotomic_rings;
pub use cyclotomic_rings::{Cyclo3, Cyclo8};
use cyclotomic_rings::*;

// ============================================================================
// QM-218: Page-Wootters Clock Dressing, Cyclotomic Q(zeta_8) Tsirelson SOS,
//         and Discrete Weyl-Wigner Phase Space on (Z_3)^2 over Q(zeta_3)
// ============================================================================

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Qm218PageWoottersTsirelsonWignerReport {
    pub pw_history_shift_unitary_and_order_4: bool,
    pub pw_constraint_projector_idempotent_hermitian: bool,
    pub pw_constraint_projector_trace: i64,
    pub pw_constraint_annihilates_projector: bool,
    pub pw_dressing_intertwines_history_shift: bool,
    pub pw_dressing_decouples_projector: bool,
    pub pw_bare_observable_breaks_constraint: bool,
    pub pw_relational_observables_commute_with_constraint: bool,
    pub pw_heisenberg_step_covariance_exact: bool,
    pub pw_static_state_sigma_x_ticks: Vec<Q>,
    pub pw_static_state_sigma_y_ticks: Vec<Q>,
    pub chsh_classical_polytope_vertex_count: usize,
    pub chsh_classical_polytope_max: Q,
    pub chsh_cyclotomic_sqrt2_squares_to_2: bool,
    pub chsh_cyclotomic_sqrt2_inverse_exact: bool,
    pub chsh_observables_involutory_and_spacelike_commuting: bool,
    pub chsh_landau_identity_exact: bool,
    pub chsh_sos_decomposition_exact: bool,
    pub chsh_bell_state_annihilated_by_sos_witnesses: bool,
    pub chsh_bell_state_eigenvalue_is_2_sqrt2: bool,
    pub chsh_separable_state_expectation_is_sqrt2: bool,
    pub wigner_phase_point_hermitian_involutory_unit_trace: bool,
    pub wigner_phase_point_orthogonality_and_completeness: bool,
    pub wigner_line_marginals_match_projectors: bool,
    pub wigner_stabilizer_nonnegative_and_normalized: bool,
    pub wigner_stabilizer_negativity: Q,
    pub wigner_superposition_normalized_and_marginals_exact: bool,
    pub wigner_superposition_min_value: Q,
    pub wigner_superposition_negativity: Q,
    pub sqrt2_square_bounds_enclose_two: bool,
    pub tsirelson_bound_decimal_12: String,
    pub tsirelson_bound_12_digits_agree: bool,
    pub bell_violation_excess_decimal_12: String,
    pub bell_violation_excess_12_digits_agree: bool,
    pub tsirelson_per_correlator_decimal_12: String,
    pub tsirelson_per_correlator_12_digits_agree: bool,
}


pub fn evaluate_qm218_page_wootters_tsirelson_wigner() -> Qm218PageWoottersTsirelsonWignerReport {
    // Part (a): Page-Wootters Relational Clock Dressing over Q(i)
    let i4 = qi_dyn_eye(4);
    let i2 = qi_dyn_eye(2);
    let i8 = qi_dyn_eye(8);

    let mut s_c = qi_dyn_zeros(4);
    for t in 0..4 {
        s_c[(t + 1) % 4][t] = Qi::one();
    }

    let mut u_s = qi_dyn_zeros(2);
    u_s[0][0] = Qi::one();
    u_s[1][1] = Qi::i_unit();

    let w_hist = qi_dyn_kron(&s_c, &u_s);
    let w2 = qi_dyn_mul(&w_hist, &w_hist);
    let w3 = qi_dyn_mul(&w2, &w_hist);
    let w4 = qi_dyn_mul(&w3, &w_hist);
    let w_powers = [i8.clone(), w_hist.clone(), w2.clone(), w3.clone()];

    let unitary_order4_ok = qi_dyn_mul(&qi_dyn_dagger(&w_hist), &w_hist) == i8 && w4 == i8;

    let c_pw = qi_dyn_sub(&i8, &w_hist);
    let pi_pw = qi_dyn_scale(
        q(1, 4),
        &qi_dyn_add(&qi_dyn_add(&i8, &w_hist), &qi_dyn_add(&w2, &w3)),
    );
    let proj_idem_herm_ok =
        qi_dyn_mul(&pi_pw, &pi_pw) == pi_pw && qi_dyn_dagger(&pi_pw) == pi_pw;
    let tr_pi = qi_dyn_trace(&pi_pw);
    assert!(tr_pi.im.is_zero());
    let proj_trace = *tr_pi.re.numer();
    let annihilates_ok =
        qi_dyn_is_zero(&qi_dyn_mul(&c_pw, &pi_pw)) && qi_dyn_is_zero(&qi_dyn_mul(&pi_pw, &c_pw));

    let us2 = qi_dyn_mul(&u_s, &u_s);
    let us3 = qi_dyn_mul(&us2, &u_s);
    let u_s_pows = [i2.clone(), u_s.clone(), us2, us3];
    let mut d_dress = qi_dyn_zeros(8);
    for t in 0..4 {
        let mut proj_t = qi_dyn_zeros(4);
        proj_t[t][t] = Qi::one();
        d_dress = qi_dyn_add(&d_dress, &qi_dyn_kron(&proj_t, &u_s_pows[t]));
    }
    let d_dag = qi_dyn_dagger(&d_dress);
    let intertwine_ok =
        qi_dyn_mul(&d_dag, &qi_dyn_mul(&w_hist, &d_dress)) == qi_dyn_kron(&s_c, &i2);

    let sc2 = qi_dyn_mul(&s_c, &s_c);
    let sc3 = qi_dyn_mul(&sc2, &s_c);
    let pi_c0 = qi_dyn_scale(
        q(1, 4),
        &qi_dyn_add(&qi_dyn_add(&i4, &s_c), &qi_dyn_add(&sc2, &sc3)),
    );
    let decouple_ok =
        qi_dyn_mul(&d_dag, &qi_dyn_mul(&pi_pw, &d_dress)) == qi_dyn_kron(&pi_c0, &i2);

    let sigma_x = vec![
        vec![Qi::zero(), Qi::one()],
        vec![Qi::one(), Qi::zero()],
    ];
    let sigma_y = vec![
        vec![Qi::zero(), Qi::new(Q::zero(), q(-1, 1))],
        vec![Qi::i_unit(), Qi::zero()],
    ];

    let bare_breaks_ok = !qi_dyn_is_zero(&qi_dyn_comm(&qi_dyn_kron(&i4, &sigma_x), &w_hist));

    let relational_observable = |tau: usize, obs_s: &QiDynMat| -> QiDynMat {
        let mut proj_tau = qi_dyn_zeros(4);
        proj_tau[tau][tau] = Qi::one();
        let seed = qi_dyn_kron(&proj_tau, obs_s);
        let mut acc = qi_dyn_zeros(8);
        for k in 0..4 {
            let wk = &w_powers[k];
            let wk_dag = qi_dyn_dagger(wk);
            acc = qi_dyn_add(&acc, &qi_dyn_mul(&wk_dag, &qi_dyn_mul(&seed, wk)));
        }
        acc
    };

    let mut psi0_hist = vec![Qi::zero(); 8];
    psi0_hist[0] = Qi::one();
    psi0_hist[1] = Qi::one();
    let psi_hist: Vec<Qi> = qi_dyn_matvec(&pi_pw, &psi0_hist)
        .into_iter()
        .map(|c| Qi::from_q(q(2, 1)).mul(c))
        .collect();
    let norm_hist = qi_dyn_inner(&psi_hist, &psi_hist);
    assert_eq!(norm_hist, Qi::from_q(q(2, 1)));

    let mut rel_comm_ok = true;
    let mut heisenberg_ok = true;
    let mut sx_ticks = Vec::with_capacity(4);
    let mut sy_ticks = Vec::with_capacity(4);
    let us_dag_sx_us = qi_dyn_mul(&qi_dyn_dagger(&u_s), &qi_dyn_mul(&sigma_x, &u_s));

    for tau in 0..4 {
        let orel_x = relational_observable(tau, &sigma_x);
        let orel_y = relational_observable(tau, &sigma_y);
        if !qi_dyn_is_zero(&qi_dyn_comm(&orel_x, &w_hist))
            || !qi_dyn_is_zero(&qi_dyn_comm(&orel_x, &pi_pw))
            || !qi_dyn_is_zero(&qi_dyn_comm(&orel_y, &w_hist))
            || !qi_dyn_is_zero(&qi_dyn_comm(&orel_y, &pi_pw))
        {
            rel_comm_ok = false;
        }
        let orel_x_next = relational_observable((tau + 1) % 4, &sigma_x);
        let orel_x_heis = relational_observable(tau, &us_dag_sx_us);
        if orel_x_next != orel_x_heis {
            heisenberg_ok = false;
        }
        let ex = qi_dyn_inner(&psi_hist, &qi_dyn_matvec(&orel_x, &psi_hist));
        let ey = qi_dyn_inner(&psi_hist, &qi_dyn_matvec(&orel_y, &psi_hist));
        assert!(ex.im.is_zero() && ey.im.is_zero());
        sx_ticks.push(ex.re / norm_hist.re);
        sy_ticks.push(ey.re / norm_hist.re);
    }

    // Part (b): Cyclotomic Q(zeta_8) Tsirelson Bound & SOS Certificate
    let mut polytope_count = 0usize;
    let mut polytope_max = Q::zero();
    for mask in 0..16 {
        let a0 = if (mask & 1) != 0 { 1i64 } else { -1i64 };
        let a1 = if (mask & 2) != 0 { 1i64 } else { -1i64 };
        let b0 = if (mask & 4) != 0 { 1i64 } else { -1i64 };
        let b1 = if (mask & 8) != 0 { 1i64 } else { -1i64 };
        let val = q((a0 * (b0 + b1) + a1 * (b0 - b1)).abs(), 1);
        polytope_count += 1;
        if val > polytope_max {
            polytope_max = val;
        }
    }

    let s2 = Cyclo8::sqrt2();
    let inv_s2 = Cyclo8::inv_sqrt2();
    let one_z8 = Cyclo8::one();
    let zero_z8 = Cyclo8::zero();
    let sqrt2_sq_ok = s2.mul(s2) == Cyclo8::from_int(2) && s2.conj() == s2;
    let sqrt2_inv_ok = s2.mul(inv_s2) == one_z8 && inv_s2.conj() == inv_s2;

    let z_pauli = vec![vec![one_z8, zero_z8], vec![zero_z8, one_z8.neg()]];
    let x_pauli = vec![vec![zero_z8, one_z8], vec![one_z8, zero_z8]];
    let i2_z8 = z8_eye(2);
    let i4_z8 = z8_eye(4);

    let a0_op = z8_kron(&z_pauli, &i2_z8);
    let a1_op = z8_kron(&x_pauli, &i2_z8);
    let b0_single = z8_scale(inv_s2, &z8_add(&z_pauli, &x_pauli));
    let b1_single = z8_scale(inv_s2, &z8_sub(&z_pauli, &x_pauli));
    let b0_op = z8_kron(&i2_z8, &b0_single);
    let b1_op = z8_kron(&i2_z8, &b1_single);

    let mut inv_comm_ok = true;
    for op in [&a0_op, &a1_op, &b0_op, &b1_op] {
        if z8_mul(op, op) != i4_z8 || z8_dagger(op) != *op {
            inv_comm_ok = false;
        }
    }
    for ai in [&a0_op, &a1_op] {
        for bj in [&b0_op, &b1_op] {
            if !z8_is_zero(&z8_comm(ai, bj)) {
                inv_comm_ok = false;
            }
        }
    }

    let b_chsh = z8_add(
        &z8_mul(&a0_op, &z8_add(&b0_op, &b1_op)),
        &z8_mul(&a1_op, &z8_sub(&b0_op, &b1_op)),
    );
    let b_chsh_sq = z8_mul(&b_chsh, &b_chsh);
    let landau_rhs = z8_sub(
        &z8_scale(Cyclo8::from_int(4), &i4_z8),
        &z8_mul(&z8_comm(&a0_op, &a1_op), &z8_comm(&b0_op, &b1_op)),
    );
    let landau_ok = b_chsh_sq == landau_rhs;

    let w1_sos = z8_sub(&z8_scale(inv_s2, &z8_add(&a0_op, &a1_op)), &b0_op);
    let w2_sos = z8_sub(&z8_scale(inv_s2, &z8_sub(&a0_op, &a1_op)), &b1_op);
    let sos_sum = z8_add(
        &z8_mul(&z8_dagger(&w1_sos), &w1_sos),
        &z8_mul(&z8_dagger(&w2_sos), &w2_sos),
    );
    let sos_lhs = z8_sub(
        &z8_scale(Cyclo8::from_int(4), &i4_z8),
        &z8_scale(s2, &b_chsh),
    );
    let sos_equiv_lhs = z8_sub(
        &z8_scale(Cyclo8::from_int(2).mul(s2), &i4_z8),
        &b_chsh,
    );
    let sos_equiv_rhs = z8_scale(inv_s2, &sos_sum);
    let sos_ok = sos_lhs == sos_sum && sos_equiv_lhs == sos_equiv_rhs;

    let phi_plus = vec![one_z8, zero_z8, zero_z8, one_z8];
    let w1_phi = z8_matvec(&w1_sos, &phi_plus);
    let w2_phi = z8_matvec(&w2_sos, &phi_plus);
    let bell_annihilated_ok =
        w1_phi.iter().all(|c| c.is_zero()) && w2_phi.iter().all(|c| c.is_zero());

    let b_phi = z8_matvec(&b_chsh, &phi_plus);
    let two_s2 = Cyclo8::from_int(2).mul(s2);
    let bell_eigen_ok = (0..4).all(|k| b_phi[k] == two_s2.mul(phi_plus[k]));

    let sep_00 = vec![one_z8, zero_z8, zero_z8, zero_z8];
    let sep_exp = z8_inner(&sep_00, &z8_matvec(&b_chsh, &sep_00));
    let sep_ok = sep_exp == s2;

    // Part (c): Discrete Weyl-Wigner on (Z_3)^2 & 12-Decimal Enclosures
    let i3_z3 = z3_eye3();
    let mut herm_inv_tr_ok = true;
    let mut ortho_comp_ok = true;
    let mut sum_all_aqp = z3_zeros3();
    let mut all_aqp = [[z3_zeros3(); 3]; 3];
    for q_idx in 0..3 {
        for p_idx in 0..3 {
            all_aqp[q_idx][p_idx] = wigner_phase_point_z3(q_idx, p_idx);
        }
    }

    for q_idx in 0..3 {
        for p_idx in 0..3 {
            let aqp = &all_aqp[q_idx][p_idx];
            sum_all_aqp = z3_add3(&sum_all_aqp, aqp);
            if z3_dagger3(aqp) != *aqp
                || z3_mul3(aqp, aqp) != i3_z3
                || z3_trace3(aqp) != Cyclo3::from_int(1)
            {
                herm_inv_tr_ok = false;
            }
            for q2 in 0..3 {
                for p2 in 0..3 {
                    let tr_prod = z3_trace3(&z3_mul3(aqp, &all_aqp[q2][p2]));
                    let expected = Cyclo3::from_int(if q_idx == q2 && p_idx == p2 { 3 } else { 0 });
                    if tr_prod != expected {
                        ortho_comp_ok = false;
                    }
                }
            }
        }
    }
    if z3_scale3(q(1, 3), &sum_all_aqp) != i3_z3 {
        ortho_comp_ok = false;
    }

    let mut line_marginals_ok = true;
    for q_idx in 0..3 {
        let mut sum_p = z3_zeros3();
        for p_idx in 0..3 {
            sum_p = z3_add3(&sum_p, &all_aqp[q_idx][p_idx]);
        }
        let mut proj_q = z3_zeros3();
        proj_q[q_idx][q_idx] = Cyclo3::from_int(1);
        if z3_scale3(q(1, 3), &sum_p) != proj_q {
            line_marginals_ok = false;
        }
    }
    for p_idx in 0..3 {
        let mut sum_q = z3_zeros3();
        for q_idx in 0..3 {
            sum_q = z3_add3(&sum_q, &all_aqp[q_idx][p_idx]);
        }
        let mut proj_p = z3_zeros3();
        for x in 0..3 {
            for y in 0..3 {
                let exp = (p_idx as i64) * ((x as i64) - (y as i64));
                proj_p[x][y] = Cyclo3::omega_pow(exp).scale(q(1, 3));
            }
        }
        if z3_scale3(q(1, 3), &sum_q) != proj_p {
            line_marginals_ok = false;
        }
    }

    let psi_stab = [
        Cyclo3::from_int(1),
        Cyclo3::from_int(0),
        Cyclo3::from_int(0),
    ];
    let w_stab = compute_wigner_table_z3_rust(&psi_stab);
    let mut stab_sum = Q::zero();
    let mut stab_abs_sum = Q::zero();
    let mut stab_nonneg = true;
    for q_idx in 0..3 {
        for p_idx in 0..3 {
            let v = w_stab[q_idx][p_idx];
            if v < Q::zero() {
                stab_nonneg = false;
            }
            stab_sum += v;
            stab_abs_sum += v.abs();
        }
    }
    let stab_nonneg_norm_ok = stab_nonneg && stab_sum == Q::one();
    let stab_negativity = stab_abs_sum - Q::one();

    let psi_neg = [
        Cyclo3::from_int(1),
        Cyclo3::from_int(-1),
        Cyclo3::from_int(0),
    ];
    let w_neg = compute_wigner_table_z3_rust(&psi_neg);
    let mut neg_sum = Q::zero();
    let mut neg_abs_sum = Q::zero();
    let mut super_min = Q::one();
    for q_idx in 0..3 {
        for p_idx in 0..3 {
            let v = w_neg[q_idx][p_idx];
            neg_sum += v;
            neg_abs_sum += v.abs();
            if v < super_min {
                super_min = v;
            }
        }
    }
    let pos_marginals: Vec<Q> = (0..3)
        .map(|q_idx| (0..3).map(|p_idx| w_neg[q_idx][p_idx]).sum())
        .collect();
    let mom_marginals: Vec<Q> = (0..3)
        .map(|p_idx| (0..3).map(|q_idx| w_neg[q_idx][p_idx]).sum())
        .collect();
    let super_ok = neg_sum == Q::one()
        && pos_marginals == vec![q(1, 2), q(1, 2), q(0, 1)]
        && mom_marginals == vec![q(0, 1), q(1, 2), q(1, 2)]
        && w_neg[2][0] == q(-1, 3);
    let super_negativity = neg_abs_sum - Q::one();

    // Certified 12-decimal enclosures for sqrt(2), 2*sqrt(2), 2*sqrt(2) - 2, and sqrt(2)/2
    let denom = BigInt::from(10u64).pow(24);
    let lo_num: BigInt = "1414213562373095048801688".parse().expect("valid BigInt");
    let hi_num: BigInt = "1414213562373095048801689".parse().expect("valid BigInt");
    let sqrt2_lo = BigRational::new(lo_num, denom.clone());
    let sqrt2_hi = BigRational::new(hi_num, denom);
    let two_br = BigRational::from_integer(BigInt::from(2));
    let sqrt2_cert_ok = &sqrt2_lo * &sqrt2_lo <= two_br && two_br <= &sqrt2_hi * &sqrt2_hi;
    let sqrt2_iv = BigInterval::new(sqrt2_lo, sqrt2_hi);

    let tsirelson_iv = sqrt2_iv.scale(BigRational::from_integer(BigInt::from(2)));
    let (tsirelson_dec_12, _ts_hi, tsirelson_ok) = tsirelson_iv.decimal_prefix(12);

    let excess_iv = tsirelson_iv.sub(&BigInterval::exact(two_br));
    let (excess_dec_12, _ex_hi, excess_ok) = excess_iv.decimal_prefix(12);

    let per_corr_iv = sqrt2_iv.scale(BigRational::new(BigInt::from(1), BigInt::from(2)));
    let (per_corr_dec_12, _pc_hi, per_corr_ok) = per_corr_iv.decimal_prefix(12);

    Qm218PageWoottersTsirelsonWignerReport {
        pw_history_shift_unitary_and_order_4: unitary_order4_ok,
        pw_constraint_projector_idempotent_hermitian: proj_idem_herm_ok,
        pw_constraint_projector_trace: proj_trace,
        pw_constraint_annihilates_projector: annihilates_ok,
        pw_dressing_intertwines_history_shift: intertwine_ok,
        pw_dressing_decouples_projector: decouple_ok,
        pw_bare_observable_breaks_constraint: bare_breaks_ok,
        pw_relational_observables_commute_with_constraint: rel_comm_ok,
        pw_heisenberg_step_covariance_exact: heisenberg_ok,
        pw_static_state_sigma_x_ticks: sx_ticks,
        pw_static_state_sigma_y_ticks: sy_ticks,
        chsh_classical_polytope_vertex_count: polytope_count,
        chsh_classical_polytope_max: polytope_max,
        chsh_cyclotomic_sqrt2_squares_to_2: sqrt2_sq_ok,
        chsh_cyclotomic_sqrt2_inverse_exact: sqrt2_inv_ok,
        chsh_observables_involutory_and_spacelike_commuting: inv_comm_ok,
        chsh_landau_identity_exact: landau_ok,
        chsh_sos_decomposition_exact: sos_ok,
        chsh_bell_state_annihilated_by_sos_witnesses: bell_annihilated_ok,
        chsh_bell_state_eigenvalue_is_2_sqrt2: bell_eigen_ok,
        chsh_separable_state_expectation_is_sqrt2: sep_ok,
        wigner_phase_point_hermitian_involutory_unit_trace: herm_inv_tr_ok,
        wigner_phase_point_orthogonality_and_completeness: ortho_comp_ok,
        wigner_line_marginals_match_projectors: line_marginals_ok,
        wigner_stabilizer_nonnegative_and_normalized: stab_nonneg_norm_ok,
        wigner_stabilizer_negativity: stab_negativity,
        wigner_superposition_normalized_and_marginals_exact: super_ok,
        wigner_superposition_min_value: super_min,
        wigner_superposition_negativity: super_negativity,
        sqrt2_square_bounds_enclose_two: sqrt2_cert_ok,
        tsirelson_bound_decimal_12: tsirelson_dec_12,
        tsirelson_bound_12_digits_agree: tsirelson_ok,
        bell_violation_excess_decimal_12: excess_dec_12,
        bell_violation_excess_12_digits_agree: excess_ok,
        tsirelson_per_correlator_decimal_12: per_corr_dec_12,
        tsirelson_per_correlator_12_digits_agree: per_corr_ok,
    }
}

#[cfg(test)]
mod tests {
    use super::super::q;
    use super::*;

    #[test]
    fn test_qm218_page_wootters_tsirelson_wigner_control() {
        let r = evaluate_qm218_page_wootters_tsirelson_wigner();
        assert!(r.pw_history_shift_unitary_and_order_4);
        assert!(r.pw_constraint_projector_idempotent_hermitian);
        assert_eq!(r.pw_constraint_projector_trace, 2);
        assert!(r.pw_constraint_annihilates_projector);
        assert!(r.pw_dressing_intertwines_history_shift);
        assert!(r.pw_dressing_decouples_projector);
        assert!(r.pw_bare_observable_breaks_constraint);
        assert!(r.pw_relational_observables_commute_with_constraint);
        assert!(r.pw_heisenberg_step_covariance_exact);
        assert_eq!(
            r.pw_static_state_sigma_x_ticks,
            vec![q(1, 1), q(0, 1), q(-1, 1), q(0, 1)]
        );
        assert_eq!(
            r.pw_static_state_sigma_y_ticks,
            vec![q(0, 1), q(1, 1), q(0, 1), q(-1, 1)]
        );
        assert_eq!(r.chsh_classical_polytope_vertex_count, 16);
        assert_eq!(r.chsh_classical_polytope_max, q(2, 1));
        assert!(r.chsh_cyclotomic_sqrt2_squares_to_2);
        assert!(r.chsh_cyclotomic_sqrt2_inverse_exact);
        assert!(r.chsh_observables_involutory_and_spacelike_commuting);
        assert!(r.chsh_landau_identity_exact);
        assert!(r.chsh_sos_decomposition_exact);
        assert!(r.chsh_bell_state_annihilated_by_sos_witnesses);
        assert!(r.chsh_bell_state_eigenvalue_is_2_sqrt2);
        assert!(r.chsh_separable_state_expectation_is_sqrt2);
        assert!(r.wigner_phase_point_hermitian_involutory_unit_trace);
        assert!(r.wigner_phase_point_orthogonality_and_completeness);
        assert!(r.wigner_line_marginals_match_projectors);
        assert!(r.wigner_stabilizer_nonnegative_and_normalized);
        assert_eq!(r.wigner_stabilizer_negativity, q(0, 1));
        assert!(r.wigner_superposition_normalized_and_marginals_exact);
        assert_eq!(r.wigner_superposition_min_value, q(-1, 3));
        assert_eq!(r.wigner_superposition_negativity, q(2, 3));
        assert!(r.sqrt2_square_bounds_enclose_two);
        assert_eq!(r.tsirelson_bound_decimal_12, "2.828427124746");
        assert!(r.tsirelson_bound_12_digits_agree);
        assert_eq!(r.bell_violation_excess_decimal_12, "0.828427124746");
        assert!(r.bell_violation_excess_12_digits_agree);
        assert_eq!(r.tsirelson_per_correlator_decimal_12, "0.707106781186");
        assert!(r.tsirelson_per_correlator_12_digits_agree);
    }
}
