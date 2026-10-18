
use std::collections::BTreeMap;

use serde::{Deserialize, Serialize};

pub const BRIDGE_PACKET_14_FIELD_COUNT: usize = 14;

pub const BRIDGE_PACKET_14_FIELD_NAMES: [&str; BRIDGE_PACKET_14_FIELD_COUNT] = [
    "Lambda",
    "A_lambda",
    "F_lambda_mu",
    "chi_lambda_mu",
    "L",
    "eta",
    "X_space",
    "pi_lambda",
    "q",
    "Prof",
    "q_bar",
    "D",
    "V",
    "tau",
];

pub type DomainId = u32;

pub type ProfileId = u32;

pub type QueryValue = u32;

#[derive(Clone, Debug, Default, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub struct SchemaSlot {
    pub name: String,
    pub declared: bool,
}

impl SchemaSlot {
    pub fn unbound(name: impl Into<String>) -> Self {
        Self {
            name: name.into(),
            declared: false,
        }
    }

    pub fn declared(name: impl Into<String>) -> Self {
        Self {
            name: name.into(),
            declared: true,
        }
    }

    pub fn is_declared(&self) -> bool {
        self.declared && !self.name.trim().is_empty()
    }
}

#[derive(Clone, Debug, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct FiniteQueryMap {
    pub domain: Vec<DomainId>,
    pub values: BTreeMap<DomainId, QueryValue>,
}

impl FiniteQueryMap {
    pub fn new(domain: Vec<DomainId>, values: BTreeMap<DomainId, QueryValue>) -> Self {
        Self { domain, values }
    }

    pub fn from_pairs(pairs: impl IntoIterator<Item = (DomainId, QueryValue)>) -> Self {
        let values: BTreeMap<DomainId, QueryValue> = pairs.into_iter().collect();
        let domain: Vec<DomainId> = values.keys().copied().collect();
        Self { domain, values }
    }

    pub fn get(&self, x: DomainId) -> Option<QueryValue> {
        self.values.get(&x).copied()
    }

    pub fn covers_domain(&self) -> bool {
        !self.domain.is_empty() && self.domain.iter().all(|x| self.values.contains_key(x))
    }
}

#[derive(Clone, Debug, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct FiniteProfileMap {
    pub domain: Vec<DomainId>,
    pub values: BTreeMap<DomainId, ProfileId>,
}

impl FiniteProfileMap {
    pub fn new(domain: Vec<DomainId>, values: BTreeMap<DomainId, ProfileId>) -> Self {
        Self { domain, values }
    }

    pub fn from_pairs(pairs: impl IntoIterator<Item = (DomainId, ProfileId)>) -> Self {
        let values: BTreeMap<DomainId, ProfileId> = pairs.into_iter().collect();
        let domain: Vec<DomainId> = values.keys().copied().collect();
        Self { domain, values }
    }

    pub fn get(&self, x: DomainId) -> Option<ProfileId> {
        self.values.get(&x).copied()
    }

    pub fn covers_domain(&self) -> bool {
        !self.domain.is_empty() && self.domain.iter().all(|x| self.values.contains_key(x))
    }
}

#[derive(Clone, Debug, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct FiniteFactorMap {
    pub values: BTreeMap<ProfileId, QueryValue>,
}

impl FiniteFactorMap {
    pub fn new(values: BTreeMap<ProfileId, QueryValue>) -> Self {
        Self { values }
    }

    pub fn from_pairs(pairs: impl IntoIterator<Item = (ProfileId, QueryValue)>) -> Self {
        Self {
            values: pairs.into_iter().collect(),
        }
    }

    pub fn get(&self, b: ProfileId) -> Option<QueryValue> {
        self.values.get(&b).copied()
    }
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct BridgePacket14 {
    pub lambda: SchemaSlot,
    pub a_lambda: SchemaSlot,
    pub f_lambda_mu: SchemaSlot,
    pub chi_lambda_mu: SchemaSlot,
    pub l: SchemaSlot,
    pub eta: SchemaSlot,
    pub x_space: SchemaSlot,
    pub pi_lambda: SchemaSlot,
    pub q: FiniteQueryMap,
    pub prof: FiniteProfileMap,
    pub q_bar: FiniteFactorMap,
    pub d: SchemaSlot,
    pub v: SchemaSlot,
    pub tau: SchemaSlot,
}

pub type CodaCsQBridgePacketV1 = BridgePacket14;

impl BridgePacket14 {
    pub const FIELD_COUNT: usize = BRIDGE_PACKET_14_FIELD_COUNT;

    pub fn finite_demo(q: FiniteQueryMap, prof: FiniteProfileMap, q_bar: FiniteFactorMap) -> Self {
        Self {
            lambda: SchemaSlot::declared("Lambda"),
            a_lambda: SchemaSlot::declared("A_lambda"),
            f_lambda_mu: SchemaSlot::declared("F_lambda_mu"),
            chi_lambda_mu: SchemaSlot::declared("chi_lambda_mu"),
            l: SchemaSlot::declared("L"),
            eta: SchemaSlot::declared("eta"),
            x_space: SchemaSlot::declared("X_space"),
            pi_lambda: SchemaSlot::declared("pi_lambda"),
            q,
            prof,
            q_bar,
            d: SchemaSlot::declared("D"),
            v: SchemaSlot::declared("V"),
            tau: SchemaSlot::declared("tau"),
        }
    }

    pub fn field_count() -> usize {
        Self::FIELD_COUNT
    }

    pub fn field_names() -> &'static [&'static str; BRIDGE_PACKET_14_FIELD_COUNT] {
        &BRIDGE_PACKET_14_FIELD_NAMES
    }

    pub fn sample_domain(&self) -> Vec<DomainId> {
        if self.q.domain.is_empty() {
            return self.prof.domain.clone();
        }
        if self.prof.domain.is_empty() {
            return self.q.domain.clone();
        }
        self.q
            .domain
            .iter()
            .copied()
            .filter(|x| self.prof.values.contains_key(x))
            .collect()
    }

    pub fn authority_effect(&self) -> &'static str {
        "None"
    }

    pub fn finite_maps_cover_domain(&self) -> bool {
        self.q.covers_domain() && self.prof.covers_domain()
    }
}

pub fn profile_factorization_holds(packet: &BridgePacket14) -> Result<(), FactorizationDefect> {
    let domain = packet.sample_domain();
    if domain.is_empty() {
        return Err(FactorizationDefect::EmptyDomain);
    }
    for x in domain {
        let q_x = packet
            .q
            .get(x)
            .ok_or(FactorizationDefect::MissingQuery(x))?;
        let prof_x = packet
            .prof
            .get(x)
            .ok_or(FactorizationDefect::MissingProfile(x))?;
        let q_bar_px = packet
            .q_bar
            .get(prof_x)
            .ok_or(FactorizationDefect::MissingFactor(prof_x))?;
        if q_x != q_bar_px {
            return Err(FactorizationDefect::Mismatch {
                x,
                q_x,
                prof_x,
                q_bar_px,
            });
        }
    }
    Ok(())
}

pub fn fiber_constant_holds(packet: &BridgePacket14) -> Result<(), FiberConstancyDefect> {
    let domain = packet.sample_domain();
    for (i, &x) in domain.iter().enumerate() {
        for &y in domain.iter().skip(i + 1) {
            let px = packet
                .prof
                .get(x)
                .ok_or(FiberConstancyDefect::MissingProfile(x))?;
            let py = packet
                .prof
                .get(y)
                .ok_or(FiberConstancyDefect::MissingProfile(y))?;
            if px == py {
                let qx = packet
                    .q
                    .get(x)
                    .ok_or(FiberConstancyDefect::MissingQuery(x))?;
                let qy = packet
                    .q
                    .get(y)
                    .ok_or(FiberConstancyDefect::MissingQuery(y))?;
                if qx != qy {
                    return Err(FiberConstancyDefect::Mismatch { x, y, px, qx, qy });
                }
            }
        }
    }
    Ok(())
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub enum FactorizationDefect {
    EmptyDomain,
    MissingQuery(DomainId),
    MissingProfile(DomainId),
    MissingFactor(ProfileId),
    Mismatch {
        x: DomainId,
        q_x: QueryValue,
        prof_x: ProfileId,
        q_bar_px: QueryValue,
    },
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub enum FiberConstancyDefect {
    MissingQuery(DomainId),
    MissingProfile(DomainId),
    Mismatch {
        x: DomainId,
        y: DomainId,
        px: ProfileId,
        qx: QueryValue,
        qy: QueryValue,
    },
}

#[cfg(test)]
mod tests {
    use super::*;

    fn factoring_packet() -> BridgePacket14 {
        let q = FiniteQueryMap::from_pairs([(0, 10), (1, 10), (2, 20), (3, 20)]);
        let prof = FiniteProfileMap::from_pairs([(0, 0), (1, 0), (2, 1), (3, 1)]);
        let q_bar = FiniteFactorMap::from_pairs([(0, 10), (1, 20)]);
        BridgePacket14::finite_demo(q, prof, q_bar)
    }

    #[test]
    fn field_count_is_fourteen() {
        assert_eq!(BridgePacket14::field_count(), 14);
        assert_eq!(BRIDGE_PACKET_14_FIELD_COUNT, 14);
        assert_eq!(BRIDGE_PACKET_14_FIELD_NAMES.len(), 14);
        assert_eq!(CodaCsQBridgePacketV1::FIELD_COUNT, 14);
    }

    #[test]
    fn field_names_match_paper_tuple_order() {
        assert_eq!(
            BridgePacket14::field_names(),
            &[
                "Lambda",
                "A_lambda",
                "F_lambda_mu",
                "chi_lambda_mu",
                "L",
                "eta",
                "X_space",
                "pi_lambda",
                "q",
                "Prof",
                "q_bar",
                "D",
                "V",
                "tau",
            ]
        );
    }

    #[test]
    fn authority_effect_is_none() {
        let p = factoring_packet();
        assert_eq!(p.authority_effect(), "None");
    }

    #[test]
    fn profile_factorization_holds_on_factoring_demo() {
        assert!(profile_factorization_holds(&factoring_packet()).is_ok());
    }

    #[test]
    fn factorization_implies_fiber_constancy_on_demo() {
        let p = factoring_packet();
        assert!(profile_factorization_holds(&p).is_ok());
        assert!(fiber_constant_holds(&p).is_ok());
    }

    #[test]
    fn factorization_fails_on_mismatch() {
        let q = FiniteQueryMap::from_pairs([(0, 1), (1, 2)]);
        let prof = FiniteProfileMap::from_pairs([(0, 0), (1, 0)]);
        let q_bar = FiniteFactorMap::from_pairs([(0, 1)]);
        let p = BridgePacket14::finite_demo(q, prof, q_bar);
        assert!(matches!(
            profile_factorization_holds(&p),
            Err(FactorizationDefect::Mismatch { x: 1, .. })
        ));
    }

    #[test]
    fn empty_domain_fails_factorization_closed() {
        let p = BridgePacket14::finite_demo(
            FiniteQueryMap::default(),
            FiniteProfileMap::default(),
            FiniteFactorMap::default(),
        );
        assert_eq!(
            profile_factorization_holds(&p),
            Err(FactorizationDefect::EmptyDomain)
        );
    }
}
