pub fn verify_day_4_correspondence(
    restore_cost_quarter_units: i64,
    drop_initial_projection: bool,
    include_restore: bool,
    task_target_d: i64,
    cached_table_d: i64,
    parent_digest_matches: bool,
    repeat_child_without_reuse: bool,
    lane_d_bounds: (u32, u32, u32),
) -> Result<(i64, i64, i64, u32), &'static str> {
    if restore_cost_quarter_units <= 0 {
        return Err("restore_cost must be positive");
    }
    if drop_initial_projection {
        return Err("dropping first coordinate collapses original classes after flip_read");
    }
    if !include_restore {
        return Err("omitting restore leaves disturbed states unrecovered");
    }
    if !parent_digest_matches {
        return Err("stale parent digest mismatch refused");
    }
    if task_target_d != cached_table_d {
        return Err("fixed R_1 table reused on changed task target d");
    }
    if lane_d_bounds != (3, 4, 2) {
        return Err("undeclared Lane D bound extension refused");
    }

    // In quarter-units: flip_read = 2, read_A/read_B = 12, restore = restore_cost_quarter_units.
    let disturbance_repair_quarters = 2 + 12 + restore_cost_quarter_units;
    let nondisturbing_quarters = 16; // 4 = 16/4
    let overall_opt_quarters = disturbance_repair_quarters.min(nondisturbing_quarters);

    // Lane C cost in half-units: 8 + 6 + 2 + 9 + 9 = 34 (which is 17). With repeat child (+9 half-units): 43 > 36 (which is 18).
    let lane_c_half_units = 34 + if repeat_child_without_reuse { 9 } else { 0 };
    if lane_c_half_units > 36 {
        return Err("Lane C trace cost exceeds budget cap 18");
    }

    let lane_d_classes = 1_u32 + 15 + 495 + 29260;
    Ok((
        disturbance_repair_quarters,
        overall_opt_quarters,
        lane_c_half_units,
        lane_d_classes,
    ))
}

#[test]
fn plan_7d_day_4_witness_and_controls() {
    let (dist_q, opt_q, c_half, d_classes) =
        verify_day_4_correspondence(1, false, true, 1, 1, true, false, (3, 4, 2))
            .expect("valid Day 4 correspondence passes");
    assert_eq!(dist_q, 15);
    assert_eq!(opt_q, 15);
    assert_eq!(c_half, 34);
    assert_eq!(d_classes, 29771);

    let (_dist_shifted, opt_shifted, _, _) =
        verify_day_4_correspondence(16, false, true, 1, 1, true, false, (3, 4, 2))
            .expect("shifted restore cost computes new optimum");
    assert_eq!(opt_shifted, 16);

    assert!(verify_day_4_correspondence(1, true, true, 1, 1, true, false, (3, 4, 2)).is_err());
    assert!(verify_day_4_correspondence(1, false, false, 1, 1, true, false, (3, 4, 2)).is_err());
    assert!(verify_day_4_correspondence(1, false, true, 2, 1, true, false, (3, 4, 2)).is_err());
    assert!(verify_day_4_correspondence(1, false, true, 1, 1, false, false, (3, 4, 2)).is_err());
    assert!(verify_day_4_correspondence(1, false, true, 1, 1, true, true, (3, 4, 2)).is_err());
    assert!(verify_day_4_correspondence(1, false, true, 1, 1, true, false, (4, 4, 2)).is_err());
}
