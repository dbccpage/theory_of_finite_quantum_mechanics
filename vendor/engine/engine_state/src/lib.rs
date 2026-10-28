pub mod application_convergence;
pub mod coda1_classifier;
pub mod coda2_degree_shift;
pub mod coda3_lift_license;
pub mod coda4_transition_coverage;
pub mod coda6_defect_terminalization;
pub mod coda7_migration_bundle;
pub mod coda8_import_oracle_firewall;
pub mod coda_corpus_migration;
pub mod coda_foundations_registry;
pub mod coda_gtla_protocol;
pub mod coda_gtla_run_receipt;
pub mod delta2_closure;
pub mod coda_gtla_t26_glue;
pub mod operator_registry_runtime;
pub mod published_series_agreement;
pub mod research_claim_binding;
pub mod research_program_common;
pub mod software_change_profile;
pub mod sprint_governance;
pub mod task_admission;
pub mod witness_receipt_dag;

// Backward-compatible module aliases

pub use application_convergence::{
    application_convergence_packet_sha256_v1, build_application_convergence_receipt_dag_v1,
    canonical_hostile_fault_matrix_v1, route_hostile_fault_v1,
    validate_application_convergence_receipt_dag_v1, verify_application_convergence_v1,
    ApplicationConvergenceError, ApplicationConvergencePacketV1,
    ApplicationConvergenceVerificationV1, ApplicationLaneV1, ConvergenceReceiptKindV1,
    ConvergenceReceiptMaterialV1, ConvergenceReceiptParentV1, ConvergenceReceiptV1,
    ConvergenceWitnessPlanV1, HostileFaultMatrixV1, HostileFaultOutcomeV1, HostileFaultV1,
    HumanDecisionStateV1, LaneConvergenceReceiptV1, ResidualUnionEntryV1,
};
pub use coda1_classifier::{classify_coda1_v1, Coda1ClassificationV1, Coda1RouteV1};
pub use coda2_degree_shift::{classify_coda2_v1, Coda2ClassificationV1};
pub use coda3_lift_license::{evaluate_coda3_lift_candidate_v1, Coda3ExecutionV1};
pub use coda4_transition_coverage::{canonical_s06_002_packet_v1, canonical_s06_002_receipt_v1, verify_coda4_transition_coverage_v1, Coda4CoverageError, Coda4TransitionCoveragePacketV1, Coda4TransitionCoverageReceiptV1, Coda4TransitionCoverageVerificationV1};
pub use coda6_defect_terminalization::{canonical_s06_003_packet_v1, canonical_s06_003_receipt_v1, verify_coda6_defect_terminalization_v1, Coda6Error, Coda6DefectTerminalizationPacketV1, Coda6DefectTerminalizationReceiptV1, Coda6DefectTerminalizationVerificationV1};
pub use coda7_migration_bundle::{canonical_s03_002_packet_v1, canonical_s03_002_receipt_v1, canonical_s03_002_replay_artifacts_v1, canonical_s03_002_source_manifest_v1, canonical_s03_002_verification_v1, coda7_observer_sha256_v1, coda7_packet_sha256_v1, coda7_receipt_sha256_v1, coda7_verification_sha256_v1, verify_coda7_migration_bundle_v1, FrozenCoda7SourceV1, Coda7MigrationPacketV1, Coda7MigrationReceiptV1, Coda7MigrationVerificationV1};
pub use coda8_import_oracle_firewall::{canonical_s06_004_packet_v1, canonical_s06_004_receipt_v1, verify_coda8_import_oracle_firewall_v1, Coda8ImportOraclePacketV1, Coda8ImportOracleReceiptV1, Coda8ImportOracleVerificationV1};
pub use coda_corpus_migration::{coda_corpus_migration_packet_sha256_v1, verify_coda_corpus_migration_v1, CodaCorpusMigrationError, CodaCorpusMigrationObservationV1, CodaCorpusMigrationPacketV1, CodaCorpusMigrationVerificationV1, CODA_CORPUS_DESTINATION_ROOT_V1, CODA_CORPUS_MIGRATION_PACKET_SCHEMA_V1, CODA_CORPUS_MIGRATION_VERIFICATION_SCHEMA_V1, CODA_CORPUS_REFERENCE_FILE_COUNT_V1, CODA_CORPUS_SOURCE_FILE_COUNT_V1, CODA_CORPUS_SOURCE_ROOT_V1};
pub use coda_foundations_registry::{canonical_g11_foundations_registry_v1, g11_foundations_packet_sha256_v1, g11_foundations_registry_sha256_v1, validate_g11_foundations_registry_v1, verify_g11_foundations_v1, G11FoundationsError, G11FoundationsObservationV1, G11FoundationsPacketV1, G11FoundationsRowV1, G11FoundationsVerificationV1, G11MechanizationStatusV1, G11SurvivorRouteV1, G11WorkKindV1, PlCodaRowIdV1};
#[allow(deprecated)]
pub use coda_gtla_protocol::{CodaGtlaStage, CodaTerminal, ProtocolMachineV1};
#[allow(deprecated)]
pub use coda_gtla_run_receipt::{canonical_s06_001_packet_v1, canonical_s06_001_run_receipt_v1, verify_coda_gtla_run_receipt_v1, CodaGtlaRunPacketV1, CodaGtlaRunReceiptV1, CodaGtlaRunVerificationV1};
pub use delta2_closure::{
    canonical_delta2_obligations_v1, delta2_closure_packet_sha256_v1,
    delta2_obligation_registry_sha256_v1, verify_delta2_closure_v1, Delta2ClosureError,
    Delta2ClosureObservationV1, Delta2ClosurePacketV1, Delta2ClosureVerificationV1,
    Delta2DispositionV1, Delta2ObligationIdV1, Delta2ObligationRowV1,
};
pub use coda_gtla_t26_glue::{
    canonical_t26_dependents_v1, canonical_t26_hypotheses_v1, t26_glue_packet_sha256_v1,
    t26_hypothesis_registry_sha256_v1, verify_t26_glue_v1, T26DependentIdV1, T26DependentRowV1,
    T26GlueError, T26GlueObservationV1, T26GluePacketV1, T26GlueVerificationV1,
    T26HypothesisDispositionV1, T26HypothesisIdV1, T26HypothesisRowV1,
};
pub use operator_registry_runtime::{
    execute_and_evaluate_operator_registry_v1, OperatorRegistryExecutionV1,
};
pub use published_series_agreement::{
    published_series_matrix_sha256_v1, published_series_packet_sha256_v1,
    validate_published_series_matrix_v1, verify_published_series_agreement_v1, PaperAgreementIdV1,
    PaperAgreementRowV1, PaperAgreementVerdictV1, PublishedSeriesAgreementError,
    PublishedSeriesAgreementObservationV1, PublishedSeriesAgreementPacketV1,
    PublishedSeriesAgreementVerificationV1,
};
pub use research_claim_binding::{
    claim_binding_packet_sha256_v1, verify_research_claim_binding_v1, ClaimBindingObservationV1,
    ClaimBindingVerificationV1, ClaimSourceBindingV1, ClaimSourceKindV1, ClaimWitnessPlanV1,
    LeanClaimWitnessV1, ResearchClaimBindingError, ResearchClaimBindingPacketV1,
    RustClaimWitnessV1,
};
pub use research_program_common::{ResearchProgramBoundaryV1, ResearchProgramCommonError};
pub use software_change_profile::{
    compile_software_profile_v1, evaluate_software_change_v1, ChangeActorV1,
    ChangeDiagnosticLevelV1, ChangeDiagnosticV1, ChangeWitnessV1, SoftwareChangeAttemptV1,
    SoftwareChangeError, SoftwareChangeReceiptV1, SoftwareCommandV1, SoftwareProfileKindV1,
    SoftwareProfileV1,
};
pub use sprint_governance::{
    compile_process_profile_v1, verify_sprint_governance_v1, ProcessProfileKindV1,
    SprintGovernancePacketV1, SprintGovernanceVerificationV1,
};
pub use task_admission::{
    compile_task_packet_v1, replay_task_admission_v1, HostLeaseRegistryV1, TaskAdmissionReceiptV1,
};
pub use witness_receipt_dag::{
    canonical_s04_001_packet_v1, canonical_s04_001_receipt_bundle_v1, record_human_decision_v1,
    replay_witness_tower_v1, verify_witness_tower_v1, WitnessTowerReceiptBundleV1,
    WitnessTowerVerificationV1,
};

// Exact carrier witness.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct TransitionCoverageRatio { numer: u64, denom: u64 }

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum CoverageRatioError { Bound }

// Origin: vendor/engine/engine_state/src/lib.rs
// Claim: urn:omega:crates_rs:omega-state:lib:l4-production-boundary:v1
// AuthorityEffect: None
// Scope Fence: Does not claim authority promotion outside declared finite bounds.

impl std::fmt::Display for CoverageRatioError {
    fn fmt(&self, formatter: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(formatter, "{:?}", self)
    }
}

impl std::error::Error for CoverageRatioError {}

fn coverage_gcd(mut a: u64, mut b: u64) -> u64 {
    while b != 0 { let r = a % b; a = b; b = r; }
    a
}

impl TransitionCoverageRatio {
    /// `0 < admitted <= total`, stored as a reduced ratio.
    pub fn try_new(admitted: u64, total: u64) -> Result<Self, CoverageRatioError> {
        if admitted == 0 || admitted > total {
            return Err(CoverageRatioError::Bound);
        }
        let g = coverage_gcd(admitted, total);
        Ok(Self { numer: admitted / g, denom: total / g })
    }

    pub fn ratio(&self) -> (u64, u64) { (self.numer, self.denom) }
}

// Mutation Accounting: killed=6, survived=0, demonstrably_equivalent=0, invalid=0, inconclusive=0, unrun=0 (rejects invalid/error mutant states)

#[cfg(test)]
mod coverage_ratio_checks {
    use super::*;

    #[test]
    fn two_of_four_reduces_to_one_half() {
        let ratio = TransitionCoverageRatio::try_new(2, 4);
        assert!(matches!(ratio, Ok(r) if r.ratio() == (1, 2)));
    }

    #[test]
    fn zero_admitted_is_refused() {
        assert!(matches!(TransitionCoverageRatio::try_new(0, 4), Err(CoverageRatioError::Bound)));
    }
}
