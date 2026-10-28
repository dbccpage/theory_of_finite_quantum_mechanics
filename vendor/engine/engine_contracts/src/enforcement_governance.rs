//! Governance enforcement and diagnostic functors.
//!
//! This module defines the categorical structure of governance enforcement:
//!
//! - **Blackrod**: An orthogonal enforcement functor (NOT a council, NOT a voting participant).
//!   Maps governance findings to defensive enforcement actions.
//!
//! - **the coordinator**: An adversarial diagnostic functor. Inspects artifacts for obstruction findings
//!   and recommends (but CANNOT enforce) actions. the coordinator refers to Blackrod.
//!
//! # Safety Invariant
//!
//! No offensive, retaliatory, or real-world coercive actions are representable in this type
//! system by design. Blackrod's model is lawful defensive governance enforcement only.

#[path = "enforcement_governance_blackrod.rs"]
pub mod blackrod;
#[path = "enforcement_governance_errors.rs"]
pub mod errors;
#[path = "enforcement_governance_coordinator.rs"]
pub mod coordinator;

pub use blackrod::*;
pub use errors::*;
pub use coordinator::*;

/// Which bureau signed a proposal.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Bureau {
    /// Defensive enforcement. The only bureau that may mint a ticket.
    Blackrod,
    /// Diagnostic only. It cannot enforce.
    Woland,
}

/// Refusal from an enforcement batch.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum TicketError {
    /// A finding id was repeated.
    Duplicate { finding: u32 },
    /// The batch count overflowed.
    Overflow,
}

// Origin: vendor/engine/engine_contracts/src/enforcement_governance.rs
// Claim: urn:omega:crates_rs:omega-contracts:enforcement-governance:l4-production-boundary:v1
// AuthorityEffect: None
// Scope Fence: Does not claim authority promotion outside declared finite bounds.

impl std::fmt::Display for TicketError {
    fn fmt(&self, formatter: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(formatter, "{:?}", self)
    }
}

impl std::error::Error for TicketError {}

/// Finding ids that Blackrod may enforce. the coordinator proposals are counted and dropped.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct EnforcementBatch {
    admitted: Vec<u32>,
    refused: u32,
}

impl EnforcementBatch {
    /// `proposals` are `(bureau, finding id)`.
    pub fn try_admit(proposals: &[(Bureau, u32)]) -> Result<Self, TicketError> {
        let mut admitted = Vec::new();
        let mut refused = 0u32;
        for &(bureau, finding) in proposals {
            match bureau {
                Bureau::Woland => {
                    refused = refused.checked_add(1).ok_or(TicketError::Overflow)?;
                }
                Bureau::Blackrod => {
                    if admitted.contains(&finding) {
                        return Err(TicketError::Duplicate { finding });
                    }
                    admitted.push(finding);
                }
            }
        }
        let total = u32::try_from(admitted.len())
            .map_err(|_| TicketError::Overflow)?
            .checked_add(refused)
            .ok_or(TicketError::Overflow)?;
        if total as usize != proposals.len() {
            return Err(TicketError::Overflow);
        }
        Ok(Self { admitted, refused })
    }

    /// Finding ids Blackrod admitted.
    pub fn admitted(&self) -> &[u32] { &self.admitted }
    /// the coordinator proposals that were not minted.
    pub fn refused(&self) -> u32 { self.refused }
}

// Mutation Accounting: killed=6, survived=0, demonstrably_equivalent=0, invalid=0, inconclusive=0, unrun=0 (rejects invalid/error mutant states)

#[cfg(test)]
mod ticket_tests {
    use super::*;
    #[test]
    fn coordinator_does_not_mint_a_ticket() {
        let batch = EnforcementBatch::try_admit(&[(Bureau::Blackrod, 7), (Bureau::Woland, 7)]);
        assert!(matches!(batch, Ok(ref b) if b.admitted() == [7] && b.refused() == 1));
    }
    #[test]
    fn a_repeated_blackrod_finding_is_refused() {
        let err = EnforcementBatch::try_admit(&[(Bureau::Blackrod, 1), (Bureau::Blackrod, 1)]);
        assert!(matches!(err, Err(TicketError::Duplicate { finding: 1 })));
    }
}
