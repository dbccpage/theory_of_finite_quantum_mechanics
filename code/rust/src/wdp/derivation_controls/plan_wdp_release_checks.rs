
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct ReleaseCheckInput {
    pub manuscript_sha256: [u8; 4],
    pub tex_header_sha256: [u8; 4],
    pub relative_directory_href_count: usize,
    pub release_manifest_matches_tree: bool,
    pub checksums_match_tree: bool,
    pub silent_baseline_refresh: bool,
    pub repin_owner_approved: bool,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct ReleaseCheckOutcome {
    pub artifacts_bound: bool,
    pub dec_wdp_repin_separate: bool,
    pub publication_clearance_claimed: bool,
}

pub fn verify_release_check_state(
    input: ReleaseCheckInput,
) -> Result<ReleaseCheckOutcome, &'static str> {
    if input.silent_baseline_refresh {
        return Err("silent trusted-baseline refresh is refused");
    }
    if input.manuscript_sha256 != input.tex_header_sha256 {
        return Err("tex header does not bind current manuscript sha256");
    }
    if input.relative_directory_href_count != 0 {
        return Err("relative directory href would render as .pdf");
    }
    if !input.release_manifest_matches_tree || !input.checksums_match_tree {
        return Err("release manifest or checksum inventory drift");
    }
    Ok(ReleaseCheckOutcome {
        artifacts_bound: true,
        dec_wdp_repin_separate: !input.repin_owner_approved,
        publication_clearance_claimed: false,
    })
}

#[test]
fn release_checks_bind_artifacts_and_refuse_silent_repin() {
    let valid = ReleaseCheckInput {
        manuscript_sha256: [0x12, 0x34, 0x56, 0x78],
        tex_header_sha256: [0x12, 0x34, 0x56, 0x78],
        relative_directory_href_count: 0,
        release_manifest_matches_tree: true,
        checksums_match_tree: true,
        silent_baseline_refresh: false,
        repin_owner_approved: false,
    };
    let outcome = verify_release_check_state(valid).expect("valid release check state");
    assert_eq!(
        outcome,
        ReleaseCheckOutcome {
            artifacts_bound: true,
            dec_wdp_repin_separate: true,
            publication_clearance_claimed: false,
        }
    );

    let mut silent_repin = valid;
    silent_repin.silent_baseline_refresh = true;
    assert_eq!(
        verify_release_check_state(silent_repin),
        Err("silent trusted-baseline refresh is refused")
    );

    let mut dir_href = valid;
    dir_href.relative_directory_href_count = 3;
    assert_eq!(
        verify_release_check_state(dir_href),
        Err("relative directory href would render as .pdf")
    );
}
