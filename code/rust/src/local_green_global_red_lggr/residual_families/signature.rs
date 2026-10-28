
use std::fmt;

use blake3::Hasher;
use linear_algebra::backend::basic_matrix::CheckedNumeric;
use tfqm_functional::gamma2::ExactCochainComplexQ;
use engine_homology::cochain_primitive_difference::CochainPrimitiveDifference;
use engine_homology::quotient::{QuotientRelation, QuotientSpace};
use serde::Serialize;

#[derive(Copy, Clone, Debug, Eq, Hash, PartialEq)]
pub struct ShapeSignature([u8; 32]);

impl ShapeSignature {
    #[must_use]
    pub fn from_bytes(bytes: [u8; 32]) -> Self {
        Self(bytes)
    }

    #[must_use]
    pub fn as_bytes(&self) -> &[u8; 32] {
        &self.0
    }
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub enum ShapeSignatureError {
    EmptyNamespace,
}

impl fmt::Display for ShapeSignatureError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::EmptyNamespace => f.write_str("shape-signature namespace must be nonempty"),
        }
    }
}

impl std::error::Error for ShapeSignatureError {}

fn cochain_shape_fingerprint(c0: usize, c1: usize, c2: usize) -> Vec<u8> {
    let mut out = Vec::with_capacity(128);
    out.extend_from_slice(b"engine_homology::CochainPrimitiveDifference::shape_fingerprint::v1");
    out.extend_from_slice(&(c0 as u64).to_le_bytes());
    out.extend_from_slice(&(c1 as u64).to_le_bytes());
    out.extend_from_slice(&(c2 as u64).to_le_bytes());
    out.extend_from_slice(&(c1 as u64).to_le_bytes());
    out.extend_from_slice(&(c0 as u64).to_le_bytes());
    out.extend_from_slice(&(c2 as u64).to_le_bytes());
    out.extend_from_slice(&(c1 as u64).to_le_bytes());
    out.extend_from_slice(b"coeff:Q");
    out
}

#[allow(clippy::too_many_arguments)]
fn signature_from_parts(
    fingerprint: &[u8],
    cochain_dims: (usize, usize, usize),
    quotient_space_id: &[u8; 32],
    coefficient_domain: &str,
    dim_total: usize,
    degree: usize,
    relation: &QuotientRelation,
    projection_shape: (usize, usize),
) -> ShapeSignature {
    let mut hasher = Hasher::new();
    hasher.update(b"omega_residual_families::shape_signature::v1");
    hasher.update(fingerprint);

    let (c0, c1, c2) = cochain_dims;
    hasher.update(b"arity");
    hasher.update(&(c0 as u64).to_le_bytes());
    hasher.update(&(c1 as u64).to_le_bytes());
    hasher.update(&(c2 as u64).to_le_bytes());

    hasher.update(b"qspace");
    hasher.update(quotient_space_id);
    hasher.update(coefficient_domain.as_bytes());
    hasher.update(&(dim_total as u64).to_le_bytes());
    hasher.update(&(degree as u64).to_le_bytes());
    let relation_bytes = serde_json::to_vec(relation)
        .expect("serde_json::to_vec on QuotientRelation (total serde derive)");
    hasher.update(&(relation_bytes.len() as u64).to_le_bytes());
    hasher.update(&relation_bytes);
    let (p_rows, p_cols) = projection_shape;
    hasher.update(&(p_rows as u64).to_le_bytes());
    hasher.update(&(p_cols as u64).to_le_bytes());

    ShapeSignature(*hasher.finalize().as_bytes())
}

pub fn shape_signature_from_exact_complex(
    namespace: &str,
    complex: &ExactCochainComplexQ,
) -> Result<ShapeSignature, ShapeSignatureError> {
    if namespace.trim().is_empty() {
        return Err(ShapeSignatureError::EmptyNamespace);
    }

    let mut quotient_hasher = Hasher::new();
    quotient_hasher.update(b"omega_residual_families::exact_quotient_space_id::v1");
    quotient_hasher.update(&(namespace.len() as u64).to_le_bytes());
    quotient_hasher.update(namespace.as_bytes());
    let quotient_space_id = *quotient_hasher.finalize().as_bytes();
    let dims = (complex.c0_dim(), complex.c1_dim(), complex.c2_dim());
    let fingerprint = cochain_shape_fingerprint(dims.0, dims.1, dims.2);

    Ok(signature_from_parts(
        &fingerprint,
        dims,
        &quotient_space_id,
        "Q",
        complex.c1_dim(),
        1,
        &QuotientRelation::ModCoboundaries,
        (complex.c1_dim(), complex.c1_dim()),
    ))
}

#[must_use]
pub fn shape_signature<K>(
    diff: &CochainPrimitiveDifference<'_>,
    q: &QuotientSpace<K>,
) -> ShapeSignature
where
    K: CheckedNumeric + PartialEq + Serialize,
{
    signature_from_parts(
        &diff.shape_fingerprint(),
        diff.cochain_dims(),
        q.complex_hash.0.as_bytes(),
        q.coefficient_domain.as_str(),
        q.dim_total,
        q.degree,
        &q.relation,
        q.projection_matrix.shape(),
    )
}

#[cfg(test)]
mod tests {
    use super::*;
    use linear_algebra::backend::basic_matrix::BasicMatrix;
    use num_bigint::BigInt;
    use num_rational::{BigRational, Rational64};
    use engine_homology::cochain_complex::{CochainComplex, TheoremProvenance};
    use engine_homology::coefficient_domain::CoefficientDomain;
    use engine_homology::hash::{Blake3Hash, ComplexHash};
    use engine_homology::quotient::{QuotientRelation, QuotientSpace};

    type Q = engine_homology::scalar::Q;

    fn r(n: i64) -> Q {
        engine_homology::scalar::q(n)
    }

    fn br(n: i64) -> BigRational {
        BigRational::from_integer(BigInt::from(n))
    }

    fn path_complex() -> CochainComplex {
        let d0 = BasicMatrix::from_row_major(2, 1, vec![r(1), r(-1)]).expect("d0");
        let d1 = BasicMatrix::from_row_major(1, 2, vec![r(1), r(1)]).expect("d1");
        CochainComplex::new(
            1,
            2,
            1,
            d0,
            d1,
            TheoremProvenance::new("signature_test".to_string()).expect("prov"),
        )
        .expect("complex")
    }

    fn fixture_qspace() -> QuotientSpace<Q> {
        QuotientSpace::new_unchecked(
            ComplexHash(Blake3Hash::new(b"fixture-complex")),
            CoefficientDomain::Rational,
            2,
            1,
            QuotientRelation::ModCoboundaries,
            BasicMatrix::from_row_major(2, 2, vec![r(1), r(0), r(0), r(1)]).expect("proj"),
        )
    }

    #[test]
    fn same_input_same_digest() {
        let cc = path_complex();
        let pd = CochainPrimitiveDifference::new(&cc);
        let q = fixture_qspace();
        let a = shape_signature(&pd, &q);
        let b = shape_signature(&pd, &q);
        assert_eq!(
            a, b,
            "two calls on the same input must produce byte-identical digests"
        );
        assert_eq!(a.as_bytes(), b.as_bytes());
    }

    #[test]
    fn exact_complex_signature_is_value_free_and_namespaced() {
        let a = ExactCochainComplexQ::try_new(
            1,
            2,
            1,
            vec![vec![br(1)], vec![br(-1)]],
            vec![vec![br(1), br(1)]],
        )
        .expect("complex a");
        let b = ExactCochainComplexQ::try_new(
            1,
            2,
            1,
            vec![vec![br(2)], vec![br(-2)]],
            vec![vec![br(3), br(3)]],
        )
        .expect("complex b");

        let a_sig = shape_signature_from_exact_complex("domain-a", &a).expect("signature a");
        let b_sig = shape_signature_from_exact_complex("domain-a", &b).expect("signature b");
        let other = shape_signature_from_exact_complex("domain-b", &a).expect("other domain");

        assert_eq!(
            a_sig, b_sig,
            "coefficient changes are outside the shape key"
        );
        assert_ne!(a_sig, other, "domain namespaces must not alias");
        assert_eq!(
            shape_signature_from_exact_complex("", &a),
            Err(ShapeSignatureError::EmptyNamespace)
        );
    }
}
