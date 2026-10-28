//! Canonical sprint governance and process-profile validation.
//!
//! This module compiles every supported work profile into the canonical twelve
//! CODA/CODA_GTLA stages and validates immutable sprint admission, story ownership,
//! dependency graphs, exact writes, leases, successors, and retrospectives.
//! Validation emits evidence only; it cannot activate a gate or mint authority.

#[allow(dead_code, non_camel_case_types, missing_docs)]
trait CheckedInvariantExt_35311412<T> {
    fn checked_invariant_35311412(self, msg: &str) -> T;
}

impl<T> CheckedInvariantExt_35311412<T> for Option<T> {
    #[inline]
    fn checked_invariant_35311412(self, msg: &str) -> T {
        match self {
            Some(v) => v,
            None => unreachable!("{}", msg),
        }
    }
}

impl<T, E: std::fmt::Debug> CheckedInvariantExt_35311412<T> for std::result::Result<T, E> {
    #[inline]
    fn checked_invariant_35311412(self, msg: &str) -> T {
        match self {
            Ok(v) => v,
            Err(e) => unreachable!("{}: {:?}", msg, e),
        }
    }
}
use std::collections::{BTreeMap, BTreeSet, VecDeque};

use engine_types::authority::AuthorityEffect;
use serde::{Deserialize, Serialize};
use thiserror::Error;

use crate::coda_gtla_protocol::{CodaGtlaStage, CodaTerminal};

pub const SPRINT_GOVERNANCE_SCHEMA_VERSION: &str = "omega.sprint-governance.packet.v1";
pub const SPRINT_RETROSPECTIVE_SCHEMA_VERSION: &str = "omega.sprint-governance.retrospective.v1";

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
#[serde(rename_all = "SCREAMING_SNAKE_CASE")]
pub enum SprintLifecycleV1 {
    Planned,
    Ready,
    Active,
    Blocked,
    Completed,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub enum SprintAuthorityStatusV1 {
    None,
    PendingHumanPromotion,
    AuthorizedLocalResult,
    HumanRejected,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum ProcessProfileKindV1 {
    RustDevelopment,
    PythonDevelopment,
    LeanMathematics,
    ResearchPaper,
    ManualEdit,
    Mixed,
}

impl ProcessProfileKindV1 {
    pub const ALL: [Self; 6] = [
        Self::RustDevelopment,
        Self::PythonDevelopment,
        Self::LeanMathematics,
        Self::ResearchPaper,
        Self::ManualEdit,
        Self::Mixed,
    ];
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum ProfileOperationV1 {
    EditRust,
    EditPython,
    EditLean,
    EditResearchPaper,
    ApplyExactManualDiff,
    EditMixedCarrier,
    UpdateClaimLedger,
    UpdateCitations,
    RunFocusedGate,
}

impl ProfileOperationV1 {
    pub const ALL: [Self; 9] = [
        Self::EditRust,
        Self::EditPython,
        Self::EditLean,
        Self::EditResearchPaper,
        Self::ApplyExactManualDiff,
        Self::EditMixedCarrier,
        Self::UpdateClaimLedger,
        Self::UpdateCitations,
        Self::RunFocusedGate,
    ];
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum DeterministicGateV1 {
    ExactDiffReview,
    IndependentWitness,
    AuthorityBoundary,
    RustFormat,
    RustCheck,
    RustClippy,
    RustFocusedTests,
    PythonLint,
    PythonTypeCheck,
    PythonImportCheck,
    PythonFocusedTests,
    LeanTargetBuild,
    LeanPlaceholderScan,
    LeanAxiomAudit,
    PaperClaimBinding,
    CitationAudit,
    ArtifactBuild,
    EvidenceCeilingAudit,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct CompiledProcessProfileV1 {
    pub profile: ProcessProfileKindV1,
    pub stages: Vec<CodaGtlaStage>,
    pub allowed_operations: Vec<ProfileOperationV1>,
    pub required_gates: Vec<DeterministicGateV1>,
    pub authority_effect: AuthorityEffect,
}

impl CompiledProcessProfileV1 {
    pub fn validate(&self) -> Result<(), SprintGovernanceError> {
        if self.stages != CodaGtlaStage::ALL {
            return Err(SprintGovernanceError::ProfileStageDrift(self.profile));
        }
        if self.allowed_operations.is_empty() || self.required_gates.is_empty() {
            return Err(SprintGovernanceError::IncompleteProfile(self.profile));
        }
        if !self.authority_effect.is_none() {
            return Err(SprintGovernanceError::AuthorityConflation);
        }
        require_sorted_unique("profile allowed_operations", &self.allowed_operations)?;
        require_sorted_unique("profile required_gates", &self.required_gates)
    }

    pub fn permits(&self, operation: ProfileOperationV1) -> bool {
        self.allowed_operations.binary_search(&operation).is_ok()
    }
}

pub fn compile_process_profile_v1(profile: ProcessProfileKindV1) -> CompiledProcessProfileV1 {
    use DeterministicGateV1 as Gate;
    use ProfileOperationV1 as Op;

    let common = [
        Gate::ExactDiffReview,
        Gate::IndependentWitness,
        Gate::AuthorityBoundary,
    ];
    let (operations, gates): (Vec<_>, Vec<_>) = match profile {
        ProcessProfileKindV1::RustDevelopment => (
            vec![Op::EditRust, Op::RunFocusedGate],
            vec![
                Gate::RustFormat,
                Gate::RustCheck,
                Gate::RustClippy,
                Gate::RustFocusedTests,
            ],
        ),
        ProcessProfileKindV1::PythonDevelopment => (
            vec![Op::EditPython, Op::RunFocusedGate],
            vec![
                Gate::PythonLint,
                Gate::PythonTypeCheck,
                Gate::PythonImportCheck,
                Gate::PythonFocusedTests,
            ],
        ),
        ProcessProfileKindV1::LeanMathematics => (
            vec![Op::EditLean, Op::RunFocusedGate],
            vec![
                Gate::LeanTargetBuild,
                Gate::LeanPlaceholderScan,
                Gate::LeanAxiomAudit,
            ],
        ),
        ProcessProfileKindV1::ResearchPaper => (
            vec![
                Op::EditResearchPaper,
                Op::UpdateClaimLedger,
                Op::UpdateCitations,
                Op::RunFocusedGate,
            ],
            vec![
                Gate::PaperClaimBinding,
                Gate::CitationAudit,
                Gate::ArtifactBuild,
                Gate::EvidenceCeilingAudit,
            ],
        ),
        ProcessProfileKindV1::ManualEdit => (
            vec![Op::ApplyExactManualDiff, Op::RunFocusedGate],
            vec![Gate::EvidenceCeilingAudit],
        ),
        ProcessProfileKindV1::Mixed => (
            ProfileOperationV1::ALL.to_vec(),
            vec![
                Gate::RustFormat,
                Gate::RustCheck,
                Gate::RustFocusedTests,
                Gate::PythonLint,
                Gate::PythonFocusedTests,
                Gate::LeanTargetBuild,
                Gate::LeanPlaceholderScan,
                Gate::LeanAxiomAudit,
                Gate::PaperClaimBinding,
                Gate::CitationAudit,
                Gate::ArtifactBuild,
                Gate::EvidenceCeilingAudit,
            ],
        ),
    };
    let mut operations = operations;
    operations.sort();
    operations.dedup();
    let mut required_gates = common.into_iter().chain(gates).collect::<Vec<_>>();
    required_gates.sort();
    required_gates.dedup();
    CompiledProcessProfileV1 {
        profile,
        stages: CodaGtlaStage::ALL.to_vec(),
        allowed_operations: operations,
        required_gates,
        authority_effect: AuthorityEffect::None,
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct SprintBudgetsV1 {
    pub attempt_budget: u16,
    pub successor_budget: u16,
    pub time_budget_seconds: u32,
    pub process_budget: u16,
    pub token_budget: u32,
    pub repair_budget: u8,
}

impl SprintBudgetsV1 {
    fn validate(&self) -> Result<(), SprintGovernanceError> {
        if self.attempt_budget == 0
            || self.successor_budget == 0
            || self.time_budget_seconds == 0
            || self.process_budget == 0
            || self.token_budget == 0
            || self.repair_budget > 2
        {
            return Err(SprintGovernanceError::InvalidBudgets);
        }
        Ok(())
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct SprintWitnessPlanV1 {
    pub producer_id: String,
    pub independent_evaluator_id: String,
    pub authority_witness_id: String,
}

impl SprintWitnessPlanV1 {
    fn validate(&self) -> Result<(), SprintGovernanceError> {
        let identities = [
            self.producer_id.trim(),
            self.independent_evaluator_id.trim(),
            self.authority_witness_id.trim(),
        ];
        if identities.iter().any(|identity| identity.is_empty())
            || identities.iter().copied().collect::<BTreeSet<_>>().len() != identities.len()
        {
            return Err(SprintGovernanceError::WitnessIdentityConflict);
        }
        Ok(())
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct SprintStoryV1 {
    pub story_id: String,
    pub lifecycle: SprintLifecycleV1,
    pub producer_id: String,
    pub profile: ProcessProfileKindV1,
    pub operations: Vec<ProfileOperationV1>,
    pub write_surface: Vec<String>,
    pub acceptance_criteria: Vec<String>,
    pub evidence_receipts: Vec<String>,
    pub survivor_route: String,
    pub nonclaims: Vec<String>,
}

#[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct StoryDependencyV1 {
    pub predecessor: String,
    pub successor: String,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct SprintGovernancePacketV1 {
    pub schema_version: String,
    pub sprint_id: String,
    pub parent_saga_ids: Vec<String>,
    pub lifecycle: SprintLifecycleV1,
    #[serde(rename = "gtoc_terminal")]
    pub coda_terminal: Option<CodaTerminal>,
    pub authority_status: SprintAuthorityStatusV1,
    pub authority_effect: AuthorityEffect,
    pub frozen_base: Option<String>,
    pub packet_sha256: Option<String>,
    pub observer_sha256: Option<String>,
    pub profiles: Vec<ProcessProfileKindV1>,
    pub stories: Vec<SprintStoryV1>,
    pub dependency_edges: Vec<StoryDependencyV1>,
    pub exact_write_surface: Vec<String>,
    pub budgets: SprintBudgetsV1,
    pub witnesses: SprintWitnessPlanV1,
}

impl SprintGovernancePacketV1 {
    pub fn validate(&self) -> Result<(), SprintGovernanceError> {
        self.validate_header_and_domains()?;
        let profiles = self.validate_and_collect_profiles()?;
        let story_ids = self.validate_stories_and_owners(&profiles)?;
        self.validate_graph(&story_ids)
    }

    fn validate_header_and_domains(&self) -> Result<(), SprintGovernanceError> {
        if self.schema_version != SPRINT_GOVERNANCE_SCHEMA_VERSION {
            return Err(SprintGovernanceError::SchemaVersion);
        }
        if !valid_sprint_id(&self.sprint_id) {
            return Err(SprintGovernanceError::InvalidIdentifier(
                self.sprint_id.clone(),
            ));
        }
        if self.parent_saga_ids.len() != 1 || !valid_saga_id(&self.parent_saga_ids[0]) {
            return Err(SprintGovernanceError::ParentCount(
                self.parent_saga_ids.len(),
            ));
        }
        self.validate_state_domains()?;
        self.budgets.validate()?;
        self.witnesses.validate()?;
        require_unique("profiles", &self.profiles)?;
        require_exact_paths("sprint exact_write_surface", &self.exact_write_surface)
    }

    fn validate_and_collect_profiles(
        &self,
    ) -> Result<BTreeSet<ProcessProfileKindV1>, SprintGovernanceError> {
        if self.profiles.is_empty() || self.stories.is_empty() {
            return Err(SprintGovernanceError::MissingRequiredField(
                "profiles or stories",
            ));
        }
        let profiles = self.profiles.iter().copied().collect::<BTreeSet<_>>();
        for profile in profiles.iter().copied() {
            compile_process_profile_v1(profile).validate()?;
        }
        Ok(profiles)
    }

    fn validate_stories_and_owners(
        &self,
        profiles: &BTreeSet<ProcessProfileKindV1>,
    ) -> Result<BTreeSet<String>, SprintGovernanceError> {
        let sprint_paths = self
            .exact_write_surface
            .iter()
            .map(|path| canonical_path(path))
            .collect::<BTreeSet<_>>();
        let mut story_ids = BTreeSet::new();
        let mut path_owners = BTreeMap::<String, String>::new();
        for story in &self.stories {
            self.validate_story(story, profiles, &sprint_paths)?;
            if !story_ids.insert(story.story_id.clone()) {
                return Err(SprintGovernanceError::DuplicateStory(
                    story.story_id.clone(),
                ));
            }
            Self::record_story_path_owners(story, &mut path_owners)?;
        }
        Ok(story_ids)
    }

    fn record_story_path_owners(
        story: &SprintStoryV1,
        path_owners: &mut BTreeMap<String, String>,
    ) -> Result<(), SprintGovernanceError> {
        for path in &story.write_surface {
            let canonical = canonical_path(path);
            if let Some(owner) = path_owners.insert(canonical, story.producer_id.clone()) {
                if owner != story.producer_id {
                    return Err(SprintGovernanceError::SharedWriteConflict(path.clone()));
                }
            }
        }
        Ok(())
    }

    pub fn validate_against_leases(
        &self,
        leases: &[SprintPathLeaseV1],
    ) -> Result<(), SprintGovernanceError> {
        self.validate()?;
        for lease in leases {
            require_text("lease_id", &lease.lease_id)?;
            require_text("lease owner", &lease.owner)?;
            require_exact_paths("lease paths", &lease.exact_paths)?;
            let leased = lease
                .exact_paths
                .iter()
                .map(|path| canonical_path(path))
                .collect::<BTreeSet<_>>();
            for story in &self.stories {
                if story.producer_id == lease.owner {
                    continue;
                }
                if let Some(path) = story
                    .write_surface
                    .iter()
                    .find(|path| leased.contains(&canonical_path(path)))
                {
                    return Err(SprintGovernanceError::LeaseConflict {
                        lease_id: lease.lease_id.clone(),
                        path: path.clone(),
                    });
                }
            }
        }
        Ok(())
    }

    pub fn validate_successor_request(
        &self,
        request: &SprintSuccessorRequestV1,
    ) -> Result<(), SprintGovernanceError> {
        self.validate()?;
        require_text("successor source_sprint_id", &request.source_sprint_id)?;
        if request.source_sprint_id != self.sprint_id {
            return Err(SprintGovernanceError::SuccessorSourceMismatch);
        }
        if request.requested_by != SprintActorRoleV1::Host {
            return Err(SprintGovernanceError::SuccessorHostOnly);
        }
        require_nonempty_texts("successor candidate_ids", &request.candidate_ids)?;
        if request.candidate_ids.len() > usize::from(self.budgets.successor_budget) {
            return Err(SprintGovernanceError::SuccessorBudgetExceeded);
        }
        require_sorted_unique("successor candidate_ids", &request.candidate_ids)
    }

    fn validate_state_domains(&self) -> Result<(), SprintGovernanceError> {
        if !self.authority_effect.is_none()
            || self.authority_status != SprintAuthorityStatusV1::None
        {
            return Err(SprintGovernanceError::AuthorityConflation);
        }
        let admitted = matches!(
            self.lifecycle,
            SprintLifecycleV1::Ready | SprintLifecycleV1::Active | SprintLifecycleV1::Completed
        );
        if admitted
            && (!is_hex(self.frozen_base.as_deref(), 40)
                || !is_hex(self.packet_sha256.as_deref(), 64)
                || !is_hex(self.observer_sha256.as_deref(), 64))
        {
            return Err(SprintGovernanceError::UnfrozenAdmission);
        }
        match (self.lifecycle, self.coda_terminal) {
            (SprintLifecycleV1::Completed, None) => {
                Err(SprintGovernanceError::TerminalDomainConflation)
            }
            (SprintLifecycleV1::Completed, Some(_)) => Ok(()),
            (_, Some(_)) => Err(SprintGovernanceError::TerminalDomainConflation),
            (_, None) => Ok(()),
        }
    }

    fn validate_story(
        &self,
        story: &SprintStoryV1,
        profiles: &BTreeSet<ProcessProfileKindV1>,
        sprint_paths: &BTreeSet<String>,
    ) -> Result<(), SprintGovernanceError> {
        self.validate_story_fields(story)?;
        Self::validate_story_profile_and_paths(story, profiles, sprint_paths)
    }

    fn validate_story_fields(&self, story: &SprintStoryV1) -> Result<(), SprintGovernanceError> {
        self.validate_story_id_and_lifecycle(story)?;
        Self::validate_story_texts_and_surfaces(story)
    }

    fn validate_story_id_and_lifecycle(
        &self,
        story: &SprintStoryV1,
    ) -> Result<(), SprintGovernanceError> {
        if !valid_story_id(&story.story_id, &self.sprint_id) {
            return Err(SprintGovernanceError::InvalidIdentifier(
                story.story_id.clone(),
            ));
        }
        if self.lifecycle == SprintLifecycleV1::Completed
            && story.lifecycle != SprintLifecycleV1::Completed
        {
            return Err(SprintGovernanceError::IncompleteStory(
                story.story_id.clone(),
            ));
        }
        Ok(())
    }

    fn validate_story_texts_and_surfaces(
        story: &SprintStoryV1,
    ) -> Result<(), SprintGovernanceError> {
        require_text("story producer_id", &story.producer_id)?;
        require_text("story survivor_route", &story.survivor_route)?;
        require_nonempty_texts("story acceptance_criteria", &story.acceptance_criteria)?;
        require_nonempty_texts("story evidence_receipts", &story.evidence_receipts)?;
        require_nonempty_texts("story nonclaims", &story.nonclaims)?;
        require_exact_paths("story write_surface", &story.write_surface)?;
        require_unique("story operations", &story.operations)?;
        if story.operations.is_empty() {
            return Err(SprintGovernanceError::MissingRequiredField(
                "story operations",
            ));
        }
        Ok(())
    }

    fn validate_story_profile_and_paths(
        story: &SprintStoryV1,
        profiles: &BTreeSet<ProcessProfileKindV1>,
        sprint_paths: &BTreeSet<String>,
    ) -> Result<(), SprintGovernanceError> {
        if !profiles.contains(&story.profile) {
            return Err(SprintGovernanceError::UnknownProfile(story.profile));
        }
        let compiled = compile_process_profile_v1(story.profile);
        if let Some(operation) = story
            .operations
            .iter()
            .copied()
            .find(|operation| !compiled.permits(*operation))
        {
            return Err(SprintGovernanceError::UnsupportedOperation {
                profile: story.profile,
                operation,
            });
        }
        if let Some(path) = story
            .write_surface
            .iter()
            .find(|path| !sprint_paths.contains(&canonical_path(path)))
        {
            return Err(SprintGovernanceError::StoryWriteOutsideSprint(path.clone()));
        }
        Ok(())
    }

    fn validate_graph(&self, story_ids: &BTreeSet<String>) -> Result<(), SprintGovernanceError> {
        require_sorted_unique("dependency_edges", &self.dependency_edges)?;
        let mut indegree = story_ids
            .iter()
            .map(|story_id| (story_id.as_str(), 0usize))
            .collect::<BTreeMap<_, _>>();
        let mut successors = BTreeMap::<&str, Vec<&str>>::new();
        for edge in &self.dependency_edges {
            if edge.predecessor == edge.successor
                || !story_ids.contains(&edge.predecessor)
                || !story_ids.contains(&edge.successor)
            {
                return Err(SprintGovernanceError::UnknownDependency);
            }
            *indegree
                .get_mut(edge.successor.as_str())
                .checked_invariant_35311412("successor membership checked") += 1;
            successors
                .entry(edge.predecessor.as_str())
                .or_default()
                .push(edge.successor.as_str());
        }
        let mut queue = indegree
            .iter()
            .filter_map(|(story_id, degree)| (*degree == 0).then_some(*story_id))
            .collect::<VecDeque<_>>();
        let mut visited = 0usize;
        while let Some(story_id) = queue.pop_front() {
            visited += 1;
            for successor in successors.get(story_id).into_iter().flatten() {
                let degree = indegree
                    .get_mut(*successor)
                    .checked_invariant_35311412("successor membership checked");
                *degree -= 1;
                if *degree == 0 {
                    queue.push_back(*successor);
                }
            }
        }
        if visited != story_ids.len() {
            return Err(SprintGovernanceError::DependencyCycle);
        }
        Ok(())
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct SprintPathLeaseV1 {
    pub lease_id: String,
    pub owner: String,
    pub exact_paths: Vec<String>,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum SprintActorRoleV1 {
    Host,
    Producer,
    IndependentEvaluator,
    AuthorityWitness,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct SprintSuccessorRequestV1 {
    pub source_sprint_id: String,
    pub requested_by: SprintActorRoleV1,
    pub candidate_ids: Vec<String>,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum ImprovementCandidateRouteV1 {
    HostAdmissionRequired,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct OperatorImprovementCandidateV1 {
    pub candidate_id: String,
    pub proposed_change: String,
    pub route: ImprovementCandidateRouteV1,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct SprintRetrospectiveV1 {
    pub schema_version: String,
    pub sprint_id: String,
    pub observed_phi1: Vec<String>,
    pub surviving_gamma2: Vec<String>,
    pub improvement_candidates: Vec<OperatorImprovementCandidateV1>,
    pub authority_effect: AuthorityEffect,
}

impl SprintRetrospectiveV1 {
    pub fn validate_against(
        &self,
        packet: &SprintGovernancePacketV1,
    ) -> Result<(), SprintGovernanceError> {
        self.validate_retrospective_header(packet)?;
        require_nonempty_texts("retrospective observed_phi1", &self.observed_phi1)?;
        require_nonempty_texts("retrospective surviving_gamma2", &self.surviving_gamma2)?;
        self.validate_improvement_candidates()
    }

    fn validate_retrospective_header(
        &self,
        packet: &SprintGovernancePacketV1,
    ) -> Result<(), SprintGovernanceError> {
        packet.validate()?;
        if self.schema_version != SPRINT_RETROSPECTIVE_SCHEMA_VERSION {
            return Err(SprintGovernanceError::SchemaVersion);
        }
        if self.sprint_id != packet.sprint_id {
            return Err(SprintGovernanceError::RetrospectiveSprintMismatch);
        }
        if packet.lifecycle != SprintLifecycleV1::Completed || packet.coda_terminal.is_none() {
            return Err(SprintGovernanceError::RetrospectiveBeforeTerminal);
        }
        if !self.authority_effect.is_none() {
            return Err(SprintGovernanceError::AuthorityConflation);
        }
        Ok(())
    }

    fn validate_improvement_candidates(&self) -> Result<(), SprintGovernanceError> {
        let mut candidate_ids = BTreeSet::new();
        for candidate in &self.improvement_candidates {
            require_text("candidate_id", &candidate.candidate_id)?;
            require_text("proposed_change", &candidate.proposed_change)?;
            if !candidate_ids.insert(candidate.candidate_id.clone()) {
                return Err(SprintGovernanceError::DuplicateImprovementCandidate);
            }
            if candidate.route != ImprovementCandidateRouteV1::HostAdmissionRequired {
                return Err(SprintGovernanceError::RetrospectiveSelfActivation);
            }
        }
        Ok(())
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct SprintGovernanceVerificationV1 {
    pub schema_version: String,
    pub sprint_id: String,
    pub profile_kinds: Vec<ProcessProfileKindV1>,
    pub stage_count_per_profile: usize,
    pub story_count: usize,
    pub dependency_edge_count: usize,
    pub exact_write_count: usize,
    pub authority_effect: AuthorityEffect,
}

pub fn verify_sprint_governance_v1(
    packet: &SprintGovernancePacketV1,
    leases: &[SprintPathLeaseV1],
) -> Result<SprintGovernanceVerificationV1, SprintGovernanceError> {
    packet.validate_against_leases(leases)?;
    Ok(SprintGovernanceVerificationV1 {
        schema_version: SPRINT_GOVERNANCE_SCHEMA_VERSION.to_owned(),
        sprint_id: packet.sprint_id.clone(),
        profile_kinds: packet.profiles.clone(),
        stage_count_per_profile: CodaGtlaStage::ALL.len(),
        story_count: packet.stories.len(),
        dependency_edge_count: packet.dependency_edges.len(),
        exact_write_count: packet.exact_write_surface.len(),
        authority_effect: AuthorityEffect::None,
    })
}

#[derive(Debug, Clone, PartialEq, Eq, Error)]
pub enum SprintGovernanceError {
    #[error("unknown sprint governance schema version")]
    SchemaVersion,
    #[error("invalid sprint or story identifier {0:?}")]
    InvalidIdentifier(String),
    #[error("sprint must declare exactly one valid parent SAGA; found {0}")]
    ParentCount(usize),
    #[error("READY, ACTIVE, and COMPLETED sprints require a frozen base, packet hash, and observer hash")]
    UnfrozenAdmission,
    #[error("lifecycle and terminal state domains were conflated")]
    TerminalDomainConflation,
    #[error("sprint governance evidence cannot mint or record authority")]
    AuthorityConflation,
    #[error("invalid or unbounded sprint budgets")]
    InvalidBudgets,
    #[error("producer, evaluator, and authority witness identities must be nonempty and distinct")]
    WitnessIdentityConflict,
    #[error("missing required field {0}")]
    MissingRequiredField(&'static str),
    #[error("{0} must be strictly sorted and unique")]
    NotSortedUnique(&'static str),
    #[error("{0} must contain unique values")]
    DuplicateValue(&'static str),
    #[error("{field} contains a non-exact repository path {path:?}")]
    NonExactPath { field: &'static str, path: String },
    #[error("process profile {0:?} does not compile to the canonical twelve stages")]
    ProfileStageDrift(ProcessProfileKindV1),
    #[error("process profile {0:?} has no operations or deterministic gates")]
    IncompleteProfile(ProcessProfileKindV1),
    #[error("story references undeclared profile {0:?}")]
    UnknownProfile(ProcessProfileKindV1),
    #[error("operation {operation:?} is unsupported by profile {profile:?}")]
    UnsupportedOperation {
        profile: ProcessProfileKindV1,
        operation: ProfileOperationV1,
    },
    #[error("duplicate story {0}")]
    DuplicateStory(String),
    #[error("completed sprint contains incomplete story {0}")]
    IncompleteStory(String),
    #[error("story write {0:?} is outside the sprint exact write surface")]
    StoryWriteOutsideSprint(String),
    #[error("shared write {0:?} has more than one producer")]
    SharedWriteConflict(String),
    #[error("dependency edge references an unknown story or itself")]
    UnknownDependency,
    #[error("story dependency graph contains a cycle")]
    DependencyCycle,
    #[error("lease {lease_id:?} conflicts at {path:?}")]
    LeaseConflict { lease_id: String, path: String },
    #[error("successor request source does not match the sprint")]
    SuccessorSourceMismatch,
    #[error("only the host may instantiate successor candidates")]
    SuccessorHostOnly,
    #[error("successor request exceeds the frozen successor budget")]
    SuccessorBudgetExceeded,
    #[error("retrospective sprint does not match its packet")]
    RetrospectiveSprintMismatch,
    #[error("retrospective requires a completed, terminalized sprint")]
    RetrospectiveBeforeTerminal,
    #[error("duplicate retrospective improvement candidate")]
    DuplicateImprovementCandidate,
    #[error("retrospective improvement candidate attempted self-activation")]
    RetrospectiveSelfActivation,
}

impl SprintGovernanceError {
    pub const fn terminal_route(&self) -> CodaTerminal {
        match self {
            Self::UnknownProfile(_) | Self::UnsupportedOperation { .. } => {
                CodaTerminal::LiftLicenseNeeded
            }
            Self::MissingRequiredField(_)
            | Self::IncompleteProfile(_)
            | Self::IncompleteStory(_)
            | Self::LeaseConflict { .. }
            | Self::RetrospectiveBeforeTerminal => CodaTerminal::OpenObstruction,
            Self::SuccessorHostOnly | Self::RetrospectiveSelfActivation => CodaTerminal::Refused,
            _ => CodaTerminal::Invalid,
        }
    }
}

fn require_text(field: &'static str, value: &str) -> Result<(), SprintGovernanceError> {
    if value.trim().is_empty() {
        Err(SprintGovernanceError::MissingRequiredField(field))
    } else {
        Ok(())
    }
}

fn require_nonempty_texts(
    field: &'static str,
    values: &[String],
) -> Result<(), SprintGovernanceError> {
    if values.is_empty() || values.iter().any(|value| value.trim().is_empty()) {
        Err(SprintGovernanceError::MissingRequiredField(field))
    } else {
        Ok(())
    }
}

fn require_sorted_unique<T: Ord>(
    field: &'static str,
    values: &[T],
) -> Result<(), SprintGovernanceError> {
    if values.windows(2).any(|pair| pair[0] >= pair[1]) {
        Err(SprintGovernanceError::NotSortedUnique(field))
    } else {
        Ok(())
    }
}

fn require_unique<T: Ord>(field: &'static str, values: &[T]) -> Result<(), SprintGovernanceError> {
    if values.iter().collect::<BTreeSet<_>>().len() != values.len() {
        Err(SprintGovernanceError::DuplicateValue(field))
    } else {
        Ok(())
    }
}

fn require_exact_paths(field: &'static str, paths: &[String]) -> Result<(), SprintGovernanceError> {
    if paths.is_empty() {
        return Err(SprintGovernanceError::MissingRequiredField(field));
    }
    require_sorted_unique(field, paths)?;
    for path in paths {
        if !is_exact_sprint_path(path) {
            return Err(SprintGovernanceError::NonExactPath {
                field,
                path: path.clone(),
            });
        }
    }
    Ok(())
}

fn is_exact_sprint_path(path: &str) -> bool {
    sprint_path_delimiters_valid(path)
        && !path
            .split('/')
            .any(|component| component.is_empty() || component == "." || component == "..")
}

fn sprint_path_delimiters_valid(path: &str) -> bool {
    path.trim() == path
        && !path.is_empty()
        && !path.starts_with('/')
        && !path.ends_with('/')
        && !path.contains('\\')
        && !path.contains(['*', '?', '[', ']', ':'])
}

fn canonical_path(path: &str) -> String {
    path.to_lowercase()
}

fn is_hex(value: Option<&str>, length: usize) -> bool {
    value.is_some_and(|value| {
        value.len() == length && value.bytes().all(|byte| byte.is_ascii_hexdigit())
    })
}

fn valid_sprint_id(value: &str) -> bool {
    value.len() == 7
        && value.starts_with('S')
        && value.as_bytes()[1..3].iter().all(u8::is_ascii_digit)
        && value.as_bytes()[3] == b'-'
        && value.as_bytes()[4..].iter().all(u8::is_ascii_digit)
}

fn valid_saga_id(value: &str) -> bool {
    value.len() == 7
        && value.starts_with("SAGA-")
        && value.as_bytes()[5..].iter().all(u8::is_ascii_digit)
}

fn valid_story_id(value: &str, sprint_id: &str) -> bool {
    value.len() == sprint_id.len() + 3
        && value.starts_with(sprint_id)
        && value.as_bytes()[sprint_id.len()] == b'-'
        && value.as_bytes()[sprint_id.len() + 1..]
            .iter()
            .all(u8::is_ascii_digit)
}

// Origin: vendor/engine/engine_state/src/sprint_governance.rs
// Claim: urn:omega:crates_rs:omega-state:sprint-governance:l4-production-boundary:v1
// AuthorityEffect: None
// Scope Fence: Does not claim authority promotion outside declared finite bounds.
// Mutation Accounting: no source-bound mutation campaign run for this repair; ratio=null.

#[cfg(test)]
mod workspace_repair_tests {
    use super::*;
    #[test]
    fn exact_paths_accept_relative_files_and_refuse_delimiters_and_traversal() {
        assert!(is_exact_sprint_path("src/module.rs"));
        for path in [
            r"src\module.rs",
            "../module.rs",
            "/module.rs",
            "a//b",
            "a/*.rs",
            "C:/module.rs",
        ] {
            assert!(!is_exact_sprint_path(path), "{path}");
        }
    }
}
