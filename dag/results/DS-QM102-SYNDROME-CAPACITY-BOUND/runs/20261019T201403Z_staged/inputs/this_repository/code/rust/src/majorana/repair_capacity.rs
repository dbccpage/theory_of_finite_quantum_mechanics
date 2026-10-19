
#![forbid(unsafe_code)]

pub fn repair_capacity_from_distance(d: u32) -> Result<u32, String> {
    if d == 0 {
        return Err(
            "repair_capacity: homology/code distance d must be positive (undeclared d refuses)"
                .into(),
        );
    }
    Ok(d.saturating_sub(1) / 2)
}

pub fn assert_repair_capacity_invariant(d: u32) -> Result<u32, String> {
    let t = repair_capacity_from_distance(d)?;
    let expected = (d - 1) / 2;
    if t != expected {
        return Err(format!(
            "repair_capacity: t={} != floor((d-1)/2)={} for d={}",
            t, expected, d
        ));
    }
    if 2 * t >= d {
        return Err(format!(
            "repair_capacity: invariant broken: t={} is not < d/2 for d={}",
            t, d
        ));
    }
    Ok(t)
}

pub fn min_weight_nontrivial(cycles: &[Vec<u8>]) -> Option<u32> {
    cycles
        .iter()
        .filter(|c| c.iter().any(|&b| b % 2 == 1))
        .map(|c| c.iter().map(|&b| (b % 2) as u32).sum::<u32>())
        .min()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn repair_capacity_matches_a_hand_table() {
        let table = [
            (1u32, 0u32),
            (2, 0),
            (3, 1),
            (4, 1),
            (5, 2),
            (8, 3),
            (9, 4),
            (15, 7),
            (u32::MAX, 2_147_483_647),
        ];
        for (d, t) in table {
            assert_eq!(repair_capacity_from_distance(d).unwrap(), t, "d={d}");
            assert_eq!(assert_repair_capacity_invariant(d).unwrap(), t, "d={d}");
        }
    }

    #[test]
    fn d_zero_refuses() {
        let err = repair_capacity_from_distance(0).unwrap_err();
        assert!(err.contains("positive"), "{err}");
        let err = assert_repair_capacity_invariant(0).unwrap_err();
        assert!(err.contains("positive"), "{err}");
    }

    #[test]
    fn min_weight_ignores_evens_empty_and_the_first_odd_vector() {
        assert_eq!(min_weight_nontrivial(&[]), None);
        assert_eq!(min_weight_nontrivial(&[vec![0, 2, 4], vec![0, 0, 0]]), None);
        assert_eq!(
            min_weight_nontrivial(&[vec![1, 1, 1], vec![0, 2, 4], vec![3]]),
            Some(1),
            "odd weight of [3] is 1 and is smaller than the leading weight-3 vector"
        );
        assert_eq!(
            min_weight_nontrivial(&[vec![1, 1, 1, 1], vec![5, 0, 7]]),
            Some(2)
        );
    }
}
