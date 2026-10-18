
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ClaimStatus {
    ExactAlgebraicTheorem,
    ConditionalImplication,
    WitnessedConstructiveExistence,
    WitnessedCounterexample,
    StructuralAbsenceResult,
    FiniteExhaustiveVerification,
    ReplayCertifiedComputation,
    BoundedEmpiricalFinding,
    SimulationObservation,
    ProtocolReplayPass,
    Definition,
    Nonclaim,
    SynthesisConclusion,
    Interpretive,
    ConjectureFalsifiable,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Ch20Status {
    Proved,
    Refuted,
    Undetermined,
    OutsideProfile,
    Refused,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct TypedRefusal {
    pub code: &'static str,
    pub authority_effect: &'static str,
}

pub fn map_claim_status(status: ClaimStatus) -> Result<Ch20Status, TypedRefusal> {
    match status {
        ClaimStatus::ExactAlgebraicTheorem
        | ClaimStatus::WitnessedConstructiveExistence
        | ClaimStatus::FiniteExhaustiveVerification
        | ClaimStatus::ReplayCertifiedComputation
        | ClaimStatus::ProtocolReplayPass => Ok(Ch20Status::Proved),
        ClaimStatus::WitnessedCounterexample => Ok(Ch20Status::Refuted),
        ClaimStatus::BoundedEmpiricalFinding
        | ClaimStatus::SimulationObservation
        | ClaimStatus::ConjectureFalsifiable => Ok(Ch20Status::Undetermined),
        ClaimStatus::ConditionalImplication => Ok(Ch20Status::OutsideProfile),
        ClaimStatus::StructuralAbsenceResult => Ok(Ch20Status::Refused),
        ClaimStatus::Definition
        | ClaimStatus::Nonclaim
        | ClaimStatus::SynthesisConclusion
        | ClaimStatus::Interpretive => Err(TypedRefusal {
            code: "unmapped_claim_status",
            authority_effect: "None",
        }),
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn fifteen_statuses_partition_into_eleven_mapped_and_four_refused() {
        let all = [
            ClaimStatus::ExactAlgebraicTheorem,
            ClaimStatus::ConditionalImplication,
            ClaimStatus::WitnessedConstructiveExistence,
            ClaimStatus::WitnessedCounterexample,
            ClaimStatus::StructuralAbsenceResult,
            ClaimStatus::FiniteExhaustiveVerification,
            ClaimStatus::ReplayCertifiedComputation,
            ClaimStatus::BoundedEmpiricalFinding,
            ClaimStatus::SimulationObservation,
            ClaimStatus::ProtocolReplayPass,
            ClaimStatus::Definition,
            ClaimStatus::Nonclaim,
            ClaimStatus::SynthesisConclusion,
            ClaimStatus::Interpretive,
            ClaimStatus::ConjectureFalsifiable,
        ];
        assert_eq!(all.len(), 15);
        let mapped_count = all.iter().filter(|s| map_claim_status(**s).is_ok()).count();
        let refused_count = all.iter().filter(|s| map_claim_status(**s).is_err()).count();
        assert_eq!(mapped_count, 11);
        assert_eq!(refused_count, 4);
    }
}
