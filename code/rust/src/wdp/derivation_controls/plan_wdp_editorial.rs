//! Finite controls for PLAN-WDP-EDITORIAL (E1-E12).
//! Nonsurjective singleton factorization, mixed-sign weight boundedness,
//! bit-to-sign CHSH conversion, vector-target adapter descent, and J.6 switching sum.

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct EditorialSummary {
    pub e1_two_target_factors: usize,
    pub e1_singleton_factors: usize,
    pub e1_sections: usize,
    pub e2_bounded_min: i64,
    pub e2_unbounded_min: i64,
    pub e3_sign_only_pm2: bool,
    pub e3_raw_bits_fail_pm2: bool,
    pub e4_raw_on_b_num: (i64, i64),
    pub e4_filtered_on_b_num: (i64, i64),
    pub e11_cross_outcome_twice_prob: i64,
    pub e11_unrestricted_twice_prob: i64,
}

pub fn check_e1_nonsurjective(answer_cardinality: usize) -> Result<(usize, usize), &'static str> {
    if answer_cardinality == 0 {
        return Err("answer_cardinality must be positive");
    }
    let q = [0usize, 0usize];
    let target_d = [0usize, 0usize];
    let mut factors = 0usize;
    for f0 in 0..answer_cardinality {
        for f1 in 0..answer_cardinality {
            let bar_d = [f0, f1];
            if bar_d[q[0]] == target_d[0] && bar_d[q[1]] == target_d[1] {
                factors += 1;
            }
        }
    }
    let mut sections = 0usize;
    for s0 in 0..2usize {
        for s1 in 0..2usize {
            if q[s0] == 0 && q[s1] == 1 {
                sections += 1;
            }
        }
    }
    Ok((factors, sections))
}

pub fn check_e2_mixed_weights(w1: i64, w2: i64, x: i64) -> i64 {
    let coeff = w1 + w2;
    let mut min_val = i64::MAX;
    for u in -6..=6 {
        let val = coeff * (x + u).abs();
        if val < min_val {
            min_val = val;
        }
    }
    min_val
}

pub fn check_e3_chsh() -> (bool, bool) {
    let mut sign_ok = true;
    let mut raw_only_pm2 = true;
    for mask in 0..16u8 {
        let a0 = i64::from(mask & 1);
        let a1 = i64::from((mask >> 1) & 1);
        let b0 = i64::from((mask >> 2) & 1);
        let b1 = i64::from((mask >> 3) & 1);
        let raw = a0 * (b0 + b1) + a1 * (b0 - b1);
        if raw != -2 && raw != 2 {
            raw_only_pm2 = false;
        }
        let sa0 = if a0 == 0 { 1 } else { -1 };
        let sa1 = if a1 == 0 { 1 } else { -1 };
        let sb0 = if b0 == 0 { 1 } else { -1 };
        let sb1 = if b1 == 0 { 1 } else { -1 };
        let sign_val = sa0 * (sb0 + sb1) + sa1 * (sb0 - sb1);
        if sign_val != -2 && sign_val != 2 {
            sign_ok = false;
        }
    }
    (sign_ok, !raw_only_pm2)
}

pub fn check_e4_vector_adapter() -> ((i64, i64), (i64, i64)) {
    let v = [1i64, -1, 1, -1];
    let raw_w = ((v[0] + v[1]) / 2, v[2]);
    let dot_v: i64 = v.iter().map(|c| c * c).sum();
    let proj_scale_num = dot_v / 4;
    let reduced = [
        v[0] - proj_scale_num * v[0],
        v[1] - proj_scale_num * v[1],
        v[2] - proj_scale_num * v[2],
        v[3] - proj_scale_num * v[3],
    ];
    let filtered_w = ((reduced[0] + reduced[1]) / 2, reduced[2]);
    (raw_w, filtered_w)
}

pub fn check_e11_switching() -> (i64, i64) {
    let mut cross_twice = 0i64;
    let mut all_twice = 0i64;
    for j in 0..2 {
        for o in 0..2 {
            let term_twice = if j == o { 1 } else { 0 };
            all_twice += term_twice;
            if j != o {
                cross_twice += term_twice;
            }
        }
    }
    (cross_twice, all_twice)
}

pub fn evaluate_editorial_controls() -> Result<EditorialSummary, &'static str> {
    let (e1_two, _) = check_e1_nonsurjective(2)?;
    let (e1_one, e1_sec) = check_e1_nonsurjective(1)?;
    let e2_bounded = check_e2_mixed_weights(-1, 2, 3);
    let e2_unbounded = check_e2_mixed_weights(-2, 1, 3);
    let (e3_sign_ok, e3_raw_fails) = check_e3_chsh();
    let (e4_raw, e4_filtered) = check_e4_vector_adapter();
    let (e11_cross, e11_all) = check_e11_switching();
    Ok(EditorialSummary {
        e1_two_target_factors: e1_two,
        e1_singleton_factors: e1_one,
        e1_sections: e1_sec,
        e2_bounded_min: e2_bounded,
        e2_unbounded_min: e2_unbounded,
        e3_sign_only_pm2: e3_sign_ok,
        e3_raw_bits_fail_pm2: e3_raw_fails,
        e4_raw_on_b_num: e4_raw,
        e4_filtered_on_b_num: e4_filtered,
        e11_cross_outcome_twice_prob: e11_cross,
        e11_unrestricted_twice_prob: e11_all,
    })
}

#[test]
fn editorial_controls_match_reconciled_manuscript() {
    let summary = evaluate_editorial_controls().expect("valid editorial controls");
    assert_eq!(
        summary,
        EditorialSummary {
            e1_two_target_factors: 2,
            e1_singleton_factors: 1,
            e1_sections: 0,
            e2_bounded_min: 0,
            e2_unbounded_min: -9,
            e3_sign_only_pm2: true,
            e3_raw_bits_fail_pm2: true,
            e4_raw_on_b_num: (0, 1),
            e4_filtered_on_b_num: (0, 0),
            e11_cross_outcome_twice_prob: 0,
            e11_unrestricted_twice_prob: 2,
        }
    );
    assert_eq!(
        check_e1_nonsurjective(0),
        Err("answer_cardinality must be positive")
    );
}
