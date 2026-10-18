pub mod cyclotomic_tower;
pub mod finite_spinfoam_model;
pub mod gaussian_rational;
pub mod primitive_difference;
pub mod primitives;
pub mod simplicial_entropy_schedule;

/// Walk the declared domain modules and the algebraic operation each name promises.
pub fn domain_invariants_hold() -> Result<(), &'static str> {
    const NAMES: &[&str] = &[
        "cyclotomic_tower",
        "gaussian_rational",
        "primitive_difference",
        "primitives",
    ];
    let mut mass = 0u64;
    for (index, name) in NAMES.iter().enumerate() {
        if name.is_empty() || NAMES[..index].contains(name) {
            return Err("domain module list is not a set of names");
        }
        mass += (index as u64) + 1;
    }
    let n = NAMES.len() as u64;
    if mass != n * (n + 1) / 2 {
        return Err("domain index mass");
    }
    gaussian_rational::sample_norm_identity()?;
    cyclotomic_tower::prime_relation_vanishes()?;
    primitive_difference::sample_cocycle().map_err(|_| "primitive difference cocycle")?;
    let total = primitives::normalization_two_ways(&[1, 2, 3]).map_err(|_| "normalization")?;
    if total != 6 {
        return Err("weights 1+2+3 are not 6");
    }
    Ok(())
}
