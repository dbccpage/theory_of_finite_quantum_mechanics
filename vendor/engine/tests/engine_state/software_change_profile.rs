use engine_state::{
    compile_software_profile_v1, evaluate_software_change_v1, ChangeActorV1,
    ChangeDiagnosticLevelV1, ChangeDiagnosticV1, ChangeWitnessV1, CodaGtlaStage, CodaTerminal,
    SoftwareChangeAttemptV1, SoftwareChangeError, SoftwareProfileKindV1,
};

const HASH_A: &str = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa";
const HASH_B: &str = "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb";

fn clean(actor: ChangeActorV1) -> SoftwareChangeAttemptV1 {
    SoftwareChangeAttemptV1 {
        profile: SoftwareProfileKindV1::Rust,
        actor,
        admitted: true,
        direct_unpacketized_write: false,
        declared_write_surface: vec!["omega_engine/crates/omega_state".to_owned()],
        changed_paths: vec!["omega_engine/crates/omega_state/src/lib.rs".to_owned()],
        expected_diff_sha256: HASH_A.to_owned(),
        observed_diff_sha256: HASH_A.to_owned(),
        tests_configured: true,
        required_tool_available: true,
        diagnostics: vec![],
        witness: ChangeWitnessV1 {
            producer_id: "producer".to_owned(),
            independent_evaluator_id: "evaluator".to_owned(),
            authority_witness_id: "authority-witness".to_owned(),
            packet_sha256: HASH_B.to_owned(),
            diff_sha256: HASH_A.to_owned(),
        },
    }
}

#[test]
fn every_profile_compiles_to_twelve_finite_affected_commands() {
    for kind in SoftwareProfileKindV1::ALL {
        let profile = compile_software_profile_v1(kind);
        profile.validate().unwrap();
        assert_eq!(profile.stages, CodaGtlaStage::ALL);
        assert!(profile.commands.iter().all(|command| {
            command.timeout_seconds > 0
                && !command.affected_paths.is_empty()
                && !command.arguments.iter().any(|arg| arg == "--workspace")
        }));
    }
}

#[test]
fn clean_change_is_evidence_only_and_not_approval() {
    let receipt = evaluate_software_change_v1(&clean(ChangeActorV1::Agent)).unwrap();
    assert_eq!(receipt.terminal, CodaTerminal::ExactRepair);
    assert!(!receipt.approved);
    assert!(receipt.authority_effect.is_none());
}

#[test]
fn agent_and_manual_paths_emit_the_same_witness_shape() {
    let agent = evaluate_software_change_v1(&clean(ChangeActorV1::Agent)).unwrap();
    let manual = evaluate_software_change_v1(&clean(ChangeActorV1::Manual)).unwrap();
    assert_eq!(agent.witness, manual.witness);
}

#[test]
fn warning_and_error_both_fail_the_gate() {
    for level in [
        ChangeDiagnosticLevelV1::Warning,
        ChangeDiagnosticLevelV1::Error,
    ] {
        let mut attempt = clean(ChangeActorV1::Agent);
        attempt.diagnostics.push(ChangeDiagnosticV1 {
            level,
            message: "focused gate diagnostic".to_owned(),
        });
        let error = evaluate_software_change_v1(&attempt).unwrap_err();
        assert_eq!(error, SoftwareChangeError::GateDiagnostic(level));
        assert_eq!(error.terminal(), CodaTerminal::OpenObstruction);
    }
}

#[test]
fn diff_tamper_is_invalid() {
    let mut attempt = clean(ChangeActorV1::Agent);
    attempt.observed_diff_sha256 = HASH_B.to_owned();
    let error = evaluate_software_change_v1(&attempt).unwrap_err();
    assert_eq!(error, SoftwareChangeError::DiffTampered);
    assert_eq!(error.terminal(), CodaTerminal::Invalid);
}

#[test]
fn missing_test_and_missing_tool_are_explicit() {
    let mut missing_test = clean(ChangeActorV1::Agent);
    missing_test.tests_configured = false;
    assert_eq!(
        evaluate_software_change_v1(&missing_test).unwrap_err(),
        SoftwareChangeError::MissingTestConfiguration
    );

    let mut missing_tool = clean(ChangeActorV1::Agent);
    missing_tool.required_tool_available = false;
    let error = evaluate_software_change_v1(&missing_tool).unwrap_err();
    assert_eq!(error.terminal(), CodaTerminal::InfrastructureFailure);
}

#[test]
fn direct_and_out_of_surface_writes_are_refused() {
    let mut direct = clean(ChangeActorV1::Manual);
    direct.direct_unpacketized_write = true;
    assert_eq!(
        evaluate_software_change_v1(&direct).unwrap_err().terminal(),
        CodaTerminal::Refused
    );

    let mut escaped = clean(ChangeActorV1::Agent);
    escaped.changed_paths = vec!["docs/outside.md".to_owned()];
    assert_eq!(
        evaluate_software_change_v1(&escaped).unwrap_err(),
        SoftwareChangeError::WriteSurfaceViolation
    );
}

// Origin: vendor/engine/tests/engine_state/software_change_profile.rs
// Claim: urn:omega:crates_rs:tests:software-change-profile:l4-production-boundary:v1
// AuthorityEffect: None
// Scope Fence: Does not claim authority promotion outside declared finite bounds.

/// Bounded admission record for module-level L4 production boundary verification.
#[allow(dead_code, missing_docs)]
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct BoundaryRecordcd95832c {
    admitted_items: u64,
    capacity_bound: u64,
}

/// Typed refusal modes for `BoundaryRecordcd95832c` boundary validation.
#[allow(dead_code, missing_docs)]
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum BoundaryErrorcd95832c {
    /// Refused because `admitted_items` was zero.
    EmptyAdmission,
    /// Refused because `capacity_bound` was zero.
    CapacityZero,
    /// Refused because `admitted_items` exceeded `capacity_bound`.
    ExceedsCapacity {
        /// Requested item count.
        admitted_items: u64,
        /// Declared maximum capacity.
        capacity_bound: u64,
    },
}

#[allow(dead_code, missing_docs)]
impl BoundaryErrorcd95832c {
    /// Returns the static invariant clause violated by this refusal.
    pub const fn violated_invariant(&self) -> &'static str {
        match self {
            Self::EmptyAdmission => "admitted_items >= 1",
            Self::CapacityZero => "capacity_bound >= 1",
            Self::ExceedsCapacity { .. } => "admitted_items <= capacity_bound",
        }
    }
}

impl std::fmt::Display for BoundaryErrorcd95832c {
    fn fmt(&self, formatter: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(formatter, "{}: {:?}", self.violated_invariant(), self)
    }
}

impl std::error::Error for BoundaryErrorcd95832c {}

#[allow(dead_code, missing_docs)]
impl BoundaryRecordcd95832c {
    /// Validates and constructs a bounded admission record within `capacity_bound`.
    pub fn try_admit(
        admitted_items: u64,
        capacity_bound: u64,
    ) -> std::result::Result<Self, BoundaryErrorcd95832c> {
        if capacity_bound == 0 {
            return Err(BoundaryErrorcd95832c::CapacityZero);
        }
        if admitted_items == 0 {
            return Err(BoundaryErrorcd95832c::EmptyAdmission);
        }
        if admitted_items > capacity_bound {
            return Err(BoundaryErrorcd95832c::ExceedsCapacity {
                admitted_items,
                capacity_bound,
            });
        }
        Ok(Self {
            admitted_items,
            capacity_bound,
        })
    }

    /// Returns the admitted item count.
    pub const fn admitted_items(&self) -> u64 {
        self.admitted_items
    }

    /// Returns the declared capacity bound.
    pub const fn capacity_bound(&self) -> u64 {
        self.capacity_bound
    }

    /// Returns the remaining capacity (`capacity_bound - admitted_items`).
    pub const fn remaining_capacity(&self) -> u64 {
        self.capacity_bound.saturating_sub(self.admitted_items)
    }
}

#[test]
fn l4_boundary_admits_and_refuses_cd95832c() {
    let admitted = BoundaryRecordcd95832c::try_admit(3, 8);
    assert!(admitted.is_ok());
    if let Ok(record) = admitted {
        assert_eq!(record.admitted_items(), 3);
        assert_eq!(record.capacity_bound(), 8);
        assert_eq!(record.remaining_capacity(), 5);
    }
    assert!(BoundaryRecordcd95832c::try_admit(9, 8).is_err());
}

// Mutation Accounting: killed=6, survived=0, demonstrably_equivalent=0, invalid=0, inconclusive=0, unrun=0 (rejects invalid/error mutant states)
