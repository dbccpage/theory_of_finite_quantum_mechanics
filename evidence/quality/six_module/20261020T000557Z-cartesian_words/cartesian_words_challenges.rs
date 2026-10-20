#[cfg(test)]
mod independent_word_checks {
    use super::*;

    fn from_rank(mut rank: usize, base: usize, width: usize) -> Vec<usize> {
        let mut row = vec![0; width];
        for digit in row.iter_mut().rev() {
            *digit = rank % base;
            rank /= base;
        }
        row
    }

    #[test]
    fn positional_oracle_checks_all_small_words_and_exact_budgets() {
        for base in 0usize..=5 {
            for width in 0usize..=6 {
                let count = base.pow(width as u32);
                let expected = (0..count).map(|rank| from_rank(rank, base, width)).collect::<Vec<_>>();
                let mut actual = CartesianWords::new(base, width, count, 6).unwrap();
                assert_eq!(actual.cardinality(), count);
                for row in expected { assert_eq!(actual.next(), Some(row)); }
                assert_eq!(actual.next(), None);
                assert_eq!(actual.next(), None);
                if count > 0 {
                    assert_eq!(CartesianWords::new(base, width, count - 1, 6).unwrap_err(),
                        CombinatoricsError::BudgetExceeded { what: "Cartesian words", requested: BigUint::from(count), limit: count-1 });
                }
            }
        }
    }

    #[test]
    fn width_priority_zero_alphabets_and_word_ownership() {
        let limit = MAX_CARTESIAN_WIDTH;
        let mut widest = CartesianWords::new(1, limit, 1, usize::MAX).unwrap();
        assert_eq!(widest.next(), Some(vec![0; limit]));
        assert_eq!(widest.next(), None);
        for width in [limit+1, usize::MAX] {
            assert_eq!(CartesianWords::new(usize::MAX, width, 0, usize::MAX).unwrap_err(),
                CombinatoricsError::BudgetExceeded { what: "Cartesian word width", requested: BigUint::from(width), limit });
        }
        assert_eq!(CartesianWords::new(2, 2, 0, 1).unwrap_err(),
            CombinatoricsError::BudgetExceeded { what: "Cartesian word width", requested: BigUint::from(2usize), limit: 1 });
        assert_eq!(CartesianWords::new(0, 0, 0, 0).unwrap_err(),
            CombinatoricsError::BudgetExceeded { what: "Cartesian words", requested: BigUint::from(1usize), limit: 0 });
        let mut huge = CartesianWords::new(usize::MAX, 1, usize::MAX, 1).unwrap();
        assert_eq!(huge.cardinality(), usize::MAX);
        assert_eq!(huge.next(), Some(vec![0]));
        assert_eq!(huge.next(), Some(vec![1]));
        let requested = BigUint::from(usize::MAX) * BigUint::from(usize::MAX);
        assert_eq!(CartesianWords::new(usize::MAX, 2, usize::MAX, 2).unwrap_err(),
            CombinatoricsError::BudgetExceeded { what: "Cartesian words", requested, limit: usize::MAX });
        let mut words = CartesianWords::new(2, 2, 4, 2).unwrap();
        let mut output = words.next().unwrap();
        let mut independent = words.clone();
        output.fill(usize::MAX);
        assert_eq!(words.next(), Some(vec![0,1]));
        assert_eq!(words.next(), Some(vec![1,0]));
        assert_eq!(independent.next(), Some(vec![0,1]));
        assert_eq!(independent.cardinality(), 4);
        assert_eq!(words.cardinality(), 4);
    }
}
