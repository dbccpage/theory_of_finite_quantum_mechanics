use std::collections::BTreeSet;

pub fn check_lane_b_and_c_bindings(reset_budget: bool) -> Result<(usize, [usize; 4], i64), &'static str> {
    let mut x0 = BTreeSet::new();
    for x in -1..=1_i64 {
        for y in -1..=1_i64 {
            x0.insert((x, y));
        }
    }
    let x1: BTreeSet<(i64, i64)> = x0.iter().map(|&(x, y)| (x + y, x - y)).collect();
    let x2: BTreeSet<(i64, i64)> = x1.iter().map(|&(u, v)| (u, v + u)).collect();
    if x0.len() != 9 || x1.len() != 9 || x2.len() != 9 {
        return Err("image carrier size mismatch");
    }
    if x1.contains(&(1, 0)) || !x2.contains(&(1, 0)) {
        return Err("probe (1,0) membership mismatch between X1 and X2");
    }
    let mut counts = [0_usize; 4];
    for (idx, d) in [-1_i64, 0, 1, 2].iter().enumerate() {
        counts[idx] = x0.iter().filter(|&&(x, y)| x + y == *d).count();
    }
    if counts != [2, 3, 2, 1] {
        return Err("Lane C solution count mismatch");
    }
    // Lane B Appendix-S table: 15/4 < 4 < 6, original-class-only 7/2
    let disturbance_num = 15_i64;
    let nondisturbing_num = 16_i64; // 16/4 == 4
    if disturbance_num >= nondisturbing_num {
        return Err("Lane B disturbance optimum must be strictly below nondisturbing optimum");
    }
    let budget_cap = 18_i64;
    let round1_spent = 5_i64;
    let remaining = if reset_budget { budget_cap } else { budget_cap - round1_spent };
    if round1_spent + remaining > budget_cap {
        return Err("budget reset allowed cumulative spend above cap");
    }
    Ok((x0.len(), counts, remaining))
}

#[test]
fn plan_7d_next_2_witness_and_controls() {
    let (card, counts, rem) = check_lane_b_and_c_bindings(false).expect("valid bindings pass");
    assert_eq!(card, 9);
    assert_eq!(counts, [2, 3, 2, 1]);
    assert_eq!(rem, 13);
    assert!(check_lane_b_and_c_bindings(true).is_err());
}
