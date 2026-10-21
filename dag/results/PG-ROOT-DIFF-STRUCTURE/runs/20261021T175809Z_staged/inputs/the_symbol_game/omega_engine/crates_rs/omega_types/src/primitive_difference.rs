//! Canonical PrimitiveDifference types and traits for the Omega Engine.
//!
//! Formal Lean 4 backing: `OmegaCore.PrimitiveDifference` (`000_primitive_axiomatics.md`).
//! Preserves the fundamental invariant: an observable is valid iff it factors through
//! the residual quotient (invariant on zero-difference related inputs).

use serde::{Deserialize, Serialize};

/// Serializable record of one PrimitiveDifference judgment.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct PrimitiveDifferenceJudgment {
    pub left_presentation: String,
    pub right_presentation: String,
    pub zero_difference_relation: String,
    pub licensed_equivalences: Vec<String>,
    pub quotient_residual: String,
    pub residual_class: String,
    pub factors_through_quotient: bool,
}

/// The zero-difference (residual) relation trait over presentations of type `A`.
pub trait PrimitiveDifferenceTrait<A> {
    /// Carrier type of difference vectors.
    type Diff;

    /// Compute difference vector between two presentations: delta(x, y) = x - y.
    fn delta(&self, x: &A, y: &A) -> Self::Diff;

    /// True iff delta is a zero-difference (coboundary / licensed-equivalence).
    fn zero(&self, diff: &Self::Diff) -> bool;

    /// True iff x and y are zero-difference related.
    fn zero_related(&self, x: &A, y: &A) -> bool {
        self.zero(&self.delta(x, y))
    }
}

type ZeroDifferencePredicate<A> = dyn Fn(&A, &A) -> bool + Send + Sync;

/// Closure-based concrete struct for `PrimitiveDifference<A>`.
pub struct PrimitiveDifference<A> {
    zero_fn: Box<ZeroDifferencePredicate<A>>,
}

impl<A> PrimitiveDifference<A> {
    /// Create from any zero-difference predicate.
    pub fn new<F>(zero_fn: F) -> Self
    where
        F: Fn(&A, &A) -> bool + Send + Sync + 'static,
    {
        Self {
            zero_fn: Box::new(zero_fn),
        }
    }

    /// Check if x and y are zero-difference related.
    pub fn zero_related(&self, x: &A, y: &A) -> bool {
        (self.zero_fn)(x, y)
    }

    /// Check if observable phi is invariant over all provided witness pairs.
    pub fn invariant_on<C: PartialEq>(&self, witnesses: &[(A, A)], phi: &impl Fn(&A) -> C) -> bool {
        witnesses
            .iter()
            .all(|(x, y)| !self.zero_related(x, y) || phi(x) == phi(y))
    }

    /// Check if observable phi factors through the residual quotient.
    pub fn factors_through<C: PartialEq>(
        &self,
        witnesses: &[(A, A)],
        phi: &impl Fn(&A) -> C,
    ) -> bool {
        self.invariant_on(witnesses, phi)
    }
}
