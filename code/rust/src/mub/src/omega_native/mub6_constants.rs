//! The MUB(6) curvature-gap constants shared by the cover, chaining, gluing
//! and synthesis modules.
//!
//! Three quantities are primitive: the gap floor ε, the Lipschitz bound L and
//! the mesh step δ. They are read from `fixtures/mub6_constants.json`: the crate
//! derives none of them. The critical step, the erosion and the margin are
//! derived from them rather than restated.
//!
//! AuthorityEffect: None.

use num_rational::BigRational;
use num_traits::ToPrimitive;
use omega_number_theory::rational::rq;

crate::fixture_set!(fixtures, "mub6_constants");

/// Base curvature gap floor ε = 37249 / 90000 (fixture: assumed, not computed).
pub fn base_gap() -> BigRational {
    fixtures().rational("base_gap")
}

/// Uniform Lipschitz bound L = 85 / 9 (fixture: assumed, not computed).
pub fn lipschitz_bound() -> BigRational {
    fixtures().rational("lipschitz_bound")
}

/// Mesh step / excision radius δ = 1 / 1000 (fixture: chosen).
pub fn delta_certified() -> BigRational {
    fixtures().rational("delta_certified")
}

/// Critical mesh step: δ_crit = ε / L = 37249 / 850000.
pub fn delta_crit() -> BigRational {
    base_gap() / lipschitz_bound()
}

/// Erosion over one mesh step: L · δ = 17 / 1800.
pub fn certified_erosion() -> BigRational {
    lipschitz_bound() * delta_certified()
}

/// Margin after one mesh step: ε − L · δ = 12133 / 30000.
pub fn certified_margin() -> BigRational {
    base_gap() - certified_erosion()
}

/// Discrete cycle circulation floor Γ = 6 · certified_margin = 12133 / 5000.
pub fn circulation_gamma() -> BigRational {
    certified_margin() * rq(6, 1)
}

/// Domain volume 1 + 1 + 1 + 1 + 1/1000 + 1 = 5001 / 1000.
pub fn total_domain_volume() -> BigRational {
    fixtures().rational("total_domain_volume")
}

/// Γ on an integer scale: ⌊Γ · scale⌋, for the integer network-simplex circulations.
pub fn circulation_gamma_scaled(scale: i128) -> i128 {
    let gamma = circulation_gamma();
    let numer = gamma.numer().to_i128().expect("circulation gamma numerator fits i128");
    let denom = gamma.denom().to_i128().expect("circulation gamma denominator fits i128");
    (numer * scale).div_euclid(denom)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn derived_constants_match_the_recorded_values() {
        assert_eq!(delta_crit(), rq(37249, 850000));
        assert_eq!(certified_erosion(), rq(17, 1800));
        assert_eq!(certified_margin(), rq(12133, 30000));
        assert_eq!(circulation_gamma(), certified_margin() * rq(6, 1));
        assert_eq!(circulation_gamma(), rq(12133, 5000));
        assert_eq!(circulation_gamma_scaled(30000), 72798);
        assert_eq!(total_domain_volume(), rq(5001, 1000));
        assert!(delta_certified() < delta_crit());
    }
}
