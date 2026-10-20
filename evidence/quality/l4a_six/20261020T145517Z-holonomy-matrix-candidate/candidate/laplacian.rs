use crate::connection::DiscreteConnection;
use crate::error::HolonomyError;
use crate::graph::CellComplex;
use crate::matrix::{ExactMatrix, ExactScalar, GaussianRational};
use num_bigint::BigInt;
use num_rational::BigRational;
use num_traits::{Signed, Zero};
use serde::{Deserialize, Serialize};
use std::collections::BTreeMap;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ConnectionLaplacian<T: ExactScalar> {
    pub matrix: ExactMatrix<T>,
    pub num_vertices: usize,
    pub fiber_dim: usize,
    pub total_dim: usize,
}

impl<T: ExactScalar> ConnectionLaplacian<T> {
    pub fn compute(
        complex: &CellComplex,
        connection: &DiscreteConnection<T>,
        weights: Option<&BTreeMap<(String, String), T>>,
    ) -> Result<Self, HolonomyError> {
        validate_vertex_registry(complex)?;
        if let Some(weights) = weights {
            weights.values().try_for_each(ExactScalar::validate_exact)?;
        }
        let n = complex.vertices.len();
        let d = connection.dim;
        let total_dim = n.checked_mul(d).ok_or(HolonomyError::AllocationFailure {
            requested: usize::MAX,
            detail: "Laplacian dimension overflow".into(),
        })?;

        let mut lap = ExactMatrix::try_zero(total_dim, total_dim)?;

        for u in &complex.vertices {
            let u_idx = u.index;
            let mut weighted_deg = T::zero();

            for v in &complex.vertices {
                if u.id == v.id {
                    continue;
                }
                let v_idx = v.index;

                if let Ok(u_mat) = connection.get_step(&u.id, &v.id) {
                    if u_mat.shape() != (d, d) {
                        return Err(HolonomyError::DimensionMismatch {
                            expected: d,
                            actual: u_mat.rows().max(u_mat.cols()),
                        });
                    }
                    let w = weights
                        .and_then(|map| {
                            map.get(&(u.id.clone(), v.id.clone()))
                                .or_else(|| map.get(&(v.id.clone(), u.id.clone())))
                        })
                        .cloned()
                        .unwrap_or_else(T::one);

                    weighted_deg += w.clone();

                    for r in 0..d {
                        for c in 0..d {
                            let val = -w.clone() * u_mat.get(r, c)?.clone();
                            lap.set(u_idx * d + r, v_idx * d + c, val)?;
                        }
                    }
                }
            }

            for r in 0..d {
                lap.set(u_idx * d + r, u_idx * d + r, weighted_deg.clone())?;
            }
        }

        Ok(Self {
            matrix: lap,
            num_vertices: n,
            fiber_dim: d,
            total_dim,
        })
    }

    pub fn is_symmetric(&self) -> bool {
        self.matrix.is_symmetric()
    }

    pub fn is_hermitian(&self) -> bool {
        self.matrix.is_hermitian()
    }

    pub fn trace(&self) -> Result<T, HolonomyError> {
        self.matrix.trace()
    }

    pub fn evaluate_quadratic_form(&self, psi: &[T]) -> Result<T, HolonomyError> {
        self.validate_dimensions()?;
        psi.iter().try_for_each(ExactScalar::validate_exact)?;
        if psi.len() != self.total_dim {
            return Err(HolonomyError::DimensionMismatch {
                expected: self.total_dim,
                actual: psi.len(),
            });
        }
        let mut sum = T::zero();
        for r in 0..self.total_dim {
            let mut row_acc = T::zero();
            for (c, psi_c) in psi.iter().enumerate().take(self.total_dim) {
                row_acc += self.matrix.get(r, c)?.clone() * psi_c.clone();
            }
            sum += crate::matrix::ScalarRef::try_new(&psi[r])?.conjugate() * row_acc;
        }
        Ok(sum)
    }

    fn validate_dimensions(&self) -> Result<(), HolonomyError> {
        let expected = self
            .num_vertices
            .checked_mul(self.fiber_dim)
            .ok_or(HolonomyError::ResourceCountOverflow)?;
        if expected != self.total_dim || self.matrix.shape() != (expected, expected) {
            return Err(HolonomyError::DimensionMismatch {
                expected,
                actual: self.total_dim,
            });
        }
        Ok(())
    }

    pub fn kernel_dimension(&self) -> Result<usize, HolonomyError> {
        self.validate_dimensions()?;
        let rank = self.matrix.rank()?;
        self.total_dim
            .checked_sub(rank)
            .ok_or(HolonomyError::DimensionMismatch {
                expected: self.total_dim,
                actual: rank,
            })
    }

    pub fn has_spectral_gap(&self) -> Result<bool, HolonomyError> {
        Ok(self.kernel_dimension()? == 0)
    }
}

pub trait RealDiagonal: ExactScalar {
    fn as_rational(&self) -> Option<BigRational>;
}

impl RealDiagonal for BigRational {
    fn as_rational(&self) -> Option<BigRational> {
        Some(self.clone())
    }
}

impl RealDiagonal for GaussianRational<BigRational> {
    fn as_rational(&self) -> Option<BigRational> {
        self.imag().is_zero().then(|| self.real().clone())
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct PerturbationCertificate {
    pub max_weighted_degree: BigRational,
    pub transport_epsilon: BigRational,
    pub operator_norm_bound: BigRational,
    pub spectral_gap_tolerance: BigRational,
    pub unperturbed_gap: BigRational,
    pub gap_survives: bool,
}

impl<T: RealDiagonal> ConnectionLaplacian<T> {
    pub fn max_weighted_degree(&self) -> Result<BigRational, HolonomyError> {
        self.validate_dimensions()?;
        let mut max = BigRational::zero();
        for i in 0..self.total_dim {
            let entry = self.matrix.get(i, i)?;
            let degree =
                entry
                    .as_rational()
                    .ok_or_else(|| HolonomyError::NonHermitianLaplacian {
                        u: i.to_string(),
                        v: i.to_string(),
                        detail: format!("diagonal entry {entry} is not real"),
                    })?;
            if degree.is_negative() {
                return Err(HolonomyError::NegativeBound {
                    quantity: format!("weighted degree at index {i}"),
                    value: degree.to_string(),
                });
            }
            if degree > max {
                max = degree;
            }
        }
        Ok(max)
    }

    pub fn perturbation_certificate(
        &self,
        transport_epsilon: BigRational,
        unperturbed_gap: BigRational,
    ) -> Result<PerturbationCertificate, HolonomyError> {
        for (quantity, value) in [
            ("transport_epsilon", &transport_epsilon),
            ("unperturbed_gap", &unperturbed_gap),
        ] {
            value.validate_exact()?;
            if value.is_negative() {
                return Err(HolonomyError::NegativeBound {
                    quantity: quantity.to_string(),
                    value: value.to_string(),
                });
            }
        }
        if let Some((r, c)) = self.first_non_hermitian_entry()? {
            return Err(HolonomyError::NonHermitianLaplacian {
                u: r.to_string(),
                v: c.to_string(),
                detail: "Weyl's perturbation bound requires a Hermitian Laplacian".to_string(),
            });
        }
        let max_weighted_degree = self.max_weighted_degree()?;
        let operator_norm_bound = &max_weighted_degree * &transport_epsilon;
        let spectral_gap_tolerance =
            &operator_norm_bound * BigRational::from_integer(BigInt::from(2));
        let gap_survives = unperturbed_gap > spectral_gap_tolerance;
        Ok(PerturbationCertificate {
            max_weighted_degree,
            transport_epsilon,
            operator_norm_bound,
            spectral_gap_tolerance,
            unperturbed_gap,
            gap_survives,
        })
    }

    fn first_non_hermitian_entry(&self) -> Result<Option<(usize, usize)>, HolonomyError> {
        self.validate_dimensions()?;
        for r in 0..self.total_dim {
            for c in r..self.total_dim {
                if !self
                    .matrix
                    .get_scalar(r, c)?
                    .conjugate_eq(self.matrix.get_scalar(c, r)?)
                {
                    return Ok(Some((r, c)));
                }
            }
        }
        Ok(None)
    }
}

pub fn compute_connection_laplacian<T: ExactScalar>(
    complex: &CellComplex,
    connection: &DiscreteConnection<T>,
    weights: Option<&BTreeMap<(String, String), T>>,
) -> Result<ConnectionLaplacian<T>, HolonomyError> {
    ConnectionLaplacian::compute(complex, connection, weights)
}

fn validate_vertex_registry(complex: &CellComplex) -> Result<(), HolonomyError> {
    if complex.vertex_map.len() != complex.vertices.len() {
        return Err(HolonomyError::DimensionMismatch {
            expected: complex.vertices.len(),
            actual: complex.vertex_map.len(),
        });
    }
    for (expected, vertex) in complex.vertices.iter().enumerate() {
        let mapped =
            *complex
                .vertex_map
                .get(&vertex.id)
                .ok_or_else(|| HolonomyError::VertexNotFound {
                    id: vertex.id.clone(),
                })?;
        if mapped != expected || vertex.index != expected {
            return Err(HolonomyError::VertexRegistryMismatch {
                id: vertex.id.clone(),
                expected,
                declared: vertex.index,
                mapped,
            });
        }
    }
    Ok(())
}
