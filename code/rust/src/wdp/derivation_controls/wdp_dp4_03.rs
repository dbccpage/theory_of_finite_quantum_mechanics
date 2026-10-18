#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ClaimIndexParityReceipt {
    pub status: &'static str,
    pub matched_count: usize,
    pub reason: &'static str,
}

pub fn check_claim_index_parity(
    expected: &[&str],
    lean: &[&str],
    python: &[&str],
    rust: &[&str],
) -> ClaimIndexParityReceipt {
    if expected.is_empty() {
        return ClaimIndexParityReceipt {
            status: "REFUSED",
            matched_count: 0,
            reason: "EMPTY_EXPECTED_CLAIM_SET",
        };
    }
    for id in expected {
        if !lean.contains(id) || !python.contains(id) || !rust.contains(id) {
            return ClaimIndexParityReceipt {
                status: "REFUSED",
                matched_count: 0,
                reason: "MISSING_CLAIM_BINDING",
            };
        }
    }
    for slice in [lean, python, rust] {
        for id in slice {
            if !expected.contains(id) {
                return ClaimIndexParityReceipt {
                    status: "REFUSED",
                    matched_count: expected.len(),
                    reason: "UNDECLARED_ORPHAN_CLAIM_ID",
                };
            }
        }
    }
    ClaimIndexParityReceipt {
        status: "PASS",
        matched_count: expected.len(),
        reason: "EXACT_THREE_WAY_CLAIM_PARITY",
    }
}

#[test]
fn test_wdp_dp4_03_claim_index_parity() {
    let claims = ["WDP-THM-2.2", "WDP-PROP-4.2", "WDP-THM-9.3"];
    let ok = check_claim_index_parity(&claims, &claims, &claims, &claims);
    assert_eq!(ok.status, "PASS");
    assert_eq!(ok.matched_count, 3);

    let missing = check_claim_index_parity(&claims, &claims[..2], &claims, &claims);
    assert_eq!(missing.status, "REFUSED");
    assert_eq!(missing.reason, "MISSING_CLAIM_BINDING");

    let orphan = check_claim_index_parity(&claims[..1], &claims[..2], &claims[..1], &claims[..1]);
    assert_eq!(orphan.status, "REFUSED");
    assert_eq!(orphan.reason, "UNDECLARED_ORPHAN_CLAIM_ID");
}
