
use linear_algebra::backend::basic_matrix::BasicMatrix;
use num_bigint::BigInt;
use num_rational::BigRational;
use num_traits::Zero;
use engine_homology::carrier::Carrier;
use engine_homology::carrier_manifest::CarrierManifest;
use engine_homology::cochain_complex::TheoremProvenance;
use engine_homology::errors::HomologicalError;

use crate::solver_of_solvers::{d1_rows_for_binding, FiniteCarrier2};

const BINDING_PROVENANCE: &str =
    "crate::carrier_binding (d0/d1 derived from FiniteCarrier2)";

#[derive(Debug, thiserror::Error)]
pub enum CarrierBindingError {
    #[error("edge {index} weight {weight} is not strictly positive")]
    WeightNotPositive { index: usize, weight: i128 },

    #[error("edge {index} endpoints ({tail}, {head}) exceed vertex count {num_vertices}")]
    EndpointOutOfRange {
        index: usize,
        tail: usize,
        head: usize,
        num_vertices: usize,
    },

    #[error("d1 derivation failed: {0}")]
    D1Derivation(String),

    #[error("matrix construction failed: {0}")]
    Matrix(String),

    #[error(transparent)]
    Homology(#[from] HomologicalError),
}

fn q(value: i64) -> BigRational {
    BigRational::from_integer(BigInt::from(value))
}

fn d0_matrix(carrier: &FiniteCarrier2) -> Result<BasicMatrix<BigRational>, CarrierBindingError> {
    let rows = carrier.edges.len();
    let cols = carrier.num_vertices;
    let mut data = vec![BigRational::zero(); rows * cols];
    for (index, edge) in carrier.edges.iter().enumerate() {
        if edge.tail >= cols || edge.head >= cols {
            return Err(CarrierBindingError::EndpointOutOfRange {
                index,
                tail: edge.tail,
                head: edge.head,
                num_vertices: cols,
            });
        }
        data[index * cols + edge.tail] = q(-1);
        data[index * cols + edge.head] = q(1);
    }
    BasicMatrix::from_row_major(rows, cols, data)
        .map_err(|error| CarrierBindingError::Matrix(format!("{error:?}")))
}

fn d1_matrix(carrier: &FiniteCarrier2) -> Result<BasicMatrix<BigRational>, CarrierBindingError> {
    let rows = d1_rows_for_binding(carrier)
        .map_err(|error| CarrierBindingError::D1Derivation(error.to_string()))?;
    let height = rows.len();
    let width = carrier.edges.len();
    let mut data = Vec::with_capacity(height * width);
    for row in &rows {
        if row.len() != width {
            return Err(CarrierBindingError::Matrix(format!(
                "d1 row has {} entries, expected {width}",
                row.len()
            )));
        }
        data.extend(row.iter().cloned());
    }
    BasicMatrix::from_row_major(height, width, data)
        .map_err(|error| CarrierBindingError::Matrix(format!("{error:?}")))
}

fn weights(carrier: &FiniteCarrier2) -> Result<Vec<BigRational>, CarrierBindingError> {
    carrier
        .edges
        .iter()
        .enumerate()
        .map(|(index, edge)| {
            if edge.weight <= 0 {
                return Err(CarrierBindingError::WeightNotPositive {
                    index,
                    weight: edge.weight,
                });
            }
            Ok(BigRational::from_integer(BigInt::from(edge.weight)))
        })
        .collect()
}

pub fn to_homology_carrier(carrier: &FiniteCarrier2) -> Result<Carrier, CarrierBindingError> {
    let d0 = d0_matrix(carrier)?;
    let d1 = d1_matrix(carrier)?;
    let w = weights(carrier)?;
    let provenance = TheoremProvenance::new(BINDING_PROVENANCE.to_string())?;
    Ok(Carrier::new(
        carrier.num_vertices,
        carrier.edges.len(),
        carrier.faces.len(),
        d0,
        d1,
        w,
        provenance,
    )?)
}

pub fn carrier_manifest(carrier: &FiniteCarrier2) -> Result<CarrierManifest, CarrierBindingError> {
    Ok(to_homology_carrier(carrier)?.manifest()?)
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct IsingCycleGradientRepair;

impl IsingCycleGradientRepair {
    pub fn compute_repair_differential(ring_size: usize, cochain: &[BigRational]) -> Vec<BigRational> {
        assert!(ring_size > 0, "Ring size must be positive");
        assert_eq!(cochain.len(), ring_size, "Cochain length must match ring size");
        let n_rat = BigRational::from_integer(BigInt::from(ring_size));
        let sum: BigRational = cochain.iter().cloned().sum();
        let mean = sum / n_rat;
        cochain.iter().map(|c| c - &mean).collect()
    }

    pub fn condition_number(_ring_size: usize) -> BigRational {
        num_traits::One::one()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::solver_of_solvers::CarrierEdge;

    fn edge(tail: usize, head: usize, weight: i128) -> CarrierEdge {
        CarrierEdge { tail, head, weight }
    }

    fn triangle() -> FiniteCarrier2 {
        FiniteCarrier2 {
            num_vertices: 3,
            edges: vec![edge(0, 1, 1), edge(1, 2, 1), edge(2, 0, 1)],
            faces: vec![(0, 1, 2)],
        }
    }

    fn open_triangle() -> FiniteCarrier2 {
        FiniteCarrier2 {
            faces: vec![],
            ..triangle()
        }
    }

    #[test]
    fn triangle_binds_and_d1_d0_is_zero() {
        let carrier = to_homology_carrier(&triangle()).expect("triangle must bind");
        assert_eq!(carrier.c0_dim(), 3);
        assert_eq!(carrier.c1_dim(), 3);
        assert_eq!(carrier.c2_dim(), 1);
    }

    #[test]
    fn manifest_is_stable_for_the_same_declaration() {
        let a = carrier_manifest(&triangle()).expect("bind");
        let b = carrier_manifest(&triangle()).expect("bind");
        assert_eq!(a, b, "the same declaration must hash identically");
    }

    #[test]
    fn manifest_differs_when_the_face_is_removed() {
        let closed = to_homology_carrier(&triangle()).expect("bind");
        let open = to_homology_carrier(&open_triangle()).expect("bind");
        assert_ne!(
            closed.manifest().expect("manifest"),
            open.manifest().expect("manifest"),
            "declaring a 2-cell must change carrier identity"
        );
        assert_eq!(open.dim_h1().expect("b1"), 1, "open triangle has b1 = 1");
        assert_eq!(
            closed.dim_h1().expect("b1"),
            0,
            "filled triangle has b1 = 0"
        );
    }

    #[test]
    fn manifest_differs_when_only_edge_weights_differ() {
        let mut heavy = triangle();
        heavy.edges[0].weight = 7;
        assert_ne!(
            carrier_manifest(&triangle()).expect("bind"),
            carrier_manifest(&heavy).expect("bind"),
        );
    }

    #[test]
    fn very_large_weight_binds_exactly() {
        let mut c = triangle();
        c.edges[0].weight = i128::MAX;
        let big = carrier_manifest(&c).expect("i128::MAX weight must bind exactly");
        assert_ne!(big, carrier_manifest(&triangle()).expect("bind"));
    }

    #[test]
    fn nonpositive_weight_is_refused() {
        let mut c = triangle();
        c.edges[1].weight = 0;
        match to_homology_carrier(&c) {
            Err(CarrierBindingError::WeightNotPositive { index, .. }) => assert_eq!(index, 1),
            other => panic!("expected a refusal, got {other:?}"),
        }
    }

    #[test]
    fn endpoint_out_of_range_is_refused() {
        let c = FiniteCarrier2 {
            num_vertices: 2,
            edges: vec![edge(0, 1, 1), edge(1, 5, 1)],
            faces: vec![],
        };
        assert!(matches!(
            to_homology_carrier(&c),
            Err(CarrierBindingError::EndpointOutOfRange { index: 1, .. })
        ));
    }

    #[test]
    fn face_whose_side_is_not_declared_is_refused() {
        let c = FiniteCarrier2 {
            num_vertices: 4,
            edges: vec![edge(0, 1, 1), edge(1, 2, 1), edge(2, 0, 1)],
            faces: vec![(0, 1, 3)],
        };
        assert!(matches!(
            to_homology_carrier(&c),
            Err(CarrierBindingError::D1Derivation(_))
        ));
    }

    #[test]
    fn reversed_edge_orientation_still_forms_a_complex() {
        let c = FiniteCarrier2 {
            num_vertices: 3,
            edges: vec![edge(0, 1, 1), edge(1, 2, 1), edge(0, 2, 1)],
            faces: vec![(0, 1, 2)],
        };
        let carrier = to_homology_carrier(&c).expect("reversed storage must still bind");
        assert_eq!(
            carrier.dim_h1().expect("b1"),
            0,
            "the declared face still kills the cycle"
        );
    }

    #[test]
    fn edge_declaration_order_changes_identity() {
        let mut reordered = triangle();
        reordered.edges.swap(0, 2);
        reordered.faces = vec![(0, 1, 2)];
        assert_ne!(
            carrier_manifest(&triangle()).expect("bind"),
            carrier_manifest(&reordered).expect("bind"),
        );
    }
}
