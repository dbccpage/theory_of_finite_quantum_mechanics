//! Register of omega_mub receipts that are fixtures, not computed evidence.
//!
//! `fixture_receipts.json` lists committed receipts whose headline verdict is a literal,
//! cannot come out false, rests on an assumed constant, or has no producer. These tests keep
//! the register bound to the committed bytes: a receipt that is rewritten must be re-reviewed
//! and its entry updated or removed on purpose.

use serde_json::Value;
use sha2::{Digest, Sha256};
use std::{fs, path::PathBuf};

const KINDS: [&str; 4] = ["literal", "by_construction", "assumed_constant", "no_producer"];

fn repo_root() -> PathBuf {
    PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../../..")
}

fn register() -> Value {
    let path = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../tests/omega_mub/fixture_receipts.json");
    serde_json::from_slice(&fs::read(path).expect("fixture register is present"))
        .expect("fixture register is valid JSON")
}

fn sha256_hex(bytes: &[u8]) -> String {
    format!("{:x}", Sha256::digest(bytes))
}

/// Returns the reason an entry fails, or `None` when it matches its committed file.
fn entry_defect(entry: &Value) -> Option<String> {
    let path = entry["path"].as_str()?;
    let bytes = match fs::read(repo_root().join(path)) {
        Ok(bytes) => bytes,
        Err(error) => return Some(format!("{path}: {error}")),
    };
    let recorded = entry["sha256"].as_str().unwrap_or_default();
    let actual = sha256_hex(&bytes);
    if recorded != actual {
        return Some(format!("{path}: register sha256 {recorded}, file {actual}"));
    }
    None
}

#[test]
fn register_declares_fixtures_without_authority() {
    let doc = register();
    assert_eq!(doc["schema"], "omega_mub.fixture_receipts.v1");
    assert_eq!(doc["authority_effect"], "None");
    let entries = doc["fixtures"].as_array().expect("fixtures is an array");
    assert!(!entries.is_empty());
    let mut paths = Vec::new();
    for entry in entries {
        let path = entry["path"].as_str().expect("path is a string");
        assert_eq!(entry["evidence_kind"], "fixture", "{path}");
        let kind = entry["kind"].as_str().expect("kind is a string");
        assert!(KINDS.contains(&kind), "{path}: unknown kind {kind}");
        assert!(
            entry["fields"].as_array().is_some_and(|f| !f.is_empty()),
            "{path}: names no verdict field"
        );
        assert!(
            entry["reason"].as_str().is_some_and(|r| !r.trim().is_empty()),
            "{path}: no reason"
        );
        for values in entry["fixture_values"].as_array().into_iter().flatten() {
            let values = values.as_str().expect("fixture_values entries are paths");
            assert!(repo_root().join(values).is_file(), "{path}: missing fixture file {values}");
        }
        if kind != "no_producer" {
            assert!(
                entry["literal_at"].as_array().is_some_and(|l| !l.is_empty()),
                "{path}: no source location for the fixed verdict"
            );
        }
        paths.push(path.to_string());
    }
    let count = paths.len();
    paths.sort();
    paths.dedup();
    assert_eq!(paths.len(), count, "duplicate register entries");
}

#[test]
fn every_registered_fixture_matches_its_committed_bytes() {
    let doc = register();
    let defects: Vec<String> = doc["fixtures"]
        .as_array()
        .unwrap()
        .iter()
        .filter_map(entry_defect)
        .collect();
    assert!(defects.is_empty(), "fixture register drift: {defects:?}");
}

#[test]
fn digest_check_rejects_a_changed_or_missing_file() {
    let dir = std::env::temp_dir().join(format!("omega-mub-fixture-register-{}", std::process::id()));
    fs::create_dir_all(&dir).unwrap();
    let file = dir.join("receipt.json");
    fs::write(&file, b"{\"certified\": true}\n").unwrap();
    let path = file.to_str().unwrap().to_string();
    let entry = |sha: &str| serde_json::json!({ "path": path, "sha256": sha });

    let good = sha256_hex(b"{\"certified\": true}\n");
    assert_eq!(entry_defect(&entry(&good)), None);

    fs::write(&file, b"{\"certified\": false}\n").unwrap();
    assert!(entry_defect(&entry(&good)).is_some(), "changed bytes must be reported");

    fs::remove_file(&file).unwrap();
    assert!(entry_defect(&entry(&good)).is_some(), "missing file must be reported");
    fs::remove_dir(&dir).unwrap();
}

#[test]
fn expanded_missing_path_is_a_defect() {
    assert!(entry_defect(&serde_json::json!({})).is_some(), "missing path was treated as a successful digest check");
}

#[test]
fn expanded_root_is_current_repository() {
    assert_eq!(repo_root().canonicalize().unwrap(), std::path::PathBuf::from("C:\\Users\\a343o\\source\\repos\\theory_of_finite_quantum_mechanics"));
}
