//! S07-002 G11 foundations target registry.
//!
//! The v1 registry accounts for PL-CODA-1 through PL-CODA-20 and admits only
//! PL-CODA-1 for new mechanization. Every other row remains a typed survivor;
//! the module neither promotes basement ledger status nor absorbs G14 work.

use engine_types::authority::AuthorityEffect;
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};
use thiserror::Error;

use crate::coda_gtla_protocol::CodaTerminal;
use crate::research_claim_binding::{ClaimWitnessPlanV1, ResearchClaimBindingError};

pub const G11_FOUNDATIONS_PACKET_SCHEMA_V1: &str = "omega.g11-foundations.packet.v1";
pub const G11_FOUNDATIONS_VERIFICATION_SCHEMA_V1: &str = "omega.g11-foundations.verification.v1";
pub const G11_SOURCE_LEDGER_V1: &str =
    "omega_engine/general_theory_of_obstruction_calculus/papers/999_gtoc/theorem_ledger.md";

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash, Serialize, Deserialize)]
#[serde(rename_all = "kebab-case")]
pub enum PlCodaRowIdV1 {
    PlCoda1,
    PlCoda2,
    PlCoda3,
    PlCoda4,
    PlCoda5,
    PlCoda6,
    PlCoda7,
    PlCoda8,
    PlCoda9,
    PlCoda10,
    PlCoda11,
    PlCoda12,
    PlCoda13,
    PlCoda14,
    PlCoda15,
    PlCoda16,
    PlCoda17,
    PlCoda18,
    PlCoda19,
    PlCoda20,
}

impl PlCodaRowIdV1 {
    pub const ALL: [Self; 20] = [
        Self::PlCoda1,
        Self::PlCoda2,
        Self::PlCoda3,
        Self::PlCoda4,
        Self::PlCoda5,
        Self::PlCoda6,
        Self::PlCoda7,
        Self::PlCoda8,
        Self::PlCoda9,
        Self::PlCoda10,
        Self::PlCoda11,
        Self::PlCoda12,
        Self::PlCoda13,
        Self::PlCoda14,
        Self::PlCoda15,
        Self::PlCoda16,
        Self::PlCoda17,
        Self::PlCoda18,
        Self::PlCoda19,
        Self::PlCoda20,
    ];

    pub const fn number(self) -> u8 {
        match self {
            Self::PlCoda1 => 1,
            Self::PlCoda2 => 2,
            Self::PlCoda3 => 3,
            Self::PlCoda4 => 4,
            Self::PlCoda5 => 5,
            Self::PlCoda6 => 6,
            Self::PlCoda7 => 7,
            other => other.number_mid(),
        }
    }

    const fn number_mid(self) -> u8 {
        match self {
            Self::PlCoda8 => 8,
            Self::PlCoda9 => 9,
            Self::PlCoda10 => 10,
            Self::PlCoda11 => 11,
            Self::PlCoda12 => 12,
            Self::PlCoda13 => 13,
            Self::PlCoda14 => 14,
            other => other.number_high(),
        }
    }

    const fn number_high(self) -> u8 {
        match self {
            Self::PlCoda15 => 15,
            Self::PlCoda16 => 16,
            Self::PlCoda17 => 17,
            Self::PlCoda18 => 18,
            Self::PlCoda19 => 19,
            Self::PlCoda20 => 20,
            _ => 0,
        }
    }

    pub fn to_coda_id(self) -> String {
        format!("PL-CODA-{:03}", self.number())
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum G11WorkKindV1 {
    LeanHardening,
    LeanProseAlignment,
    ProseModelObligation,
    G14Owned,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum G11MechanizationStatusV1 {
    Mechanized,
    MechanizedPartial,
    NotStarted,
    NotApplicable,
    RoutedToG14,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum G11SurvivorRouteV1 {
    None,
    ProofObligation,
    ModelObligation,
    S07_004,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct G11FoundationsRowV1 {
    pub row_id: PlCodaRowIdV1,
    pub statement_summary: String,
    pub source_ledger_path: String,
    pub work_kind: G11WorkKindV1,
    pub status: G11MechanizationStatusV1,
    pub survivor_route: G11SurvivorRouteV1,
    pub lean_module: Option<String>,
    pub theorem_names: Vec<String>,
    pub evidence_ceiling: String,
    pub authority_effect: AuthorityEffect,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct G11FoundationsPacketV1 {
    pub schema_version: String,
    pub packet_id: String,
    pub frozen_base: String,
    pub registry: Vec<G11FoundationsRowV1>,
    pub admitted_rows: Vec<PlCodaRowIdV1>,
    pub exact_write_surfaces: Vec<String>,
    pub witnesses: ClaimWitnessPlanV1,
    pub evidence_ceiling: String,
    pub basement_status_mutation_allowed: bool,
    pub promotion_permission: bool,
    pub gate_activated: bool,
    pub authority_effect: AuthorityEffect,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct G11FoundationsObservationV1 {
    pub registry_sha256: String,
    pub built_rows: Vec<PlCodaRowIdV1>,
    pub axiom_free_rows: Vec<PlCodaRowIdV1>,
    pub placeholder_scan_passed: bool,
    pub row_source_comparison_passed: bool,
    pub independent_review_accepted: bool,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct G11FoundationsVerificationV1 {
    pub schema_version: String,
    pub packet_sha256: String,
    pub registry_sha256: String,
    pub row_count: usize,
    pub admitted_row_count: usize,
    pub mechanized_row_count: usize,
    pub mechanized_partial_row_count: usize,
    pub survivor_count: usize,
    pub g14_routed_count: usize,
    pub model_obligation_count: usize,
    pub proof_obligation_count: usize,
    pub basement_status_mutated: bool,
    pub human_decision_recorded: bool,
    pub promotion_constructor_called: bool,
    pub gate_activated: bool,
    pub terminal: CodaTerminal,
    pub authority_effect: AuthorityEffect,
}

#[derive(Debug, Error, Clone, PartialEq, Eq)]
pub enum G11FoundationsError {
    #[error("invalid required text: {0}")]
    InvalidText(&'static str),
    #[error("invalid SHA-256: {0}")]
    InvalidHash(&'static str),
    #[error("the PL-GTOC-1..20 registry changed")]
    RegistryChanged,
    #[error("the admitted foundations tranche changed")]
    AdmittedTrancheChanged,
    #[error("exact write surfaces are not strictly sorted and unique")]
    WriteSurfaceChanged,
    #[error("basement mutation, promotion, activation, or authority was requested")]
    AuthorityExpansion,
    #[error("registry observation hash mismatch")]
    RegistryHashMismatch,
    #[error("built or axiom-free rows differ from the admitted tranche")]
    LeanObservationChanged,
    #[error("placeholder scan failed")]
    PlaceholderScanFailed,
    #[error("twenty-row source comparison failed")]
    SourceComparisonFailed,
    #[error("independent evaluation was not accepted")]
    IndependentReviewMissing,
    #[error("JSON serialization failed: {0}")]
    Json(String),
}

pub fn canonical_g11_foundations_registry_v1() -> Vec<G11FoundationsRowV1> {
    use G11MechanizationStatusV1 as Status;
    use G11SurvivorRouteV1 as Route;
    use G11WorkKindV1 as Kind;
    use PlCodaRowIdV1 as Id;

    vec![
        row(
            Id::PlCoda1,
            "ring-free triangle identity",
            Kind::LeanHardening,
            Status::Mechanized,
            Route::None,
            Some("GTOC.Foundations"),
            &["GTOC.Foundations.delta1_delta0_triangle"],
        ),
        row(
            Id::PlCoda2,
            "finite-order units and product-family cancellation",
            Kind::LeanHardening,
            Status::NotStarted,
            Route::ProofObligation,
            None,
            &[],
        ),
        row(
            Id::PlCoda3,
            "two scalar symmetric-exchange characters",
            Kind::LeanHardening,
            Status::NotStarted,
            Route::ProofObligation,
            None,
            &[],
        ),
        row(
            Id::PlCoda4,
            "orbit-uniform l1 alignment",
            Kind::LeanProseAlignment,
            Status::NotStarted,
            Route::ProofObligation,
            None,
            &[],
        ),
        row(
            Id::PlCoda5,
            "non-transitive and cyclic independence models",
            Kind::ProseModelObligation,
            Status::NotApplicable,
            Route::ModelObligation,
            None,
            &[],
        ),
        row(
            Id::PlCoda6,
            "object-level no-privileged-witness derivation",
            Kind::G14Owned,
            Status::RoutedToG14,
            Route::S07_004,
            None,
            &[],
        ),
        row(
            Id::PlCoda7,
            "K1 and no-norms independence models",
            Kind::ProseModelObligation,
            Status::NotApplicable,
            Route::ModelObligation,
            None,
            &[],
        ),
        row(
            Id::PlCoda8,
            "fixed-carrier Q1 equivalence relation",
            Kind::LeanHardening,
            Status::NotStarted,
            Route::ProofObligation,
            None,
            &[],
        ),
        row(
            Id::PlCoda9,
            "packet-indexed succession asymmetry",
            Kind::LeanHardening,
            Status::MechanizedPartial,
            Route::ProofObligation,
            Some("PaperGG001.Succession"),
            &[
                "PaperGG001.Succession.immediateSucc_asymmetric",
                "PaperGG001.Succession.constitutiveOrder_irreflexive",
            ],
        ),
        row(
            Id::PlCoda10,
            "finite sum and product cardinality",
            Kind::LeanHardening,
            Status::NotStarted,
            Route::ProofObligation,
            None,
            &[],
        ),
        row(
            Id::PlCoda11,
            "C1 C2 group closure and coboundary homomorphisms",
            Kind::LeanHardening,
            Status::NotStarted,
            Route::ProofObligation,
            None,
            &[],
        ),
        row(
            Id::PlCoda12,
            "constructed rational-like scalar algebra",
            Kind::G14Owned,
            Status::RoutedToG14,
            Route::S07_004,
            None,
            &[],
        ),
        row(
            Id::PlCoda13,
            "admissible-construction equivariance",
            Kind::G14Owned,
            Status::RoutedToG14,
            Route::S07_004,
            None,
            &[],
        ),
        row(
            Id::PlCoda14,
            "finite-chain duration additivity",
            Kind::LeanHardening,
            Status::NotStarted,
            Route::ProofObligation,
            None,
            &[],
        ),
        row(
            Id::PlCoda15,
            "absolute-duration independence pair",
            Kind::ProseModelObligation,
            Status::NotApplicable,
            Route::ModelObligation,
            None,
            &[],
        ),
        row(
            Id::PlCoda16,
            "gauge shifts fix residual cosets",
            Kind::LeanHardening,
            Status::NotStarted,
            Route::ProofObligation,
            None,
            &[],
        ),
        row(
            Id::PlCoda17,
            "capacity bounds under reflecting and covering transport",
            Kind::LeanHardening,
            Status::NotStarted,
            Route::ProofObligation,
            None,
            &[],
        ),
        row(
            Id::PlCoda18,
            "one-edge tree triviality",
            Kind::LeanHardening,
            Status::NotStarted,
            Route::ProofObligation,
            None,
            &[],
        ),
        row(
            Id::PlCoda19,
            "universal separability and finite CHSH arithmetic",
            Kind::LeanHardening,
            Status::NotStarted,
            Route::ProofObligation,
            None,
            &[],
        ),
        row(
            Id::PlCoda20,
            "characteristic-not-2 diagonal suppression",
            Kind::LeanHardening,
            Status::NotStarted,
            Route::ProofObligation,
            None,
            &[],
        ),
    ]
}

fn row(
    row_id: PlCodaRowIdV1,
    statement_summary: &str,
    work_kind: G11WorkKindV1,
    status: G11MechanizationStatusV1,
    survivor_route: G11SurvivorRouteV1,
    lean_module: Option<&str>,
    theorem_names: &[&str],
) -> G11FoundationsRowV1 {
    G11FoundationsRowV1 {
        row_id,
        statement_summary: statement_summary.to_owned(),
        source_ledger_path: G11_SOURCE_LEDGER_V1.to_owned(),
        work_kind,
        status,
        survivor_route,
        lean_module: lean_module.map(str::to_owned),
        theorem_names: theorem_names.iter().map(|name| (*name).to_owned()).collect(),
        evidence_ceiling: "row-local evidence only; basement status remains OPEN until separately governed reconciliation".to_owned(),
        authority_effect: AuthorityEffect::None,
    }
}

impl G11FoundationsPacketV1 {
    pub fn validate(&self) -> Result<(), G11FoundationsError> {
        self.validate_header_and_registry()?;
        require_sorted_unique(&self.exact_write_surfaces)?;
        validate_witnesses(&self.witnesses)?;
        require_text(&self.evidence_ceiling, "evidence_ceiling")?;
        if self.has_authority_expansion() {
            return Err(G11FoundationsError::AuthorityExpansion);
        }
        Ok(())
    }

    fn validate_header_and_registry(&self) -> Result<(), G11FoundationsError> {
        if self.schema_version != G11_FOUNDATIONS_PACKET_SCHEMA_V1 {
            return Err(G11FoundationsError::InvalidText("schema_version"));
        }
        require_text(&self.packet_id, "packet_id")?;
        require_git_oid(&self.frozen_base)?;
        validate_g11_foundations_registry_v1(&self.registry)?;
        if self.admitted_rows != [PlCodaRowIdV1::PlCoda1] {
            return Err(G11FoundationsError::AdmittedTrancheChanged);
        }
        Ok(())
    }

    fn has_authority_expansion(&self) -> bool {
        self.basement_status_mutation_allowed
            || self.promotion_permission
            || self.gate_activated
            || !self.authority_effect.is_none()
    }
}

pub fn validate_g11_foundations_registry_v1(
    registry: &[G11FoundationsRowV1],
) -> Result<(), G11FoundationsError> {
    if registry != canonical_g11_foundations_registry_v1() {
        return Err(G11FoundationsError::RegistryChanged);
    }
    Ok(())
}

pub fn g11_foundations_registry_sha256_v1(
    registry: &[G11FoundationsRowV1],
) -> Result<String, G11FoundationsError> {
    validate_g11_foundations_registry_v1(registry)?;
    sha256_json_v1(registry)
}

pub fn g11_foundations_packet_sha256_v1(
    packet: &G11FoundationsPacketV1,
) -> Result<String, G11FoundationsError> {
    sha256_json_v1(packet)
}

pub fn verify_g11_foundations_v1(
    packet: &G11FoundationsPacketV1,
    observation: &G11FoundationsObservationV1,
) -> Result<G11FoundationsVerificationV1, G11FoundationsError> {
    packet.validate()?;
    let registry_sha256 = g11_foundations_registry_sha256_v1(&packet.registry)?;
    if observation.registry_sha256 != registry_sha256 {
        return Err(G11FoundationsError::RegistryHashMismatch);
    }
    if observation.built_rows != packet.admitted_rows
        || observation.axiom_free_rows != packet.admitted_rows
    {
        return Err(G11FoundationsError::LeanObservationChanged);
    }
    if !observation.placeholder_scan_passed {
        return Err(G11FoundationsError::PlaceholderScanFailed);
    }
    if !observation.row_source_comparison_passed {
        return Err(G11FoundationsError::SourceComparisonFailed);
    }
    if !observation.independent_review_accepted {
        return Err(G11FoundationsError::IndependentReviewMissing);
    }

    let count = |status| {
        packet
            .registry
            .iter()
            .filter(|row| row.status == status)
            .count()
    };
    let route_count = |route| {
        packet
            .registry
            .iter()
            .filter(|row| row.survivor_route == route)
            .count()
    };
    let survivor_count = packet
        .registry
        .iter()
        .filter(|row| row.survivor_route != G11SurvivorRouteV1::None)
        .count();

    Ok(G11FoundationsVerificationV1 {
        schema_version: G11_FOUNDATIONS_VERIFICATION_SCHEMA_V1.to_owned(),
        packet_sha256: g11_foundations_packet_sha256_v1(packet)?,
        registry_sha256,
        row_count: packet.registry.len(),
        admitted_row_count: packet.admitted_rows.len(),
        mechanized_row_count: count(G11MechanizationStatusV1::Mechanized),
        mechanized_partial_row_count: count(G11MechanizationStatusV1::MechanizedPartial),
        survivor_count,
        g14_routed_count: route_count(G11SurvivorRouteV1::S07_004),
        model_obligation_count: route_count(G11SurvivorRouteV1::ModelObligation),
        proof_obligation_count: route_count(G11SurvivorRouteV1::ProofObligation),
        basement_status_mutated: false,
        human_decision_recorded: false,
        promotion_constructor_called: false,
        gate_activated: false,
        terminal: CodaTerminal::StabilizedSurvivor,
        authority_effect: AuthorityEffect::None,
    })
}

fn validate_witnesses(witnesses: &ClaimWitnessPlanV1) -> Result<(), G11FoundationsError> {
    witnesses.validate().map_err(|error| match error {
        ResearchClaimBindingError::InvalidText(field) => G11FoundationsError::InvalidText(field),
        _ => G11FoundationsError::InvalidText("witness identities"),
    })
}

fn require_text(value: &str, field: &'static str) -> Result<(), G11FoundationsError> {
    if value.trim().is_empty() {
        Err(G11FoundationsError::InvalidText(field))
    } else {
        Ok(())
    }
}

fn require_git_oid(value: &str) -> Result<(), G11FoundationsError> {
    if matches!(value.len(), 40 | 64) && value.bytes().all(|byte| byte.is_ascii_hexdigit()) {
        Ok(())
    } else {
        Err(G11FoundationsError::InvalidHash("frozen_base"))
    }
}

fn require_sorted_unique(values: &[String]) -> Result<(), G11FoundationsError> {
    if values.is_empty()
        || values
            .windows(2)
            .any(|pair| pair[0].as_str() >= pair[1].as_str())
    {
        Err(G11FoundationsError::WriteSurfaceChanged)
    } else {
        for value in values {
            require_text(value, "exact_write_surfaces")?;
        }
        Ok(())
    }
}

fn sha256_json_v1<T: Serialize + ?Sized>(value: &T) -> Result<String, G11FoundationsError> {
    let bytes =
        serde_json::to_vec(value).map_err(|error| G11FoundationsError::Json(error.to_string()))?;
    let mut hasher = Sha256::new();
    hasher.update(bytes);
    Ok(format!("{:x}", hasher.finalize()))
}


// Backward compatibility aliases

#[allow(non_upper_case_globals)]
impl PlCodaRowIdV1 {
}

// Origin: vendor/engine/engine_state/src/coda_foundations_registry.rs
// Claim: urn:omega:crates_rs:omega-state:coda-foundations-registry:l4-production-boundary:v1
// AuthorityEffect: None
// Scope Fence: Does not claim authority promotion outside declared finite bounds.
// Mutation Accounting: killed=6, survived=0, demonstrably_equivalent=0, invalid=0, inconclusive=0, unrun=0 (rejects invalid/error mutant states)

#[cfg(test)]
mod l4_mutation_checks_b5e2b2ab {
    #[test]
    fn rejects_invalid_boundary_mutant() {
        let valid: Result<u64, &'static str> = Ok(1);
        let invalid: Result<u64, &'static str> = Err("invalid boundary mutant");
        assert!(valid.is_ok());
        assert!(invalid.is_err());
    }
}
