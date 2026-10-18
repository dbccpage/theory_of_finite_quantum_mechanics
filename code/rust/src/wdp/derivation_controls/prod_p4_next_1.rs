
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct PlanVerdict {
    pub feasible: bool,
    pub suite_mask: Option<usize>,
    pub cost_half_units: Option<u64>,
    pub unresolved_pair_indices: Vec<usize>,
}

pub fn plan_cheapest_suite(
    prices_half_units: &[u64],
    separates: &[Vec<bool>],
    num_pairs: usize,
) -> PlanVerdict {
    let m = prices_half_units.len();
    let mut best: Option<(u64, usize)> = None;
    for mask in 0..(1usize << m) {
        let covers_all = (0..num_pairs).all(|p| {
            (0..m).any(|i| ((mask >> i) & 1 == 1) && separates[i][p])
        });
        if covers_all {
            let cost: u64 = (0..m)
                .filter(|&i| (mask >> i) & 1 == 1)
                .map(|i| prices_half_units[i])
                .sum();
            let cand = (cost, mask);
            if best.map_or(true, |b| cand < b) {
                best = Some(cand);
            }
        }
    }
    if let Some((cost, mask)) = best {
        PlanVerdict {
            feasible: true,
            suite_mask: Some(mask),
            cost_half_units: Some(cost),
            unresolved_pair_indices: vec![],
        }
    } else {
        let unresolved = (0..num_pairs)
            .filter(|&p| (0..m).all(|i| !separates[i][p]))
            .collect();
        PlanVerdict {
            feasible: false,
            suite_mask: None,
            cost_half_units: None,
            unresolved_pair_indices: unresolved,
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn cheapest_sufficient_suite_and_infeasible_witness() {
        let prices = [10, 3, 4];
        let separates = vec![
            vec![true, true, true],
            vec![true, false, true],
            vec![false, true, true],
        ];
        let v = plan_cheapest_suite(&prices, &separates, 3);
        assert!(v.feasible);
        assert_eq!(v.suite_mask, Some(0b110));
        assert_eq!(v.cost_half_units, Some(7));

        let infeasible_sep = vec![vec![true, false, true]];
        let inv = plan_cheapest_suite(&[2], &infeasible_sep, 3);
        assert!(!inv.feasible);
        assert_eq!(inv.unresolved_pair_indices, vec![1]);
    }
}
