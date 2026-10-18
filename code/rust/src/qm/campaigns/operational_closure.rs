//! Unresolved inventory of the original ten FQMC-1 clauses.
//! Candidate labels are not verified evidence. No launch-class binding or
//! dependency audit is implemented here. AuthorityEffect: None.

use serde::{Deserialize, Serialize};
use serde_json::json;

pub const FQMC1_CLAUSES: [&str; 10] = [
    "Finite carrier and scalar domain",
    "Normalized states, effects, and their probability pairing",
    "Transformations and measurement instruments",
    "Composition rule and subsystem interface",
    "Reversible and irreversible dynamics with explicit time semantics",
    "Contextual and multipartite correlation semantics",
    "Terminating algorithms for every computational claim",
    "Theorem, countermodel, or explicit OPEN status for every structural claim",
    "Named metric and error bound for every finite-to-infinite comparison",
    "Price/refusal ledger naming every imported structure",
];

pub const REFUSAL_IDS: [&str; 4] = [
    "REFUSAL-C500-01",
    "REFUSAL-C500-02",
    "REFUSAL-C500-03",
    "REFUSAL-C500-04",
];

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct Fqmc1ContractAudit {
    pub obligation_count: usize,
    pub untyped_internal_obligations: usize,
    pub open_internal_obligations: usize,
    pub terminal_outcome: String,
    pub refusal_count: usize,
    pub all_block_bets_scored: Option<bool>,
}

impl Fqmc1ContractAudit {
    /// Derive counts from this unresolved inventory. No clause is certified.
    pub fn evaluate() -> Self {
        Self {
            obligation_count: fqmc1_obligation_count(),
            untyped_internal_obligations: untyped_internal_obligation_count(),
            open_internal_obligations: open_internal_obligation_count(),
            terminal_outcome: terminal_outcome().to_string(),
            refusal_count: refusal_count(),
            all_block_bets_scored: all_block_bets_scored(),
        }
    }
}

pub fn fqmc1_obligation_count() -> usize {
    FQMC1_CLAUSES.len()
}

/// The launch-frozen class identity has not been established.
pub fn untyped_internal_obligation_count() -> usize {
    ["launch-frozen class identity"].len()
}

/// Every original clause needs a class-wide evidence audit.
pub fn open_internal_obligation_count() -> usize {
    FQMC1_CLAUSES.len()
}

/// Bookkeeping rule conditional on independently audited counts.
pub fn decide_terminal(untyped: usize, open: usize, global_refusal: bool) -> &'static str {
    if global_refusal {
        "FQMC1_REFUSED_AS_GLOBAL_FINITE_REPLACEMENT"
    } else if untyped > 0 || open > 0 {
        "FQMC1_OPEN_INTERNAL_GAPS"
    } else {
        "FQMC1_CLOSED_AT_DECLARED_CLASS"
    }
}

pub fn terminal_outcome() -> &'static str {
    decide_terminal(
        untyped_internal_obligation_count(),
        open_internal_obligation_count(),
        false,
    )
}

pub fn refusal_count() -> usize {
    REFUSAL_IDS.len()
}

/// This kernel does not parse or adjudicate the block scores.
pub fn all_block_bets_scored() -> Option<bool> {
    None
}

pub fn generate_canonical_block10_rust_receipt() -> serde_json::Value {
    let audit = Fqmc1ContractAudit::evaluate();
    json!({
        "campaign": "C500",
        "block": "block_10",
        "authority_effect": "None",
        "terminal_outcome": audit.terminal_outcome,
        "fqmc1_obligation_count": audit.obligation_count,
        "untyped_internal_obligation_count": audit.untyped_internal_obligations,
        "open_internal_obligation_count": audit.open_internal_obligations,
        "refusal_count": audit.refusal_count,
        "all_block_bets_scored": audit.all_block_bets_scored,
        "class_binding_status": "NOT_ESTABLISHED",
        "clause_names": FQMC1_CLAUSES,
        "clause_status": "OPEN_UNVERIFIED",
        "status": "OPEN_EVIDENCE_AUDIT"
    })
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn unresolved_class_and_clauses_cannot_close() {
        let audit = Fqmc1ContractAudit::evaluate();
        assert_eq!(audit.obligation_count, 10);
        assert_eq!(audit.untyped_internal_obligations, 1);
        assert_eq!(audit.open_internal_obligations, 10);
        assert_eq!(audit.terminal_outcome, "FQMC1_OPEN_INTERNAL_GAPS");
        assert_eq!(audit.all_block_bets_scored, None);
        assert_eq!(refusal_count(), 4);
    }

    #[test]
    fn terminal_rule_distinguishes_unknown_from_global_refusal() {
        assert_eq!(decide_terminal(1, 0, false), "FQMC1_OPEN_INTERNAL_GAPS");
        assert_eq!(decide_terminal(0, 1, false), "FQMC1_OPEN_INTERNAL_GAPS");
        assert_eq!(
            decide_terminal(0, 0, false),
            "FQMC1_CLOSED_AT_DECLARED_CLASS"
        );
        assert_eq!(
            decide_terminal(0, 0, true),
            "FQMC1_REFUSED_AS_GLOBAL_FINITE_REPLACEMENT"
        );
    }

    #[test]
    fn receipt_preserves_unknown_score_status() {
        let receipt = generate_canonical_block10_rust_receipt();
        assert_eq!(receipt["status"], "OPEN_EVIDENCE_AUDIT");
        assert!(receipt["all_block_bets_scored"].is_null());
        assert_eq!(
            receipt["clause_names"][6],
            "Terminating algorithms for every computational claim"
        );
    }
}
