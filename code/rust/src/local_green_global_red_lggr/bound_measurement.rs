
use serde::Serialize;
use sha2::{Digest, Sha256};

use crate::epk_engine::{
    calculate_metrics, evaluator_gluing_defect, BoundarySlice, CompositionRecord, EpkError,
    EpkMetrics, GluingDefect, TraceLedger,
};
use omega_types::authority::AuthorityEffect;
use omega_types::ceiling::EvidenceCeiling;
use omega_types::{DetectorCapacityEvidence, DetectorDeploymentDeclaration};

use crate::adequacy::{evaluate_detector_adequacy, DetectorAdequacyVerdict};
use crate::ledger::EpkResidualLedger;
use crate::prime_seam::{
    descent_receipt_hash, AdequacyKindProjection, ContinuationEvidence, LggrEpkObservation,
    PrimeDescentReceipt, VerifiedDescentReceipt, PRIME_DESCENT_RECEIPT_SCHEMA,
};
use crate::verdict::{classify, EvaluatorProvenance, LggrVerdict};

pub const BOUND_MEASUREMENT_SCHEMA: &str = "omega.epk.bound-measurement.v1";


pub(crate) struct CanonicalHasher {
    hasher: Sha256,
}

impl CanonicalHasher {
    pub(crate) fn new(schema: &str) -> Self {
        let mut this = Self {
            hasher: Sha256::new(),
        };
        this.bytes("schema", schema.as_bytes());
        this
    }

    pub(crate) fn bytes(&mut self, tag: &str, value: &[u8]) -> &mut Self {
        self.hasher.update((tag.len() as u64).to_be_bytes());
        self.hasher.update(tag.as_bytes());
        self.hasher.update((value.len() as u64).to_be_bytes());
        self.hasher.update(value);
        self
    }

    pub(crate) fn str_field(&mut self, tag: &str, value: &str) -> &mut Self {
        self.bytes(tag, value.as_bytes())
    }

    pub(crate) fn opt_str(&mut self, tag: &str, value: Option<&str>) -> &mut Self {
        match value {
            Some(v) => {
                self.bytes(tag, &[1u8]);
                self.bytes(tag, v.as_bytes())
            }
            None => self.bytes(tag, &[0u8]),
        }
    }

    pub(crate) fn u8_field(&mut self, tag: &str, value: u8) -> &mut Self {
        self.bytes(tag, &[value])
    }

    pub(crate) fn i8_field(&mut self, tag: &str, value: i8) -> &mut Self {
        self.bytes(tag, &value.to_be_bytes())
    }

    pub(crate) fn f64_field(&mut self, tag: &str, value: f64) -> &mut Self {
        self.bytes(tag, &value.to_bits().to_be_bytes())
    }

    pub(crate) fn opt_f64(&mut self, tag: &str, value: Option<f64>) -> &mut Self {
        match value {
            Some(v) => {
                self.bytes(tag, &[1u8]);
                self.f64_field(tag, v)
            }
            None => self.bytes(tag, &[0u8]),
        }
    }

    pub(crate) fn finish(self) -> String {
        let digest = self.hasher.finalize();
        let mut out = String::with_capacity(7 + digest.len() * 2);
        out.push_str("sha256:");
        for b in digest {
            out.push_str(&format!("{b:02x}"));
        }
        out
    }
}

pub(crate) fn verdict_tag(v: &LggrVerdict) -> &'static str {
    match v {
        LggrVerdict::Red { .. } => "Red",
        LggrVerdict::PositiveGluingDefect { .. } => "PositiveGluingDefect",
        LggrVerdict::GreenOracleNeeded { .. } => "GreenOracleNeeded",
        LggrVerdict::GreenNumericallySupported { .. } => "GreenNumericallySupported",
        LggrVerdict::OracleExtractedUnsound { .. } => "OracleExtractedUnsound",
    }
}


#[derive(Debug, Clone, PartialEq, thiserror::Error)]
pub enum BoundMeasurementError {
    #[error("cannot measure an empty corpus")]
    EmptyCorpus,
    #[error(transparent)]
    Metrics(#[from] EpkError),
    #[error("row {index} is out of range for a corpus of {len} records")]
    RowOutOfRange { index: usize, len: usize },
    #[error(
        "provenance Exhibited refused: record {record_id} declares \
         (left={declared_left}, right={declared_right}) but the trace ledger \
         records (left={ledger_left:?}, right={ledger_right:?})"
    )]
    ProvenanceNotExhibited {
        record_id: String,
        declared_left: bool,
        declared_right: bool,
        ledger_left: Option<bool>,
        ledger_right: Option<bool>,
    },
    #[error("receipt hash mismatch: claimed {claimed}, recomputed {recomputed}")]
    ReceiptHashMismatch { claimed: String, recomputed: String },
    #[error(
        "receipt is bound to corpus {receipt_digest}, this measurement is {measurement_digest}"
    )]
    ReceiptCorpusMismatch {
        receipt_digest: String,
        measurement_digest: String,
    },
}


#[derive(Debug, Clone, Serialize)]
pub struct BoundEpkMeasurement {
    schema: &'static str,
    corpus_digest: String,
    record_ids: Vec<String>,
    defects: Vec<GluingDefect>,
    metrics: EpkMetrics,
    ledger: EpkResidualLedger,
    #[serde(skip)]
    adequacy: DetectorAdequacyVerdict,
    provenance: EvaluatorProvenance,
}

impl BoundEpkMeasurement {
    pub fn measure(
        records: &[CompositionRecord],
        trace_ledger: &TraceLedger,
        boundary: &BoundarySlice,
        declaration: Option<&DetectorDeploymentDeclaration>,
        evidence: Option<&DetectorCapacityEvidence>,
        requested_provenance: EvaluatorProvenance,
    ) -> Result<Self, BoundMeasurementError> {
        if records.is_empty() {
            return Err(BoundMeasurementError::EmptyCorpus);
        }

        if requested_provenance == EvaluatorProvenance::Exhibited {
            for record in records {
                let ledger_left = trace_ledger
                    .get(&record.left_trace_id)
                    .map(|t| t.evaluator_pass);
                let ledger_right = trace_ledger
                    .get(&record.right_trace_id)
                    .map(|t| t.evaluator_pass);
                if ledger_left != Some(record.local_left_pass)
                    || ledger_right != Some(record.local_right_pass)
                {
                    return Err(BoundMeasurementError::ProvenanceNotExhibited {
                        record_id: record.composed_trace_id.clone(),
                        declared_left: record.local_left_pass,
                        declared_right: record.local_right_pass,
                        ledger_left,
                        ledger_right,
                    });
                }
            }
        }

        let adequacy =
            evaluate_detector_adequacy(declaration, evidence, records, trace_ledger, boundary);
        let metrics = calculate_metrics(records, Some(trace_ledger), None, None, None)?;
        let ledger = EpkResidualLedger::from_metrics(&metrics);
        let defects: Vec<GluingDefect> = records.iter().map(evaluator_gluing_defect).collect();
        let record_ids: Vec<String> = records
            .iter()
            .map(|r| r.composed_trace_id.clone())
            .collect();

        let mut h = CanonicalHasher::new(BOUND_MEASUREMENT_SCHEMA);
        h.str_field("observed_corpus", adequacy.observed_corpus_digest());
        h.str_field(
            "provenance",
            match requested_provenance {
                EvaluatorProvenance::Exhibited => "Exhibited",
                EvaluatorProvenance::OracleExtracted => "OracleExtracted",
            },
        );
        for (id, d) in record_ids.iter().zip(defects.iter()) {
            h.str_field("row_id", id);
            h.i8_field("row_delta", d.delta_eval);
            h.u8_field("row_local_product", d.local_product as u8);
            h.u8_field("row_global_pass", d.global_pass as u8);
        }
        h.f64_field("ngd", ledger.ngd);
        h.opt_f64("nrke", ledger.nrke);
        let corpus_digest = h.finish();

        Ok(Self {
            schema: BOUND_MEASUREMENT_SCHEMA,
            corpus_digest,
            record_ids,
            defects,
            metrics,
            ledger,
            adequacy,
            provenance: requested_provenance,
        })
    }

    pub fn schema(&self) -> &'static str {
        self.schema
    }

    pub fn corpus_digest(&self) -> &str {
        &self.corpus_digest
    }

    pub fn metrics(&self) -> &EpkMetrics {
        &self.metrics
    }

    pub fn ledger(&self) -> &EpkResidualLedger {
        &self.ledger
    }

    pub fn adequacy(&self) -> &DetectorAdequacyVerdict {
        &self.adequacy
    }

    pub fn provenance(&self) -> EvaluatorProvenance {
        self.provenance
    }

    pub fn row_count(&self) -> usize {
        self.defects.len()
    }

    pub fn record_id(&self, index: usize) -> Option<&str> {
        self.record_ids.get(index).map(String::as_str)
    }

    pub fn defect(&self, index: usize) -> Result<&GluingDefect, BoundMeasurementError> {
        self.defects
            .get(index)
            .ok_or(BoundMeasurementError::RowOutOfRange {
                index,
                len: self.defects.len(),
            })
    }

    pub fn verdict(&self, index: usize) -> Result<LggrVerdict, BoundMeasurementError> {
        let defect = self.defect(index)?;
        Ok(classify(defect, Some(&self.adequacy), self.provenance)
            .expect("defects derived from evaluator_gluing_defect are always well-formed"))
    }

    pub fn authority_effect(&self) -> AuthorityEffect {
        AuthorityEffect::None
    }

    pub fn evidence_ceiling(&self, index: usize) -> Result<EvidenceCeiling, BoundMeasurementError> {
        Ok(self
            .verdict(index)?
            .evidence_ceiling()
            .meet(EvidenceCeiling::BoundaryChecked))
    }


    pub fn observe(&self, index: usize) -> Result<LggrEpkObservation, BoundMeasurementError> {
        let defect = *self.defect(index)?;
        let verdict = self.verdict(index)?;
        Ok(LggrEpkObservation::new_bound(
            self.ledger.clone(),
            verdict,
            AdequacyKindProjection::from_kind(self.adequacy.kind()),
            self.corpus_digest.clone(),
            self.record_ids[index].clone(),
            defect,
            self.ledger.obstruction_status,
        ))
    }

    pub fn descend(
        &self,
        source_carrier: impl Into<String>,
        target_carrier: impl Into<String>,
        observation: &LggrEpkObservation,
        residual_preservation_verified: bool,
        loss_ledger: Vec<String>,
    ) -> Result<VerifiedDescentReceipt, BoundMeasurementError> {
        self.require_same_corpus(observation.observed_corpus_digest())?;
        let source_carrier = source_carrier.into();
        let target_carrier = target_carrier.into();
        let receipt_hash = descent_receipt_hash(
            &source_carrier,
            &target_carrier,
            &self.corpus_digest,
            residual_preservation_verified,
            &loss_ledger,
            observation,
        );
        Ok(VerifiedDescentReceipt::seal(PrimeDescentReceipt {
            schema: PRIME_DESCENT_RECEIPT_SCHEMA.to_string(),
            source_carrier,
            target_carrier,
            observed_corpus_digest: self.corpus_digest.clone(),
            residual_preservation_verified,
            loss_ledger,
            receipt_hash,
        }))
    }

    pub fn verify_receipt(
        &self,
        receipt: PrimeDescentReceipt,
        observation: &LggrEpkObservation,
    ) -> Result<VerifiedDescentReceipt, BoundMeasurementError> {
        self.require_same_corpus(Some(receipt.observed_corpus_digest.as_str()))?;
        self.require_same_corpus(observation.observed_corpus_digest())?;
        let recomputed = receipt.recomputed_hash(observation);
        if recomputed != receipt.receipt_hash {
            return Err(BoundMeasurementError::ReceiptHashMismatch {
                claimed: receipt.receipt_hash,
                recomputed,
            });
        }
        Ok(VerifiedDescentReceipt::seal(receipt))
    }

    pub fn continuation_evidence(
        &self,
        receipt: &VerifiedDescentReceipt,
    ) -> Result<ContinuationEvidence, BoundMeasurementError> {
        self.require_same_corpus(Some(receipt.observed_corpus_digest()))?;
        Ok(ContinuationEvidence::seal(
            self.corpus_digest.clone(),
            receipt.receipt_hash().to_string(),
            AdequacyKindProjection::from_kind(self.adequacy.kind()).permits_detector_adequate(),
            receipt.residual_preservation_verified(),
        ))
    }

    fn require_same_corpus(&self, digest: Option<&str>) -> Result<(), BoundMeasurementError> {
        match digest {
            Some(d) if d == self.corpus_digest => Ok(()),
            other => Err(BoundMeasurementError::ReceiptCorpusMismatch {
                receipt_digest: other.unwrap_or("<none>").to_string(),
                measurement_digest: self.corpus_digest.clone(),
            }),
        }
    }
}
