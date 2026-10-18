
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ClaimStatus {
    Verified,
    BoundedExternal,
    OpenDeclared,
    UnverifiedWritten,
    InvalidLink,
}

pub fn recompute_claim_status(
    declared: ClaimStatus,
    pointers_all_exist: bool,
    deps_all_verified: bool,
) -> ClaimStatus {
    if !pointers_all_exist {
        return ClaimStatus::InvalidLink;
    }
    if declared == ClaimStatus::Verified && !deps_all_verified {
        return ClaimStatus::UnverifiedWritten;
    }
    declared
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_p5_recompute_status() {
        assert_eq!(
            recompute_claim_status(ClaimStatus::Verified, true, true),
            ClaimStatus::Verified
        );
        assert_eq!(
            recompute_claim_status(ClaimStatus::Verified, false, true),
            ClaimStatus::InvalidLink
        );
        assert_eq!(
            recompute_claim_status(ClaimStatus::Verified, true, false),
            ClaimStatus::UnverifiedWritten
        );
    }
}
