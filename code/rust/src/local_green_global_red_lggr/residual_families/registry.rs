//! `FamilyRegistry` — in-memory shape-keyed lookup table.
//!
//! The $d_0$ gauge surface (packet §3): `lookup` and `record`. Storage is
//! private — a `HashMap<ShapeSignature, ResidualClassRecord>`. Diagnostic-only,
//! mints no authority.

use std::collections::HashMap;

use crate::residual_families::record::{Gamma2ClassId, Q1ClassId, ResidualClassRecord};
use crate::residual_families::signature::ShapeSignature;

/// Outcome of a [`FamilyRegistry::record`] call.
#[derive(Copy, Clone, Debug, Eq, PartialEq)]
#[must_use = "a Hit{collision:true} is a d_1 single-valuedness violation the caller must surface"]
pub enum RegistryWrite {
    /// A new shape key — record inserted.
    Inserted,
    /// The shape key already existed — `hits` was incremented.
    ///
    /// `collision = true` iff the prior `(q1_class_id, gamma2_class_id)` pair
    /// differs from the just-submitted pair; that indicates a $d_1$
    /// single-valuedness violation that the caller MUST surface.
    Hit { collision: bool },
}

/// Result of consulting a shape key before class ids are derived.
///
/// The fields are private so a caller cannot fabricate a pre-replay lookup.
#[derive(Copy, Clone, Debug, Eq, PartialEq)]
pub struct FamilyConsultation {
    signature: ShapeSignature,
    prior: Option<ResidualClassRecord>,
}

impl FamilyConsultation {
    /// Shape key that was consulted.
    #[must_use]
    pub fn signature(&self) -> ShapeSignature {
        self.signature
    }

    /// Snapshot of the prior record, when the lookup hit.
    #[must_use]
    pub fn prior(&self) -> Option<ResidualClassRecord> {
        self.prior
    }

    /// Whether the lookup hit before exact class-id derivation.
    #[must_use]
    pub fn was_hit(&self) -> bool {
        self.prior.is_some()
    }
}

/// In-memory shape-keyed registry of residual-class records.
#[derive(Default, Debug)]
pub struct FamilyRegistry {
    table: HashMap<ShapeSignature, ResidualClassRecord>,
}

impl FamilyRegistry {
    /// Construct an empty registry.
    #[must_use]
    pub fn new() -> Self {
        Self {
            table: HashMap::new(),
        }
    }

    /// Look up a previously recorded class by its shape signature.
    #[must_use]
    pub fn lookup(&self, sig: &ShapeSignature) -> Option<&ResidualClassRecord> {
        self.table.get(sig)
    }

    /// Consult a shape before exact Phi1/Gamma2 class ids are derived.
    ///
    /// A hit is diagnostic reuse only. Callers must still replay the current
    /// exact evidence and reconcile it through `wire::reconcile_verified`.
    #[must_use]
    pub fn consult(&self, signature: ShapeSignature) -> FamilyConsultation {
        FamilyConsultation {
            signature,
            prior: self.lookup(&signature).copied(),
        }
    }

    /// Record a `(q1_class_id, gamma2_class_id)` against a shape signature.
    ///
    /// - On a new key, inserts a fresh `ResidualClassRecord` with `hits = 1`
    ///   and returns [`RegistryWrite::Inserted`].
    /// - On an existing key, bumps `hits` and returns
    ///   [`RegistryWrite::Hit { collision }`] where
    ///   `collision = (existing.q1_class_id, existing.gamma2_class_id) != (q1, g2)`.
    pub fn record(
        &mut self,
        sig: ShapeSignature,
        q1: Q1ClassId,
        g2: Gamma2ClassId,
    ) -> RegistryWrite {
        match self.table.get_mut(&sig) {
            Some(existing) => {
                let collision = (existing.q1_class_id, existing.gamma2_class_id) != (q1, g2);
                existing.hits = existing.hits.saturating_add(1);
                RegistryWrite::Hit { collision }
            }
            None => {
                self.table
                    .insert(sig, ResidualClassRecord::new(sig, q1, g2));
                RegistryWrite::Inserted
            }
        }
    }

    /// Number of distinct shape keys currently in the registry.
    #[must_use]
    pub fn len(&self) -> usize {
        self.table.len()
    }

    /// `true` iff the registry is empty.
    #[must_use]
    pub fn is_empty(&self) -> bool {
        self.table.is_empty()
    }

    /// Iterate over the stored records. Used by [`crate::residual_families::recurrence::registry_hit_recurrence`].
    pub fn iter_records(&self) -> impl Iterator<Item = &ResidualClassRecord> {
        self.table.values()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::residual_families::signature::ShapeSignature;

    #[test]
    fn lookup_is_single_valued() {
        let mut reg = FamilyRegistry::new();
        let sig = ShapeSignature::from_bytes([42u8; 32]);
        let q1 = Q1ClassId::from_u64(1);
        let g2 = Gamma2ClassId::from_u64(2);

        // First record: Inserted.
        assert_eq!(reg.record(sig, q1, g2), RegistryWrite::Inserted);

        // Same shape + same (q1, g2): Hit { collision: false }. Hits = 2.
        assert_eq!(
            reg.record(sig, q1, g2),
            RegistryWrite::Hit { collision: false }
        );

        // Lookup is single-valued: returns the original (q1, g2).
        let rec = reg.lookup(&sig).expect("lookup must hit");
        assert_eq!(rec.q1_class_id, q1);
        assert_eq!(rec.gamma2_class_id, g2);
        assert_eq!(rec.hits, 2);

        // Different (q1, g2) under the same shape: Hit { collision: true }, hits = 3.
        // (d_1 single-valuedness violation surfaced to the caller; the registry does
        // NOT silently overwrite — the prior record stays put.)
        let q1_other = Q1ClassId::from_u64(99);
        assert_eq!(
            reg.record(sig, q1_other, g2),
            RegistryWrite::Hit { collision: true }
        );
        let rec_after = reg.lookup(&sig).expect("lookup must still hit");
        assert_eq!(
            rec_after.q1_class_id, q1,
            "registry must not silently overwrite"
        );
        assert_eq!(rec_after.gamma2_class_id, g2);
        assert_eq!(rec_after.hits, 3);
    }

    #[test]
    fn lookup_miss_returns_none() {
        let reg = FamilyRegistry::new();
        let sig = ShapeSignature::from_bytes([0u8; 32]);
        assert!(reg.lookup(&sig).is_none());
    }
}
