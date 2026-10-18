//! `ResidualClassRecord` + opaque local id newtypes.
//!
//! `Q1ClassId` and `Gamma2ClassId` are LOCAL ids only. They carry NO
//! authority. Product-local terminal stamping and checked-packet certification
//! are evidence-only; authority requires the separate authenticated host
//! promotion contract. This module has no dependency on those paths.

/// Local opaque id for a `Q^1` residual class.
///
/// Computed by [`crate::residual_families::wire::derive_q1_class_id`] as a deterministic
/// `blake3`-derived digest over the shape-relevant accessors of
/// `omega_functional::phi1::VerifiedExactPhi1` (specifically `.value()` and
/// `.d0()`; see S7b). NO authority — local registry id only.
///
/// # Collision bound
///
/// This id is the low 64 bits of a 256-bit `blake3` digest (see
/// [`crate::residual_families::wire::derive_q1_class_id`]). The birthday bound is therefore
/// `~2^32` distinct classes before a 50% chance of an accidental id collision.
/// At the registry's current scale this is comfortable; if the registry is
/// ever expected to hold `> 2^24` classes, widen this newtype to `u128` /
/// `[u8; 16]`.
#[derive(Copy, Clone, Debug, Eq, Hash, PartialEq)]
pub struct Q1ClassId(u64);

impl Q1ClassId {
    /// Construct from a raw `u64`. Test-and-fixture-only.
    #[must_use]
    pub fn from_u64(bits: u64) -> Self {
        Self(bits)
    }

    /// Borrow the underlying `u64`. For equality testing only; opaque elsewhere.
    #[must_use]
    pub fn as_u64(self) -> u64 {
        self.0
    }
}

/// Local opaque id for a `Gamma_2` closure-defect class.
///
/// Computed by [`crate::residual_families::wire::derive_gamma2_class_id`] as a deterministic
/// `blake3`-derived digest over the shape-relevant accessors of
/// `omega_functional::gamma2::ExactGamma2Result` (specifically `.value()` and
/// `.d0()`; see S7b). NO authority — local registry id only.
///
/// # Collision bound
///
/// Same 64-bit-truncation collision bound as [`Q1ClassId`]: the id is the low
/// 64 bits of a 256-bit `blake3` digest, so the birthday bound is `~2^32`
/// classes. Widen to `u128` / `[u8; 16]` if the registry is ever expected to
/// hold `> 2^24` classes.
#[derive(Copy, Clone, Debug, Eq, Hash, PartialEq)]
pub struct Gamma2ClassId(u64);

impl Gamma2ClassId {
    /// Construct from a raw `u64`. Test-and-fixture-only.
    #[must_use]
    pub fn from_u64(bits: u64) -> Self {
        Self(bits)
    }

    /// Borrow the underlying `u64`. For equality testing only; opaque elsewhere.
    #[must_use]
    pub fn as_u64(self) -> u64 {
        self.0
    }
}

/// One residual-class record: a hashed shape key plus the prior
/// `(q1_class_id, gamma2_class_id)` hit and a hit counter.
#[derive(Copy, Clone, Debug, Eq, PartialEq)]
pub struct ResidualClassRecord {
    pub signature: crate::residual_families::signature::ShapeSignature,
    pub q1_class_id: Q1ClassId,
    pub gamma2_class_id: Gamma2ClassId,
    pub hits: u64,
}

impl ResidualClassRecord {
    #[must_use]
    pub fn new(
        signature: crate::residual_families::signature::ShapeSignature,
        q1_class_id: Q1ClassId,
        gamma2_class_id: Gamma2ClassId,
    ) -> Self {
        Self {
            signature,
            q1_class_id,
            gamma2_class_id,
            hits: 1,
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::residual_families::signature::ShapeSignature;

    #[test]
    fn record_round_trip_fields() {
        let sig = ShapeSignature::from_bytes([7u8; 32]);
        let q1 = Q1ClassId::from_u64(0x1234_5678_9abc_def0);
        let g2 = Gamma2ClassId::from_u64(0x0fed_cba9_8765_4321);
        let rec = ResidualClassRecord::new(sig, q1, g2);
        assert_eq!(rec.signature, sig);
        assert_eq!(rec.q1_class_id, q1);
        assert_eq!(rec.gamma2_class_id, g2);
        assert_eq!(rec.hits, 1);
        assert_eq!(rec.q1_class_id.as_u64(), 0x1234_5678_9abc_def0);
        assert_eq!(rec.gamma2_class_id.as_u64(), 0x0fed_cba9_8765_4321);
    }
}
