//! Functor hierarchy shells for omega_category_theory.
//! AuthorityEffect: None. Not PROVED / GlobalGreen.

pub mod constant_functor;
pub mod copresheaf;
pub mod diagonal_functor;
pub mod equivalence_of_categories;
pub mod essentially_surjective;
pub mod faithful_functor;
pub mod forgetful_functor;
pub mod free_functor;
pub mod full_functor;
#[allow(clippy::module_inception)]
pub mod functor;
pub mod functor_category;
pub mod hom_functor;
pub mod horizontal_composition;
pub mod identity_functor;
pub mod isomorphism_of_categories;
pub mod nat_trans_components;
pub mod natural_transformation;
pub mod presheaf;
pub mod representable_functor;
pub mod vertical_composition;
pub mod yoneda;

pub use constant_functor::ConstantFunctor;
pub use copresheaf::Copresheaf;
pub use diagonal_functor::DiagonalFunctor;
pub use equivalence_of_categories::EquivalenceOfCategories;
pub use essentially_surjective::EssentiallySurjective;
pub use faithful_functor::FaithfulFunctor;
pub use forgetful_functor::ForgetfulFunctor;
pub use free_functor::FreeFunctor;
pub use full_functor::FullFunctor;
pub use functor::Functor;
pub use functor_category::FunctorCategory;
pub use hom_functor::HomFunctor;
pub use horizontal_composition::HorizontalComposition;
pub use identity_functor::IdentityFunctor;
pub use isomorphism_of_categories::IsomorphismOfCategories;
pub use nat_trans_components::NatTransComponents;
pub use natural_transformation::NaturalTransformation;
pub use presheaf::Presheaf;
pub use representable_functor::RepresentableFunctor;
pub use vertical_composition::VerticalComposition;
pub use yoneda::Yoneda;
