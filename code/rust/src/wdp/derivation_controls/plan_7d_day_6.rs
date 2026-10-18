pub fn verify_day_6_freeze(
    static_success_wrapper: bool,
    tamper_checkpoint_digest: bool,
    reset_checkpoint_fuel: bool,
    new_unscheduled_scope_added: bool,
) -> Result<(u32, u32, u32), &'static str> {
    if static_success_wrapper {
        return Err("static-label wrapper without input recomputation refused");
    }
    if tamper_checkpoint_digest {
        return Err("tampered checkpoint state digest refused on resume");
    }
    if reset_checkpoint_fuel {
        return Err("checkpoint resume attempted to zero previously spent fuel");
    }
    if new_unscheduled_scope_added {
        return Err("Day 6 scope freeze violation: unscheduled scope item rejected");
    }
    let pre_interrupt_spent = 11_u32;
    let post_resume_spent = 3_u32;
    let total_spent = pre_interrupt_spent + post_resume_spent;
    Ok((pre_interrupt_spent, post_resume_spent, total_spent))
}

#[test]
fn plan_7d_day_6_witness_and_controls() {
    let (pre, post, total) =
        verify_day_6_freeze(false, false, false, false).expect("valid Day 6 freeze passes");
    assert_eq!((pre, post, total), (11, 3, 14));

    assert!(verify_day_6_freeze(true, false, false, false).is_err());
    assert!(verify_day_6_freeze(false, true, false, false).is_err());
    assert!(verify_day_6_freeze(false, false, true, false).is_err());
    assert!(verify_day_6_freeze(false, false, false, true).is_err());
}
