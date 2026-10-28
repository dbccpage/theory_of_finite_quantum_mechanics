
use crate::prime_algos::prime_scope::{digest, ScopeBinding};
use engine_kernel::evidence::Hash256;
use engine_types::authority::AuthorityEffect;
use serde::Serialize;
use std::collections::BTreeMap;
use std::fmt;

const LEDGER_DOMAIN: &str = "oeprm.ledger.v1";

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct LossLedger {
    scope: ScopeBinding,
    entries: BTreeMap<String, usize>,
    sound: bool,
}

impl LossLedger {
    pub fn empty(scope: ScopeBinding) -> Self {
        Self {
            scope,
            entries: BTreeMap::new(),
            sound: true,
        }
    }

    pub fn booked(entries: Vec<(String, usize)>, scope: ScopeBinding) -> Self {
        let sound = entries.iter().all(|(k, n)| *n > 0 && !k.trim().is_empty());
        Self {
            scope,
            entries: entries.into_iter().collect(),
            sound,
        }
    }

    pub fn scope(&self) -> &ScopeBinding {
        &self.scope
    }

    pub fn is_sound(&self) -> bool {
        self.sound
    }

    pub fn is_empty(&self) -> bool {
        self.entries.is_empty()
    }

    pub fn total_lost(&self) -> usize {
        self.entries.values().sum()
    }

    pub fn entries(&self) -> &BTreeMap<String, usize> {
        &self.entries
    }

    pub fn commit(&self) -> Hash256 {
        let mut parts: Vec<Vec<u8>> = Vec::new();
        parts.push(self.scope.commit().0.to_vec());
        for (k, n) in &self.entries {
            parts.push(k.as_bytes().to_vec());
            parts.push((*n as u64).to_le_bytes().to_vec());
        }
        parts.push(vec![u8::from(self.sound)]);
        let refs: Vec<&[u8]> = parts.iter().map(|p| p.as_slice()).collect();
        digest(LEDGER_DOMAIN, &refs)
    }
}

impl fmt::Display for LossLedger {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        if self.entries.is_empty() {
            return write!(f, "L_adapter: nothing lost (claimed)");
        }
        write!(
            f,
            "L_adapter: {} item(s), {} total [{}]",
            self.entries.len(),
            self.total_lost(),
            self.entries
                .iter()
                .map(|(k, n)| format!("{k}={n}"))
                .collect::<Vec<_>>()
                .join(", ")
        )
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize)]
#[serde(rename_all = "snake_case")]
pub enum TransportStatus {
    Proposed,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub enum TransportRefusal {
    UnsoundLedger { detail: String },
    SameCarrier,
}

impl fmt::Display for TransportRefusal {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            TransportRefusal::UnsoundLedger { detail } => {
                write!(f, "transport refused: unsound loss ledger: {detail}")
            }
            TransportRefusal::SameCarrier => {
                write!(
                    f,
                    "transport refused: source and target carrier are identical"
                )
            }
        }
    }
}

impl std::error::Error for TransportRefusal {}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct TransportedPacket {
    from: Hash256,
    to: Hash256,
    payload: Hash256,
    ledger: LossLedger,
    status: TransportStatus,
}

impl TransportedPacket {
    pub fn from_carrier(&self) -> &Hash256 {
        &self.from
    }
    pub fn to_carrier(&self) -> &Hash256 {
        &self.to
    }
    pub fn payload(&self) -> &Hash256 {
        &self.payload
    }
    pub fn ledger(&self) -> &LossLedger {
        &self.ledger
    }
    pub fn status(&self) -> TransportStatus {
        self.status
    }
}

pub fn transport(
    from: Hash256,
    to: Hash256,
    payload: Hash256,
    ledger: LossLedger,
    _source_was_admitted: bool,
) -> Result<TransportedPacket, TransportRefusal> {
    if from == to {
        return Err(TransportRefusal::SameCarrier);
    }
    if ledger.scope().carrier() != &from {
        return Err(TransportRefusal::UnsoundLedger {
            detail: format!(
                "ledger bound to carrier {} does not match transport source {}",
                crate::prime_algos::prime_scope::short(ledger.scope().carrier()),
                crate::prime_algos::prime_scope::short(&from),
            ),
        });
    }
    if !ledger.is_sound() {
        return Err(TransportRefusal::UnsoundLedger {
            detail: ledger.to_string(),
        });
    }
    Ok(TransportedPacket {
        from,
        to,
        payload,
        ledger,
        status: TransportStatus::Proposed,
    })
}

pub const AUTHORITY_EFFECT: AuthorityEffect = AuthorityEffect::None;

#[cfg(test)]
mod tests {
    use super::*;

    fn h(n: u8) -> Hash256 {
        Hash256([n; 32])
    }

    fn test_scope(carrier: Hash256) -> ScopeBinding {
        ScopeBinding::with_carrier_and_d0(h(0), carrier, h(100), h(200), None, 0)
    }

    #[test]
    fn translation_does_not_confer_validity() {
        let p = transport(h(1), h(2), h(9), LossLedger::empty(test_scope(h(1))), true)
            .expect("a sound transport must succeed");
        assert_eq!(
            p.status(),
            TransportStatus::Proposed,
            "an admitted packet must arrive as a proposal"
        );
    }

    #[test]
    fn transport_succeeds_for_both_source_statuses_and_upgrades_neither() {
        for was_admitted in [true, false] {
            let p = transport(
                h(1),
                h(2),
                h(9),
                LossLedger::empty(test_scope(h(1))),
                was_admitted,
            )
            .unwrap();
            assert_eq!(p.status(), TransportStatus::Proposed);
        }
    }

    #[test]
    fn an_unsound_ledger_refuses() {
        let bad = LossLedger::booked(vec![("dropped".into(), 0)], test_scope(h(1)));
        assert!(!bad.is_sound(), "a zero-count entry is unsound");
        let err = transport(h(1), h(2), h(9), bad, false).expect_err("must refuse");
        assert!(matches!(err, TransportRefusal::UnsoundLedger { .. }));
    }

    #[test]
    fn a_blank_loss_key_is_unsound() {
        assert!(!LossLedger::booked(vec![("   ".into(), 3)], test_scope(h(1))).is_sound());
    }

    #[test]
    fn transport_to_the_same_carrier_refuses() {
        let err =
            transport(h(1), h(1), h(9), LossLedger::empty(test_scope(h(1))), false).unwrap_err();
        assert_eq!(err, TransportRefusal::SameCarrier);
    }

    #[test]
    fn transport_with_mismatched_ledger_carrier_refuses() {
        let err = transport(
            h(1),
            h(2),
            h(9),
            LossLedger::empty(test_scope(h(99))),
            false,
        )
        .unwrap_err();
        assert!(matches!(err, TransportRefusal::UnsoundLedger { .. }));
    }

    #[test]
    fn an_empty_ledger_is_a_claim_not_an_absence() {
        let l = LossLedger::empty(test_scope(h(1)));
        assert!(l.is_empty());
        assert!(l.is_sound());
        assert_eq!(l.total_lost(), 0);
    }

    #[test]
    fn a_booked_ledger_reports_its_total() {
        let l = LossLedger::booked(
            vec![("faces".into(), 2), ("orientations".into(), 5)],
            test_scope(h(1)),
        );
        assert!(l.is_sound());
        assert!(!l.is_empty());
        assert_eq!(l.total_lost(), 7);
    }

    #[test]
    fn distinct_ledgers_commit_distinctly() {
        let a = LossLedger::booked(vec![("faces".into(), 2)], test_scope(h(1)));
        let b = LossLedger::booked(vec![("faces".into(), 3)], test_scope(h(1)));
        let c = LossLedger::booked(vec![("edges".into(), 2)], test_scope(h(1)));
        assert_ne!(a.commit(), b.commit(), "count must be committed");
        assert_ne!(a.commit(), c.commit(), "key must be committed");
        assert_ne!(a.commit(), LossLedger::empty(test_scope(h(1))).commit());
        assert_eq!(
            a.commit(),
            LossLedger::booked(vec![("faces".into(), 2)], test_scope(h(1))).commit()
        );
    }

    #[test]
    fn soundness_is_committed() {
        let sound = LossLedger::empty(test_scope(h(1)));
        let unsound = LossLedger::booked(vec![("x".into(), 0)], test_scope(h(1)));
        assert_ne!(sound.commit(), unsound.commit());
    }

    #[test]
    fn display_never_panics_on_hostile_keys() {
        let l = LossLedger::booked(vec![("\u{1F600}\u{00E9}".into(), 1)], test_scope(h(1)));
        assert!(!l.to_string().is_empty());
    }

    #[test]
    fn authority_effect_is_none() {
        assert_eq!(AUTHORITY_EFFECT, AuthorityEffect::None);
    }
}
