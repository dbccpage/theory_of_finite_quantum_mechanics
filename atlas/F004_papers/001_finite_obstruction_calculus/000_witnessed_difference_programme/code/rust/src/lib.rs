// Executable finite evidence; AuthorityEffect: None.
//! # Witnessed Difference Programme (WDP) Finite Witness & Obstruction Calculus
//!
//! Sovereign, hermetic Rust crate implementing exact finite obstruction calculus,
//! discrete rational cochains, Moore behavioral quotients, and Genesis history transducers.
//!
//! In accordance with Anomalon and CODA doctrine:
//! - All computations operate with `AuthorityEffect::None`.
//! - Discrete exactness is guaranteed using `num_rational::BigRational`.
//! - Floating-point representations are rejected by the exact rational firewall.

pub mod cochains;
pub mod difference;
pub mod error;
pub mod foundational_bridges;
pub mod functional_classification;
pub mod genesis_observer;
pub mod obstruction;
pub mod profile_evaluator;
pub mod self_reference;
pub mod semiring;

pub use cochains::{Cochain0, Cochain1, FiniteComplex};
pub use difference::{Carrier, Mark};
pub use error::WdpError;
pub use foundational_bridges::{
    admit_mark, apartness_witness, bool_d0, bool_d1, bool_xor, check_no_authority_effect,
    compute_triangle_mark_differences, empty_inscription, evaluate_report_claim,
    find_rational_l1_minimizer, product_transducer, rational_l1_norm, solve_frustrated_spin_cycle,
    verify_deterministic_retention, verify_flat_locus_curvature, verify_triangle_coboundary_zero,
    AuthorityEffect, EvaluationStatus as BridgeEvaluationStatus, FiniteTransducer, Inscription,
    MathematicalReceipt, MultiplicityDistribution,
};
pub use functional_classification::{classify_observer, FunctionalClass};
pub use genesis_observer::{DescentResult, HistoryMemory, WordTransducer};
pub use obstruction::{solve_exact_potential, DualWitnessCertificate};
pub use profile_evaluator::{EvaluationStatus, Evidence, FiniteProfile};
pub use self_reference::{evaluate_diagonal_fixed_point, SelfReferenceWitness};
pub use semiring::{coarse_grain, CoarseGrainReceipt};
