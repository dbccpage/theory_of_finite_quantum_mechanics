#[cfg(test)]
mod independent_partition_checks {
    use super::*;
    use num_bigint::BigInt;
    use std::collections::{BTreeMap, BTreeSet};

    // Euler's generalized-pentagonal identity, not the production coin-change DP.
    fn pentagonal_counts(n: usize) -> Vec<BigUint> {
        let mut values = vec![BigInt::from(1u8)];
        for total in 1..=n {
            let mut value = BigInt::from(0u8);
            for k in 1usize.. {
                let first = k * (3*k-1)/2;
                if first > total { break; }
                let second = k * (3*k+1)/2;
                let mut contribution = values[total-first].clone();
                if second <= total { contribution += &values[total-second]; }
                if k % 2 == 1 { value += contribution; } else { value -= contribution; }
            }
            values.push(value);
        }
        values.into_iter().map(|value| value.to_biguint().unwrap()).collect()
    }

    // Cut masks enumerate positive compositions; sorting/dedup gives partitions.
    fn cut_oracle(n: usize) -> Vec<Vec<usize>> {
        if n == 0 { return vec![vec![]]; }
        let mut result = BTreeSet::new();
        for mask in 0..(1usize << (n-1)) {
            let mut row = Vec::new();
            let mut length = 1;
            for gap in 0..n-1 {
                if mask & (1 << gap) != 0 { row.push(length); length = 1; }
                else { length += 1; }
            }
            row.push(length);
            row.sort_by(|a,b| b.cmp(a));
            result.insert(row);
        }
        result.into_iter().rev().collect()
    }

    fn histogram(prefix: &mut Vec<usize>, rest: Vec<usize>, counts: &mut BTreeMap<Vec<usize>,u64>) {
        if !rest.is_empty() {
            for i in 0..rest.len() {
                let mut remaining = rest.clone();
                prefix.push(remaining.remove(i));
                histogram(prefix, remaining, counts);
                prefix.pop();
            }
            return;
        }
        let mut seen = vec![false; prefix.len()];
        let mut lengths = Vec::new();
        for start in 0..prefix.len() {
            if seen[start] { continue; }
            let mut at = start;
            let mut length = 0;
            while !seen[at] { seen[at] = true; length += 1; at = prefix[at]; }
            lengths.push(length);
        }
        lengths.sort_by(|a,b| b.cmp(a));
        *counts.entry(lengths).or_default() += 1;
    }

    #[test]
    fn counts_match_independent_identity_and_lists_match_cut_masks() {
        let counts = pentagonal_counts(MAX_PARTITION_ARGUMENT);
        for (n, count) in counts.iter().enumerate() { assert_eq!(&partition_count(n).unwrap(), count); }
        for n in 0..=14 {
            let expected = cut_oracle(n);
            assert_eq!(partitions(n, expected.len()).unwrap(), expected);
            if !expected.is_empty() {
                assert_eq!(partitions(n, expected.len()-1).unwrap_err(), CombinatoricsError::BudgetExceeded {
                    what: "partitions", requested: BigUint::from(expected.len()), limit: expected.len()-1
                });
            }
        }
    }

    #[test]
    fn symmetric_group_cycle_histograms_give_exact_class_sizes() {
        for n in 0..=8 {
            let mut counts = BTreeMap::new();
            histogram(&mut Vec::new(), (0..n).collect(), &mut counts);
            let expected_total = (1..=n as u64).product::<u64>();
            assert_eq!(counts.values().sum::<u64>(), expected_total);
            for (parts, count) in counts {
                assert_eq!(conjugacy_class_size(&parts).unwrap(), BigUint::from(count));
                let mut permuted = parts.clone(); permuted.reverse();
                assert_eq!(conjugacy_class_size(&permuted).unwrap(), BigUint::from(count));
            }
        }
    }

    #[test]
    fn resource_refusal_order_and_bounded_stack_preserve_semantics() {
        for n in [MAX_PARTITION_ARGUMENT+1, usize::MAX] {
            assert_eq!(partition_count(n).unwrap_err(), CombinatoricsError::ArgumentTooLarge {
                what: "partitions", argument: n as u64, max: MAX_PARTITION_ARGUMENT as u64
            });
        }
        let rows = partitions(38, 26015).unwrap();
        assert_eq!(rows.len(), 26015);
        assert_eq!(rows.first(), Some(&vec![38]));
        assert_eq!(rows.last(), Some(&vec![1;38]));
        assert!(rows.iter().all(|r| r.iter().sum::<usize>()==38 && r.iter().all(|&x|x>0) && r.windows(2).all(|p|p[0]>=p[1])));
        assert_eq!(rows.iter().collect::<BTreeSet<_>>().len(), rows.len());
        assert_eq!(partitions(39, 31185).unwrap_err(), CombinatoricsError::BudgetExceeded {
            what: "partition cell upper bound", requested: BigUint::from(39usize*31185), limit: MAX_PARTITION_CELLS
        });
        assert!(matches!(partitions(39, 0), Err(CombinatoricsError::BudgetExceeded { what: "partitions", .. })));
        assert!(matches!(conjugacy_class_size(&[usize::MAX,1,0]), Err(CombinatoricsError::ArgumentTooLarge { what: "cycle length (must be positive)", .. })));
        assert!(matches!(conjugacy_class_size(&[usize::MAX,1]), Err(CombinatoricsError::ArgumentTooLarge { what: "sum of cycle lengths", .. })));
        let too_many = vec![1; crate::enumeration::MAX_FACTORIAL_ARGUMENT+1];
        assert!(matches!(conjugacy_class_size(&too_many), Err(CombinatoricsError::ArgumentTooLarge { what: "factorial", .. })));
        let n = crate::enumeration::MAX_FACTORIAL_ARGUMENT;
        assert_eq!(conjugacy_class_size(&[n]).unwrap(), crate::enumeration::factorial(n-1).unwrap());
    }
}
