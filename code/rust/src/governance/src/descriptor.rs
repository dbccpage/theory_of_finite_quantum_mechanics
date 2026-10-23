//! A typed view of one `*.contract.score.yaml` companion (schema
//! `tfqm.contract-score.v1`, stored as JSON): which bytes it binds, what it
//! claims, and the current score record.
//!
//! Parsing is lenient on purpose: a missing or mistyped field is kept as
//! `None` or recorded in `missing_keys`, and the verifiers turn that into a
//! precise [`Violation`]. Only text that is not JSON at all fails here.
//!
//! Cost: O(n) in the companion's size, plus SHA-256 of the two current history entries.

use serde_json::{Map, Value};
use sha2::{Digest, Sha256};

use super::score::{Gate, GateGrades, Grade, Level, ScoreToken};
use super::verify::Violation;

/// Top-level keys every companion document must carry.
pub const REQUIRED_KEYS: [&str; 7] =
    ["schema_version", "artifact", "contract", "current_contract", "current_scoring", "contract_history", "scoring_history"];

/// The current score record of a companion, as stored.
#[derive(Debug, Clone, PartialEq)]
pub struct ScoreRecord {
    /// Digest named by `current_scoring`.
    pub digest: String,
    /// True when the history entry's `raw_utf8` hashes to `digest` with the stated length.
    pub digest_ok: bool,
    /// `schema_version` of the record (`2.0.0` for SCORING.md v2).
    pub schema_version: Option<String>,
    /// Bound source path.
    pub artifact_path: Option<String>,
    /// Bound source digest.
    pub artifact_sha256: Option<String>,
    /// Declared language.
    pub language: Option<String>,
    /// Raw `level` value.
    pub level: Option<Value>,
    /// Raw `gates` value.
    pub gates: Option<Value>,
    /// Raw `composite_grade` value.
    pub composite_grade: Option<Value>,
    /// Raw `score_token` value.
    pub score_token: Option<Value>,
    /// `is_complete` flag.
    pub is_complete: Option<bool>,
}

/// A typed view of a companion document.
#[derive(Debug, Clone, PartialEq)]
pub struct ContractDescriptor {
    /// Repository-relative path of the companion.
    pub companion_path: String,
    /// `schema_version` of the document.
    pub document_schema: Option<String>,
    /// Required top-level keys that are absent.
    pub missing_keys: Vec<&'static str>,
    /// Source path bound by the current contract.
    pub artifact_path: Option<String>,
    /// Source digest bound by the current contract.
    pub artifact_sha256: Option<String>,
    /// Language declared by the contract, if any.
    pub language: Option<String>,
    /// Claim or contract URN.
    pub contract_urn: Option<String>,
    /// Exported symbols the contract covers.
    pub symbols: Vec<String>,
    /// Invariants the contract owns.
    pub owned_invariants: Vec<String>,
    /// True when `contract` equals the record of the `current_contract` history entry.
    pub contract_view_ok: bool,
    /// The current score record, if `current_scoring` names a history entry.
    pub current_score: Option<ScoreRecord>,
}

impl ContractDescriptor {
    /// Parse companion text. Fails only when the text is not a JSON object.
    pub fn parse(companion_path: &str, text: &str) -> Result<ContractDescriptor, Violation> {
        let malformed = |message: String| Violation::MalformedJson { path: companion_path.to_owned(), message };
        let value: Value = serde_json::from_str(text).map_err(|e| malformed(e.to_string()))?;
        let doc = value.as_object().ok_or_else(|| malformed("top level is not an object".into()))?;
        let missing_keys = REQUIRED_KEYS.into_iter().filter(|key| !doc.contains_key(*key)).collect();
        let contract = doc.get("contract").and_then(Value::as_object);
        let (artifact_path, artifact_sha256, language) = contract.map(binding).unwrap_or_default();
        let contract_view_ok = history_entry(doc, "contract_history", "current_contract")
            .is_some_and(|entry| entry.get("record") == doc.get("contract") && digest_ok(entry));
        Ok(ContractDescriptor {
            companion_path: companion_path.to_owned(),
            document_schema: text_field(doc, "schema_version"),
            missing_keys,
            artifact_path,
            artifact_sha256,
            language,
            contract_urn: contract.and_then(|c| ["contract_urn", "claim", "contract_id"].iter().find_map(|k| text_field(c, k))),
            symbols: contract.map(|c| string_list(c, "symbols")).unwrap_or_default(),
            owned_invariants: contract.map(|c| string_list(c, "owned_invariants")).unwrap_or_default(),
            contract_view_ok,
            current_score: current_score(doc),
        })
    }

    fn schema(&self, field: &str, expected: &str, found: String) -> Violation {
        Violation::Schema { path: self.companion_path.clone(), field: field.to_owned(), expected: expected.to_owned(), found }
    }

    fn score(&self) -> Result<&ScoreRecord, Violation> {
        self.current_score.as_ref().ok_or_else(|| self.schema("current_scoring", "a digest naming a scoring_history entry", "no such entry".into()))
    }

    /// The capability level of the current score.
    pub fn level(&self) -> Result<Level, Violation> {
        let raw = self.score()?.level.clone().unwrap_or(Value::Null);
        raw.as_str().and_then(|s| s.parse().ok()).ok_or_else(|| self.schema("level", "L1..L5", raw.to_string()))
    }

    /// The five gate grades of the current score.
    pub fn gate_grades(&self) -> Result<GateGrades, Violation> {
        let raw = self.score()?.gates.clone().unwrap_or(Value::Null);
        let gates = raw.as_object().ok_or_else(|| self.schema("gates", "an object with keys G1..G5", raw.to_string()))?;
        let mut grades = [None; 5];
        for (slot, gate) in grades.iter_mut().zip(Gate::ALL) {
            let value = gates.get(gate.as_str()).ok_or_else(|| self.schema(&format!("gates.{gate}"), "a grade or null", "absent".into()))?;
            *slot = self.optional_grade(&format!("gates.{gate}"), value)?;
        }
        Ok(GateGrades::new(grades))
    }

    /// The stored composite grade, `None` when it is null.
    pub fn composite(&self) -> Result<Option<Grade>, Violation> {
        let raw = self.score()?.composite_grade.clone().unwrap_or(Value::Null);
        self.optional_grade("composite_grade", &raw)
    }

    /// The stored score token, `None` when it is null.
    pub fn token(&self) -> Result<Option<ScoreToken>, Violation> {
        match self.score()?.score_token.clone().unwrap_or(Value::Null) {
            Value::Null => Ok(None),
            Value::String(text) => text.parse().map(Some).map_err(|_| self.schema("score_token", "L<level><grade> or null", text)),
            other => Err(self.schema("score_token", "L<level><grade> or null", other.to_string())),
        }
    }

    fn optional_grade(&self, field: &str, value: &Value) -> Result<Option<Grade>, Violation> {
        match value {
            Value::Null => Ok(None),
            Value::String(text) => text.parse().map(Some).map_err(|_| self.schema(field, "E, D, C, B, A, A+ or null", text.clone())),
            other => Err(self.schema(field, "E, D, C, B, A, A+ or null", other.to_string())),
        }
    }
}

/// `(path, sha256, language)` bound by a contract or score record. Two layouts are
/// in use: `artifact: {path, sha256, language}` and `subject` + `source_sha256`.
fn binding(record: &Map<String, Value>) -> (Option<String>, Option<String>, Option<String>) {
    match record.get("artifact").and_then(Value::as_object) {
        Some(artifact) => (text_field(artifact, "path"), text_field(artifact, "sha256"), text_field(artifact, "language")),
        None => (text_field(record, "subject"), text_field(record, "source_sha256"), None),
    }
}

fn current_score(doc: &Map<String, Value>) -> Option<ScoreRecord> {
    let entry = history_entry(doc, "scoring_history", "current_scoring")?;
    let record = entry.get("record").and_then(Value::as_object);
    let (artifact_path, artifact_sha256, language) = record.map(binding).unwrap_or_default();
    let get = |key: &str| record.and_then(|r| r.get(key)).cloned();
    Some(ScoreRecord {
        digest: text_field(entry, "sha256").unwrap_or_default(),
        digest_ok: digest_ok(entry),
        schema_version: record.and_then(|r| text_field(r, "schema_version")),
        artifact_path,
        artifact_sha256,
        language,
        level: get("level"),
        gates: get("gates"),
        composite_grade: get("composite_grade"),
        score_token: get("score_token"),
        is_complete: record.and_then(|r| r.get("is_complete")).and_then(Value::as_bool),
    })
}

fn history_entry<'a>(doc: &'a Map<String, Value>, history: &str, current: &str) -> Option<&'a Map<String, Value>> {
    let digest = doc.get(current)?.as_str()?;
    doc.get(history)?
        .as_array()?
        .iter()
        .filter_map(Value::as_object)
        .find(|entry| entry.get("sha256").and_then(Value::as_str) == Some(digest))
}

/// The history entry's stored bytes hash to its digest and have its stated length.
fn digest_ok(entry: &Map<String, Value>) -> bool {
    let raw = entry.get("raw_utf8").and_then(Value::as_str).unwrap_or_default().as_bytes();
    let digest = entry.get("sha256").and_then(Value::as_str);
    let length = entry.get("bytes").and_then(Value::as_u64);
    digest == Some(hex(&Sha256::digest(raw)).as_str()) && length == u64::try_from(raw.len()).ok()
}

/// Lower-case hexadecimal of bytes.
pub fn hex(bytes: &[u8]) -> String {
    bytes.iter().map(|b| format!("{b:02x}")).collect()
}

fn text_field(map: &Map<String, Value>, key: &str) -> Option<String> {
    map.get(key).and_then(Value::as_str).map(str::to_owned)
}

fn string_list(map: &Map<String, Value>, key: &str) -> Vec<String> {
    map.get(key).and_then(Value::as_array).map(|items| items.iter().filter_map(Value::as_str).map(str::to_owned).collect()).unwrap_or_default()
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::expect_used, clippy::indexing_slicing, clippy::panic)]
pub(crate) mod tests {
    use super::*;
    use serde_json::json;

    /// Build a companion document whose history entries are internally consistent.
    pub(crate) fn companion(path: &str, sha: &str, score: Value) -> String {
        let contract = json!({
            "schema_id": "tfqm.source-contract.v1",
            "artifact": {"path": path, "sha256": sha, "language": "Rust"},
            "contract_urn": "urn:tfqm:test",
            "symbols": ["f", "g"],
            "owned_invariants": ["inv"],
        });
        let entry = |record: &Value| {
            let raw = serde_json::to_string_pretty(record).unwrap();
            json!({"sha256": hex(&Sha256::digest(raw.as_bytes())), "bytes": raw.len(), "record": record, "raw_utf8": raw, "original_paths": []})
        };
        let (c, s) = (entry(&contract), entry(&score));
        json!({
            "schema_version": "tfqm.contract-score.v1",
            "artifact": path,
            "contract": contract,
            "current_contract": c["sha256"],
            "current_scoring": s["sha256"],
            "contract_history": [c],
            "scoring_history": [s],
        })
        .to_string()
    }

    pub(crate) fn score(path: &str, sha: &str, level: &str, gates: [Option<&str>; 5], composite: Option<&str>, token: Option<&str>, complete: bool) -> Value {
        let [g1, g2, g3, g4, g5] = gates;
        json!({
            "schema_version": "2.0.0",
            "artifact": {"path": path, "sha256": sha, "language": "Rust"},
            "level": level,
            "gates": {"G1": g1, "G2": g2, "G3": g3, "G4": g4, "G5": g5},
            "composite_grade": composite,
            "score_token": token,
            "is_complete": complete,
        })
    }

    #[test]
    fn parses_a_complete_companion() {
        let sha = "a".repeat(64);
        let text = companion("code/x.rs", &sha, score("code/x.rs", &sha, "L4", [Some("C"); 5], Some("C"), Some("L4C"), true));
        let d = ContractDescriptor::parse("code/x.contract.score.yaml", &text).unwrap();
        assert!(d.missing_keys.is_empty());
        assert!(d.contract_view_ok);
        assert_eq!(d.artifact_path.as_deref(), Some("code/x.rs"));
        assert_eq!(d.artifact_sha256.as_deref(), Some(sha.as_str()));
        assert_eq!(d.language.as_deref(), Some("Rust"));
        assert_eq!(d.contract_urn.as_deref(), Some("urn:tfqm:test"));
        assert_eq!(d.symbols, ["f", "g"]);
        assert_eq!(d.owned_invariants, ["inv"]);
        let s = d.current_score.as_ref().unwrap();
        assert!(s.digest_ok);
        assert_eq!(d.level().unwrap(), Level::L4);
        assert_eq!(d.composite().unwrap(), Some(Grade::C));
        assert_eq!(d.token().unwrap().unwrap().to_string(), "L4C");
        assert_eq!(d.gate_grades().unwrap().composite(), Some(Grade::C));
    }

    #[test]
    fn malformed_json_is_a_typed_error() {
        let err = ContractDescriptor::parse("c.yaml", "{\"a\": 1 \"b\": 2}").unwrap_err();
        assert!(matches!(&err, Violation::MalformedJson { path, .. } if path == "c.yaml"), "{err}");
        let err = ContractDescriptor::parse("c.yaml", "[1]").unwrap_err();
        assert!(matches!(err, Violation::MalformedJson { .. }));
        let err = ContractDescriptor::parse("c.yaml", "schema_version: x\n").unwrap_err();
        assert!(matches!(err, Violation::MalformedJson { .. }));
    }

    #[test]
    fn legacy_subject_layout_and_missing_pieces() {
        let text = json!({"schema_version": "tfqm.contract-score.v1", "contract": {"subject": "lean4/A.lean", "source_sha256": "b", "claim": "urn:c"}}).to_string();
        let d = ContractDescriptor::parse("lean4/A.contract.score.yaml", &text).unwrap();
        assert_eq!(d.artifact_path.as_deref(), Some("lean4/A.lean"));
        assert_eq!(d.artifact_sha256.as_deref(), Some("b"));
        assert_eq!(d.contract_urn.as_deref(), Some("urn:c"));
        assert_eq!(d.missing_keys, ["artifact", "current_contract", "current_scoring", "contract_history", "scoring_history"]);
        assert!(!d.contract_view_ok);
        assert!(d.current_score.is_none());
        assert!(matches!(d.level(), Err(Violation::Schema { field, .. }) if field == "current_scoring"));
    }

    #[test]
    fn tampered_history_bytes_are_detected() {
        let sha = "a".repeat(64);
        let text = companion("code/x.rs", &sha, score("code/x.rs", &sha, "L4", [Some("C"); 5], Some("C"), Some("L4C"), true));
        let mut v: Value = serde_json::from_str(&text).unwrap();
        v["scoring_history"][0]["raw_utf8"] = json!("tampered");
        let d = ContractDescriptor::parse("c", &v.to_string()).unwrap();
        assert!(!d.current_score.unwrap().digest_ok);
        let mut v: Value = serde_json::from_str(&text).unwrap();
        v["contract"]["symbols"] = json!(["changed"]);
        assert!(!ContractDescriptor::parse("c", &v.to_string()).unwrap().contract_view_ok);
    }

    #[test]
    fn invalid_vocabulary_is_reported_by_field() {
        let sha = "a".repeat(64);
        let bad = |s: Value| ContractDescriptor::parse("c", &companion("code/x.rs", &sha, s)).unwrap();
        let d = bad(score("code/x.rs", &sha, "L7", [Some("C"); 5], Some("C"), Some("L4C"), true));
        assert!(matches!(d.level(), Err(Violation::Schema { field, found, .. }) if field == "level" && found == "\"L7\""));
        let d = bad(score("code/x.rs", &sha, "L4", [Some("C"), Some("C"), Some("Q"), Some("C"), Some("C")], Some("C"), Some("L4C"), true));
        assert!(matches!(d.gate_grades(), Err(Violation::Schema { field, .. }) if field == "gates.G3"));
        let d = bad(score("code/x.rs", &sha, "L4", [Some("C"); 5], Some("B-"), Some("L4X"), true));
        assert!(matches!(d.composite(), Err(Violation::Schema { field, .. }) if field == "composite_grade"));
        assert!(matches!(d.token(), Err(Violation::Schema { field, .. }) if field == "score_token"));
        let mut s = score("code/x.rs", &sha, "L4", [Some("C"); 5], Some("C"), Some("L4C"), true);
        s["gates"] = json!({"G1": "C"});
        assert!(matches!(bad(s.clone()).gate_grades(), Err(Violation::Schema { field, .. }) if field == "gates.G2"));
        s["gates"] = json!(["C"]);
        s["score_token"] = json!(4);
        s["composite_grade"] = json!(1);
        let d = bad(s);
        assert!(matches!(d.gate_grades(), Err(Violation::Schema { field, .. }) if field == "gates"));
        assert!(matches!(d.token(), Err(Violation::Schema { field, .. }) if field == "score_token"));
        assert!(matches!(d.composite(), Err(Violation::Schema { field, .. }) if field == "composite_grade"));
    }
}
