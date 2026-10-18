//! Exact finite causal sets, interval abundances and the dimension-two interval action.
//! These finite observables do not identify a continuum spacetime. AuthorityEffect: None.
pub const AUTHORITY_FENCE: &str =
    "AuthorityEffect None; not PROVED; not GlobalGreen; finite causal set; no continuum admission.";
use num_bigint::BigInt;
use num_traits::Zero;
use omega_homology::finite_poset::{FinitePoset, PosetError};
use omega_number_theory::rational::Rational;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct CausalSet {
    pub degree: usize,
    pub label: String,
    order: FinitePoset,
}
impl CausalSet {
    /// A discrete causal set of `degree` events carrying the declared label.
    /// Use from_order for a nontrivial validated causal order.
    pub fn new(degree: usize, label: impl Into<String>) -> Result<Self, PosetError> {
        Ok(Self {
            degree,
            label: label.into(),
            order: FinitePoset::new(degree, [])?,
        })
    }
    pub fn from_order(order: FinitePoset, label: impl Into<String>) -> Self {
        Self {
            degree: order.size(),
            label: label.into(),
            order,
        }
    }
    pub fn authority_fence() -> &'static str {
        AUTHORITY_FENCE
    }
    pub fn order(&self) -> &FinitePoset {
        &self.order
    }
    pub fn spacelike(&self, u: usize, v: usize) -> Result<bool, PosetError> {
        Ok(u != v && !self.order.less(u, v)? && !self.order.less(v, u)?)
    }
    pub fn alexandrov_interval(&self, u: usize, v: usize) -> Result<Vec<usize>, PosetError> {
        self.order.interval(u, v)
    }
    pub fn past(&self, v: usize) -> Result<Vec<usize>, PosetError> {
        self.order.predecessors(v)
    }
    pub fn future(&self, v: usize) -> Result<Vec<usize>, PosetError> {
        self.order.successors(v)
    }
    pub fn ordering_fraction(&self) -> Rational {
        let n = self.order.size();
        if n < 2 {
            return Rational::zero();
        }
        Rational::new(
            BigInt::from(2) * BigInt::from(self.order.relation_count()),
            BigInt::from(n) * BigInt::from(n - 1),
        )
    }
    /// Counts comparable pairs with each cardinality of their open interval.
    pub fn interval_abundances(&self) -> Result<Vec<BigInt>, PosetError> {
        let mut counts = vec![BigInt::zero(); self.order.size().saturating_sub(1)];
        for (u, v) in self.order.strict_relations() {
            let open = self.order.interval(u, v)?.len() - 2;
            counts[open] += 1;
        }
        Ok(counts)
    }
    /// The dimension-two Benincasa-Dowker interval polynomial, before any
    /// continuum normalization: N-2N0+4N1-2N2 (Ni has i interior events).
    pub fn two_dimensional_interval_action(&self) -> Result<BigInt, PosetError> {
        let counts = self.interval_abundances()?;
        let count = |i| counts.get(i).cloned().unwrap_or_else(BigInt::zero);
        Ok(BigInt::from(self.order.size()) - 2 * count(0) + 4 * count(1) - 2 * count(2))
    }
}
