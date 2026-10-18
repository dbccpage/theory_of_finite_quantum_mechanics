
pub fn optimal_subset_cost_halves(
    costs_in_halves: &[u64],
    pair_masks: &[u8],
    required_mask: u8,
) -> Option<(u8, u64)> {
    let n = costs_in_halves.len();
    let mut best: Option<(u8, u64)> = None;
    for mask in 0u8..(1u8 << n) {
        let mut covered = 0u8;
        let mut cost = 0u64;
        for i in 0..n {
            if (mask & (1u8 << i)) != 0 {
                covered |= pair_masks[i];
                cost += costs_in_halves[i];
            }
        }
        if (covered & required_mask) == required_mask {
            if best.map_or(true, |(_, c)| cost < c) {
                best = Some((mask, cost));
            }
        }
    }
    best
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_p4_planner_beats_monolithic() {
        let costs = [10u64, 3, 4];
        let masks = [0b111u8, 0b101, 0b110];
        let (mask, cost) = optimal_subset_cost_halves(&costs, &masks, 0b111).unwrap();
        assert_eq!(mask, 0b110);
        assert_eq!(cost, 7);
    }
}
