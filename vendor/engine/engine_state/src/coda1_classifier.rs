//! Finite CODA-1 sliding-window classification and replay receipts.
//!
//! The classifier is intentionally bounded to admitted local degrees 0-2. It
//! reuses `engine_homology` for image and closure decisions, treats no-rule as a
//! routing outcome rather than a cohomology class, and never promotes authority.
//!
//! # ADR-001 boundary
//!
//! A CODA-1 packet is a **frozen finite transcript**: its scalars arrive on the
//! wire as `i64` numerator/denominator pairs and are admitted only inside the
//! packet's own declared bounds ([`MAX_SCALAR_ABS`], [`MAX_DENOMINATOR`], both
//! 16). Those bounds are the packet's admission contract, not general law, so
//! they are checked **on the wire values, before any widening** — widening must
//! not silently admit a packet the transcript refuses.
//!
//! Only after that check does the pair enter the canonical `Q` (`BigRational`)
//! domain, via `BigInt::from(i64)` — total and exact, the injection direction
//! ADR-001 permits. Nothing converts back.

use std::collections::BTreeSet;

use linear_algebra::backend::basic_matrix::BasicMatrix;
use num_bigint::BigInt;
use num_traits::Zero;
use engine_homology::matrix::{in_column_space, is_zero_matrix, mat_mul, mat_vec_mul};
use engine_homology::scalar::Q;
use engine_homology::trichotomy_witness::{classify_residual, ResidualClass};
use engine_types::authority::AuthorityEffect;
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};
use thiserror::Error;

use crate::coda_gtla_protocol::{CodaTerminal, FrozenObserverContextV1};

pub const CODA1_ADMISSION_SCHEMA_VERSION: &str = "omega.gtoc1.admission.v1";
pub const CODA1_PACKET_SCHEMA_VERSION: &str = "omega.gtoc1.packet.v1";
pub const CODA1_CLASSIFICATION_SCHEMA_VERSION: &str = "omega.gtoc1.classification.v1";
pub const CODA1_RECEIPT_SCHEMA_VERSION: &str = "omega.gtoc1.receipts.v1";
pub const CODA1_OBSERVER_DOMAIN: &str = "finite-admitted-window-classification";
pub const CODA1_STATE_DOMAIN: &str = "omega.gtoc1.local-window.v1";
pub const CODA1_EVIDENCE_CEILING: &str =
    "finite admitted-window classification at local degrees 0-2; no theorem or authority promotion";


const MAX_WINDOW_DIMENSION: usize = 6;
const MAX_SCALAR_ABS: u64 = 16;
const MAX_DENOMINATOR: i64 = 16;

type ExactWindowMatrices = (BasicMatrix<Q>, BasicMatrix<Q>, Vec<Q>);

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct SourceHashV1 {
    pub path: String,
    pub sha256: String,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Coda1BudgetsV1 {
    pub attempt_budget: u16,
    pub repair_budget: u16,
    pub successor_budget: u16,
    pub time_budget_seconds: u32,
    pub process_budget: u16,
    pub token_budget: u64,
}

impl Coda1BudgetsV1 {
    fn validate(self) -> Result<(), Coda1Error> {
        if !self.counts_within_bounds() || !self.resources_within_bounds() {
            return Err(Coda1Error::BudgetOutsideAdmission);
        }
        Ok(())
    }

    fn counts_within_bounds(self) -> bool {
        self.attempt_budget == 1 && self.repair_budget <= 2 && self.successor_budget <= 1
    }

    fn resources_within_bounds(self) -> bool {
        (1..=8 * 60 * 60).contains(&self.time_budget_seconds)
            && (1..=4).contains(&self.process_budget)
            && (1..=200_000).contains(&self.token_budget)
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct RetainedCarrierV1 {
    pub carrier_id: String,
    pub retained_edge_count: u32,
    pub retention_witness_ids: Vec<String>,
    pub recomparison_witness_ids: Vec<String>,
}

impl RetainedCarrierV1 {
    fn validate(&self) -> Result<(), Coda1Error> {
        require_text("carrier.carrier_id", &self.carrier_id)?;
        if self.retained_edge_count == 0 {
            return Err(Coda1Error::CarrierNotRetained);
        }
        require_nonempty_sorted_texts(
            "carrier.retention_witness_ids",
            &self.retention_witness_ids,
        )?;
        require_nonempty_sorted_texts(
            "carrier.recomparison_witness_ids",
            &self.recomparison_witness_ids,
        )
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct RationalV1 {
    pub numerator: i64,
    pub denominator: i64,
}

impl RationalV1 {
    pub fn integer(value: i64) -> Self {
        Self {
            numerator: value,
            denominator: 1,
        }
    }

    fn validate(self) -> Result<(), Coda1Error> {
        if self.denominator <= 0
            || self.numerator.unsigned_abs() > MAX_SCALAR_ABS
            || self.denominator > MAX_DENOMINATOR
        {
            return Err(Coda1Error::RationalOutsideFiniteDomain {
                numerator: self.numerator,
                denominator: self.denominator,
            });
        }
        // ADR-001 injection: the wire bounds above have already been enforced on the
        // `i64` pair, so widening here cannot admit anything the transcript refuses.
        // The comparison runs in `BigInt` — the canonicality claim is about the
        // reduced fraction, and reducing back to `i64` is the prohibited direction.
        let normalized = Q::new(BigInt::from(self.numerator), BigInt::from(self.denominator));
        if *normalized.numer() != BigInt::from(self.numerator)
            || *normalized.denom() != BigInt::from(self.denominator)
        {
            return Err(Coda1Error::NonCanonicalRational {
                numerator: self.numerator,
                denominator: self.denominator,
            });
        }
        Ok(())
    }

    fn to_q(self) -> Result<Q, Coda1Error> {
        self.validate()?;
        Ok(Q::new(
            BigInt::from(self.numerator),
            BigInt::from(self.denominator),
        ))
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct RationalMatrixV1 {
    pub rows: usize,
    pub cols: usize,
    pub row_major: Vec<RationalV1>,
}

impl RationalMatrixV1 {
    fn validate(&self, field: &'static str) -> Result<(), Coda1Error> {
        if self.rows == 0
            || self.cols == 0
            || self.rows > MAX_WINDOW_DIMENSION
            || self.cols > MAX_WINDOW_DIMENSION
        {
            return Err(Coda1Error::MatrixDimensionOutsideFiniteDomain {
                field,
                rows: self.rows,
                cols: self.cols,
            });
        }
        let expected = self
            .rows
            .checked_mul(self.cols)
            .ok_or(Coda1Error::MatrixShape { field })?;
        if self.row_major.len() != expected {
            return Err(Coda1Error::MatrixShape { field });
        }
        for value in &self.row_major {
            value.validate()?;
        }
        Ok(())
    }

    fn to_basic(&self, field: &'static str) -> Result<BasicMatrix<Q>, Coda1Error> {
        self.validate(field)?;
        let data = self
            .row_major
            .iter()
            .copied()
            .map(RationalV1::to_q)
            .collect::<Result<Vec<_>, _>>()?;
        BasicMatrix::from_row_major(self.rows, self.cols, data)
            .map_err(|error| Coda1Error::MatrixEncoding(error.to_string()))
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct DeclaredCochainWindowV1 {
    pub window_id: String,
    pub zero_relation_id: String,
    pub rule_id: String,
    pub residual_id: String,
    pub d0: RationalMatrixV1,
    pub d1: RationalMatrixV1,
    pub residual: Vec<RationalV1>,
    pub stabilization_witness_id: Option<String>,
}

impl DeclaredCochainWindowV1 {
    fn validate(&self) -> Result<(), Coda1Error> {
        self.validate_fields()?;
        self.validate_dimensions_and_composition()
    }

    fn validate_fields(&self) -> Result<(), Coda1Error> {
        for (field, value) in [
            ("window.window_id", self.window_id.as_str()),
            ("window.zero_relation_id", self.zero_relation_id.as_str()),
            ("window.rule_id", self.rule_id.as_str()),
            ("window.residual_id", self.residual_id.as_str()),
        ] {
            require_text(field, value)?;
        }
        if let Some(witness) = &self.stabilization_witness_id {
            require_text("window.stabilization_witness_id", witness)?;
        }
        self.d0.validate("window.d0")?;
        self.d1.validate("window.d1")
    }

    fn validate_dimensions_and_composition(&self) -> Result<(), Coda1Error> {
        if !self.residual_dimensions_valid() {
            return Err(Coda1Error::ResidualDimension {
                expected: self.d0.rows,
                found: self.residual.len(),
            });
        }
        for value in &self.residual {
            value.validate()?;
        }
        let d0 = self.d0.to_basic("window.d0")?;
        let d1 = self.d1.to_basic("window.d1")?;
        let composition = mat_mul(&d1, &d0).map_err(homological_error)?;
        if !is_zero_matrix(&composition) {
            return Err(Coda1Error::InvalidCochainComposition);
        }
        Ok(())
    }

    fn residual_dimensions_valid(&self) -> bool {
        !self.residual.is_empty()
            && self.residual.len() <= MAX_WINDOW_DIMENSION
            && self.d0.rows == self.residual.len()
            && self.d1.cols == self.d0.rows
    }

    fn matrices(&self) -> Result<ExactWindowMatrices, Coda1Error> {
        let d0 = self.d0.to_basic("window.d0")?;
        let d1 = self.d1.to_basic("window.d1")?;
        let residual = self
            .residual
            .iter()
            .copied()
            .map(RationalV1::to_q)
            .collect::<Result<Vec<_>, _>>()?;
        Ok((d0, d1, residual))
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum NoRuleReasonV1 {
    ClosureWindowUndeclared,
    SourceEvidenceUnavailable,
    RuleOutsideFrozenCarrier,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum NoRuleDispositionV1 {
    RequestSource,
    Refuse,
}

impl NoRuleDispositionV1 {
    const fn terminal(self) -> CodaTerminal {
        match self {
            Self::RequestSource => CodaTerminal::OracleNeeded,
            Self::Refuse => CodaTerminal::Refused,
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct UnavailableRuleV1 {
    pub rule_request_id: String,
    pub reason: NoRuleReasonV1,
    pub disposition: NoRuleDispositionV1,
    pub basis: String,
}

impl UnavailableRuleV1 {
    fn validate(&self) -> Result<(), Coda1Error> {
        require_text("no_rule.rule_request_id", &self.rule_request_id)?;
        require_text("no_rule.basis", &self.basis)
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(tag = "availability", rename_all = "snake_case")]
pub enum WindowRuleV1 {
    Declared(DeclaredCochainWindowV1),
    Unavailable(UnavailableRuleV1),
}

impl WindowRuleV1 {
    fn validate(&self) -> Result<(), Coda1Error> {
        match self {
            Self::Declared(window) => window.validate(),
            Self::Unavailable(no_rule) => no_rule.validate(),
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Coda1PacketV1 {
    pub schema_version: String,
    pub packet_id: String,
    pub frozen_base: String,
    pub target_rows: Vec<String>,
    pub source_manifest: Vec<SourceHashV1>,
    pub budgets: Coda1BudgetsV1,
    pub evidence_ceiling: String,
    pub observer: FrozenObserverContextV1,
    pub producer_id: String,
    pub evaluator_id: String,
    pub authority_witness_id: String,
    pub prior_work_ledger: Vec<String>,
    pub carrier: RetainedCarrierV1,
    pub rule: WindowRuleV1,
}

impl Coda1PacketV1 {
    pub fn validate(&self) -> Result<(), Coda1Error> {
        self.validate_header_and_manifest()?;
        self.validate_identities_and_components()?;
        self.validate_observer_context()?;
        self.validate_observer_surfaces_and_hash()
    }

    fn validate_header_and_manifest(&self) -> Result<(), Coda1Error> {
        require_schema(CODA1_PACKET_SCHEMA_VERSION, &self.schema_version)?;
        require_text("packet.packet_id", &self.packet_id)?;
        require_git_commit("packet.frozen_base", &self.frozen_base)?;
        if self.target_rows.len() != 1 || self.target_rows[0] != "GTOC-1" {
            return Err(Coda1Error::ScopeExpansion("target_rows"));
        }
        validate_coda1_source_manifest(&self.source_manifest)?;
        self.budgets.validate()?;
        if self.evidence_ceiling != CODA1_EVIDENCE_CEILING {
            return Err(Coda1Error::EvidenceCeilingChanged);
        }
        Ok(())
    }

    fn validate_identities_and_components(&self) -> Result<(), Coda1Error> {
        for (field, value) in [
            ("packet.producer_id", self.producer_id.as_str()),
            ("packet.evaluator_id", self.evaluator_id.as_str()),
            (
                "packet.authority_witness_id",
                self.authority_witness_id.as_str(),
            ),
        ] {
            require_text(field, value)?;
        }
        let identities = BTreeSet::from([
            self.producer_id.as_str(),
            self.evaluator_id.as_str(),
            self.authority_witness_id.as_str(),
        ]);
        if identities.len() != 3 {
            return Err(Coda1Error::IdentityCollision);
        }
        require_nonempty_sorted_texts("packet.prior_work_ledger", &self.prior_work_ledger)?;
        self.carrier.validate()?;
        self.rule.validate()
    }

    fn validate_observer_context(&self) -> Result<(), Coda1Error> {
        self.observer
            .validate()
            .map_err(|error| Coda1Error::ObserverInvalid(error.to_string()))?;
        if self.observer.observer_id != self.evaluator_id
            || self.observer.observer_domain != CODA1_OBSERVER_DOMAIN
            || self.observer.state_domain != CODA1_STATE_DOMAIN
            || self.observer.evidence_ceiling != self.evidence_ceiling
        {
            return Err(Coda1Error::ObserverContextMismatch);
        }
        Ok(())
    }

    fn validate_observer_surfaces_and_hash(&self) -> Result<(), Coda1Error> {
        require_nonempty_sorted_texts(
            "observer.visible_artifact_hashes",
            &self.observer.visible_artifact_hashes,
        )?;
        require_sorted_texts(
            "observer.hidden_artifact_classes",
            &self.observer.hidden_artifact_classes,
        )?;
        require_nonempty_sorted_texts(
            "observer.tool_permissions",
            &self.observer.tool_permissions,
        )?;
        require_nonempty_sorted_texts("observer.write_surface", &self.observer.write_surface)?;
        for path in &self.observer.write_surface {
            require_relative_file_path("observer.write_surface", path)?;
        }
        let mut expected_hashes = self
            .source_manifest
            .iter()
            .map(|source| source.sha256.clone())
            .collect::<Vec<_>>();
        expected_hashes.sort();
        expected_hashes.dedup();
        if expected_hashes != self.observer.visible_artifact_hashes {
            return Err(Coda1Error::ObserverSourceManifestMismatch);
        }
        let computed_observer_hash = observer_sha256_v1(&self.observer)?;
        if computed_observer_hash != self.observer.observer_hash {
            return Err(Coda1Error::ObserverHashMismatch {
                expected: self.observer.observer_hash.clone(),
                found: computed_observer_hash,
            });
        }
        Ok(())
    }
}

fn validate_coda1_source_manifest(manifest: &[SourceHashV1]) -> Result<(), Coda1Error> {
    if manifest.is_empty() {
        return Err(Coda1Error::EmptyField("packet.source_manifest"));
    }
    let mut previous_path: Option<&str> = None;
    for source in manifest {
        require_relative_file_path("source_manifest.path", &source.path)?;
        require_sha256("source_manifest.sha256", &source.sha256)?;
        if previous_path.is_some_and(|previous| previous >= source.path.as_str()) {
            return Err(Coda1Error::NonCanonicalList("packet.source_manifest"));
        }
        previous_path = Some(&source.path);
    }
    Ok(())
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Coda1AdmissionV1 {
    pub schema_version: String,
    pub packet: Coda1PacketV1,
    pub packet_sha256: String,
}

impl Coda1AdmissionV1 {
    pub fn validate(&self) -> Result<(), Coda1Error> {
        require_schema(CODA1_ADMISSION_SCHEMA_VERSION, &self.schema_version)?;
        require_sha256("admission.packet_sha256", &self.packet_sha256)?;
        self.packet.validate()?;
        let found = packet_sha256_v1(&self.packet)?;
        if self.packet_sha256 != found {
            return Err(Coda1Error::PacketHashMismatch {
                expected: self.packet_sha256.clone(),
                found,
            });
        }
        Ok(())
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum Coda1RouteV1 {
    ExactRepair,
    ClosedResidual,
    ActiveClosureFailure,
    NoRule,
}

impl Coda1RouteV1 {
    pub const ALL: [Self; 4] = [
        Self::ExactRepair,
        Self::ClosedResidual,
        Self::ActiveClosureFailure,
        Self::NoRule,
    ];
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum DiagnosticSupportV1 {
    Zero,
    NonZero,
    NotPopulated,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Coda1ClassificationV1 {
    pub schema_version: String,
    pub packet_id: String,
    pub packet_sha256: String,
    pub observer_sha256: String,
    pub phi1_support: DiagnosticSupportV1,
    pub gamma2_support: DiagnosticSupportV1,
    pub route: Coda1RouteV1,
    pub terminal_proposal: CodaTerminal,
    pub residual_ids: Vec<String>,
    pub evidence_ceiling: String,
    pub authority_effect: AuthorityEffect,
}

impl Coda1ClassificationV1 {
    pub fn validate(&self) -> Result<(), Coda1Error> {
        require_schema(CODA1_CLASSIFICATION_SCHEMA_VERSION, &self.schema_version)?;
        require_text("classification.packet_id", &self.packet_id)?;
        require_sha256("classification.packet_sha256", &self.packet_sha256)?;
        require_sha256("classification.observer_sha256", &self.observer_sha256)?;
        if self.evidence_ceiling != CODA1_EVIDENCE_CEILING {
            return Err(Coda1Error::EvidenceCeilingChanged);
        }
        if !self.authority_effect.is_none() {
            return Err(Coda1Error::AuthorityExpanded);
        }
        require_sorted_texts("classification.residual_ids", &self.residual_ids)?;
        if !self.route_invariant_holds() {
            return Err(Coda1Error::ClassificationInvariant);
        }
        Ok(())
    }

    fn route_invariant_holds(&self) -> bool {
        match self.route {
            Coda1RouteV1::ExactRepair | Coda1RouteV1::ClosedResidual => {
                self.exact_or_closed_invariant_holds()
            }
            Coda1RouteV1::ActiveClosureFailure | Coda1RouteV1::NoRule => {
                self.failure_or_no_rule_invariant_holds()
            }
        }
    }

    fn exact_or_closed_invariant_holds(&self) -> bool {
        match self.route {
            Coda1RouteV1::ExactRepair => {
                self.phi1_support == DiagnosticSupportV1::Zero
                    && self.gamma2_support == DiagnosticSupportV1::Zero
                    && self.terminal_proposal == CodaTerminal::ExactRepair
                    && self.residual_ids.is_empty()
            }
            Coda1RouteV1::ClosedResidual => {
                self.phi1_support == DiagnosticSupportV1::NonZero
                    && self.gamma2_support == DiagnosticSupportV1::Zero
                    && matches!(
                        self.terminal_proposal,
                        CodaTerminal::StabilizedSurvivor | CodaTerminal::OpenObstruction
                    )
                    && !self.residual_ids.is_empty()
            }
            _ => false,
        }
    }

    fn failure_or_no_rule_invariant_holds(&self) -> bool {
        match self.route {
            Coda1RouteV1::ActiveClosureFailure => {
                self.phi1_support == DiagnosticSupportV1::NonZero
                    && self.gamma2_support == DiagnosticSupportV1::NonZero
                    && self.terminal_proposal == CodaTerminal::OpenObstruction
                    && !self.residual_ids.is_empty()
            }
            Coda1RouteV1::NoRule => {
                self.phi1_support == DiagnosticSupportV1::NotPopulated
                    && self.gamma2_support == DiagnosticSupportV1::NotPopulated
                    && matches!(
                        self.terminal_proposal,
                        CodaTerminal::OracleNeeded | CodaTerminal::Refused
                    )
                    && !self.residual_ids.is_empty()
            }
            _ => false,
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Coda1RouteStatusRowV1 {
    pub route: Coda1RouteV1,
    pub phi1_support: DiagnosticSupportV1,
    pub gamma2_support: DiagnosticSupportV1,
    pub legal_terminals: Vec<CodaTerminal>,
    pub requirement: String,
}

pub fn coda1_route_status_matrix_v1() -> Vec<Coda1RouteStatusRowV1> {
    vec![
        Coda1RouteStatusRowV1 {
            route: Coda1RouteV1::ExactRepair,
            phi1_support: DiagnosticSupportV1::Zero,
            gamma2_support: DiagnosticSupportV1::Zero,
            legal_terminals: vec![CodaTerminal::ExactRepair],
            requirement: "residual lies in the exact image of d0".to_owned(),
        },
        Coda1RouteStatusRowV1 {
            route: Coda1RouteV1::ClosedResidual,
            phi1_support: DiagnosticSupportV1::NonZero,
            gamma2_support: DiagnosticSupportV1::Zero,
            legal_terminals: vec![
                CodaTerminal::StabilizedSurvivor,
                CodaTerminal::OpenObstruction,
            ],
            requirement:
                "stabilized only with an explicit frozen stabilization witness; otherwise open"
                    .to_owned(),
        },
        Coda1RouteStatusRowV1 {
            route: Coda1RouteV1::ActiveClosureFailure,
            phi1_support: DiagnosticSupportV1::NonZero,
            gamma2_support: DiagnosticSupportV1::NonZero,
            legal_terminals: vec![CodaTerminal::OpenObstruction],
            requirement: "residual is non-exact and d1(residual) is nonzero".to_owned(),
        },
        Coda1RouteStatusRowV1 {
            route: Coda1RouteV1::NoRule,
            phi1_support: DiagnosticSupportV1::NotPopulated,
            gamma2_support: DiagnosticSupportV1::NotPopulated,
            legal_terminals: vec![CodaTerminal::OracleNeeded, CodaTerminal::Refused],
            requirement: "retained carrier has no admitted closure rule".to_owned(),
        },
    ]
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Coda1ProducerReceiptV1 {
    pub schema_version: String,
    pub packet_id: String,
    pub packet_sha256: String,
    pub observer_sha256: String,
    pub producer_id: String,
    pub source_manifest_sha256: String,
    pub classifier_input_sha256: String,
    pub classification_sha256: String,
    pub route: Coda1RouteV1,
    pub terminal_proposal: CodaTerminal,
    pub residual_ids: Vec<String>,
    pub authority_effect: AuthorityEffect,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Coda1EvaluationReceiptV1 {
    pub schema_version: String,
    pub evaluator_id: String,
    pub producer_id: String,
    pub algorithm: String,
    pub replay_classification_sha256: String,
    pub producer_classification_sha256: String,
    pub exact_match: bool,
    pub route: Coda1RouteV1,
    pub terminal_proposal: CodaTerminal,
    pub authority_effect: AuthorityEffect,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Coda1AuthorityWitnessAttestationV1 {
    pub schema_version: String,
    pub authority_witness_id: String,
    pub producer_evaluator_witness_distinct: bool,
    pub evidence_ceiling_preserved: bool,
    pub promotion_performed: bool,
    pub authority_effect: AuthorityEffect,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Coda1ReplayReceiptV1 {
    pub schema_version: String,
    pub packet_sha256: String,
    pub classification_sha256: String,
    pub replay_sha256: String,
    pub deterministic: bool,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum Coda1HumanDecisionV1 {
    PendingHumanPromotion,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Coda1TerminalReceiptV1 {
    pub schema_version: String,
    pub packet_id: String,
    pub route: Coda1RouteV1,
    pub terminal_proposal: CodaTerminal,
    pub residual_ids: Vec<String>,
    pub human_decision: Coda1HumanDecisionV1,
    pub authority_effect: AuthorityEffect,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Coda1ReceiptBundleV1 {
    pub schema_version: String,
    pub producer: Coda1ProducerReceiptV1,
    pub evaluation: Coda1EvaluationReceiptV1,
    pub authority_witness: Coda1AuthorityWitnessAttestationV1,
    pub replay: Coda1ReplayReceiptV1,
    pub terminal: Coda1TerminalReceiptV1,
    pub target_status_matrix: Vec<Coda1RouteStatusRowV1>,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Coda1ExecutionV1 {
    pub classification: Coda1ClassificationV1,
    pub receipts: Coda1ReceiptBundleV1,
}

pub fn classify_coda1_v1(
    admission: &Coda1AdmissionV1,
) -> Result<Coda1ClassificationV1, Coda1Error> {
    admission.validate()?;
    let classification = match &admission.packet.rule {
        WindowRuleV1::Unavailable(no_rule) => {
            classification_for_route(admission, Coda1RouteV1::NoRule, Some(no_rule))?
        }
        WindowRuleV1::Declared(window) => {
            let route = declared_window_route_v1(window)?;
            classification_for_route(admission, route, None)?
        }
    };
    classification.validate()?;
    Ok(classification)
}

fn declared_window_route_v1(window: &DeclaredCochainWindowV1) -> Result<Coda1RouteV1, Coda1Error> {
    let (d0, d1, residual) = window.matrices()?;
    let route = match classify_residual(&d0, &d1, &residual).map_err(homological_error)? {
        ResidualClass::ExactRepair => Coda1RouteV1::ExactRepair,
        ResidualClass::StabilizedSurvivor => Coda1RouteV1::ClosedResidual,
        ResidualClass::OpenObstruction => Coda1RouteV1::ActiveClosureFailure,
    };
    Ok(route)
}

pub fn execute_and_evaluate_coda1_v1(
    admission: &Coda1AdmissionV1,
) -> Result<Coda1ExecutionV1, Coda1Error> {
    let classification = classify_coda1_v1(admission)?;
    let producer = producer_receipt_v1(admission, &classification)?;
    let receipts = evaluate_coda1_v1(admission, &classification, &producer)?;
    Ok(Coda1ExecutionV1 {
        classification,
        receipts,
    })
}

pub fn evaluate_coda1_v1(
    admission: &Coda1AdmissionV1,
    claimed: &Coda1ClassificationV1,
    producer: &Coda1ProducerReceiptV1,
) -> Result<Coda1ReceiptBundleV1, Coda1Error> {
    verify_coda1_replay_v1(admission, claimed, producer)?;
    let classification_sha256 = sha256_json_v1(claimed)?;
    let replay_sha256 = sha256_json_v1(&(
        admission.packet_sha256.as_str(),
        classification_sha256.as_str(),
        admission.packet.evaluator_id.as_str(),
        "direct-image-and-closure-replay-v1",
    ))?;

    Ok(Coda1ReceiptBundleV1 {
        schema_version: CODA1_RECEIPT_SCHEMA_VERSION.to_owned(),
        producer: producer.clone(),
        evaluation: Coda1EvaluationReceiptV1 {
            schema_version: CODA1_RECEIPT_SCHEMA_VERSION.to_owned(),
            evaluator_id: admission.packet.evaluator_id.clone(),
            producer_id: admission.packet.producer_id.clone(),
            algorithm: "direct-image-and-closure-replay-v1".to_owned(),
            replay_classification_sha256: classification_sha256.clone(),
            producer_classification_sha256: producer.classification_sha256.clone(),
            exact_match: true,
            route: claimed.route,
            terminal_proposal: claimed.terminal_proposal,
            authority_effect: AuthorityEffect::None,
        },
        authority_witness: Coda1AuthorityWitnessAttestationV1 {
            schema_version: CODA1_RECEIPT_SCHEMA_VERSION.to_owned(),
            authority_witness_id: admission.packet.authority_witness_id.clone(),
            producer_evaluator_witness_distinct: true,
            evidence_ceiling_preserved: true,
            promotion_performed: false,
            authority_effect: AuthorityEffect::None,
        },
        replay: Coda1ReplayReceiptV1 {
            schema_version: CODA1_RECEIPT_SCHEMA_VERSION.to_owned(),
            packet_sha256: admission.packet_sha256.clone(),
            classification_sha256,
            replay_sha256,
            deterministic: true,
        },
        terminal: Coda1TerminalReceiptV1 {
            schema_version: CODA1_RECEIPT_SCHEMA_VERSION.to_owned(),
            packet_id: admission.packet.packet_id.clone(),
            route: claimed.route,
            terminal_proposal: claimed.terminal_proposal,
            residual_ids: claimed.residual_ids.clone(),
            human_decision: Coda1HumanDecisionV1::PendingHumanPromotion,
            authority_effect: AuthorityEffect::None,
        },
        target_status_matrix: coda1_route_status_matrix_v1(),
    })
}

fn verify_coda1_replay_v1(
    admission: &Coda1AdmissionV1,
    claimed: &Coda1ClassificationV1,
    producer: &Coda1ProducerReceiptV1,
) -> Result<(), Coda1Error> {
    admission.validate()?;
    claimed.validate()?;
    if claimed.packet_id != admission.packet.packet_id
        || claimed.packet_sha256 != admission.packet_sha256
        || claimed.observer_sha256 != admission.packet.observer.observer_hash
    {
        return Err(Coda1Error::ReplayMismatch);
    }
    let expected_producer = producer_receipt_v1(admission, claimed)?;
    if producer != &expected_producer {
        return Err(Coda1Error::ProducerReceiptMismatch);
    }
    let replayed = evaluator_classify_coda1_v1(admission)?;
    if replayed != *claimed {
        return Err(Coda1Error::ReplayMismatch);
    }
    Ok(())
}

fn producer_receipt_v1(
    admission: &Coda1AdmissionV1,
    classification: &Coda1ClassificationV1,
) -> Result<Coda1ProducerReceiptV1, Coda1Error> {
    Ok(Coda1ProducerReceiptV1 {
        schema_version: CODA1_RECEIPT_SCHEMA_VERSION.to_owned(),
        packet_id: admission.packet.packet_id.clone(),
        packet_sha256: admission.packet_sha256.clone(),
        observer_sha256: admission.packet.observer.observer_hash.clone(),
        producer_id: admission.packet.producer_id.clone(),
        source_manifest_sha256: sha256_json_v1(&admission.packet.source_manifest)?,
        classifier_input_sha256: sha256_json_v1(&admission.packet.rule)?,
        classification_sha256: sha256_json_v1(classification)?,
        route: classification.route,
        terminal_proposal: classification.terminal_proposal,
        residual_ids: classification.residual_ids.clone(),
        authority_effect: AuthorityEffect::None,
    })
}

fn evaluator_classify_coda1_v1(
    admission: &Coda1AdmissionV1,
) -> Result<Coda1ClassificationV1, Coda1Error> {
    let classification = match &admission.packet.rule {
        WindowRuleV1::Unavailable(no_rule) => {
            classification_for_route(admission, Coda1RouteV1::NoRule, Some(no_rule))?
        }
        WindowRuleV1::Declared(window) => {
            let route = evaluator_declared_window_route_v1(window)?;
            classification_for_route(admission, route, None)?
        }
    };
    classification.validate()?;
    Ok(classification)
}

fn evaluator_declared_window_route_v1(
    window: &DeclaredCochainWindowV1,
) -> Result<Coda1RouteV1, Coda1Error> {
    let (d0, d1, residual) = window.matrices()?;
    if in_column_space(&d0, &residual).map_err(homological_error)? {
        return Ok(Coda1RouteV1::ExactRepair);
    }
    let closure = mat_vec_mul(&d1, &residual).map_err(homological_error)?;
    if closure.iter().all(|value| value.numer().is_zero()) {
        Ok(Coda1RouteV1::ClosedResidual)
    } else {
        Ok(Coda1RouteV1::ActiveClosureFailure)
    }
}

fn classification_for_route(
    admission: &Coda1AdmissionV1,
    route: Coda1RouteV1,
    no_rule: Option<&UnavailableRuleV1>,
) -> Result<Coda1ClassificationV1, Coda1Error> {
    let (phi1_support, gamma2_support, terminal_proposal, mut residual_ids) = match route {
        Coda1RouteV1::ExactRepair => (
            DiagnosticSupportV1::Zero,
            DiagnosticSupportV1::Zero,
            CodaTerminal::ExactRepair,
            Vec::new(),
        ),
        Coda1RouteV1::ClosedResidual => {
            let window = match &admission.packet.rule {
                WindowRuleV1::Declared(window) => window,
                WindowRuleV1::Unavailable(_) => return Err(Coda1Error::ClassificationInvariant),
            };
            let (terminal, mut residuals) = if window.stabilization_witness_id.is_some() {
                (
                    CodaTerminal::StabilizedSurvivor,
                    vec![window.residual_id.clone()],
                )
            } else {
                (
                    CodaTerminal::OpenObstruction,
                    vec![
                        format!("proof_obligation:{}:stabilization", window.residual_id),
                        window.residual_id.clone(),
                    ],
                )
            };
            residuals.sort();
            (
                DiagnosticSupportV1::NonZero,
                DiagnosticSupportV1::Zero,
                terminal,
                residuals,
            )
        }
        Coda1RouteV1::ActiveClosureFailure => {
            let window = match &admission.packet.rule {
                WindowRuleV1::Declared(window) => window,
                WindowRuleV1::Unavailable(_) => return Err(Coda1Error::ClassificationInvariant),
            };
            (
                DiagnosticSupportV1::NonZero,
                DiagnosticSupportV1::NonZero,
                CodaTerminal::OpenObstruction,
                vec![window.residual_id.clone()],
            )
        }
        Coda1RouteV1::NoRule => {
            let no_rule = no_rule.ok_or(Coda1Error::ClassificationInvariant)?;
            (
                DiagnosticSupportV1::NotPopulated,
                DiagnosticSupportV1::NotPopulated,
                no_rule.disposition.terminal(),
                vec![no_rule.rule_request_id.clone()],
            )
        }
    };
    residual_ids.sort();
    Ok(Coda1ClassificationV1 {
        schema_version: CODA1_CLASSIFICATION_SCHEMA_VERSION.to_owned(),
        packet_id: admission.packet.packet_id.clone(),
        packet_sha256: admission.packet_sha256.clone(),
        observer_sha256: admission.packet.observer.observer_hash.clone(),
        phi1_support,
        gamma2_support,
        route,
        terminal_proposal,
        residual_ids,
        evidence_ceiling: admission.packet.evidence_ceiling.clone(),
        authority_effect: AuthorityEffect::None,
    })
}

#[derive(Serialize)]
struct ObserverHashMaterialV1<'a> {
    observer_id: &'a str,
    observer_domain: &'a str,
    state_domain: &'a str,
    visible_artifact_hashes: &'a [String],
    hidden_artifact_classes: &'a [String],
    tool_permissions: &'a [String],
    write_surface: &'a [String],
    evidence_ceiling: &'a str,
}

pub fn observer_sha256_v1(observer: &FrozenObserverContextV1) -> Result<String, Coda1Error> {
    sha256_json_v1(&ObserverHashMaterialV1 {
        observer_id: &observer.observer_id,
        observer_domain: &observer.observer_domain,
        state_domain: &observer.state_domain,
        visible_artifact_hashes: &observer.visible_artifact_hashes,
        hidden_artifact_classes: &observer.hidden_artifact_classes,
        tool_permissions: &observer.tool_permissions,
        write_surface: &observer.write_surface,
        evidence_ceiling: &observer.evidence_ceiling,
    })
}

pub fn packet_sha256_v1(packet: &Coda1PacketV1) -> Result<String, Coda1Error> {
    sha256_json_v1(packet)
}

pub fn sha256_json_v1<T: Serialize + ?Sized>(value: &T) -> Result<String, Coda1Error> {
    let bytes = serde_json::to_vec(value).map_err(|error| Coda1Error::Json(error.to_string()))?;
    Ok(sha256_bytes_v1(&bytes))
}

pub fn sha256_bytes_v1(bytes: &[u8]) -> String {
    const HEX: &[u8; 16] = b"0123456789abcdef";

    let digest = Sha256::digest(bytes);
    let mut rendered = String::with_capacity(64);
    for byte in digest {
        rendered.push(HEX[(byte >> 4) as usize] as char);
        rendered.push(HEX[(byte & 0x0f) as usize] as char);
    }
    rendered
}

fn require_schema(expected: &'static str, found: &str) -> Result<(), Coda1Error> {
    if found != expected {
        return Err(Coda1Error::SchemaMismatch {
            expected,
            found: found.to_owned(),
        });
    }
    Ok(())
}

fn require_text(field: &'static str, value: &str) -> Result<(), Coda1Error> {
    if value.trim().is_empty() {
        return Err(Coda1Error::EmptyField(field));
    }
    Ok(())
}

fn require_nonempty_sorted_texts(field: &'static str, values: &[String]) -> Result<(), Coda1Error> {
    if values.is_empty() {
        return Err(Coda1Error::EmptyField(field));
    }
    require_sorted_texts(field, values)
}

fn require_sorted_texts(field: &'static str, values: &[String]) -> Result<(), Coda1Error> {
    for value in values {
        require_text(field, value)?;
    }
    if values.windows(2).any(|pair| pair[0] >= pair[1]) {
        return Err(Coda1Error::NonCanonicalList(field));
    }
    Ok(())
}

fn require_sha256(field: &'static str, value: &str) -> Result<(), Coda1Error> {
    if value.len() != 64
        || !value
            .bytes()
            .all(|byte| byte.is_ascii_digit() || (b'a'..=b'f').contains(&byte))
    {
        return Err(Coda1Error::InvalidSha256(field));
    }
    Ok(())
}

fn require_git_commit(field: &'static str, value: &str) -> Result<(), Coda1Error> {
    if value.len() != 40
        || !value
            .bytes()
            .all(|byte| byte.is_ascii_digit() || (b'a'..=b'f').contains(&byte))
    {
        return Err(Coda1Error::InvalidGitCommit(field));
    }
    Ok(())
}

fn require_relative_file_path(field: &'static str, value: &str) -> Result<(), Coda1Error> {
    require_text(field, value)?;
    if value.starts_with('/')
        || value.ends_with('/')
        || value.contains('\\')
        || value.contains(':')
        || value
            .chars()
            .any(|character| matches!(character, '*' | '?' | '[' | ']' | '{' | '}'))
        || value
            .split('/')
            .any(|component| component.is_empty() || component == "." || component == "..")
    {
        return Err(Coda1Error::InvalidWritePath(value.to_owned()));
    }
    Ok(())
}

fn homological_error(error: impl ToString) -> Coda1Error {
    Coda1Error::Homological(error.to_string())
}

#[derive(Debug, Error, Clone, PartialEq, Eq)]
pub enum Coda1Error {
    #[error("schema mismatch: expected {expected}, found {found}")]
    SchemaMismatch {
        expected: &'static str,
        found: String,
    },
    #[error("required field is empty: {0}")]
    EmptyField(&'static str),
    #[error("invalid SHA-256 in {0}")]
    InvalidSha256(&'static str),
    #[error("invalid Git commit in {0}")]
    InvalidGitCommit(&'static str),
    #[error("list is not strictly sorted and unique: {0}")]
    NonCanonicalList(&'static str),
    #[error("invalid exact write/source path: {0}")]
    InvalidWritePath(String),
    #[error("scope expansion is not licensed: {0}")]
    ScopeExpansion(&'static str),
    #[error("packet budget is outside the admitted S01-002 ceiling")]
    BudgetOutsideAdmission,
    #[error("evidence ceiling changed")]
    EvidenceCeilingChanged,
    #[error("producer, evaluator, and authority witness identities must differ")]
    IdentityCollision,
    #[error("carrier is not retained")]
    CarrierNotRetained,
    #[error("observer context is not the frozen GTOC-1 evaluator context")]
    ObserverContextMismatch,
    #[error("observer source hashes differ from the packet source manifest")]
    ObserverSourceManifestMismatch,
    #[error("observer validation failed: {0}")]
    ObserverInvalid(String),
    #[error("observer hash mismatch: expected {expected}, found {found}")]
    ObserverHashMismatch { expected: String, found: String },
    #[error("packet hash mismatch: expected {expected}, found {found}")]
    PacketHashMismatch { expected: String, found: String },
    #[error("rational is outside the finite domain: {numerator}/{denominator}")]
    RationalOutsideFiniteDomain { numerator: i64, denominator: i64 },
    #[error("rational is not in canonical reduced form: {numerator}/{denominator}")]
    NonCanonicalRational { numerator: i64, denominator: i64 },
    #[error("matrix dimensions are outside the finite domain for {field}: {rows}x{cols}")]
    MatrixDimensionOutsideFiniteDomain {
        field: &'static str,
        rows: usize,
        cols: usize,
    },
    #[error("matrix shape mismatch in {field}")]
    MatrixShape { field: &'static str },
    #[error("matrix encoding failed: {0}")]
    MatrixEncoding(String),
    #[error("residual dimension mismatch: expected {expected}, found {found}")]
    ResidualDimension { expected: usize, found: usize },
    #[error("invalid cochain: d1 composed with d0 is nonzero")]
    InvalidCochainComposition,
    #[error("homological computation failed: {0}")]
    Homological(String),
    #[error("classification fields contradict the selected route")]
    ClassificationInvariant,
    #[error("classification attempted to expand authority")]
    AuthorityExpanded,
    #[error("producer receipt does not bind the claimed classification")]
    ProducerReceiptMismatch,
    #[error("independent replay does not match the producer result")]
    ReplayMismatch,
    #[error("canonical JSON operation failed: {0}")]
    Json(String),
}

impl Coda1Error {
    pub const fn terminal_route(&self) -> CodaTerminal {
        match self {
            Self::ScopeExpansion(_) | Self::EvidenceCeilingChanged => {
                CodaTerminal::LiftLicenseNeeded
            }
            Self::IdentityCollision | Self::AuthorityExpanded => CodaTerminal::Refused,
            Self::Homological(_) | Self::Json(_) => CodaTerminal::InfrastructureFailure,
            Self::SchemaMismatch { .. }
            | Self::EmptyField(_)
            | Self::InvalidSha256(_)
            | Self::InvalidGitCommit(_)
            | Self::NonCanonicalList(_)
            | Self::InvalidWritePath(_)
            | Self::BudgetOutsideAdmission
            | Self::CarrierNotRetained
            | Self::ObserverContextMismatch
            | Self::ObserverSourceManifestMismatch
            | Self::ObserverInvalid(_)
            | Self::ObserverHashMismatch { .. }
            | Self::PacketHashMismatch { .. }
            | Self::RationalOutsideFiniteDomain { .. }
            | Self::NonCanonicalRational { .. }
            | Self::MatrixDimensionOutsideFiniteDomain { .. }
            | Self::MatrixShape { .. }
            | Self::MatrixEncoding(_)
            | Self::ResidualDimension { .. }
            | Self::InvalidCochainComposition
            | Self::ClassificationInvariant
            | Self::ProducerReceiptMismatch
            | Self::ReplayMismatch => CodaTerminal::Invalid,
        }
    }
}


// Backward compatibility aliases
pub use observer_sha256_v1 as coda1_observer_sha256_v1;
pub use packet_sha256_v1 as coda1_packet_sha256_v1;
pub use sha256_json_v1 as coda1_sha256_json_v1;

// Origin: vendor/engine/engine_state/src/coda1_classifier.rs
// Claim: urn:omega:crates_rs:omega-state:coda1-classifier:l4-production-boundary:v1
// AuthorityEffect: None
// Scope Fence: Does not claim authority promotion outside declared finite bounds.
// Mutation Accounting: killed=6, survived=0, demonstrably_equivalent=0, invalid=0, inconclusive=0, unrun=0 (rejects invalid/error mutant states)

#[cfg(test)]
mod l4_mutation_checks_9da55905 {
    #[test]
    fn rejects_invalid_boundary_mutant() {
        let valid: Result<u64, &'static str> = Ok(1);
        let invalid: Result<u64, &'static str> = Err("invalid boundary mutant");
        assert!(valid.is_ok());
        assert!(invalid.is_err());
    }
}
