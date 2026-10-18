//! Realization Tier for Operad Theory.
//!
//! AuthorityEffect: None.

pub mod algebra_over_operad;
pub mod module_over_operad;
pub mod associativity_witness;

pub use algebra_over_operad::{EvaluationOutcome, EvaluationReceipt, OperadAlgebra, PolicyDecisionRef};
pub use module_over_operad::{AlgebraModule, OperadicModule};
pub use associativity_witness::{ComputationStatus, EvidenceKind, LawResult, StructuralAssociativityWitness};
