
use crate::open_set::{OpenSet, PosetTopology};
use num_rational::Ratio;
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct StructureSheaf {
    pub topology: PosetTopology,
}

impl StructureSheaf {
    pub fn new(topology: PosetTopology) -> Self {
        Self { topology }
    }

    pub fn sections(&self, u: &OpenSet) -> Vec<Vec<Ratio<i64>>> {
        let k = u.elements.len();
        if k == 0 {
            return vec![vec![]];
        }

        let zero = vec![Ratio::from_integer(0); k];
        let mut basis = vec![zero];
        for i in 0..k {
            let mut vec = vec![Ratio::from_integer(0); k];
            vec[i] = Ratio::from_integer(1);
            basis.push(vec);
        }
        basis
    }

    pub fn section_rank(&self, u: &OpenSet) -> usize {
        u.elements.len()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_structure_sheaf_basis() {
        let top = PosetTopology::discrete(vec!["0", "1", "01"]);
        let str_sheaf = StructureSheaf::new(top);
        let u = OpenSet::new(vec!["0", "1"]);
        let basis = str_sheaf.sections(&u);
        assert_eq!(basis.len(), 3);
    }
}
