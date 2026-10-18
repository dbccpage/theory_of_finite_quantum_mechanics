pub fn verify_day_7_audit(
    promote_unrun_sg_episodes: bool,
    promote_open_lane_e_continuum_duality: bool,
    actual_paid_spend_cents: u32,
    pilot_cap_cents: u32,
    campaign_cap_cents: u32,
) -> Result<(usize, usize, usize, u32), &'static str> {
    if promote_unrun_sg_episodes {
        return Err("deadline-driven promotion of NOT_RUN SG episodes refused");
    }
    if promote_open_lane_e_continuum_duality {
        return Err("promotion of open infinite locally compact duality obligation refused");
    }
    if actual_paid_spend_cents > pilot_cap_cents || pilot_cap_cents > campaign_cap_cents {
        return Err("spend ledger violated pilot or campaign cost ceiling");
    }
    let total_sg = 50_usize;
    let local_staged_passed = 2_usize;
    let not_run = total_sg - local_staged_passed;
    Ok((total_sg, local_staged_passed, not_run, actual_paid_spend_cents))
}

#[test]
fn plan_7d_day_7_witness_and_controls() {
    let (total, passed, not_run, spend) =
        verify_day_7_audit(false, false, 0, 20, 2000).expect("valid Day 7 audit passes");
    assert_eq!((total, passed, not_run, spend), (50, 2, 48, 0));

    assert!(verify_day_7_audit(true, false, 0, 20, 2000).is_err());
    assert!(verify_day_7_audit(false, true, 0, 20, 2000).is_err());
    assert!(verify_day_7_audit(false, false, 25, 20, 2000).is_err());
}
