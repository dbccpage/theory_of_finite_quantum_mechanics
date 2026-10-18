//! `spectral_triple` — finite dual-face object for `omega_general_relativity`.
//!
//! AUTHORING_QUALITY: human_llm_best_effort_slop (best-effort dual-face scaffold; not human-canon math; not PROVED; not GlobalGreen).
//! **AuthorityEffect:** None.

/// Fence string (proposal).
pub const AUTHORITY_FENCE: &str =
    "AuthorityEffect None; not PROVED; not GlobalGreen; best-effort scaffold.";

/// Finite carrier for `spectral_triple` (proposal; not full classical object).
#[derive(Debug, Clone, PartialEq, Eq, Default)]
pub struct SpectralTriple {
    /// Degree / dimension / stage proxy (ℕ₀).
    pub degree: usize,
    /// Stable label / object id (finite string).
    pub label: String,
}

impl SpectralTriple {
    /// Construct a finite carrier.
    pub fn new(degree: usize, label: impl Into<String>) -> Self {
        Self {
            degree,
            label: label.into(),
        }
    }

    /// Authority fence (never mints PROVED/GlobalGreen).
    pub fn authority_fence() -> &'static str {
        AUTHORITY_FENCE
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn new_and_fence() {
        let x = SpectralTriple::new(1, "test");
        assert_eq!(x.degree, 1);
        assert_eq!(x.label, "test");
        assert!(SpectralTriple::authority_fence().contains("AuthorityEffect None"));
    }
}
