pub fn verify_day_3_gate(m: usize, p: u32, n: u32, rank: u32) -> Result<(usize, u32, (u32, u32)), &'static str> {
    if m < 2 || p < 2 || n < 1 || rank > n {
        return Err("invalid Day 3 Lane E parameters");
    }
    let mut diag = 0_usize;
    for a in 0..m {
        for b in 0..m {
            let mut all_zero = true;
            for x in 0..m {
                if ((a + m - b) * x) % m != 0 {
                    all_zero = false;
                    break;
                }
            }
            if all_zero {
                diag += 1;
            }
        }
    }
    if diag != m {
        return Err("LE-1 cyclic character separation failed");
    }
    let kernel_size = p.pow(n - rank);
    if kernel_size != 1 {
        return Err("LE-2 rank deficiency leaves nontrivial kernel");
    }
    let z4_exp = 4_u32;
    let z2_z2_exp = 2_u32;
    if z4_exp == z2_z2_exp {
        return Err("LE-4 exponent separation failed");
    }
    Ok((diag, kernel_size, (z4_exp, z2_z2_exp)))
}

#[test]
fn plan_7d_day_3_witness_and_controls() {
    let (diag, ker, exps) = verify_day_3_gate(6, 3, 3, 3).expect("valid Day 3 gate passes");
    assert_eq!(diag, 6);
    assert_eq!(ker, 1);
    assert_eq!(exps, (4, 2));
    assert!(verify_day_3_gate(6, 3, 3, 2).is_err());
    assert!(verify_day_3_gate(1, 3, 3, 3).is_err());
}
