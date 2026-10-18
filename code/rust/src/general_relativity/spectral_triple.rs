
pub const AUTHORITY_FENCE: &str =
    "AuthorityEffect None; not PROVED; not GlobalGreen; best-effort scaffold.";

#[derive(Debug, Clone, PartialEq, Eq, Default)]
pub struct SpectralTriple {
    pub degree: usize,
    pub label: String,
}

impl SpectralTriple {
    pub fn new(degree: usize, label: impl Into<String>) -> Self {
        Self {
            degree,
            label: label.into(),
        }
    }

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
