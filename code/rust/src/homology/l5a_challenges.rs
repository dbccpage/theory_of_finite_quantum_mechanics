//! Independent fixtures and adversarial certificate challenges. AuthorityEffect: None.

use super::*;
use crate::linear_algebra::basic_matrix::BasicMatrix;
use crate::linear_algebra::scalars::{q, qr};
use chain::Chain;
use cochain::Cochain;
use cochain_complex::{CochainComplex, TheoremProvenance};
use ids::{BasisId, Degree};
use rank_certificate::{certify_rank, RankCertificate};
use simplicial::{OrientedSimplex, Simplex, SimplicialComplex};

fn basis(name: &str) -> BasisId {
    BasisId::new(name).unwrap()
}
fn provenance() -> TheoremProvenance {
    TheoremProvenance::new("independent fixtures".into()).unwrap()
}
fn matrix(rows: usize, cols: usize, entries: &[i64]) -> BasicMatrix<Q> {
    BasicMatrix::from_row_major(rows, cols, entries.iter().map(|n| q(*n)).collect()).unwrap()
}

#[test]
fn arithmetic_binds_basis_degree_and_vector_kind() {
    let a = Chain::new(Degree(1), basis("a"), vec![q(1)]).unwrap();
    let b = Chain::new(Degree(1), basis("b"), vec![q(1)]).unwrap();
    let c = Chain::new(Degree(2), basis("a"), vec![q(1)]).unwrap();
    let dual = Cochain::new(Degree(1), basis("a"), vec![q(1)]).unwrap();
    assert!(matches!(
        a.add(&b),
        Err(HomologicalError::BasisMismatch { .. })
    ));
    assert!(matches!(
        a.sub(&b),
        Err(HomologicalError::BasisMismatch { .. })
    ));
    assert!(a.add(&c).is_err());
    assert_ne!(a.hash(), b.hash());
    assert_ne!(a.hash(), c.hash());
    assert_ne!(a.hash(), dual.hash());
    let x = Cochain::new(Degree(1), basis("b"), vec![q(1)]).unwrap();
    assert!(dual.add(&x).is_err());
    assert!(dual.sub(&x).is_err());
}

#[test]
fn map_admission_and_application_reject_wrong_degrees() {
    use boundary::BoundaryMap;
    use coboundary::CoboundaryMap;
    assert!(BoundaryMap::new(Degree(0), Degree(1), matrix(1, 1, &[1])).is_err());
    assert!(CoboundaryMap::new(Degree(i32::MAX), Degree(0), matrix(1, 1, &[1])).is_err());
    assert!(BoundaryMap::new(Degree(i32::MIN), Degree(0), matrix(1, 1, &[1])).is_err());
    let down = BoundaryMap::new(Degree(1), Degree(0), matrix(1, 1, &[1])).unwrap();
    let up = CoboundaryMap::new(Degree(0), Degree(1), matrix(1, 1, &[1])).unwrap();
    let chain = Chain::new(Degree(0), basis("x"), vec![q(1)]).unwrap();
    let cochain = Cochain::new(Degree(1), basis("x"), vec![q(1)]).unwrap();
    assert!(down.apply(&chain).is_err());
    assert!(up.apply(&cochain).is_err());
}

#[test]
fn unchecked_rationals_and_impossible_allocation_are_refused() {
    let undefined = Q::new_raw(1.into(), 0.into());
    let unreduced = Q::new_raw(2.into(), 4.into());
    for value in [undefined, unreduced] {
        assert!(Chain::new(Degree(0), basis("x"), vec![value.clone()]).is_err());
        let raw = BasicMatrix::from_row_major(1, 1, vec![value.clone()]).unwrap();
        assert!(certify_rank(&raw).is_err());
        let chain = Chain::new(Degree(0), basis("x"), vec![q(1)]).unwrap();
        assert!(chain.scalar_mul(&value).is_err());
    }
    assert!(Chain::zero(Degree(0), basis("x"), usize::MAX).is_err());
    let empty = matrix(0, 0, &[]);
    assert!(
        chain_complex::ChainComplex::new(usize::MAX, 2, 0, empty.clone(), empty.clone()).is_err()
    );
    assert!(CochainComplex::new(usize::MAX, 2, 0, empty.clone(), empty, provenance()).is_err());
}

#[test]
fn serde_cannot_bypass_identifier_provenance_or_simplex_admission() {
    assert!(serde_json::from_str::<ids::ChainId>("0").is_err());
    assert!(serde_json::from_str::<BasisId>("\"  \"").is_err());
    assert!(serde_json::from_str::<TheoremProvenance>("\"\"").is_err());
    for wire in [
        r#"{"vertices":[]}"#,
        r#"{"vertices":[1,1]}"#,
        r#"{"vertices":[2,1]}"#,
    ] {
        assert!(serde_json::from_str::<Simplex>(wire).is_err());
    }
    assert!(serde_json::from_str::<OrientedSimplex>(
        r#"{"simplex":{"vertices":[0,1]},"orientation":0}"#
    )
    .is_err());
}

#[test]
fn serialized_carrier_is_revalidated_and_hash_bound() {
    let carrier = Carrier::new(
        1,
        1,
        1,
        ExactMatrix(matrix(1, 1, &[0])),
        ExactMatrix(matrix(1, 1, &[0])),
        vec![q(1)],
    )
    .unwrap();
    let wire = serde_json::to_value(&carrier).unwrap();
    let roundtrip: Carrier = serde_json::from_value(wire.clone()).unwrap();
    assert_eq!(carrier, roundtrip);
    let mut forged = wire.clone();
    forged["c1_dim"] = 2.into();
    assert!(serde_json::from_value::<Carrier>(forged).is_err());
    let mut forged = wire.clone();
    forged["weights"] = serde_json::to_value(vec![q(0)]).unwrap();
    assert!(serde_json::from_value::<Carrier>(forged).is_err());
    let mut forged = wire;
    forged["d0_hash"] = serde_json::to_value(Hash256([0; 32])).unwrap();
    assert!(serde_json::from_value::<Carrier>(forged).is_err());
}

#[test]
fn graph_constructor_rejects_each_invalid_incidence_class() {
    use exact_carrier::graph_carrier;
    assert!(graph_carrier(1, &[(0, 0)], &[], vec![q(1)]).is_err());
    assert!(graph_carrier(2, &[(2, 1)], &[], vec![q(1)]).is_err());
    assert!(graph_carrier(2, &[(0, 2)], &[], vec![q(1)]).is_err());
    assert!(graph_carrier(2, &[(0, 1), (0, 1)], &[], vec![q(1); 2]).is_err());
    assert!(graph_carrier(3, &[], &[(0, 1, 2)], vec![]).is_err());
    assert!(graph_carrier(3, &[], &[(0, 1, 3)], vec![]).is_err());
    assert!(graph_carrier(3, &[], &[(0, 0, 1)], vec![]).is_err());
    assert!(graph_carrier(2, &[(0, 1)], &[], vec![]).is_err());
    assert!(graph_carrier(2, &[(0, 1)], &[], vec![q(-1)]).is_err());
}

#[test]
fn rank_certificates_reject_independently_forged_identities_and_binding() {
    let m = matrix(2, 3, &[1, 2, 3, 2, 4, 6]);
    let receipt = certify_rank(&m).unwrap();
    assert_eq!(receipt.rank(), 1);
    receipt.verify_against(&m).unwrap();
    let candidate = receipt.candidate().clone();
    // All split identities still hold for this candidate; only M=UV can reject
    // binding a nonzero factorization to the zero matrix.
    assert!(RankCertificate::try_admit(&matrix(2, 3, &[0; 6]), candidate.clone()).is_err());
    let mut bad = candidate.clone();
    bad.image.set(0, 0, q(0)).unwrap();
    assert!(RankCertificate::try_admit(&m, bad).is_err());
    let mut bad = candidate.clone();
    bad.image_retraction = BasicMatrix::zero(1, 2).unwrap();
    assert!(RankCertificate::try_admit(&m, bad).is_err());
    let mut bad = candidate.clone();
    bad.coordinate_section = BasicMatrix::zero(3, 1).unwrap();
    assert!(RankCertificate::try_admit(&m, bad).is_err());
    let mut bad = candidate;
    bad.coordinates = BasicMatrix::zero(2, 3).unwrap();
    assert!(RankCertificate::try_admit(&m, bad).is_err());
    assert!(receipt.verify_against(&matrix(2, 3, &[0; 6])).is_err());
}

#[test]
fn rank_inequality_does_not_replace_the_coboundary_law() {
    // rank(d0)+rank(d1)=2=dim(C1), yet d1*d0=[1], so the law fails.
    let d0 = matrix(2, 1, &[1, 0]);
    let d1 = matrix(1, 2, &[1, 0]);
    assert!(matches!(
        carrier::Carrier::new(1, 2, 1, d0, d1, vec![q(1); 2], provenance()),
        Err(HomologicalError::CoboundaryLawViolation { .. })
    ));
}

#[test]
fn exact_rank_fixture_exceeds_fixed_width_and_covers_empty_shapes() {
    let big = num_bigint::BigInt::from(1) << 200usize;
    let m = BasicMatrix::from_row_major(2, 2, vec![Q::from_integer(big), qr(1, 3), q(0), qr(2, 7)])
        .unwrap();
    assert_eq!(certify_rank(&m).unwrap().rank(), 2);
    for (r, c) in [(0, 0), (0, 3), (3, 0), (2, 3)] {
        assert_eq!(
            certify_rank(&BasicMatrix::zero(r, c).unwrap())
                .unwrap()
                .rank(),
            0
        );
    }
}

#[test]
fn all_two_by_two_ternary_matrix_ranks_match_determinant_oracle() {
    for code in 0..81usize {
        let a = (code % 3) as i64 - 1;
        let b = ((code / 3) % 3) as i64 - 1;
        let c = ((code / 9) % 3) as i64 - 1;
        let d = ((code / 27) % 3) as i64 - 1;
        let expected = if a * d - b * c != 0 {
            2
        } else {
            usize::from([a, b, c, d] != [0; 4])
        };
        assert_eq!(
            certify_rank(&matrix(2, 2, &[a, b, c, d])).unwrap().rank(),
            expected
        );
    }
}

#[test]
fn graph_betti_numbers_match_combinatorial_component_oracle() {
    // Every labelled simple graph on four vertices; H1=E-V+components.
    let possible = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)];
    for bits in 0..64 {
        let edges: Vec<_> = possible
            .iter()
            .enumerate()
            .filter(|(i, _)| bits & (1 << i) != 0)
            .map(|(_, e)| *e)
            .collect();
        let mut labels = [0, 1, 2, 3];
        for &(a, b) in &edges {
            let from = labels[b];
            let to = labels[a];
            for label in &mut labels {
                if *label == from {
                    *label = to;
                }
            }
        }
        let components = labels
            .into_iter()
            .collect::<std::collections::BTreeSet<_>>()
            .len();
        let c = exact_carrier::graph_carrier(4, &edges, &[], vec![q(1); edges.len()]).unwrap();
        assert_eq!(c.dim_h1(), edges.len() + components - 4);
        assert!(carrier_manifest::CarrierManifest::from_carrier(&c).verifies(c.as_ref()));
    }
}

#[test]
fn simplicial_limits_roundtrip_and_known_topology() {
    assert!(SimplicialComplex::standard_n_simplex(usize::MAX).is_err());
    assert!(
        SimplicialComplex::from_simplices(vec![Simplex::new(vec![usize::MAX]).unwrap()]).is_err()
    );
    let disk = SimplicialComplex::standard_n_simplex(2).unwrap();
    assert!(disk.coboundary_matrix(usize::MAX).is_err());
    assert_eq!(disk.rational_betti_numbers().unwrap(), vec![1, 0, 0]);
    let wire = serde_json::to_string(&disk).unwrap();
    assert_eq!(
        serde_json::from_str::<SimplicialComplex>(&wire).unwrap(),
        disk
    );
    // Boundary of the tetrahedron is S2: independently known Betti vector.
    let facets = [vec![0, 1, 2], vec![0, 1, 3], vec![0, 2, 3], vec![1, 2, 3]];
    let sphere = SimplicialComplex::from_simplices(
        facets
            .into_iter()
            .map(|v| Simplex::new(v).unwrap())
            .collect(),
    )
    .unwrap();
    assert_eq!(sphere.rational_betti_numbers().unwrap(), vec![1, 0, 1]);
    assert_eq!(sphere.euler_characteristic(), 2);
}
