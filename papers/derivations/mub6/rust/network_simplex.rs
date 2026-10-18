
use num_rational::Ratio;
use num_traits::{One, Zero};
use serde::{Deserialize, Serialize};
use std::collections::BTreeMap;

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum SimplexError {
    InfeasibleSupplyDemand,
    CycleDetected,
    UnboundedFlow,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct NetworkEdge {
    pub src: usize,
    pub tgt: usize,
    pub capacity: Ratio<i64>,
    pub cost: Ratio<i64>,
    pub flow: Ratio<i64>,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct ExactNetworkSimplex {
    pub num_nodes: usize,
    pub edges: Vec<NetworkEdge>,
    pub node_supplies: Vec<Ratio<i64>>,
}

impl ExactNetworkSimplex {
    pub fn new(num_nodes: usize, node_supplies: Vec<Ratio<i64>>) -> Result<Self, SimplexError> {
        let sum_supply: Ratio<i64> = node_supplies.iter().copied().sum();
        if !sum_supply.is_zero() {
            return Err(SimplexError::InfeasibleSupplyDemand);
        }
        Ok(Self {
            num_nodes,
            edges: Vec::new(),
            node_supplies,
        })
    }

    pub fn add_edge(&mut self, src: usize, tgt: usize, capacity: Ratio<i64>, cost: Ratio<i64>) {
        self.edges.push(NetworkEdge {
            src,
            tgt,
            capacity,
            cost,
            flow: Ratio::zero(),
        });
    }

    pub fn total_cost(&self) -> Ratio<i64> {
        self.edges.iter().map(|e| e.flow * e.cost).sum()
    }

    pub fn verify_conservation(&self) -> bool {
        for node in 0..self.num_nodes {
            let mut balance = Ratio::zero();
            for e in &self.edges {
                if e.src == node {
                    balance += e.flow;
                }
                if e.tgt == node {
                    balance -= e.flow;
                }
            }
            if balance != self.node_supplies[node] {
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
    fn test_balanced_network_simplex() {
        let supplies = vec![Ratio::from_integer(10), Ratio::from_integer(-10)];
        let mut net = ExactNetworkSimplex::new(2, supplies).unwrap();
        net.add_edge(0, 1, Ratio::from_integer(15), Ratio::from_integer(2));
        net.edges[0].flow = Ratio::from_integer(10);
        assert!(net.verify_conservation());
        assert_eq!(net.total_cost(), Ratio::from_integer(20));
    }
}
