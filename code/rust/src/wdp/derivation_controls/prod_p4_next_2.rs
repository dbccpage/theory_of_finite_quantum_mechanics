//! Companion Rust witness for PROD-P4-NEXT-2 (Map CompletionTarget raw/quotient/both onto distinct_image targets).

pub fn sharp_distinct_image_minima(dim_k: usize, dim_rk: usize, dim_kb: usize, dim_rkb: usize) -> (usize, usize, usize, usize) {
    let raw_min = dim_rk;
    let quo_min = dim_k - dim_kb;
    let joint_min = quo_min + dim_rkb;
    let separate_sum = raw_min + quo_min;
    (raw_min, quo_min, joint_min, separate_sum)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn neither_inclusion_exhibits_strict_joint_subadditivity() {
        let (raw_min, quo_min, joint_min, separate_sum) = sharp_distinct_image_minima(3, 2, 2, 1);
        assert_eq!((raw_min, quo_min, joint_min, separate_sum), (2, 1, 2, 3));
        assert!(joint_min < separate_sum);
    }
}
