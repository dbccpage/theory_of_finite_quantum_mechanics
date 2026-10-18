pub fn run_sg_48_episodes(
    candidate_op: [usize; 3],
    verify_stage_5_before_use: bool,
    task2_sealed_during_ep1: bool,
    reuse_ep1_receipt_for_ep2: bool,
    mutate_task1_target: usize,
    promote_uncertified_metalift: bool,
) -> Result<(usize, usize, usize, usize), &'static str> {
    if !task2_sealed_during_ep1 {
        return Err("task_2 must remain sealed until Episode 1 Stage 5 admission");
    }
    if mutate_task1_target != 2 {
        return Err("task_1 target mutation refused");
    }
    if promote_uncertified_metalift {
        return Err("uncertified MetaLift promotion refused");
    }
    if !verify_stage_5_before_use {
        return Err("pre-verification operator execution refused");
    }
    if reuse_ep1_receipt_for_ep2 {
        return Err("cached Episode 1 receipt refused for Episode 2");
    }

    let swap_ab = [1_usize, 0, 2];
    for x in 0..3 {
        let y = candidate_op[x];
        if y >= 3 || candidate_op[y] != x {
            return Err("Stage 5 host verifier rejected non-involution candidate operator");
        }
    }

    let ep1_out = candidate_op[swap_ab[0]];
    if ep1_out != 2 {
        return Err("Episode 1 composition did not reach c");
    }
    let ep2_out = candidate_op[1];
    if ep2_out != 2 {
        return Err("Episode 2 reuse did not reach c");
    }

    Ok((2, 3, ep1_out, ep2_out))
}

#[test]
fn sg_48_witness_and_controls() {
    let (r0_len, r1_len, ep1_out, ep2_out) =
        run_sg_48_episodes([0, 2, 1], true, true, false, 2, false)
            .expect("valid SG-48 two-episode loop passes");
    assert_eq!((r0_len, r1_len, ep1_out, ep2_out), (2, 3, 2, 2));

    assert!(run_sg_48_episodes([0, 2, 1], false, true, false, 2, false).is_err());
    assert!(run_sg_48_episodes([0, 2, 1], true, false, false, 2, false).is_err());
    assert!(run_sg_48_episodes([0, 2, 1], true, true, true, 2, false).is_err());
    assert!(run_sg_48_episodes([0, 2, 1], true, true, false, 1, false).is_err());
    assert!(run_sg_48_episodes([0, 2, 1], true, true, false, 2, true).is_err());
    assert!(run_sg_48_episodes([0, 2, 2], true, true, false, 2, false).is_err());
}
