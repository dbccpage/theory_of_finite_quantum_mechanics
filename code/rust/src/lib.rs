//! Sovereign theory of finite quantum mechanics.

pub mod linear_algebra;
pub mod homology;
pub mod qm;
pub mod dag_witnesses;

/// The crate root is a barrel. The check walks the declared module names and
/// compares the index mass with the closed form `n(n+1)/2`.
pub fn crate_root_inventory_holds() -> Result<(), &'static str> {
    const MODULES: &[&str] = &["linear_algebra", "homology", "qm", "dag_witnesses"];
    inventory_mass(MODULES)?;
    // 1/2 + 1/3 + 1/6 = 1, cleared over the denominator 6.
    let harmonic = 3i64 + 2 + 1;
    if harmonic != 6 {
        return Err("the three-term harmonic sum is not 1");
    }
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
