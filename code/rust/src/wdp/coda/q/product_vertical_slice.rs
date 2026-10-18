
use std::collections::BTreeMap;
use std::fmt;

use serde::{Deserialize, Serialize};


#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub enum FeatureStatus {
    ExperimentalDisabled,
    ExperimentalEnabled,
    ProductionEnabled,
}

impl FeatureStatus {
    pub fn as_str(self) -> &'static str {
        match self {
            Self::ExperimentalDisabled => "experimental_disabled",
            Self::ExperimentalEnabled => "experimental_enabled",
            Self::ProductionEnabled => "production_enabled",
        }
    }

    pub fn allows_product_mount(self) -> bool {
        matches!(self, Self::ExperimentalEnabled | Self::ProductionEnabled)
    }

    pub fn is_production(self) -> bool {
        matches!(self, Self::ProductionEnabled)
    }
}

pub const Q_CODA_PRODUCT_INTEGRATION: FeatureStatus = FeatureStatus::ExperimentalDisabled;

pub const AUTHORITY_EFFECT: &str = "None";

pub const RELEASE_NOT_CANDIDATE: &str = "NOT_RELEASE_CANDIDATE";

pub const RELEASE_DIAGNOSTIC_ONLY: &str = "DIAGNOSTIC_ONLY_NOT_PROMOTED";

pub const PROMOTION_NOT_PROMOTED: &str = "NOT_PROMOTED";

pub const PROMOTION_PROMOTED: &str = "PROMOTED";

#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash, Serialize, Deserialize)]
#[repr(u8)]
pub enum LaunchTarget {
    Target1 = 1,
    Target2 = 2,
    Target3 = 3,
    Target4 = 4,
    Target5 = 5,
    Target6 = 6,
    Target7 = 7,
}

impl LaunchTarget {
    pub const ALL: [LaunchTarget; 7] = [
        Self::Target1,
        Self::Target2,
        Self::Target3,
        Self::Target4,
        Self::Target5,
        Self::Target6,
        Self::Target7,
    ];

    pub fn id(self) -> u8 {
        self as u8
    }
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct LaunchTargetBoard {
    complete: BTreeMap<u8, bool>,
}

impl Default for LaunchTargetBoard {
    fn default() -> Self {
        let mut complete = BTreeMap::new();
        for t in LaunchTarget::ALL {
            complete.insert(t.id(), false);
        }
        Self { complete }
    }
}

impl LaunchTargetBoard {
    pub fn new() -> Self {
        Self::default()
    }

    pub fn is_complete(&self, target: LaunchTarget) -> bool {
        self.complete.get(&target.id()).copied().unwrap_or(false)
    }

    pub fn mark_complete(&mut self, target: LaunchTarget) {
        self.complete.insert(target.id(), true);
    }

    pub fn all_complete(&self) -> bool {
        LaunchTarget::ALL.iter().all(|t| self.is_complete(*t))
    }

    pub fn incomplete(&self) -> Vec<u8> {
        LaunchTarget::ALL
            .iter()
            .filter(|t| !self.is_complete(**t))
            .map(|t| t.id())
            .collect()
    }
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub enum ProductGateError {
    TargetsIncomplete { incomplete: Vec<u8> },
    SilentProdEnablementRefused {
        requested: FeatureStatus,
        standing: FeatureStatus,
    },
    HumanOnlyPromotionFirewall,
    ProductMountDisabled { standing: FeatureStatus },
}

impl fmt::Display for ProductGateError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::TargetsIncomplete { incomplete } => {
                write!(
                    f,
                    "Q/CODA product integration disabled: launch targets incomplete {incomplete:?}"
                )
            }
            Self::SilentProdEnablementRefused {
                requested,
                standing,
            } => write!(
                f,
                "refused silent PROD enablement (requested={}, standing={})",
                requested.as_str(),
                standing.as_str()
            ),
            Self::HumanOnlyPromotionFirewall => {
                write!(
                    f,
                    "promotion is human-only; PROMOTED is never set by this module"
                )
            }
            Self::ProductMountDisabled { standing } => write!(
                f,
                "Q/CODA product mount disabled (standing={})",
                standing.as_str()
            ),
        }
    }
}

impl std::error::Error for ProductGateError {}

pub fn evaluate_q_coda_integration(board: &LaunchTargetBoard) -> FeatureStatus {
    if !board.all_complete() {
        FeatureStatus::ExperimentalDisabled
    } else {
        Q_CODA_PRODUCT_INTEGRATION
    }
}

pub fn refuse_silent_prod_enablement(requested: FeatureStatus) -> Result<(), ProductGateError> {
    if requested.is_production() {
        return Err(ProductGateError::SilentProdEnablementRefused {
            requested,
            standing: Q_CODA_PRODUCT_INTEGRATION,
        });
    }
    Ok(())
}

pub fn q_coda_product_mount_allowed() -> bool {
    Q_CODA_PRODUCT_INTEGRATION.allows_product_mount()
}

pub fn gate_product_mount(board: &LaunchTargetBoard) -> Result<FeatureStatus, ProductGateError> {
    let status = evaluate_q_coda_integration(board);
    if !board.all_complete() {
        return Err(ProductGateError::TargetsIncomplete {
            incomplete: board.incomplete(),
        });
    }
    if !status.allows_product_mount() {
        return Err(ProductGateError::ProductMountDisabled { standing: status });
    }
    refuse_silent_prod_enablement(status)?;
    Ok(status)
}

pub fn try_auto_promote() -> Result<(), ProductGateError> {
    Err(ProductGateError::HumanOnlyPromotionFirewall)
}


#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub enum ClaimStatus {
    Open,
    Resolved,
    Blocked,
}

impl ClaimStatus {
    pub fn as_str(self) -> &'static str {
        match self {
            Self::Open => "OPEN",
            Self::Resolved => "RESOLVED",
            Self::Blocked => "BLOCKED",
        }
    }
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct ClaimRecord {
    pub claim_id: String,
    pub statement: String,
    pub status: ClaimStatus,
}

impl ClaimRecord {
    pub fn open(claim_id: impl Into<String>, statement: impl Into<String>) -> Self {
        Self {
            claim_id: claim_id.into(),
            statement: statement.into(),
            status: ClaimStatus::Open,
        }
    }

    pub fn resolved(claim_id: impl Into<String>, statement: impl Into<String>) -> Self {
        Self {
            claim_id: claim_id.into(),
            statement: statement.into(),
            status: ClaimStatus::Resolved,
        }
    }
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct ProductProposal {
    pub proposal_id: String,
    pub title: String,
    pub body: String,
    pub seed_claims: Vec<ClaimRecord>,
}

impl ProductProposal {
    pub fn new(
        proposal_id: impl Into<String>,
        title: impl Into<String>,
        body: impl Into<String>,
    ) -> Self {
        Self {
            proposal_id: proposal_id.into(),
            title: title.into(),
            body: body.into(),
            seed_claims: Vec::new(),
        }
    }

    pub fn with_claim(mut self, claim: ClaimRecord) -> Self {
        self.seed_claims.push(claim);
        self
    }
}


#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub enum PipelineStage {
    Proposal,
    PromptReview,
    ScopedResearch,
    DraftPaper,
    AdversarialReview,
    FullReview,
    ManifestBoundZip,
}

impl PipelineStage {
    pub const ALL: [PipelineStage; 7] = [
        Self::Proposal,
        Self::PromptReview,
        Self::ScopedResearch,
        Self::DraftPaper,
        Self::AdversarialReview,
        Self::FullReview,
        Self::ManifestBoundZip,
    ];

    pub fn id(self) -> &'static str {
        match self {
            Self::Proposal => "proposal",
            Self::PromptReview => "prompt_review",
            Self::ScopedResearch => "scoped_research",
            Self::DraftPaper => "draft_paper",
            Self::AdversarialReview => "adversarial_review",
            Self::FullReview => "full_review",
            Self::ManifestBoundZip => "manifest_bound_zip",
        }
    }
}

#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub enum StageStatus {
    Passed,
    Blocked,
    UnresolvedClaims,
}

impl StageStatus {
    pub fn as_str(self) -> &'static str {
        match self {
            Self::Passed => "Passed",
            Self::Blocked => "Blocked",
            Self::UnresolvedClaims => "UnresolvedClaims",
        }
    }
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct StageReceipt {
    pub stage_id: PipelineStage,
    pub status: StageStatus,
    pub unresolved_claims: Vec<String>,
    pub artifact_hash: Option<String>,
}

impl StageReceipt {
    pub fn new(stage_id: PipelineStage, status: StageStatus) -> Self {
        Self {
            stage_id,
            status,
            unresolved_claims: Vec::new(),
            artifact_hash: None,
        }
    }

    pub fn with_unresolved(mut self, claims: Vec<String>) -> Self {
        self.unresolved_claims = claims;
        self
    }

    pub fn with_artifact_hash(mut self, hash: impl Into<String>) -> Self {
        self.artifact_hash = Some(hash.into());
        self
    }
}


#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct PackageManifest {
    pub schema: String,
    pub proposal_id: String,
    pub claim_ids: Vec<String>,
    pub residual_open_claims: Vec<String>,
    pub release_status: String,
    pub promotion: String,
    pub authority_effect: String,
    pub feature_status: String,
    pub package_note: String,
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct ManifestBoundZip {
    pub manifest: PackageManifest,
    pub entries: BTreeMap<String, String>,
    pub package_hash: String,
}

impl ManifestBoundZip {
    pub fn build(
        proposal_id: &str,
        claims: &[ClaimRecord],
        draft_paper: &str,
        stage_receipts: &[StageReceipt],
    ) -> Self {
        let mut claim_ids: Vec<String> = claims.iter().map(|c| c.claim_id.clone()).collect();
        claim_ids.sort();
        claim_ids.dedup();

        let mut residual_open_claims: Vec<String> = claims
            .iter()
            .filter(|c| c.status == ClaimStatus::Open || c.status == ClaimStatus::Blocked)
            .map(|c| format!("{}:{}:{}", c.claim_id, c.status.as_str(), c.statement))
            .collect();
        residual_open_claims.sort();

        let has_residuals = !residual_open_claims.is_empty();
        let release_status = if has_residuals {
            RELEASE_NOT_CANDIDATE.to_string()
        } else {
            RELEASE_DIAGNOSTIC_ONLY.to_string()
        };

        let manifest = PackageManifest {
            schema: "omega.q_coda.product_vertical_slice.manifest.v1".to_string(),
            proposal_id: proposal_id.to_string(),
            claim_ids: claim_ids.clone(),
            residual_open_claims: residual_open_claims.clone(),
            release_status: release_status.clone(),
            promotion: PROMOTION_NOT_PROMOTED.to_string(),
            authority_effect: AUTHORITY_EFFECT.to_string(),
            feature_status: Q_CODA_PRODUCT_INTEGRATION.as_str().to_string(),
            package_note: if has_residuals {
                "residuals remain OPEN/BLOCKED; package is not a release candidate; never auto-promoted"
                    .to_string()
            } else {
                "all claims resolved inside diagnostic pipeline; still NOT_PROMOTED (human-only firewall)"
                    .to_string()
            },
        };

        let mut entries = BTreeMap::new();
        entries.insert("MANIFEST.json".to_string(), stable_json_manifest(&manifest));
        entries.insert("draft_paper.md".to_string(), draft_paper.to_string());
        entries.insert(
            "claims.jsonl".to_string(),
            claims
                .iter()
                .map(|c| {
                    format!(
                        "{{\"claim_id\":{},\"status\":{},\"statement\":{}}}",
                        json_escape(&c.claim_id),
                        json_escape(c.status.as_str()),
                        json_escape(&c.statement)
                    )
                })
                .collect::<Vec<_>>()
                .join("\n"),
        );
        entries.insert(
            "receipts.jsonl".to_string(),
            stage_receipts
                .iter()
                .map(|r| {
                    format!(
                        "{{\"stage_id\":{},\"status\":{},\"unresolved_claims\":{},\"artifact_hash\":{}}}",
                        json_escape(r.stage_id.id()),
                        json_escape(r.status.as_str()),
                        json_string_array(&r.unresolved_claims),
                        r.artifact_hash
                            .as_ref()
                            .map(|h| json_escape(h))
                            .unwrap_or_else(|| "null".to_string())
                    )
                })
                .collect::<Vec<_>>()
                .join("\n"),
        );
        entries.insert(
            "AUTHORITY".to_string(),
            format!(
                "authority_effect={AUTHORITY_EFFECT}\npromotion={PROMOTION_NOT_PROMOTED}\nrelease_status={release_status}\n"
            ),
        );

        let package_hash = hash_hex(&serialize_package_bytes(&entries));

        Self {
            manifest,
            entries,
            package_hash,
        }
    }

    pub fn to_bytes(&self) -> Vec<u8> {
        serialize_package_bytes(&self.entries)
    }

    pub fn release_status(&self) -> &str {
        &self.manifest.release_status
    }

    pub fn residual_open_claims(&self) -> &[String] {
        &self.manifest.residual_open_claims
    }

    pub fn as_temp_dir_map(&self) -> BTreeMap<String, Vec<u8>> {
        self.entries
            .iter()
            .map(|(k, v)| (k.clone(), v.as_bytes().to_vec()))
            .collect()
    }
}

fn serialize_package_bytes(entries: &BTreeMap<String, String>) -> Vec<u8> {
    let mut out = Vec::new();
    out.extend_from_slice(b"OMEGA_MANIFEST_BOUND_ZIP_V1\n");
    for (path, content) in entries {
        out.extend_from_slice(b"FILE\n");
        out.extend_from_slice(path.as_bytes());
        out.push(b'\n');
        out.extend_from_slice(content.len().to_string().as_bytes());
        out.push(b'\n');
        out.extend_from_slice(content.as_bytes());
        out.push(b'\n');
    }
    out
}

fn stable_json_manifest(m: &PackageManifest) -> String {
    format!(
        "{{\n  \"schema\": {},\n  \"proposal_id\": {},\n  \"claim_ids\": {},\n  \"residual_open_claims\": {},\n  \"release_status\": {},\n  \"promotion\": {},\n  \"authority_effect\": {},\n  \"feature_status\": {},\n  \"package_note\": {}\n}}\n",
        json_escape(&m.schema),
        json_escape(&m.proposal_id),
        json_string_array(&m.claim_ids),
        json_string_array(&m.residual_open_claims),
        json_escape(&m.release_status),
        json_escape(&m.promotion),
        json_escape(&m.authority_effect),
        json_escape(&m.feature_status),
        json_escape(&m.package_note),
    )
}

fn json_escape(s: &str) -> String {
    let mut out = String::from("\"");
    for ch in s.chars() {
        match ch {
            '"' => out.push_str("\\\""),
            '\\' => out.push_str("\\\\"),
            '\n' => out.push_str("\\n"),
            '\r' => out.push_str("\\r"),
            '\t' => out.push_str("\\t"),
            c if c.is_control() => out.push_str(&format!("\\u{:04x}", c as u32)),
            c => out.push(c),
        }
    }
    out.push('"');
    out
}

fn json_string_array(items: &[String]) -> String {
    let inner = items
        .iter()
        .map(|s| json_escape(s))
        .collect::<Vec<_>>()
        .join(",");
    format!("[{inner}]")
}

fn hash_hex(bytes: impl AsRef<[u8]>) -> String {
    const FNV_OFFSET: u64 = 0xcbf29ce484222325;
    const FNV_PRIME: u64 = 0x100000001b3;
    let mut hash = FNV_OFFSET;
    for b in bytes.as_ref() {
        hash ^= u64::from(*b);
        hash = hash.wrapping_mul(FNV_PRIME);
    }
    format!("fnv1a64:{hash:016x}")
}


#[derive(Clone, Debug, PartialEq, Eq)]
struct PipelineState {
    proposal: ProductProposal,
    claims: Vec<ClaimRecord>,
    research_notes: String,
    draft_paper: String,
    receipts: Vec<StageReceipt>,
    package: Option<ManifestBoundZip>,
    blocked_reason: Option<String>,
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct VerticalSliceRun {
    pub run_id: String,
    pub proposal_id: String,
    pub receipts: Vec<StageReceipt>,
    pub package: Option<ManifestBoundZip>,
    pub authority_effect: String,
    pub feature_status: FeatureStatus,
    pub release_status: String,
    pub promotion: String,
    pub unresolved_claims: Vec<String>,
}

impl VerticalSliceRun {
    pub fn has_unresolved(&self) -> bool {
        !self.unresolved_claims.is_empty()
    }

    pub fn is_promoted(&self) -> bool {
        self.promotion == PROMOTION_PROMOTED
    }
}

#[derive(Clone, Debug, Default)]
pub struct ProductVerticalSlice;

impl ProductVerticalSlice {
    pub fn new() -> Self {
        Self
    }

    pub fn run(&self, proposal: ProductProposal) -> VerticalSliceRun {
        let run_id = format!("pvs:{}", proposal.proposal_id);
        let mut state = PipelineState {
            claims: proposal.seed_claims.clone(),
            proposal,
            research_notes: String::new(),
            draft_paper: String::new(),
            receipts: Vec::new(),
            package: None,
            blocked_reason: None,
        };

        for stage in PipelineStage::ALL {
            if state.blocked_reason.is_some() && stage != PipelineStage::ManifestBoundZip {
                let open = open_claim_ids(&state.claims);
                state.receipts.push(
                    StageReceipt::new(stage, StageStatus::Blocked)
                        .with_unresolved(open)
                        .with_artifact_hash(hash_hex(
                            state.blocked_reason.as_deref().unwrap_or("blocked"),
                        )),
                );
                continue;
            }
            let receipt = match stage {
                PipelineStage::Proposal => self.stage_proposal(&mut state),
                PipelineStage::PromptReview => self.stage_prompt_review(&mut state),
                PipelineStage::ScopedResearch => self.stage_scoped_research(&mut state),
                PipelineStage::DraftPaper => self.stage_draft_paper(&mut state),
                PipelineStage::AdversarialReview => self.stage_adversarial_review(&mut state),
                PipelineStage::FullReview => self.stage_full_review(&mut state),
                PipelineStage::ManifestBoundZip => self.stage_manifest_bound_zip(&mut state),
            };
            state.receipts.push(receipt);
        }

        let unresolved = open_claim_ids(&state.claims);
        let release_status = state
            .package
            .as_ref()
            .map(|p| p.release_status().to_string())
            .unwrap_or_else(|| RELEASE_NOT_CANDIDATE.to_string());

        VerticalSliceRun {
            run_id,
            proposal_id: state.proposal.proposal_id,
            receipts: state.receipts,
            package: state.package,
            authority_effect: AUTHORITY_EFFECT.to_string(),
            feature_status: Q_CODA_PRODUCT_INTEGRATION,
            release_status,
            promotion: PROMOTION_NOT_PROMOTED.to_string(),
            unresolved_claims: unresolved,
        }
    }

    fn stage_proposal(&self, state: &mut PipelineState) -> StageReceipt {
        let empty_id = state.proposal.proposal_id.trim().is_empty();
        let empty_title = state.proposal.title.trim().is_empty();
        if empty_id || empty_title {
            state.blocked_reason = Some("proposal missing id or title".to_string());
            return StageReceipt::new(PipelineStage::Proposal, StageStatus::Blocked)
                .with_unresolved(open_claim_ids(&state.claims))
                .with_artifact_hash(hash_hex("proposal:blocked"));
        }
        if state.claims.is_empty() {
            state.claims.push(ClaimRecord::open(
                format!("claim:{}:implicit-scope", state.proposal.proposal_id),
                "proposal carried no seed claims; scope residual remains OPEN",
            ));
        }
        let payload = format!(
            "{}|{}|{}",
            state.proposal.proposal_id, state.proposal.title, state.proposal.body
        );
        let open = open_claim_ids(&state.claims);
        let status = if open.is_empty() {
            StageStatus::Passed
        } else {
            StageStatus::UnresolvedClaims
        };
        StageReceipt::new(PipelineStage::Proposal, status)
            .with_unresolved(open)
            .with_artifact_hash(hash_hex(payload))
    }

    fn stage_prompt_review(&self, state: &mut PipelineState) -> StageReceipt {
        let body_ok = state.proposal.body.trim().len() >= 8;
        if !body_ok {
            state.claims.push(ClaimRecord::open(
                format!("claim:{}:prompt-thin", state.proposal.proposal_id),
                "proposal body too thin for scoped research",
            ));
        }
        let open = open_claim_ids(&state.claims);
        let status = if open.is_empty() {
            StageStatus::Passed
        } else {
            StageStatus::UnresolvedClaims
        };
        let review = format!(
            "prompt_review:title_len={}:body_len={}:open={}",
            state.proposal.title.len(),
            state.proposal.body.len(),
            open.len()
        );
        StageReceipt::new(PipelineStage::PromptReview, status)
            .with_unresolved(open)
            .with_artifact_hash(hash_hex(review))
    }

    fn stage_scoped_research(&self, state: &mut PipelineState) -> StageReceipt {
        let mut notes = String::new();
        notes.push_str("# Scoped research (diagnostic)\n");
        notes.push_str(&format!("proposal: {}\n", state.proposal.proposal_id));
        for c in &state.claims {
            notes.push_str(&format!(
                "- [{}] {} — {}\n",
                c.status.as_str(),
                c.claim_id,
                c.statement
            ));
        }
        state.research_notes = notes.clone();
        let open = open_claim_ids(&state.claims);
        let status = if open.is_empty() {
            StageStatus::Passed
        } else {
            StageStatus::UnresolvedClaims
        };
        StageReceipt::new(PipelineStage::ScopedResearch, status)
            .with_unresolved(open)
            .with_artifact_hash(hash_hex(notes))
    }

    fn stage_draft_paper(&self, state: &mut PipelineState) -> StageReceipt {
        let mut draft = String::new();
        draft.push_str(&format!("# {}\n\n", state.proposal.title));
        draft.push_str(&format!(
            "**AuthorityEffect:** `{AUTHORITY_EFFECT}`  \n**Promotion:** `{PROMOTION_NOT_PROMOTED}`  \n**Feature:** `{}`\n\n",
            Q_CODA_PRODUCT_INTEGRATION.as_str()
        ));
        draft.push_str("## Proposal\n\n");
        draft.push_str(&state.proposal.body);
        draft.push_str("\n\n## Research notes\n\n");
        draft.push_str(&state.research_notes);
        draft.push_str("\n## Claims ledger\n\n");
        for c in &state.claims {
            draft.push_str(&format!(
                "- `{}` ({}) {}\n",
                c.claim_id,
                c.status.as_str(),
                c.statement
            ));
        }
        draft.push_str(
            "\n## Residual policy\n\nUnresolved claims remain explicit. This draft is not a release candidate and is never auto-promoted.\n",
        );
        state.draft_paper = draft.clone();
        let open = open_claim_ids(&state.claims);
        let status = if open.is_empty() {
            StageStatus::Passed
        } else {
            StageStatus::UnresolvedClaims
        };
        StageReceipt::new(PipelineStage::DraftPaper, status)
            .with_unresolved(open)
            .with_artifact_hash(hash_hex(draft))
    }

    fn stage_adversarial_review(&self, state: &mut PipelineState) -> StageReceipt {
        if state.draft_paper.trim().is_empty() {
            state.blocked_reason = Some("adversarial review: empty draft".to_string());
            return StageReceipt::new(PipelineStage::AdversarialReview, StageStatus::Blocked)
                .with_unresolved(open_claim_ids(&state.claims))
                .with_artifact_hash(hash_hex("adversarial:empty"));
        }
        let open = open_claim_ids(&state.claims);
        let status = if open.is_empty() {
            StageStatus::Passed
        } else {
            StageStatus::UnresolvedClaims
        };
        let artifact = format!("adversarial:open={}", open.join(","));
        StageReceipt::new(PipelineStage::AdversarialReview, status)
            .with_unresolved(open)
            .with_artifact_hash(hash_hex(artifact))
    }

    fn stage_full_review(&self, state: &mut PipelineState) -> StageReceipt {
        let open = open_claim_ids(&state.claims);
        let status = if open.is_empty() {
            StageStatus::Passed
        } else {
            StageStatus::UnresolvedClaims
        };
        let _ = try_auto_promote();
        StageReceipt::new(PipelineStage::FullReview, status)
            .with_unresolved(open.clone())
            .with_artifact_hash(hash_hex(format!(
                "full_review:open={}:promotion={PROMOTION_NOT_PROMOTED}",
                open.len()
            )))
    }

    fn stage_manifest_bound_zip(&self, state: &mut PipelineState) -> StageReceipt {
        let package = ManifestBoundZip::build(
            &state.proposal.proposal_id,
            &state.claims,
            &state.draft_paper,
            &state.receipts,
        );
        let open = open_claim_ids(&state.claims);
        let status = if state.blocked_reason.is_some() && state.draft_paper.is_empty() {
            StageStatus::Blocked
        } else if !open.is_empty() {
            StageStatus::UnresolvedClaims
        } else {
            StageStatus::Passed
        };
        let hash = package.package_hash.clone();
        debug_assert_ne!(package.manifest.promotion, PROMOTION_PROMOTED);
        debug_assert_eq!(package.manifest.authority_effect, AUTHORITY_EFFECT);
        state.package = Some(package);
        StageReceipt::new(PipelineStage::ManifestBoundZip, status)
            .with_unresolved(open)
            .with_artifact_hash(hash)
    }
}

fn open_claim_ids(claims: &[ClaimRecord]) -> Vec<String> {
    let mut ids: Vec<String> = claims
        .iter()
        .filter(|c| c.status == ClaimStatus::Open || c.status == ClaimStatus::Blocked)
        .map(|c| c.claim_id.clone())
        .collect();
    ids.sort();
    ids.dedup();
    ids
}


#[cfg(test)]
mod tests {
    use super::*;

    fn proposal_with_open_claim() -> ProductProposal {
        ProductProposal::new(
            "prop-001",
            "Q/CODA diagnostic paper",
            "Seed body for scoped research on residual honesty.",
        )
        .with_claim(ClaimRecord::open(
            "claim:coda-cs-bridge",
            "finite-shadow bridge to continuum claim remains OPEN",
        ))
    }

    fn proposal_all_resolved() -> ProductProposal {
        ProductProposal::new(
            "prop-002",
            "Resolved claims diagnostic",
            "Body long enough for prompt review stage.",
        )
        .with_claim(ClaimRecord::resolved(
            "claim:local-finite",
            "finite local claim closed inside diagnostic scope",
        ))
    }

    #[test]
    fn standing_integration_is_experimental_disabled() {
        assert_eq!(
            Q_CODA_PRODUCT_INTEGRATION,
            FeatureStatus::ExperimentalDisabled
        );
        assert!(!q_coda_product_mount_allowed());
        assert!(!Q_CODA_PRODUCT_INTEGRATION.allows_product_mount());
        assert!(!Q_CODA_PRODUCT_INTEGRATION.is_production());
    }

    #[test]
    fn incomplete_targets_force_disabled_integration() {
        let board = LaunchTargetBoard::default();
        assert!(!board.all_complete());
        assert_eq!(
            evaluate_q_coda_integration(&board),
            FeatureStatus::ExperimentalDisabled
        );
        let err = gate_product_mount(&board).expect_err("mount must fail closed");
        match err {
            ProductGateError::TargetsIncomplete { incomplete } => {
                assert_eq!(incomplete, vec![1, 2, 3, 4, 5, 6, 7]);
            }
            other => panic!("unexpected gate error: {other}"),
        }
    }

    #[test]
    fn complete_targets_still_refuse_silent_prod() {
        let mut board = LaunchTargetBoard::new();
        for t in LaunchTarget::ALL {
            board.mark_complete(t);
        }
        assert!(board.all_complete());
        assert_eq!(
            evaluate_q_coda_integration(&board),
            FeatureStatus::ExperimentalDisabled
        );
        assert!(matches!(
            refuse_silent_prod_enablement(FeatureStatus::ProductionEnabled),
            Err(ProductGateError::SilentProdEnablementRefused { .. })
        ));
        assert!(refuse_silent_prod_enablement(FeatureStatus::ExperimentalEnabled).is_ok());
    }

    #[test]
    fn human_only_promotion_firewall() {
        assert!(matches!(
            try_auto_promote(),
            Err(ProductGateError::HumanOnlyPromotionFirewall)
        ));
    }

    #[test]
    fn pipeline_emits_seven_receipts_and_keeps_open_claims() {
        let run = ProductVerticalSlice::new().run(proposal_with_open_claim());
        assert_eq!(run.receipts.len(), 7);
        assert_eq!(
            run.receipts.iter().map(|r| r.stage_id).collect::<Vec<_>>(),
            PipelineStage::ALL.to_vec()
        );
        assert_eq!(run.authority_effect, AUTHORITY_EFFECT);
        assert_eq!(run.promotion, PROMOTION_NOT_PROMOTED);
        assert!(!run.is_promoted());
        assert!(run.has_unresolved());
        assert!(run
            .unresolved_claims
            .iter()
            .any(|c| c == "claim:coda-cs-bridge"));
        assert_eq!(run.feature_status, FeatureStatus::ExperimentalDisabled);

        let adv = run
            .receipts
            .iter()
            .find(|r| r.stage_id == PipelineStage::AdversarialReview)
            .expect("adversarial receipt");
        assert_eq!(adv.status, StageStatus::UnresolvedClaims);
        assert!(!adv.unresolved_claims.is_empty());
    }

    #[test]
    fn manifest_zip_not_release_candidate_when_residuals_remain() {
        let run = ProductVerticalSlice::new().run(proposal_with_open_claim());
        let pkg = run.package.expect("package built even with residuals");
        assert_eq!(pkg.release_status(), RELEASE_NOT_CANDIDATE);
        assert_eq!(pkg.manifest.promotion, PROMOTION_NOT_PROMOTED);
        assert_eq!(pkg.manifest.authority_effect, AUTHORITY_EFFECT);
        assert!(!pkg.residual_open_claims().is_empty());
        assert!(pkg.entries.contains_key("MANIFEST.json"));
        assert!(pkg.entries.contains_key("draft_paper.md"));
        assert!(pkg.entries.contains_key("claims.jsonl"));
        assert!(pkg.entries.contains_key("receipts.jsonl"));
        assert!(pkg.entries.contains_key("AUTHORITY"));
        assert_eq!(pkg.package_hash, hash_hex(pkg.to_bytes()));
        let again = ProductVerticalSlice::new().run(proposal_with_open_claim());
        assert_eq!(
            again.package.as_ref().map(|p| p.package_hash.clone()),
            Some(pkg.package_hash.clone())
        );
    }

    #[test]
    fn resolved_claims_still_not_promoted() {
        let run = ProductVerticalSlice::new().run(proposal_all_resolved());
        assert!(!run.has_unresolved());
        assert_eq!(run.promotion, PROMOTION_NOT_PROMOTED);
        let pkg = run.package.expect("package");
        assert_eq!(pkg.release_status(), RELEASE_DIAGNOSTIC_ONLY);
        assert_eq!(pkg.manifest.promotion, PROMOTION_NOT_PROMOTED);
        assert_ne!(pkg.manifest.promotion, PROMOTION_PROMOTED);
        let full = run
            .receipts
            .iter()
            .find(|r| r.stage_id == PipelineStage::FullReview)
            .expect("full review");
        assert_eq!(full.status, StageStatus::Passed);
    }

    #[test]
    fn empty_proposal_blocks_without_promotion() {
        let run = ProductVerticalSlice::new().run(ProductProposal::new("", "", ""));
        assert_eq!(run.promotion, PROMOTION_NOT_PROMOTED);
        assert_eq!(run.authority_effect, AUTHORITY_EFFECT);
        let first = &run.receipts[0];
        assert_eq!(first.stage_id, PipelineStage::Proposal);
        assert_eq!(first.status, StageStatus::Blocked);
    }

    #[test]
    fn product_disables_q_coda_when_targets_incomplete() {
        let board = LaunchTargetBoard::default();
        assert!(!board.all_complete());
        assert_eq!(
            evaluate_q_coda_integration(&board),
            FeatureStatus::ExperimentalDisabled
        );
        assert_eq!(Q_CODA_PRODUCT_INTEGRATION.as_str(), "experimental_disabled");
        assert!(gate_product_mount(&board).is_err());
        assert!(!q_coda_product_mount_allowed());
    }

    #[test]
    fn stage_receipts_carry_optional_artifact_hash() {
        let run = ProductVerticalSlice::new().run(proposal_with_open_claim());
        for r in &run.receipts {
            assert!(
                r.artifact_hash.is_some(),
                "stage {} missing artifact_hash",
                r.stage_id.id()
            );
        }
    }
}
