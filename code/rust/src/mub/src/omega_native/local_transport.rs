//! Checked receipt for the pinned d=6 transport-closure subcertificate.
//!
//! This module validates the shape and key terminal fields of the existing
//! transport-closure receipt. It does not rebuild the Apache-derived
//! certificate and it does not prove coverage of all MUB(6) triples.

use std::path::Path;

use serde::Serialize;
use serde_json::Value;

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Serialize)]
pub enum LocalTransportStatus {
    ReceiptChecked,
    MissingReceipt,
    InvalidReceipt,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct LocalTransportSubcertificate {
    pub status: LocalTransportStatus,
    pub relative_path: &'static str,
    pub scope: &'static str,
    pub h_size: Option<u64>,
    pub generators: Vec<u64>,
    pub stage2_rank: Option<u64>,
    pub invariant_dimension: Option<u64>,
    pub determining_rank: Option<u64>,
    pub checked_properties: Vec<&'static str>,
    pub remaining_obligations: Vec<&'static str>,
    pub error: Option<String>,
}

const TRANSPORT_RECEIPT: &str =
    "../mub/public-export/evidence/transport-closure-exact-2026-06-12.json";

pub fn check_pinned_transport_receipt(crate_root: &Path) -> LocalTransportSubcertificate {
    let path = crate_root.join(TRANSPORT_RECEIPT);
    let bytes = match std::fs::read(&path) {
        Ok(bytes) => bytes,
        Err(error) if error.kind() == std::io::ErrorKind::NotFound => {
            return failed(LocalTransportStatus::MissingReceipt, format!("{error}"));
        }
        Err(error) => return failed(LocalTransportStatus::InvalidReceipt, format!("{error}")),
    };
    let value: Value = match serde_json::from_slice(&bytes) {
        Ok(value) => value,
        Err(error) => return failed(LocalTransportStatus::InvalidReceipt, error.to_string()),
    };

    match validate_transport_receipt(&value) {
        Ok(summary) => summary,
        Err(error) => failed(LocalTransportStatus::InvalidReceipt, error),
    }
}

fn validate_transport_receipt(value: &Value) -> Result<LocalTransportSubcertificate, String> {
    expect_str(
        value,
        &["schema"],
        "invariant_systems.mub6_transport_closure_exact.v1",
    )?;
    expect_bool(value, &["stage1_group", "generator_exact_unitarity"], true)?;
    expect_u64(
        value,
        &["stage1_group", "triple_columns_exact_unit_norm"],
        18,
    )?;
    expect_u64(value, &["stage1_group", "h_size"], 432)?;
    expect_u64(value, &["stage2_ztilde_transport", "n_points"], 441)?;
    expect_u64(value, &["stage2_ztilde_transport", "rank_modp"], 441)?;
    expect_u64(value, &["stage4_dim_inv", "d_inv"], 56)?;
    expect_u64(value, &["stage5_determining_set", "rank_modp"], 56)?;
    expect_u64(value, &["stage5_determining_set", "d_inv"], 56)?;
    expect_bool(value, &["stage0_rebuild", "identity_exact"], true)?;
    expect_bool(value, &["stage0_rebuild", "Q_zstar_zero_exact"], true)?;
    expect_bool(value, &["stage0_rebuild", "Q_kernel71_zero_exact"], true)?;
    expect_bool(value, &["stage0_rebuild", "psd_certified"], true)?;
    expect_bool(value, &["stage6_d_zero", "all_exactly_zero"], true)?;
    expect_bool(
        value,
        &["theorem", "transport_closed_deterministically"],
        true,
    )?;

    let stages = get(value, &["stages_completed"])?
        .as_array()
        .ok_or_else(|| "stages_completed is not an array".to_string())?;
    for stage in [
        "stage0", "stage1", "stage2", "stage3", "stage4", "stage5", "stage6",
    ] {
        if !stages.iter().any(|item| item.as_str() == Some(stage)) {
            return Err(format!("missing completed stage {stage}"));
        }
    }

    let generators = get(value, &["stage1_group", "generators"])?
        .as_array()
        .ok_or_else(|| "stage1_group.generators is not an array".to_string())?
        .iter()
        .map(|item| {
            item.as_u64()
                .ok_or_else(|| "stage1_group.generators contains a non-u64".to_string())
        })
        .collect::<Result<Vec<_>, _>>()?;
    if generators.len() != 3 {
        return Err("stage1_group.generators must contain exactly 3 generators".to_string());
    }

    let line_perms = get(value, &["stage1_group", "generator_line_permutations"])?
        .as_array()
        .ok_or_else(|| "stage1_group.generator_line_permutations is not an array".to_string())?;
    if line_perms.len() != 3 {
        return Err("expected 3 generator line permutations".to_string());
    }
    for perm in line_perms {
        exact_line_permutation(perm)?;
    }

    Ok(LocalTransportSubcertificate {
        status: LocalTransportStatus::ReceiptChecked,
        relative_path: TRANSPORT_RECEIPT,
        scope: "pinned canonical d=6 triple and its H-symmetry certificate lane only",
        h_size: Some(read_u64(value, &["stage1_group", "h_size"])?),
        generators,
        stage2_rank: Some(read_u64(value, &["stage2_ztilde_transport", "rank_modp"])?),
        invariant_dimension: Some(read_u64(value, &["stage4_dim_inv", "d_inv"])?),
        determining_rank: Some(read_u64(value, &["stage5_determining_set", "rank_modp"])?),
        checked_properties: vec![
            "receipt schema matches transport-closure exact v1",
            "H-size, generators, and line permutations of 0..17 match the receipt shape; this is not transport replay",
            "ztilde transport rank matches the 441-dimensional form space",
            "invariant subspace rank matches the 56-dimensional determining set",
            "receipt records exact identity, kernel, PSD, and d-zero checks",
            "receipt records deterministic transport closure with no Schwartz-Zippel residual",
        ],
        remaining_obligations: vec![
            "independent local replay still requires the loaded Q and PSD witness artifacts",
            "this H-lane transport does not classify all admissible MUB(6) triples",
            "transport outside the pinned H-symmetry lane remains unproved",
            "basis-gluing from fourth-vector obstruction to complete-set nonexistence remains unproved",
        ],
        error: None,
    })
}

fn exact_line_permutation(perm: &Value) -> Result<(), String> {
    let perm = perm
        .as_array()
        .ok_or_else(|| "generator line permutation is not an array".to_string())?;
    if perm.len() != 18 {
        return Err("generator line permutation must have 18 entries".to_string());
    }
    let mut seen = [false; 18];
    for entry in perm {
        let index = entry.as_u64().ok_or_else(|| {
            "generator line permutation entries must be integers in 0..17".to_string()
        })?;
        if index >= 18 {
            return Err("generator line permutation entry is outside 0..17".to_string());
        }
        let slot = index as usize;
        if seen[slot] {
            return Err("generator line permutation repeats an index".to_string());
        }
        seen[slot] = true;
    }
    Ok(())
}

fn failed(status: LocalTransportStatus, error: String) -> LocalTransportSubcertificate {
    LocalTransportSubcertificate {
        status,
        relative_path: TRANSPORT_RECEIPT,
        scope: "pinned canonical d=6 triple and its H-symmetry certificate lane only",
        h_size: None,
        generators: vec![],
        stage2_rank: None,
        invariant_dimension: None,
        determining_rank: None,
        checked_properties: vec![],
        remaining_obligations: vec![
            "provide a valid pinned transport-closure receipt",
            "independent local replay still requires the loaded Q and PSD witness artifacts",
            "global MUB(6) cover and gluing remain unproved",
        ],
        error: Some(error),
    }
}

fn expect_str(value: &Value, path: &[&str], expected: &str) -> Result<(), String> {
    let actual = get(value, path)?
        .as_str()
        .ok_or_else(|| format!("{} is not a string", path.join(".")))?;
    if actual == expected {
        Ok(())
    } else {
        Err(format!(
            "{} expected {expected}, got {actual}",
            path.join(".")
        ))
    }
}

fn expect_bool(value: &Value, path: &[&str], expected: bool) -> Result<(), String> {
    let actual = get(value, path)?
        .as_bool()
        .ok_or_else(|| format!("{} is not a bool", path.join(".")))?;
    if actual == expected {
        Ok(())
    } else {
        Err(format!(
            "{} expected {expected}, got {actual}",
            path.join(".")
        ))
    }
}

fn expect_u64(value: &Value, path: &[&str], expected: u64) -> Result<(), String> {
    let actual = read_u64(value, path)?;
    if actual == expected {
        Ok(())
    } else {
        Err(format!(
            "{} expected {expected}, got {actual}",
            path.join(".")
        ))
    }
}

fn read_u64(value: &Value, path: &[&str]) -> Result<u64, String> {
    get(value, path)?
        .as_u64()
        .ok_or_else(|| format!("{} is not a u64", path.join(".")))
}

fn get<'a>(value: &'a Value, path: &[&str]) -> Result<&'a Value, String> {
    let mut cursor = value;
    for segment in path {
        cursor = cursor
            .get(*segment)
            .ok_or_else(|| format!("missing JSON field {}", path.join(".")))?;
    }
    Ok(cursor)
}

#[cfg(test)]
mod tests {
    use super::*;

    fn crate_root() -> &'static Path {
        Path::new(env!("CARGO_MANIFEST_DIR"))
    }

    #[test]
    #[ignore = "needs the ../mub/public-export/evidence receipts, which are not in this repository"]
    fn pinned_transport_receipt_checks_local_h_lane() {
        let cert = check_pinned_transport_receipt(crate_root());
        assert_eq!(cert.status, LocalTransportStatus::ReceiptChecked);
        assert_eq!(cert.h_size, Some(432));
        assert_eq!(cert.generators, vec![5, 18, 402]);
        assert_eq!(cert.stage2_rank, Some(441));
        assert_eq!(cert.invariant_dimension, Some(56));
        assert_eq!(cert.determining_rank, Some(56));
    }

    #[test]
    fn missing_transport_receipt_is_refused_not_checked() {
        let cert = check_pinned_transport_receipt(Path::new("a/directory/with/no/receipts"));
        assert_eq!(cert.status, LocalTransportStatus::MissingReceipt);
        assert!(cert.h_size.is_none());
    }

    fn minimal_receipt(perms: serde_json::Value) -> serde_json::Value {
        serde_json::json!({
            "schema": "invariant_systems.mub6_transport_closure_exact.v1",
            "stage1_group": {
                "generator_exact_unitarity": true,
                "triple_columns_exact_unit_norm": 18,
                "h_size": 432,
                "generators": [5, 18, 402],
                "generator_line_permutations": perms,
            },
            "stage2_ztilde_transport": { "n_points": 441, "rank_modp": 441 },
            "stage4_dim_inv": { "d_inv": 56 },
            "stage5_determining_set": { "rank_modp": 56, "d_inv": 56 },
            "stage0_rebuild": {
                "identity_exact": true,
                "Q_zstar_zero_exact": true,
                "Q_kernel71_zero_exact": true,
                "psd_certified": true,
            },
            "stage6_d_zero": { "all_exactly_zero": true },
            "theorem": { "transport_closed_deterministically": true },
            "stages_completed": ["stage0", "stage1", "stage2", "stage3", "stage4", "stage5", "stage6"],
        })
    }

    #[test]
    fn line_permutation_entries_must_be_a_permutation_of_0_through_17() {
        let identity: Vec<u64> = (0..18).collect();
        let perms = serde_json::json!([identity.clone(), identity.clone(), identity.clone()]);
        let admitted = validate_transport_receipt(&minimal_receipt(perms)).expect("identity");
        assert_eq!(admitted.status, LocalTransportStatus::ReceiptChecked);
        assert!(admitted
            .checked_properties
            .iter()
            .any(|item| item.contains("not transport replay")));

        let eighteen_nulls = vec![serde_json::Value::Null; 18];
        let eighteen_strings = vec!["0"; 18];
        let eighteen_zeros = vec![0; 18];
        let out_of_range: Vec<u64> = (1..19).collect();
        for hostile in [
            serde_json::json!([eighteen_nulls, identity.clone(), identity.clone()]),
            serde_json::json!([eighteen_strings, identity.clone(), identity.clone()]),
            serde_json::json!([eighteen_zeros, identity.clone(), identity.clone()]),
            serde_json::json!([out_of_range, identity.clone(), identity.clone()]),
        ] {
            assert!(validate_transport_receipt(&minimal_receipt(hostile)).is_err());
        }
    }

    #[test]
    #[ignore = "needs the ../mub/public-export/evidence receipts, which are not in this repository"]
    fn pinned_transport_receipt_does_not_close_global_mub6() {
        let cert = check_pinned_transport_receipt(crate_root());
        assert!(cert
            .remaining_obligations
            .iter()
            .any(|obligation| obligation.contains("does not classify all admissible")));
        assert!(cert
            .remaining_obligations
            .iter()
            .any(|obligation| obligation.contains("basis-gluing")));
    }
}
