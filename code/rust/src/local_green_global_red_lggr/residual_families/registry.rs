
use std::collections::HashMap;

use crate::residual_families::record::{Gamma2ClassId, Q1ClassId, ResidualClassRecord};
use crate::residual_families::signature::ShapeSignature;

#[derive(Copy, Clone, Debug, Eq, PartialEq)]
#[must_use = "a Hit{collision:true} is a d_1 single-valuedness violation the caller must surface"]
pub enum RegistryWrite {
    Inserted,
    Hit { collision: bool },
}

#[derive(Copy, Clone, Debug, Eq, PartialEq)]
pub struct FamilyConsultation {
    signature: ShapeSignature,
    prior: Option<ResidualClassRecord>,
}

impl FamilyConsultation {
    #[must_use]
    pub fn signature(&self) -> ShapeSignature {
        self.signature
    }

    #[must_use]
    pub fn prior(&self) -> Option<ResidualClassRecord> {
        self.prior
    }

    #[must_use]
    pub fn was_hit(&self) -> bool {
        self.prior.is_some()
    }
}

#[derive(Default, Debug)]
pub struct FamilyRegistry {
    table: HashMap<ShapeSignature, ResidualClassRecord>,
}

impl FamilyRegistry {
    #[must_use]
    pub fn new() -> Self {
        Self {
            table: HashMap::new(),
        }
    }

    #[must_use]
    pub fn lookup(&self, sig: &ShapeSignature) -> Option<&ResidualClassRecord> {
        self.table.get(sig)
    }

    #[must_use]
    pub fn consult(&self, signature: ShapeSignature) -> FamilyConsultation {
        FamilyConsultation {
            signature,
            prior: self.lookup(&signature).copied(),
        }
    }

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

    #[must_use]
    pub fn len(&self) -> usize {
        self.table.len()
    }

    #[must_use]
    pub fn is_empty(&self) -> bool {
        self.table.is_empty()
    }

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

        assert_eq!(reg.record(sig, q1, g2), RegistryWrite::Inserted);

        assert_eq!(
            reg.record(sig, q1, g2),
            RegistryWrite::Hit { collision: false }
        );

        let rec = reg.lookup(&sig).expect("lookup must hit");
        assert_eq!(rec.q1_class_id, q1);
        assert_eq!(rec.gamma2_class_id, g2);
        assert_eq!(rec.hits, 2);

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
