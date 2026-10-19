#[cfg(test)]
mod independent_resource_checks {
    use super::*;

    fn reference_compositions(total: usize, parts: usize) -> Vec<Vec<usize>> {
        if parts == 0 {
            return if total == 0 { vec![vec![]] } else { vec![] };
        }
        let mut result = Vec::new();
        for first in 0..=total {
            for tail in reference_compositions(total - first, parts - 1) {
                let mut row = vec![first];
                row.extend(tail);
                result.push(row);
            }
        }
        result
    }

    fn product_words(base: usize, width: usize) -> Vec<Vec<usize>> {
        if width == 0 {
            return vec![vec![]];
        }
        let mut result = Vec::new();
        for prefix in product_words(base, width - 1) {
            for digit in 0..base {
                let mut row = prefix.clone();
                row.push(digit);
                result.push(row);
            }
        }
        result
    }

    #[test]
    fn small_exact_counts_and_enumerators() {
        let mut expected_factorial = 1u128;
        for n in 0..=20 {
            if n > 0 { expected_factorial *= n as u128; }
            assert_eq!(factorial(n).unwrap(), BigUint::from(expected_factorial));
        }
        let mut pascal = vec![1u128];
        for n in 0..=25usize {
            for k in 0..=n + 1 {
                let expected = pascal.get(k).copied().unwrap_or(0);
                assert_eq!(binomial(n as u64, k as u64).unwrap(), BigUint::from(expected));
            }
            let mut next = vec![1u128; pascal.len() + 1];
            for k in 1..pascal.len() { next[k] = pascal[k - 1] + pascal[k]; }
            pascal = next;
        }
        for n in 0..=10 {
            for k in 0..=n + 2 {
                let mut expected = (0..(1usize << n)).filter(|mask| mask.count_ones() as usize == k)
                    .map(|mask| (0..n).filter(|i| mask & (1 << i) != 0).collect::<Vec<_>>())
                    .collect::<Vec<_>>();
                expected.sort();
                assert_eq!(combinations(n, k, 1024).unwrap(), expected);
            }
        }
        for n in 0..=5 {
            let expected = product_words(n, n).into_iter().filter(|row| {
                let mut distinct = row.clone(); distinct.sort(); distinct.dedup(); distinct.len() == n
            }).collect::<Vec<_>>();
            assert_eq!(permutations(n, 120).unwrap(), expected);
        }
        for width in 0..=4 {
            let words = product_words(3, width);
            for word in &words {
                let mut multiset = word.clone(); multiset.sort();
                let expected = words.iter().find(|candidate| {
                    let mut sorted = (*candidate).clone(); sorted.sort();
                    sorted == multiset && *candidate > word
                });
                let mut actual = word.clone();
                assert_eq!(next_permutation(&mut actual), expected.is_some());
                assert_eq!(&actual, expected.unwrap_or(word));
            }
        }
        for total in 0..=8 {
            for parts in 0..=5 {
                let expected = reference_compositions(total, parts);
                assert_eq!(weak_compositions(total, parts, expected.len()).unwrap(), expected);
                if !expected.is_empty() {
                    assert!(matches!(weak_compositions(total, parts, expected.len()-1),
                        Err(CombinatoricsError::BudgetExceeded { what: "weak compositions", .. })));
                }
            }
        }
    }

    #[test]
    fn admission_precedes_allocation_and_keeps_exact_failure_priority() {
        for parts in [MAX_ENUMERATION_WIDTH + 1, usize::MAX] {
            assert_eq!(weak_compositions(0, parts, 1), Err(CombinatoricsError::ArgumentTooLarge {
                what: "weak composition parts", argument: parts as u64, max: MAX_ENUMERATION_WIDTH as u64
            }));
        }
        let mut wide = Combinations::new(MAX_ENUMERATION_WIDTH, MAX_ENUMERATION_WIDTH, 1).unwrap();
        assert_eq!(wide.next(), Some((0..MAX_ENUMERATION_WIDTH).collect()));
        assert_eq!(wide.next(), None);
        assert_eq!(wide.next(), None);
        assert_eq!(Combinations::new(usize::MAX, usize::MAX, 1).unwrap_err(),
            CombinatoricsError::ArgumentTooLarge { what: "combination width", argument: u64::MAX,
                max: MAX_ENUMERATION_WIDTH as u64 });
        assert!(Combinations::new(0, usize::MAX, 0).unwrap().next().is_none());
        assert_eq!(weak_compositions(usize::MAX, 1, 1).unwrap(), vec![vec![usize::MAX]]);
        assert_eq!(weak_compositions(usize::MAX, 0, 0).unwrap(), Vec::<Vec<usize>>::new());
        assert_eq!(weak_compositions(0, MAX_ENUMERATION_WIDTH, 1).unwrap(), vec![vec![0; MAX_ENUMERATION_WIDTH]]);
        assert!(matches!(weak_compositions(usize::MAX, 2, 1), Err(CombinatoricsError::ArgumentTooLarge { what: "weak_compositions", .. })));
        let rows = weak_compositions(1, 1024, 1024).unwrap();
        assert_eq!(rows.len(), 1024);
        assert!(rows.iter().all(|row| row.len() == 1024 && row.iter().sum::<usize>() == 1));
        assert!(matches!(weak_compositions(1, 1025, 1024), Err(CombinatoricsError::BudgetExceeded { what: "weak compositions", .. })));
        assert_eq!(weak_compositions(1, 1025, 1025), Err(CombinatoricsError::BudgetExceeded {
            what: "weak composition cells", requested: BigUint::from(1025usize * 1025), limit: MAX_COMPOSITION_CELLS
        }));
    }

    #[test]
    fn malformed_successors_diagnostics_and_conversion_are_literal() {
        for mut invalid in [vec![0,0], vec![1,0], vec![0,3], vec![usize::MAX]] {
            let original = invalid.clone();
            assert!(!next_combination(&mut invalid, 3));
            assert_eq!(invalid, original);
        }
        assert!(!next_combination(&mut [0,1,2], 2));
        assert!(!next_combination(&mut [], 4));
        let huge = BigUint::from(u64::MAX) + BigUint::one();
        assert_eq!(to_u64(&BigUint::from(u64::MAX)), Some(u64::MAX));
        assert_eq!(to_u64(&huge), None);
        let err = factorial(MAX_FACTORIAL_ARGUMENT + 1).unwrap_err();
        assert_eq!(err.measured_parameters(), vec![("what", "factorial".into()),
            ("argument", (MAX_FACTORIAL_ARGUMENT+1).to_string()), ("max", MAX_FACTORIAL_ARGUMENT.to_string())]);
        assert_eq!(err.violated_invariant(), "argument stays inside the admitted exact bound");
        let err = permutations(3, 5).unwrap_err();
        assert_eq!(err.measured_parameters(), vec![("what", "permutations".into()),
            ("requested", "6".into()), ("limit", "5".into())]);
        assert_eq!(err.violated_invariant(), "emitted cardinality stays inside the caller budget");
    }
}
