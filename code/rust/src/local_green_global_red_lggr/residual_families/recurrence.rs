
use crate::residual_families::registry::FamilyRegistry;

#[must_use]
pub fn registry_hit_recurrence(reg: &FamilyRegistry) -> u64 {
    reg.iter_records().filter(|rec| rec.hits >= 2).count() as u64
}
