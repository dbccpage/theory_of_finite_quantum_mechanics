//! Omega category theory crate.
//!
//! Hierarchical shells under `foundations/`, `category/`, `functor/`, …
//! plus legacy finite-category records at crate root.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.

// --- Hierarchical catalog (new) ---
extern crate self as omega_category_theory;
pub mod abelian;
pub mod adjunction;
pub mod category;
pub mod enriched;
pub mod finite_continuation;
pub mod foundations;
pub mod functor;
#[cfg(test)]
mod l5a_challenges;
pub mod limits_colimits;
pub mod monad;
pub mod monoidal;

// --- Legacy arithmos / finite records (pre-hierarchy) ---
pub mod core {
    pub trait Category {
        type Ob: Clone + PartialEq + Eq + std::fmt::Debug;
        type Mor: Clone + PartialEq + Eq + std::fmt::Debug;

        fn identity<A>(object: &A) -> Self::Mor;
        fn compose<A, B, C>(first: &Self::Mor, second: &Self::Mor) -> Option<Self::Mor>;
    }

    pub trait MorphismEq: Category {
        fn morphism_eq<A, B>(left: &Self::Mor, right: &Self::Mor) -> bool {
            left == right
        }
    }
}

pub mod errors {
    #[derive(Debug, Clone, PartialEq, Eq)]
    pub enum ArithmosError {
        LawViolation(String),
        PreconditionFailed(String),
        InvalidShape(String),
    }
}

pub mod witness {
    #[derive(Debug, Clone, PartialEq, Eq)]
    pub struct Witness {
        pub name: String,
    }

    impl Witness {
        pub fn new(name: impl Into<String>) -> Self {
            Self { name: name.into() }
        }
    }
}

pub mod law {
    use super::errors::ArithmosError;
    use super::witness::Witness;

    pub trait Law {
        type Subject;
        fn check(subject: &Self::Subject) -> Result<Witness, ArithmosError>;
    }
}

pub mod braided_monoidal {
    pub trait BraidedMonoidalCategory: super::monoidal_category::MonoidalCategory {
        fn braiding<A, B>() -> Self::Mor
        where
            Self: super::core::Category;
    }
}

pub mod monoidal_category {
    use super::core::Category;

    pub trait MonoidalCategory: Category {
        type TensorProduct<A, B>: Clone;
        fn unit() -> Self::Ob;
    }
}

pub mod agent_functor;
pub mod arrow;
pub mod bridges;
pub mod cat_functor;
pub mod category_contract_alignment;
pub mod cauchy;
pub mod coend;
pub mod colimits;
pub mod condensation;
pub mod density_matrix_functor;
pub mod eilenberg_moore;
pub mod family_category;
pub mod finite_category;
pub mod finite_category_builder;
pub mod finite_category_validation;
pub mod finite_groupoid;
pub mod finite_profunctor;
pub mod functor_composition;
pub mod grothendieck_construction;
pub mod higher;
pub mod higher_functor;
pub mod hom_adjunction;
pub mod hott_topos_bridge;
pub mod kleisli_category;
pub mod lawvere;
pub mod legacy_adjunction;
pub mod legacy_monad;
pub mod limits;
pub mod morphism;
pub mod mssn_functor_bridge;
pub mod natural_trans;
pub mod natural_trans_composition;
pub mod nerve;
pub mod operad;
pub mod rewriting;
pub mod simplicial_hott_bridge;
pub mod topos_hott_model;
pub mod validation;
pub mod zeta_functor;

// Compatibility aliases for older import paths
pub use legacy_adjunction as adjunction_legacy;
pub use legacy_monad as monad_legacy;

pub mod bounded_counter;
pub mod finite_functional_dependencies;
pub mod finite_moore;
pub mod finite_path;
pub mod finite_relational;

pub mod context_reflection;

pub mod finite_functional_classification;
pub mod finite_retention_choices;
pub mod finite_self_reference;

pub mod dagger;
pub mod finite_history_context;
pub mod finite_partial_structure;
pub mod finite_question_family;
pub mod finite_report_descent;
pub mod finite_report_query;
pub mod finite_report_repair;
pub mod finite_section_separation;

pub mod finite_independence;
pub mod finite_joint_carrier;
pub mod finite_joint_dynamics;
pub mod finite_simulation;
pub mod finite_trace;
