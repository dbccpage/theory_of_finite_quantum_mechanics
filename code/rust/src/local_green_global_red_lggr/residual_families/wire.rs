
use std::fmt;

use omega_linear_algebra::backend::basic_matrix::CheckedNumeric;
use omega_functional::gamma2::ExactGamma2Result;
use omega_functional::phi1::VerifiedExactPhi1;
use omega_homology::cochain_primitive_difference::CochainPrimitiveDifference;
use omega_homology::quotient::QuotientSpace;
use omega_types::observer::Observer;
use serde::Serialize;

use crate::residual_families::record::{Gamma2ClassId, Q1ClassId};
use crate::residual_families::registry::{FamilyConsultation, FamilyRegistry, RegistryWrite};
use crate::residual_families::signature::shape_signature;

fn truncate_to_u64(digest: &blake3::Hash) -> u64 {
    let bytes = digest.as_bytes();
    let mut buf = [0u8; 8];
    buf.copy_from_slice(&bytes[..8]);
    u64::from_le_bytes(buf)
}

#[must_use]
pub fn derive_q1_class_id(phi1: &VerifiedExactPhi1) -> Q1ClassId {
    let mut hasher = blake3::Hasher::new();
    hasher.update(b"omega_residual_families::derive_q1_class_id::v1");

    let value_bytes = serde_json::to_vec(phi1.value())
        .expect("serde_json::to_vec on VerifiedExactPhi1::value (BigRational total serde)");
    hasher.update(b"phi1.value");
    hasher.update(&(value_bytes.len() as u64).to_le_bytes());
    hasher.update(&value_bytes);

    let d0_bytes = serde_json::to_vec(phi1.d0())
        .expect("serde_json::to_vec on VerifiedExactPhi1::d0 (Vec<Vec<BigRational>> total serde)");
    hasher.update(b"phi1.d0");
    hasher.update(&(d0_bytes.len() as u64).to_le_bytes());
    hasher.update(&d0_bytes);

    let digest = hasher.finalize();
    Q1ClassId::from_u64(truncate_to_u64(&digest))
}

#[must_use]
pub fn derive_gamma2_class_id(gamma2: &ExactGamma2Result) -> Gamma2ClassId {
    let mut hasher = blake3::Hasher::new();
    hasher.update(b"omega_residual_families::derive_gamma2_class_id::v1");

    let value_bytes = serde_json::to_vec(gamma2.value())
        .expect("serde_json::to_vec on ExactGamma2Result::value (BigRational total serde)");
    hasher.update(b"gamma2.value");
    hasher.update(&(value_bytes.len() as u64).to_le_bytes());
    hasher.update(&value_bytes);

    let d0_bytes = serde_json::to_vec(gamma2.d0())
        .expect("serde_json::to_vec on ExactGamma2Result::d0 (Vec<Vec<BigRational>> total serde)");
    hasher.update(b"gamma2.d0");
    hasher.update(&(d0_bytes.len() as u64).to_le_bytes());
    hasher.update(&d0_bytes);

    let digest = hasher.finalize();
    Gamma2ClassId::from_u64(truncate_to_u64(&digest))
}

#[derive(Copy, Clone, Debug, Eq, PartialEq)]
pub struct FamilyResolution {
    signature: crate::residual_families::signature::ShapeSignature,
    q1_class_id: Q1ClassId,
    gamma2_class_id: Gamma2ClassId,
    lookup_hit: bool,
    write: RegistryWrite,
}

impl FamilyResolution {
    #[must_use]
    pub fn signature(&self) -> crate::residual_families::signature::ShapeSignature {
        self.signature
    }

    #[must_use]
    pub fn q1_class_id(&self) -> Q1ClassId {
        self.q1_class_id
    }

    #[must_use]
    pub fn gamma2_class_id(&self) -> Gamma2ClassId {
        self.gamma2_class_id
    }

    #[must_use]
    pub fn lookup_hit(&self) -> bool {
        self.lookup_hit
    }

    pub fn registry_write(&self) -> RegistryWrite {
        self.write
    }
}

#[derive(Copy, Clone, Debug, Eq, PartialEq)]
pub struct FamilyCollision {
    pub signature: crate::residual_families::signature::ShapeSignature,
    pub prior_q1_class_id: Q1ClassId,
    pub prior_gamma2_class_id: Gamma2ClassId,
    pub observed_q1_class_id: Q1ClassId,
    pub observed_gamma2_class_id: Gamma2ClassId,
}

impl fmt::Display for FamilyCollision {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.write_str("residual-family shape mapped to a different exact Phi1/Gamma2 class")
    }
}

impl std::error::Error for FamilyCollision {}

pub fn reconcile_verified(
    reg: &mut FamilyRegistry,
    consultation: FamilyConsultation,
    phi1: &VerifiedExactPhi1,
    gamma2: &ExactGamma2Result,
    observer: &Observer,
) -> Result<FamilyResolution, FamilyCollision> {
    let _ = (&observer.id, &observer.kind);
    let signature = consultation.signature();
    let lookup_hit = consultation.was_hit();
    let q1 = derive_q1_class_id(phi1);
    let g2 = derive_gamma2_class_id(gamma2);
    let write = reg.record(signature, q1, g2);

    if write == (RegistryWrite::Hit { collision: true }) {
        let prior = reg
            .lookup(&signature)
            .expect("collision implies an existing registry record");
        return Err(FamilyCollision {
            signature,
            prior_q1_class_id: prior.q1_class_id,
            prior_gamma2_class_id: prior.gamma2_class_id,
            observed_q1_class_id: q1,
            observed_gamma2_class_id: g2,
        });
    }

    Ok(FamilyResolution {
        signature,
        q1_class_id: q1,
        gamma2_class_id: g2,
        lookup_hit,
        write,
    })
}

pub fn record_from_verified<K>(
    reg: &mut FamilyRegistry,
    diff: &CochainPrimitiveDifference<'_>,
    q: &QuotientSpace<K>,
    phi1: &VerifiedExactPhi1,
    gamma2: &ExactGamma2Result,
    observer: &Observer,
) -> RegistryWrite
where
    K: CheckedNumeric + PartialEq + Serialize,
{
    let _ = (&observer.id, &observer.kind);

    let sig = shape_signature(diff, q);
    let q1 = derive_q1_class_id(phi1);
    let g2 = derive_gamma2_class_id(gamma2);
    reg.record(sig, q1, g2)
}
