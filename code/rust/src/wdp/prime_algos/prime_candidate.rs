//! Prime -1 candidate records and Prime Triad stage records (U03).
//!
//! Owns Prime -1 untrusted candidate records and trace logging for
//! Prime stage transitions (Prime -1, Prime 000, Prime 001, Prime 002).
//! AuthorityEffect: None (const).

use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};
use std::fs::{create_dir_all, OpenOptions};
use std::io::Write;
use std::path::{Path, PathBuf};

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

/// Untrusted raw candidate proposal at Prime -1.
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

/// Trace record for Prime Triad stage transitions (Prime -1, 000, 001, 002).
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
        let record = PrimeStageRecordV1::new(
            self.seq_counter,
            stage,
            packet_id,
            actor,
            status,
            witness_or_refusal,
            self.last_hash.clone(),
        );

        self.last_hash = Some(record.record_hash.clone());
        self.seq_counter += 1;

        let line = serde_json::to_string(&record)
            .map_err(|e| std::io::Error::new(std::io::ErrorKind::InvalidData, e))?;

        let mut file = OpenOptions::new()
            .create(true)
            .append(true)
            .open(&self.log_path)?;

        writeln!(file, "{}", line)?;
        file.flush()?;
        Ok(record)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_candidate_proposal_lifecycle() {
        let payload = b"def candidate_algorithm(): return True";
        let mut proposal = CandidateProposalV1::new("PROP_1", "LOCUS_A", payload, "agent_1");

        assert_eq!(proposal.proposal_id, "PROP_1");
        assert_eq!(proposal.locus_id, "LOCUS_A");
        assert!(!proposal.raw_payload_hash.is_empty());
        assert_eq!(proposal.enters_dda_trace, false);
        assert_eq!(proposal.refusal_reason, None);
        assert_eq!(proposal.authority_effect, "None");

        proposal.refuse("Defective boundary");
        assert_eq!(proposal.enters_dda_trace, false);
        assert_eq!(
            proposal.refusal_reason,
            Some("Defective boundary".to_string())
        );

        proposal.admit_to_trace();
        assert_eq!(proposal.enters_dda_trace, true);
        assert_eq!(proposal.refusal_reason, None);
    }

    #[test]
    fn test_prime_stage_record_hash_chain() {
        let r0 = PrimeStageRecordV1::new(
            0,
            PrimeStage::PrimeMinus1,
            "PKT_0",
            "actor_0",
            "UNTRUSTED",
            "none",
            None,
        );
        assert_eq!(r0.seq, 0);
        assert_eq!(r0.stage, PrimeStage::PrimeMinus1);
        assert_eq!(r0.prev_record_hash, None);
        assert!(!r0.record_hash.is_empty());

        let r1 = PrimeStageRecordV1::new(
            1,
            PrimeStage::Prime000,
            "PKT_1",
            "actor_1",
            "ADMITTED",
            "valid_cochain",
            Some(r0.record_hash.clone()),
        );
        assert_eq!(r1.seq, 1);
        assert_eq!(r1.stage, PrimeStage::Prime000);
        assert_eq!(
            r1.prev_record_hash.as_deref(),
            Some(r0.record_hash.as_str())
        );
        assert_ne!(r1.record_hash, r0.record_hash);
    }

    #[test]
    fn test_prime_trace_logger() {
        let temp_dir = std::env::temp_dir().join(format!(
            "test_prime_log_{}",
            std::time::SystemTime::now()
                .duration_since(std::time::UNIX_EPOCH)
                .unwrap()
                .as_nanos()
        ));
        let log_file = temp_dir.join("prime_trace.jsonl");

        let mut logger = PrimeTraceLogger::new(&log_file).expect("create logger");
        let rec1 = logger
            .append_stage(
                PrimeStage::PrimeMinus1,
                "PKT_0",
                "agent_a",
                "PROPOSED",
                "wit_0",
            )
            .expect("append rec1");
        assert_eq!(rec1.seq, 0);

        let rec2 = logger
            .append_stage(
                PrimeStage::Prime000,
                "PKT_1",
                "agent_b",
                "ADMITTED",
                "wit_1",
            )
            .expect("append rec2");
        assert_eq!(rec2.seq, 1);
        assert_eq!(rec2.prev_record_hash, Some(rec1.record_hash));

        let _ = std::fs::remove_dir_all(&temp_dir);
    }
}
