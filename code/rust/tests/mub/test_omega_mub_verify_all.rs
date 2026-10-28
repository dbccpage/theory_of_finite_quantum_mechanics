//! Integration Test Suite for Native Verifier `mub_verify_all`.
//!
//! AuthorityEffect: None
//!
//! Enforces:
//! 1. AST-level and lexical zero-float discipline (`f32`/`f64` forbidden).
//! 2. Deterministic execution of partition covers, chaining, Čech cocycles, and moment SDP.
//! 3. Execution of `mub_verify_all`, which fails closed (exit code 1, no
//!    receipt) while the B3 no-go rests on sampled coverage.
//! 4. Claim hygiene and epistemic firewall lines.

use std::fs;
use std::path::Path;
use std::process::Command;

use syn::visit::Visit;

// ============================================================================
// 1. AST-Level Strict Zero-Float Discipline Audit
// ============================================================================

struct FloatAuditVisitor {
    found_floats: Vec<String>,
}

impl<'ast> Visit<'ast> for FloatAuditVisitor {
    fn visit_type_path(&mut self, node: &'ast syn::TypePath) {
        for seg in &node.path.segments {
            let ident_str = seg.ident.to_string();
            if ident_str == "f32" || ident_str == "f64" {
                self.found_floats
                    .push(format!("Forbidden float type: {}", ident_str));
            }
        }
        syn::visit::visit_type_path(self, node);
    }

    fn visit_lit_float(&mut self, node: &'ast syn::LitFloat) {
        self.found_floats
            .push(format!("Forbidden float literal: {}", node));
        syn::visit::visit_lit_float(self, node);
    }
}

#[test]
fn test_mub_verify_all_ast_zero_float_compliance() {
    let manifest_dir = env!("CARGO_MANIFEST_DIR");
    let target_file = Path::new(manifest_dir)
        .join("src")
        .join("bin")
        .join("mub_verify_all.rs");

    let source = fs::read_to_string(&target_file)
        .unwrap_or_else(|e| panic!("Failed to read {}: {}", target_file.display(), e));

    let syntax_tree = syn::parse_file(&source)
        .unwrap_or_else(|e| panic!("Failed to parse {}: {}", target_file.display(), e));

    let mut visitor = FloatAuditVisitor {
        found_floats: Vec::new(),
    };
    visitor.visit_file(&syntax_tree);

    assert!(
        visitor.found_floats.is_empty(),
        "mub_verify_all.rs violated zero-float discipline at AST level: {:?}",
        visitor.found_floats
    );

    // Also assert verbatim text excludes f32 / f64 tokens
    assert!(
        !source.contains("f32"),
        "mub_verify_all.rs must contain zero occurrences of f32"
    );
    assert!(
        !source.contains("f64"),
        "mub_verify_all.rs must contain zero occurrences of f64"
    );
}

// ============================================================================
// 2. Binary Execution & Exit Code 0 Verification
// ============================================================================

#[test]
fn test_mub_verify_all_reports_b3_no_go_not_established() {
    let bin_path = env!("CARGO_BIN_EXE_mub_verify_all");

    let output = Command::new(bin_path)
        .arg("--json")
        .output()
        .expect("Failed to execute mub_verify_all binary");

    let stdout = String::from_utf8_lossy(&output.stdout);
    let stderr = String::from_utf8_lossy(&output.stderr);

    // B3's covering closure rests on sampled coverage, so the run must stop
    // there rather than certify the no-go.
    assert_eq!(
        output.status.code(),
        Some(1),
        "Binary must fail while the B3 no-go is not established\nStdout:\n{stdout}\nStderr:\n{stderr}"
    );
    assert!(
        stderr.contains("Target B3 no-go not established"),
        "Failure must name the unestablished B3 no-go\nStderr:\n{stderr}"
    );
    assert!(
        !stdout.contains("CERTIFIED_ALL_CHECKS_PASSED"),
        "A failed run must not emit a passing receipt\nStdout:\n{stdout}"
    );
    assert!(
        !stdout.contains("Strictly Forbidden") && !stdout.to_lowercase().contains("zero float"),
        "A fail-closed run must not certify that floats are absent\nStdout:\n{stdout}"
    );
    let stripped = stdout.replace(
        "stated region only; mints no authority",
        "",
    );
    assert!(!stripped.contains("MUB(6)=3") && !stripped.contains("MUB(6)<=3"));
}

// ============================================================================
// 3. CLI Options (Help, Quiet, Emit) Test
// ============================================================================

#[test]
fn test_mub_verify_all_cli_help() {
    let bin_path = env!("CARGO_BIN_EXE_mub_verify_all");

    let output = Command::new(bin_path)
        .arg("--help")
        .output()
        .expect("Failed to execute with --help");

    assert!(output.status.success());
    let stdout = String::from_utf8_lossy(&output.stdout);
    assert!(stdout.contains("mub_verify_all"));
    assert!(stdout.contains("AuthorityEffect: None"));
    assert!(stdout.contains("Firewall Line: stated region only; mints no authority"));
}

#[test]
fn test_mub_verify_all_cli_output_file() {
    let bin_path = env!("CARGO_BIN_EXE_mub_verify_all");
    let temp_dir = std::env::temp_dir();
    let receipt_path = temp_dir.join("omega_mub_verify_all_test_receipt.json");

    if receipt_path.exists() {
        let _ = fs::remove_file(&receipt_path);
    }

    let output = Command::new(bin_path)
        .arg("--quiet")
        .arg("--output")
        .arg(&receipt_path)
        .output()
        .expect("Failed to execute with --output");

    // The run fails at the unestablished B3 no-go, and a failed run writes
    // no receipt.
    assert!(!output.status.success());
    assert!(
        !receipt_path.exists(),
        "A failed verification must not write a receipt"
    );
}

// ============================================================================
// 4. Epistemic Firewall and Negative Constraint Audit
// ============================================================================

#[test]
fn test_epistemic_firewall_and_negative_constraints() {
    let manifest_dir = env!("CARGO_MANIFEST_DIR");
    let target_file = Path::new(manifest_dir)
        .join("src")
        .join("bin")
        .join("mub_verify_all.rs");

    let source = fs::read_to_string(&target_file)
        .unwrap_or_else(|e| panic!("Failed to read {}: {}", target_file.display(), e));

    // The binary prints the shared firewall line, which is the canonical text.
    assert!(
        source
            .contains("use tfqm_mub::native::exact::mub6_firewall::{AUTHORITY_EFFECT, FIREWALL};"),
        "Source must take its firewall line from mub6_firewall"
    );
    assert_eq!(
        tfqm_mub::native::exact::mub6_firewall::FIREWALL,
        "stated region only; mints no authority"
    );

    assert!(
        !source.contains("MUB(6) = 3"),
        "Source must never assert MUB(6) = 3"
    );
    assert!(
        !source.contains("MUB(6) <= 3"),
        "Source must never assert MUB(6) <= 3"
    );
}
