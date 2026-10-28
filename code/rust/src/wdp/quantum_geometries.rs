
use std::collections::BTreeMap;

use linear_algebra::exact_ldlt::is_psd_rational;
use num_bigint::BigInt;
use num_rational::BigRational;
use num_traits::{One, Zero};
use serde::{Deserialize, Serialize};

use crate::types::AuthorityEffect;
use linear_algebra::backend::basic_matrix::BasicMatrix;
use engine_number_theory::cyclotomic::GaussianRat;
use engine_quantum_physics::exact_channel::{ExactChannelError, ExactKrausChannel};

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct QuantumGeometryReceipt {
    pub is_valid_density: bool,
    pub trace: BigRational,
    pub is_positive_semidefinite: bool,
    pub classical_shadow_probabilities: Vec<BigRational>,
    pub trace_distance_to_target: Option<BigRational>,
    pub classical_l1_distance: Option<BigRational>,
    pub is_contractive: bool,
    pub authority_effect: AuthorityEffect,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct QuantumDensityStalk {
    pub dim: usize,
    pub data: Vec<Vec<BigRational>>,
    pub authority_effect: AuthorityEffect,
}

impl QuantumDensityStalk {
    pub fn new(data: Vec<Vec<BigRational>>) -> Result<Self, &'static str> {
        let k = data.len();
        if k == 0 {
            return Err("Density stalk dimension cannot be 0");
        }
        for row in &data {
            if row.len() != k {
                return Err("Density matrix must be square");
            }
        }
        Ok(Self {
            dim: k,
            data,
            authority_effect: AuthorityEffect::None,
        })
    }

    pub fn from_pure_vector(psi: &[BigRational]) -> Result<Self, &'static str> {
        let k = psi.len();
        if k == 0 {
            return Err("Vector dimension cannot be 0");
        }
        let norm_sq: BigRational = psi.iter().map(|x| x * x).sum();
        if norm_sq.is_zero() {
            return Err("Cannot form pure state from zero vector");
        }
        let mut data = vec![vec![BigRational::zero(); k]; k];
        for i in 0..k {
            for j in 0..k {
                data[i][j] = (&psi[i] * &psi[j]) / &norm_sq;
            }
        }
        Ok(Self {
            dim: k,
            data,
            authority_effect: AuthorityEffect::None,
        })
    }

    pub fn maximally_mixed(dim: usize) -> Result<Self, &'static str> {
        if dim == 0 {
            return Err("Dimension cannot be 0");
        }
        let factor = BigRational::new(BigInt::one(), BigInt::from(dim));
        let mut data = vec![vec![BigRational::zero(); dim]; dim];
        for i in 0..dim {
            data[i][i] = factor.clone();
        }
        Ok(Self {
            dim,
            data,
            authority_effect: AuthorityEffect::None,
        })
    }

    pub fn try_density(data: Vec<Vec<BigRational>>) -> Result<Self, &'static str> {
        let stalk = Self::new(data)?;
        if !stalk.is_symmetric() {
            return Err("Density matrix must be symmetric");
        }
        if stalk.trace() != BigRational::one() {
            return Err("Density matrix must have trace one");
        }
        if !stalk.is_positive_semidefinite() {
            return Err("Density matrix must be positive semidefinite");
        }
        Ok(stalk)
    }

    pub fn to_gaussian(&self) -> Result<BasicMatrix<GaussianRat>, &'static str> {
        if !self.has_valid_shape() {
            return Err("Density matrix shape does not match its dimension");
        }
        to_gaussian_matrix(&self.data)
    }

    pub fn trace(&self) -> BigRational {
        let mut tr = BigRational::zero();
        for i in 0..self.dim {
            tr += &self.data[i][i];
        }
        tr
    }

    pub fn is_symmetric(&self) -> bool {
        for i in 0..self.dim {
            for j in (i + 1)..self.dim {
                if self.data[i][j] != self.data[j][i] {
                    return false;
                }
            }
        }
        true
    }

    pub fn is_positive_semidefinite(&self) -> bool {
        self.is_symmetric() && is_psd_rational(&self.data)
    }

    pub fn is_valid_density_matrix(&self) -> bool {
        self.has_valid_shape()
            && self.trace() == BigRational::one()
            && self.is_positive_semidefinite()
    }

    pub fn classical_population_shadow(&self) -> Vec<BigRational> {
        (0..self.dim).map(|i| self.data[i][i].clone()).collect()
    }

    pub fn trace_distance_squared_2x2(&self, other: &Self) -> Result<BigRational, &'static str> {
        if self.dim != 2 || other.dim != 2 {
            return Err("trace_distance_2x2 is specialized for dimension 2");
        }
        if !self.has_valid_shape() || !other.has_valid_shape() {
            return Err("Density matrix shape does not match its dimension");
        }
        engine_functional::distinguishability::DistinguishabilityFunctional::qubit_trace_distance_squared(&self.data, &other.data)
    }

    pub fn trace_distance_2x2(&self, other: &Self) -> Result<BigRational, &'static str> {
        if self.dim != 2 || other.dim != 2 {
            return Err("trace_distance_2x2 is specialized for dimension 2");
        }
        if !self.has_valid_shape() || !other.has_valid_shape() {
            return Err("Density matrix shape does not match its dimension");
        }
        engine_functional::distinguishability::DistinguishabilityFunctional::qubit_trace_distance(
            &self.data,
            &other.data,
        )
    }

    pub fn classical_shadow_contraction_slack_2x2(
        &self,
        other: &Self,
    ) -> Result<BigRational, &'static str> {
        if self.dim != 2 || other.dim != 2 {
            return Err("trace_distance_2x2 is specialized for dimension 2");
        }
        if !self.has_valid_shape() || !other.has_valid_shape() {
            return Err("Density matrix shape does not match its dimension");
        }
        engine_functional::distinguishability::DistinguishabilityFunctional::qubit_shadow_contraction_slack(&self.data, &other.data)
    }

    fn has_valid_shape(&self) -> bool {
        self.dim > 0
            && self.data.len() == self.dim
            && self.data.iter().all(|row| row.len() == self.dim)
    }

    pub fn classical_l1_distance(&self, other: &Self) -> BigRational {
        let p = self.classical_population_shadow();
        let q = other.classical_population_shadow();
        engine_functional::distinguishability::DistinguishabilityFunctional::rational_total_variation(&p,&q)
            .expect("matching exact diagonal shadows")
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct CptpChannel {
    pub dim: usize,
    pub kraus_operators: Vec<Vec<Vec<BigRational>>>,
    pub authority_effect: AuthorityEffect,
}

impl CptpChannel {
    pub fn identity(dim: usize) -> Self {
        let mut k0 = vec![vec![BigRational::zero(); dim]; dim];
        for i in 0..dim {
            k0[i][i] = BigRational::one();
        }
        Self {
            dim,
            kraus_operators: vec![k0],
            authority_effect: AuthorityEffect::None,
        }
    }

    pub fn new(kraus: Vec<Vec<Vec<BigRational>>>) -> Result<Self, &'static str> {
        if kraus.is_empty() {
            return Err("Must have at least one Kraus operator");
        }
        let dim = kraus[0].len();
        if dim == 0 {
            return Err("Kraus operator dimension cannot be 0");
        }
        if kraus
            .iter()
            .any(|k| k.len() != dim || k.iter().any(|row| row.len() != dim))
        {
            return Err("Kraus operators must be square and share a dimension");
        }
        let mut sum_kt_k = vec![vec![BigRational::zero(); dim]; dim];
        for k in &kraus {
            if k.len() != dim {
                return Err("Kraus operator dimension mismatch");
            }
            for i in 0..dim {
                for j in 0..dim {
                    let mut dot = BigRational::zero();
                    for m in 0..dim {
                        dot += &k[m][i] * &k[m][j];
                    }
                    sum_kt_k[i][j] += dot;
                }
            }
        }
        for i in 0..dim {
            for j in 0..dim {
                let expected = if i == j {
                    BigRational::one()
                } else {
                    BigRational::zero()
                };
                if sum_kt_k[i][j] != expected {
                    return Err("Kraus operators do not satisfy trace preservation completeness sum K_i^T K_i = I");
                }
            }
        }
        Ok(Self {
            dim,
            kraus_operators: kraus,
            authority_effect: AuthorityEffect::None,
        })
    }

    fn has_valid_shape(&self) -> bool {
        self.dim > 0
            && !self.kraus_operators.is_empty()
            && self
                .kraus_operators
                .iter()
                .all(|k| k.len() == self.dim && k.iter().all(|row| row.len() == self.dim))
    }

    pub fn to_exact_kraus(&self) -> Result<ExactKrausChannel, ExactChannelError> {
        if self.dim == 0 {
            return Err(ExactChannelError::ZeroDimension);
        }
        if self.kraus_operators.is_empty() {
            return Err(ExactChannelError::EmptyKrausSet);
        }
        let mut ops = Vec::with_capacity(self.kraus_operators.len());
        for (index, k) in self.kraus_operators.iter().enumerate() {
            let cols = k.first().map_or(0, Vec::len);
            if k.len() != self.dim || k.iter().any(|row| row.len() != self.dim) {
                return Err(ExactChannelError::KrausShape {
                    index,
                    expected: (self.dim, self.dim),
                    actual: (k.len(), cols),
                });
            }
            ops.push(
                to_gaussian_matrix(k).map_err(|_| ExactChannelError::KrausShape {
                    index,
                    expected: (self.dim, self.dim),
                    actual: (k.len(), cols),
                })?,
            );
        }
        ExactKrausChannel::try_new(self.dim, self.dim, ops, "wdp_cptp_channel")
    }

    pub fn apply(&self, stalk: &QuantumDensityStalk) -> Result<QuantumDensityStalk, &'static str> {
        if stalk.dim != self.dim {
            return Err("Density stalk dimension must match channel dimension");
        }
        if !stalk.has_valid_shape() || !self.has_valid_shape() {
            return Err("Channel or stalk shape does not match its dimension");
        }
        let dim = self.dim;
        let mut out_data = vec![vec![BigRational::zero(); dim]; dim];

        for k in &self.kraus_operators {
            let mut k_rho = vec![vec![BigRational::zero(); dim]; dim];
            for i in 0..dim {
                for j in 0..dim {
                    let mut sum = BigRational::zero();
                    for m in 0..dim {
                        sum += &k[i][m] * &stalk.data[m][j];
                    }
                    k_rho[i][j] = sum;
                }
            }
            for i in 0..dim {
                for j in 0..dim {
                    let mut sum = BigRational::zero();
                    for m in 0..dim {
                        sum += &k_rho[i][m] * &k[j][m];
                    }
                    out_data[i][j] += sum;
                }
            }
        }

        QuantumDensityStalk::new(out_data)
    }
}

fn to_gaussian_matrix(rows: &[Vec<BigRational>]) -> Result<BasicMatrix<GaussianRat>, &'static str> {
    let n = rows.len();
    let data = rows
        .iter()
        .flat_map(|r| r.iter().map(|x| GaussianRat::from_rational(x.clone())))
        .collect();
    BasicMatrix::from_row_major(n, n, data).map_err(|_| "matrix is not square")
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct QuantumObserverBundle {
    pub vertices: Vec<String>,
    pub edges: Vec<(String, String)>,
    pub vertex_stalks: BTreeMap<String, QuantumDensityStalk>,
    pub edge_channels: BTreeMap<(String, String), CptpChannel>,
    pub authority_effect: AuthorityEffect,
}

impl QuantumObserverBundle {
    pub fn new(
        vertices: Vec<String>,
        edges: Vec<(String, String)>,
        stalks: BTreeMap<String, QuantumDensityStalk>,
        channels: BTreeMap<(String, String), CptpChannel>,
    ) -> Result<Self, &'static str> {
        for v in &vertices {
            if !stalks.contains_key(v) {
                return Err("Missing stalk for declared vertex");
            }
        }
        for e in &edges {
            if !channels.contains_key(e) {
                return Err("Missing transition channel for declared edge");
            }
        }
        Ok(Self {
            vertices,
            edges,
            vertex_stalks: stalks,
            edge_channels: channels,
            authority_effect: AuthorityEffect::None,
        })
    }

    pub fn evaluate_edge_defect_2x2(&self, u: &str, v: &str) -> Result<BigRational, &'static str> {
        let edge_key = (u.to_string(), v.to_string());
        let channel = self
            .edge_channels
            .get(&edge_key)
            .ok_or("Channel not found")?;
        let rho_u = self.vertex_stalks.get(u).ok_or("Stalk u not found")?;
        let rho_v = self.vertex_stalks.get(v).ok_or("Stalk v not found")?;

        let evolved = channel.apply(rho_u)?;
        evolved.trace_distance_2x2(rho_v)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use engine_homology::scalar::{q, qr};

    #[test]
    fn test_density_stalk_validity_and_shadow() {
        let rho = QuantumDensityStalk::maximally_mixed(2).unwrap();
        assert!(rho.is_valid_density_matrix());
        assert_eq!(rho.trace(), q(1));

        let shadow = rho.classical_population_shadow();
        assert_eq!(shadow, vec![qr(1, 2), qr(1, 2)]);
        assert_eq!(rho.authority_effect, AuthorityEffect::None);
    }

    #[test]
    fn test_psd_is_exact_in_every_dimension() {
        let rows = |r: &[[i64; 4]]| r.iter().map(|row| row.map(q).to_vec()).collect::<Vec<_>>();
        let indefinite_3 = QuantumDensityStalk::new(vec![
            vec![q(0), q(0), q(0)],
            vec![q(0), q(0), q(1)],
            vec![q(0), q(1), q(0)],
        ])
        .unwrap();
        assert!(!indefinite_3.is_positive_semidefinite());

        let indefinite_4 = QuantumDensityStalk::new(rows(&[
            [1, 2, 0, 0],
            [2, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ]))
        .unwrap();
        assert!(!indefinite_4.is_positive_semidefinite());

        let mixed_4 = QuantumDensityStalk::maximally_mixed(4).unwrap();
        assert!(mixed_4.is_valid_density_matrix());
    }

    #[test]
    fn test_cptp_channel_trace_preservation() {
        let id_channel = CptpChannel::identity(2);
        let psi = vec![q(1), q(0)];
        let pure = QuantumDensityStalk::from_pure_vector(&psi).unwrap();

        let evolved = id_channel.apply(&pure).unwrap();
        assert_eq!(evolved.trace(), q(1));
        assert_eq!(evolved, pure);
    }

    #[test]
    fn test_schatten_to_classical_contraction() {
        let psi0 = vec![q(1), q(0)];
        let psi1 = vec![q(0), q(1)];
        let rho0 = QuantumDensityStalk::from_pure_vector(&psi0).unwrap();
        let rho1 = QuantumDensityStalk::from_pure_vector(&psi1).unwrap();

        let trace_dist = rho0.trace_distance_2x2(&rho1).unwrap();
        let classical_dist = rho0.classical_l1_distance(&rho1);

        assert_eq!(trace_dist, q(1));
        assert_eq!(classical_dist, q(1));
        assert!(classical_dist <= trace_dist);
    }
}
