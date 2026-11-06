//! Integration tests for MSS-N Stage 024 pullback monic factorization.
//!
//! AuthorityEffect: None. GenesisEffect: None.

use mssn_stage_024::{Stage024Candidate, Stage024Error};

#[test]
fn test_integration_valid_boundary_packet() {
    let packet = "<stage024<sub<s0><s1>><amb<x0><x1><x2>><m<<s0><x0>><<s1><x1>>><truth<true><false>><true<true>><chi<<x0><true>><<x1><true>><<x2><false>>>>";
    let candidate = Stage024Candidate::parse_boundary_packet(packet)
        .expect("Valid pure boundary packet should parse without error");

    let receipt = candidate
        .verify()
        .expect("Valid pullback monic square should verify PASS");

    assert_eq!(receipt.stage, 24);
    assert_eq!(receipt.status, "PASS");
    assert!(receipt.monic_certified);
    assert!(receipt.commutativity_certified);
    assert!(receipt.pullback_certified);
    assert_eq!(receipt.subobject_size, 2);
    assert_eq!(receipt.ambient_size, 3);
    assert_eq!(receipt.truth_values_count, 2);

    // Verify JSON serialization of typed machine receipt
    let json_str = serde_json::to_string(&receipt).expect("Receipt must serialize to JSON");
    assert!(json_str.contains("\"status\":\"PASS\""));
    assert!(json_str.contains("\"stage\":24"));
}

#[test]
fn test_integration_non_monic_fiber_collision_fails_closed() {
    // Non-monic candidate packet: m(s0) = x0, m(s1) = x0
    let packet = "<stage024<sub<s0><s1>><amb<x0><x1>><m<<s0><x0>><<s1><x0>>><truth<true><false>><true<true>><chi<<x0><true>><<x1><false>>>>";
    let candidate = Stage024Candidate::parse_boundary_packet(packet)
        .expect("Syntax is valid even if mathematical structure fails");

    let err = candidate.verify().expect_err("Non-monic map must fail verification");
    match err {
        Stage024Error::ErrSubobjectMonoDefect(msg) => {
            assert!(msg.contains("fibers collide"));
        }
        other => panic!("Expected ErrSubobjectMonoDefect, got: {:?}", other),
    }
}

#[test]
fn test_integration_label_mismatch_fails_closed() {
    // Diagram does not commute: chi(m(s1)) = false != true
    let packet = "<stage024<sub<s0><s1>><amb<x0><x1>><m<<s0><x0>><<s1><x1>>><truth<true><false>><true<true>><chi<<x0><true>><<x1><false>>>>";
    let candidate = Stage024Candidate::parse_boundary_packet(packet)
        .expect("Packet syntax is valid");

    let err = candidate.verify().expect_err("Non-commuting square must fail verification");
    match err {
        Stage024Error::R024LabelMismatch(msg) => {
            assert!(msg.contains("Diagram does not commute"));
        }
        other => panic!("Expected R024LabelMismatch, got: {:?}", other),
    }
}

#[test]
fn test_integration_not_pullback_fails_closed() {
    // Universal property fails: chi(x2) = true, but x2 is not in im(m)
    let packet = "<stage024<sub<s0>><amb<x0><x2>><m<<s0><x0>>><truth<true><false>><true<true>><chi<<x0><true>><<x2><true>>>>";
    let candidate = Stage024Candidate::parse_boundary_packet(packet)
        .expect("Packet syntax is valid");

    let err = candidate.verify().expect_err("Non-pullback must fail verification");
    match err {
        Stage024Error::R024NotPullback(msg) => {
            assert!(msg.contains("not in the image of m"));
        }
        other => panic!("Expected R024NotPullback, got: {:?}", other),
    }
}

#[test]
fn test_integration_malformed_syntax_fails_closed() {
    let unclosed = "<stage024<sub<s0><s1>>";
    let err = Stage024Candidate::parse_boundary_packet(unclosed).expect_err("Unclosed packet must fail");
    match err {
        Stage024Error::MalformedPacket(_) => (),
        other => panic!("Expected MalformedPacket, got: {:?}", other),
    }

    let missing_section = "<stage024<sub<s0><s1>><amb<x0><x1>>>";
    let err = Stage024Candidate::parse_boundary_packet(missing_section).expect_err("Missing sections must fail");
    match err {
        Stage024Error::MalformedPacket(msg) => {
            assert!(msg.contains("Missing"));
        }
        other => panic!("Expected MalformedPacket, got: {:?}", other),
    }
}
