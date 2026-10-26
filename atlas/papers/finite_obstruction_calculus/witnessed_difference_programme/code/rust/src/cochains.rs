// Executable finite evidence; AuthorityEffect: None.
use crate::error::WdpError;
use num_rational::BigRational;
use num_traits::Zero;
use serde::{Deserialize, Serialize};
use std::collections::BTreeMap;

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct FiniteComplex {
    pub vertices: Vec<String>,
    pub edges: Vec<(String, String)>,
}

impl FiniteComplex {
    pub fn new(vertices: Vec<String>, edges: Vec<(String, String)>) -> Result<Self, WdpError> {
        let vset: std::collections::BTreeSet<_> = vertices.iter().cloned().collect();
        if vset.len() != vertices.len() {
            return Err(WdpError::InvalidInput {
                detail: "Duplicate vertices".into(),
            });
        }
        let eset: std::collections::BTreeSet<_> = edges.iter().collect();
        if eset.len() != edges.len() {
            return Err(WdpError::InvalidInput { detail: "Duplicate edges require separate cell identifiers".into() });
        }
        for (u, v) in &edges {
            if !vset.contains(u) || !vset.contains(v) {
                return Err(WdpError::InvalidInput {
                    detail: format!("Edge ({}, {}) references undeclared vertex", u, v),
                });
            }
        }
        Ok(Self { vertices, edges })
    }

    pub fn num_vertices(&self) -> usize {
        self.vertices.len()
    }

    pub fn num_edges(&self) -> usize {
        self.edges.len()
    }

    pub fn coboundary_0(&self, c0: &Cochain0) -> Result<Cochain1, WdpError> {
        let mut values = BTreeMap::new();
        for (u, v) in &self.edges {
            let val_u = c0.get(u)?;
            let val_v = c0.get(v)?;
            let diff = val_v - val_u;
            values.insert((u.clone(), v.clone()), diff);
        }
        Ok(Cochain1 { values })
    }

    pub fn boundary_1(&self, c1: &Cochain1) -> Result<Cochain0, WdpError> {
        let mut values = BTreeMap::new();
        for v in &self.vertices {
            values.insert(v.clone(), BigRational::zero());
        }
        for ((u, v), val) in &c1.values {
            let u_entry = values.get_mut(u).ok_or_else(|| WdpError::InvalidInput {
                detail: format!("unknown vertex {}", u),
            })?;
            *u_entry -= val;
            let v_entry = values.get_mut(v).ok_or_else(|| WdpError::InvalidInput {
                detail: format!("unknown vertex {}", v),
            })?;
            *v_entry += val;
        }
        Ok(Cochain0 { values })
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct Cochain0 {
    pub values: BTreeMap<String, BigRational>,
}

impl Cochain0 {
    pub fn get(&self, vertex: &str) -> Result<BigRational, WdpError> {
        self.values
            .get(vertex)
            .cloned()
            .ok_or_else(|| WdpError::InvalidInput {
                detail: format!("Vertex {} not found in cochain", vertex),
            })
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct Cochain1 {
    pub values: BTreeMap<(String, String), BigRational>,
}

impl Cochain1 {
    pub fn l1_norm(&self) -> BigRational {
        omega_functional::Phi1Functional::unweighted_l1_rational(
            &self.values.values().cloned().collect::<Vec<_>>(),
        )
        .expect("exact cochain entries")
    }
}
