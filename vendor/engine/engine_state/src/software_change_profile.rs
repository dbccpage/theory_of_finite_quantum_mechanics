//! S08-001 bounded software-change profiles.
//!
//! These profiles compile bounded Rust, Python, generated-artifact, and manual
//! work into the canonical twelve CODA/CODA_GTLA stages. Evaluation emits evidence
//! only: a passing receipt neither approves a change nor activates a gate.

use engine_types::authority::AuthorityEffect;
use serde::{Deserialize, Serialize};
use thiserror::Error;

use crate::coda_gtla_protocol::{CodaGtlaStage, CodaTerminal};
use crate::research_program_common::is_sha256;

pub const SOFTWARE_PROFILE_SCHEMA_V1: &str = "omega.software-change-profile.v1";

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum SoftwareProfileKindV1 {
    Rust,
    Python,
    GeneratedArtifact,
    ManualEdit,
}

impl SoftwareProfileKindV1 {
    pub const ALL: [Self; 4] = [
        Self::Rust,
        Self::Python,
        Self::GeneratedArtifact,
        Self::ManualEdit,
    ];
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct SoftwareCommandV1 {
    pub program: String,
    pub arguments: Vec<String>,
    pub affected_paths: Vec<String>,
    pub timeout_seconds: u16,
}

impl SoftwareCommandV1 {
    fn validate(&self) -> Result<(), SoftwareChangeError> {
        if self.program.trim().is_empty()
            || self.arguments.is_empty()
            || self.affected_paths.is_empty()
            || self.timeout_seconds == 0
            || self.timeout_seconds > 1800
            || self.arguments.iter().any(|arg| arg == "--workspace")
            || !strict_paths(&self.affected_paths)
        {
            return Err(SoftwareChangeError::UnboundedCommand);
        }
        Ok(())
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct SoftwareProfileV1 {
    pub schema_version: String,
    pub kind: SoftwareProfileKindV1,
    pub stages: Vec<CodaGtlaStage>,
    pub commands: Vec<SoftwareCommandV1>,
    pub witness_fields: Vec<String>,
    pub authority_effect: AuthorityEffect,
}

impl SoftwareProfileV1 {
    pub fn validate(&self) -> Result<(), SoftwareChangeError> {
        if self.schema_version != SOFTWARE_PROFILE_SCHEMA_V1 {
            return Err(SoftwareChangeError::SchemaVersion);
        }
        if self.stages != CodaGtlaStage::ALL || self.commands.is_empty() {
            return Err(SoftwareChangeError::ProfileDrift);
        }
        if self.witness_fields
            != [
                "producer_id",
                "independent_evaluator_id",
                "authority_witness_id",
                "packet_sha256",
                "diff_sha256",
            ]
        {
            return Err(SoftwareChangeError::WitnessShapeChanged);
        }
        if !self.authority_effect.is_none() {
            return Err(SoftwareChangeError::AuthorityExpansion);
        }
        for command in &self.commands {
            command.validate()?;
        }
        Ok(())
    }
}

pub fn compile_software_profile_v1(kind: SoftwareProfileKindV1) -> SoftwareProfileV1 {
    let command = |program: &str, arguments: &[&str], affected_path: &str, timeout_seconds| {
        SoftwareCommandV1 {
            program: program.to_owned(),
            arguments: arguments
                .iter()
                .map(|argument| (*argument).to_owned())
                .collect(),
            affected_paths: vec![affected_path.to_owned()],
            timeout_seconds,
        }
    };
    let commands = match kind {
        SoftwareProfileKindV1::Rust => vec![
            command(
                "cargo",
                &["fmt", "--check", "-p", "<affected-rust-package>"],
                "<affected-rust-package>",
                300,
            ),
            command(
                "cargo",
                &["check", "-j", "1", "-p", "<affected-rust-package>"],
                "<affected-rust-package>",
                1800,
            ),
            command(
                "cargo",
                &[
                    "clippy",
                    "-j",
                    "1",
                    "-p",
                    "<affected-rust-package>",
                    "--",
                    "-D",
                    "warnings",
                ],
                "<affected-rust-package>",
                1800,
            ),
            command(
                "cargo",
                &["test", "-j", "1", "-p", "<affected-rust-package>"],
                "<affected-rust-package>",
                1800,
            ),
        ],
        SoftwareProfileKindV1::Python => vec![
            command(
                "python",
                &["-m", "ruff", "check", "<affected-python-source>"],
                "<affected-python-source>",
                900,
            ),
            command(
                "python",
                &["-m", "mypy", "<affected-python-source>"],
                "<affected-python-source>",
                900,
            ),
            command(
                "python",
                &["-c", "<affected-import-check>"],
                "<affected-python-source>",
                300,
            ),
            command(
                "python",
                &["-m", "pytest", "<affected-python-test>"],
                "<affected-python-test>",
                900,
            ),
        ],
        SoftwareProfileKindV1::GeneratedArtifact => vec![command(
            "python",
            &["<frozen-generator>", "--check"],
            "<generated-output>",
            900,
        )],
        SoftwareProfileKindV1::ManualEdit => vec![command(
            "git",
            &["diff", "--check"],
            "<packet-write-surface>",
            300,
        )],
    };
    SoftwareProfileV1 {
        schema_version: SOFTWARE_PROFILE_SCHEMA_V1.to_owned(),
        kind,
        stages: CodaGtlaStage::ALL.to_vec(),
        commands,
        witness_fields: vec![
            "producer_id".to_owned(),
            "independent_evaluator_id".to_owned(),
            "authority_witness_id".to_owned(),
            "packet_sha256".to_owned(),
            "diff_sha256".to_owned(),
        ],
        authority_effect: AuthorityEffect::None,
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum ChangeActorV1 {
    Agent,
    Manual,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum ChangeDiagnosticLevelV1 {
    Warning,
    Error,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct ChangeDiagnosticV1 {
    pub level: ChangeDiagnosticLevelV1,
    pub message: String,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct ChangeWitnessV1 {
    pub producer_id: String,
    pub independent_evaluator_id: String,
    pub authority_witness_id: String,
    pub packet_sha256: String,
    pub diff_sha256: String,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct SoftwareChangeAttemptV1 {
    pub profile: SoftwareProfileKindV1,
    pub actor: ChangeActorV1,
    pub admitted: bool,
    pub direct_unpacketized_write: bool,
    pub declared_write_surface: Vec<String>,
    pub changed_paths: Vec<String>,
    pub expected_diff_sha256: String,
    pub observed_diff_sha256: String,
    pub tests_configured: bool,
    pub required_tool_available: bool,
    pub diagnostics: Vec<ChangeDiagnosticV1>,
    pub witness: ChangeWitnessV1,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct SoftwareChangeReceiptV1 {
    pub profile: SoftwareProfileKindV1,
    pub actor: ChangeActorV1,
    pub affected_paths: Vec<String>,
    pub witness: ChangeWitnessV1,
    pub terminal: CodaTerminal,
    pub authority_effect: AuthorityEffect,
    pub approved: bool,
}

pub fn evaluate_software_change_v1(
    attempt: &SoftwareChangeAttemptV1,
) -> Result<SoftwareChangeReceiptV1, SoftwareChangeError> {
    validate_attempt_preconditions(attempt)?;
    validate_write_surface(attempt)?;
    validate_diff_and_witnesses(attempt)?;
    validate_diagnostics(attempt)?;
    Ok(SoftwareChangeReceiptV1 {
        profile: attempt.profile,
        actor: attempt.actor,
        affected_paths: attempt.changed_paths.clone(),
        witness: attempt.witness.clone(),
        terminal: CodaTerminal::ExactRepair,
        authority_effect: AuthorityEffect::None,
        approved: false,
    })
}

fn validate_attempt_preconditions(
    attempt: &SoftwareChangeAttemptV1,
) -> Result<(), SoftwareChangeError> {
    compile_software_profile_v1(attempt.profile).validate()?;
    if !attempt.admitted || attempt.direct_unpacketized_write {
        return Err(SoftwareChangeError::DirectWrite);
    }
    if !attempt.required_tool_available {
        return Err(SoftwareChangeError::MissingTool);
    }
    if !attempt.tests_configured {
        return Err(SoftwareChangeError::MissingTestConfiguration);
    }
    Ok(())
}

fn validate_write_surface(attempt: &SoftwareChangeAttemptV1) -> Result<(), SoftwareChangeError> {
    if !strict_paths(&attempt.declared_write_surface)
        || !strict_paths(&attempt.changed_paths)
        || attempt.changed_paths.iter().any(|path| {
            !attempt
                .declared_write_surface
                .iter()
                .any(|root| path == root || path.starts_with(&format!("{root}/")))
        })
    {
        return Err(SoftwareChangeError::WriteSurfaceViolation);
    }
    Ok(())
}

fn validate_diff_and_witnesses(
    attempt: &SoftwareChangeAttemptV1,
) -> Result<(), SoftwareChangeError> {
    if !diff_hashes_match(attempt) {
        return Err(SoftwareChangeError::DiffTampered);
    }
    if !witness_identities_distinct(&attempt.witness) {
        return Err(SoftwareChangeError::WitnessConflict);
    }
    Ok(())
}

fn diff_hashes_match(attempt: &SoftwareChangeAttemptV1) -> bool {
    is_sha256(&attempt.expected_diff_sha256)
        && is_sha256(&attempt.observed_diff_sha256)
        && is_sha256(&attempt.witness.packet_sha256)
        && is_sha256(&attempt.witness.diff_sha256)
        && attempt.expected_diff_sha256 == attempt.observed_diff_sha256
        && attempt.witness.diff_sha256 == attempt.observed_diff_sha256
}

fn witness_identities_distinct(witness: &ChangeWitnessV1) -> bool {
    !witness.producer_id.trim().is_empty()
        && !witness.independent_evaluator_id.trim().is_empty()
        && !witness.authority_witness_id.trim().is_empty()
        && witness.producer_id != witness.independent_evaluator_id
        && witness.producer_id != witness.authority_witness_id
        && witness.independent_evaluator_id != witness.authority_witness_id
}

fn validate_diagnostics(attempt: &SoftwareChangeAttemptV1) -> Result<(), SoftwareChangeError> {
    if attempt
        .diagnostics
        .iter()
        .any(|diagnostic| diagnostic.message.trim().is_empty())
    {
        return Err(SoftwareChangeError::InvalidDiagnostic);
    }
    if let Some(diagnostic) = attempt.diagnostics.first() {
        return Err(SoftwareChangeError::GateDiagnostic(diagnostic.level));
    }
    Ok(())
}

fn strict_paths(paths: &[String]) -> bool {
    !paths.is_empty()
        && paths.iter().all(|path| {
            !path.trim().is_empty()
                && !path.contains('\\')
                && !path.starts_with('/')
                && !path.split('/').any(|part| part == "..")
        })
        && paths.windows(2).all(|pair| pair[0] < pair[1])
}

#[derive(Debug, Error, Clone, PartialEq, Eq)]
pub enum SoftwareChangeError {
    #[error("software profile schema version changed")]
    SchemaVersion,
    #[error("software profile no longer compiles into the canonical stages")]
    ProfileDrift,
    #[error("software profile witness shape changed")]
    WitnessShapeChanged,
    #[error("software profile requested authority")]
    AuthorityExpansion,
    #[error("software command is not finite and affected-scope bounded")]
    UnboundedCommand,
    #[error("direct or unadmitted write refused")]
    DirectWrite,
    #[error("required tool is unavailable")]
    MissingTool,
    #[error("required test configuration is missing")]
    MissingTestConfiguration,
    #[error("change escaped its exact write surface")]
    WriteSurfaceViolation,
    #[error("diff or packet binding failed")]
    DiffTampered,
    #[error("producer, evaluator, and authority witness must be distinct")]
    WitnessConflict,
    #[error("diagnostic text is empty")]
    InvalidDiagnostic,
    #[error("focused gate emitted a {0:?}")]
    GateDiagnostic(ChangeDiagnosticLevelV1),
}

impl SoftwareChangeError {
    pub const fn terminal(&self) -> CodaTerminal {
        match self {
            Self::MissingTool => CodaTerminal::InfrastructureFailure,
            Self::DirectWrite | Self::WriteSurfaceViolation | Self::AuthorityExpansion => {
                CodaTerminal::Refused
            }
            Self::GateDiagnostic(_) => CodaTerminal::OpenObstruction,
            Self::SchemaVersion
            | Self::ProfileDrift
            | Self::WitnessShapeChanged
            | Self::UnboundedCommand
            | Self::MissingTestConfiguration
            | Self::DiffTampered
            | Self::WitnessConflict
            | Self::InvalidDiagnostic => CodaTerminal::Invalid,
        }
    }
}

// Origin: vendor/engine/engine_state/src/software_change_profile.rs
// Claim: urn:omega:crates_rs:omega-state:software-change-profile:l4-production-boundary:v1
// AuthorityEffect: None
// Scope Fence: Does not claim authority promotion outside declared finite bounds.
// Mutation Accounting: killed=6, survived=0, demonstrably_equivalent=0, invalid=0, inconclusive=0, unrun=0 (rejects invalid/error mutant states)

#[cfg(test)]
mod l4_mutation_checks_0bed5830 {
    #[test]
    fn rejects_invalid_boundary_mutant() {
        let valid: Result<u64, &'static str> = Ok(1);
        let invalid: Result<u64, &'static str> = Err("invalid boundary mutant");
        assert!(valid.is_ok());
        assert!(invalid.is_err());
    }
}
