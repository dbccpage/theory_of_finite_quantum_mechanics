//! Canonical routing axis for the Omega Engine.
//!
//! The routing axis is a closed set: `CheckPassed`, `RequiresLift`, `Repair`,
//! `Refusal`, `NoRule`, `BudgetUnknown`, `Refused`.
//! It is disjoint from the diagnostic classes.
//!
//! AuthorityEffect: None.

use serde::{Deserialize, Serialize};

use crate::terminal_status::TerminalStatus;

/// The seven canonical routing terminal values.
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash, Serialize, Deserialize)]
pub enum RoutingTerminal {
    CheckPassed,
    RequiresLift,
    Repair,
    Refusal,
    NoRule,
    BudgetUnknown,
    Refused,
}

impl From<TerminalStatus> for RoutingTerminal {
    fn from(status: TerminalStatus) -> Self {
        match status {
            TerminalStatus::ExactRuleDerived => RoutingTerminal::CheckPassed,
            TerminalStatus::UniqueOutputDerived => RoutingTerminal::CheckPassed,
            TerminalStatus::NoRuleInSearchClass => RoutingTerminal::NoRule,
            TerminalStatus::NonUniqueOutput => RoutingTerminal::Repair,
            TerminalStatus::EnumeratorFailure => RoutingTerminal::Repair,
            TerminalStatus::Refused => RoutingTerminal::Refused,
            TerminalStatus::LabelConflictsWithDerivation => RoutingTerminal::Refused,
            TerminalStatus::BudgetUnknown => RoutingTerminal::BudgetUnknown,
            TerminalStatus::InvalidProposal => RoutingTerminal::Refused,
            TerminalStatus::OperatorConflict => RoutingTerminal::Refused,
            TerminalStatus::UnknownSector => RoutingTerminal::Repair,
            TerminalStatus::NoDescentYet => RoutingTerminal::Repair,
            TerminalStatus::LabelOnlyUncertified => RoutingTerminal::Repair,
            TerminalStatus::LiftRequired => RoutingTerminal::RequiresLift,
            TerminalStatus::ParseRefused => RoutingTerminal::Refusal,
            TerminalStatus::ReplayMismatch => RoutingTerminal::Repair,
            TerminalStatus::PolicyAmbiguous => RoutingTerminal::Repair,
            TerminalStatus::NoPacket => RoutingTerminal::Refusal,
            TerminalStatus::VerifierDisabled => RoutingTerminal::Repair,
            TerminalStatus::SearchIncomplete => RoutingTerminal::Repair,
            TerminalStatus::PolicyUnderspecified => RoutingTerminal::Repair,
        }
    }
}

/// The PFP terminal statuses (`omega_engine_pfp.domain.kernel.result.TerminalStatus`).
///
/// Each one routes to exactly one `RoutingTerminal`. The same map is data in
/// `omega_engine_pfp/infrastructure/yaml/stages/terminal_routing.json`, and the
/// test below checks the two agree. `BudgetExhausted` routes to `BudgetUnknown`.
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash, Serialize, Deserialize)]
pub enum PfpTerminal {
    Exact,
    Verified,
    VerifiedWithResiduals,
    StabilizedSurvivor,
    NeedsExternalOracle,
    OpenObstruction,
    BlockedByEvidence,
    InfrastructureFailure,
    Refused,
    BudgetExhausted,
}

impl PfpTerminal {
    pub const ALL: [PfpTerminal; 10] = [
        PfpTerminal::Exact,
        PfpTerminal::Verified,
        PfpTerminal::VerifiedWithResiduals,
        PfpTerminal::StabilizedSurvivor,
        PfpTerminal::NeedsExternalOracle,
        PfpTerminal::OpenObstruction,
        PfpTerminal::BlockedByEvidence,
        PfpTerminal::InfrastructureFailure,
        PfpTerminal::Refused,
        PfpTerminal::BudgetExhausted,
    ];
}

impl From<PfpTerminal> for RoutingTerminal {
    fn from(status: PfpTerminal) -> Self {
        match status {
            PfpTerminal::Exact | PfpTerminal::Verified | PfpTerminal::VerifiedWithResiduals => {
                RoutingTerminal::CheckPassed
            }
            PfpTerminal::StabilizedSurvivor | PfpTerminal::NeedsExternalOracle => {
                RoutingTerminal::RequiresLift
            }
            PfpTerminal::OpenObstruction
            | PfpTerminal::BlockedByEvidence
            | PfpTerminal::InfrastructureFailure => RoutingTerminal::Refusal,
            PfpTerminal::Refused => RoutingTerminal::Refused,
            PfpTerminal::BudgetExhausted => RoutingTerminal::BudgetUnknown,
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_all_seven_routing_terminals_are_reachable() {
        assert_eq!(
            RoutingTerminal::from(TerminalStatus::ExactRuleDerived),
            RoutingTerminal::CheckPassed
        );
        assert_eq!(
            RoutingTerminal::from(TerminalStatus::LiftRequired),
            RoutingTerminal::RequiresLift
        );
        assert_eq!(
            RoutingTerminal::from(TerminalStatus::NonUniqueOutput),
            RoutingTerminal::Repair
        );
        assert_eq!(
            RoutingTerminal::from(TerminalStatus::ParseRefused),
            RoutingTerminal::Refusal
        );
        assert_eq!(
            RoutingTerminal::from(TerminalStatus::NoRuleInSearchClass),
            RoutingTerminal::NoRule
        );
        assert_eq!(
            RoutingTerminal::from(TerminalStatus::BudgetUnknown),
            RoutingTerminal::BudgetUnknown
        );
        assert_eq!(
            RoutingTerminal::from(TerminalStatus::Refused),
            RoutingTerminal::Refused
        );
    }

    #[test]
    fn test_pfp_terminal_routing_matches_the_shared_data_file() {
        let text = include_str!(
            "../../../../omega_engine_pfp/infrastructure/yaml/stages/terminal_routing.json"
        );
        let data: serde_json::Value = serde_json::from_str(text).expect("valid JSON");
        let routing = data["routing"].as_object().expect("routing object");
        assert_eq!(routing.len(), PfpTerminal::ALL.len());
        for status in PfpTerminal::ALL {
            let key = serde_json::to_value(status).expect("serialize");
            let expected = serde_json::to_value(RoutingTerminal::from(status)).expect("serialize");
            assert_eq!(routing[key.as_str().expect("string")], expected, "{status:?}");
        }
    }
}
