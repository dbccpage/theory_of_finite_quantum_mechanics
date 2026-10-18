// Executable finite evidence; AuthorityEffect: None.
//! Chapter 5: Declared U(1) connections, gauge transformations,
//! Hermitian connection Laplacians, and spectral perturbation bounds.
//! Finite evidence for WDP-CH05-P01, WDP-CH05-P02, and the declared U(1)
//! specialization of WDP-CH05-O01; not a general vector-bundle perturbation proof.
//!
//! WDP owns the declaration: a named vertex carrier and exact unit-modulus
//! phases over Q(i), validated once in [`U1Connection::new`]. Everything
//! computed from it belongs to `omega_holonomy`, exactly and without floats:
//! - loop holonomy: `omega_holonomy::compute_loop_holonomy` on [`U1Connection::connection`];
//! - the Hermitian connection Laplacian L_U = D - A_U and its quadratic form:
//!   `omega_holonomy::ConnectionLaplacian::compute`;
//! - the WDP-CH05-O01 Weyl–Gershgorin bound:
//!   `omega_holonomy::ConnectionLaplacian::perturbation_certificate`.

use omega_kernel::resource_limits::OperationLimits;
use std::collections::{BTreeMap, BTreeSet};

use num_rational::BigRational;
use num_traits::{One, Signed, Zero};
use omega_holonomy::{CellComplex, DiscreteConnection, ExactMatrix, ExactScalar, GaussianRational};
use serde::Serialize;

use crate::error::WdpError;
use crate::types::AuthorityEffect;

/// A declared U(1) connection on a finite oriented graph.
///
/// Phases are exact Gaussian rationals of modulus one, such as `3/5 + 4/5 i`.
/// A reverse edge, if declared, must carry exactly the conjugate phase; if it is
/// not declared, `omega_holonomy` supplies the inverse, which for a unit phase is
/// the conjugate. There is no deserializer: every value passed through `new`.
#[derive(Debug, Clone, Serialize)]
pub struct U1Connection {
    complex: CellComplex,
    connection: DiscreteConnection<GaussianRational<BigRational>>,
    authority_effect: AuthorityEffect,
}

/// Exact finite comparison of two declared unweighted U(1) Laplacians.
/// The spectral statement is conditional on the caller's supplied lower bound
/// being a valid gap bound for the first Laplacian; this receipt does not prove it.
#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct U1PerturbationComparison {
    pub row_sum_bounds: Vec<BigRational>,
    pub operator_norm_bound: BigRational,
    pub gap_shrinkage_bound: BigRational,
    pub assumed_gap_lower_bound: BigRational,
    pub gap_survives_if_assumption_holds: bool,
    pub authority_effect: AuthorityEffect,
}

impl U1Connection {
    pub fn new(
        vertices: BTreeSet<String>,
        phases: BTreeMap<(String, String), GaussianRational<BigRational>>,
    ) -> Result<Self, WdpError> {
        if vertices.is_empty() {
            return Err(WdpError::InvalidInput {
                detail: "connection vertices cannot be empty".to_string(),
            });
        }
        let limits = OperationLimits::holonomy();
        let mut complex = CellComplex::new(limits);
        for v in &vertices {
            complex.add_vertex(v.clone())?;
        }
        let mut connection = DiscreteConnection::new(1, limits);
        for ((u, v), ph) in &phases {
            if u == v {
                return Err(WdpError::InvalidInput {
                    detail: format!("connection self-loop ({u}, {v}) not allowed"),
                });
            }
            if !vertices.contains(u) || !vertices.contains(v) {
                return Err(WdpError::InvalidInput {
                    detail: format!("connection edge ({u}, {v}) leaves carrier"),
                });
            }
            if !ph.norm_sq().is_one() {
                return Err(WdpError::InvalidInput {
                    detail: format!("connection phase for ({u}, {v}) is not unit modulus"),
                });
            }
            if let Some(rev_ph) = phases.get(&(v.clone(), u.clone())) {
                if *rev_ph != ph.conjugate() {
                    return Err(WdpError::InvalidInput {
                        detail: format!("reverse edge ({v}, {u}) is not conjugate phase"),
                    });
                }
                if u > v {
                    // Already registered from the (v, u) declaration.
                    continue;
                }
            }
            complex.add_edge(u, v)?;
            connection.set_connection(
                u.clone(),
                v.clone(),
                ExactMatrix::try_new(1, 1, vec![ph.clone()])?,
            )?;
        }

        Ok(Self {
            complex,
            connection,
            authority_effect: AuthorityEffect::None,
        })
    }

    /// The vertex and edge carrier, as `omega_holonomy` sees it.
    pub fn complex(&self) -> &CellComplex {
        &self.complex
    }

    /// The 1×1 transport matrices, as `omega_holonomy` sees them.
    pub fn connection(&self) -> &DiscreteConnection<GaussianRational<BigRational>> {
        &self.connection
    }

    pub fn authority_effect(&self) -> AuthorityEffect {
        self.authority_effect
    }

    /// Compute an exact perturbation bound from the two actual connections.
    ///
    /// With H = L(other) - L(self), each |H_ij| is at most
    /// |Re H_ij| + |Im H_ij|. Hermiticity gives ||H||_2 <= max row sum,
    /// so Weyl bounds every ordered eigenvalue displacement by that value
    /// and every adjacent spectral-gap shrinkage by twice that value.
    /// Unlike an epsilon declaration, these bounds are computed from transports.
    pub fn perturbation_comparison(
        &self,
        other: &Self,
        assumed_gap_lower_bound: BigRational,
    ) -> Result<U1PerturbationComparison, WdpError> {
        if assumed_gap_lower_bound.is_negative() {
            return Err(WdpError::InvalidInput {
                detail: "assumed spectral gap cannot be negative".to_string(),
            });
        }
        let names = |connection: &Self| {
            connection
                .complex
                .vertices
                .iter()
                .map(|v| v.id.clone())
                .collect::<Vec<_>>()
        };
        if names(self) != names(other) {
            return Err(WdpError::InvalidInput {
                detail: "perturbation comparison requires the same ordered vertex carrier"
                    .to_string(),
            });
        }
        let first =
            omega_holonomy::ConnectionLaplacian::compute(&self.complex, &self.connection, None)?;
        let second =
            omega_holonomy::ConnectionLaplacian::compute(&other.complex, &other.connection, None)?;
        let mut row_sum_bounds = Vec::with_capacity(first.total_dim);
        for i in 0..first.total_dim {
            let mut sum = BigRational::zero();
            for j in 0..first.total_dim {
                let delta = second.matrix.get(i, j).clone() - first.matrix.get(i, j).clone();
                sum += delta.re.abs() + delta.im.abs();
            }
            row_sum_bounds.push(sum);
        }
        let operator_norm_bound = row_sum_bounds
            .iter()
            .max()
            .cloned()
            .unwrap_or_else(BigRational::zero);
        let gap_shrinkage_bound = &operator_norm_bound + &operator_norm_bound;
        Ok(U1PerturbationComparison {
            gap_survives_if_assumption_holds: assumed_gap_lower_bound > gap_shrinkage_bound,
            assumed_gap_lower_bound,
            row_sum_bounds,
            operator_norm_bound,
            gap_shrinkage_bound,
            authority_effect: AuthorityEffect::None,
        })
    }

    /// Applies a U(1) gauge transformation g: V -> U(1), U'_uv = g(u)^* U_uv g(v).
    ///
    /// Each gauge phase must be exactly unit modulus, so the result is again a
    /// U(1) connection. The action itself is `omega_holonomy`'s
    /// `apply_gauge_transformation`, U'(u, v) = g(v) U(u, v) g(u)^{-1}, which for
    /// commuting unit phases is the same map.
    pub fn gauge_transform(
        &self,
        gauge: &BTreeMap<String, GaussianRational<BigRational>>,
    ) -> Result<Self, WdpError> {
        let mut potentials = BTreeMap::new();
        for vertex in &self.complex.vertices {
            let g = gauge
                .get(&vertex.id)
                .ok_or_else(|| WdpError::InvalidInput {
                    detail: format!("missing gauge phase for vertex {}", vertex.id),
                })?;
            if !g.norm_sq().is_one() {
                return Err(WdpError::InvalidInput {
                    detail: format!("gauge phase for vertex {} is not unit modulus", vertex.id),
                });
            }
            potentials.insert(
                vertex.id.clone(),
                ExactMatrix::try_new(1, 1, vec![g.clone()])?,
            );
        }
        Ok(Self {
            complex: self.complex.clone(),
            connection: self.connection.apply_gauge_transformation(&potentials)?,
            authority_effect: AuthorityEffect::None,
        })
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use num_traits::Zero;
    use omega_holonomy::{compute_loop_holonomy, ConnectionLaplacian};
    use omega_homology::scalar::{q, qr};

    fn phase(re: BigRational, im: BigRational) -> GaussianRational<BigRational> {
        GaussianRational::new(re, im)
    }

    fn triangle(phases: [GaussianRational<BigRational>; 3]) -> U1Connection {
        let vertices = BTreeSet::from(["0".to_string(), "1".to_string(), "2".to_string()]);
        let edges = [("0", "1"), ("1", "2"), ("2", "0")];
        let map = edges
            .iter()
            .zip(phases)
            .map(|((u, v), ph)| ((u.to_string(), v.to_string()), ph))
            .collect();
        U1Connection::new(vertices, map).unwrap()
    }

    fn loop_path() -> Vec<String> {
        ["0", "1", "2", "0"].map(String::from).to_vec()
    }

    #[test]
    fn test_u1_connection_and_laplacian() {
        let one = GaussianRational::one();
        let conn = triangle([one.clone(), one.clone(), one.clone()]);
        let hol = compute_loop_holonomy(conn.connection(), &loop_path()).unwrap();
        assert_eq!(hol.get(0, 0), &one);

        let lap = ConnectionLaplacian::compute(conn.complex(), conn.connection(), None).unwrap();
        assert!(lap.is_hermitian());
        // A flat connection's constant section has zero Dirichlet energy.
        let constant = vec![one.clone(), one.clone(), one];
        assert!(lap.evaluate_quadratic_form(&constant).unwrap().is_zero());

        // Delta_W = 2 on the triangle: bound 2/100, tolerance 4/100 < 1/2.
        let cert = lap.perturbation_certificate(qr(1, 100), qr(1, 2)).unwrap();
        assert_eq!(cert.max_weighted_degree, q(2));
        assert!(cert.gap_survives);
    }

    #[test]
    fn test_frustrated_holonomy_is_gauge_invariant() {
        let one = GaussianRational::one();
        let rotation = phase(qr(3, 5), qr(4, 5));
        let conn = triangle([rotation.clone(), one.clone(), one]);
        let hol = compute_loop_holonomy(conn.connection(), &loop_path()).unwrap();
        assert_eq!(hol.get(0, 0), &rotation);

        let gauge = BTreeMap::from([
            ("0".to_string(), phase(qr(5, 13), qr(12, 13))),
            ("1".to_string(), phase(q(0), q(1))),
            ("2".to_string(), phase(qr(-3, 5), qr(4, 5))),
        ]);
        let gauged = conn.gauge_transform(&gauge).unwrap();
        let gauged_hol = compute_loop_holonomy(gauged.connection(), &loop_path()).unwrap();
        assert_eq!(gauged_hol.get(0, 0), &rotation);

        // A frustrated U(1) cycle has no parallel section: the Laplacian kernel is trivial.
        let lap = ConnectionLaplacian::compute(conn.complex(), conn.connection(), None).unwrap();
        assert!(lap.has_spectral_gap());
    }

    #[test]
    fn test_declarations_are_validated_exactly() {
        let vertices = BTreeSet::from(["0".to_string(), "1".to_string()]);
        let e01 = ("0".to_string(), "1".to_string());
        let e10 = ("1".to_string(), "0".to_string());

        let not_unit = BTreeMap::from([(e01.clone(), phase(qr(3, 5), qr(4, 6)))]);
        assert!(U1Connection::new(vertices.clone(), not_unit).is_err());

        let rotation = phase(qr(3, 5), qr(4, 5));
        let not_conjugate = BTreeMap::from([
            (e01.clone(), rotation.clone()),
            (e10.clone(), rotation.clone()),
        ]);
        assert!(U1Connection::new(vertices.clone(), not_conjugate).is_err());

        let conjugate = BTreeMap::from([(e01, rotation.clone()), (e10, rotation.conjugate())]);
        let conn = U1Connection::new(vertices, conjugate).unwrap();
        assert_eq!(conn.complex().edges.len(), 1);

        let not_unit_gauge = BTreeMap::from([
            ("0".to_string(), phase(q(2), q(0))),
            ("1".to_string(), GaussianRational::one()),
        ]);
        assert!(conn.gauge_transform(&not_unit_gauge).is_err());
    }
}
