
#[derive(Copy, Clone, Debug, Eq, Hash, PartialEq)]
pub struct Q1ClassId(u64);

impl Q1ClassId {
    #[must_use]
    pub fn from_u64(bits: u64) -> Self {
        Self(bits)
    }

    #[must_use]
    pub fn as_u64(self) -> u64 {
        self.0
    }
}

#[derive(Copy, Clone, Debug, Eq, Hash, PartialEq)]
pub struct Gamma2ClassId(u64);

impl Gamma2ClassId {
    #[must_use]
    pub fn from_u64(bits: u64) -> Self {
        Self(bits)
    }

    #[must_use]
    pub fn as_u64(self) -> u64 {
        self.0
    }
}

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
