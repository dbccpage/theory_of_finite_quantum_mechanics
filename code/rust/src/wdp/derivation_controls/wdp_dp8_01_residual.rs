#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ProductTargetSpec<'a> {
    pub target_id: &'a str,
    pub consumer: &'a str,
    pub defect_witness: &'a str,
    pub rust_owner: &'a str,
    pub deciding_check: &'a str,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ProductTargetSelectionReceipt {
    pub status: &'static str,
    pub selected_count: usize,
    pub reason: &'static str,
}

pub fn verify_product_target_selection(
    targets: &[ProductTargetSpec<'_>],
) -> ProductTargetSelectionReceipt {
    if targets.is_empty() {
        return ProductTargetSelectionReceipt {
            status: "REFUSED",
            selected_count: 0,
            reason: "EMPTY_PRODUCT_TARGET_SET",
        };
    }
    for (idx, t) in targets.iter().enumerate() {
        if t.target_id.trim().is_empty()
            || t.consumer.trim().is_empty()
            || t.defect_witness.trim().is_empty()
            || t.rust_owner.trim().is_empty()
            || t.deciding_check.trim().is_empty()
        {
            return ProductTargetSelectionReceipt {
                status: "REFUSED",
                selected_count: idx,
                reason: "MISSING_REQUIRED_TARGET_FIELD",
            };
        }
        if !t.rust_owner.starts_with("omega_engine/crates_rs/") {
            return ProductTargetSelectionReceipt {
                status: "REFUSED",
                selected_count: idx,
                reason: "NON_CANONICAL_RUST_OWNER",
            };
        }
    }
    ProductTargetSelectionReceipt {
        status: "PASS",
        selected_count: targets.len(),
        reason: "CONCRETE_PRODUCT_TARGETS_VERIFIED",
    }
}

#[test]
fn test_wdp_dp8_01_residual_product_target_selection() {
    let valid = [
        ProductTargetSpec {
            target_id: "TARGET-1-PROTECTED-QUESTION-SEAM",
            consumer: "omega_engine_woland",
            defect_witness: "unwitnessed_summary_collapse",
            rust_owner: "omega_engine/crates_rs/omega_wdp/src/lib.rs",
            deciding_check: "cargo test -p omega_wdp",
        },
        ProductTargetSpec {
            target_id: "TARGET-2-PARITY-BRIDGE",
            consumer: "omega_engine_pfp",
            defect_witness: "untyped_packet_fallback",
            rust_owner: "omega_engine/crates_rs/omega_symbol_game/src/lib.rs",
            deciding_check: "cargo test -p omega_symbol_game",
        },
    ];
    let ok = verify_product_target_selection(&valid);
    assert_eq!(ok.status, "PASS");
    assert_eq!(ok.selected_count, 2);

    let invalid = [ProductTargetSpec {
        target_id: "TARGET-BAD",
        consumer: "omega_engine_woland",
        defect_witness: "",
        rust_owner: "omega_engine/crates_rs/omega_wdp/src/lib.rs",
        deciding_check: "cargo test -p omega_wdp",
    }];
    let bad = verify_product_target_selection(&invalid);
    assert_eq!(bad.status, "REFUSED");
    assert_eq!(bad.reason, "MISSING_REQUIRED_TARGET_FIELD");
}
