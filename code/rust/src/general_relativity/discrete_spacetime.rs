
use engine_homology::errors::HomologicalError;
use engine_homology::simplicial::{OrientedSimplex, Simplex, SimplicialComplex};

pub const AUTHORITY_FENCE: &str =
    "AuthorityEffect None; not PROVED; not GlobalGreen; finite simplicial spacetime.";

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DiscreteSpacetime {
    pub complex: SimplicialComplex,
    pub label: String,
}

impl DiscreteSpacetime {
    pub fn new(degree: usize, label: impl Into<String>) -> Self {
        let complex = SimplicialComplex::standard_n_simplex(degree)
            .expect("standard_n_simplex succeeds for finite n");
        Self {
            complex,
            label: label.into(),
        }
    }

    pub fn try_from_maximal(
        maximal: Vec<OrientedSimplex>,
        label: impl Into<String>,
    ) -> Result<Self, HomologicalError> {
        Ok(Self {
            complex: SimplicialComplex::from_maximal_simplices(maximal)?,
            label: label.into(),
        })
    }

    pub fn standard_simplex(n: usize, label: impl Into<String>) -> Result<Self, HomologicalError> {
        Ok(Self {
            complex: SimplicialComplex::standard_n_simplex(n)?,
            label: label.into(),
        })
    }

    pub fn event_count_proxy(&self) -> usize {
        self.complex.num_vertices()
    }

    pub fn degree(&self) -> usize {
        self.complex.max_dimension()
    }

    pub fn count(&self, dim: usize) -> usize {
        self.complex.count(dim)
    }

    pub fn euler_characteristic(&self) -> i64 {
        self.complex.euler_characteristic()
    }

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
        assert_eq!(st.euler_characteristic(), 1);
    }

    #[test]
    fn new_and_fence() {
        let x = DiscreteSpacetime::new(1, "test");
        assert_eq!(x.degree(), 1);
        assert!(DiscreteSpacetime::authority_fence().contains("AuthorityEffect None"));
    }
}
