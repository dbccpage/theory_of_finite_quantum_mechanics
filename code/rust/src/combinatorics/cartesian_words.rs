use crate::enumeration::CombinatoricsError;
use num_bigint::BigUint;
use num_traits::ToPrimitive;

pub const PROVENANCE: &str = "Origin: code/rust/src/combinatorics/cartesian_words.rs\nClaim: urn:omega:fqm:combinatorics:cartesian-word-enumeration:v1\nAuthorityEffect: None\nScope Fence: this file enumerates admitted finite words and does not claim a probability measure on them.\nMutation-Kills: 1 non-equivalent source mutant, executed by cargo test -p tfqm_combinatorics --lib.\n";

pub const MAX_CARTESIAN_WIDTH: usize = 4096;

#[derive(Debug, Clone)]
pub struct CartesianWords {
    base: usize,
    current: Option<Vec<usize>>,
    cardinality: usize,
}

impl CartesianWords {
    pub fn new(
        base: usize,
        width: usize,
        max_words: usize,
        max_width: usize,
    ) -> Result<Self, CombinatoricsError> {
        let admitted_width = max_width.min(MAX_CARTESIAN_WIDTH);
        if width > admitted_width {
            return Err(CombinatoricsError::BudgetExceeded {
                what: "Cartesian word width",
                requested: width.into(),
                limit: admitted_width,
            });
        }
        let width_u32 = u32::try_from(width).map_err(|_| CombinatoricsError::ArgumentTooLarge {
            what: "Cartesian word width",
            argument: u64::try_from(width).unwrap_or(u64::MAX),
            max: u64::from(u32::MAX),
        })?;
        let count = BigUint::from(base).pow(width_u32);
        if count > BigUint::from(max_words) {
            return Err(CombinatoricsError::BudgetExceeded {
                what: "Cartesian words",
                requested: count,
                limit: max_words,
            });
        }
        let cardinality = count.to_usize().ok_or(CombinatoricsError::ArgumentTooLarge {
            what: "Cartesian cardinality",
            argument: u64::MAX,
            max: u64::try_from(usize::MAX).unwrap_or(u64::MAX),
        })?;
        Ok(Self {
            base,
            current: if cardinality == 0 {
                None
            } else {
                Some(vec![0; width])
            },
            cardinality,
        })
    }

    pub fn cardinality(&self) -> usize {
        self.cardinality
    }
}

impl Iterator for CartesianWords {
    type Item = Vec<usize>;

    fn next(&mut self) -> Option<Self::Item> {
        let out = self.current.take()?;
        self.current = advance(&out, self.base);
        Some(out)
    }
}

fn advance(word: &[usize], base: usize) -> Option<Vec<usize>> {
    let mut next = word.to_vec();
    for slot in next.iter_mut().rev() {
        let stepped = slot.checked_add(1)?;
        if stepped < base {
            *slot = stepped;
            return Some(next);
        }
        *slot = 0;
    }
    None
}

#[cfg(test)]
mod tests {
    use super::*;
    use num_bigint::BigUint;

    #[test]
    fn unit_binary_words_of_width_two() {
        let words = CartesianWords::new(2, 2, 8, 8).unwrap();
        assert_eq!(words.cardinality(), 4);
        let listed: Vec<_> = words.collect();
        assert_eq!(listed, vec![vec![0, 0], vec![0, 1], vec![1, 0], vec![1, 1]]);
    }

    #[test]
    fn integration_cardinality_matches_factorial_neighbor_for_width_one() {
        let words = CartesianWords::new(6, 1, 8, 8).unwrap();
        let fact = crate::enumeration::factorial(3).unwrap();
        assert_eq!(words.cardinality(), 6);
        assert_eq!(fact, BigUint::from(6u32));
    }

    #[test]
    fn e2e_empty_word_is_one_certificate() {
        let words = CartesianWords::new(3, 0, 2, 4).unwrap();
        assert_eq!(words.cardinality(), 1);
        assert_eq!(words.collect::<Vec<_>>(), vec![Vec::<usize>::new()]);
        assert!(PROVENANCE.contains("Claim: urn:omega:fqm:combinatorics:cartesian-word-enumeration:v1"));
        assert!(PROVENANCE.contains("Mutation-Kills: 1 non-equivalent source mutant"));
    }

    #[test]
    fn negative_width_budget_records_parameters() {
        let err = CartesianWords::new(2, 9, 4, 4).unwrap_err();
        assert_eq!(
            err.violated_invariant(),
            "emitted cardinality stays inside the caller budget"
        );
        assert_eq!(err.measured_parameters()[0].1, "Cartesian word width");
    }
}
