//! Compatibility facade for the admitted rational carrier. AuthorityEffect: None.
//!
//! All three carrier entry points share the same immutable law-checked core.

use super::cochain_complex::TheoremProvenance;
use crate::linear_algebra::basic_matrix::BasicMatrix;
use crate::linear_algebra::scalars::{q, Q};
use std::collections::BTreeMap;

pub use super::carrier_manifest::CarrierManifest;
pub use super::errors::HomologicalError as CarrierError;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Carrier {
    inner: super::carrier::Carrier,
}

impl AsRef<super::carrier::Carrier> for Carrier {
    fn as_ref(&self) -> &super::carrier::Carrier {
        &self.inner
    }
}

impl Carrier {
    pub fn new(
        c0_dim: usize,
        c1_dim: usize,
        c2_dim: usize,
        d0: BasicMatrix<Q>,
        d1: BasicMatrix<Q>,
        weights: Vec<Q>,
    ) -> Result<Self, CarrierError> {
        let provenance = TheoremProvenance::new("runtime exact d1*d0 verification".into())?;
        Ok(Self {
            inner: super::carrier::Carrier::new(
                c0_dim, c1_dim, c2_dim, d0, d1, weights, provenance,
            )?,
        })
    }
    pub fn c0_dim(&self) -> usize {
        self.inner.c0_dim()
    }
    pub fn c1_dim(&self) -> usize {
        self.inner.c1_dim()
    }
    pub fn c2_dim(&self) -> usize {
        self.inner.c2_dim()
    }
    pub fn d0(&self) -> &BasicMatrix<Q> {
        self.inner.d0()
    }
    pub fn d1(&self) -> &BasicMatrix<Q> {
        self.inner.d1()
    }
    pub fn weights(&self) -> &[Q] {
        self.inner.weights()
    }
    pub fn rank_d0(&self) -> usize {
        self.inner.rank_d0()
    }
    pub fn rank_d1(&self) -> usize {
        self.inner.rank_d1()
    }
    pub fn dim_q1(&self) -> usize {
        self.c1_dim() - self.rank_d0()
    }
    /// Rank inclusion was checked during construction; subtraction cannot underflow.
    pub fn dim_h1(&self) -> usize {
        self.c1_dim() - self.rank_d1() - self.rank_d0()
    }
}

/// Signed incidence carrier for a finite simple directed presentation.
/// Triangles (a,b,c) require edges a->b, b->c and a->c. Missing edges,
/// repeated vertices, parallel edges and self loops are rejected explicitly.
/// Construction costs O(E log E + T log E) table work, plus exact law/rank checks.
/// Opposite directed edges are distinct; duplicate directed edges are refused.
/// Triangle rows may repeat. Only repeated vertices within one triangle are
/// refused; each supplied triangle contributes its own signed row.
pub fn graph_carrier(
    num_nodes: usize,
    edges: &[(usize, usize)],
    triangles: &[(usize, usize, usize)],
    weights: Vec<Q>,
) -> Result<Carrier, CarrierError> {
    let indices = edge_indices(num_nodes, edges)?;
    let mut d0 = BasicMatrix::<Q>::zero(edges.len(), num_nodes)?;
    for (i, &(src, tgt)) in edges.iter().enumerate() {
        d0.set(i, src, q(-1))?;
        d0.set(i, tgt, q(1))?;
    }
    let d1 = triangle_boundary(num_nodes, edges.len(), triangles, &indices)?;
    Carrier::new(num_nodes, edges.len(), triangles.len(), d0, d1, weights)
}

fn triangle_boundary(
    num_nodes: usize,
    num_edges: usize,
    triangles: &[(usize, usize, usize)],
    indices: &BTreeMap<(usize, usize), usize>,
) -> Result<BasicMatrix<Q>, CarrierError> {
    let mut d1 = BasicMatrix::<Q>::zero(triangles.len(), num_edges)?;
    for (i, &(a, b, c)) in triangles.iter().enumerate() {
        admit_triangle(num_nodes, i, (a, b, c))?;
        for (src, tgt, sign) in [(a, b, 1), (b, c, 1), (a, c, -1)] {
            let col = indices
                .get(&(src, tgt))
                .ok_or(CarrierError::TriangleMissingEdge {
                    triangle: i,
                    src,
                    tgt,
                })?;
            d1.set(i, *col, q(sign))?;
        }
    }
    Ok(d1)
}

fn edge_indices(
    num_nodes: usize,
    edges: &[(usize, usize)],
) -> Result<BTreeMap<(usize, usize), usize>, CarrierError> {
    let mut indices = BTreeMap::new();
    for (i, &(src, tgt)) in edges.iter().enumerate() {
        admit_edge(num_nodes, i, src, tgt)?;
        if indices.insert((src, tgt), i).is_some() {
            return Err(CarrierError::BasisMismatch {
                description: "parallel directed edges".into(),
            });
        }
    }
    Ok(indices)
}

fn admit_edge(n: usize, edge: usize, src: usize, tgt: usize) -> Result<(), CarrierError> {
    if src >= n {
        return Err(CarrierError::EdgeSourceOutOfRange { edge, src });
    }
    if tgt >= n {
        return Err(CarrierError::EdgeTargetOutOfRange { edge, tgt });
    }
    if src == tgt {
        return Err(CarrierError::SelfLoopNotAllowed { node: src });
    }
    Ok(())
}

fn admit_triangle(
    n: usize,
    triangle: usize,
    (a, b, c): (usize, usize, usize),
) -> Result<(), CarrierError> {
    for vertex in [a, b, c] {
        if vertex >= n {
            return Err(CarrierError::TriangleVertexOutOfRange { triangle, vertex });
        }
    }
    if a == b || b == c || a == c {
        return Err(CarrierError::BasisMismatch {
            description: "triangle vertices must be distinct".into(),
        });
    }
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    use linear_algebra::linear_algebra::image_kernel::ExactRowReduction;

    fn r(n: i64) -> Q {
        q(n)
    }

    fn unit_weights(n: usize) -> Vec<Q> {
        vec![q(1); n]
    }

    #[test]
    fn maps_with_non_composable_shapes_must_be_rejected() {
        let d0 = BasicMatrix::<Q>::from_row_major(1, 2, vec![r(-1), r(1)]).unwrap();
        let d1 = BasicMatrix::<Q>::from_row_major(1, 1, vec![r(1)]).unwrap();
        let result = Carrier::new(2, 2, 1, d0, d1, unit_weights(2));
        assert!(matches!(result, Err(CarrierError::ShapeMismatch { .. })));
    }

    #[test]
    fn zero_complex() {
        let cx = Carrier::new(
            0,
            0,
            0,
            BasicMatrix::<Q>::zero(0, 0).unwrap(),
            BasicMatrix::<Q>::zero(0, 0).unwrap(),
            vec![],
        );
        assert!(cx.is_ok());
        let cx = cx.unwrap();
        assert_eq!(cx.dim_q1(), 0);
        assert_eq!(cx.dim_h1(), 0);
    }

    #[test]
    fn single_edge_tree() {
        let cx = graph_carrier(2, &[(0, 1)], &[], unit_weights(1)).unwrap();

        assert_eq!(cx.c0_dim(), 2);
        assert_eq!(cx.c1_dim(), 1);
        assert_eq!(cx.c2_dim(), 0);
        assert_eq!(cx.rank_d0(), 1);
        assert_eq!(cx.dim_q1(), 0);
        assert_eq!(cx.dim_h1(), 0);
    }

    #[test]
    fn triangle_cycle() {
        let cx =
            graph_carrier(3, &[(0, 1), (1, 2), (0, 2)], &[(0, 1, 2)], unit_weights(3)).unwrap();

        assert_eq!(cx.c0_dim(), 3);
        assert_eq!(cx.c1_dim(), 3);
        assert_eq!(cx.c2_dim(), 1);
        assert_eq!(cx.rank_d0(), 2);
        assert_eq!(cx.dim_q1(), 1);
        assert_eq!(cx.dim_h1(), 0);
    }

    #[test]
    fn triangle_cycle_no_filling() {
        let cx = graph_carrier(3, &[(0, 1), (1, 2), (0, 2)], &[], unit_weights(3)).unwrap();

        assert_eq!(cx.dim_q1(), 1);
        assert_eq!(cx.dim_h1(), 1);
    }

    #[test]
    fn path_graph_no_survivor() {
        let cx = graph_carrier(3, &[(0, 1), (1, 2)], &[], unit_weights(2)).unwrap();

        assert_eq!(cx.rank_d0(), 2);
        assert_eq!(cx.dim_q1(), 0);
        assert_eq!(cx.dim_h1(), 0);
    }

    #[test]
    fn cochain_relation_enforced() {
        let d0 = BasicMatrix::<Q>::from_row_major(2, 2, vec![r(1), r(0), r(0), r(1)]).unwrap();
        let d1 = BasicMatrix::<Q>::from_row_major(1, 2, vec![r(1), r(1)]).unwrap();

        let result = Carrier::new(2, 2, 1, d0, d1, unit_weights(2));
        assert_eq!(
            result,
            Err(CarrierError::CoboundaryLawViolation { degree: 0 })
        );
    }

    #[test]
    fn non_positive_weight_rejected() {
        let d0 = BasicMatrix::<Q>::from_row_major(1, 2, vec![r(-1), r(1)]).unwrap();
        let d1 = BasicMatrix::<Q>::zero(0, 1).unwrap();

        let result = Carrier::new(2, 1, 0, d0, d1, vec![q(0)]);
        assert!(matches!(
            result,
            Err(CarrierError::NonPositiveWeight { .. })
        ));
    }

    #[test]
    fn carrier_manifest_deterministic() {
        let cx = graph_carrier(3, &[(0, 1), (1, 2), (0, 2)], &[], unit_weights(3)).unwrap();

        let m1 = CarrierManifest::from_carrier(&cx);
        let m2 = CarrierManifest::from_carrier(&cx);

        assert_eq!(m1.carrier_hash(), m2.carrier_hash());
        assert_eq!(m1.dimensions().1 - m1.ranks().0, 1);
        assert_eq!(m1.dimensions().1 - m1.ranks().0 - m1.ranks().1, 1);
    }

    #[test]
    fn different_carriers_different_hashes() {
        let cx1 = graph_carrier(3, &[(0, 1), (1, 2), (0, 2)], &[], unit_weights(3)).unwrap();
        let cx2 = graph_carrier(3, &[(0, 1), (1, 2)], &[], unit_weights(2)).unwrap();

        let m1 = CarrierManifest::from_carrier(&cx1);
        let m2 = CarrierManifest::from_carrier(&cx2);

        assert_ne!(m1.carrier_hash(), m2.carrier_hash());
    }

    #[test]
    fn matrix_kernel_basis() {
        let cx = graph_carrier(3, &[(0, 1), (1, 2), (0, 2)], &[], unit_weights(3)).unwrap();
        let ker = cx.d0().try_transpose().unwrap().kernel_basis().unwrap();
        assert_eq!(ker.len(), 1);
    }
}
