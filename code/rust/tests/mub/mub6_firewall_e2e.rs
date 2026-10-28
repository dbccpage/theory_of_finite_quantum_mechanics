//! End-to-end launches of the two MUB(6) bins.
//!
//! Each bin runs twice. Stdout must carry the firewall, stay free of a solved
//! global claim, and match across the pair. Conjecture 2 stays a finite sample.
//! The gap solver's certificate types stay proposals.
//!
//! AuthorityEffect: None
//! Firewall Line: NOT MUB(6)=3, NOT MUB(6)<=3; stated region only; mints no authority

use std::process::Command;

use tfqm_mub::native::exact::mub6_firewall::FIREWALL;

fn run(bin: &str) -> (String, String, i32) {
    let path = match bin {
        "mub6_gap_solver" => env!("CARGO_BIN_EXE_mub6_gap_solver"),
        "mub6_conj2_verifier" => env!("CARGO_BIN_EXE_mub6_conj2_verifier"),
        other => panic!("unknown bin {other}"),
    };
    let output = Command::new(path)
        .output()
        .unwrap_or_else(|err| panic!("launch {bin}: {err}"));
    let code = output.status.code().unwrap_or(1);
    let stdout = String::from_utf8_lossy(&output.stdout).to_string();
    let stderr = String::from_utf8_lossy(&output.stderr).to_string();
    (stdout, stderr, code)
}

fn asserts_no_solved_claim(stdout: &str) {
    assert!(
        stdout.contains(FIREWALL),
        "missing firewall:\n{stdout}"
    );
    let stripped = stdout.replace(FIREWALL, "");
    for claim in [
        "MUB(6)=3",
        "MUB(6)<=3",
        "MUB(6) = 3",
        "MUB(6) <= 3",
        "global solution",
        "CERTIFIED_ALL_CHECKS_PASSED",
    ] {
        assert!(
            !stripped.contains(claim),
            "stdout states {claim} outside the firewall:\n{stdout}"
        );
    }
}

#[test]
fn gap_solver_firewall_is_stable_and_does_not_verify_proposals() {
    let first = run("mub6_gap_solver");
    let second = run("mub6_gap_solver");
    assert_eq!(first.2, 0, "stderr:\n{}", first.1);
    assert_eq!(first.0, second.0, "stdout drifted");
    assert_eq!(first.1, second.1, "stderr drifted");
    asserts_no_solved_claim(&first.0);
    assert!(
        first.0.contains("AlgebraicElimination"),
        "the report should list a proposed certificate type"
    );
    assert!(
        !first.0.contains("\"verified\""),
        "proposed certificate types must not be marked verified:\n{}",
        first.0
    );
}

#[test]
fn conj2_verifier_is_a_stable_finite_sample() {
    let first = run("mub6_conj2_verifier");
    let second = run("mub6_conj2_verifier");
    assert_eq!(first.2, 0, "stderr:\n{}\nstdout:\n{}", first.1, first.0);
    assert_eq!(first.0, second.0, "stdout drifted");
    assert_eq!(first.1, second.1, "stderr drifted");
    asserts_no_solved_claim(&first.0);
    assert!(
        first.0.contains("finite-sample"),
        "Conj2 must say it is a finite sample:\n{}",
        first.0
    );
    assert!(
        first.0.contains("not a proof"),
        "Conj2 must refuse a proof claim:\n{}",
        first.0
    );
}
