//! Finite discrete spacetime as a simplicial complex.
//!
//! Combinatorial carrier is [`omega_homology::simplicial::SimplicialComplex`]
//! (canonical face-closed complex). Metric / Regge data live in
//! [`crate::regge_calculus`].
//!
//! AuthorityEffect: None. Not continuum GR. Not PROVED / GlobalGreen.

use omega_homology::errors::HomologicalError;
use omega_homology::simplicial::{OrientedSimplex, Simplex, SimplicialComplex};

/// Fence string (proposal).
pub const AUTHORITY_FENCE: &str =
    "AuthorityEffect None; not PROVED; not GlobalGreen; finite simplicial spacetime.";

/// Finite discrete spacetime: face-closed simplicial complex + label.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DiscreteSpacetime {
    /// Combinatorial spacetime (closed under faces).
    pub complex: SimplicialComplex,
    /// Stable label.
    pub label: String,
}

impl DiscreteSpacetime {
    /// Scaffold constructor: standard n-simplex (combinatorial only).
    ///
    /// `degree` maps to ambient dimension n = max(degree, 0) of Δⁿ.
    pub fn new(degree: usize, label: impl Into<String>) -> Self {
        let complex = SimplicialComplex::standard_n_simplex(degree)
            .expect("standard_n_simplex succeeds for finite n");
        Self {
            complex,
            label: label.into(),
        }
    }

    /// Build from maximal simplices (auto face-closure via omega_homology).
    pub fn try_from_maximal(
        maximal: Vec<OrientedSimplex>,
        label: impl Into<String>,
    ) -> Result<Self, HomologicalError> {
        Ok(Self {
            complex: SimplicialComplex::from_maximal_simplices(maximal)?,
            label: label.into(),
        })
    }

    /// Standard combinatorial n-simplex.
    pub fn standard_simplex(n: usize, label: impl Into<String>) -> Result<Self, HomologicalError> {
        Ok(Self {
            complex: SimplicialComplex::standard_n_simplex(n)?,
            label: label.into(),
        })
    }

    /// Event / vertex count.
    pub fn event_count_proxy(&self) -> usize {
        self.complex.num_vertices()
    }

    /// Degree proxy = max simplex dimension.
    pub fn degree(&self) -> usize {
        self.complex.max_dimension()
    }

    /// Number of k-simplices.
    pub fn count(&self, dim: usize) -> usize {
        self.complex.count(dim)
    }

    /// Euler characteristic χ (combinatorial).
    pub fn euler_characteristic(&self) -> i64 {
        self.complex.euler_characteristic()
    }

    /// Whether the complex contains a simplex.
    pub fn contains(&self, simplex: &Simplex) -> bool {
        self.complex.contains(simplex)
    }

    pub fn authority_fence() -> &'static str {
        AUTHORITY_FENCE
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn triangle_has_three_edges() {
        let st = DiscreteSpacetime::standard_simplex(2, "Δ2").unwrap();
        assert_eq!(st.count(0), 3);
        assert_eq!(st.count(1), 3);
        assert_eq!(st.count(2), 1);
        assert_eq!(st.euler_characteristic(), 1); // disk-like triangle χ=1
    }

    #[test]
    fn new_and_fence() {
        let x = DiscreteSpacetime::new(1, "test");
        assert_eq!(x.degree(), 1);
        assert!(DiscreteSpacetime::authority_fence().contains("AuthorityEffect None"));
    }
}
