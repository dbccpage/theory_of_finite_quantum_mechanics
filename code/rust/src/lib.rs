//! Sovereign theory of finite quantum mechanics.

pub mod linear_algebra;
pub mod homology;
pub mod qm;
pub mod dag_witnesses;

pub use tfqm_category_theory as category_theory;
pub use tfqm_combinatorics as combinatorics;
pub use tfqm_finite_probability as finite_probability;
pub use tfqm_functional as functional;
pub use tfqm_fusion_categories as fusion_categories;
pub use tfqm_general_relativity as general_relativity;
pub use tfqm_higher_category_theory as higher_category_theory;
pub use tfqm_holonomy as holonomy;
pub use tfqm_homotopy_type_theory as homotopy_type_theory;
pub use tfqm_lie_theory as lie_theory;
pub use tfqm_local_green_global_red_lggr as local_green_global_red_lggr;
pub use tfqm_majorana as majorana;
pub use tfqm_mub as mub;
pub use tfqm_number_theory as number_theory;
pub use tfqm_operad_theory as operad_theory;
pub use tfqm_sheaf_theory as sheaf_theory;
pub use tfqm_wdp as wdp;

pub use qm::*;
pub use qm::group_param as group_parameter;
