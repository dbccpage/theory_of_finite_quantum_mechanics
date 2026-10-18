use serde_json::Value;
use std::{fs, path::PathBuf, process::Command};

/// The shared test directory; the frozen receipts are in its `artifacts/`.
fn root() -> PathBuf {
    PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../tests/omega_mub")
}

#[test]
fn default_verification_fails_closed_and_does_not_rewrite_receipts() {
    let path = root().join("artifacts/grand_unified_mub6_verification_receipt.json");
    let before = fs::read(&path).unwrap();
    let output = Command::new(env!("CARGO_BIN_EXE_mub_grand_unified_verifier"))
        .output()
        .unwrap();
    assert_eq!(
        output.status.code(),
        Some(2),
        "{}",
        String::from_utf8_lossy(&output.stderr)
    );
    let receipt: Value = serde_json::from_slice(&output.stdout).unwrap();
    assert_eq!(
        receipt["overall_verdict"],
        "INCOMPLETE_MATHEMATICAL_CERTIFICATION"
    );
    assert_eq!(receipt["mathematical_certification"], false);
    assert_eq!(receipt["frontier_receipts_replayed"], 6);
    assert_eq!(before, fs::read(&path).unwrap());
}

#[test]
fn explicit_integrity_check_replays_scoped_receipts() {
    let output = Command::new(env!("CARGO_BIN_EXE_mub_grand_unified_verifier"))
        .arg("--integrity-only")
        .output()
        .unwrap();
    assert!(
        output.status.success(),
        "{}",
        String::from_utf8_lossy(&output.stderr)
    );
    let receipt: Value = serde_json::from_slice(&output.stdout).unwrap();
    assert_eq!(receipt["artifacts"].as_array().unwrap().len(), 21);
    assert_eq!(receipt["integrity_status"], "PASS");
    assert_eq!(receipt["mathematical_certification"], false);
    assert_eq!(
        receipt,
        serde_json::from_slice::<Value>(
            &fs::read(root().join("artifacts/grand_unified_mub6_verification_receipt.json"))
                .unwrap()
        )
        .unwrap()
    );
}

#[test]
fn corrupt_or_missing_artifact_is_rejected() {
    let dir =
        std::env::temp_dir().join(format!("grand-verifier-corruption-{}", std::process::id()));
    fs::create_dir_all(&dir).unwrap();
    // The first required artifact is a frozen receipt. A counterfeit must fail
    // before any success receipt is emitted, even in integrity-only mode.
    let first =
        "dita_seed_F6_0_8_neigh_delta_1_1000_gauge_fixed_5_torus_presplit6_merged_complete.json";
    fs::write(dir.join(first), b"{}").unwrap();
    let run = || {
        Command::new(env!("CARGO_BIN_EXE_mub_grand_unified_verifier"))
            .arg("--integrity-only")
            .arg("--artifacts-dir")
            .arg(&dir)
            .output()
            .unwrap()
    };
    let corrupt = run();
    assert_eq!(corrupt.status.code(), Some(1));
    assert!(String::from_utf8_lossy(&corrupt.stderr).contains("SHA-256 mismatch"));
    assert!(corrupt.stdout.is_empty());
    fs::remove_file(dir.join(first)).unwrap();
    let missing = run();
    assert_eq!(missing.status.code(), Some(1));
    assert!(missing.stdout.is_empty());
    fs::remove_dir(&dir).unwrap();
}
