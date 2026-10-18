
use crate::linear_algebra::scalars::{hash_rational, q, Q};
use crate::linear_algebra::basic_matrix::BasicMatrix;
use linear_algebra::linear_algebra::image_kernel::ExactRowReduction;
use num_traits::Zero;
use serde::{Deserialize, Serialize};

pub fn matrix_content_hash(m: &BasicMatrix<Q>) -> [u8; 32] {
    let mut hasher = blake3::Hasher::new();
    hasher.update(&(m.rows() as u64).to_le_bytes());
    hasher.update(&(m.cols() as u64).to_le_bytes());
    for val in m.as_slice() {
        hash_rational(&mut hasher, val);
    }
    *hasher.finalize().as_bytes()
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum CarrierError {
    CochainRelationViolated,
    DimensionMismatch {
        map_name: String,
        expected: (usize, usize),
        got: (usize, usize),
    },
    WeightDimensionMismatch {
        expected: usize,
        got: usize,
    },
    NonPositiveWeight {
        index: usize,
    },
    MatrixConstructionFailed,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Carrier {
    pub c0_dim: usize,
    pub c1_dim: usize,
    pub c2_dim: usize,
    pub d0: BasicMatrix<Q>,
    pub d1: BasicMatrix<Q>,
    pub weights: Vec<Q>,
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
        if d0.rows() != c1_dim || d0.cols() != c0_dim {
            return Err(CarrierError::DimensionMismatch {
                map_name: "d0".into(),
                expected: (c1_dim, c0_dim),
                got: (d0.rows(), d0.cols()),
            });
        }

        if d1.rows() != c2_dim || d1.cols() != c1_dim {
            return Err(CarrierError::DimensionMismatch {
                map_name: "d1".into(),
                expected: (c2_dim, c1_dim),
                got: (d1.rows(), d1.cols()),
            });
        }

        if weights.len() != c1_dim {
            return Err(CarrierError::WeightDimensionMismatch {
                expected: c1_dim,
                got: weights.len(),
            });
        }

        for (i, w) in weights.iter().enumerate() {
            if w <= &Q::zero() {
                return Err(CarrierError::NonPositiveWeight { index: i });
            }
        }

        if c2_dim > 0 && c0_dim > 0 {
            let product = d1
                .mul(&d0)
                .map_err(|_| CarrierError::MatrixConstructionFailed)?;
            if !product.as_slice().iter().all(|x| x.is_zero()) {
                return Err(CarrierError::CochainRelationViolated);
            }
        }

        Ok(Self {
            c0_dim,
            c1_dim,
            c2_dim,
            d0,
            d1,
            weights,
        })
    }

    pub fn rank_d0(&self) -> usize {
        self.d0
            .rank()
            .expect("rank is defined for finite Q matrices")
    }

    pub fn dim_q1(&self) -> usize {
        self.c1_dim - self.rank_d0()
    }

    pub fn rank_d1(&self) -> usize {
        self.d1
            .rank()
            .expect("rank is defined for finite Q matrices")
    }

    pub fn dim_h1(&self) -> usize {
        let ker_d1_dim = self.c1_dim - self.rank_d1();
        let im_d0_dim = self.rank_d0();
        ker_d1_dim.saturating_sub(im_d0_dim)
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct CarrierManifest {
    pub carrier_hash: [u8; 32],
    pub d0_hash: [u8; 32],
    pub d1_hash: [u8; 32],
    pub c0_dim: usize,
    pub c1_dim: usize,
    pub c2_dim: usize,
    pub rank_d0: usize,
    pub dim_q1: usize,
    pub dim_h1: usize,
}

impl CarrierManifest {
    pub fn from_carrier(carrier: &Carrier) -> Self {
        let d0_hash = matrix_content_hash(&carrier.d0);
        let d1_hash = matrix_content_hash(&carrier.d1);

        let mut hasher = blake3::Hasher::new();
        hasher.update(&d0_hash);
        hasher.update(&d1_hash);
        hasher.update(&(carrier.c0_dim as u64).to_le_bytes());
        hasher.update(&(carrier.c1_dim as u64).to_le_bytes());
        hasher.update(&(carrier.c2_dim as u64).to_le_bytes());
        for w in &carrier.weights {
            hash_rational(&mut hasher, w);
        }
        let carrier_hash = *hasher.finalize().as_bytes();

        Self {
            carrier_hash,
            d0_hash,
            d1_hash,
            c0_dim: carrier.c0_dim,
            c1_dim: carrier.c1_dim,
            c2_dim: carrier.c2_dim,
            rank_d0: carrier.rank_d0(),
            dim_q1: carrier.dim_q1(),
            dim_h1: carrier.dim_h1(),
        }
    }
}

pub fn graph_carrier(
    num_nodes: usize,
    edges: &[(usize, usize)],
    triangles: &[(usize, usize, usize)],
    weights: Vec<Q>,
) -> Result<Carrier, CarrierError> {
    let num_edges = edges.len();
    let num_triangles = triangles.len();

    let mut d0 = BasicMatrix::<Q>::zero(num_edges, num_nodes)
        .map_err(|_| CarrierError::MatrixConstructionFailed)?;
    for (e_idx, &(src, tgt)) in edges.iter().enumerate() {
        if src >= num_nodes || tgt >= num_nodes {
            return Err(CarrierError::DimensionMismatch {
                map_name: "graph_edge".into(),
                expected: (num_nodes, num_nodes),
                got: (src, tgt),
            });
        }
        d0.set(e_idx, src, q(-1))
            .map_err(|_| CarrierError::MatrixConstructionFailed)?;
        d0.set(e_idx, tgt, q(1))
            .map_err(|_| CarrierError::MatrixConstructionFailed)?;
    }

    let mut d1 = BasicMatrix::<Q>::zero(num_triangles, num_edges)
        .map_err(|_| CarrierError::MatrixConstructionFailed)?;
    for (t_idx, &(a, b, c)) in triangles.iter().enumerate() {
        for (e_idx, &(src, tgt)) in edges.iter().enumerate() {
            if src == a && tgt == b {
                d1.set(t_idx, e_idx, q(1))
                    .map_err(|_| CarrierError::MatrixConstructionFailed)?;
            } else if src == b && tgt == c {
                d1.set(t_idx, e_idx, q(1))
                    .map_err(|_| CarrierError::MatrixConstructionFailed)?;
            } else if src == a && tgt == c {
                d1.set(t_idx, e_idx, q(-1))
                    .map_err(|_| CarrierError::MatrixConstructionFailed)?;
            }
        }
    }

    Carrier::new(num_nodes, num_edges, num_triangles, d0, d1, weights)
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
        assert!(matches!(
            result,
            Err(CarrierError::DimensionMismatch { .. })
        ));
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

        assert_eq!(cx.c0_dim, 2);
        assert_eq!(cx.c1_dim, 1);
        assert_eq!(cx.c2_dim, 0);
        assert_eq!(cx.rank_d0(), 1);
        assert_eq!(cx.dim_q1(), 0);
        assert_eq!(cx.dim_h1(), 0);
    }

    #[test]
    fn triangle_cycle() {
        let cx =
            graph_carrier(3, &[(0, 1), (1, 2), (0, 2)], &[(0, 1, 2)], unit_weights(3)).unwrap();

        assert_eq!(cx.c0_dim, 3);
        assert_eq!(cx.c1_dim, 3);
        assert_eq!(cx.c2_dim, 1);
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
        assert_eq!(result, Err(CarrierError::CochainRelationViolated));
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

        assert_eq!(m1.carrier_hash, m2.carrier_hash);
        assert_eq!(m1.dim_q1, 1);
        assert_eq!(m1.dim_h1, 1);
    }

    #[test]
    fn different_carriers_different_hashes() {
        let cx1 = graph_carrier(3, &[(0, 1), (1, 2), (0, 2)], &[], unit_weights(3)).unwrap();
        let cx2 = graph_carrier(3, &[(0, 1), (1, 2)], &[], unit_weights(2)).unwrap();

        let m1 = CarrierManifest::from_carrier(&cx1);
        let m2 = CarrierManifest::from_carrier(&cx2);

        assert_ne!(m1.carrier_hash, m2.carrier_hash);
    }

    #[test]
    fn matrix_kernel_basis() {
        let cx = graph_carrier(3, &[(0, 1), (1, 2), (0, 2)], &[], unit_weights(3)).unwrap();
        let ker = cx.d0.try_transpose().unwrap().kernel_basis().unwrap();
        assert_eq!(ker.len(), 1);
    }
}
