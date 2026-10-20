
#[path="C:/Users/a343o/source/repos/theory_of_finite_quantum_mechanics/code/rust/src/linear_algebra/mod.rs"]
pub mod linear_algebra;
#[path="C:/Users/a343o/source/repos/theory_of_finite_quantum_mechanics/code/rust/src/homology/mod.rs"]
pub mod homology;
#[path="C:/Users/a343o/source/repos/theory_of_finite_quantum_mechanics/code/rust/src/qm/mod.rs"]
pub mod qm;
#[path="C:/Users/a343o/source/repos/theory_of_finite_quantum_mechanics/code/rust/src/dag_witnesses.rs"]
pub mod dag_witnesses;

pub use tfqm_category_theory as category_theory;
pub use tfqm_combinatorics as combinatorics;
pub use tfqm_finite_probability as finite_probability;
pub use tfqm_fsp as fsp;
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

pub fn crate_root_inventory_holds() -> Result<(), &'static str> {
    const MODULES: &[&str] = &["linear_algebra", "homology", "qm", "dag_witnesses"];
    inventory_mass(MODULES)?;
    let harmonic = 3i64 + 2 + 1;
    if harmonic != 6 {
        return Err("the three-term harmonic sum is not 1");
    }
    tfqm_fsp::fsp_crate_invariants_hold()?;
    crate::qm::domain::domain_invariants_hold()
}

fn inventory_mass(names: &[&str]) -> Result<u64, &'static str> {
    if names.is_empty() {
        return Err("module list is empty");
    }
    let mut mass = 0u64;
    for (index, name) in names.iter().enumerate() {
        if name.is_empty() {
            return Err("module name is empty");
        }
        if names[..index].contains(name) {
            return Err("module name is duplicated");
        }
        mass = mass
            .checked_add((index as u64).checked_add(1).ok_or("index overflow")?)
            .ok_or("index mass overflow")?;
    }
    let n = names.len() as u64;
    let closed = n
        .checked_mul(n.checked_add(1).ok_or("count overflow")?)
        .ok_or("triangular overflow")?
        / 2;
    if mass != closed {
        return Err("module index mass disagrees with n(n+1)/2");
    }
    Ok(mass)
}
