#[derive(Debug, Clone, PartialEq, Eq)]
pub struct CleanExportReceipt {
    pub status: &'static str,
    pub verified_files: usize,
    pub reason: &'static str,
}

pub fn verify_clean_export_manifest(
    declared: &[(&str, &str)],
    extracted: &[(&str, &str)],
    outside_refs: &[&str],
) -> CleanExportReceipt {
    if declared.is_empty() {
        return CleanExportReceipt {
            status: "REFUSED",
            verified_files: 0,
            reason: "EMPTY_DECLARED_MANIFEST",
        };
    }
    if !outside_refs.is_empty() {
        return CleanExportReceipt {
            status: "REFUSED",
            verified_files: 0,
            reason: "HERMETIC_ESCAPE_TO_CHECKOUT",
        };
    }
    if declared.len() != extracted.len() {
        return CleanExportReceipt {
            status: "REFUSED",
            verified_files: 0,
            reason: "UNDECLARED_EXTRACTED_FILE",
        };
    }
    for (path, sha) in declared {
        if path.starts_with('/') || path.split('/').any(|p| p == "..") {
            return CleanExportReceipt {
                status: "REFUSED",
                verified_files: 0,
                reason: "UNSAFE_MANIFEST_PATH",
            };
        }
        match extracted.iter().find(|(ep, _)| ep == path) {
            Some((_, esha)) if esha == sha => {}
            _ => {
                return CleanExportReceipt {
                    status: "REFUSED",
                    verified_files: 0,
                    reason: "HASH_MISMATCH",
                };
            }
        }
    }
    CleanExportReceipt {
        status: "PASS",
        verified_files: declared.len(),
        reason: "CLEAN_EXPORT_VERIFIED",
    }
}

#[test]
fn test_wdp_dp7_03_clean_export_verification() {
    let manifest = [("manuscript.md", "sha256:aaa"), ("code/witness.py", "sha256:bbb")];
    let ok = verify_clean_export_manifest(&manifest, &manifest, &[]);
    assert_eq!(ok.status, "PASS");
    assert_eq!(ok.verified_files, 2);

    let escaped = verify_clean_export_manifest(&manifest, &manifest, &["../checkout.json"]);
    assert_eq!(escaped.status, "REFUSED");
    assert_eq!(escaped.reason, "HERMETIC_ESCAPE_TO_CHECKOUT");
}
