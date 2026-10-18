//! Lexicographic words over 0..base, including the unique empty word.
//! Cardinality is exact and checked before enumeration. Width has its own
//! explicit resource ceiling; cardinality one does not admit a huge buffer.
use crate::enumeration::CombinatoricsError;
use num_bigint::BigUint;
use num_traits::ToPrimitive;

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
        let count = BigUint::from(base).pow(u32::try_from(width).expect("width ceiling fits u32"));
        if count > BigUint::from(max_words) {
            return Err(CombinatoricsError::BudgetExceeded {
                what: "Cartesian words",
                requested: count,
                limit: max_words,
            });
        }
        let cardinality = count.to_usize().expect("count below usize limit");
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
        let out = self.current.clone()?;
        let mut next = out.clone();
        let mut advanced = false;
        for slot in next.iter_mut().rev() {
            *slot += 1;
            if *slot < self.base {
                advanced = true;
                break;
            }
            *slot = 0;
        }
        self.current = if advanced { Some(next) } else { None };
        Some(out)
    }
}
