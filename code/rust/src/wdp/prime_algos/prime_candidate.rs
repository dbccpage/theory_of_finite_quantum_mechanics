
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};
use std::fs::{create_dir_all, OpenOptions};
use std::io::Write;
use std::path::{Path, PathBuf};

pub const ORIGIN: &str = "Origin: code/rust/src/wdp/prime_algos/prime_candidate.rs @ 40de7d5cda1ff1f0db8305d0c1b2103646fab197";
pub const CLAIM: &str = "Claim: a prime-stage record hash is the sha256 of the little-endian sequence, stage, packet, actor, status, witness, and optional previous hash";
pub const AUTHORITY_EFFECT: &str = "AuthorityEffect: None";
pub const MUTATION_KILLS: u32 = 0;
pub const EMPTY_STAGE_HASH: &str = "760958dfc04208a94736527d6c79034a0699a6e211725cf4512756244d9b3944";

fn default_authority_effect() -> String {
    "None".to_string()
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub enum PrimeStage {
    #[serde(rename = "PRIME_-1")]
    PrimeMinus1,
    #[serde(rename = "PRIME_000")]
    Prime000,
    #[serde(rename = "PRIME_001")]
    Prime001,
    #[serde(rename = "PRIME_002")]
    Prime002,
}

impl PrimeStage {
    pub fn as_str(&self) -> &'static str {
        match self {
            PrimeStage::PrimeMinus1 => "PRIME_-1",
            PrimeStage::Prime000 => "PRIME_000",
            PrimeStage::Prime001 => "PRIME_001",
            PrimeStage::Prime002 => "PRIME_002",
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct CandidateProposalV1 {
    pub proposal_id: String,
    pub locus_id: String,
    pub raw_payload_hash: String,
    pub actor: String,
    pub enters_dda_trace: bool,
    pub refusal_reason: Option<String>,
    #[serde(default = "default_authority_effect")]
    pub authority_effect: String,
}

impl CandidateProposalV1 {
    pub fn new(
        proposal_id: impl Into<String>,
        locus_id: impl Into<String>,
        raw_payload: &[u8],
        actor: impl Into<String>,
    ) -> Self {
        let mut hasher = Sha256::new();
        hasher.update(raw_payload);
        let payload_hash = format!("{:x}", hasher.finalize());

        Self {
            proposal_id: proposal_id.into(),
            locus_id: locus_id.into(),
            raw_payload_hash: payload_hash,
            actor: actor.into(),
            enters_dda_trace: false,
            refusal_reason: None,
            authority_effect: default_authority_effect(),
        }
    }

    pub fn refuse(&mut self, reason: impl Into<String>) {
        self.refusal_reason = Some(reason.into());
        self.enters_dda_trace = false;
    }

    pub fn admit_to_trace(&mut self) {
        self.refusal_reason = None;
        self.enters_dda_trace = true;
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct PrimeStageRecordV1 {
    pub seq: u64,
    pub stage: PrimeStage,
    pub packet_id: String,
    pub actor: String,
    pub status: String,
    pub witness_or_refusal: String,
    pub prev_record_hash: Option<String>,
    pub record_hash: String,
    #[serde(default = "default_authority_effect")]
    pub authority_effect: String,
}

pub fn compute_prime_stage_hash(
    seq: u64,
    stage: &str,
    packet_id: &str,
    actor: &str,
    status: &str,
    witness_or_refusal: &str,
    prev_hash: Option<&str>,
) -> String {
    let mut hasher = Sha256::new();
    hasher.update(seq.to_le_bytes());
    hasher.update(stage.as_bytes());
    hasher.update(packet_id.as_bytes());
    hasher.update(actor.as_bytes());
    hasher.update(status.as_bytes());
    hasher.update(witness_or_refusal.as_bytes());
    if let Some(prev) = prev_hash {
        hasher.update(b":prev:");
        hasher.update(prev.as_bytes());
    }
    format!("{:x}", hasher.finalize())
}

impl PrimeStageRecordV1 {
    pub fn new(
        seq: u64,
        stage: PrimeStage,
        packet_id: impl Into<String>,
        actor: impl Into<String>,
        status: impl Into<String>,
        witness_or_refusal: impl Into<String>,
        prev_record_hash: Option<String>,
    ) -> Self {
        let p_id = packet_id.into();
        let act = actor.into();
        let stat = status.into();
        let wit = witness_or_refusal.into();
        let hash = compute_prime_stage_hash(
            seq,
            stage.as_str(),
            &p_id,
            &act,
            &stat,
            &wit,
            prev_record_hash.as_deref(),
        );

        Self {
            seq,
            stage,
            packet_id: p_id,
            actor: act,
            status: stat,
            witness_or_refusal: wit,
            prev_record_hash,
            record_hash: hash,
            authority_effect: default_authority_effect(),
        }
    }
}

pub struct PrimeTraceLogger {
    pub log_path: PathBuf,
    pub last_hash: Option<String>,
    pub seq_counter: u64,
}

impl PrimeTraceLogger {
    pub fn new(log_path: impl AsRef<Path>) -> std::io::Result<Self> {
        let path = log_path.as_ref().to_path_buf();
        if let Some(parent) = path.parent() {
            create_dir_all(parent)?;
        }
        Ok(Self {
            log_path: path,
            last_hash: None,
            seq_counter: 0,
        })
    }

    pub fn append_stage(
        &mut self,
        stage: PrimeStage,
        packet_id: &str,
        actor: &str,
        status: &str,
        witness_or_refusal: &str,
    ) -> std::io::Result<PrimeStageRecordV1> {
        let record = self.stage_record(stage, packet_id, actor, status, witness_or_refusal)?;
        write_record(&self.log_path, &record)?;
        Ok(record)
    }

    fn stage_record(
        &mut self,
        stage: PrimeStage,
        packet_id: &str,
        actor: &str,
        status: &str,
        witness_or_refusal: &str,
    ) -> std::io::Result<PrimeStageRecordV1> {
        let record = PrimeStageRecordV1::new(
            self.seq_counter,
            stage,
            packet_id,
            actor,
            status,
            witness_or_refusal,
            self.last_hash.clone(),
        );
        let next = self.seq_counter.checked_add(1).ok_or_else(|| {
            std::io::Error::new(
                std::io::ErrorKind::InvalidData,
                "prime trace sequence overflow",
            )
        })?;
        self.last_hash = Some(record.record_hash.clone());
        self.seq_counter = next;
        Ok(record)
    }
}

fn write_record(path: &Path, record: &PrimeStageRecordV1) -> std::io::Result<()> {
    let line = serde_json::to_string(record)
        .map_err(|error| std::io::Error::new(std::io::ErrorKind::InvalidData, error))?;
    let mut file = OpenOptions::new().create(true).append(true).open(path)?;
    write_line(&mut file, &line)
}

fn write_line(file: &mut impl Write, line: &str) -> std::io::Result<()> {
    writeln!(file, "{line}")?;
    file.flush()
}

pub fn admit_exact_integer(token: &str) -> Result<i64, PrimeTokenError> {
    if token == "true" || token == "false" {
        return Err(PrimeTokenError::BooleanAsNumber);
    }
    if token.bytes().any(|byte| matches!(byte, b'.' | b'e' | b'E')) {
        return Err(PrimeTokenError::BinaryFloatRefused);
    }
    parse_signed_digits(token)
}

fn parse_signed_digits(token: &str) -> Result<i64, PrimeTokenError> {
    let (negative, digits) = match token.strip_prefix('-') {
        Some(rest) => (true, rest),
        None => (false, token),
    };
    if digits.is_empty() || !digits.bytes().all(|byte| byte.is_ascii_digit()) {
        return Err(PrimeTokenError::InexactToken);
    }
    let mut value = 0i64;
    for byte in digits.bytes() {
        let digit = i64::from(byte - b'0');
        value = value
            .checked_mul(10)
            .and_then(|place| place.checked_add(digit))
            .ok_or(PrimeTokenError::Overflow)?;
    }
    if negative {
        value = value.checked_neg().ok_or(PrimeTokenError::Overflow)?;
    }
    Ok(value)
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum PrimeTokenError {
    BinaryFloatRefused,
    BooleanAsNumber,
    InexactToken,
    Overflow,
}

#[cfg(test)]
mod tests {
    use super::*;

    fn need(cond: bool, message: &str) -> Result<(), String> {
        if cond {
            Ok(())
        } else {
            Err(message.to_string())
        }
    }

    #[test]
    fn unit_known_stage_hash_and_refusal_clear_on_admission() -> Result<(), String> {
        unit_hash().and_then(|_| unit_admission())
    }

    fn unit_hash() -> Result<(), String> {
        let record = PrimeStageRecordV1::new(
            0,
            PrimeStage::PrimeMinus1,
            "PKT_0",
            "actor_0",
            "UNTRUSTED",
            "none",
            None,
        );
        need(record.record_hash == EMPTY_STAGE_HASH, "vector")?;
        need(record.prev_record_hash.is_none(), "genesis")?;
        need(record.authority_effect == "None", "authority")
    }

    fn unit_admission() -> Result<(), String> {
        let mut proposal = CandidateProposalV1::new("PROP_1", "LOCUS_A", b"payload", "agent_1");
        proposal.refuse("Defective boundary");
        need(proposal.refusal_reason.as_deref() == Some("Defective boundary"), "refuse")?;
        need(!proposal.enters_dda_trace, "trace closed")?;
        proposal.admit_to_trace();
        unit_admitted(&proposal)
    }

    fn unit_admitted(proposal: &CandidateProposalV1) -> Result<(), String> {
        need(proposal.refusal_reason.is_none(), "cleared")?;
        need(proposal.enters_dda_trace, "admitted")
    }

    #[test]
    fn integration_next_record_keeps_the_previous_hash() -> Result<(), String> {
        let first = PrimeStageRecordV1::new(0, PrimeStage::PrimeMinus1, "PKT_0", "actor_0", "UNTRUSTED", "none", None);
        let second = PrimeStageRecordV1::new(
            1,
            PrimeStage::Prime000,
            "PKT_1",
            "actor_1",
            "ADMITTED",
            "valid_cochain",
            Some(first.record_hash.clone()),
        );
        need(second.prev_record_hash.as_deref() == Some(first.record_hash.as_str()), "link")?;
        need(second.record_hash != first.record_hash, "distinct")?;
        Ok(())
    }

    #[test]
    fn e2e_logger_appends_a_linked_pair() -> Result<(), String> {
        e2e_records().and_then(|(first, second, temp_dir)| e2e_chain(first, second, temp_dir))
    }

    fn e2e_records() -> Result<(PrimeStageRecordV1, PrimeStageRecordV1, std::path::PathBuf), String> {
        let temp_dir = std::env::temp_dir().join("tfqm_wdp_prime_candidate_l5a");
        let log_file = temp_dir.join("prime_trace.jsonl");
        let mut logger = PrimeTraceLogger::new(&log_file).map_err(|error| error.to_string())?;
        let first = logger
            .append_stage(PrimeStage::PrimeMinus1, "PKT_0", "agent_a", "PROPOSED", "wit_0")
            .map_err(|error| error.to_string())?;
        let second = logger
            .append_stage(PrimeStage::Prime000, "PKT_1", "agent_b", "ADMITTED", "wit_1")
            .map_err(|error| error.to_string())?;
        Ok((first, second, temp_dir))
    }

    fn e2e_chain(
        first: PrimeStageRecordV1,
        second: PrimeStageRecordV1,
        temp_dir: std::path::PathBuf,
    ) -> Result<(), String> {
        need(first.seq == 0, "seq0")?;
        need(second.seq == 1, "seq1")?;
        need(second.prev_record_hash.as_deref() == Some(first.record_hash.as_str()), "chain")?;
        e2e_text(temp_dir)
    }

    fn e2e_text(temp_dir: std::path::PathBuf) -> Result<(), String> {
        let _ = std::fs::remove_dir_all(&temp_dir);
        need(ORIGIN.contains("prime_candidate.rs"), "origin")?;
        need(CLAIM.contains("sha256"), "claim")
    }

    #[test]
    fn negative_refuses_float_boolean_and_a_changed_witness_hash() -> Result<(), String> {
        let record = PrimeStageRecordV1::new(0, PrimeStage::PrimeMinus1, "PKT_0", "actor_0", "UNTRUSTED", "none", None);
        let changed = PrimeStageRecordV1::new(0, PrimeStage::PrimeMinus1, "PKT_0", "actor_0", "UNTRUSTED", "other", None);
        need(changed.record_hash != record.record_hash, "witness")?;
        need(admit_exact_integer("1.0") == Err(PrimeTokenError::BinaryFloatRefused), "float")?;
        need(admit_exact_integer("true") == Err(PrimeTokenError::BooleanAsNumber), "bool")?;
        Ok(())
    }
}
