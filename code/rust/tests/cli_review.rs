//! The aggregate command computes outputs without inventing a gate receipt.

use std::process::Command;

#[test]
fn c500_aggregate_preserves_open_evidence_boundary() {
    let output = Command::new(env!("CARGO_BIN_EXE_finite_qm_cli"))
        .arg("--c500-all")
        .output()
        .expect("run C500 aggregate");
    assert!(output.status.success());
    let receipt: serde_json::Value = serde_json::from_slice(&output.stdout).unwrap();
    assert_eq!(receipt["blocks"].as_array().unwrap().len(), 10);
    assert_eq!(receipt["launch_preconditions_verified"], false);
    assert_eq!(receipt["gate_status"], "NOT_VERIFIED_BY_CLI");
    assert!(receipt.get("targets_completed").is_none());
    assert!(receipt.get("all_gates_pass").is_none());
    assert_eq!(
        receipt["blocks"][9]["terminal_outcome"],
        "FQMC1_OPEN_INTERNAL_GAPS"
    );
}
