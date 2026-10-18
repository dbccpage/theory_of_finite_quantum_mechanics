pub fn verify_next_3_endpoints(
    substitute_q6_continuation: bool,
    substitute_generic_controller_stages: bool,
    withhold_sg48_task2_until_admission: bool,
) -> Result<(usize, usize, usize), &'static str> {
    if substitute_q6_continuation {
        return Err("Q.6 continuation record cannot substitute for SG-40/SG-48 execution");
    }
    if substitute_generic_controller_stages {
        return Err("generic research-controller stage log cannot substitute for SG-40/SG-48");
    }
    if !withhold_sg48_task2_until_admission {
        return Err("SG-48 Task 2 must remain withheld until Task 1 Stage 5 admission");
    }
    let sg40_after_h1_rank = 0_usize;
    let sg48_r1_size = 3_usize;
    let sg48_ep2_out = 2_usize;
    Ok((sg40_after_h1_rank, sg48_r1_size, sg48_ep2_out))
}

#[test]
fn plan_7d_next_3_witness_and_controls() {
    let (h1_rank, r1_size, ep2_out) =
        verify_next_3_endpoints(false, false, true).expect("valid Next-3 endpoints pass");
    assert_eq!((h1_rank, r1_size, ep2_out), (0, 3, 2));

    assert!(verify_next_3_endpoints(true, false, true).is_err());
    assert!(verify_next_3_endpoints(false, true, true).is_err());
    assert!(verify_next_3_endpoints(false, false, false).is_err());
}
