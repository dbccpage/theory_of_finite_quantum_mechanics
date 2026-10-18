
pub mod cech;
pub mod empirical_presheaf;
pub mod epistemic_observer;
pub mod exact_sequence;
pub mod finite_report_gluing;
pub mod functors;
pub mod open_set;
pub mod presheaf;
pub mod sheaf;
pub mod sheafification;
pub mod site;
pub mod stack;
pub mod stalk;
pub mod structure_sheaf;
pub mod torsor;

pub const AUTHORITY_FENCE: &str =
    "AuthorityEffect None; not PROVED; not GlobalGreen; finite simplicial sheaf theory.";

pub use cech::{
    cech_coboundary_rational, compute_cech_h0, compute_cech_h1_obstruction, CechCochain,
    CechH1Result,
};
pub use exact_sequence::{
    connecting_homomorphism_delta_star, is_flasque_sheaf, ConnectingHomomorphismResult,
    LocalToGlobalSpectralSequencePage, PartitionOfUnity,
};
pub use functors::{pullback_presheaf, pushforward_sheaf};
pub use open_set::{Cover, OpenSet, PosetTopology};
pub use presheaf::{presheaf_kernel, Presheaf, PresheafError, PresheafMorphism};
pub use sheaf::{
    check_separated, check_sheaf_condition, compute_equalizer_kernel, SheafConditionResult,
};
pub use sheafification::{
    make_constant_presheaf, make_skyscraper_sheaf, plus_construction, sheafify,
};
pub use site::{validate_sheaf_on_site, GrothendieckSite};
pub use stack::{
    CharacterStack, DerivedScheme, DerivedStack, HigherStack, Hypercover, Stack, StackyGroupoid,
};
pub use stalk::{compute_stalk, Germ};
pub use structure_sheaf::StructureSheaf;
pub use torsor::PrincipalBundleZ2;

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_authority_fence() {
        assert!(AUTHORITY_FENCE.contains("AuthorityEffect None"));
    }
}
