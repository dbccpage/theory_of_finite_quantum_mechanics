//! Companion Rust witness for PROD-P5-NEXT-2 (CertificationService 21.11 dependency-order propagation).

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Status {
    Proved,
    Undetermined,
}

pub fn propagate_21_11_chain(
    c1_pointers_complete: bool,
    c2_pointers_complete: bool,
    c3_pointers_complete: bool,
    c_ind_pointers_complete: bool,
) -> (Status, Status, Status, Status) {
    let s1 = if c1_pointers_complete {
        Status::Proved
    } else {
        Status::Undetermined
    };
    let s2 = if c2_pointers_complete && s1 == Status::Proved {
        Status::Proved
    } else {
        Status::Undetermined
    };
    let s3 = if c3_pointers_complete && s2 == Status::Proved {
        Status::Proved
    } else {
        Status::Undetermined
    };
    let s_ind = if c_ind_pointers_complete {
        Status::Proved
    } else {
        Status::Undetermined
    };
    (s1, s2, s3, s_ind)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn missing_pointer_at_root_propagates_along_dependency_chain_only() {
        let (s1, s2, s3, s_ind) = propagate_21_11_chain(false, true, true, true);
        assert_eq!(s1, Status::Undetermined);
        assert_eq!(s2, Status::Undetermined);
        assert_eq!(s3, Status::Undetermined);
        assert_eq!(s_ind, Status::Proved);
    }
}
