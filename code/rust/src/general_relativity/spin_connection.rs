
use num_rational::Ratio;
use num_traits::Zero;
use serde::{Deserialize, Serialize};
use std::collections::BTreeMap;

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum SpinConnectionError {
    IndexOutOfBounds,
    TorsionDetected,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct DiscreteSpinConnection {
    pub dim: usize,
    pub omega: BTreeMap<(usize, usize, usize), Ratio<i64>>,
}

impl DiscreteSpinConnection {
    pub fn new(dim: usize) -> Self {
        Self {
            dim,
            omega: BTreeMap::new(),
        }
    }

    pub fn set_component(&mut self, edge: usize, a: usize, b: usize, val: Ratio<i64>) {
        self.omega.insert((edge, a, b), val);
        self.omega.insert((edge, b, a), -val);
    }

    pub fn get_component(&self, edge: usize, a: usize, b: usize) -> Ratio<i64> {
        self.omega.get(&(edge, a, b)).copied().unwrap_or_else(Ratio::zero)
    }

    pub fn verify_antisymmetry(&self) -> bool {
        for (&(edge, a, b), &val) in &self.omega {
            let rev = self.get_component(edge, b, a);
            if val + rev != Ratio::zero() {
                return false;
            }
        }
        true
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn spin_connection_antisymmetry() {
        let mut sc = DiscreteSpinConnection::new(4);
        sc.set_component(0, 0, 1, Ratio::new(3, 4));
        assert!(sc.verify_antisymmetry());
        assert_eq!(sc.get_component(0, 1, 0), Ratio::new(-3, 4));
    }
}
