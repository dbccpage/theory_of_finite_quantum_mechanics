//! Omega Higher Category Theory crate.
//!
//! Provides mathematically rigorous foundations for higher category theory:
//! - Strict 2-categories (`two_category`)
//! - Weak 2-categories / Bicategories (`bicategory`)
//! - Middle-four exchange / interchange law (`exchange`)
//! - Mac Lane pentagon & triangle coherence verification (`coherence`)
//! - Differential Graded categories (`dg_category`)
//! - Triangulated categories and Verdier axioms (`triangulated`)
//! - Derived categories and mapping cones (`derived`)
//! - Bounded derived categories (`bounded_derived`)
//! - Unbounded derived categories (`unbounded_derived`)
//! - Strict double categories (`double_category`)
//! - Enriched categories (`enriched`)
//! - Typed error domain and Soviet Builder allocation (`error`), using
//!   `omega_kernel::resource_limits::OperationLimits` directly
//!
//! AuthorityEffect: None.

pub mod bicategory;
pub mod bounded_derived;
pub mod coherence;
pub mod compactly_generated;
pub mod dendroidal_set;
pub mod derived;
pub mod dg_category;
pub mod double_category;
pub mod enriched;
pub mod error;
pub mod exchange;
pub mod model_category;
pub mod operadic_nerve;
pub mod simplicial_set;
pub mod stable_infinity;
pub mod triangulated;
pub mod two_category;
pub mod unbounded_derived;

pub use bicategory::{Bicategory, FiniteBicategory, Invertible2Cell};
pub use bounded_derived::{BoundedComplex, BoundedDerivedCategory, CohomologyBoundValidator};
pub use coherence::{
    check_pentagon_coherence, check_triangle_coherence, verify_bicategory_coherence,
    CoherenceReport,
};
pub use compactly_generated::{
    CompactObject, CompactlyGeneratedCategory, DiagramStage, FactorizationWitness, FilteredDiagram,
};
pub use dendroidal_set::{DendroidalSet, PlanarTree, TreeEdge, TreeInnerHorn, TreeVertex};
pub use derived::{
    ChainComplex, ChainMap, ConeDifferentialMatrix, DerivedCategory, MappingCone, QuasiIsomorphism,
};
pub use dg_category::{
    add_terms, canonicalize_terms, scale_terms, ChainDifferential, CohomologyCategoryH0,
    DgCategory, DifferentialMap, GradedHomComplex, GradedMorphism, LeibnizSignValidator,
};
pub use double_category::{
    DoubleCategory, HorizontalCell, SquareCell, SquareInterchange, VerticalCell,
};
pub use enriched::{EnrichedCategory, EnrichedComposition, EnrichedUnit, EnrichedUnitMorphism, HomObject};
pub use error::{reserve_exact, HigherCategoryError};
pub use exchange::{
    check_exchange_composability, verify_all_exchange_laws, verify_exchange_law, ExchangeQuadruple,
};
pub use model_category::{
    CommutativeSquare, ModelCategory, ModelMorphism, MorphismFactorizations,
};
pub use operadic_nerve::{
    fill_inner_horn_2_1, ColouredOperad, InnerHorn2_1, MultiAryOp, OperadNerve0, OperadNerve1,
    OperadNerve2, OperadicNerve,
};
pub use simplicial_set::{
    Horn, KanComplexValidator, QuasiCategoryValidator, Simplex, SimplicialSet,
};
pub use stable_infinity::{
    FiberSequence, PointedMorphism, PointedObject, SpectrumLevel, StableInfinityCategory,
};
pub use triangulated::{
    DistinguishedTriangle, OctahedralBraidValidator, OctahedralDiagram, RotationValidator,
    TranslationFunctor, TriangulatedCategory,
};
pub use two_category::{OneMorphismData, Strict2Category, TwoCategory, TwoMorphismData};
pub use unbounded_derived::{ChainComplexChain, ResolutionStrategy, UnboundedDerivedCategory};

