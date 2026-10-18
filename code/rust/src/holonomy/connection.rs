
use crate::error::HolonomyError;
use crate::graph::CellComplex;
use crate::matrix::{ExactMatrix, ExactScalar};
use num_rational::BigRational;
use omega_kernel::resource_limits::OperationLimits;
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};
use std::collections::BTreeMap;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DiscreteConnection<T: ExactScalar> {
    pub dim: usize,
    pub limits: OperationLimits,
    pub forward: BTreeMap<(String, String), ExactMatrix<T>>,
    pub reverse: BTreeMap<(String, String), ExactMatrix<T>>,
}

impl<T: ExactScalar> DiscreteConnection<T> {
    pub fn new(dim: usize, limits: OperationLimits) -> Self {
        Self {
            dim,
            limits,
            forward: BTreeMap::new(),
            reverse: BTreeMap::new(),
        }
    }

    pub fn set_connection(
        &mut self,
        u: impl Into<String>,
        v: impl Into<String>,
        matrix: ExactMatrix<T>,
    ) -> Result<(), HolonomyError> {
        let u_str = u.into();
        let v_str = v.into();

        if matrix.rows != self.dim || matrix.cols != self.dim {
            return Err(HolonomyError::DimensionMismatch {
                expected: self.dim,
                actual: matrix.rows,
            });
        }
        let forward_key = (u_str.clone(), v_str.clone());
        let opposite_key = (v_str.clone(), u_str.clone());
        let replacing =
            self.forward.contains_key(&forward_key) || self.forward.contains_key(&opposite_key);
        if !replacing && self.forward.len() >= self.limits.max_edges {
            return Err(HolonomyError::AllocationFailure {
                requested: self.forward.len() + 1,
                detail: format!("Max edges limit exceeded ({})", self.limits.max_edges),
            });
        }

        let inv = matrix.inverse().map_err(|e| match e {
            HolonomyError::SingularMatrix { detail } => HolonomyError::SingularConnection {
                src: u_str.clone(),
                tgt: v_str.clone(),
                detail,
            },
            other => other,
        })?;

        self.forward.remove(&forward_key);
        self.forward.remove(&opposite_key);
        self.reverse.remove(&forward_key);
        self.reverse.remove(&opposite_key);
        self.forward.insert(forward_key, matrix);
        self.reverse.insert(opposite_key, inv);
        Ok(())
    }

    pub fn get_step(&self, u: &str, v: &str) -> Result<&ExactMatrix<T>, HolonomyError> {
        let key = (u.to_string(), v.to_string());
        if let Some(m) = self.forward.get(&key) {
            return Ok(m);
        }
        if let Some(m) = self.reverse.get(&key) {
            return Ok(m);
        }
        Err(HolonomyError::EdgeNotFound {
            src: u.to_string(),
            tgt: v.to_string(),
        })
    }

    pub fn from_pure_gauge(
        complex: &CellComplex,
        gauge_potentials: &BTreeMap<String, ExactMatrix<T>>,
        dim: usize,
        limits: OperationLimits,
    ) -> Result<Self, HolonomyError> {
        let mut conn = Self::new(dim, limits);
        for v in &complex.vertices {
            if !gauge_potentials.contains_key(&v.id) {
                return Err(HolonomyError::VertexNotFound { id: v.id.clone() });
            }
        }

        for edge in &complex.edges {
            let gu = gauge_potentials.get(&edge.source).unwrap();
            let gv = gauge_potentials.get(&edge.target).unwrap();
            if gu.rows != dim || gu.cols != dim || gv.rows != dim || gv.cols != dim {
                return Err(HolonomyError::DimensionMismatch {
                    expected: dim,
                    actual: gu.rows,
                });
            }
            let gu_inv = gu.inverse()?;
            let u_mat = gv.matmul(&gu_inv)?;
            conn.set_connection(&edge.source, &edge.target, u_mat)?;
        }
        Ok(conn)
    }

    pub fn apply_gauge_transformation(
        &self,
        gauge_potentials: &BTreeMap<String, ExactMatrix<T>>,
    ) -> Result<Self, HolonomyError> {
        let mut transformed = Self::new(self.dim, self.limits);
        for ((u, v), u_mat) in &self.forward {
            let gu = gauge_potentials
                .get(u)
                .ok_or_else(|| HolonomyError::VertexNotFound { id: u.clone() })?;
            let gv = gauge_potentials
                .get(v)
                .ok_or_else(|| HolonomyError::VertexNotFound { id: v.clone() })?;
            if gu.rows != self.dim
                || gu.cols != self.dim
                || gv.rows != self.dim
                || gv.cols != self.dim
            {
                return Err(HolonomyError::DimensionMismatch {
                    expected: self.dim,
                    actual: gu.rows,
                });
            }
            let gu_inv = gu.inverse()?;
            let gv_u = gv.matmul(u_mat)?;
            let new_u = gv_u.matmul(&gu_inv)?;
            transformed.set_connection(u, v, new_u)?;
        }
        Ok(transformed)
    }

    pub fn content_hash(&self) -> String {
        let mut hasher = Sha256::new();
        hasher.update(format!("DiscreteConnection:dim={}\n", self.dim).as_bytes());
        for ((u, v), m) in &self.forward {
            hasher.update(format!("Edge:{u}->{v}:{};\n", m.sha256_digest()).as_bytes());
        }
        format!("{:x}", hasher.finalize())
    }
}

pub type Connection = DiscreteConnection<BigRational>;
