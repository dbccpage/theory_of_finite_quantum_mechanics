pub fn run_sg_40_episode(
    partial_2: [i64; 3],
    beta: i64,
    extension_declared: bool,
    issuer_is_host_stage_5: bool,
) -> Result<(usize, usize, [i64; 3], [i64; 3]), &'static str> {
    if !issuer_is_host_stage_5 {
        return Err("parser self-receipt refused: Stage 5 host verifier required");
    }
    if !extension_declared {
        return Err("undeclared 2-cell attachment refused");
    }
    let partial_1: [[i64; 3]; 3] = [[-1, 0, 1], [1, -1, 0], [0, 1, -1]];
    let z: [i64; 3] = [1, 1, 1];

    let mut d1_z = [0_i64; 3];
    let mut d1_d2 = [0_i64; 3];
    for i in 0..3 {
        for j in 0..3 {
            d1_z[i] += partial_1[i][j] * z[j];
            d1_d2[i] += partial_1[i][j] * partial_2[j];
        }
    }
    if d1_z != [0, 0, 0] {
        return Err("z is not a 1-cycle");
    }
    if d1_d2 != [0, 0, 0] {
        return Err("chain complex identity d1 * d2 = 0 failed");
    }
    let d2_beta = [
        partial_2[0] * beta,
        partial_2[1] * beta,
        partial_2[2] * beta,
    ];
    if d2_beta != z {
        return Err("witness equation d2 * beta = z failed");
    }
    let before_h1_rank = 3 - 2 - 0;
    let after_h1_rank = 3 - 2 - 1;
    Ok((before_h1_rank, after_h1_rank, d1_d2, d2_beta))
}

#[test]
fn sg_40_witness_and_controls() {
    let (before_rank, after_rank, d1_d2, d2_beta) =
        run_sg_40_episode([1, 1, 1], 1, true, true).expect("valid SG-40 episode passes");
    assert_eq!(before_rank, 1);
    assert_eq!(after_rank, 0);
    assert_eq!(d1_d2, [0, 0, 0]);
    assert_eq!(d2_beta, [1, 1, 1]);

    assert!(run_sg_40_episode([1, 1, 1], 0, true, true).is_err());
    assert!(run_sg_40_episode([1, 1, -1], 1, true, true).is_err());
    assert!(run_sg_40_episode([1, 1, 1], 1, false, true).is_err());
    assert!(run_sg_40_episode([1, 1, 1], 1, true, false).is_err());
}
