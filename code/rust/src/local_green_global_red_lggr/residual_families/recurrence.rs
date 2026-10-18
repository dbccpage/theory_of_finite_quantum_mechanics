//! Registry-exercise accounting.
//!
//! [`registry_hit_recurrence`] counts distinct shape keys with `hits >= 2`.
//! NOT a Phi_1 measurement — the system-wide $\Phi_1$ closure for the
//! packet's $Q^1$ depends on consumer-side wiring (`omega_solvers`,
//! `omega_epk`, `omega_symbol_game` consulting [`crate::residual_families::FamilyRegistry::lookup`]
//! before re-deriving). That wiring is `defer: PD-RF-PHI1-WIRING` -> successor
//! packet `omega_residual_families_wiring_packet.md` (not yet authored).

use crate::residual_families::registry::FamilyRegistry;

/// Number of distinct shape keys in `reg` whose `hits >= 2`.
///
/// Measures **registry exercise** — i.e. how often the lookup surface saw the
/// same shape more than once. NOT a Phi_1 measurement.
///
/// Downstream consumers (solvers / EPK / Symbol Game) closing
/// $\Phi_1$ system-wide would require this module's `lookup` to be CALLED before
/// re-deriving residuals, which is `defer: PD-RF-PHI1-WIRING` and out of scope
/// for the registry crate itself.
#[must_use]
pub fn registry_hit_recurrence(reg: &FamilyRegistry) -> u64 {
    reg.iter_records().filter(|rec| rec.hits >= 2).count() as u64
}
